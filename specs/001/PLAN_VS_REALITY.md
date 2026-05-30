# Plan vs Reality: how synth-attest diverged from the original action plan (2026-05-30)

This records what we planned months ago, what we actually built, and every place the plan
CHANGED under contact with evidence. Honesty discipline: this is the audit trail of our own
course corrections, not a success-only narrative.

## Origin
- Idea origin: a BlueDot #focus-ai-x-biosec-governance Slack post (2024-09-17, Miti Saksena):
  auditable logs for DNA-synthesis orders are "extremely intuitive, weird it is not being done."
- First artifact: the Mar-2026 "Attestix for Biosecurity" action plan + IEEE 1-pager. A paper,
  zero code, roadmap Phase 1 (Q2 2026) / Phase 2 (Q3-Q4) / Phase 3 (2027).

## What CHANGED from the original plan (and why)

| Original plan (Mar 2026) | Now (2026-05-30) | Why it changed |
|---|---|---|
| "Attestix for Biosecurity" - a VibeTensor commercial product | **synth-attest** - independent, Apache-2.0, personal repo, attestix optional | Funder review: a grant cannot subsidize a for-profit's product. Vendor-neutral is the fundable + defensible posture. |
| Credential = portable "BiosafetyClearanceCredential" with BDL tiers | Split: portable **ResearcherIdentityCredential** (identity only) + provider-local **ExemptionCredential**; **BDL dropped** | Domain expert refuted BDL (it tiers DATA not clearance) and the person-vs-order conflation (clearance can't be portable; provider keeps liability). |
| Zero-knowledge clearance proofs | **Selective-disclosure** presentation; ZK marked future research | Adversary: attestix rc2 does selective disclosure, not ZK range proofs. Honesty over overclaim. |
| Tamper-evident public anchoring | **Salted-hash, fixed-size-batch** anchoring; verdict off customer path | BlueDot+adversary: naive anchoring leaks order volume/timing/verdict (itself an infohazard). |
| "Defense layer that reduces pandemic risk" | One honest kill-chain node: **fraud/attribution/deterrence**, explicitly NOT prevention | BlueDot: identity != intent; a credentialed insider isn't stopped. Overclaim would fail review. |
| Build on attestix (assumed API) | Swappable **CredentialEngine**; StubEngine default (zero deps); attestix one backend | Funder lock-in concern + the real attestix rc2 API differs from the rc3 dev tree. |
| "pip install attestix==0.4.0rc2" as the foundation | attestix IS on PyPI (rc2 latest); rc2 public surface = service layer (MCP tools), differs from rc3 dev tree functional API | Verified live: corrected an earlier "not on PyPI" misread; engine auto-detects both surfaces. |

## What stayed TRUE to the plan
- Sits ON TOP of screening, never replaces it (Principle I) - held throughout.
- W3C DID/VC as the identity standard - held.
- Tamper-evident audit as a core pillar - held (hardened, not dropped).
- Roadmap phasing (identity -> exemption -> audit -> disclosure -> demo) - delivered in order.

## Plan vs reality: delivery status
| Planned capability | Status |
|---|---|
| Researcher identity credential | DONE (issue/verify/revoke/tamper-detect) |
| Provider exemption credential | DONE |
| Tamper-evident order audit | DONE (salted-hash batch, privacy-tested) |
| Screening adapters (SecureDNA, IBBIS) | DONE (mock-backed, contract-correct) |
| Selective-disclosure proof | DONE |
| Customer custody (no-wallet) | DONE |
| Regulatory mapping (machine-checked) | DONE |
| End-to-end demo | DONE |
| CI source-blind on published rc2 | DONE (green) |
| Technical paper | DONE (paper/synth-attest.pdf) |
| Issuer trust-root design | OPEN (principal architectural question) |
| Live provider integration | NOT STARTED (future) |
| Throughput/anchor-cost benchmark | NOT STARTED (next) |

## Net assessment
The plan changed substantially and for good reasons: every change was forced by a verified
finding (web fact-check, persona review, or the real attestix API), not by drift. The direction
held (identity + audit layer on top of screening, W3C standards); the framing got more honest
(independent/open, narrower scope, no overclaim) and the architecture got more defensible
(vendor-neutral, privacy-hardened). We are aligned with the *intent* of the original plan and
deliberately divergent from its *overclaims*.
