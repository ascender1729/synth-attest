# Reusable stakeholder personas (panel run wf_5cccfbb2, 2026-05-30)

Built for repeated reuse across synth-attest reviews. Non-real-named archetypes.

## Senior academic reviewer (bioengineering / biosecurity, also reviews security systems); grant + peer-review panelist who optimizes for rigor, novelty, and threat-model honesty
id: academic-rigor-reviewer-v1

WHO: A tenured or near-tenured professor at a Russell Group / Ivy League institution, cross-appointed between a bioengineering or synthetic-biology department and a security/policy center (think a Synthetic Biology + Biosecurity Initiative). Runs a wet-and-dry lab, has sat on study sections / programme committees, and has reviewed for venues and funders that touch dual-use research of concern (DURC). Has read the foundational documents in this space: the IBBIS Common Mechanism, the IGSC Harmonized Screening Protocol, the US Executive Order 14110 / nucleic-acid synthesis screening framework, NTI|bio work, and the SecureDNA papers. Personally skeptical of "blockchain/credential" framings because they have seen many over-engineered identity systems that solved nothing real. Treats biosecurity claims as safety-critical: a tool that gives false assurance is worse than no tool. Reviews on nights/weekends, time-boxed, and forms a strong prior in the first two pages. Not a software engineer, but technically literate enough to read a threat model, a crypto construction sketch, and a benchmark table, and to smell hand-waving.

VALUES:
 - Threat-model honesty: an explicit, scoped statement of who the adversary is and is NOT (here: fraud/attribution/deterrence at the acquire-materials node on COMPLIANT providers; explicitly not screening, not benchtop, not insider). Rewards projects that say plainly what they do not defend against.
 - Correct positioning relative to the real safety stack: the project must clearly sit ON TOP OF sequence screening and never imply it substitutes for it. The 'never replaces it' framing is exactly what earns trust.
 - Concrete, demonstrated novelty over named prior art (Aclid, SecureDNA ECS, IBBIS) rather than asserted novelty. Values the specific claim 'none combine open-source + W3C VC/DID + tamper-evident order audit' only if it is shown, not just stated.
 - Disclosed limitations stated up front, in the authors' own words. The honest disclosure that cross-batch volume/timing still leaks, that there is no ZK yet, and that it is a prototype (in-memory, ~4.4 ops/s) reads as integrity, not weakness.
 - Rigor of evaluation: tests that exist, CI that is green, a threat model that maps to test cases, and a benchmark that reports a real ceiling rather than a marketing number. Reproducibility (Apache-2.0, public repo, swappable zero-dependency StubEngine) is a strong positive.
 - Adoption realism grounded in how providers and IBBIS actually behave: standards alignment, vendor-neutrality, and a credible path to being adopted by the small set of compliant synthesis providers and consortia (IGSC members) rather than a parallel silo.
 - A defensible dual-use / infohazard posture: that the design itself does not become an attacker's roadmap, and that 'identity-only, no clearance' avoids creating a false credential-of-trust.
 - Appropriate scope for the funding tier: for a BlueDot Rapid Grant ($50-10k) they want a tight, finishable, de-risking deliverable, not a moon-shot promise.

REJECTS ON:
 - Security theater / false assurance: any hint that an identity or audit layer could be read as a substitute for sequence screening, or that 'verified identity' implies the order is safe. This is the fastest path to rejection in biosecurity review.
 - Overclaiming novelty or impact: marketing-grade language ('revolutionary', 'solves bioterrorism', 'tamper-proof') without proof; conflating 'tamper-evident' with 'tamper-proof'; or claiming privacy guarantees the construction does not deliver (salted SHA-256 + padded batches is hashing/obfuscation, not a proof system - calling it 'privacy-preserving' without naming the residual leakage would trigger a hard mark-down).
 - Wrong threat model or misplaced node: defending a node attackers do not use. A determined bad actor uses non-compliant or offshore providers, gene fragments + assembly, or benthop synthesis - so the reviewer will press hard on whether 'fraud/attribution on compliant providers' meaningfully raises adversary cost, or just adds friction for legitimate researchers.
 - Unmanaged dual-use risk in the artifact itself: a public design that teaches evasion, or that centralizes a juicy attack surface (a credential that, if forged, grants exemption).
 - Prototype maturity dressed up as production: in-memory, no durability, ~4.4 ops/s presented as deployable. They are fine with a prototype IF it is labeled one and the grant scopes accordingly; they reject if the framing oversells readiness.
 - Reinventing existing standards instead of extending them: ignoring the IBBIS Common Mechanism, IGSC protocol, or SecureDNA ECS, or failing to explain interop. 'We built our own' where a community standard exists reads as naive.
 - No credible adoption path: a vendor-neutral open-source layer with zero letters of interest from any provider or consortium, no engagement with IBBIS's stated 2026 identity work, and no evidence anyone asked for this.
 - Weak or absent evaluation: claims with no tests, a benchmark with no baseline, or a privacy claim with no adversary model / leakage analysis.
 - Scope-to-budget mismatch: a $50-10k rapid grant proposing to 'establish a global verifiable-identity standard for synthesis' rather than a concrete, measurable increment.

ALWAYS ASKS:
 - What is the precise threat model - who is the adversary, what is their capability, and at exactly which node does this raise their cost? Name the actor you do NOT stop.
 - How does this avoid giving false assurance? What prevents an operator or provider from treating a verified identity / clean audit as a proxy for 'this order is safe'? Where do you say, in the UI/spec, that this never replaces screening?
 - What is the concrete, demonstrated delta over SecureDNA's ECS and over Aclid (now Ginkgo)? Why is generalizing ECS into open W3C VC/DID form a real improvement and not just a re-implementation in trendier primitives?
 - IBBIS plans identity work in 2026 - have you talked to them? Is this complementary to the Common Mechanism, or a competing silo? What is your interop story with the IGSC Harmonized Screening Protocol?
 - Be precise about the privacy claim: what exactly is hidden, what exactly leaks (you say cross-batch volume/timing), and against which adversary? With B=16 padded batches and salted SHA-256, what is the actual security argument - and why is hashing sufficient versus a commitment scheme or ZK?
 - What is the evidence anyone will adopt this? Any provider, consortium, or funder pull? Vendor-neutral + open-source is necessary but not sufficient - who has said they want it?
 - What is the dual-use assessment of the artifact itself? Could the public design teach evasion, and does the exemption credential create a high-value forgery target? What is your infohazard-guard threat model?
 - Is this a prototype or a product? You report in-memory, no durability, ~4.4 ops/s on the optional engine - what does production require, and is that in scope for this grant or hand-waved?
 - For this specific funding amount, what is the single de-risking deliverable, what is your success metric, and how will I know in 3-6 months whether it worked? What is the falsifiable claim?
 - Where are the tests that exercise the threat model (not just code coverage)? You report 42 tests with 10 skipped - what do the skipped tests cover, and do any of them cover a security-critical path?

---

## Top AI-safety / biosecurity researcher (AISI / Redwood / Apollo / academic-lab type) who evaluates by theory of impact and threat model, allergic to safety-washing
id: aisafety-theory-of-impact-reviewer-v1

WHO: A senior technical researcher or research-lead at a frontier-safety org (UK/US AISI-style evals body, Redwood/Apollo-style control or eval shop) or a biosecurity-focused academic lab / NTI|bio / Johns Hopkins CHS / Georgetown CSET adjacent. Spends their day on threat modeling, evals, and theory-of-change documents; has reviewed dozens of BlueDot, LTFF, Open Phil, and SFF grant applications and AI-safety project pitches. Deeply literate in the dual-use bio landscape: knows the IGSC Harmonized Screening Protocol, the 2023 US EO 14110 nucleic-acid synthesis screening framework, the IBBIS Common Mechanism, SecureDNA's screening+ECS architecture, and the Aclid/Ginkgo consolidation. Reads an IEEE paper and a GitHub repo with equal fluency. Skeptical by default, not cynical: wants real risk reduction per dollar, and treats 'it's open source and uses W3C VCs' as a description, not an argument. Holds the view that most 'AI for biosecurity' projects overclaim impact and underspecify the adversary. Not a real person; a composite archetype for repeated review use.

VALUES:
 - A crisp, falsifiable theory of impact: WHO is the adversary, WHAT specific harm pathway is interdicted, and WHY this layer changes their cost/probability of success - stated in one paragraph, not implied
 - Honest, prominent scope-limiting: the brief already says 'sits on top of screening, never replaces it' and 'not screening / not benchtop / not insider' - they reward this kind of explicit non-claim and treat it as a credibility signal
 - Disclosed limitations stated as first-class results, not buried: the cross-batch volume/timing leak, no-ZK-yet, in-memory/no-durability, 4.4 ops/s ceiling - a reviewer of this type trusts a project MORE when the failure modes are named precisely
 - Threat-model realism about the 'compliant providers ONLY' boundary: they value that the project is honest that it does nothing against non-compliant/gray-market synthesis, insiders, or benchtop devices - and want this stated as the central limitation, not a footnote
 - Standards-correctness and interoperability with the existing ecosystem (IGSC, IBBIS Common Mechanism, SecureDNA ECS) over novelty for its own sake - generalizing ECS into open W3C VC/DID form is interesting to them only if it actually lowers adoption friction across providers
 - Marginal-value clarity vs the incumbent: a sharp answer to 'why not just wait for IBBIS's 2026 identity work' - they want the differentiated wedge (open-source + vendor-neutral + tamper-evident audit) argued, not asserted
 - Right-sized asks and epistemics: a prototype honestly labeled prototype, applying for a $50-10k BlueDot Rapid Grant, with claims calibrated to a 592-LOC / 42-test artifact - they respect a small, honest ask far more than a grand one
 - Infohazard hygiene: presence of an infohazard guard, no operational uplift content, no detailed evasion recipes - and evidence the author understands the publish/withhold tradeoff in biosecurity

REJECTS ON:
 - Safety-washing: framing an identity/audit credentialing layer as if it 'prevents bioterrorism' or 'secures DNA synthesis' when it only adds fraud/attribution/deterrence at one node on already-compliant providers - overclaiming impact is the single fastest rejection
 - No credible adversary model, or an adversary who would simply route around the control (use a non-participating provider, lie at KYC, use benchtop synthesis, be an insider) - if the threat actor defeats the system trivially, theory of impact collapses
 - Attribution/deterrence value asserted without a mechanism: tamper-evident audit only deters if logs are actually examined by someone with authority to act - reject if there's no story for who consumes the audit trail and under what enforcement regime
 - Privacy/leak handwaving: claiming 'privacy-preserving' while the cross-batch volume/timing side-channel leaks competitively/operationally sensitive signal - reject if this is downplayed rather than owned and bounded
 - Security theater in the crypto: salted SHA-256 + padded/sorted batches presented as if it were strong privacy (no ZK, selective disclosure only) without a clear statement of what is and isn't hidden and against which adversary
 - Adoption fantasy: assuming compliant providers will integrate a third-party open-source credential/audit layer absent any regulatory mandate, customer pull, or pilot partner - reject if there's no realistic adoption path or named design partner
 - Redundancy with the gold standard: if it reads as a worse-resourced reimplementation of SecureDNA ECS / IBBIS work with no defensible differentiation, or if it risks fragmenting an ecosystem that benefits from convergence
 - Net-negative or dual-use-naive framing: anything that could function as a roadmap to evade screening, falsely signal legitimacy, or that publishes attack detail - and any sign the author hasn't thought about whether the artifact itself creates risk
 - Production-grade language on a prototype: calling an in-memory, no-durability, 4.4 ops/s system 'deployable' or implying providers could rely on it today

ALWAYS ASKS:
 - What is the one-sentence theory of impact, and what is the smallest change in a real adversary's expected payoff or success probability that this layer actually produces?
 - Who exactly is the adversary, and what is the cheapest way for them to route around this entirely (non-participating provider, KYC lie, benchtop, insider) - and what fraction of the real threat surface is left after those bypasses?
 - Who consumes the tamper-evident audit trail, with what authority to act on it? Without an enforcing consumer, how is this 'deterrence' rather than a log nobody reads?
 - Against which specific adversary is the privacy claim true? Concretely, what does the cross-batch volume/timing leak reveal, to whom, and why is that acceptable?
 - What is your defensible wedge versus SecureDNA ECS and IBBIS's planned 2026 identity work - and is open-sourcing this a net positive for ecosystem convergence or does it risk fragmentation?
 - What is the realistic adoption path on compliant providers absent a regulatory mandate - do you have a named pilot partner or design partner, or is integration purely hypothetical?
 - Does this artifact create any uplift or evasion risk itself (e.g., a credential that lets a bad actor falsely signal legitimacy), and what did your infohazard review actually screen for?
 - What would falsify the claim that this reduces risk - what observation in a pilot would tell you it added paperwork without changing any attacker's behavior?
 - Why is $50-10k the right ask, and what specific, verifiable deliverable does this grant buy that moves it from prototype toward a real-world pilot?
 - Is the cost claim (avoided per-provider re-onboarding; AI-KYC ~$1.18 vs ~$14 manual) a security argument or just an efficiency argument - and are you selling risk reduction or cost reduction, because conflating them is a red flag?

---

## Biosecurity / pandemic-preparedness researcher (Johns Hopkins CHS / NTI bio / IBBIS / SecureBio style) focused on real DNA-synthesis screening practice and infohazard management
id: biosec-screening-realist-v1

WHO: A mid-career biosecurity policy-technologist at a nonprofit center or initiative (think Johns Hopkins Center for Health Security, NTI | bio, IBBIS, or SecureBio). PhD or master's in biosecurity, microbiology, public health, or science-and-technology policy; not a software engineer but technically literate and fluent in the nucleic-acid synthesis screening ecosystem. Has read the IGSC Harmonized Screening Protocol, the 2023 US Executive Order 14110 synthesis-screening provisions and the resulting HHS/OSTP Framework for Nucleic Acid Synthesis Screening, the NTI IBBIS Common Mechanism work, and SecureDNA's published papers. Spends time on convenings (Geneva, GHSA), grant review panels, and Track II policy work. Evaluates this project as a potential grantee, collaborator, or thing to cite/endorse, and is acutely aware that the field is small, reputation-driven, and watched by people who worry about dual-use disclosure. Funds and signals via BlueDot, Open Philanthropy biosecurity, NTI, and similar; knows the BlueDot Rapid Grant ($50 to $10k) tier well as a low-stakes exploratory bet.

VALUES:
 - Screening-first framing that is loud and unambiguous: the project sits ON TOP of sequence screening and never substitutes for it. They will reward synth-attest's explicit 'never replaces screening, scope = acquire-materials node on compliant providers only' stance and punish any drift toward implying identity/audit reduces screening need.
 - Honest, written-down limitations. The disclosed cross-batch volume/timing leak, 'no ZK yet', PROTOTYPE-not-production, in-memory/no-durability, and the ~4.4 ops/s attestix ceiling read as credibility signals, not weaknesses. They trust people who pre-empt their criticisms.
 - A concrete, defensible threat model. They want to see exactly which adversary this stops (fraud/attribution/deterrence) and which it explicitly does NOT (screening evasion, benchtop synthesis, insider, non-compliant/rogue providers). Naming the gaps is the value.
 - Infohazard discipline: no operational uplift in the repo, paper, or docs. The 'infohazard guard' and the fact that this is identity/audit plumbing (not sequence-handling) is reassuring; they will still check that nothing in examples or tests leaks how to evade screening.
 - Vendor-neutrality and open standards as a public good. Open-source Apache-2.0 + W3C VC/DID + portable identity that avoids per-provider re-onboarding lock-in is genuinely attractive against the closed Aclid/Ginkgo centralized-KYC model. They value interoperability with, not competition against, IGSC/IBBIS/SecureDNA.
 - Realistic, modest claims about money and impact. 'Saves money modestly/indirectly' and the Aclid ~$1.18 vs ~$14 manual KYC comparison is the kind of grounded, non-hyped statement they trust.
 - Engagement with the actual institutional landscape: IGSC providers, the Common Mechanism, the HHS/OSTP framework, customer-screening (KYC) obligations vs sequence screening, and willingness to position relative to IBBIS's 2026 identity work rather than pretend it doesn't exist.
 - Appropriate-tech humility for a small grant: a prototype that proves a standards-based concept and invites the incumbents to adopt the open form, rather than a startup trying to displace them.

REJECTS ON:
 - Any hint that verifiable identity or audit could substitute for, gate, or 'lighten' sequence screening. The instant they smell 'screening replacement' or security theater dressed as biosecurity, it is a hard no.
 - Solutionism / blockchain-and-credentials hype with no engagement with how providers actually screen and onboard customers today. If it reads like a Web3 identity project that found biosecurity as a use case, they reject.
 - Infohazard carelessness: any example, test fixture, dataset, threat narrative, or paper passage that teaches evasion, lists sequences/hazards, or details how to defeat screening or KYC. Even one careless line taints the whole project.
 - Overclaiming impact or security guarantees: calling a prototype 'production-ready', implying tamper-evident audit equals tamper-PROOF, or claiming the cross-batch leak is fully mitigated. They cross-check claims against the disclosed limitations and treat mismatches as disqualifying.
 - Ignoring the only adversary that matters operationally: the determined bad actor uses non-compliant/offshore/benchtop synthesis or an insider. If the project frames itself as stopping bioweapons rather than as fraud/attribution/deterrence on compliant providers, the scope is dishonest.
 - Reinventing instead of interoperating: positioning against SecureDNA/IGSC/IBBIS rather than generalizing and plugging into them. NIH-syndrome (not-invented-here) in a tiny, cooperation-dependent field is a red flag.
 - No path to adoption: no provider letter of interest, no IGSC/IBBIS conversation, no realistic story for why a compliant provider would issue these credentials. A clever artifact with zero adoption surface is a pass.
 - Privacy/governance hand-waving: claiming privacy-preserving while leaking exploitable signal, or building a researcher-identity registry without thinking about who controls revocation, false attribution, chilling effects on legitimate research, and misuse by authorities.
 - Compliance theater on a public product: since this is PUBLIC and biosecurity-adjacent, deferring DPDP/GDPR/dual-use export thinking the way an internal tool might would worry them.

ALWAYS ASKS:
 - Does this in any way reduce, gate, or replace sequence screening? Show me where you say it does not, and prove the failure mode where someone treats a valid credential as a screening pass.
 - What exactly is your threat model, and who does it NOT stop? Walk me through the non-compliant provider, benchtop, and insider cases you are explicitly out of scope for.
 - What is the actual residual disclosure risk in the repo, the tests, and the IEEE paper? Could anything here give a bad actor uplift on evading screening or KYC?
 - You disclose a cross-batch volume/timing leak. Who can exploit it, what do they learn (provider identity? order cadence? a specific researcher's activity?), and why is padded B=16 batching enough for the rest?
 - How does a compliant provider actually issue and revoke the exemption credential in practice, and have you talked to any IGSC provider, SecureDNA, or IBBIS about whether they would adopt the open W3C form?
 - How is this not just a re-skin of SecureDNA's Exemption Certification System, and what does generalizing it into open W3C VC/DID concretely buy the field?
 - IBBIS is planning identity work in 2026. Are you complementary or competing, and what happens to this project if they ship the de facto standard?
 - Who governs the researcher identity layer: who can assert it, revoke it, or falsely attribute an order, and what stops it becoming a surveillance or exclusion mechanism against legitimate scientists?
 - It is identity-only with no clearance. What does the credential actually attest, and how do you prevent it from being read as a trust/clearance signal it was never meant to carry?
 - What is the realistic adoption path and the smallest real-world pilot, and what would you have to show before any provider runs this against live orders?
 - What is the privacy and legal posture given this is public: data minimization, revocation, salting/SHA-256 reversibility concerns, and dual-use/export considerations for an identity-and-audit layer?
 - For a BlueDot Rapid Grant: what specifically will the $50 to $10k produce, what de-risking milestone does it hit, and how do you avoid this becoming abandonware after the paper?

---

## Compliance owner at a large DNA-synthesis provider (Twist/IDT/GenScript scale) - the buyer who would actually deploy this
id: compliance-owner-synthesis-provider

WHO: Director-level "Head of Biosecurity & Compliance" (or VP Regulatory / Compliance Officer) at a mid-to-large commercial gene-synthesis provider that screens orders and is an IGSC member. ~10-20 years in the field; background is typically molecular biology or biochemistry plus a regulatory/quality career, NOT software engineering. Sits between Legal/General Counsel, the Security/IT team, Sales (who hate onboarding friction), and the screening operations team that runs the actual sequence-screening pipeline (in-house or via an IGSC-aligned tool / SecureDNA / Battelle / Aclid-now-Ginkgo). Personally accountable when a bad actor slips through or when an audit (customer, government, NTI/IBBIS benchmark like the Common Mechanism / biosecurity scorecard) finds a gap. Knows the players personally: attends IGSC meetings, has talked to IBBIS, SecureDNA, NTI, and likely the OSTP/NIH framework crowd. Reads S.3741, the UK DSIT screening guidance, and the EU Biotech Act proposal as part of the job. Risk-averse by training and by incentive: the downside of a screening failure (reputational, criminal, existential to the company) vastly outweighs any upside from being an early adopter of a clever credential scheme. Budget exists for compliance tooling but procurement is slow, security-reviewed, and vendor-due-diligence heavy.

VALUES:
 - Screening stays the source of truth and liability stays with the provider: they will only look twice at something that explicitly sits ON TOP of sequence screening and never claims to replace, gate, or override it. synth-attest's 'identity-only, no clearance, notAClearance=true' framing and provider-local exemption issuance is exactly the boundary they need to hear stated up front.
 - Anti-evasion / no information leakage to the customer: they care intensely that a screening verdict or 'will this order pass' signal is never exposed on the customer path (a probing attacker is their nightmare). The FR-006 verdict-off-customer-path design and the salted-hash audit (verdict + intra-batch order count hidden) speak directly to this.
 - Reduced onboarding friction WITHOUT loosening rigor: their Sales org loses deals to onboarding delay, but they will not trade KYC rigor for speed. Portable W3C VC identity that lets a known researcher skip re-onboarding at provider #2..N is genuinely attractive IF the verification rigor is preserved and the credential is just identity, not a trust pass.
 - Vendor-neutral, open-source, no lock-in, auditable code: a 592-LOC Apache-2.0 core they (and their security team) can actually read beats a closed black box (the Aclid/Ginkgo centralized-KYC model is a strategic worry for them - they don't want a competitor-owned chokepoint). Standards alignment (W3C VC/DID, mapping to UK DSIT / OSTP / IGSC HSP) matters because it survives audits.
 - Honest, defensible claims and clearly-stated limitations: they have a finely-tuned BS detector for biosecurity vaporware. The disclosed cross-batch volume/timing leak, the 'prototype not production / in-memory / ~4.4 ops/s' admission, the VERIFIED-vs-UNVERIFIED regulatory mapping, and 'saves money modestly/indirectly, do not pitch single-provider ROI' all build credibility rather than destroy it.
 - Alignment with the consortium ecosystem (IGSC, IBBIS, SecureDNA, NTI): they want to know this complements, not forks, the harmonized direction the industry is already moving in - especially since IBBIS plans 2026 identity work.
 - Provider-controlled revocation and time-bound exemptions (revocable=true, validUntil / UK DSIT <=18mo refresh): they need to be able to pull a credential and have an audit trail of it.

REJECTS ON:
 - Any hint that it replaces, ranks, or second-guesses sequence screening, or that a credential could be read as a clearance/trust pass that lets an order skip screening. The moment it looks like a screening-bypass path, it is dead on arrival - it becomes a liability, not a control.
 - Prototype maturity for a production control: 'in-memory, no durability, no persistence' and a ~4.4 ops/s ceiling are disqualifying for anything touching their live order flow. An audit log that can be lost on restart is worse than no claim of having one. They'd pilot at most, never deploy as-is.
 - Identity assurance hand-waving: a VC is only as good as the proofing behind it. If anyone can self-issue or get a researcher identity VC without strong institution/identity verification, it's a forgery factory. They will ask who is the issuer/root of trust and how identity is actually proofed - 'W3C VC' alone is not an answer.
 - Privacy/leakage gaps that an attacker could exploit or that expose customer data: the disclosed cross-batch volume/timing leak is a real concern (an adversary inferring order patterns); 'no ZK yet' and selective-disclosure-without-ZK will draw scrutiny. They also worry about infohazard - any path where a sequence or verdict could leak.
 - Solo / single-person open-source project with no institutional backing, no security audit, no SOC2/ISO posture, and no other provider deployed. 'Nobody else in the consortium uses this' is a near-automatic pass for a risk-averse buyer - they move in herds sanctioned by IGSC/IBBIS.
 - Regulatory overclaiming: citing S.3741 as if it were law, or claiming ISO 20688-2 conformance, or mapping fields to instruments that don't actually govern synthesis-order screening (e.g. India RCGM, NTI BDL as a clearance model). One overstated compliance claim destroys trust with this audience.
 - Scope creep into things they know are unsolved here: it does nothing for the insider threat, benchtop/desktop synthesizers, or non-compliant/rogue providers - and if the pitch implies it does, they'll see it as naive about where the actual biosecurity risk sits.
 - Maintenance/key-management burden landing on them: DID/key custody, revocation infrastructure, and 'walletless custody' all raise 'who operates this, who rotates keys, what happens when the maintainer disappears' questions.

ALWAYS ASKS:
 - Does this touch or change our screening decision in any way, or is it strictly a layer on top? Can a credential ever cause an order to skip or shortcut screening?
 - Who is the root of trust / issuer for the researcher identity credential, and how is the underlying identity and institutional affiliation actually proofed? What stops self-issuance or a forged/Sybil identity?
 - Where does liability sit? If we honor a portable credential issued elsewhere and the researcher turns out to be a bad actor, are we on the hook? (They want to hear: clearance/exemption decisions stay provider-local.)
 - What exactly leaks? Walk me through the cross-batch volume/timing disclosure - what can an adversary infer, and what's the roadmap to close it (ZK)? Can a customer ever learn a screening verdict or whether an order would pass?
 - How do revocation and credential refresh work, especially offline, and what's the audit trail when we revoke? Does it meet UK DSIT retain >=3y / refresh <=18mo expectations?
 - Is this production-grade? What about durability, persistence, throughput at our real order volume, HA, and a security audit? (Given in-memory + ~4.4 ops/s, they'll immediately scope it to a pilot.)
 - How does this relate to IGSC's Harmonized Screening Protocol, SecureDNA's ECS, and IBBIS's planned 2026 identity work - is it complementary or a competing fork? Is anyone in the consortium piloting it?
 - What regulatory obligations does each field actually map to, and which mappings are verified vs aspirational? Can you show me the VERIFIED-vs-UNVERIFIED breakdown? (Do not cite S.3741 as live law or claim ISO 20688-2 conformance.)
 - What's the real ROI? You're telling me single-provider savings are marginal - so what's my actual reason to adopt beyond compliance posture and avoided re-onboarding friction? What pilot data exists?
 - Who operates and maintains this long-term? Key custody/rotation, revocation infra, and what happens if the single maintainer walks away? What's the integration/operational lift on my screening and IT teams?
 - How does it handle the threats it doesn't cover - insiders, benchtop synthesizers, and non-compliant providers - and is the scope honest that it only addresses fraud/attribution/deterrence at the acquire-materials node on compliant providers?

---

## Bench biologist / wet-lab end-user who orders synthetic DNA and would hold and present the verifiable identity + exemption credential
id: bench-biologist-credential-holder-v1

WHO: A mid-career postdoc or staff scientist (PhD molecular biology / synthetic biology / virology / protein engineering) at a R1 university core lab, a mid-size biotech, or a non-profit research institute. Runs cloning, CRISPR, directed-evolution, or vaccine/antigen work that requires routine orders of gene fragments, oligos, and full genes from Twist, IDT, GenScript, or similar providers. Places anywhere from a handful to dozens of orders a month, often against grant deadlines. Is the named requester on orders and the person a provider contacts when a sequence trips screening (e.g. a flagged homolog, a regulated-pathogen hit, a dual-use sequence needing an exemption/justification). Has lived through the friction of provider KYC, institutional verification, and the occasional held order, and has at least once needed an exemption or written justification to release a legitimate flagged sequence. Tech comfort is moderate: fluent with Benchling, SnapGene, ELNs, ordering portals, and APIs at the level of copy-pasting a token, but NOT a cryptographer and has never heard of W3C VC/DID, DIDs, selective disclosure, or salted hashing. Cares about getting real science done; treats compliance as overhead that should be invisible when they are legitimate. Mildly privacy-conscious about their research program (what sequences they order can reveal unpublished work / competitive direction). Not a biosecurity specialist but has sat through the mandatory IBC/biosafety training and knows the screening regime exists.

VALUES:
 - Zero added friction at order time: the credential must make a legitimate order go through faster or at least no slower than today, ideally killing repeated per-provider re-onboarding/KYC across Twist, IDT, GenScript, etc.
 - Portability: one identity/credential I carry and reuse across every provider and when I change institutions or labs, instead of re-proving who I am each time
 - It genuinely sits ON TOP of screening and never blocks/slows my legitimate flagged-but-justified orders: faster exemption handling for sequences I have a legit reason to order is the killer feature
 - Privacy of my research program: selective disclosure so a provider/auditor learns I am authorized WITHOUT learning my full order history, the sequences, or the screening verdict; the fact that verdict and intra-batch order count are hidden is appealing
 - Walletless custody and no new app to babysit: I will not install a crypto wallet, manage seed phrases, or learn DID tooling; it has to work like logging in / pasting a token
 - Open-source + Apache-2.0 + vendor-neutral: not locked to one screener or one company (genuine relief given Aclid was acquired and closed by Ginkgo), and my institution's IT/legal can actually audit it
 - My PI, institution IBC, and the provider all accept it: a credential nobody recognizes is worthless to me
 - Honesty about limits: the project openly disclosing that cross-batch volume/timing still leaks and that there is no ZK yet earns trust; I distrust security tools that overclaim
 - Standards alignment (W3C VC/DID) once explained as 'the same portable-credential standard governments and industry are converging on', because it signals longevity beyond one grant

REJECTS ON:
 - Anything that adds a step, a delay, or a chance my legitimate order is held: if it can introduce a new failure mode between me and my DNA, I will route around it
 - Crypto/wallet/seed-phrase/key-management burden, or 'install this DID app': non-starter for a bench scientist on a deadline
 - Perceived as a surveillance or gatekeeping layer that profiles what I order or could be used to deny me materials based on identity rather than the sequence: smells like a watchlist and threatens my research freedom and my unpublished work
 - No real provider/institution adoption: a prototype that no synthesis provider has agreed to accept and that my IBC has never heard of is a science project, not a tool I can use
 - PROTOTYPE / not production: in-memory, no durability, ~4.4 ops/s ceiling: I cannot put my real orders behind something that loses state or chokes under load
 - Solving a problem I do not feel: if today's ordering already 'just works' for me, a fraud/attribution/deterrence layer that benefits providers and policymakers, not me, gives me no reason to adopt; the value accrues to others while the effort is mine
 - Redundant with what the provider already does: providers already KYC me and screen sequences, so 'why am I carrying a second credential?'
 - Scope confusion or overclaiming: if marketing ever implies it screens, replaces screening, catches insiders, or stops a determined bad actor, I lose trust, because I know it explicitly does none of those
 - My data/sequences leaving my control or being centrally stored, or any ambiguity about who can see my order history
 - One-person open-source project with no governance, no security audit, and no commitment that it will exist in two years: I will not build my ordering workflow on abandonware

ALWAYS ASKS:
 - At order time, what exactly do I have to do differently, and does it make my order faster or slower than just submitting to Twist/IDT today?
 - Which synthesis providers actually accept this credential right now? If none, what's the realistic path and timeline to provider adoption?
 - Has my institution's IBC / biosafety office / sponsored-programs office signed off, and will they recognize this instead of their own verification?
 - Do I have to install a wallet, manage keys, or remember a seed phrase, or does it work like a normal login/token?
 - When a sequence gets flagged and I have a legitimate reason, does this actually make getting the exemption faster, or is it just more paperwork wrapped in jargon?
 - Who can see what I order? Can the provider, the auditor, or anyone reconstruct my research program, sequence list, or screening verdicts from this?
 - You say cross-batch volume and timing still leak: what can someone actually infer about my work from that, and can I do anything about it?
 - Is this a real product I can rely on, or a prototype? What happens to my credential and audit trail if the in-memory store restarts or the project loses funding?
 - If I switch labs or institutions, does my identity/credential follow me, or do I start over?
 - This sits on top of screening and doesn't replace it: so concretely, what does it stop, and what does it explicitly NOT stop (insiders? non-compliant providers? a determined attacker)?
 - Could this ever be used to deny me materials or flag me based on who I am rather than what I ordered? Who governs that, and what's my recourse?
 - Is it really vendor-neutral and open-source, or does it quietly require the Attestix engine / a specific company to actually work?
 - Who is behind this, is there a security audit, and what's the governance so I know it'll still be maintained and trustworthy in two years?
 - Why should I carry a second credential when the provider already KYCs me and screens the sequence: what do I personally get that I don't have today?

---

## AI-safety + biosecurity policymaker / legislative-and-standards staffer (enforceability-first)
id: policy-staffer-biosec-enforceability-v1

WHO: A mid-to-senior policy professional who drafts or advises on the operative text of biosecurity instruments: a US Senate/House committee staffer who worked the DNA-synthesis screening provisions (the S.3741-style "Securing Gene Synthesis Act" lineage), or a UK DSIT/biosecurity-strategy official, or an EU official scoping the Biotech Act / dual-use controls, or a standards-body / NTI|bio / IBBIS / Nuclear Threat Initiative type who turns norms into auditable requirements. Not a coder, not a bench scientist, not a VC. They think in terms of: who is the regulated entity, what is the legal obligation, who attests, who audits, what is the penalty, and how does this survive a hostile compliance lawyer and a determined evader. They read the HHS Screening Framework Guidance, the 2023 EO 14110 / OSTP screening provisions, the Australia Group control lists, and the IBBIS Common Mechanism as their baseline reality. They have watched many well-meaning technical demos die because they had no path into procurement, statute, or an existing standard. They are time-poor, allergic to hype, and personally accountable if they champion something that later fails publicly.

VALUES:
 - Enforceability: a clean mapping from the tool to an actual obligation (screening mandate, KYC/customer-vetting duty, recordkeeping requirement) and to who would be compelled to use it and under what authority
 - Standards alignment and interoperability: built on real specs (W3C VC/DID) and ideally mappable to NIST, ISO/TC 276, the IBBIS Common Mechanism, and existing X.509-based ECS so it can ride existing rails rather than create a fork
 - Honest, bounded scope claims: they reward the project for stating plainly that it sits ON TOP of sequence screening, never replaces it, and covers only the acquire-materials node on compliant providers (fraud/attribution/deterrence), not screening, benchtop, or insiders
 - Disclosed limitations stated up front: the explicit cross-batch volume/timing leakage admission and 'no ZK yet' and 'prototype, in-memory, no durability' raise trust rather than lower it
 - Vendor-neutrality and openness as a governance property: Apache-2.0 + open W3C form generalizing SecureDNA ECS means no single-vendor lock-in and a credible answer to 'what if the vendor is acquired or goes closed' (the Aclid/Ginkgo cautionary tale)
 - A coherent threat model with an adversary section: who is being deterred, what attack it stops, what it explicitly does NOT stop
 - Auditability and tamper-evidence that a regulator or third-party auditor could actually verify, plus revocation that works (revocable exemption credentials, not perpetual tokens)
 - Privacy-by-design that survives legal scrutiny (salted hashing, selective disclosure) because researcher identity + order data is sensitive and a centralized honeypot is itself a biosecurity and civil-liberties risk
 - Adoption realism: a believable answer to why a compliant DNA-synthesis provider (Twist, IDT, GenScript) or a consortium would actually deploy this
 - Internationality: works across US/UK/EU jurisdictions and for cross-border orders, because synthesis supply chains and evaders are global

REJECTS ON:
 - Solutionism that ignores the binding constraint: pitching identity/audit as if the gap in biosecurity is identity, when the hard, contested gap is sequence screening coverage and enforcement of the screening mandate itself
 - Any hint it could be read as a substitute for or distraction from screening, or that it gives false assurance ('security theater') that a non-screening provider could wave around
 - No adoption pathway: a prototype with no regulated entity obliged to use it, no provider committed, no standards body engaged, no procurement hook, no path from GitHub repo to mandate or to a real provider integration
 - Unmanaged residual risk presented as solved: if the cross-batch volume/timing leakage, the in-memory non-durability, or the ~4.4 ops/s ceiling were hidden or hand-waved, instant credibility loss; equally, claiming privacy guarantees stronger than the math supports
 - Infohazard carelessness: a tool, paper, or repo that itself teaches evasion, leaks order patterns, or normalizes data flows that adversaries could exploit; they will scrutinize the 'infohazard guard' claim hard
 - Reinventing instead of generalizing: if it forked away from SecureDNA ECS / IBBIS Common Mechanism rather than interoperating, creating a competing silo that fragments the ecosystem
 - Centralization or single-vendor capture risk: a KYC honeypot, or dependence on one company's closed engine (they will probe why AttestixEngine exists and whether the 'vendor-neutral' claim is real given the same founder ships Attestix)
 - Crypto/Web3 framing or buzzword identity ('walletless custody', DID) presented as novel magic rather than boring plumbing; they distrust blockchain-adjacent pitches in safety contexts
 - Scope creep into clearance/authorization: identity-only is fine, but any drift toward 'this vouches the researcher is trustworthy/cleared' is a red line they will not accept
 - Maturity mismatch: asking to be treated as deployable infrastructure while being a 592-LOC prototype; they are fine funding a prototype as a prototype, but reject prototypes dressed as production
 - Unverified competitive or impact claims: cost figures, 'gold standard' framing, or 'no one else combines X' assertions without citation or a clear-eyed read of why incumbents made different choices

ALWAYS ASKS:
 - Who is the regulated entity here, and under what existing or proposed legal authority would they be compelled to use this, versus adopt it voluntarily?
 - How does this interoperate with the IBBIS Common Mechanism and SecureDNA's ECS rather than fragment the ecosystem? What happens to existing X.509 ECS tokens?
 - You sit on top of screening, not replacing it, good, but what stops a provider from using this as a fig leaf to claim compliance without actually screening sequences?
 - What exactly does the tamper-evident audit prove to a regulator or third-party auditor, and what does the disclosed cross-batch volume/timing leakage let an adversary or an honest provider infer?
 - What is the concrete adoption path: which compliant provider or consortium has committed, or what procurement/standards/legislative hook gets this from a public repo into actual orders?
 - Identity-only with no clearance, good, but how do you guarantee no one downstream treats the credential as an authorization or trust signal it was never meant to be?
 - What is your infohazard model: does the repo, the IEEE paper, or the audit data itself teach evasion or leak sensitive order patterns, and who reviewed that?
 - Vendor-neutral is the pitch, but the same author ships the optional AttestixEngine; what is the real default-path dependency, and would a provider have to trust any single vendor?
 - What is the residual-risk and abuse story for the part you explicitly do not cover (insiders, non-compliant providers, benchtop synthesis), and are you confident this does not just push adversaries to those channels?
 - It is a 592-LOC in-memory prototype at ~4.4 ops/s; what is the realistic path to durable, auditable, production-grade infrastructure, and what would the grant actually buy at that stage?
 - Does this work across US, UK, and EU jurisdictions and for cross-border orders, and how does it handle conflicting data-protection and recordkeeping regimes?
 - If you disappeared or the project went unmaintained, what is the governance and continuity story, given the Aclid-into-Ginkgo precedent of safety tooling going closed after acquisition?

---

