# Implementation cross-check: how others build it vs how synth-attest builds it (2026-05-30)

Source: 13-agent workflow (run wf_c0b8bd9c), 6 actors deep-read for IMPLEMENTATION (not
marketing), each adversarially verified. The synthesis agent was rate-limited; this doc is
written from the verified per-actor comparisons.

## One-line clarity
synth-attest is the only OPEN-SOURCE system combining W3C decentralized credentials (DID/VC) with
a tamper-evident DNA-synthesis order audit. It is an unshipped prototype; every actor below is
materially ahead on what makes a biosecurity product real (screening, traction, funding).

## Implementation comparison matrix
| Actor | Identity mechanism | Exemption/authz | Audit mechanism | Privacy | Screens? | Open? |
|---|---|---|---|---|---|---|
| Aclid (now Ginkgo) | centralized sanctions/watchlist KYC, no credential | internal flag/adjudication | central cloud logging (ISO 27001) | none disclosed; sequence enters their cloud | YES (own DB + AI-construct detection) | closed |
| SecureDNA ECS | none (verifies orders, not a portable person-cred) | X.509-style PKI exemption tokens, order-specific, screening-coupled | screening-coupled | advanced (privacy-preserving screening protocol) | YES | partial |
| IBBIS Common Mechanism | guidance/forms only (NIST SP 800-63 alignment recommended) | none | none | none | YES (open screening lib) | open (screening) |
| Know Your Scientist | institution-vouching + shared exclusion lists (proposal) | tiered access (proposal) | plain logging (proposal) | none | no (AI-tool access chokepoint) | paper-only |
| GA4GH Passports / ORCID | OAuth2/OIDC JWT (federated) / central researcher ID | n/a | none for synthesis | token-scoped | no | standards |
| **synth-attest** | **W3C VC/DID, portable, decentralized, identity-only** | **machine-verifiable revocable ExemptionCredential, provider issuer-of-record** | **salted SHA-256 commitment, B=16 padded+sorted batches** | **selective disclosure; verdict + intra-batch count hidden** | **no (layers on top, opaque verdicts)** | **Apache-2.0, vendor-neutral** |

## Per-module differentiation (real vs thin)
- IDENTITY: REAL - only one issuing portable W3C VCs. But an architecture difference, NOT
  superiority; Aclid's list-matching does regulatory KYC work our VC alone does not.
- EXEMPTION: REAL but DERIVATIVE - we generalize SecureDNA's ECS into open W3C-VC form. They
  invented it; we re-implement openly. Credit them in the paper (done).
- AUDIT: REAL (code-verified) with a CORRECTED overclaim - salted SHA-256 + B=16 hides the verdict
  and the intra-batch order count, but cross-batch volume/timing STILL LEAKS. Paper + spec now say
  this explicitly; fixed-cadence anchoring is future work.
- DISCLOSURE: REAL - selective disclosure built; true ZK explicitly unbuilt.
- SCREENING BOUNDARY: THIN (reframed) - "no sequence enters" is a consequence of not being a
  screener, i.e. a scope limitation, not a feature.
- OPENNESS: REAL - only Apache-2.0 vendor-neutral implementation.
- CUSTODY: REAL - walletless HMAC(registry-secret, email) handle; nobody else has the concept.

## Where others are ahead (honest)
- Aclid/Ginkgo: real maintained pathogen DB, AI-construct detection (the Paraphrase threat),
  named paying providers (Agilent, Ansa), public-company backing. We have zero users, in-memory.
- SecureDNA: de facto global standard, free, deployed across major synthesizers, peer-reviewed
  crypto, real ECS issuers. We model on them.
- IBBIS: credible NTI-backed neutral standards body; their 2026 identity work could absorb our
  niche. This is the main strategic risk and the reason to establish an open reference now.
- Know Your Scientist: peer-reviewed academic credibility (but proposal, no code).
- GA4GH/ORCID: global-scale deployed identity (but not for synthesis, no order audit).

## Is anyone doing exactly this?
No. Closest two: (1) SecureDNA ECS - but screening-coupled, X.509 not W3C VC, no portable
identity; (2) IBBIS - guidance not software, but plans 2026 identity work.

## Clarity verdict
Differentiation is REAL but NARROW and TIME-SENSITIVE. Defensible: "only open-source decentralized-
credential + tamper-evident-audit implementation, a reference for the layer IBBIS guidance
describes but nobody built openly." NOT defensible: any superiority over Aclid/SecureDNA on
capability, traction, or completeness. Grant framing must be "credible open reference
implementation," never "better than incumbents."

## Actions taken from this cross-check
- Paper audit-privacy claim corrected (verdict + intra-batch count hidden; cross-batch leak
  disclosed) with a labeled forward-reference to Limitations.
- Paper Related Work upgraded: Aclid-as-Ginkgo + first-party screener; SecureDNA credited as ECS
  originator we generalize.
