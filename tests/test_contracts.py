"""Engine contract tests, parametrized over StubEngine and AttestixEngine.

StubEngine is the authoritative contract (SC-005: the layer is not locked to Attestix).
AttestixEngine runs the same contract against the real backend; if a behavior is not yet
supported by attestix 0.4.x, the failure is a real, reported engineering gap, not hidden."""

import copy

import pytest

from synth_attest.engine import AttestixEngine, StubEngine
from synth_attest.schemas import researcher_identity_claims, exemption_claims


@pytest.fixture(params=[StubEngine, AttestixEngine], ids=lambda e: e.name)
def engine(request):
    try:
        return request.param()
    except Exception as e:  # pragma: no cover - backend unavailable
        pytest.skip(f"{request.param.__name__} unavailable: {e}")


def _identity(engine):
    iss = engine.create_did()
    sub = engine.create_did()
    assert iss and sub, "create_did returned empty"
    claims = researcher_identity_claims(
        full_name="Dr Ada Researcher", institution="Example University",
        ror_id="https://ror.org/01abc23de", orcid="0000-0002-1825-0097",
    )
    return iss, sub, engine.issue(
        issuer_did=iss, subject_did=sub, claims=claims,
        credential_type="ResearcherIdentityCredential",
    )


def test_issue_and_verify_identity(engine):
    _, _, cred = _identity(engine)
    assert engine.verify(cred) is True


def test_tamper_is_rejected(engine):
    _, _, cred = _identity(engine)
    tampered = copy.deepcopy(cred)
    subj = tampered.get("credentialSubject") or tampered.get("claims") or tampered
    if isinstance(subj, dict):
        subj["institution"] = "Evil Front Company"
    assert engine.verify(tampered) is False


def test_revocation_invalidates(engine):
    iss, _, cred = _identity(engine)
    cid = engine.cred_id(cred)
    assert cid, "no credential id"
    assert engine.verify(cred) is True
    engine.revoke(credential_id=cid, issuer_did=iss)
    assert engine.verify(cred) is False


def test_provider_exemption_issue_verify(engine):
    provider = engine.create_did()
    customer = engine.create_did()
    claims = exemption_claims(
        customer_did=customer, sequence_class="igsc-flagged:teaching-exempt",
        provider="Example Synthesis Inc", valid_until="2026-12-31",
        order_ref="ord-1001",
    )
    cred = engine.issue(
        issuer_did=provider, subject_did=customer, claims=claims,
        credential_type="ExemptionCredential",
    )
    assert engine.verify(cred) is True
