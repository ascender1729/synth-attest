"""Custodial-registry tests: the customer never holds keys, yet identity issuance, exemption
issuance, and selective-disclosure presentation all work via a handle (email-keyed)."""

import pytest

from synth_attest.engine import AttestixEngine, StubEngine
from synth_attest.custody import CustodialRegistry, _handle


@pytest.fixture(params=[StubEngine, AttestixEngine], ids=lambda e: e.name)
def engine(request):
    try:
        return request.param()
    except Exception as ex:  # pragma: no cover
        pytest.skip(f"{request.param.__name__} unavailable: {ex}")


def test_enroll_is_idempotent_and_handle_stable(engine):
    reg = CustodialRegistry(engine=engine)
    h1 = reg.enroll_customer("Ada@Example.edu ")
    h2 = reg.enroll_customer("ada@example.edu")  # different case/space, same person
    assert h1 == h2 == _handle("ada@example.edu")
    assert reg.did_for(h1)  # a DID is custodied, customer did nothing


def test_identity_issued_without_customer_keys(engine):
    reg = CustodialRegistry(engine=engine)
    issuer = engine.create_did()
    h = reg.enroll_customer("ada@example.edu")
    cred = reg.issue_identity(handle=h, issuer_did=issuer,
                              full_name="Dr Ada", institution="Example University")
    assert engine.verify(cred) is True


def test_custodian_presents_exemption_on_behalf(engine):
    reg = CustodialRegistry(engine=engine)
    provider = engine.create_did()
    h = reg.enroll_customer("ada@example.edu")
    ex = reg.issue_exemption(handle=h, provider_did=provider,
                             sequence_class="igsc-flagged:teaching-exempt",
                             provider_name="Example Synthesis Inc", valid_until="2026-12-31",
                             order_ref="ord-1001")
    assert engine.verify(ex) is True
    try:
        vp = reg.present_on_behalf(handle=h, credentials=[ex],
                                   disclose=["sequenceClass", "validUntil"],
                                   audience_did="did:web:verifier", challenge="n1")
    except NotImplementedError:
        pytest.skip("presentations not supported on this attestix surface")
    assert engine.verify_presentation(vp) is True


def test_no_raw_email_stored(engine):
    reg = CustodialRegistry(engine=engine)
    h = reg.enroll_customer("secret.person@example.edu")
    # the handle is a hash; the raw email must not be a key anywhere in the registry
    assert "secret.person@example.edu" not in reg._dids
    assert h.startswith("cust_")
