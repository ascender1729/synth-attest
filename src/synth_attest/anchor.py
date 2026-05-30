"""External witnessed anchor backends (Sprint S-01.3, addresses panel CRITICAL CC-3).

The panel's sharpest technical objection: an in-memory or provider-held anchor is NOT
tamper-evident against the audited provider itself - the provider can restart, reorder, and
re-anchor a consistent-but-false history. Tamper-evidence requires an EXTERNAL append-only
witness the provider cannot rewrite.

This module provides a small AnchorSink interface with two implementations:
  - InMemoryAnchorSink: the prototype default (NOT tamper-evident against the provider; for tests).
  - S3ObjectLockAnchorSink: writes each batch root to an AWS S3 bucket with Object Lock (WORM).
    In COMPLIANCE mode, even the account root cannot delete or overwrite the object before its
    retention expires - demonstrated live 2026-05-30 (delete returned "AccessDenied because object
    protected by object lock"); see specs/001/S3_ANCHOR_PROOF.md. This is the external witness.

S3 is an OPTIONAL dependency (extras: synth-attest[aws] -> boto3). The core stays dependency-free;
importing this module does not import boto3 until S3ObjectLockAnchorSink is constructed.
"""

from __future__ import annotations

import abc
import json
from typing import Optional


class AnchorSink(abc.ABC):
    """Where a batch root commitment is witnessed. Append-only by contract."""

    name = "abstract"

    @abc.abstractmethod
    def put_root(self, batch_id: str, root_hex: str) -> dict:
        """Persist a batch root. Returns a receipt dict (backend-specific)."""

    @abc.abstractmethod
    def get_root(self, batch_id: str) -> Optional[str]:
        """Read back a previously witnessed root, or None."""


class InMemoryAnchorSink(AnchorSink):
    """Prototype default. NOT tamper-evident against the provider (mutable, non-durable).
    Use only for tests and local demos; production must use an external witness."""

    name = "memory"

    def __init__(self):
        self._roots: dict[str, str] = {}

    def put_root(self, batch_id, root_hex):
        # honest: this CAN be overwritten - that is exactly the weakness S3ObjectLock fixes
        self._roots[batch_id] = root_hex
        return {"sink": self.name, "batch_id": batch_id, "immutable": False}

    def get_root(self, batch_id):
        return self._roots.get(batch_id)


class S3ObjectLockAnchorSink(AnchorSink):
    """External witness: AWS S3 with Object Lock (WORM). With COMPLIANCE-mode retention the object
    version cannot be deleted or overwritten before retention expires, by anyone including the
    account root. Roots are written under anchors/<batch_id>.root.

    Requires boto3 (synth-attest[aws]) and an S3 bucket that already has Object Lock enabled with a
    default retention rule. This sink never creates or configures the bucket (that is an operator,
    infra-as-code concern); it only writes/reads roots, so it holds no destructive permission."""

    name = "s3-object-lock"

    def __init__(self, bucket: str, prefix: str = "anchors/", client=None):
        self.bucket = bucket
        self.prefix = prefix.rstrip("/") + "/"
        if client is None:
            import boto3  # optional dep; imported lazily
            client = boto3.client("s3")
        self._s3 = client

    def _key(self, batch_id: str) -> str:
        return f"{self.prefix}{batch_id}.root"

    def put_root(self, batch_id, root_hex):
        body = json.dumps({"batch_id": batch_id, "root": root_hex}).encode()
        resp = self._s3.put_object(Bucket=self.bucket, Key=self._key(batch_id), Body=body)
        retain = resp.get("ObjectLockRetainUntilDate")
        return {
            "sink": self.name,
            "batch_id": batch_id,
            "bucket": self.bucket,
            "key": self._key(batch_id),
            "version_id": resp.get("VersionId"),
            "object_lock_mode": resp.get("ObjectLockMode"),
            "retain_until": str(retain) if retain else None,
            "immutable": resp.get("ObjectLockMode") in ("GOVERNANCE", "COMPLIANCE"),
        }

    def get_root(self, batch_id):
        try:
            obj = self._s3.get_object(Bucket=self.bucket, Key=self._key(batch_id))
        except Exception:
            return None
        payload = json.loads(obj["Body"].read().decode())
        return payload.get("root")
