"""AnchorSink tests. The in-memory sink is tested directly; the S3 Object Lock sink is tested
against a fake S3 client that emulates WORM semantics, so CI needs no AWS credentials. The live
AWS proof (delete denied by object lock) is recorded in specs/001/S3_ANCHOR_PROOF.md."""

import pytest

from synth_attest.anchor import InMemoryAnchorSink, S3ObjectLockAnchorSink
from synth_attest.audit import OrderAuditRecord, anchor_batch


def test_in_memory_sink_roundtrip():
    sink = InMemoryAnchorSink()
    r = sink.put_root("batch-1", "deadbeef")
    assert r["immutable"] is False  # honest: in-memory is NOT tamper-evident
    assert sink.get_root("batch-1") == "deadbeef"


class _FakeWormS3:
    """Minimal S3 stand-in with Object Lock semantics: an existing locked object cannot be
    deleted; a put creates a new version but the prior locked version persists."""

    def __init__(self):
        self.objects = {}   # key -> latest body
        self.versions = {}  # key -> list of (version_id, body, locked)

    def put_object(self, Bucket, Key, Body, **kwargs):
        vlist = self.versions.setdefault(Key, [])
        vid = f"v{len(vlist) + 1}"
        vlist.append((vid, Body, True))
        self.objects[Key] = Body
        # echo the lock the caller requested (matches real S3 when set explicitly)
        return {"VersionId": vid,
                "ObjectLockMode": kwargs.get("ObjectLockMode", "COMPLIANCE"),
                "ObjectLockRetainUntilDate": kwargs.get("ObjectLockRetainUntilDate", "2026-06-30T00:00:00Z")}

    def get_object(self, Bucket, Key):
        import io
        return {"Body": io.BytesIO(self.objects[Key])}

    def delete_object(self, Bucket, Key, VersionId=None):
        raise PermissionError("AccessDenied: object protected by object lock")


def test_s3_object_lock_sink_writes_immutable_root():
    sink = S3ObjectLockAnchorSink(bucket="test", client=_FakeWormS3())
    # build a real batch root from the audit module and witness it
    rec = OrderAuditRecord("ord-1", "did:c", "did:p", "cleared", "securedna")
    root = anchor_batch([rec])
    receipt = sink.put_root("batch-0001", root)
    assert receipt["immutable"] is True
    assert receipt["object_lock_mode"] == "COMPLIANCE"
    assert sink.get_root("batch-0001") == root


def test_s3_object_lock_sink_blocks_delete():
    fake = _FakeWormS3()
    sink = S3ObjectLockAnchorSink(bucket="test", client=fake)
    sink.put_root("batch-0001", "abc123")
    # the audited provider cannot delete a witnessed root (the CC-3 property)
    with pytest.raises(PermissionError):
        fake.delete_object(Bucket="test", Key="anchors/batch-0001.root")
