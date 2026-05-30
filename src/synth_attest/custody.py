"""Customer credential custody (the [critical] adoption blocker from USER_FLOW.md).

Synthesis customers are biologists, not wallet operators. If they must create and manage a DID
and keys, step 1 of the flow never happens. This module provides a CUSTODIAL issuer: the
provider (or a neutral registry) holds the customer's DID/key material server-side, keyed by a
stable customer identifier (e.g. a verified email), so the customer never touches a wallet.

Design notes / alternatives (USER_FLOW.md, T012b):
  - provider-custodied (this module): lowest friction, no new dependency, no lock-in. The
    custodian is the engine; the customer is referenced by a handle. Trade-off: custody trust
    sits with the provider/registry (acceptable - they already hold the customer relationship).
  - magic-link / self-custody-later: a follow-on; the customer can take control of their DID
    by rotating to a key they hold. Out of scope for this prototype.
This module is intentionally engine-agnostic (works with StubEngine or AttestixEngine).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Optional

from .engine import CredentialEngine
from .schemas import researcher_identity_claims, exemption_claims


def _handle(customer_email: str) -> str:
    """Stable, non-reversible handle for a customer (do not store raw email as the key)."""
    return "cust_" + hashlib.sha256(customer_email.strip().lower().encode()).hexdigest()[:16]


@dataclass
class CustodialRegistry:
    """Holds customer DIDs server-side so the customer never manages keys. One registry instance
    per custodian (provider or neutral body). Backed by whatever CredentialEngine is configured."""

    engine: CredentialEngine
    _dids: dict = field(default_factory=dict)  # handle -> did

    def enroll_customer(self, customer_email: str) -> str:
        """Idempotent: create-and-custody a DID for this customer if absent; return the handle.
        The customer does nothing except be a verified email/identity to the provider."""
        h = _handle(customer_email)
        if h not in self._dids:
            self._dids[h] = self.engine.create_did()
        return h

    def did_for(self, handle: str) -> Optional[str]:
        return self._dids.get(handle)

    def issue_identity(self, *, handle: str, issuer_did: str, full_name: str, institution: str,
                       ror_id: str = None, orcid: str = None) -> dict:
        did = self._dids[handle]
        claims = researcher_identity_claims(full_name=full_name, institution=institution,
                                            ror_id=ror_id, orcid=orcid)
        return self.engine.issue(issuer_did=issuer_did, subject_did=did, claims=claims,
                                 credential_type="ResearcherIdentityCredential")

    def issue_exemption(self, *, handle: str, provider_did: str, sequence_class: str,
                        provider_name: str, valid_until: str, order_ref: str = None) -> dict:
        did = self._dids[handle]
        claims = exemption_claims(customer_did=did, sequence_class=sequence_class,
                                  provider=provider_name, valid_until=valid_until,
                                  order_ref=order_ref)
        return self.engine.issue(issuer_did=provider_did, subject_did=did, claims=claims,
                                 credential_type="ExemptionCredential")

    def present_on_behalf(self, *, handle: str, credentials: list, disclose: list,
                          audience_did: str = "", challenge: str = "") -> dict:
        """Custodian builds a selective-disclosure presentation on the customer's behalf - the
        customer never holds keys, yet a valid exemption can still be proven to a verifier."""
        did = self._dids[handle]
        return self.engine.present(holder_did=did, credentials=credentials, disclose=disclose,
                                   audience_did=audience_did, challenge=challenge)
