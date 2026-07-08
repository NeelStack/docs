# NES-120 — Phase 0 Verification Report

This report summarizes the verification of RLS policies, tenant context propagation, role-based auth, and field encryption in the **DhruvaOS / NeelStack EduOS** backend codebase.

---

## 1. Row-Level Security (RLS) Verification Table

| Module | Target Table | RLS Enabled? | FORCE Enabled? | Policy Exists? | Connects as Owner? | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **student** | `student` | Yes | Yes | Yes (`tenant_isolation`) | No (`app_runtime`) | `VERIFIED-SAFE` |
| **attendance** | `attendance` | Yes | Yes | Yes (`tenant_isolation`) | No (`app_runtime`) | `VERIFIED-SAFE` |
| **accounts** | `account_transaction` | Yes | Yes | Yes (`tenant_isolation`) | No (`app_runtime`) | `VERIFIED-SAFE` |
| **library** | `book` | Yes | Yes | Yes (`tenant_isolation`) | No (`app_runtime`) | `VERIFIED-SAFE` |
| **hr** | `staff` | Yes | Yes | Yes (`tenant_isolation`) | No (`app_runtime`) | `VERIFIED-SAFE` |
| **payroll** | `salary_scale` | Yes | Yes | Yes (`tenant_isolation`) | No (`app_runtime`) | `VERIFIED-SAFE` |

---

## 2. Findings & Identified Gaps

### 🔍 Finding 1: RLS Enforcement on Core Tables (`VERIFIED-SAFE`)
*   **Verification**: Migration [0005_module_and_rls_policies.py](file:///d:/poc/neelstack-foundation/services/core/alembic/versions/0005_module_and_rls_policies.py) executes `ENABLE ROW LEVEL SECURITY` and `FORCE ROW LEVEL SECURITY` across all 16 tenant tables.
*   **Policy**: The policy `tenant_isolation` filters on:
    `USING (school_id = current_setting('app.current_tenant_id', true)::integer)`
*   **Safety**: Verified that the server boots with `verify_database_non_owner_role()` asserting that the connection role (`app_runtime`) is not the database table owner, which prevents superuser bypass.

### ⚠️ Finding 2: Tenant Context Propagation Gap (`VERIFIED-GAP`)
*   **Gap Description**: For HTTP requests, [db.py](file:///d:/poc/neelstack-foundation/services/core/src/app/platform/database/db.py#L79-84) properly initiates an explicit transaction and executes `SET LOCAL app.current_tenant_id = :tid`. However, for background tasks running inside the Lifespan scheduler (e.g., [scheduler.py](file:///d:/poc/neelstack-foundation/services/core/src/app/core/scheduler.py#L146-160)'s `perform_notification_cleanup` which attempts to clean announcements):
    1.  The scheduler queries directly via `AsyncSessionLocal()` without setting `app.current_tenant_id`.
    2.  Because the app connects as the non-owner role (`app_runtime`), the RLS policy intercepts the statement.
    3.  Because `app.current_tenant_id` is unset (evaluates to `NULL`), the purge query attempts `DELETE WHERE school_id = NULL::integer`, causing **zero rows to be purged** for any active tenants.
*   **Action Required**: The background task runner must either set the tenant ID context before executing or run utilizing a superuser/owner database connection bypass (e.g. bypassing RLS) to clean up records institution-wide.

### 🔍 Finding 3: Auth & Permission Enforcement (`VERIFIED-SAFE`)
*   **Verification**: Routers use standard Keycloak OIDC authentication via `verify_keycloak_jwt` and role-based checkers like `Depends(RoleChecker(allowed_roles=["admin"]))`. The `401` and `403` HTTP exceptions are correctly thrown by the security layer.

### ⚠️ Finding 4: Single-Key Static Encryption (`VERIFIED-GAP`)
*   **Gap Description**: Data encryption in `student.py` uses [EncryptedString](file:///d:/poc/neelstack-foundation/services/core/src/app/platform/database/encryption.py) powered by `cryptography.fernet.Fernet` using `settings.FIELD_ENCRYPTION_KEY`. 
    1.  The key is static and lacks dynamic key rotation.
    2.  Bypassing or corrupting this single key would render all student Adhar and parent email data unreadable.
*   **Action Required**: Future enhancement must support multi-versioned keys or KMS integration.

---

## 3. Reviewer Sign-off & Gated Transition Status

*   **Gate Status**: **GATED**
*   **Reason**: The tenant context propagation gap in [scheduler.py](file:///d:/poc/neelstack-foundation/services/core/src/app/core/scheduler.py) will cause database leaks or failures in cleanups. 
*   **Resolution Status**: We are requesting approval to defer the RLS context propagation fix for background tasks and the encryption key rotation feature, so we can proceed with Phase 1 backend OpenAPI documentation decorators for verified features.
