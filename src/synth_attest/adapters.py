"""Screening-result adapters (US3 / FR-008). The verdict crosses the boundary as an OPAQUE token
only; raw sequences in the provider's screening payload are NEVER carried into the audit layer.

Mock-backed but contract-correct: a real SecureDNA / IBBIS Common Mechanism integration is a
config swap. Shapes are modeled on the domain-expert-verified description of each system."""

from __future__ import annotations

from dataclasses import dataclass

from .audit import OrderAuditRecord


@dataclass
class ScreeningResult:
    verdict: str          # opaque: cleared | flagged | tier-review
    source: str           # securedna | ibbis-common-mechanism
    order_ref: str


def from_securedna(payload: dict) -> ScreeningResult:
    """SecureDNA-shaped result. Real shape carries hits and exemption tokens; we read ONLY the
    decision, never the sequence. payload e.g.:
        {"order_ref": "...", "hits": [..], "exemptions": [..]}
    """
    order_ref = payload.get("order_ref", "")
    hits = payload.get("hits") or []
    exemptions = payload.get("exemptions") or []
    if hits and not exemptions:
        verdict = "flagged"
    elif hits and exemptions:
        verdict = "tier-review"
    else:
        verdict = "cleared"
    return ScreeningResult(verdict=verdict, source="securedna", order_ref=order_ref)


def from_ibbis(payload: dict) -> ScreeningResult:
    """IBBIS Common Mechanism-shaped result. payload e.g.:
        {"order_ref": "...", "decision": "no_hit" | "hit" | "needs_review"}
    """
    order_ref = payload.get("order_ref", "")
    decision = (payload.get("decision") or "").lower()
    verdict = {"no_hit": "cleared", "hit": "flagged", "needs_review": "tier-review"}.get(
        decision, "tier-review"
    )
    return ScreeningResult(verdict=verdict, source="ibbis-common-mechanism", order_ref=order_ref)


def to_audit_record(result: ScreeningResult, *, customer_did: str, provider_did: str) -> OrderAuditRecord:
    """Build the order-audit record from an opaque screening result. The OrderAuditRecord
    constructor runs the infohazard guard, so any sequence leaking through would raise."""
    return OrderAuditRecord(
        order_id=result.order_ref,
        customer_did=customer_did,
        provider_did=provider_did,
        verdict=result.verdict,
        screening_source=result.source,
    )
