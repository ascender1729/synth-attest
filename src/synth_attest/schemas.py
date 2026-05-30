"""Credential claim builders + the infohazard sequence guard (FR-005, Constitution Principle IV).

Two distinct credentials, per the domain-expert review (REVIEW_FINDINGS.md): a PORTABLE
identity credential (KYC/affiliation only, NOT a clearance) and a PROVIDER-ISSUED exemption
credential (authorizes a sequence CLASS for a specific order context, time-bound, revocable),
modeled on SecureDNA's Exemption Certification System. No credential carries a raw sequence."""

from __future__ import annotations

import re

# Guard definition (was an unspecified comment in the spec; the adversary review flagged it).
# Reject any run of >= MIN_RUN characters drawn only from the nucleotide alphabet (case-
# insensitive), after stripping whitespace. This is deliberately conservative: it errs toward
# false positives, which is the safe direction for an infohazard boundary.
MIN_RUN = 20
_SEQ = re.compile(r"[ACGTU]{%d,}" % MIN_RUN, re.IGNORECASE)


class InfohazardError(ValueError):
    """Raised when a payload contains sequence-like data that must never enter the layer."""


def _iter_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _iter_strings(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from _iter_strings(v)


def assert_no_sequence(payload) -> None:
    """Raise InfohazardError if any string anywhere in payload looks like a nucleotide run."""
    for s in _iter_strings(payload):
        if _SEQ.search(s.replace(" ", "").replace("\n", "")):
            raise InfohazardError("sequence-like data rejected by infohazard guard (FR-005)")


def researcher_identity_claims(*, full_name, institution, ror_id=None, orcid=None):
    """Portable identity + affiliation ONLY. Not a clearance, no tier (BDL dropped). Maps to
    UK DSIT customer-info + EU Biotech Act Art.44 identity requirements (both UNVERIFIED legal
    force, see spec sec 7)."""
    claims = {
        "@type": "ResearcherIdentityCredential",
        "fullName": full_name,
        "institution": institution,
        "credentialPurpose": "identity-affiliation-only",
        "notAClearance": True,
    }
    if ror_id:
        claims["rorId"] = ror_id
    if orcid:
        claims["orcid"] = orcid
    assert_no_sequence(claims)
    return claims


def exemption_claims(*, customer_did, sequence_class, provider, valid_until, order_ref=None):
    """Provider-issued exemption for a sequence CLASS (a label, never a sequence), time-bound and
    revocable. Models SecureDNA ECS semantics: issued by the provider/biosafety authority, scoped,
    expiring. `sequence_class` MUST be a class label (e.g. 'igsc-flagged:teaching-exempt'), not a
    sequence; the guard enforces this."""
    claims = {
        "@type": "ExemptionCredential",
        "customerDid": customer_did,
        "sequenceClass": sequence_class,
        "issuingProvider": provider,
        "validUntil": valid_until,
        "revocable": True,
    }
    if order_ref:
        claims["orderRef"] = order_ref
    assert_no_sequence(claims)
    return claims
