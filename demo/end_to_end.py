"""End-to-end flow (US6): identity -> provider exemption -> mock screen -> opaque verdict ->
anchored audit -> customer receipt. Run: python demo/end_to_end.py [--engine attestix|stub]

This is the flow every persona is walked through in USER_FLOW.md."""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from synth_attest.engine import AttestixEngine, StubEngine
from synth_attest.schemas import researcher_identity_claims, exemption_claims
from synth_attest.adapters import from_securedna, to_audit_record
from synth_attest.audit import anchor_batch, customer_receipt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", choices=["attestix", "stub"], default="attestix")
    args = ap.parse_args()
    engine = AttestixEngine() if args.engine == "attestix" else StubEngine()
    print(f"engine = {engine.name}")

    # 1. Identity: a registry/issuer issues a portable researcher identity credential.
    issuer = engine.create_did()       # an accredited identity issuer (trust-root, see T030)
    customer = engine.create_did()     # the researcher
    id_vc = engine.issue(
        issuer_did=issuer, subject_did=customer,
        claims=researcher_identity_claims(
            full_name="Dr Ada Researcher", institution="Example University",
            ror_id="https://ror.org/01abc23de", orcid="0000-0002-1825-0097"),
        credential_type="ResearcherIdentityCredential")
    print("1. identity VC verifies:", engine.verify(id_vc))

    # 2. Provider verifies identity, then issues its OWN exemption (clearance stays provider-local).
    provider = engine.create_did()
    ex_vc = engine.issue(
        issuer_did=provider, subject_did=customer,
        claims=exemption_claims(
            customer_did=customer, sequence_class="igsc-flagged:teaching-exempt",
            provider="Example Synthesis Inc", valid_until="2026-12-31", order_ref="ord-1001"),
        credential_type="ExemptionCredential")
    print("2. exemption VC verifies:", engine.verify(ex_vc))

    # 3. Screening runs externally; adapter maps the result to an OPAQUE verdict (no sequence).
    screening_payload = {"order_ref": "ord-1001", "hits": ["match"], "exemptions": ["e1"],
                         "raw_sequence": "ATCGATCGATCGATCGATCGATCG"}  # sequence present in input
    result = from_securedna(screening_payload)
    print("3. screening verdict (opaque):", result.verdict)

    # 4. Tamper-evident audit record + privacy-preserving batch anchor.
    rec = to_audit_record(result, customer_did=customer, provider_did=provider)
    root = anchor_batch([rec])
    print("4. anchored batch root:", root[:24] + "...")

    # 5. Customer receipt: never reveals the verdict (anti-evasion).
    print("5. customer receipt:", customer_receipt(rec))
    print("\nflow OK")


if __name__ == "__main__":
    main()
