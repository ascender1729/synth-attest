"""synth-attest: an open, vendor-neutral identity + exemption attestation layer on top of
DNA-synthesis screening. See specs/001/spec.md. A swappable CredentialEngine keeps the core free
of any proprietary dependency; attestix is one optional backend (FR-009)."""

from .engine import CredentialEngine, AttestixEngine, StubEngine
from .schemas import (
    researcher_identity_claims,
    exemption_claims,
    assert_no_sequence,
    InfohazardError,
)

__all__ = [
    "CredentialEngine",
    "AttestixEngine",
    "StubEngine",
    "researcher_identity_claims",
    "exemption_claims",
    "assert_no_sequence",
    "InfohazardError",
]
