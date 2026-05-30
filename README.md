# synth-attest

An open, vendor-neutral **verifiable-identity and tamper-evident audit layer for DNA-synthesis
order compliance.** It sits *on top of* sequence screening (SecureDNA, IBBIS Common Mechanism,
Battelle) and never replaces it.

This is an independent open-source project. It is an exploration of one honest question: as the
barrier to designing dangerous biological sequences drops, the synthesis-order step is a physical
chokepoint, and screening answers "is this sequence dangerous" but not "who ordered it, are they
verified, and is there a trustworthy record." synth-attest adds that missing identity + audit layer
using open W3C standards.

## What it does

- **Portable researcher identity credential** (W3C Verifiable Credential / DID) - identity and
  institutional affiliation only, NOT a clearance.
- **Provider-issued exemption credential** - authorizes a sequence *class* (never a sequence),
  time-bound and revocable, modeled on SecureDNA's Exemption Certification System. The clearance
  decision stays with the provider.
- **Privacy-preserving, tamper-evident order audit** - each order decision is recorded and a
  salted-hash commitment is anchored in fixed-size batches, so order volume, timing, and the
  screening verdict are not recoverable from what is anchored.
- **Selective-disclosure proof** - prove a valid exemption without revealing the rest of the
  credential.
- **Infohazard guard** - no sequence-like data is ever allowed into the layer (tested).

## Vendor-neutral by construction

The core has **zero proprietary dependencies**. It ships with a dependency-free reference engine
(`StubEngine`) so the whole flow runs with nothing but Python. A swappable `CredentialEngine`
interface means any W3C VC/DID backend can be plugged in; an optional `AttestixEngine` adapter
([attestix](https://pypi.org/project/attestix/)) is provided as one such backend, but it is not
required.

```bash
pip install -e .            # core only, no proprietary deps
pip install -e ".[attestix]"  # optional: enable the attestix backend
```

## Run it

```bash
pip install -e ".[dev]"
pytest -q                      # core suite (StubEngine); attestix-backed tests self-skip if absent
python demo/end_to_end.py --engine stub
```

End-to-end demo flow: researcher identity credential -> provider exemption -> external screen
(opaque verdict) -> tamper-evident anchored audit -> selective-disclosure proof -> customer receipt
(which never reveals the verdict).

## Honest scope

This layer intervenes at ONE node of the engineered-pandemic kill chain - acquire-materials, at
compliant providers - and addresses fraud, attribution, and deterrence. It does **not** screen
sequences, does **not** stop benchtop or non-compliant synthesis, and does **not** stop a
genuinely-credentialed malicious insider. It is one layer, not a guarantee. See
`specs/001/spec.md` and `specs/001/REGULATORY_MAPPING.md`.

## Status

Early-stage prototype. Tests pass in CI on Python 3.11 and 3.12 (core with no proprietary deps;
a second job validates the optional attestix backend source-blind against the published wheel).

## License

Apache-2.0.
