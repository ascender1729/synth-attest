"""Privacy-preserving, tamper-evident order audit (US4 / FR-005, FR-006).

Resolves the Principle III (tamper-evidence) vs Principle IV (no metadata leakage) tension the
adversary review flagged:
  - The provider keeps the full OrderAuditRecord locally.
  - Only a SALTED HASH commitment is anchored, and commitments are anchored in FIXED-SIZE padded
    batches so per-order volume/timing is not recoverable from the anchor (SC-004).
  - The customer-facing receipt NEVER contains the screening verdict (anti-evasion, FR-006).
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass, field
from typing import Optional

from .schemas import assert_no_sequence

# Opaque verdict tokens that may cross the screening boundary. "flagged" must never reach the
# customer path (see customer_receipt).
OPAQUE_VERDICTS = ("cleared", "flagged", "tier-review")

BATCH_SIZE = 16  # commitments per anchored batch; orders are padded up to hide true volume


@dataclass
class OrderAuditRecord:
    order_id: str
    customer_did: str
    provider_did: str
    verdict: str
    screening_source: str
    salt: str = field(default_factory=lambda: os.urandom(16).hex())

    def __post_init__(self):
        if self.verdict not in OPAQUE_VERDICTS:
            raise ValueError(f"verdict must be one of {OPAQUE_VERDICTS}, got {self.verdict!r}")
        # Infohazard guard: no sequence-like data anywhere in the record (FR-005).
        assert_no_sequence({
            "order_id": self.order_id,
            "customer_did": self.customer_did,
            "provider_did": self.provider_did,
            "verdict": self.verdict,
            "screening_source": self.screening_source,
        })

    def commitment(self) -> str:
        """Salted hash hiding order_id + verdict. Salt stays provider-private and is NOT anchored,
        so the verdict bit is not recoverable from the anchor (resolves the verdict-oracle risk)."""
        h = hashlib.sha256()
        h.update(self.salt.encode())
        h.update(self.order_id.encode())
        h.update(self.verdict.encode())
        h.update(self.customer_did.encode())
        return h.hexdigest()


def customer_receipt(record: OrderAuditRecord) -> dict:
    """What the customer is allowed to see. NEVER the verdict (FR-006 anti-evasion)."""
    return {"orderId": record.order_id, "status": "recorded"}


def anchor_batch(records: list[OrderAuditRecord], batch_size: int = BATCH_SIZE) -> str:
    """Anchor commitments as a single root over a FIXED-SIZE batch. Real orders are padded with
    indistinguishable filler commitments so the count within a batch (and thus order volume) is
    not recoverable from what is anchored (SC-004). Returns the batch root only."""
    commits = [r.commitment() for r in records[:batch_size]]
    # pad to fixed size with random commitments indistinguishable from real ones
    while len(commits) < batch_size:
        commits.append(hashlib.sha256(os.urandom(32)).hexdigest())
    commits.sort()  # order within batch carries no information
    root = hashlib.sha256()
    for c in commits:
        root.update(bytes.fromhex(c))
    return root.hexdigest()
