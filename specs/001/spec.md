# Spec 001: Verified-Researcher Identity + Exemption Attestation for DNA-Synthesis Orders

Status: REVISED v2 (post design review 2026-05-30)
Project: synth-attest (independent, Apache-2.0)
Architecture: swappable CredentialEngine; default StubEngine has zero proprietary deps; attestix is one optional backend

## 1. Summary

A portable verified-researcher identity credential plus a privacy-preserving, tamper-evident
attestation of synthesis-order decisions, sitting ON TOP of sequence screening. It lets a
provider (a) accept a portable proof that a customer is a real, verified researcher at a real
institution, (b) issue and check provider-local exemptions modeled on SecureDNA's Exemption
Certification System, and (c) write a verifiable, metadata-minimal record of each order
decision. It does NOT screen sequences and does NOT make the clearance decision portable.

## 2. Threat model and honest scope (kill-chain)

Engineered-pandemic kill chain: capability uplift -> acquire materials -> synthesize ->
weaponize -> release. This layer intervenes at ONE node, ACQUIRE MATERIALS, and ONLY for
actors routing through compliant commercial providers. It addresses FRAUD (identity spoofing),
ATTRIBUTION (who ordered what), and DETERRENCE (raising cost of the legitimate path). It does
NOT address: capability uplift, benchtop/in-house synthesis, non-compliant or overseas
providers, weaponization, or a legitimately-credentialed malicious insider (identity proves
identity, not intent). Any framing as "prevents engineered pandemics" is forbidden
(Principle V). It is one honest layer, not a substitute for benchtop governance or BDT controls.

## 3. Personas served: ICP user, funder, BlueDot, biosecurity domain expert (see REVIEW_FINDINGS.md).

## 4. User scenarios

### US1 (P1) - Portable researcher identity credential
A customer is issued a `ResearcherIdentityCredential` (W3C VC) bound to their DID, asserting a
verified person + institutional affiliation (NOT a clearance). A provider verifies it offline.
Acceptance: DID created (did:key default), VC issued and verifies true; field tampering fails
verification; revoked credential checks as invalid.

### US2 (P1) - Provider-issued exemption credential (SecureDNA-ECS-aligned)
A provider issues an `ExemptionCredential` to a vetted customer authorizing a sequence CLASS
(not a sequence), revocable, time-bound. The provider is issuer-of-record, signs with its own
key. Acceptance: exemption issued, verified, and revoked via attestix revoke_credential; status
check reflects revocation.

### US3 (P1) - Screening-result adapter (the adoption gate)
A thin adapter ingests a screening result in SecureDNA / IBBIS Common Mechanism output shape
and produces a US4 audit entry. Verdict crosses the boundary as an OPAQUE token; the customer
never learns cleared-vs-flagged granularity (anti-evasion). Mock-backed, contract-correct.
Acceptance: sample SecureDNA-shaped payload yields a valid audit entry; no sequence data and no
flagged/cleared leak to the customer path.

### US4 (P1) - Privacy-preserving tamper-evident order audit
Each order decision writes a signed, append-only record and anchors a SALTED HASH only (no
queryable metadata, no per-provider public batch). Third parties verify integrity without
learning order volume/timing. Acceptance: record via log_action; anchored via anchor_audit_batch
(salted-hash commitment); get_audit_trail + verify_anchor valid; FR-005 sequence-guard passes;
no order metadata recoverable from the anchor.

### US5 (P2) - Selective-disclosure exemption proof (ZK is follow-on research)
A customer proves "I hold a valid exemption covering this order class" via a selective-disclosure
Verifiable Presentation (create_verifiable_presentation), revealing nothing else. True
zero-knowledge range proof is UNBUILT RESEARCH, explicitly out of this spec. Acceptance: verifier
accepts the VP without seeing the full credential; revoked exemption is rejected.

### US6 (P3) - End-to-end demo + cross-jurisdiction mapping + declaration
One scripted flow (identity VC -> provider exemption -> mock screen -> opaque verdict -> anchored
audit -> selective-disclosure proof) plus a per-field mapping to S.3741, UK DSIT, ISO 20688-2
(EU Art. 44 marked UNVERIFIED), and an optional regulator-facing declaration of conformity
(create_compliance_profile + record_conformity_assessment + generate_declaration_of_conformity).
Acceptance: one command runs green; each mapped field marked VERIFIED / UNVERIFIED.

## 5. Functional requirements

- FR-001 Issue/verify `ResearcherIdentityCredential` (identity + affiliation only) via
  CredentialEngine (attestix create_did_key + issue_credential + verify_credential).
- FR-002 Issue/verify provider-issued `ExemptionCredential` (sequence-CLASS authorization,
  time-bound), provider as issuer-of-record signing with provider key.
- FR-003 Credential revocation + status check (revoke_credential); short-lived VCs + status
  list to reconcile offline verifiability with prompt revocation.
- FR-004 Schemas as JSON-LD; every field maps to a named clause (S.3741 / UK DSIT / ISO
  20688-2), each marked VERIFIED / UNVERIFIED. No field maps to BDL.
- FR-005 Append-only signed order-audit records; anchor SALTED HASHES only (anchor_audit_batch);
  retrieval (get_audit_trail) + verification (verify_anchor). MUST reject any payload containing
  sequence-like data (infohazard guard) and MUST NOT anchor queryable order metadata.
- FR-006 Opaque verdict token across the screening boundary; customer path never exposes
  cleared/flagged granularity.
- FR-007 Selective-disclosure presentations (create_verifiable_presentation). ZK range proof
  marked UNBUILT RESEARCH (not implemented).
- FR-008 Screening adapter interface + SecureDNA-shaped and IBBIS-Common-Mechanism-shaped
  reference implementations (mock-backed).
- FR-009 Swappable `CredentialEngine` interface so attestix is one backend, not a lock-in.
- FR-010 Degraded mode: order flow does not hard-block if anchoring is unavailable; anchoring
  is async with an integrity-backfill SLA.
- FR-011 Optional compliance profile + declaration of conformity, signed by the provider.

## 6. Non-goals
Sequence screening; generic researcher-data-access identity (GA4GH/ELIXIR/ORCID); storing any
pathogen/BSAT/DURC data; portable CLEARANCE decisions; true ZK proofs in this spec; a
production India RCGM pilot (keep schema RCGM-extensible only).

## 7. Dependencies, assumptions, carry-forward unknowns
- attestix==0.4.0rc2 behind CredentialEngine; verify each named tool exists at this version
  before use (do not assume signatures).
- Screening systems external; opaque verdicts only.
- DROPPED: BDL tier model (refuted; tiers data not clearance).
- UNVERIFIED: EU Biotech Act Art. 44 numbering (Act in draft); IGSC version + Regulated Pathogen
  Database (RPD) naming; ISO 20688-2 exact title. Resolve with source bodies before any external claim.
- Issuer trust-root model is an OPEN DESIGN ITEM (avoid recreating a centralized CA); tracked in tasks.

## 8. Success criteria
- SC-001 Provider verifies a customer identity, issues+checks an exemption, and writes a
  verifiable, metadata-minimal order-audit entry with zero sequence exposure, end to end, one run.
- SC-002 Identity credential verifies on a second machine from the public DID doc (did:key);
  a revoked credential fails on both.
- SC-003 Every credential/audit field traces to a named clause, each VERIFIED/UNVERIFIED.
- SC-004 No order metadata is recoverable from anchored data (privacy test passes).
- SC-005 Swapping the CredentialEngine to a stub backend keeps all contract tests green
  (lock-in disproven).

## 9. Constitution Check
| # | Principle | Status |
|---|---|---|
| I | Layer, never screening | PASS - opaque verdict, FR-005 guard |
| II | W3C standards-first identity | PASS - did:key/VC, FR-003 revocation reconciled |
| III | Tamper-evidence & verifiability | PASS - FR-005 salted-hash anchor (privacy-reconciled with IV) |
| IV | Privacy & infohazard containment | PASS - FR-005/FR-006 no metadata/verdict leak, SC-004 test |
| V | Honesty over marketing | PASS - ZK downgraded (FR-007), unknowns carried, scope narrowed (sec 2) |
| VI | Regulatory traceability | PASS - FR-004 per-clause mapping |
| VII | Build on real Attestix | PASS - FR-009 swappable, tools verified before use |
| VIII | Security & secrets hygiene | PASS - private repo, no secrets/PII |
| IX | Persona-validated before lock | PASS - 5 reviews incorporated (REVIEW_FINDINGS.md); Bedrock 55-persona run is next gate |

## 10. Resolved review questions
1. Portability: portable IDENTITY only; clearance/exemption stays provider-local (liability). RESOLVED.
2. Fundability: open-source neutral layer + swappable engine (FR-009) + ecosystem letters. RESOLVED in tasks.
3. Theory of impact: one honest kill-chain node (fraud/attribution/deterrence), not prevention. RESOLVED sec 2.
4. ZK vs reality: re-modeled to identity + provider exemption (SecureDNA ECS); ZK is research. RESOLVED.
