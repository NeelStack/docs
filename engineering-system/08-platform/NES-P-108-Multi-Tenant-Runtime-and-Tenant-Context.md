---
document_id: NES-P-108
title: Multi-Tenant Runtime & Tenant Context
version: 1.0.0
status: Approved
owner: Platform Kernel Team
---

# NES-P-108 — Multi-Tenant Runtime & Tenant Context

> **"Data isolation is thread-safe and async-safe. Every request runs inside a bounded ContextVar container."**

---

# 1. Purpose

This document describes the **runtime context isolation, schema resolving middleware, and dynamic connection pools** that manage multi-tenancy inside the DhruvaOS core engine. It outlines the specific class interfaces and middleware pipelines used to separate tenant scopes.

---

# 2. Context Isolation Architecture

DhruvaOS manages tenant context using Python's native `ContextVar` libraries:

```text
Incoming HTTP Request
       │
       ▼
TenantContextMiddleware
  1. Extract tenant domain header ('x-tenant-domain')
  2. Query cache for tenant config (database schema, flags)
  3. Initialize TenantContext object
  4. Bind to ContextVar: `_tenant_context.set(tenant_context)`
       │
       ▼
FastAPI Router / Business Logic
  - Domain code accesses context via `PlatformKernel.get_tenant_context()`
  - Safe across concurrency loops and async/thread executions
       │
       ▼
Request Clean Up
  - Middleware clears ContextVar token
  - Prevents memory leaks and cross-request contamination
```

---

# 3. Code Specifications

The runtime context is managed by two core modules:

- **[context.py](file:///d:/poc/neelstack-foundation/services/core/src/app/kernel/context.py)**: Defines the `TenantContext` model and `PlatformKernel` context wrapper.
- **[middleware.py](file:///d:/poc/neelstack-foundation/services/core/src/app/kernel/middleware.py)**: The FastAPI middleware that intercepts requests.

---

# 4. Database Connection Routing & Pool Strategy

When SQL database commands execute, the database pool dynamically routes traffic based on the active `TenantContext` to guarantee physical or logical isolation:

### 4.1 Connection Pool Tradeoffs
- **Pool-per-Tenant**: Leads to connection socket exhaustion on PostgreSQL, as Postgres creates a process for every active socket.
- **Shared Pool (Selected)**: Enforces high connection recycling efficiency utilizing a centralized **PgBouncer** proxy in transaction pooling mode. The transaction manager executes search path overrides dynamically within transactions.

### 4.2 Routing Mechanics
1. The repository wrapper requests a connection socket from the shared pool.
2. It retrieves the active context from `PlatformKernel.get_tenant()` (which resolves to `TenantContext` bound to the async execution worker via the ContextVar middleware).
3. The database wrapper executes the prefix override command inside the explicit transaction block:
   ```sql
   SET LOCAL search_path = :schema, public;
   ```
4. On transaction commit or rollback, Postgres discards the local search path parameters automatically, ensuring that when the connection returns to the shared pool, there is **zero leakage** of parameters to subsequent requests.
5. In background asynchronous processes (e.g. Arq jobs), the database generator `get_db` automatically falls back to checking the active `ContextVar` inside the worker thread to map the schema isolation path.

### 4.3 High-Availability (HA) & Replication
- Postgres HA is orchestrated using Patroni cluster managers across 3-node HA topologies.
- Read requests are distributed to replica endpoints when the tenant context triggers analytics workloads.
- Active master failure triggers automated promotion of the healthiest read-replica within 30 seconds (RTO 30s).

---

# 5. Core Development Rules

1. **Never Cache Context Objects Globally**: Do not bind `TenantContext` to global variables, module levels, or static class parameters. Always resolve dynamically via `PlatformKernel.get_tenant_context()`.
2. **Handle Context Absences**: Code that runs in offline tasks (e.g., system crons, migration scripts) must explicitly instantiate a dummy context frame using:
   ```python
   with PlatformKernel.tenant_scope(system_tenant_id):
       # execute logic
   ```
3. **Audit Context Failures**: Any request that fails to resolve a valid tenant schema must immediately return a `400 Bad Request (Missing Tenant Context)` header, logging the exception to Loki telemetry.
