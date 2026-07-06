---
document_id: NES-P-107
title: Security Architecture
version: 1.0.0
status: Approved
owner: Platform Security Team
---

# NES-P-107 — Security Architecture

> **"DhruvaOS enforces multi-tenant security at every layer: unified OIDC authorization, dynamic schema-level database isolation, and structured audit logs."**

---

# 1. Purpose

This document outlines the **security guidelines, cryptographic practices, authorization systems, and data isolation strategies** that secure DhruvaOS workloads. It details the integrations between Zitadel (OIDC/SSO), tenant database schemes, and our auditing registries.

---

# 2. Layered Security Model

Our platform maintains isolation across five primary security planes:

```text
  User Request
       │
       ▼
  [Edge Layer]      SSL Termination & Rate Limiting via Traefik
       │
       ▼
 [Identity Layer]   Zitadel OIDC JWT validation & Role decryption
       │
       ▼
  [Kernel Layer]    Tenant Middleware binds ContextVar schema identifiers
       │
       ▼
  [Storage Layer]   PostgreSQL connection pool maps to target tenant schema
       │
       ▼
  [Auditing logs]   AuditSDK pushes system mutation logs directly to Loki
```

---

# 3. Authentication & Authorization (Zitadel integration)

## 3.1 Bearer Token Introspection
All API routes are protected by JSON Web Token (JWT) verification:
- Signature checks compile certificates from the OIDC Key Web Keyset (`jwks_uri`) endpoint.
- Signing keys are cached locally using `PyJWKClient` to prevent round-trip overhead.

## 3.2 Role-Based Access Control (RBAC)
User permissions are mapped from token resource claims:
- The system extracts roles from Zitadel project claims (format: `urn:zitadel:iam:org:project:role:*`).
- Routes are protected by FastAPI dependencies verifying required permissions (e.g., `attendance.edit`).

---

# 4. Multi-Tenant Database Isolation

DhruvaOS prevents data leaks by applying dynamic Postgres schema routing:

1. **Routing Metadata**: When a request starts, the kernel middleware extracts the `x-tenant-domain` or OIDC tenant claim.
2. **Schema Separation**: The connection pool executes `SET search_path TO tenant_<tenant_slug>` to bind the session.
3. **No Cross-Talk**: All SQL queries execute under the isolated schema namespace. It is physically impossible to fetch rows from other tenant tables.

---

# 5. Auditing Standards

Every database transaction that modifies tables (INSERT, UPDATE, DELETE) must write an audit record via `PlatformSDK.audit.log_action()`:

- **Audit Properties**: User ID, timestamp, HTTP request ID, action identifier, before-and-after values.
- **Audit Storage**: Logs are dispatched to standard out, captured by Loki, and archived in read-only MinIO bucket directories.
- **Access Rule**: Audit logs are immutable. They cannot be modified by application code or tenant admins.
