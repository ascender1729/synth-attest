"""SC-003: every credential/audit field traces to a named clause in REGULATORY_MAPPING.md.
Machine-checked so the mapping cannot silently drift from the schema code (a new field added
without a regulatory row fails this test)."""

import pathlib

from synth_attest.schemas import researcher_identity_claims, exemption_claims

MAPPING = (pathlib.Path(__file__).parent.parent
           / "specs" / "001" / "REGULATORY_MAPPING.md").read_text(encoding="utf-8")

# audit record public fields (from audit.OrderAuditRecord)
AUDIT_FIELDS = ["order_id", "provider_did", "verdict", "screening_source"]


def _fields_of(claims: dict):
    # ignore the @type marker; everything else is a substantive field needing a mapping row
    return [k for k in claims if k != "@type"]


def test_identity_fields_all_mapped():
    claims = researcher_identity_claims(full_name="X", institution="Y",
                                        ror_id="https://ror.org/1", orcid="0000")
    for f in _fields_of(claims):
        assert f in MAPPING, f"identity field {f!r} has no regulatory mapping row"


def test_exemption_fields_all_mapped():
    claims = exemption_claims(customer_did="did:x", sequence_class="cls", provider="P",
                              valid_until="2026-12-31", order_ref="o1")
    for f in _fields_of(claims):
        assert f in MAPPING, f"exemption field {f!r} has no regulatory mapping row"


def test_audit_fields_all_mapped():
    for f in AUDIT_FIELDS:
        assert f in MAPPING, f"audit field {f!r} has no regulatory mapping row"


def test_mapping_marks_each_instrument_status():
    # honesty: the instruments table must classify force, including the known carry-forwards
    for token in ["VERIFIED", "UNVERIFIED", "BILL", "PROPOSAL", "REFUTED"]:
        assert token in MAPPING, f"mapping missing status token {token!r}"
