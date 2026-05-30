# Proof of Concept (2026-05-30): end-to-end flow with a real external-witness anchor

This is the demonstrable PoC for the BlueDot Rapid Grant ask. It runs the full synth-attest order
flow on a dependency-free engine and witnesses the tamper-evident audit root to AWS S3 Object Lock
(WORM), proving the panel's #1 critical (CC-3, external witness) end to end, not just in isolation.

## Command
    pip install -e ".[aws]"
    python demo/end_to_end.py --engine stub --anchor s3 --bucket <object-lock-bucket>

## Live output (real AWS, account 320524884470, us-east-1, 2026-05-30)
    engine = stub
    1. identity VC verifies: True
    2. exemption VC verifies: True
    3. screening verdict (opaque): tier-review
    4. batch root 47828ef5... witnessed via s3-object-lock (immutable=True)
       read-back matches: True
    5. customer receipt: {'orderId': 'ord-1001', 'status': 'recorded'}
    flow OK

Then, attempting to delete the witnessed root version:
    aws s3api delete-object --bucket <b> --key anchors/batch-0001.root --version-id <v>
    -> An error occurred (AccessDenied) when calling the DeleteObject operation:
       Access Denied because object protected by object lock.

That delete-denial IS the CC-3 property, demonstrated against the live object the flow just wrote.

## What each line proves
1. Portable W3C researcher-identity credential issued + verified (US1).
2. Provider-issued, revocable exemption credential for a sequence CLASS (US2); clearance stays local.
3. External screening result mapped to an OPAQUE verdict; no sequence enters the layer (US3, FR-005/6).
4. Tamper-evident audit root WITNESSED to S3 Object Lock with immutable=True - the provider cannot
   delete or rewrite it before retention expires (CC-3 closed for durability+WORM). Read-back matched.
5. Customer receipt carries no verdict (anti-evasion, FR-006).

## Honest scope of this PoC
- Proves durability + WORM external witnessing, NOT full RFC-6962 non-equivocation (signed-tree-head
  is future work). See S3_ANCHOR_PROOF.md.
- Ran with GOVERNANCE-mode retention (cleanable test); production uses COMPLIANCE mode.
- Ran on the operator's existing AWS account as a capability proof; an independent account is
  preferable for the project long-term.
- StubEngine is symmetric-integrity reference, not production VC authenticity (it now refuses its
  insecure default unless explicitly opted in).

## Reproducibility
Suite: 46 passed / 10 skipped (core, no proprietary deps) and full pass with the optional attestix
backend, CI green on Python 3.11 + 3.12. The S3 sink is unit-tested against a fake WORM client so CI
needs no AWS credentials; this PoC is the live confirmation of that contract.
