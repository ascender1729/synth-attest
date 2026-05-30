# Verified citations (live arXiv API, 2026-05-30)

Checked via export.arxiv.org/api/query (script: specs/001/verify_citations.py). Each entry below
was confirmed by id or title against the live API, or explicitly marked as non-arXiv to verify
elsewhere. Do not cite anything not on this list without re-running the check.

## CONFIRMED on arXiv (id verified, real title + authors)
- **arXiv 2403.14023v3** - "A system capable of verifiably and privately screening global DNA
  synthesis" (SecureDNA). Authors include Baum, Berlips, Chen, Cozzarini, Cui, Damgard, Esvelt,
  Foner, Gretton, ... Rivest, Sage-Ling, Shamir, ... Vaikuntanathan, ... Yao, Yu, ... This is the
  gold-standard prior art (Turing-laureate cryptographers Rivest/Shamir/Yao). We GENERALIZE its
  Exemption Certification System into an open W3C-VC form; we do not compete with its screening.
- **arXiv 2602.06172v1** - "Know Your Scientist: KYC as Biosecurity Infrastructure" (Jonathan
  Feldman, Tal Feldman, Annie I. Anton). The leading KYC-for-biosecurity policy proposal; governs
  AI-tool access (a different chokepoint) via institution-vouching + exclusion lists; no VC/DID.
- **arXiv 2506.11613** - "Model Organisms for Emergent Misalignment" (Turner, Soligo, Taylor,
  Rajamanoharan, Nanda). Belongs to the operator's SEPARATE AI-safety track, not this bio project.

## CONFIRMED prior art for VC/blockchain KYC (found during verification - cite to ground our
## standards approach; shows self-sovereign-identity KYC is established, not exotic)
- **arXiv 2001.01659** - "KYChain: User-Controlled KYC Data Sharing and Certification" (Dragan,
  Manulis).
- **arXiv 2112.01237** - "Designing a Framework for Digital KYC Processes Built on Blockchain-Based
  Self-Sovereign Identity" (Schlatt, Sedlmeir, Feulner, Urbach).

## NOT on arXiv - cite via the correct primary venue (do NOT cite as arXiv)
- Microsoft "Paraphrase Project" - **Science (Oct 2025)**. AI-designed toxin variants evaded
  vendor screening (one tool missed >75% of ~76,000 variants before patching). Our motivation.
- W3C Verifiable Credentials Data Model + DID Core - **w3.org Recommendations**.
- US S.3741 Biosecurity Modernization and Innovation Act - **congress.gov** (a BILL, not law).
- UK DSIT synthetic-nucleic-acid screening guidance - **gov.uk** (in force, 2024).
- ISO 20688-2:2024 - **iso.org** (DNA-manufacturing quality+screening standard; NOT an identity schema).

## Honesty notes
- The Microsoft Paraphrase work is Science-only; an arXiv title search returned unrelated papers,
  so it must never be cited with an arXiv id.
- 2602.06172 uses the 2026 arXiv id scheme (YYMM = Feb 2026), consistent with its publication date.
