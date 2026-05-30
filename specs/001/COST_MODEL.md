# synth-attest cost model (honest, all figures are labeled estimates)

Question: if a DNA-synthesis provider or a researcher USES synth-attest, do they save money?

Verdict (from the 2026-05-30 financial audit, confidence medium): YES, but MODESTLY and
INDIRECTLY. The real saving is avoided per-provider re-onboarding for researchers who order from
multiple providers, plus near-zero running cost. It is NOT a large single-provider ROI, and any
hard-dollar ROI claim is not yet defensible without deployment data. Numbers below are
order-of-magnitude estimates with stated assumptions, not measured results.

## Reference points (sourced)
- Customer screening / KYC cost: Aclid reports AI-assisted KYC at ~$1.18/customer vs ~$14.04
  manual (bioRxiv 2026.02.27.708645). This anchors the screening-side per-customer cost.
- SecureDNA sequence screening: free.
- IDV vendors (Veriff/Persona-class): ~$1-2 per identity verification (public pricing ranges).
- S.3741 proposes penalties for non-compliance (penalty-avoidance is a real but SPECULATIVE
  driver while the bill is not law).

## Where synth-attest changes cost
| Cost item | Without synth-attest | With synth-attest | Who saves |
|---|---|---|---|
| Researcher onboarding at provider #2..N | Re-verify identity each time (~$1-14 each + days of researcher/admin time) | Present an already-issued portable identity VC | Researcher + provider |
| Order-audit recordkeeping | Per-provider ad hoc logs | Standard signed record + one hash anchor per batch of 16 | Provider |
| Anchoring/compute | n/a | One SHA-256 root per 16 orders; effectively free on commodity compute | - |
| Identity/VC infra | n/a | Open-source, zero proprietary deps (StubEngine) or optional backend | Provider |
| Custody hosting | n/a | A small keyed-handle DID store; low | Provider |

## Honest net
- For a RESEARCHER ordering across k providers: re-onboarding is paid ~once instead of k times.
  If onboarding is ~$1-14 plus hours of back-and-forth, the saving scales with k and with the
  admin-time component (often the larger cost).
- For a SINGLE provider in isolation: the saving is marginal; synth-attest is adopted for
  compliance + auditability, not primarily for cost reduction. Do not pitch single-provider ROI.
- Running cost is near-zero (hashing), so the value question is friction/compliance, not opex.
- Penalty-avoidance could dominate the model IF S.3741 passes with its proposed penalties, but
  that is speculative today and must be labeled as such.

## What would make this defensible
A pilot with one provider measuring (a) onboarding hours saved per repeat researcher, (b) actual
anchor/hosting cost at real volume. Until then: "low running cost + avoided re-onboarding
friction", with numbers as estimates.
