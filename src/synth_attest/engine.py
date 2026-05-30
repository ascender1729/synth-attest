"""Swappable credential engine (FR-009). AttestixEngine wraps attestix==0.4.x; StubEngine is a
dependency-free reference so contract tests prove the layer is not locked to Attestix (SC-005)."""

from __future__ import annotations

import abc
import hashlib
import hmac
import json
import uuid
from typing import Optional


def _first(d, *keys, default=None):
    if not isinstance(d, dict):
        return default
    for k in keys:
        if d.get(k) is not None:
            return d[k]
    return default


class CredentialEngine(abc.ABC):
    name = "abstract"

    @abc.abstractmethod
    def create_did(self) -> str: ...

    @abc.abstractmethod
    def issue(self, *, issuer_did: str, subject_did: str, claims: dict,
              credential_type: str, expiration: Optional[str] = None) -> dict: ...

    @abc.abstractmethod
    def verify(self, credential: dict) -> bool: ...

    @abc.abstractmethod
    def revoke(self, *, credential_id: str, issuer_did: str) -> None: ...

    @abc.abstractmethod
    def cred_id(self, credential: dict) -> Optional[str]: ...

    # US5: selective-disclosure presentation. Default raises so an engine that cannot do it is
    # explicit rather than silently wrong.
    def present(self, *, holder_did: str, credentials: list, disclose: list,
                audience_did: str = "", challenge: str = "") -> dict:
        raise NotImplementedError("engine does not support presentations")

    def verify_presentation(self, presentation: dict) -> bool:
        raise NotImplementedError("engine does not support presentations")


class AttestixEngine(CredentialEngine):
    """Real backend. Auto-detects the attestix surface (verified 2026-05-30):

    - SERVICE layer (published 0.4.0rc2 and the stable line): DIDService / CredentialService.
      issue -> {credential_id, credential, status}; verify_credential_external(body) checks the
      signature (catches tampering); verify_credential(id) checks status (catches revocation).
      This is the portable, published surface and is preferred.
    - FUNCTIONAL tools (rc3 dev tree): did_tools.create_did_key(repo, signer=...), etc.

    Both satisfy the same CredentialEngine contract."""

    name = "attestix"

    def __init__(self):
        if self._try_service_layer():
            self._mode = "service"
            return
        if self._try_functional_tools():
            self._mode = "functional"
            return
        raise RuntimeError(
            "no usable attestix surface found (neither services.CredentialService nor "
            "functional did_tools.create_did_key)."
        )

    # ---- service layer (rc2 / stable) ----
    def _try_service_layer(self) -> bool:
        try:
            from attestix.services.credential_service import CredentialService
            from attestix.services.did_service import DIDService
        except Exception:
            return False
        if not hasattr(CredentialService, "issue_credential"):
            return False
        signer = self._build_signer()
        self._dids = DIDService()
        # One CredentialService instance: revoke + status-verify must share state.
        try:
            self._cs = CredentialService(signer=signer)
        except TypeError:
            self._cs = CredentialService()
        return True

    # ---- functional tools (rc3 dev tree) ----
    def _try_functional_tools(self) -> bool:
        try:
            from attestix.tools import credential_tools, did_tools
        except Exception:
            return False
        if not hasattr(did_tools, "create_did_key"):
            return False
        try:
            from attestix.storage.memory_repository import MemoryRepository as _Repo
        except ImportError:
            try:
                from attestix.storage.memory_repository import InMemoryRepository as _Repo
            except Exception:
                return False
        self._repo = _Repo()
        self._signer = self._build_signer()
        self._did = did_tools
        self._credt = credential_tools
        return True

    @staticmethod
    def _build_signer():
        # A retaining key_store keeps the issuer key resolvable at verify time
        # (default store surfaces verify -> "unknown_issuer_key" on the functional tools).
        try:
            from attestix.signing.inprocess_signer import InProcessSigner
            try:
                return InProcessSigner(key_store={})
            except TypeError:
                return InProcessSigner()
        except Exception:
            return None

    def create_did(self) -> str:
        if self._mode == "service":
            r = self._dids.create_did_key()
        else:
            r = self._did.create_did_key(self._repo, signer=self._signer)
        did = _first(r, "did", "id")
        if not did and isinstance(r, dict):
            did = _first(r.get("did_document", {}), "id") or _first(r.get("didDocument", {}), "id")
        return did

    def issue(self, *, issuer_did, subject_did, claims, credential_type, expiration=None):
        if self._mode == "service":
            # rc2: issuer is the service identity; issuer_did is recorded as issuer_name.
            r = self._cs.issue_credential(
                subject_id=subject_did, credential_type=credential_type,
                issuer_name=issuer_did or "attestix-biosec", claims=claims,
            )
        else:
            r = self._credt.issue_credential(
                self._repo, issuer_did=issuer_did, subject_did=subject_did,
                claims=claims, credential_type=credential_type,
                expiration=expiration, signer=self._signer,
            )
        cred = _first(r, "credential", default=r)
        outer_id = _first(r, "credential_id", "credentialId")
        if isinstance(cred, dict) and outer_id and not _first(cred, "id", "credentialId", "@id"):
            cred = {**cred, "_attestix_credential_id": outer_id}
        return cred

    def verify(self, credential) -> bool:
        if self._mode == "service":
            body = {k: v for k, v in credential.items() if k != "_attestix_credential_id"}
            # 1. signature check on the body catches any tampering.
            ext = self._cs.verify_credential_external(body)
            if not bool(_first(ext, "verified", "valid", "ok", default=False)):
                return False
            # 2. if we know the credential id, the status check catches revocation/expiry.
            cid = _first(credential, "_attestix_credential_id", "credential_id", "id")
            if cid:
                try:
                    st = self._cs.verify_credential(cid)
                    return bool(_first(st, "verified", "valid", "ok", default=False))
                except Exception:
                    pass
            return True
        # functional
        r = self._credt.verify_credential(self._repo, credential=credential)
        if isinstance(r, bool):
            return r
        return bool(_first(r, "verified", "valid", "ok", default=False))

    def revoke(self, *, credential_id, issuer_did) -> None:
        if self._mode == "service":
            self._cs.revoke_credential(credential_id, reason="revoked by attestix-biosec")
        else:
            self._credt.revoke_credential(
                self._repo, credential_id=credential_id, issuer_did=issuer_did)

    def cred_id(self, credential):
        return _first(credential, "id", "credentialId", "@id", "_attestix_credential_id")

    def present(self, *, holder_did, credentials, disclose, audience_did="", challenge=""):
        if self._mode != "service":
            raise NotImplementedError("presentations require the attestix service layer")
        # Never present a revoked/invalid credential (matches StubEngine; rc2's
        # create_verifiable_presentation does not itself re-check status).
        for c in credentials:
            if not self.verify(c):
                raise ValueError("cannot present an invalid/revoked credential")
        cids = [self.cred_id(c) for c in credentials if self.cred_id(c)]
        r = self._cs.create_verifiable_presentation(holder_did, cids, audience_did, challenge)
        return _first(r, "presentation", default=r)

    def verify_presentation(self, presentation) -> bool:
        if self._mode != "service":
            raise NotImplementedError("presentations require the attestix service layer")
        r = self._cs.verify_presentation(presentation)
        return bool(_first(r, "verified", "valid", "ok", default=False))


class StubEngine(CredentialEngine):
    """Dependency-free reference engine. HMAC over canonical JSON of the credential body. Proves
    the contract (issue/verify/tamper/revoke) independently of Attestix so SC-005 (no lock-in)
    is testable."""

    name = "stub"

    def __init__(self, secret: bytes = b"synth-attest-stub"):
        self._secret = secret
        self._revoked: set[str] = set()

    def create_did(self) -> str:
        return "did:stub:" + uuid.uuid4().hex

    def _sign(self, body: dict) -> str:
        msg = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
        return hmac.new(self._secret, msg, hashlib.sha256).hexdigest()

    def issue(self, *, issuer_did, subject_did, claims, credential_type, expiration=None) -> dict:
        body = {
            "id": "urn:stub:" + uuid.uuid4().hex,
            "type": ["VerifiableCredential", credential_type],
            "issuer": issuer_did,
            "credentialSubject": {"id": subject_did, **claims},
            "expiration": expiration,
        }
        return {**body, "proof": {"type": "StubHmac2026", "value": self._sign(body)}}

    def verify(self, credential) -> bool:
        if credential.get("id") in self._revoked:
            return False
        proof = credential.get("proof") or {}
        body = {k: v for k, v in credential.items() if k != "proof"}
        return hmac.compare_digest(self._sign(body), proof.get("value", ""))

    def revoke(self, *, credential_id, issuer_did) -> None:
        self._revoked.add(credential_id)

    def cred_id(self, credential):
        return credential.get("id")

    def present(self, *, holder_did, credentials, disclose, audience_did="", challenge=""):
        """Selective disclosure: reveal ONLY the `disclose` fields from each credential's subject
        (US5 - prove a valid exemption without revealing customer/order/other fields). The proof
        binds holder + audience + challenge + the disclosed subset, so a verifier can trust the
        disclosed claims without seeing the rest."""
        disclosed = []
        for c in credentials:
            # verify the source credential is itself valid before presenting it
            if not self.verify(c):
                raise ValueError("cannot present an invalid/revoked credential")
            subj = c.get("credentialSubject", {})
            revealed = {k: subj[k] for k in disclose if k in subj}
            disclosed.append({"credentialId": c.get("id"), "disclosed": revealed,
                              "type": c.get("type")})
        body = {
            "@context": ["https://www.w3.org/2018/credentials/v1"],
            "type": ["VerifiablePresentation"],
            "holder": holder_did,
            "audience": audience_did,
            "challenge": challenge,
            "verifiableCredential": disclosed,
        }
        return {**body, "proof": {"type": "StubHmac2026", "value": self._sign(body)}}

    def verify_presentation(self, presentation) -> bool:
        # signature integrity of the presentation
        proof = presentation.get("proof") or {}
        body = {k: v for k, v in presentation.items() if k != "proof"}
        if not hmac.compare_digest(self._sign(body), proof.get("value", "")):
            return False
        # and none of the presented credentials are revoked
        for vc in presentation.get("verifiableCredential", []):
            if vc.get("credentialId") in self._revoked:
                return False
        return True
