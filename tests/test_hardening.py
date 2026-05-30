"""Hardening / failure-mode tests added after the 2026-05-30 architecture audit. They lock in the
fixes for: infohazard-guard bypasses, custody pseudonymization, commitment domain separation, and
malformed-input handling."""

import pytest

from synth_attest.schemas import assert_no_sequence, InfohazardError, _canonical
from synth_attest.audit import OrderAuditRecord
from synth_attest.custody import CustodialRegistry, _handle
from synth_attest.engine import StubEngine


# --- infohazard guard: previously-bypassable obfuscations must now be caught ---

@pytest.mark.parametrize("payload", [
    "ATCGATCGATCGATCGATCGATCG",                       # plain
    "atcgatcgatcgatcgatcgatcg",                       # lowercase
    "ATCG ATCG ATCG ATCG ATCG ATCG",                  # spaced
    "ATCG\tATCG\tATCG\tATCG\tATCG\tATCG",             # tabbed
    "ATCG-ATCG-ATCG-ATCG-ATCG-ATCG",                  # hyphen-separated
    ">seq1 description\nATCGATCGATCGATCGATCGATCG",     # FASTA header + newline
    "a.t.c.g.a.t.c.g.a.t.c.g.a.t.c.g.a.t.c.g.a.t.c.g",  # punctuation gaps
])
def test_guard_catches_obfuscated_sequences(payload):
    with pytest.raises(InfohazardError):
        assert_no_sequence({"field": payload})


def test_guard_allows_normal_text():
    # ordinary metadata must not trip the guard
    assert_no_sequence({"institution": "Cattic Cat Lab", "note": "order placed"})  # short, no long run


def test_canonical_strips_separators():
    assert _canonical(">h\nA T-C.g\tA") == "ATCGA"


# --- custody: handle is pseudonymous and registry-secret-dependent ---

def test_handle_depends_on_secret():
    h1 = _handle("ada@example.edu", b"secret-one")
    h2 = _handle("ada@example.edu", b"secret-two")
    assert h1 != h2  # different registries cannot cross-link the same email


def test_registry_does_not_store_raw_email():
    reg = CustodialRegistry(engine=StubEngine())
    h = reg.enroll_customer("secret.person@example.edu")
    assert "secret.person@example.edu" not in reg._dids
    assert h.startswith("cust_")


# --- audit commitment: domain separation prevents field-boundary collisions ---

def test_commitment_domain_separation():
    a = OrderAuditRecord("ab", "didc", "didp", "cleared", "securedna", salt="s")
    b = OrderAuditRecord("a", "bdidc", "didp", "cleared", "securedna", salt="s")
    # same concatenation ("ab"+"didc" vs "a"+"bdidc") must NOT collide
    assert a.commitment() != b.commitment()


def test_commitment_stable_for_same_input():
    a = OrderAuditRecord("o1", "didc", "didp", "cleared", "securedna", salt="fixed")
    b = OrderAuditRecord("o1", "didc", "didp", "cleared", "securedna", salt="fixed")
    assert a.commitment() == b.commitment()


# --- malformed input ---

def test_unknown_verdict_rejected():
    with pytest.raises(ValueError):
        OrderAuditRecord("o1", "didc", "didp", "definitely-fine", "securedna")
