# ADR-012 — Database Security and RLS Hardening

## Context
NeelStack EduOS relies on PostgreSQL Row-Level Security (RLS) to enforce data boundaries between tenants in shared database deployments. Under load-balancing and database connection pooling (e.g. pgBouncer or connection pools), session states can leak if connections are reused without clearing session variables (e.g., `app.current_tenant_id`).

Additionally:
- High-value credentials (like dedicated database URLs) are encrypted via a single master AES key, creating a single point of failure.
- The `document_vectors` pgvector table does not have active RLS policies in place, leaving vector search queries dependent purely on application-level filters.
- We lack automated verification pipelines in CI to validate that data boundaries are strictly enforced.

## Decision
We will execute a systematic hardening of database access, encryption, and testing interfaces.

### 1. Connection Pool Scoping & Transaction Boundary Fixes
- Every database transaction setting session parameters (e.g., `SET LOCAL app.current_tenant_id`) must wrap its SQL inside an explicit transaction block (`BEGIN ... COMMIT/ROLLBACK`). Using `SET LOCAL` ensures Postgres automatically discards the setting once the transaction exits, preventing leak risks on connection reuse.
- All shared tables will be configured with `ALTER TABLE x FORCE ROW LEVEL SECURITY;`. This ensures that even the table owner (if not a superuser) is bound by the policy checks.
- The core API will connect to PostgreSQL using a dedicated non-owner role initialized with `NOBYPASSRLS`. Superusers or tables owners bypass RLS by default; using a limited role guarantees RLS applies under all execution conditions.

### 2. pgvector Vector Store Isolation
- Create an RLS policy on the `document_vectors` table using `school_id` as the tenant partition key:
  ```sql
  ALTER TABLE document_vectors ENABLE ROW LEVEL SECURITY;
  ALTER TABLE document_vectors FORCE ROW LEVEL SECURITY;
  
  CREATE POLICY tenant_vector_isolation ON document_vectors
  USING (school_id = current_setting('app.current_tenant_id', true)::integer);
  ```
- Application-level filters are retained, but the database now acts as the primary boundary.

### 3. Envelope Encryption via Key Management Service (KMS)
- Replace single-key Fernet encryption for `dedicated_db_url` and high-value credentials with envelope encryption.
- A Master Key (stored in AWS KMS, GCP KMS, or HashiCorp Vault) encrypts unique, per-tenant Data Encryption Keys (DEKs). The database stores the ciphertext of the credentials alongside the encrypted DEK.
- De-serialization decrypts the DEK via KMS first, and then decodes the payload locally in-memory, allowing secure key rotation.

### 4. Cross-Tenant Isolation Test Suite & CI release Gate
- Build an automated regression test suite executing queries attempting to fetch records from Tenant A using a session configured for Tenant B.
- Any test returning > 0 records fails the build.
- Integrate the isolation tests in GitHub Actions as a mandatory blocker gate for release deployments.

## Consequences
- **Positive**: Strict data separation guarantees at the database level, preventing session leaks.
- **Positive**: High security posture for client database passwords.
- **Positive**: Automated validation prevents regressions in policy definitions.
- **Negative**: KMS integration introduces minor external latency during credentials load. Mitigated by decrypting credentials once at session setup and caching securely in-memory.
