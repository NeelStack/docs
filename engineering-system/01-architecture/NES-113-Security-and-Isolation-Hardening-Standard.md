---
document_id: NES-113
title: Security & Isolation Hardening Standard
subtitle: RLS Correctness, Envelope Encryption, and Offline Licensing for Air-Gapped Deployments
version: 1.0.0
status: Draft — Pending Review
classification: Internal — Security Sensitive
owner: Chief Solution Architect / Security Lead
review_cycle: Every 6 Months
document_type: Architecture Decision Record (ADR)
parent_document: NES-111 Multi-Tenant Deployment Strategy
next_document: NES-114 API Gateway Standards
---

# NES-113 — Security & Isolation Hardening Standard

> **"A cross-tenant data leak in an education platform is not an incident. It's the incident that ends the company."**

---

# 1. Problem Statement

Review of NES-110/111 surfaced three findings that must be closed before any tenant is marked production-hardened. These are ordered by blast radius, not by convenience of implementation.

1. **RLS transaction-scoping risk** — `SET LOCAL app.current_tenant_id` is transaction-scoped. If a connection returns to the pool without a guaranteed commit/rollback boundary, the next tenant's request can inherit the previous tenant's session variable on the same physical connection — defeating RLS entirely under load.
2. **No `FORCE ROW LEVEL SECURITY`** — `ENABLE ROW LEVEL SECURITY` alone does not apply to the table owner. If the application connects using the owning role (a common default), RLS policies are silently bypassed for all application traffic.
3. **Single master key for credential encryption** — `EncryptedString` uses one AES key for all dedicated-tenant DB credentials. Compromise of that single key (or the secret store holding it) exposes every dedicated-cloud client's database credentials simultaneously.
4. **Vector store has no enforced isolation** — `document_vectors` relies on the application remembering a `WHERE school_id = ...` filter, which is exactly the anti-pattern NES-111 itself warns against elsewhere.
5. **Licensing contradicts the "air-gapped" claim** — self-hosted licensing requires periodic phone-home to a central endpoint. A genuinely air-gapped customer (no outbound internet — a realistic requirement for government/defense education deployments) can never satisfy this, making "air-gapped" marketing language rather than a supported deployment mode.

---

# 2. Decision: RLS Transaction Correctness

## 2.1 Guaranteed transaction boundary

`SET LOCAL` must execute inside a transaction that is *always* committed or rolled back before the session object is released back to the pool — including on exception paths. The current `get_tenant_db` context manager in NES-111 does not make this guarantee explicit.

```python
# services/core/src/app/shared/database.py

from contextlib import asynccontextmanager
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared.models import TenantContext

@asynccontextmanager
async def get_tenant_db(tenant: TenantContext) -> AsyncSession:
    if tenant.deployment_model == "saas_rls":
        async with AsyncSession(_shared_engine) as session:
            async with session.begin():  # explicit transaction — guarantees commit/rollback below
                await session.execute(
                    text("SET LOCAL app.current_tenant_id = :tid"),
                    {"tid": tenant.id}
                )
                try:
                    yield session
                except Exception:
                    # session.begin() context manager rolls back automatically on exception,
                    # which discards the SET LOCAL value before the connection returns to pool
                    raise
            # commit (or rollback) has occurred here — SET LOCAL scope is guaranteed cleared
    # ... schema_isolated / dedicated branches unchanged from NES-111,
    # but schema_isolated gets the identical session.begin() wrapping treatment
```

**Key change from NES-111's version:** the `SET LOCAL` call and the yielded work now live inside `session.begin()`, not a bare `AsyncSession` block. This ensures SQLAlchemy commits or rolls back the transaction — and therefore clears the `SET LOCAL` value — before the connection is returned to `_shared_engine`'s pool, regardless of whether the request handler raised.

## 2.2 `FORCE ROW LEVEL SECURITY`

```sql
-- Applied to every shared, RLS-protected table
ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE students FORCE ROW LEVEL SECURITY;   -- applies RLS even to the table owner

ALTER TABLE enrollments ENABLE ROW LEVEL SECURITY;
ALTER TABLE enrollments FORCE ROW LEVEL SECURITY;

ALTER TABLE grades ENABLE ROW LEVEL SECURITY;
ALTER TABLE grades FORCE ROW LEVEL SECURITY;
```

## 2.3 Dedicated, non-owner application role

```sql
-- The application must NOT connect as the table owner or a superuser
CREATE ROLE app_runtime LOGIN PASSWORD '...' NOBYPASSRLS;
GRANT SELECT, INSERT, UPDATE, DELETE ON students, enrollments, grades TO app_runtime;
-- app_runtime does NOT own these tables, and FORCE RLS + NOBYPASSRLS together
-- guarantee policies apply to every query the application issues.
```

`SHARED_DATABASE_URL` (and every dedicated/self-hosted DB URL) must connect as `app_runtime`, never as the migration/owner role. This is enforced by a startup check: the core API refuses to boot if `current_user` matches the configured table-owner role.

## 2.4 Vector store isolation

```sql
ALTER TABLE document_vectors ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_vectors FORCE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON document_vectors
    USING (school_id = current_setting('app.current_tenant_id')::uuid);
```

The application-level `WHERE school_id = ...` filter in cosine-distance queries (NES-110 §5) remains as defense-in-depth, but is no longer the *only* control. This closes the gap where `document_vectors` was the one table NES-111's own anti-pattern warning didn't actually cover in practice.

## 2.5 Mandatory isolation test suite (CI-gating, not checklist-only)

```python
# tests/test_rls_isolation.py

async def test_cross_tenant_read_returns_zero_rows(tenant_a, tenant_b):
    """
    Seeds a student record under tenant_a, then attempts to read it
    using a session context-set to tenant_b. Must return zero rows —
    not an error, not a filtered result, exactly zero rows.
    """
    async with get_tenant_db(tenant_a) as db:
        await db.execute("INSERT INTO students (id, name, tenant_id) VALUES (...)")

    async with get_tenant_db(tenant_b) as db:
        result = await db.execute("SELECT * FROM students WHERE id = :id", {"id": student_id})
        assert result.fetchall() == []

async def test_connection_pool_reuse_does_not_leak_tenant_context(tenant_a, tenant_b):
    """
    Regression test for the exact pooling bug this ADR fixes: acquires and releases
    a connection under tenant_a, then immediately acquires under tenant_b from the
    same pool, and confirms current_setting('app.current_tenant_id') reflects tenant_b.
    """
    ...

async def test_document_vectors_isolated_across_tenants(tenant_a, tenant_b):
    ...

async def test_app_role_cannot_bypass_rls_as_owner(db_owner_role):
    """
    Confirms FORCE RLS is active by attempting a query as the owner role
    and verifying it is still row-filtered, not just as app_runtime.
    """
    ...
```

This suite is a **required, blocking CI gate** on every PR touching `services/core/src/app/shared/database.py`, any RLS policy migration, or any table in the shared-schema tenant model. It is promoted from NES-111's "Production Checklist" (an aspirational list) to an enforced build gate.

---

# 3. Decision: Envelope Encryption for Dedicated-Tenant Credentials

## 3.1 Current risk

`EncryptedString` (NES-110 §4) encrypts every dedicated tenant's DB credentials with one AES symmetric key injected at runtime. This is a single point of catastrophic failure: one key compromise exposes every dedicated-cloud client's database credentials at once, with no per-tenant blast radius containment and no rotation path that doesn't require re-encrypting everything at once.

## 3.2 Envelope encryption model

```text
                    ┌─────────────────────────┐
                    │   KMS Master Key (KEK)   │   ← lives in AWS KMS / Vault / age,
                    │   never leaves the KMS   │      never touches application memory in raw form
                    └───────────┬─────────────┘
                                │ wraps
                                ▼
        ┌──────────────────────────────────────────────┐
        │  Per-record Data Encryption Key (DEK)         │
        │  Generated fresh for each tenant's credential  │
        │  record. Encrypted (wrapped) by the KEK.      │
        │  Stored alongside the ciphertext in the DB.   │
        └───────────────────┬────────────────────────────┘
                            │ encrypts
                            ▼
              tenant.dedicated_db_url (ciphertext)
```

```python
# services/core/src/app/shared/encryption.py

import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from app.shared.kms_client import kms_wrap_key, kms_unwrap_key  # KMS SDK wrapper

class EncryptedString:
    """
    Envelope-encrypted SQLAlchemy type. Each value gets its own one-time DEK,
    which is itself encrypted by the KMS-held master key (KEK). Compromising
    one DEK exposes exactly one record, not the entire credential store.
    """

    def encrypt(self, plaintext: str) -> dict:
        dek = AESGCM.generate_key(bit_length=256)
        aesgcm = AESGCM(dek)
        nonce = os.urandom(12)
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)

        wrapped_dek = kms_wrap_key(dek)  # KMS call — DEK never persisted unwrapped
        return {
            "ciphertext": ciphertext.hex(),
            "nonce": nonce.hex(),
            "wrapped_dek": wrapped_dek,
            "kek_version": kms_current_key_version(),  # supports KEK rotation, see 3.3
        }

    def decrypt(self, stored: dict) -> str:
        dek = kms_unwrap_key(stored["wrapped_dek"], key_version=stored["kek_version"])
        aesgcm = AESGCM(dek)
        return aesgcm.decrypt(
            bytes.fromhex(stored["nonce"]),
            bytes.fromhex(stored["ciphertext"]),
            None
        ).decode()
```

## 3.3 KEK rotation without a big-bang re-encryption

Because each record stores `kek_version`, rotating the master key means:
1. KMS issues a new KEK version; old versions remain available for unwrapping (standard KMS behavior).
2. New writes use the new KEK version.
3. Existing records remain decryptable via their stored `kek_version` indefinitely — no forced mass re-encryption event, though a background job may opportunistically re-wrap DEKs under the newest KEK over time.

This directly resolves the rotation gap flagged in review: previously, rotating the single AES key would have invalidated every existing ciphertext simultaneously.

## 3.4 Same pattern applies to HMAC export-signing key

The GDPR Article 15 export signature key (NES-110 §6A) moves to the same KMS-backed model — `kek_version` stored alongside each `signature.sha256`, so rotating the signing key doesn't retroactively invalidate previously issued exports.

---

# 4. Decision: Offline Asymmetric Licensing for Air-Gapped Self-Hosted

## 4.1 Problem

NES-110's licensing service validates self-hosted signatures against a central NeelStack endpoint, falling back to a 30-day offline grace period on failure. A genuinely air-gapped deployment (no outbound internet at all — the realistic case for defense/government education customers) never successfully phones home even once, meaning it perpetually runs on borrowed time rather than being a supported mode.

## 4.2 Offline license file model

```text
NeelStack (issuer)                          Customer (air-gapped server)
─────────────────                          ─────────────────────────────
Holds RSA private key                       Holds only the RSA public key
(never distributed)                         (baked into the Docker image)

Generates license.lic:
  {
    tenant_id, tenant_name,
    modules_entitled: [...],
    issued_at, expires_at,
    max_students, max_staff
  }
  signed with RSA-PSS + SHA-256
                    │
                    │  delivered out-of-band
                    │  (email, USB, portal download —
                    │   NOT a network call at runtime)
                    ▼
                                             license.py verifies signature
                                             locally using the embedded public key.
                                             No network call required, ever.
```

```python
# services/core/src/app/shared/license.py

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

PUBLIC_KEY = serialization.load_pem_public_key(EMBEDDED_PUBLIC_KEY_PEM)

def verify_license(license_payload: bytes, signature: bytes) -> LicenseInfo:
    """
    Verifies a license file's RSA-PSS signature entirely offline.
    Raises InvalidLicense if signature verification fails or expires_at has passed.
    Never makes a network call — safe for fully air-gapped deployments.
    """
    PUBLIC_KEY.verify(
        signature,
        license_payload,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256(),
    )
    info = LicenseInfo.model_validate_json(license_payload)
    if info.expires_at < datetime.utcnow():
        raise LicenseExpired(grace_period_days=30)  # existing 30-day grace period still applies
    return info
```

## 4.3 Two supported licensing modes, explicit and separate

| Mode | Mechanism | Use case |
|---|---|---|
| `networked` | Phone-home to central endpoint, 30-day offline grace fallback (existing NES-110 behavior) | Self-hosted customers with normal internet access who want centralized renewal |
| `air_gapped` | Offline `.lic` file, RSA-PSS signature, no network call ever | Government/defense/fully isolated network customers — the actual "air-gapped" claim from NES-110 §1 |

`DEPLOYMENT_LICENSING_MODE` becomes an explicit `.env` setting chosen at install time (NES-111 §"Self-Hosted Setup — 5 Commands"), rather than air-gapped support being an implicit, untested side effect of the grace period.

---

# 5. Anti-Patterns

> [!CAUTION]

❌ **Bare session block for RLS context:**
```python
# WRONG — no guaranteed transaction boundary, SET LOCAL scope is unclear on exception
async with AsyncSession(_shared_engine) as session:
    await session.execute(text("SET LOCAL app.current_tenant_id = :tid"), {"tid": tenant.id})
    yield session

# CORRECT — explicit transaction guarantees SET LOCAL is cleared before pool return
async with AsyncSession(_shared_engine) as session:
    async with session.begin():
        await session.execute(text("SET LOCAL app.current_tenant_id = :tid"), {"tid": tenant.id})
        yield session
```

❌ **Single static encryption key with no version tracking:**
```python
# WRONG — rotating this key invalidates every existing ciphertext at once
CIPHER_KEY = os.environ["MASTER_KEY"]

# CORRECT — per-record DEK wrapped by a versioned KEK, see §3
```

❌ **Treating "air-gapped" as a side effect of a grace period** rather than an explicitly designed, tested licensing mode.

---

# 6. Production Checklist

- [ ] `session.begin()` wraps every `SET LOCAL app.current_tenant_id` call; `test_connection_pool_reuse_does_not_leak_tenant_context` passes under concurrent load (minimum 50 concurrent requests across 2+ tenants on a pool size of 5)
- [ ] `FORCE ROW LEVEL SECURITY` applied to `students`, `enrollments`, `grades`, `document_vectors`, and any future shared tenant table added to the schema
- [ ] Application connects as `app_runtime` (non-owner, `NOBYPASSRLS`) in every environment, verified by a startup assertion that fails closed
- [ ] `document_vectors` has an active RLS policy, not just an application-level filter
- [ ] `EncryptedString` upgraded to per-record DEK + KMS-wrapped KEK; `kek_version` present on all new writes
- [ ] KEK rotation tested end-to-end: old records remain decryptable, new writes use new version, no forced re-encryption required
- [ ] `air_gapped` licensing mode implemented, tested with network access fully disabled in the test environment
- [ ] `test_rls_isolation.py` suite is a blocking CI gate, not an optional/manual checklist item

---

# 7. Success Criteria

1. Under sustained concurrent load across multiple tenants, zero cross-tenant row leakage is observed in automated testing — including via the specific connection-pool-reuse path this ADR closes.
2. A KEK rotation can be performed with zero downtime and zero forced mass re-encryption event.
3. A self-hosted customer with `DEPLOYMENT_LICENSING_MODE=air_gapped` can run the platform indefinitely with zero outbound network access, verified in a test environment with egress fully blocked.
4. Compromise of any single DEK is contained to exactly one credential record, not the full dedicated-tenant credential store.

---

# Document Status

**Document:** NES-113 — Security & Isolation Hardening Standard
**Version:** 1.0.0
**Status:** Draft — Pending Review
**Owner:** Chief Solution Architect / Security Lead
**Next Review:** Prior to Phase 1 implementation kickoff
**Next Document:** NES-114 — API Gateway Standards
