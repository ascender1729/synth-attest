"""End-to-end flow (US6): identity -> provider exemption -> mock screen -> opaque verdict ->
tamper-evident audit -> external witness anchor -> customer receipt.

Run:
  python demo/end_to_end.py                       # stub engine, in-memory anchor
  python demo/end_to_end.py --engine attestix     # attestix backend (rc3 dev tree)
  python demo/end_to_end.py --anchor s3 --bucket NAME   # witness the batch root to AWS S3 WORM

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
from synth_attest.anchor import InMemoryAnchorSink, S3ObjectLockAnchorSink


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", choices=["attestix", "stub"], default="stub")
    ap.add_argument("--anchor", choices=["memory", "s3"], default="memory")
    ap.add_argument("--bucket", default=None, help="S3 bucket (Object Lock enabled) for --anchor s3")
    args = ap.parse_args()

    engine = AttestixEngine() if args.engine == "attestix" else StubEngine(allow_insecure_default=True)
    print(f"engine = {engine.name}")

    # 1. Identity: a registry/issuer issues a portable researcher identity credential.
    issuer = engine.create_did()       # an accredited identity issuer (trust-root, see GOVERNANCE.md)
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

    # 4. Tamper-evident audit record + batch root, then WITNESS the root to an external append-only sink.
    rec = to_audit_record(result, customer_did=customer, provider_did=provider)
    root = anchor_batch([rec])
    if args.anchor == "s3":
        if not args.bucket:
            sys.exit("--anchor s3 requires --bucket NAME (an Object-Lock-enabled bucket)")
        sink = S3ObjectLockAnchorSink(bucket=args.bucket)
    else:
        sink = InMemoryAnchorSink()
    receipt = sink.put_root("batch-0001", root)
    print(f"4. batch root {root[:16]}... witnessed via {sink.name} (immutable={receipt['immutable']})")
    print("   read-back matches:", sink.get_root("batch-0001") == root)

    # 5. Customer receipt: never reveals the verdict (anti-evasion).
    print("5. customer receipt:", customer_receipt(rec))
    print("\nflow OK")


if __name__ == "__main__":
    main()
