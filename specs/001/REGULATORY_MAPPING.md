# Cross-Jurisdiction Regulatory Mapping (T022 / SC-003 / FR-004)

Per-field trace from the attestix-biosec credentials and audit record to named regulatory
obligations. Each row is marked VERIFIED (confirmed against primary/authoritative text) or
UNVERIFIED (claimed but not yet confirmed, or instrument still in draft). Honesty discipline
(Constitution Principle V): a field with no obligation does not ship; an UNVERIFIED row may not
be used in any external/marketing claim until confirmed with the source body.

Fact-checks below incorporate the biosecurity domain-expert review (REVIEW_FINDINGS.md), which
verified the instruments via primary sources on 2026-05-30.

## Instruments and their current legal force

| Instrument | Status | Force | Source |
|---|---|---|---|
| US S.3741 Biosecurity Modernization & Innovation Act 2026 | VERIFIED exists | BILL (directs future Commerce rulemaking; NOT yet live law) | congress.gov/bill/119th-congress/senate-bill/3741/text |
| US OSTP / NIH framework (NOT-OD-25-012) | VERIFIED | FRAMEWORK (funding-conditioned for federally-funded research) | aspr.hhs.gov OSTP Framework page |
| UK DSIT screening guidance (8 Oct 2024) | VERIFIED | GUIDANCE (not hard law; verify identity, retain >=3y, refresh <=18mo) | gov.uk uk-screening-guidance-on-synthetic-nucleic-acids |
| EU Biotech Act Art. 44 (KYC) / Art. 45 (benchtop) | UNVERIFIED numbering | PROPOSAL (Commission adopted 16 Dec 2025; article numbers may shift before adoption) | EU Biotech Act proposal |
| ISO 20688-2:2024 | VERIFIED exists | STANDARD - but it is a DNA-MANUFACTURING quality+screening standard, NOT an identity/credential schema | iso.org/standard/75852.html |
| IGSC Harmonized Screening Protocol v3.0 (Sept 2024) | VERIFIED | INDUSTRY PROTOCOL; database = Regulated Pathogen Database (RPD) | genesynthesisconsortium.org |
| India RCGM / BWC | UNVERIFIED applicability | RCGM governs GMO/recombinant approvals, NOT synthesis-order screening; no Indian synthesis mandate yet | aspirational only |
| NTI Biosecurity Data Levels (BDL) | REFUTED as a clearance model | tiers DATA sensitivity, not researcher clearance - DROPPED from schema | - |

## ResearcherIdentityCredential field map

| Field | Obligation | Status | Note |
|---|---|---|---|
| fullName | UK DSIT "verify the identity of the customer"; EU Art.44 identity | VERIFIED (UK), UNVERIFIED (EU numbering) | |
| institution | UK DSIT legitimacy of customer/institution | VERIFIED | |
| credentialPurpose | honesty marker = "identity-affiliation-only" (scopes the credential) | N/A | enforces Principle V: not a clearance |
| rorId | operational (institutional identity); not a named legal requirement | N/A | helps legitimacy assessment; reused as BioSecure/IBBIS do |
| orcid | operational (researcher identity); not legally mandated | N/A | |
| notAClearance=true | honesty guard (Principle V): credential asserts identity, not authorization | N/A | prevents misreading identity as clearance |

NOTE: identity fields are anchored to UK DSIT + (provisionally) EU Art.44, NOT to ISO 20688-2.
ISO 20688-2 specifies no customer-credential fields - mapping identity fields to it would be a
category error (domain-expert [critical] finding). ISO 20688-2 applies on the screening/
production side only (the adapter context).

## ExemptionCredential field map

| Field | Obligation / model | Status | Note |
|---|---|---|---|
| customerDid | S.3741 / UK DSIT "who is the customer" - binds the exemption to the verified customer | VERIFIED (US, UK) | links exemption to the ResearcherIdentityCredential subject |
| sequenceClass | SecureDNA Exemption Certification System (per-class authorization); a CLASS label, never a sequence | VERIFIED (model) | infohazard guard enforces no sequence |
| issuingProvider | S.3741 / OSTP recordkeeping: provider is issuer-of-record and accountable | VERIFIED (US framework) | clearance decision stays provider-local (liability) |
| validUntil | UK DSIT refresh <=18 months; exemptions are time-bound | VERIFIED | |
| revocable=true | exemptions are revocable in practice (SecureDNA ECS) | VERIFIED (model) | reconciled with offline verify via status check |
| orderRef | OSTP/S.3741 per-order recordkeeping | VERIFIED (US framework) | |

## OrderAuditRecord field map

| Field | Obligation | Status | Note |
|---|---|---|---|
| order_id + provider_did | S.3741 / OSTP / UK DSIT recordkeeping (who, which order) | VERIFIED (US, UK) | |
| verdict (opaque) | screening decision record; OSTP "maintain secure records" | VERIFIED | verdict kept off the customer path (FR-006 anti-evasion) |
| salted-hash anchor | tamper-evidence (Constitution III) reconciled with no-metadata-leak (IV) | DESIGN | not a named legal requirement; design choice for verifiability without leakage |
| screening_source | provenance of the screening decision | operational | |

## Carry-forward unknowns (must resolve before external claims)
1. EU Biotech Act Art. 44/45 numbering - confirm against enacted text before citing the article.
2. India RCGM mapping - do NOT map fields to RCGM; mark aspirational until an Indian synthesis
   mandate exists.
3. S.3741 is a BILL - phrase all US claims as "converging on mandating", never "now mandates".
4. ISO 20688-2 exact normative text is paywalled - mappings here are scope-level, not clause-level
   verified; obtain the standard before claiming clause-level conformance.
