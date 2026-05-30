"""Order-audit + adapter tests: infohazard guard, anti-evasion receipt, anchor privacy,
and the SecureDNA / IBBIS screening adapters."""

import pytest

from synth_attest.audit import (
    OrderAuditRecord,
    anchor_batch,
    customer_receipt,
)
from synth_attest.adapters import from_securedna, from_ibbis, to_audit_record
from synth_attest.schemas import InfohazardError


def _record(verdict="cleared", order_id="ord-1"):
    return OrderAuditRecord(
        order_id=order_id, customer_did="did:stub:cust", provider_did="did:stub:prov",
        verdict=verdict, screening_source="securedna",
    )


def test_audit_record_accepts_opaque_verdict():
    rec = _record("cleared")
    assert rec.commitment()  # non-empty hex


def test_audit_record_rejects_unknown_verdict():
    with pytest.raises(ValueError):
        _record(verdict="totally-safe-trust-me")


def test_infohazard_guard_rejects_sequence():
    # a nucleotide run sneaking into an id must be rejected (FR-005)
    with pytest.raises(InfohazardError):
        OrderAuditRecord(
            order_id="ATCGATCGATCGATCGATCGATCG", customer_did="did:stub:c",
            provider_did="did:stub:p", verdict="cleared", screening_source="securedna",
        )


def test_customer_receipt_hides_verdict():
    rec = _record("flagged")
    receipt = customer_receipt(rec)
    assert receipt["status"] == "recorded"
    assert "flagged" not in str(receipt).lower()
    assert "verdict" not in receipt


def test_anchor_hides_volume():
    # one real order and ten real orders both produce a fixed-width batch root of equal length;
    # the number of real orders is not recoverable from the anchored root (SC-004)
    root_1 = anchor_batch([_record(order_id="o1")])
    root_10 = anchor_batch([_record(order_id=f"o{i}") for i in range(10)])
    assert len(root_1) == len(root_10) == 64
    assert root_1 != root_10  # different content, same shape


def test_commitment_salt_not_recoverable():
    # two records with identical public fields but different salts produce different commitments,
    # so the commitment does not leak the verdict by lookup
    a = OrderAuditRecord("o1", "did:c", "did:p", "flagged", "securedna")
    b = OrderAuditRecord("o1", "did:c", "did:p", "flagged", "securedna")
    assert a.commitment() != b.commitment()


def test_securedna_adapter_maps_verdicts():
    assert from_securedna({"order_ref": "o1", "hits": [], "exemptions": []}).verdict == "cleared"
    assert from_securedna({"order_ref": "o2", "hits": ["x"], "exemptions": []}).verdict == "flagged"
    assert from_securedna({"order_ref": "o3", "hits": ["x"], "exemptions": ["e"]}).verdict == "tier-review"


def test_ibbis_adapter_maps_verdicts():
    assert from_ibbis({"order_ref": "o1", "decision": "no_hit"}).verdict == "cleared"
    assert from_ibbis({"order_ref": "o2", "decision": "hit"}).verdict == "flagged"


def test_adapter_does_not_carry_sequence_into_audit():
    # provider screening payload may contain a sequence; the adapter must extract only the verdict,
    # so the resulting audit record passes the infohazard guard
    payload = {"order_ref": "o9", "hits": ["match"], "exemptions": [],
               "raw_sequence": "ATCGATCGATCGATCGATCGATCGATCG"}
    result = from_securedna(payload)
    rec = to_audit_record(result, customer_did="did:c", provider_did="did:p")
    assert rec.verdict == "flagged"
