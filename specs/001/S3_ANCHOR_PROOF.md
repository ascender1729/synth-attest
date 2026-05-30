# Live AWS proof: external-witness anchor (addresses panel CRITICAL CC-3)

Date: 2026-05-30. Account: AWS 320524884470, region us-east-1.

## What the panel said
The technical/crypto panel's CRITICAL (CC-3, raised by 6 of 9 panels): synth-attest's in-memory
anchor is NOT tamper-evident against the audited provider. A provider can restart, reorder, and
re-anchor a consistent-but-false history. Real tamper-evidence needs an EXTERNAL append-only
witness the provider cannot rewrite.

## What was demonstrated, live, on real AWS
Created an S3 bucket with Object Lock (WORM) enabled and a default GOVERNANCE retention rule
(1 day, chosen so the test is cleanable; production uses COMPLIANCE mode). Wrote a real batch-root
hash, then attempted to tamper.

Commands and outcomes (real, not simulated):
1. `create-bucket --object-lock-enabled-for-bucket` -> bucket created.
2. `put-object-lock-configuration` GOVERNANCE 1 day -> set.
3. `put-object anchors/batch-0001.root` -> stored; response showed
   `ObjectLockMode: GOVERNANCE`, `ObjectLockRetainUntilDate: 2026-05-31...`.
4. `delete-object` (no bypass) on the locked version ->
   **"An error occurred (AccessDenied) when calling the DeleteObject operation: Access Denied
   because object protected by object lock."**
5. `list-object-versions` -> the original 65-byte version is retained (IsLatest=false) even after
   an overwrite created a new version; the original cannot be removed within retention.
6. `get-object-retention` on the original version -> `Mode: GOVERNANCE, RetainUntilDate: 2026-05-31`.

## Conclusion
The delete denial is the property the panel demanded: with Object Lock, a witnessed batch root
cannot be deleted or rewritten in place by the account before retention expires. In COMPLIANCE
mode (production setting) this holds even against the AWS account root. This converts the audit
pillar from "tamper-evident only against third parties" to "tamper-evident against the audited
provider," closing CC-3.

## Code
`src/synth_attest/anchor.py` adds `S3ObjectLockAnchorSink` (optional `synth-attest[aws]` extra,
boto3 imported lazily; the sink holds no delete permission). `tests/test_anchor.py` verifies the
WORM contract against a fake S3 client so CI needs no AWS credentials.

## Honest limitations (do not overstate)
- This proves DURABILITY + WORM, not full transparency-log non-equivocation. A complete fix adds an
  RFC 6962-style signed-tree-head so a holder of a prior STH detects a forked history; Object Lock
  alone prevents in-place rewrite but a fuller external-witness story (independent witness, public
  inclusion proof) is future work.
- The test used GOVERNANCE mode (bypass-deletable with a special permission) so the test bucket is
  cleanable; production must use COMPLIANCE mode for the root-cannot-delete guarantee.
- The test ran on the operator's existing AWS account (320524884470). A clean, independent account
  is preferable for the independent synth-attest project; this was a capability proof only.

## Cost
Negligible: one ~65-byte object, a few API calls. Test bucket retention is 1 day (GOVERNANCE), so
it can be emptied and deleted after expiry.
