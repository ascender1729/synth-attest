Facts confirmed (zero core deps, attestix==0.4.0rc2 optional, Apache-2.0, version 0.1.0). Writing the consolidated report now.

# synth-attest: Consolidated Multi-Stakeholder Panel Report + BlueDot Rapid Grant Package
Prepared for: Pavan Kumar Dubasi | Date: 2026-05-30 | Repo: github.com/ascender1729/synth-attest (Apache-2.0)

## 1. CONSOLIDATED VERDICT

Average score: 59.4 / 100 across 8 panels. Spread: 43 points (low 38, high 81). Median: 62. Modal verdict: SUPPORT-WITH-FIXES (6 of 8); two WEAK (both end-user/commercial seats: the bench biologist at 38 and the VC/commercial panel at 38).

The split is diagnostic, not contradictory. Every technically-grounded reviewer (academic rigor 77, screening-realist 81, crypto/security 64, adversarial 62, policy-staffer 63, theory-of-impact 66) lands at SUPPORT-WITH-FIXES and praises the same thing: unusual honesty and correct scoping. Both WEAK scores come from the two seats that ask "would I actually USE or FUND this today" and hit the same wall: zero adoption. The engineering and the integrity are not in question; whether anyone in the real synthesis ecosystem wants it before IBBIS ships its 2026 identity work is.

Single sharpest objection (raised, in some form, by 7 of 8 panels and named existential by the project's own IMPLEMENTATION_CROSSCHECK.md): NO ADOPTION SURFACE. There is no documented conversation with IBBIS, SecureDNA, or any IGSC provider; zero letters of interest; live provider integration NOT STARTED. IBBIS's planned 2026 identity work "could absorb our niche." A vendor-neutral open-source reference layer that nobody has agreed to issue or consume is, on current evidence, a parallel reference the community routes around once the trusted convener ships. The one fix every panel converges on: convert the grant deliverable from "more code" into "one documented external touchpoint plus interop mapping," and reposition explicitly as IBBIS's open reference implementation, not a competitor.

## 2. PANEL SCORECARD TABLE

| Panel | Verdict | Score | One thing to change |
|---|---|---|---|
| Academic Rigor Reviewer | SUPPORT-WITH-FIXES | 77 | Make the grant deliverable an interop+pull artifact: documented IBBIS contact + field-level mapping to IGSC Harmonized Screening Protocol v3.0 + >=1 provider/IGSC expression-of-interest, as a falsifiable 3-6 month metric. |
| Screening / infohazard realist | SUPPORT-WITH-FIXES | 81 | Produce one real adoption touchpoint (IBBIS/SecureDNA/IGSC provider) paired with ADOPTION.md (smallest pilot) and GOVERNANCE.md (issuer accreditation, revocation due-process, exclusion safeguards). |
| Commercial / Compliance owner (provider) | SUPPORT-WITH-FIXES | 61 | Specify the issuance root-of-trust and identity-proofing model (who issues, what LoA, how Sybil/self-issuance is prevented; portable credential is INPUT to provider-local KYC, never a substitute). |
| AI-safety / theory-of-impact | SUPPORT-WITH-FIXES | 66 | Replace layer-level value story with one falsifiable theory-of-impact paragraph: the one adversary class affected, the enforcing audit consumer, the residual threat surface after the four bypasses. |
| Policy staffer (enforceability) | SUPPORT-WITH-FIXES | 63 | Bind the audit artifact to a screening attestation (verifier fails closed when none present) AND add a duty-bearer section naming the regulated entity + obligation. |
| Adversarial reject-oriented | SUPPORT-WITH-FIXES | 62 | Resolve deterrence-vs-leak: either reframe headline to "tamper-evident record-keeping for post-hoc attribution," or implement fixed-cadence anchoring (audit.py line 28) and benchmark its leakage bound. |
| Technical (cryptography/security eng.) | SUPPORT-WITH-FIXES | 64 | Anchor batch roots to an external independently-witnessed append-only log (RFC 6962 STH / public ledger / RFC 3161); until provider equivocation is externally detectable it is not "tamper-evident" against the audited party. |
| Bench biologist (end-user) | WEAK | 38 | Land ONE real acceptance: a provider sandbox that consumes the VC, or a university IBC that pilots recognizing it. |
| Company / Commercial (VC + vendor) | WEAK | 38 | Decide in writing: public good or company. Evidence says public good; get one credible biosecurity-governance party to commit on paper to reference/pilot/co-author the spec. |

## 3. CONVERGENT CRITICALS (raised by 3+ panels = must-fix)

CC-1. No adoption surface / no external pull (8 of 8 panels). Zero provider, IGSC, IBBIS, or IBC touchpoint; live integration NOT STARTED; IBBIS 2026 identity work named as existential risk. This is the gating issue.

CC-2. Reposition as IBBIS/IGSC reference implementation, not competitor (theory-of-impact, screening-realist, commercial-owner, policy-staffer, adversarial, company = 6 panels). The win condition is "IBBIS or a provider adopts/cites this," not "this beats IBBIS." Fragmenting a convergence-dependent ecosystem is a net-negative outcome reviewers will reject.

CC-3. Tamper-evidence is not real against the audited party until externally anchored (crypto panel critical, screening-realist, adversarial, commercial-owner, policy-staffer, company = 6 panels). Anchors live in process memory only; a provider can restart/reorder/back-date and re-anchor a consistent-but-false history. In-memory + no durability also nullifies the audit pillar for any real order flow.

CC-4. Theory of impact / adversary-cost not reduced to a falsifiable claim, and the headline must drop "deterrence" toward "attribution" (theory-of-impact critical, academic, adversarial, policy-staffer, company = 5 panels). Name the one adversary class who must transact with compliant providers (credential-fraud / stolen-identity / order-laundering / structuring), the enforcing audit consumer, and the residual surface after the four disclosed bypasses (non-compliant provider, KYC lie, benchtop, insider).

CC-5. Issuance root-of-trust / identity-proofing is unspecified (commercial-owner critical, screening-realist governance, theory-of-impact dual-use, bench-biologist surveillance = 4 panels). A W3C VC is only as strong as the proofing behind issuance. Without an LoA framework (e.g. NIST 800-63 IAL2 / eIDAS substantial) and Sybil/self-issuance controls, portable identity is a forgery factory. The credential is INPUT to provider-local KYC, never a substitute.

CC-6. "Privacy-preserving" headline overclaims the property; rename and bound it (academic, theory-of-impact, commercial-owner, crypto, bench-biologist = 5 panels). Salted SHA-256 + B=16 padded/sorted batches is leakage-bounded hash obfuscation, not ZK and not a hiding commitment. Cross-batch volume/timing leaks. Rename to "tamper-evident, leakage-bounded (hash-based) order audit" where it leads; reserve "privacy-preserving" for qualified contexts; add an explicit audit-channel adversary model with leakage function L = {batch_count, batch_timing, padded_size}.

CC-7. Audit-channel value depends on an enforcing consumer who can act (theory-of-impact critical, policy-staffer = 2 panels, plus governance-adjacent in 2 more). A tamper-evident log nobody reads is paperwork. Name the consumer (provider compliance, IGSC body, regulator, consortium) and the action they can take, or downgrade "deterrence" to "after-the-fact attribution conditional on an investigator existing."

## 4. STRONGEST POINTS (what to lead the grant with)

These are where panels independently agreed the project is strong. Lead the grant with the first three.

S-1. Threat-model honesty is load-bearing, not decorative (all 8 panels). "Sits on top of screening, never replaces it"; one node only (acquire-materials, compliant providers); explicitly NOT screening, NOT benchtop, NOT non-compliant, NOT insider, NOT capability uplift. "Identity proves identity, not intent." The paper states any claim it prevents engineered pandemics is unsupported and avoided. The 77-scoring academic reviewer: "Naming the actor you do NOT stop is exactly the discipline biosecurity review rewards." This is the inverse of safety-washing and the single biggest credibility signal.

S-2. Non-substitution is enforced in the data model, not just prose (academic, screening-realist, commercial-owner, policy-staffer). The verdict crosses the screening boundary as an OPAQUE token; customer_receipt() returns only {orderId, status:'recorded'} and a test asserts "flagged"/"verdict" never appear; the exemption authorizes a sequence CLASS, never a sequence, with clearance staying provider-local. This actively denies an attacker a "will this order pass" oracle.

S-3. Self-corrected privacy overclaim and disclosed limitations as first-class results (all 8 panels). IMPLEMENTATION_CROSSCHECK.md labels the earlier privacy claim a "CORRECTED overclaim"; cross-batch volume/timing leak, no-ZK, in-memory/no-durability, and the attestix rc2 ~4.4 ops/s ceiling are all named precisely in code, spec, and paper. PLAN_VS_REALITY.md is a genuine self-critical audit trail. Reviewers trust this MORE, not less.

S-4. Vendor-neutrality is structural, not asserted (academic, screening-realist, policy-staffer, adversarial, commercial-owner, company). Apache-2.0; pyproject dependencies=[] (verified: zero proprietary core); StubEngine is the dependency-free default; attestix is one optional extra (attestix==0.4.0rc2, verified); CI validates the optional backend source-blind. A genuine answer to the Aclid-acquired-by-Ginkgo closed-chokepoint concern.

S-5. Standards-grounded and machine-checked (academic, crypto, policy-staffer). W3C VC Data Model + DID Core (real Recommendations); generalizes SecureDNA's ECS into open W3C form crediting the originators rather than erasing them; test_regulatory_traceability.py FAILS if any schema field lacks a mapping row; CITATIONS_VERIFIED.md + verify_citations.py run against the live arXiv API; instruments correctly marked BILL / PROPOSAL / GUIDANCE / VERIFIED / UNVERIFIED.

S-6. Hardened, tested infohazard guard (screening-realist, crypto, adversarial). assert_no_sequence canonicalizes (NFKC, strip non-letters, uppercase) and rejects 7 obfuscation bypasses (lowercase/tab/FASTA/hyphen/punctuation); the only nucleotide-like strings in the repo are negative test fixtures proving the guard fires. Described precisely as defense-in-depth field validation, with not-being-a-screener as the actual structural protection.

## 5. SPRINT PLAN — Sprint S-01 (LOOP.md style: spec -> build -> test -> review)

Theme: convert synth-attest from "honest clever artifact" to "fundable open reference the incumbents can adopt." Ordered by dependency. Each task is one PR.

S-01.1 [SPEC] Reposition + theory-of-impact + duty-bearer (addresses CC-1, CC-2, CC-4, CC-7).
- spec: add THEORY_OF_IMPACT.md and a README top-of-funnel paragraph. One falsifiable paragraph: adversary class = semi-legitimate actor who must transact with compliant providers (credential-fraud / stolen-identity ordering / order-laundering / threshold-structuring), the enforcing audit consumer + the action they can take, and the residual threat surface after the four disclosed bypasses. Add a duty-bearer section (regulated entity, the customer-vetting/recordkeeping obligation under HHS framework + UK DSIT guidance, S.3741 as prospective hook).
- build: edit README, paper abstract; drop "deterrence" from headline -> "tamper-evident record-keeping for post-hoc attribution on compliant providers."
- test: grep gate that README/abstract no longer lead with "prevents"/"biosecurity guarantee"; persona spot-check rows for impact + duty-bearer.
- review: screening-realist + theory-of-impact persona pass. DoD: a grant reviewer can verify scope + impact in under five minutes.

S-01.2 [SPEC] Headline rename + audit-channel adversary model (addresses CC-6).
- spec: rename leading property to "tamper-evident, leakage-bounded (hash-based) order audit" in README bullet + paper abstract/subsection heading; keep "privacy-preserving" only where immediately qualified. Add half-page adversary model: observer, prior, explicit leakage function L = {batch_count, batch_timing, padded_size}; state plainly NOT ZK, NOT a hiding commitment, cross-batch correlation open.
- build: edits to README, spec.md, paper.
- test: add an assertion in CI doc-lint that the unqualified phrase "privacy-preserving" does not appear in the README headline bullet.
- review: crypto + academic persona. DoD: headline claim matches what the code earns.

S-01.3 [BUILD] Durable external anchor (addresses CC-3 — the crypto-panel CRITICAL).
- spec: define an append-only durable backend with external witnessing: file/append-only log for durability now, plus an RFC 6962-style signed-tree-head transparency-log interface (or RFC 3161 timestamp) so a holder of a prior STH detects provider equivocation.
- build: AppendOnlyLogEngine backend (no attestix throughput ceiling); anchor_batch persists + emits a witnessable root.
- test: restart-survives-tamper test; equivocation-detected test against a stored prior STH; add per-context domain tags (b'synth-attest/commit/v1', '/batch-root/v1', '/custody/v1').
- review: crypto persona. DoD: tamper-evidence holds against the audited provider, not just third parties; durability documented as the first production step delivered.

S-01.4 [BUILD] Crypto correctness pass (supports CC-3, CC-6; crypto-panel highs).
- spec: per-field 256-bit salts; RFC-6962 leaf(0x00)/node(0x01) prefixing if inclusion proofs are added; StubEngine refuses to start with the default hardcoded secret unless an explicit allow-insecure flag is set (else loud non-production warning); full-length custody HMAC handle (>=128-bit).
- build: engine.py, audit.py, custody.py.
- test: leaf-cannot-validate-as-node test; default-secret-refusal test; handle-length test; correct the "domain separation" wording in the paper to "per-field length-prefixing within the commitment."
- review: crypto persona. DoD: prose matches code; StubEngine cannot be mistaken for a production trust anchor.

S-01.5 [BUILD] Fixed-cadence anchoring + leakage bound (addresses CC-4/CC-6 mitigation, adversarial CRITICAL).
- spec: implement the fixed-cadence anchoring audit.py line 28 already names (emit every T seconds regardless of load, fully padding empty windows); treat (B, T) as documented security parameters.
- build: scheduler/flush trigger on the StubEngine path.
- test: benchmark and report the leakage bound; report StubEngine throughput separately from the attestix rc2 ~4.4 ops/s figure (or relabel rc2 as "unbenchmarked, expected low" until measured).
- review: adversarial persona. DoD: the structuring/order-splitting channel is bounded or honestly disclosed as residual with a k-anonymity argument.

S-01.6 [SPEC] Issuance root-of-trust + GOVERNANCE.md (addresses CC-5).
- spec: GOVERNANCE.md + an issuance trust-model section: who accredits issuers (trust list, avoid recreating a centralized CA), required identity + institutional-affiliation proofing mapped to an LoA framework (NIST 800-63 IAL2 / eIDAS substantial), Sybil/self-issuance controls, revocation due-process, false-attribution recourse, data-minimization, and explicit chilling-effect/exclusion-misuse mitigations. State the credential is INPUT to provider-local KYC, never a substitute; elevate notAClearance into a governance commitment.
- build: docs only (pre-implementation sketch is acceptable for grant stage).
- test: regulatory-traceability test extended to assert a governance row exists.
- review: commercial-owner + screening-realist persona. DoD: a provider GC can map it to onboarding; a foreign credential's handling is specified.

S-01.7 [BUILD] Screening-binding + machine-readable scope assertion (addresses CC-3/CC-7 fig-leaf risk, academic medium).
- spec: bind the audit/exemption artifact to a screening attestation (commit to a hash of a SecureDNA-style verdict / IBBIS Common Mechanism run) so an attested order is incomplete without a linked screening record; verifier fails closed when none present. Add attestation_scope='identity_only' and screening_status='not_evaluated_here' to every verification/audit/receipt response.
- build: schemas + verifier + receipt.
- test: assert no response field can be parsed as an order-safety clearance; assert verifier fails closed without a screening attestation.
- review: policy-staffer + academic persona. DoD: the credential can never be waved as a screening fig leaf.

S-01.8 [SPEC+REVIEW] ADOPTION.md + interop mapping + one documented touchpoint (addresses CC-1, CC-2 — the existential one; do this in parallel, it gates the grant's success metric).
- spec: ADOPTION.md (smallest real pilot, e.g. a provider issuing exemption VCs for a teaching-exempt class against mock orders; the exact de-risking milestone; "what happens if IBBIS ships" contingency = you become their open reference impl). Field-level mapping from credential/audit schema to IGSC Harmonized Screening Protocol v3.0 (extend REGULATORY_MAPPING.md). X.509-ECS-to-VC bridge note.
- build: docs + one outreach email thread to IBBIS / SecureDNA / one IGSC provider acknowledging the open W3C reference and asking whether they would issue/consume it.
- test: n/a (artifact-based).
- review: company + screening-realist persona. DoD (and the grant's falsifiable 3-6 month metric): at least one written external touchpoint on record, plus the IGSC interop mapping committed.

## 6. GRANT PACKAGE — BlueDot Rapid Grant (ready to paste)

Recommended ask: USD 8,000 (within the $50-10k band; reserves headroom and signals a scoped, milestone-bound increment, not a max-out reach).

Line items:
- USD 3,000 — Durable, externally-witnessed audit anchor (append-only log + RFC 6962-style signed-tree-head interface) so tamper-evidence holds against the audited provider, not just third parties (S-01.3). The single highest-leverage engineering fix.
- USD 1,500 — Crypto-correctness pass: per-field 256-bit salts, per-context domain tags, RFC-6962 leaf/node prefixing, StubEngine default-secret refusal, fixed-cadence anchoring with a documented leakage bound (S-01.4, S-01.5).
- USD 1,500 — Issuance root-of-trust + GOVERNANCE.md (LoA framework, Sybil/self-issuance controls, revocation due-process, false-attribution recourse, exclusion safeguards) and the screening-binding + machine-readable scope assertion (S-01.6, S-01.7).
- USD 1,500 — Interop + adoption: field-level mapping to the IGSC Harmonized Screening Protocol v3.0, X.509-ECS-to-VC bridge note, ADOPTION.md, and documented outreach to IBBIS / SecureDNA / one IGSC provider (S-01.1, S-01.8).
- USD 500 — External infohazard + security review of repo + paper by a named biosecurity-governance reviewer, cited in the paper.

Three strongest evidence points:
1. Already substantially built and unusually honest: a 592-LOC dependency-free core (pyproject dependencies=[] verified), 42 tests, CI green on Python 3.11+3.12, an IEEE paper with figures and tables compiled, and a public Apache-2.0 repo. The team self-corrected its own earlier privacy overclaim (logged in IMPLEMENTATION_CROSSCHECK.md) and discloses every limitation (cross-batch volume/timing leak, no-ZK, in-memory durability, the attestix rc2 ~4.4 ops/s ceiling) in code, spec, and paper.
2. Correct, structurally-enforced scope: it sits on top of sequence screening and never replaces it. The screening verdict crosses the boundary as an opaque token, the customer receipt strips it entirely (asserted by test), the exemption authorizes a sequence class rather than a sequence, and a hardened tested infohazard guard ensures no sequence data ever enters the layer. This denies an attacker a screening-pass oracle.
3. Genuine, verifiable white space: no existing system combines open-source + W3C VC/DID portable identity + tamper-evident order audit. Aclid (acquired by Ginkgo, 2024) is a closed first-party screener with centralized KYC; SecureDNA's ECS is the screening-coupled gold standard whose exemption design we generalize into open W3C form; IBBIS today ships guidance and forms. A machine-checked regulatory-traceability test and a live-arXiv citation verifier keep every claim grounded.

Application text (what makes this successful / why you / why now), verified facts only:
synth-attest is the open, vendor-neutral reference implementation of the portable-identity-plus-tamper-evident-audit layer that current biosecurity guidance describes but that no one has built in open form, generalizing SecureDNA's Exemption Certification System (Baum et al., arXiv 2403.14023, with cryptographers Rivest, Shamir, and Yao) into the W3C Verifiable Credentials and DID Core Recommendations. It is deliberately narrow: it sits on top of sequence screening and never replaces it, intervenes only at the acquire-materials node on already-compliant providers, addresses fraud, attribution, and after-the-fact accountability, and explicitly does not screen, does not cover benchtop or non-compliant synthesis, and does not stop a credentialed insider, because identity proves identity, not intent. The work is the right fit for a Rapid Grant precisely because the engineering and the honesty are already credibly in place, an Apache-2.0 prototype with a dependency-free core, a compiled IEEE paper, and self-disclosed limitations, so the grant funds a tightly-scoped de-risking increment rather than speculation. Now is the moment because the policy environment is converging toward exactly this kind of auditable customer-vetting layer, with the US S.3741 bill, in-force UK DSIT synthetic-nucleic-acid guidance, and ISO 20688-2:2024 all pointing the same direction, and because IBBIS has signaled identity work for 2026, which makes establishing a credible open reference, and engaging IBBIS and providers as a complement rather than a competitor, time-critical. The grant's falsifiable success metric is concrete and external: a durable externally-witnessed audit anchor, a field-level mapping to the IGSC Harmonized Screening Protocol, and at least one documented expression of interest from IBBIS, SecureDNA, or a synthesis provider within three to six months. The right framing is humble: this generalizes the field's gold-standard prior art into open standards so the trusted conveners can adopt it, not a claim to outperform them.

## 7. CITATION LIST (use exactly; do not invent)

arXiv (verified via live arXiv API 2026-05-30):
- arXiv 2602.06172v1 — "Know Your Scientist: KYC as Biosecurity Infrastructure" (Jonathan Feldman, Tal Feldman, Annie I. Anton). CONFIRMED. CITE-AS arXiv.
- arXiv 2403.14023v3 — "A system capable of verifiably and privately screening global DNA synthesis" (SecureDNA; Baum, Berlips, Chen, ... Esvelt, Rivest, Shamir, Vaikuntanathan, Yao, Yu, ...). CONFIRMED. CITE-AS the gold-standard prior art being generalized; never as a peer outclassed on cryptography.
- arXiv 2001.01659 — "KYChain: User-Controlled KYC Data Sharing and Certification" (Dragan, Manulis). CONFIRMED. CITE-AS established VC/blockchain KYC prior art.
- arXiv 2112.01237 — "Designing a Framework for Digital KYC Processes Built on Blockchain-Based Self-Sovereign Identity" (Schlatt, Sedlmeir, Feulner, Urbach). CONFIRMED. CITE-AS established SSI-KYC prior art.
- arXiv 2506.11613 — "Model Organisms for Emergent Misalignment" (Turner, Soligo, Taylor, Rajamanoharan, Nanda). CONFIRMED. CITE-AS only in the operator's separate AI-safety track; NOT relevant to this bio project.

Non-arXiv (cite by the stated venue, never as arXiv):
- Microsoft "Paraphrase Project" — CITE-AS Science (Oct 2025). MUST NOT be cited as arXiv.
- W3C Verifiable Credentials Data Model + DID Core — CITE-AS w3.org Recommendations.
- US S.3741 — CITE-AS a BILL (congress.gov), "proposed legislation (introduced), not enacted." Never as in-force law.
- UK DSIT synthetic-nucleic-acid guidance — CITE-AS gov.uk, in force.
- ISO 20688-2:2024 — CITE-AS iso.org; use "aligned with" / "mapped to" only, never "conforms" / "certified."

## 8. HONESTY LEDGER

Claims that must NOT be made:
- Do NOT claim it prevents engineered pandemics, secures DNA synthesis, or stops a determined/sophisticated actor. It does not screen, does not cover benchtop or non-compliant/offshore synthesis, and does not stop a credentialed insider.
- Do NOT use "privacy-preserving" as an unqualified headline. The property is leakage-bounded hash obfuscation, not ZK and not a hiding commitment.
- Do NOT claim "tamper-proof"; use "tamper-evident." And do NOT imply tamper-evidence holds against the audited provider until external witnessing is implemented (today anchors are in-memory; a provider can rewrite its own history undetectably).
- Do NOT claim "domain separation" for the commitment; it is per-field length-prefixing within one hash. The batch root is a flat hash-of-concatenation with no RFC-6962 leaf/node separation.
- Do NOT present StubEngine signatures or its tamper/revocation tests as authenticity or asymmetric VC security; it is symmetric integrity under a hardcoded key.
- Do NOT present "selective disclosure" as a sound SD primitive in the default engine; it is HMAC-resign-the-subset, linkable and predicate-incapable. "No ZK yet" must not imply the only gap is range proofs.
- Do NOT present the $1.18 (AI-KYC) vs $14 (manual) figure as synth-attest's own saving; it is an Aclid AI-KYC estimate. State source and method.
- Do NOT claim conformance/certification to ISO 20688-2; "aligned with" only. Do NOT cite S.3741 as enacted. Do NOT cite Paraphrase as arXiv.
- Do NOT claim superiority over Aclid or SecureDNA. Do NOT imply production-readiness. Do NOT cite LOC/test counts as a quality signal.
- Do NOT overstate the infohazard guard as a security boundary; it is defense-in-depth field validation. The structural protection is not being a screener.
- Do NOT present "core 32 pass / 10 skip" as full independent coverage of the attestix-backed flow; the 10 skips are optional-backend tests, and the attestix path is validated source-blind in a separate CI job.

Disclosed limitations (keep visible, near every headline claim):
- PROTOTYPE not production: in-memory store, no durability, no external anchor in the default engine; tamper-evidence does not survive a restart.
- Cross-batch volume/timing still leaks coarse volume (batch count + timing + padded size); verdict and intra-batch order count are hidden. Fixed-cadence anchoring is the named-but-unimplemented mitigation.
- No ZK; selective disclosure only, and the default-engine SD is not a sound primitive (linkable).
- AttestixEngine attestix==0.4.0rc2 is a pre-release pin; the ~4.4 ops/s ceiling is itself currently unbenchmarked (Throughput/anchor-cost benchmark NOT STARTED) — either measure it or label it "unbenchmarked, expected low."
- B=16 anonymity set is small; the batch flush trigger is unspecified/unimplemented, so (B,T) are security parameters not yet operationalized.
- Custody centralizes DID/key material server-side; registry-secret compromise = full deanonymization + impersonation of all custodied customers. Handle is 64-bit (birthday-collision exposure).
- Issuance root-of-trust, identity-proofing LoA, and governance/recourse for the identity registry are unbuilt (flagged as the principal open architectural question).
- Zero users, zero provider/IGSC/IBBIS adoption; live provider integration NOT STARTED; IBBIS 2026 identity work is the main strategic risk.
- GDPR/DPDP immutable-audit-vs-erasure tension is acknowledged and unresolved.
