"""Credential claim builders + the infohazard sequence guard (FR-005, Constitution Principle IV).

Two distinct credentials, per the domain-expert review (REVIEW_FINDINGS.md): a PORTABLE
identity credential (KYC/affiliation only, NOT a clearance) and a PROVIDER-ISSUED exemption
credential (authorizes a sequence CLASS for a specific order context, time-bound, revocable),
modeled on SecureDNA's Exemption Certification System. No credential carries a raw sequence."""

from __future__ import annotations

import re
import unicodedata

# Infohazard guard (FR-005). Hardened after the 2026-05-30 architecture audit, which showed the
# original (strip spaces/newlines only) was trivially bypassable via tabs, FASTA headers, mixed
# case, or punctuation gaps. We now NFKC-normalize, uppercase, and strip ALL non-letter
# characters before scanning, so "a t c g..." / "ATCG-ATCG..." / FASTA-wrapped runs are caught.
# Deliberately conservative: errs toward false positives, the safe direction for an infohazard
# boundary. This is a defence-in-depth heuristic, not a proof; sequence data must never be sent
# to this layer in the first place.
MIN_RUN = 20
_SEQ = re.compile(r"[ACGTU]{%d,}" % MIN_RUN)
_NON_LETTER = re.compile(r"[^A-Za-z]+")


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


def _canonical(s: str) -> str:
    """NFKC-normalize, drop every non-letter character, uppercase. Collapses whitespace, tabs,
    FASTA headers, hyphens, and other separators so an obfuscated run is still detected."""
    s = unicodedata.normalize("NFKC", s)
    return _NON_LETTER.sub("", s).upper()


def assert_no_sequence(payload) -> None:
    """Raise InfohazardError if any string anywhere in payload looks like a nucleotide run, after
    canonicalization (FR-005). Defence-in-depth: callers must never pass sequence data at all."""
    for s in _iter_strings(payload):
        if _SEQ.search(_canonical(s)):
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
