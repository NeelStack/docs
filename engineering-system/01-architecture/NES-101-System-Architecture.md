---
document_id: NES-101
title: System Architecture
subtitle: Enterprise Reference Architecture for the NeelStack Ecosystem
version: 2.0.0
status: Approved
classification: Internal
owner: Chief Solution Architect
review_cycle: Every 6 Months
document_type: Architecture Standard
parent_document: NES-100 Architecture Principles
next_document: NES-102 Monorepo Architecture
---

# NES-101 — System Architecture

This document presents the authoritative, finalized system architecture and technology stack of **DhruvaOS (NeelStack)**, an AI-Native Education Operating System (EdOS) Platform.

---

## 1. System Vision & Topology

```text
                            ┌─────────────────────────┐
                            │   Next.js Web Console   │
                            │  / Vite Mobile Client   │
                            └────────────┬────────────┘
                                         │
                                         ▼
                            ┌─────────────────────────┐
                            │     Traefik Ingress     │
                            └────────────┬────────────┘
                                         │
                                         ▼
                            ┌─────────────────────────┐
                            │   Core API / Gateway    │
                            └────────────┬────────────┘
                                         │
                                         ▼
                   ======================================
                          DHRUVAOS PLATFORM KERNEL
                       (Context & Middleware Routing)
                   ======================================
                                         │
         ┌───────────────────────────────┼───────────────────────────────┐
         ▼                               ▼                               ▼
┌──────────────────┐            ┌──────────────────┐            ┌──────────────────┐
│  Plugin Loader   │            │   Platform SDK   │            │   AI Registry    │
│(Manifest Engine) │            │ (15 Namespaces)  │            │(10 Tier Platform)│
└────────┬─────────┘            └────────┬─────────┘            └────────┬─────────┘
         │                               │                               │
         ▼                               ▼                               ▼
┌──────────────────┐            ┌──────────────────┐            ┌──────────────────┐
│  Domain Plugins  │            │   Service Bus    │            │    AI Agents     │
│(Attendance, etc.)│            │(NATS + JetStream)│            │(Dynamic memory)  │
└──────────────────┘            └──────────────────┘            └──────────────────┘
```

---

## 2. Platform Core Infrastructure Stack

| Layer | Component | Chosen Technology | Role in Architecture |
| :--- | :--- | :--- | :--- |
| **Monorepo** | Monorepo Tooling | Turbo | Fast incremental builds and execution caching. |
| **Ingress** | Ingress Gateway / Reverse Proxy | Traefik | Edge SSL termination, path routing, and rate-limiting. |
| **SSO / IAM** | Identity Provider | Zitadel (OIDC / OAuth 2) | Multi-tenant user federation, JWT signing keys, project roles. |
| **Database** | Database Engine | PostgreSQL (pgvector) | Relational student database + Vector embeddings storage. |
| **Cache & Jobs** | Cache / Queue | Redis + Arq | High-speed key-value cache and background worker queue. |
| **Event Bus** | Messaging System | NATS + JetStream | High-throughput async message pipeline with persistence. |
| **Object Store**| Storage Service | MinIO / S3 | Clustered binary artifact and document store. |
| **Observability**| Telemetry / Audit | Loki + Prometheus + Grafana | Structured logs collector, p-percentiles metrics, dashboards. |
| **Automations** | Visual Workflows | n8n | Flow orchestration for school administrative triggers. |

---

## 3. Platform Kernel & Context Routing

The **Platform Kernel** manages the dynamic request isolation boundary:
1. **Tenant Context**: Maps incoming request subdomains or claims to target isolated tenant schemas (e.g. `SET search_path TO tenant_[slug]`).
2. **Context Manager**: Thread-safe `TenantContext` using Python's native `ContextVar` to secure transactions across concurrent asynchronous tasks.
3. **Middleware**: Fast-path HTTP middleware enforcing schema mapping, auth token decryption, and session cleanups to prevent data leaks.

---

## 4. Dynamic Plugin Manifest Spec (`module.yaml`)

Domain microservices function as isolated plugins, self-registering at application boot:
- **Manifest Properties**: Declare route prefixes, permissions, produces/consumes event topics, AI tools, sidebar links, dependencies, feature flags, and kernel compatibility requirements (`requires_sdk`).
- **Plugin Loader**: Performs topological sorts, resolves dependencies, and dynamically mounts FastAPI routing handlers using `importlib` based on the plugin's manifest configuration.

---

## 5. Unified Platform SDK (15 Namespaces)

Domain plugins never import low-level drivers. They interact through the structured `platform` SDK namespace:
- `platform.auth`          → Tenant token authentication
- `platform.events`        → NATS JetStream event publishing
- `platform.storage`       → MinIO / S3 object upload/download
- `platform.audit`         → Structured audit log records
- `platform.notifications` → Push, in-app alerts, SMS, and email
- `platform.search`        → Querying via abstract search providers (Postgres FTS / OpenSearch)
- `platform.ai`            → AI Gateway integration (chat, embed, summarise)
- `platform.cache`         → Redis key caching
- `platform.queue`         → Arq background worker enqueuing
- `platform.config`        → Dynamic tenant feature flags
- `platform.files`         → High-level metadata file records
- `platform.mail`          → Transactional email dispatching
- `platform.sms`           → SMS route gateways
- `platform.payments`      → Stripe & Razorpay order tracking
- `platform.scheduler`     → Cron, scheduled nightlies, and recurring jobs

---

## 6. Multi-Tier AI Registry Framework

The AI Gateway service incorporates a 10-tier dynamic registry, eliminating hardcoded orchestrator dispatches:

1. **Models Registry**: Maps generic models to OpenAI/Gemini providers.
2. **Providers Registry**: Manages provider credentials and failover rules.
3. **Prompts Registry**: Controls version-tracked Jinja system instructions templates.
4. **Knowledge Registry**: Catalogs semantic RAG search sources, indexes, and document chunk configs.
5. **Memory Registry**: Coordinates short-term session and long-term profiles memory pools.
6. **Tools Registry**: Compiles Python function signatures into JSON schemas.
7. **Agents Registry**: Resolves intent triggers (`@AgentRegistry.register_agent`) to agent executors.
8. **Policies Registry**: Enforces daily spending budgets per tenant, agent, and user.
   - *Mechanics*: Tracks cumulative USD expenditures inside Redis strings (`budget:usage:<tenant_id>`). 
   - *Granularity*: Checks policies on every incoming API token validation.
   - *Threshold Actions*:
     - **80% of budget**: Fires a soft-warning webhook event (`budget.warning.v1`) to alert tenant administrators.
     - **100% of budget**: Trigger an immediate hard-cutoff, denying any downstream LLM invocation by returning a `402 Payment Required` exception.
     - *Overage handling*: Unused tokens or queued jobs are immediately denied.
9. **Guardrails Registry**: Filters inputs and outputs for PII or policy violations.
   - *Mechanics*: Performs Named Entity Recognition (NER) utilizing local Microsoft Presidio models paired with deterministic regex rules to identify and mask email addresses, SSNs, phone numbers, and names.
   - *Filtering Action*: Concrete redaction of identified text replacing entities with classification tokens (e.g. `[REDACTED_PHONE]`) prior to external model transit.
   - *Prompt Injection Mitigation*: Rejects queries containing known system override phrases (e.g., "ignore previous instructions") via semantic similarity checks. All tool calls execute inside isolated sandbox runtimes, validating outputs against Pydantic schemas before code processing.
10. **Observability Registry**: Reports inference token counts, latency, and cost telemetry.

---

## 7. Environment Delivery Pipeline

DhruvaOS standardizes a structured delivery pipeline composed of five environments, ensuring seamless migration from local code iteration to global SaaS scale:

```text
  Local ──► Development ──► Testing ──► UAT ──► Production
```

- **Local / Dev**: Lightweight docker compose profiles mapping dependencies locally (0 cost). Uses localhost ports.
- **Testing / UAT / Prod**: Configured using cloud-native orchestration config maps or secure container injection variables. Never uses hardcoded defaults.

*Flexibility: Adding a UAT or staging environment requires zero application changes, driven purely by Pydantic environment configurations.*

---

## 8. Database Strategy & Isolation Triggers

Instead of linking data isolation strictly to the number of tenants, DhruvaOS maps database topologies dynamically based on business triggers and security SLAs:

| Business / Compliance Trigger | Data Isolation Strategy | Expected Infrastructure Topology | Target Uptime | RPO / RTO | p99 Latency |
| --- | --- | --- | :---: | :---: | :---: |
| **Standard SaaS Tiers** | **Schema-per-tenant** | Shared PostgreSQL instance; dynamic `search_path` middleware isolation. | 99.9% | 1 hour / 4 hours | < 200ms |
| **Data Compliance SLAs** | **Database-per-tenant** | Dedicated logical databases on shared or dedicated Postgres clusters. | 99.95% | 15 min / 1 hour | < 150ms |
| **Enterprise SLA & Performance** | **Dedicated Cluster** | Completely isolated compute, memory, and database servers. | 99.99% | 5 min / 15 min | < 100ms |
| **Sovereign Cloud & Residency** | **Regional Deployment** | Region-locked Kubernetes clusters and regional PostgreSQL replicates. | 99.99% | 1 min / 5 min | < 80ms |

---

## 9. Platform & Plugin Versioning Governance

To evolve the core services without causing regression breaks in active domain modules, the system establishes a strict version governance framework:

1. **FastAPI Routes Versioning**: All plugin endpoints must be explicitly versioned in their path prefixes (e.g., `/api/v1/attendance`). Breaking endpoint contract adjustments must bump to `/api/v2/` and keep the v1 router mounted during a deprecation window.
2. **SDK and Kernel Bindings (`requires_sdk`)**: Plugins declare compatibility ranges inside `module.yaml` (e.g. `requires_sdk: ">=1.2.0, <2.0.0"`). If a plugin is loaded on a kernel that falls outside of this compatibility limit, the `PluginLoader` raises a boot exception.
3. **SDK Version Adapters**: If changes are made to the `PlatformSDK` interfaces, the SDK classes must deploy backward-compatibility wrappers/adapters rather than immediate deprecations, allowing legacy plugins to continue operation.

---

## 10. Resilience & Failure Modes

Every core platform infrastructure service is configured with explicit failure tracking metrics, retry limits, and degraded execution states:

### 10.1 Traefik Ingress
- **Failure Mode**: Router crash or ingress connection limits exceeded.
- **Detection Method**: Ingress health check returns HTTP failure code (e.g., `GET /ping` returns non-200), or metrics indicate a spike in raw connection drops.
- **High-Availability (HA) Configuration**:
  - Deploy a minimum of 3 replicas distributed across separate cluster nodes utilizing pod anti-affinity.
  - Enable session affinity utilizing cookie-based routing mechanisms (`sticky: true`).
  - Traefik health check parameters are configurable (see NES-310 §1.1 for current parameters).
- **Degraded-Mode Behavior**: Traffic is rejected at the ingress boundary. Cloudflare edge points return `HTTP 502 Bad Gateway` or `520 Web Server is Down` errors.
- **Recovery Procedure**: Automatic Kubernetes controller restart. Dynamic scaling parameters are managed under infrastructure variables (see NES-310 §1.1 for metrics thresholds).

### 10.2 NATS + JetStream
- **Failure Mode**: Storage volume full, stream corrupt, or consumer lag exceeds thresholds.
- **Detection Method**: Prometheus alert triggers when consumer lag metrics exceed thresholds (see NES-310 §2.1 for current parameters).
- **Lag & Backpressure Handling**: JetStream uses flow control windows. If consumer queue buffers fill, NATS blocks publishers before failing, forcing core gateway services to queue events locally (see NES-310 §2.1 for current buffer and timeout parameters).
- **Retry / Timeout Parameters**: Event publication failures trigger exponential backoff retry cycles (see NES-310 §2.2 for current parameters).
- **Degraded-Mode Behavior**: Decoupled async tasks are delayed, but synchronous API requests complete successfully. Core API spools pending logs to local disk temporarily if in-memory queue overflows.
- **Recovery Procedure**: Cluster auto-resizes volumes; JetStream controllers automatically re-elect partition leaders.

### 10.3 PostgreSQL
- **Failure Mode**: Main instance connection pools exhausted or database host crash.
- **Detection Method**: Connection pool timeouts throw `ConnectionTimeoutError` to gateway services, or Postgres metrics show `active_connections >= max_connections`.
- **Connection Pool Tradeoffs**:
  - *Pool-per-tenant*: Provides isolation, but creates connection socket sprawl on the database, exhausting Postgres process limits.
  - *Shared Pool*: **Selected Strategy**. Uses a central PgBouncer proxy operating in transaction pooling mode. High socket reuse is enforced while middleware executes `SET search_path` dynamically inside transactions.
  - *Noisy-Neighbor Mitigation*: PgBouncer per-tenant pool reservation limits and gateway sliding-window rate limiting policies are enforced (see NES-310 §3.1 for current connection and rate limits).
- **Retry / Timeout Parameters**: PostgreSQL connection failures trigger exponential backoff retry cycles (see NES-310 §3.2 for current parameters).
- **Degraded-Mode Behavior**: Gateway blocks state modifications and returns `HTTP 503 Service Unavailable`. Reads that are cached inside Redis remain active.
- **Recovery Procedure**: Cluster management systems (e.g., Patroni) promote a read-replica to master status within 30 seconds (RTO 30s).

### 10.4 Redis
- **Failure Mode**: Redis engine runs out of memory (OOM) or crashes.
- **Detection Method**: Redis health logs report OOM errors, or response ping times exceed 1000ms.
- **Retry / Timeout Parameters**: Redis lookup failures trigger connection retry cycles (see NES-310 §4.2 for current parameters).
- **Degraded-Mode Behavior**: Session storage lookups fall back directly to primary Postgres tables, increasing DB latency. Temporary telemetry writes fail silently in the background. Eviction is set to `allkeys-lru` to auto-clear old session caches.
- **Recovery Procedure**: Redis Sentinel triggers master replica promotion.

### 10.5 MinIO Object Storage
- **Failure Mode**: Disk arrays fail, causing object access loss.
- **Detection Method**: `GET /minio/health/live` returns HTTP 500 errors.
- **Retry / Timeout Parameters**: MinIO storage access failures trigger exponential backoff retry cycles (see NES-310 §5.1 for current parameters).
- **Degraded-Mode Behavior**: Document uploads fail immediately. Document downloads route temporarily through edge CDN caches or throw retrieval errors.
- **Recovery Procedure**: MinIO Erasure Coding automatically reconstructs data blocks from remaining drives.

---

## 11. Security & Tenant Isolation Assurance

Security boundaries are validated continuously to maintain strict data segregation:

### 11.1 Secrets Management
- All database credentials, OAuth tokens, and model keys are managed inside a clustered **HashiCorp Vault** deployment.
- **Rotation Policies**:
  - Database credentials are automatically rotated every **30 days** via Vault's dynamic secrets engine.
  - JWT asymmetric signing keys are rotated every **90 days**.
  - Third-party model API keys are rotated every **180 days** via automated Vault pipeline schedules.

### 11.2 Encryption
- **Encryption At-Rest**: Sensitive tenant columns (student contact records, grades, billing parameters) are encrypted using AES-256-GCM via pg_crypto utilizing per-tenant database encryption keys (DEKs) master-wrapped by Vault keys.
- **Encryption In-Transit**: Perimeter TLS (v1.3) is terminated at the Traefik ingress gateway. Within the internal Kubernetes cluster, strict **mutual TLS (mTLS)** is enforced across all container sidecars via service mesh proxies.

### 11.3 Tenant-Boundary Verification Testing
- A dedicated isolation test suite runs on every CI/CD pipeline build.
- The test harness spins up two distinct mock database instances (`tenant_a`, `tenant_b`), mocks an active user token under `tenant_a`, and executes SQL injections, header spoofing payloads, and manual search path alteration queries.
- The pipeline asserts that any returned row count from `tenant_b` is exactly `0`, throwing a pipeline build block if any cross-tenant data leakage is observed.

### 11.4 Incident Response SLA & Blast Radius
- **Blast Radius**: Confined strictly to a single schema (Standard SaaS) or single logical database (Compliance Tier).
- **Isolation Breach SLA**: A security incident of tenant breach (SEV-0) triggers immediate lock-down of the compromised schema. Tenant administrators must be notified within **2 hours** of incident detection, with full security patches completed within **4 hours**. The SLA clock is owned by the Security Response Team on-call rotation. Priority alerts are dispatched via PagerDuty priority routing (SEV-0 target notification in under 15 minutes, with escalating supervisor overrides if unacknowledged within 5 minutes).

---

## 12. Tenant Migration & Data Lifecycle

Moving live tenant accounts between isolation tiers must follow a strict operational runbook:

```text
  Schema-per-tenant (SaaS)
            │
            ▼ [Logical Dump & Restore]
  Database-per-tenant (Compliance)
            │
            ▼ [Replica Migration]
  Dedicated Cluster (Enterprise)
            │
            ▼ [Multi-region replication sync]
  Regional Deployment (Sovereign)
```

### 12.1 Migration Process (Schema-per-tenant ──► Database-per-tenant)
Ops-managed logical migration execution procedures are detailed in the playbook (see NES-310 §6.2 for step-by-step commands).

### 12.2 Data Consistency Verification
Before traffic cut-over is completed, operations must verify transactional consistency and hash states between source and target database instances (see NES-310 §6.2 for check scripts).

### 12.3 Rollback Plan
Migration recovery rollback commands are detailed in the operational playbook (see NES-310 §6.3 for rollback CLI scripts).

### 12.4 Migration Ownership
Migrations are ops-initiated, triggered manually by administrators following resource utilization warnings (e.g. tenant activity triggers persistent CPU load alerts exceeding 80% capacity on the shared host).
- *Automated Recommendation Engine*: To optimize performance management, an automated evaluation system monitors cost, request volume, and token metrics from the Observability Registry. If a tenant consistently breaches the resource utilization baseline metrics, the platform automatically flags them as a migration candidate (see NES-310 §6.1 for current thresholds).

---

## 13. Governance of Automated Workflows (n8n)

Integrating visual automations must not bypass platform auditing, database isolation, or security controls:

1. **Workflow Authoring**: Creating and publishing n8n automations is restricted to system administrators with Multi-Factor Authentication (MFA) enabled.
2. **Version Control Integration**: n8n workflows must be exported to JSON files and committed to the monorepo under `/infrastructure/workflows/`. They are subject to peer code review (PR approvals) before deployment.
3. **Database Access Restriction**: Workflows are blocked from directly querying database instances (direct TCP SQL node configurations are disabled). All data mutations and lookups must execute via authenticated platform HTTP API endpoints.
4. **Audit Logging**: Every workflow invocation must transmit the tenant context and the administrator's security token. Execution audit logs are pushed directly to `platform.audit` by the API gateway.
