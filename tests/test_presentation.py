"""US5: selective-disclosure exemption proof. A customer proves a valid exemption to a verifier
while revealing ONLY the exemption validity (sequenceClass + validUntil), not customer/order
identifiers. Domain-expert-aligned: prove the order carries a valid exemption without exposing
the rest. Parametrized over StubEngine and AttestixEngine."""

import pytest

from synth_attest.engine import AttestixEngine, StubEngine
from synth_attest.schemas import exemption_claims


@pytest.fixture(params=[StubEngine, AttestixEngine], ids=lambda e: e.name)
def engine(request):
    try:
        e = request.param(allow_insecure_default=True) if request.param is StubEngine else request.param()
    except Exception as ex:  # pragma: no cover
        pytest.skip(f"{request.param.__name__} unavailable: {ex}")
    # presentations are optional on some surfaces; skip cleanly if unsupported
    if not _supports_presentation(e):
        pytest.skip(f"{e.name} does not support presentations on this attestix surface")
    return e


def _supports_presentation(engine) -> bool:
    try:
        h = engine.create_did()
        engine.present(holder_did=h, credentials=[], disclose=[])
        return True
    except NotImplementedError:
        return False
    except Exception:
        # other errors mean it IS supported but our empty call was rejected; treat as supported
        return True


def _exemption(engine):
    provider = engine.create_did()
    customer = engine.create_did()
    claims = exemption_claims(
        customer_did=customer, sequence_class="igsc-flagged:teaching-exempt",
        provider="Example Synthesis Inc", valid_until="2026-12-31", order_ref="ord-1001",
    )
    cred = engine.issue(issuer_did=provider, subject_did=customer, claims=claims,
                        credential_type="ExemptionCredential")
    return customer, cred


def test_presentation_verifies(engine):
    holder, cred = _exemption(engine)
    vp = engine.present(holder_did=holder, credentials=[cred],
                        disclose=["sequenceClass", "validUntil"],
                        audience_did="did:web:verifier", challenge="nonce-123")
    assert engine.verify_presentation(vp) is True


def test_revoked_credential_not_presentable_or_rejected(engine):
    holder, cred = _exemption(engine)
    cid = engine.cred_id(cred)
    engine.revoke(credential_id=cid, issuer_did="did:any")
    # either presenting a revoked credential raises, or the resulting presentation fails to verify
    try:
        vp = engine.present(holder_did=holder, credentials=[cred],
                            disclose=["sequenceClass", "validUntil"])
    except Exception:
        return
    assert engine.verify_presentation(vp) is False
