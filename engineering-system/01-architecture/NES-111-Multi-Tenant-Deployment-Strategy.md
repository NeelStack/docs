---
document_id: NES-111
title: Multi-Tenant Deployment Strategy
subtitle: Single Codebase — Four Deployment Models (SaaS, White Label, Dedicated Cloud, Self-Hosted)
version: 1.0.0
status: Approved
classification: Internal
owner: Chief Solution Architect
review_cycle: Every 6 Months
document_type: Architecture Standard
parent_document: NES-110 Architecture Governance
next_document: NES-112 API Gateway Standards
---

# NES-111 — Multi-Tenant Deployment Strategy

> **"One codebase. Four deployment models. Zero if-else spaghetti."**

---

# Executive Summary

NeelStack EduOS must serve four radically different customer segments — from a small 200-student school sharing cloud infrastructure with thousands of others, to a government education authority running everything inside their own data centre.

This document answers the critical question:

**Can a single codebase realistically support SaaS, White Label, Dedicated Cloud, and Self-Hosted deployments?**

**Answer: Yes. But only if you build it correctly from day one.**

This standard defines the exact architecture, patterns, and code contracts that make this possible. Every team member must understand and follow these rules.

---

# The Four Deployment Models

```text
┌─────────────────────────────────────────────────────────────────┐
│              NeelStack EduOS — Single Application Codebase      │
└────────────────────────────┬────────────────────────────────────┘
                             │ Same code. Different configuration.
       ┌─────────────────────┼──────────────────────────────┐
       ▼                     ▼                  ▼            ▼
  ┌──────────┐       ┌─────────────┐   ┌──────────────┐  ┌──────────────┐
  │   SaaS   │       │ White Label │   │  Dedicated   │  │ Self-Hosted  │
  │          │       │    SaaS     │   │    Cloud     │  │ On-Premise   │
  │Shared    │       │Custom domain│   │  Dedicated   │  │Customer owns │
  │infra     │       │Cust branding│   │  infra       │  │everything    │
  │Shared DB │       │Still hosted │   │  Managed by  │  │Docker/K8s    │
  │(RLS)     │       │by NeelStack │   │  NeelStack   │  │Deployment    │
  └──────────┘       └─────────────┘   └──────────────┘  └──────────────┘
```

---

# Core Principle: Configuration Over Code Branching

> [!IMPORTANT]
> **The Golden Rule:** Business logic MUST NEVER check the deployment model directly.
>
> ❌ **WRONG:** `if deployment_model == "saas": do_x() elif deployment_model == "self_hosted": do_y()`
>
> ✅ **CORRECT:** `if feature_flags.ai_assistant_enabled: do_x()`

The deployment model determines which feature flags are enabled. Feature flags determine behavior. Business logic never knows "where" it is running.

---

# Layer 1: Tenant Resolution — How the System Knows Who Is Asking

Every HTTP request enters the system through a **Tenant Resolution Middleware** before any business logic runs.

## How Tenant Resolution Works

```text
Incoming Request: POST https://stmarys.neelstack.com/api/v1/students
                                    │
                                    ▼
              ┌─────────────────────────────────────────┐
              │         Tenant Resolution Middleware     │
              │                                         │
              │  1. Extract host header:                │
              │     host = "stmarys.neelstack.com"      │
              │                                         │
              │  2. Look up tenant in Redis cache:       │
              │     tenant = redis.get("tenant:stmarys.neelstack.com")
              │                                         │
              │  3. Cache miss? Query PostgreSQL:        │
              │     SELECT * FROM tenants WHERE domain = 'stmarys.neelstack.com'
              │                                         │
              │  4. Build TenantContext:                 │
              │     {                                    │
              │       id: "tenant_abc123",               │
              │       name: "St. Mary's School",         │
              │       deployment_model: "saas_shared",   │
              │       db_schema: "tenant_abc123",        │
              │       features: { ai: true, wl: false }, │
              │       branding: { color: "#1E40AF", ... }│
              │     }                                    │
              │                                         │
              │  5. Attach to request.state.tenant       │
              └─────────────────────────────────────────┘
                                    │
                                    ▼
              ┌─────────────────────────────────────────┐
              │            Business Logic               │
              │   Reads from request.state.tenant       │
              │   Has ZERO knowledge of deployment type  │
              └─────────────────────────────────────────┘
```

## Python Implementation

```python
# services/core/src/app/shared/middleware/tenant.py

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.shared.tenant_registry import TenantRegistry

class TenantResolutionMiddleware(BaseHTTPMiddleware):
    """
    Resolves tenant context from the incoming request host header.
    Attaches TenantContext to request.state.tenant for all downstream handlers.
    
    This middleware runs FIRST before any route handlers.
    """

    async def dispatch(self, request: Request, call_next):
        host = request.headers.get("host", "").split(":")[0]  # Strip port

        tenant = await TenantRegistry.resolve_by_domain(host)

        if tenant is None:
            return JSONResponse(
                status_code=404,
                content={"error": "Tenant not found for domain"},
            )

        request.state.tenant = tenant
        response = await call_next(request)
        return response
```

```python
# services/core/src/app/shared/tenant_registry.py

import json
from app.shared.cache import redis_client
from app.shared.database import get_admin_db
from app.shared.models import TenantContext, FeatureFlags, BrandConfig

class TenantRegistry:
    CACHE_TTL = 300  # 5 minutes

    @classmethod
    async def resolve_by_domain(cls, domain: str) -> TenantContext | None:
        cache_key = f"tenant:domain:{domain}"

        # 1. Try Redis cache first
        cached = await redis_client.get(cache_key)
        if cached:
            return TenantContext.model_validate_json(cached)

        # 2. Query database
        async with get_admin_db() as db:
            row = await db.execute(
                "SELECT * FROM tenants WHERE custom_domain = $1 OR subdomain = $1",
                domain
            )
            tenant_row = row.fetchone()

        if not tenant_row:
            return None

        # 3. Build context
        tenant = TenantContext(
            id=tenant_row.id,
            name=tenant_row.name,
            deployment_model=tenant_row.deployment_model,
            db_schema=tenant_row.db_schema,
            db_url=tenant_row.dedicated_db_url,   # None for shared DB tenants
            features=FeatureFlags(**tenant_row.features),
            branding=BrandConfig(**tenant_row.branding),
        )

        # 4. Cache result
        await redis_client.setex(cache_key, cls.CACHE_TTL, tenant.model_dump_json())
        return tenant
```

---

# Layer 2: Database Isolation Strategy

Different deployment models require different levels of data isolation.

## Isolation Modes

| Deployment Model | DB Strategy | Isolation Level | Notes |
| :--- | :--- | :--- | :--- |
| SaaS Free / Standard | Shared DB + Row-Level Security (RLS) | Logical | All tenants in shared tables. RLS prevents cross-tenant reads. |
| White Label SaaS | Shared DB + Schema Isolation | Logical+ | Each tenant has own PostgreSQL schema (`SET search_path`) |
| Dedicated Cloud | Dedicated RDS Instance | Physical | Separate DB. NeelStack manages infra. |
| Self-Hosted | Customer-managed DB | Physical | Customer provides DB URL. No NeelStack infra. |

## Connection Factory — One Pattern for All Modes

```python
# services/core/src/app/shared/database.py

from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from app.shared.models import TenantContext

# Shared connection pool (used for SaaS and White Label tenants)
_shared_engine = create_async_engine(settings.SHARED_DATABASE_URL, pool_size=20)

# Dedicated engine cache (used for Dedicated Cloud / Self-Hosted tenants)
_dedicated_engines: dict[str, AsyncEngine] = {}

@asynccontextmanager
async def get_tenant_db(tenant: TenantContext) -> AsyncSession:
    """
    Returns an async database session correctly configured for the tenant's
    deployment model. Business logic does not need to know which mode is active.
    """
    if tenant.deployment_model == "saas_rls":
        # Mode 1: Shared DB with Row-Level Security
        async with AsyncSession(_shared_engine) as session:
            # Set tenant context for RLS policies
            await session.execute(
                text("SET LOCAL app.current_tenant_id = :tid"),
                {"tid": tenant.id}
            )
            yield session

    elif tenant.deployment_model == "schema_isolated":
        # Mode 2: Schema-per-Tenant (White Label / Premium SaaS)
        async with AsyncSession(_shared_engine) as session:
            await session.execute(
                text("SET LOCAL search_path = :schema, public"),
                {"schema": tenant.db_schema}
            )
            yield session

    else:
        # Mode 3: Dedicated database (Dedicated Cloud or Self-Hosted)
        if tenant.id not in _dedicated_engines:
            _dedicated_engines[tenant.id] = create_async_engine(
                tenant.db_url, pool_size=5
            )
        async with AsyncSession(_dedicated_engines[tenant.id]) as session:
            yield session
```

## Row-Level Security (RLS) PostgreSQL Setup

For SaaS tenants sharing a database, PostgreSQL RLS ensures one tenant can never read another's data even if a developer forgets the WHERE clause.

```sql
-- Run once during database setup
-- Enable RLS on all shared tenant tables

ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE enrollments ENABLE ROW LEVEL SECURITY;
ALTER TABLE grades ENABLE ROW LEVEL SECURITY;

-- Create RLS policy: tenants can only see their own rows
CREATE POLICY tenant_isolation ON students
    USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

CREATE POLICY tenant_isolation ON enrollments
    USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

CREATE POLICY tenant_isolation ON grades
    USING (tenant_id = current_setting('app.current_tenant_id')::uuid);
```

---

# Layer 3: Feature Flags — Behavior by Plan, Not by Deployment Model

Feature flags decouple business behavior from the deployment model. This is the mechanism that allows one codebase to serve all four deployment models without if-deployment-model branching.

## Feature Flag Model

```python
# services/core/src/app/shared/models.py

from pydantic import BaseModel

class FeatureFlags(BaseModel):
    # AI Features
    ai_academic_assistant: bool = False
    ai_grade_prediction: bool = False
    ai_plagiarism_detection: bool = False

    # Search
    opensearch_enabled: bool = False   # SaaS Enterprise only
    # Default search: PostgreSQL full-text search (always on)

    # Branding
    white_label_enabled: bool = False  # White Label plan only
    custom_domain_enabled: bool = False

    # Data & Compliance
    advanced_analytics: bool = False
    audit_log_enabled: bool = True     # Always on
    gdpr_tools_enabled: bool = False

    # Integrations
    saml_sso_enabled: bool = False     # Enterprise plans
    public_api_access: bool = False

    # Mobile
    offline_sync_enabled: bool = False # Self-hosted schools with bad connectivity

    class Config:
        frozen = True  # Feature flags are immutable per request
```

## Plan-to-Feature-Flag Mapping

```python
# services/core/src/app/shared/plan_features.py

PLAN_FEATURE_MAP = {
    "saas_free": FeatureFlags(
        ai_academic_assistant=False,
        advanced_analytics=False,
        audit_log_enabled=True,
    ),
    "saas_standard": FeatureFlags(
        ai_academic_assistant=True,
        advanced_analytics=False,
        audit_log_enabled=True,
    ),
    "saas_enterprise": FeatureFlags(
        ai_academic_assistant=True,
        ai_grade_prediction=True,
        opensearch_enabled=True,
        advanced_analytics=True,
        saml_sso_enabled=True,
        public_api_access=True,
        audit_log_enabled=True,
    ),
    "white_label": FeatureFlags(
        ai_academic_assistant=True,
        white_label_enabled=True,
        custom_domain_enabled=True,
        advanced_analytics=True,
        audit_log_enabled=True,
    ),
    "dedicated_cloud": FeatureFlags(
        ai_academic_assistant=True,
        ai_grade_prediction=True,
        advanced_analytics=True,
        saml_sso_enabled=True,
        public_api_access=True,
        audit_log_enabled=True,
        gdpr_tools_enabled=True,
    ),
    "self_hosted": FeatureFlags(
        ai_academic_assistant=True,    # Runs locally, customer's API keys
        advanced_analytics=True,
        saml_sso_enabled=True,
        offline_sync_enabled=True,     # Critical for low-connectivity schools
        audit_log_enabled=True,
        gdpr_tools_enabled=True,
    ),
}
```

---

# Layer 4: White-Label Branding Engine

White Label tenants get a fully branded experience — custom colors, logo, app name, email templates, and mobile branding — without any code changes.

## How It Works

```text
Browser Request to erp.customerdomain.com
                    │
                    ▼
         Next.js Page Server-Side Render
                    │
                    ▼
    GET /api/v1/public/brand?domain=erp.customerdomain.com
                    │
                    ▼
         Returns BrandConfig JSON:
         {
           primary_color: "#0052CC",
           secondary_color: "#172B4D",
           logo_url: "https://cdn.neelstack.com/tenants/t_xyz/logo.png",
           app_name: "AtlasEdu School Portal",
           favicon_url: "...",
           font_family: "Inter",
         }
                    │
                    ▼
    Next.js injects into <html>:
    <style>
      :root {
        --color-primary: #0052CC;
        --color-secondary: #172B4D;
        --font-family: 'Inter', sans-serif;
      }
    </style>
```

## Brand Config Data Model

```python
# services/core/src/app/shared/models.py

class BrandConfig(BaseModel):
    primary_color: str = "#6366F1"         # Default NeelStack purple
    secondary_color: str = "#4F46E5"
    accent_color: str = "#0EA5E9"
    logo_url: str | None = None            # None = use NeelStack logo
    favicon_url: str | None = None
    app_name: str = "NeelStack EduOS"
    font_family: str = "Inter"
    custom_css_url: str | None = None      # Advanced: custom CSS injection
    email_from_name: str = "NeelStack EduOS"
    email_logo_url: str | None = None
    mobile_splash_color: str = "#6366F1"   # For Capacitor splash screen
    mobile_app_name: str = "EduOS"
```

## Public Brand API Endpoint

```python
# services/core/src/app/domains/tenant/router.py

@router.get("/public/brand", response_model=BrandConfig)
async def get_brand_config(request: Request):
    """
    Public endpoint — no auth required.
    Returns branding configuration for the current tenant domain.
    Used by Next.js to inject CSS variables at page load.
    """
    tenant = request.state.tenant
    if not tenant.features.white_label_enabled:
        # Return default NeelStack branding for non-white-label tenants
        return BrandConfig()
    return tenant.branding
```

## Next.js Integration

```typescript
// apps/web/lib/branding.ts

export interface BrandConfig {
  primaryColor: string;
  secondaryColor: string;
  logoUrl: string | null;
  appName: string;
  fontFamily: string;
}

export async function fetchBrandConfig(domain: string): Promise<BrandConfig> {
  const res = await fetch(`/api/v1/public/brand?domain=${domain}`, {
    next: { revalidate: 300 }, // Cache for 5 minutes (Next.js ISR)
  });
  return res.json();
}
```

```typescript
// apps/web/app/layout.tsx

import { fetchBrandConfig } from "@/lib/branding";
import { headers } from "next/headers";

export default async function RootLayout({ children }) {
  const headerList = headers();
  const domain = headerList.get("host") ?? "";
  const brand = await fetchBrandConfig(domain);

  return (
    <html lang="en">
      <head>
        {/* Inject CSS variables for white-label branding */}
        <style>{`
          :root {
            --color-primary: ${brand.primaryColor};
            --color-secondary: ${brand.secondaryColor};
            --font-family: ${brand.fontFamily}, sans-serif;
          }
        `}</style>
        <title>{brand.appName}</title>
      </head>
      <body>{children}</body>
    </html>
  );
}
```

---

# Layer 5: Infrastructure Profiles — Docker Compose Configuration

One codebase requires different infrastructure profiles for different deployment models. We use **Docker Compose profiles** to manage this.

## Compose Profile Strategy

```yaml
# infrastructure/docker/docker-compose.base.yml
# Core services — always required, all deployment models

services:
  # Always On
  postgres:
    image: pgvector/pgvector:pg16
    restart: unless-stopped
    # ... config

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    # ... config

  core-api:
    build: ../../services/core
    restart: unless-stopped
    # ... config

  ai-api:
    build: ../../services/ai
    restart: unless-stopped
    # ... config

  sockets:
    build: ../../services/sockets
    restart: unless-stopped
    # ... config

  web:
    build: ../../apps/web
    restart: unless-stopped
    # ... config
```

```yaml
# infrastructure/docker/docker-compose.saas.yml
# SaaS Cloud — additional services for hosted deployment

services:
  opensearch:
    image: opensearchproject/opensearch:2.11.0
    profiles: ["saas"]
    # Only starts when running: docker compose --profile saas up

  auth:
    image: ghcr.io/zitadel/zitadel:latest
    profiles: ["saas"]
    # Auth server — managed by NeelStack in cloud
```

```yaml
# infrastructure/docker/docker-compose.selfhosted.yml
# Self-Hosted / On-Premise — minimal footprint, no heavy Java services

services:
  auth:
    image: ghcr.io/zitadel/zitadel:latest
    # Zitadel is Go binary — 50MB RAM idle vs Keycloak's 800MB
    environment:
      ZITADEL_DATABASE_POSTGRES_HOST: postgres
      ZITADEL_MASTERKEY: ${ZITADEL_MASTERKEY}
    restart: unless-stopped
    # NOTE: No OpenSearch, no RabbitMQ — uses PostgreSQL FTS + Redis
```

## Deployment Commands Per Model

```bash
# SaaS (cloud hosted — full stack with OpenSearch + Auth)
docker compose \
  -f infrastructure/docker/docker-compose.base.yml \
  -f infrastructure/docker/docker-compose.saas.yml \
  --profile saas up -d

# Self-Hosted (minimal footprint — school on-premise server)
docker compose \
  -f infrastructure/docker/docker-compose.base.yml \
  -f infrastructure/docker/docker-compose.selfhosted.yml \
  up -d

# Development (local, minimal)
docker compose -f infrastructure/docker/docker-compose.dev.yml up -d
```

---

# Tenant Database Schema

```sql
-- The central tenants table that powers all multi-tenancy

CREATE TABLE tenants (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(255) NOT NULL,
    slug            VARCHAR(100) UNIQUE NOT NULL,       -- e.g. "stmarys"

    -- Domain Routing
    subdomain       VARCHAR(100) UNIQUE,                -- stmarys.neelstack.com
    custom_domain   VARCHAR(255) UNIQUE,                -- erp.stmarys.edu (White Label)

    -- Deployment Model
    deployment_model VARCHAR(50) NOT NULL               -- saas_rls | schema_isolated | dedicated | self_hosted
        CHECK (deployment_model IN ('saas_rls', 'schema_isolated', 'dedicated', 'self_hosted')),

    -- Database Isolation
    db_schema       VARCHAR(100),                       -- For schema_isolated mode
    dedicated_db_url TEXT,                              -- For dedicated/self_hosted mode (encrypted)

    -- Subscription
    plan            VARCHAR(50) NOT NULL DEFAULT 'saas_free',

    -- Branding (JSON, cached in Redis)
    branding        JSONB NOT NULL DEFAULT '{}'::jsonb,

    -- Feature Flags (JSON, derived from plan at runtime)
    feature_overrides JSONB NOT NULL DEFAULT '{}'::jsonb,  -- Per-tenant overrides

    -- Status
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index for fast domain lookups (used every request)
CREATE INDEX idx_tenants_subdomain ON tenants(subdomain) WHERE subdomain IS NOT NULL;
CREATE INDEX idx_tenants_custom_domain ON tenants(custom_domain) WHERE custom_domain IS NOT NULL;
```

---

# Deployment Decision Tree

Use this tree to determine which deployment model and configuration to apply for a new customer:

```text
Start: New Customer Onboarding
            │
            ▼
Does the customer want to manage their own servers?
            │
   YES ─────┴──── NO
    │               │
    ▼               ▼
Self-Hosted     Do they want a custom domain and branding?
                    │
           YES ─────┴──── NO
            │               │
            ▼               ▼
       White Label     NeelStack-managed dedicated infra?
                            │
                   YES ─────┴──── NO
                    │               │
                    ▼               ▼
              Dedicated          SaaS Plan
              Cloud          (Free/Standard/Enterprise)
```

---

# Anti-Patterns — What NOT to Do

> [!CAUTION]
> Violating these rules will cause cross-tenant data leaks, branding failures, or deployment model lock-in.

❌ **Direct deployment model checks in business logic:**
```python
# WRONG — hardcoded deployment model check in business logic
if tenant.deployment_model == "self_hosted":
    use_local_ai()
else:
    use_cloud_ai()

# CORRECT — check feature flag instead
if tenant.features.ai_academic_assistant:
    use_ai()
```

❌ **Missing tenant_id in database queries:**
```python
# WRONG — no tenant filter, data leak risk
students = await db.execute("SELECT * FROM students")

# CORRECT — RLS handles it automatically when tenant middleware is set
students = await db.execute("SELECT * FROM students")
# RLS policy enforces: WHERE tenant_id = current_setting('app.current_tenant_id')
```

❌ **Hardcoded NeelStack branding in UI components:**
```tsx
// WRONG — hardcoded brand color
<button style={{ background: "#6366F1" }}>Submit</button>

// CORRECT — use CSS variable injected by white-label engine
<button style={{ background: "var(--color-primary)" }}>Submit</button>
```

❌ **Single Docker Compose for all deployments:**
```bash
# WRONG — same docker-compose for cloud and self-hosted
# Forces schools to run OpenSearch, RabbitMQ, Keycloak on 4GB VMs

# CORRECT — separate compose files per deployment profile
docker compose -f docker-compose.selfhosted.yml up -d
```

---

# Self-Hosted Deployment Package

When a customer deploys self-hosted, they receive a deployment package that is designed to run on a minimum 8GB RAM server.

## Minimum Requirements

| Resource | Minimum | Recommended |
| :--- | :--- | :--- |
| RAM | 8 GB | 16 GB |
| CPU | 4 cores | 8 cores |
| Disk | 100 GB SSD | 500 GB SSD |
| OS | Ubuntu 22.04 LTS | Ubuntu 24.04 LTS |
| Docker | 24.x + Compose v2 | Latest stable |

## Self-Hosted Setup — 5 Commands

The goal: a school IT admin with basic Docker knowledge can deploy the full platform in under 30 minutes.

```bash
# Step 1: Download deployment package
curl -sSL https://deploy.neelstack.com/selfhosted/install.sh | bash

# Step 2: Configure environment
cp .env.example .env
nano .env  # Set DB passwords, domain, admin email

# Step 3: Launch (minimal profile — no OpenSearch, no heavy auth server)
docker compose -f docker-compose.selfhosted.yml up -d

# Step 4: Run database migrations
docker compose exec core-api alembic upgrade head

# Step 5: Create first admin account
docker compose exec core-api python -m cli.create_admin --email admin@school.edu
```

---

# Production Checklist

- [ ] Tenant resolution middleware is installed and tested for all three domain types (subdomain, custom domain, localhost)
- [ ] PostgreSQL RLS policies are active on all shared tenant tables
- [ ] Schema-per-tenant migration script is tested with at least 3 tenants
- [ ] White-label branding API returns correct config and falls back to NeelStack defaults
- [ ] Next.js layout injects CSS variables from branding API at page load
- [ ] Feature flags are correctly resolved from subscription plan with no hardcoded deployment model checks
- [ ] Docker Compose profiles are validated for `saas`, `dedicated`, and `selfhosted`
- [ ] Self-hosted deployment completes in under 30 minutes on a clean Ubuntu server
- [ ] Cross-tenant data isolation is tested (attempting to access Tenant B's data from Tenant A's session must return 0 rows)
- [ ] Tenant onboarding script provisions database schema, seeds default data, and creates first admin in < 60 seconds

---

# Success Criteria

The Multi-Tenant Deployment Strategy is successful when:

1. A new SaaS tenant can be onboarded programmatically in under 60 seconds.
2. A White Label tenant's branding is reflected across all UI surfaces and email templates without any code changes.
3. A Self-Hosted deployment runs stable on a server with 8GB RAM.
4. Cross-tenant data isolation is verified by automated tests — no cross-contamination is possible.
5. A developer can add a new domain module without knowing which deployment model it will run on.

---

# Custom Domain Resolution — Full Reference

## Every Domain Format Supported

The platform resolves tenant identity from the HTTP `Host` header on every request.
No matter what domain format the client uses, the middleware handles it identically.

```text
Domain Format                  Example                         Works?
──────────────────────────────────────────────────────────────────────
NeelStack Subdomain            abcschool.neelstack.com         ✅ YES
Client Subdomain               erp.abcschool.com               ✅ YES
Client Apex Domain             abcschool.com                   ✅ YES
www + Apex Domain              www.abcschool.com               ✅ YES  (auto-stripped)
Any TLD                        erp.stmaryschool.org            ✅ YES
Any TLD Apex                   stmaryschool.in                 ✅ YES
Self-Hosted + NeelStack DNS    myschool.neelstack.com          ✅ YES
```

## Domain Resolution Flow

```text
Incoming Request: Host: abcschool.com
        │
        ▼
normalise_domain()
  • Strip port if present    abcschool.com:443 → abcschool.com
  • Lowercase                AbcSchool.COM    → abcschool.com
        │
        ▼
DEPLOYMENT_CONTEXT == "self_hosted"?
  ├── YES → Load from env vars (TENANT_DOMAIN, TENANT_NAME, etc.)
  │         No database query. Single-tenant. Done.
  └── NO  → SaaS multi-tenant path:
                │
                ▼
        www. prefix? → strip it (www.abcschool.com → abcschool.com)
        Build candidate list: [abcschool.com]
                │
                ▼
        Redis cache lookup (TTL=5min)
          HIT → deserialise TenantContext. Done.
          MISS → PostgreSQL query:
                  WHERE custom_domain IN (candidates)
                     OR subdomain IN (candidates)
                  AND is_active = true
                │
                ▼
        Tenant found?
          NO  → HTTP 404 with tenant_not_found JSON
          YES → Build TenantContext
                Cache in Redis
                Attach to request.state.tenant
```

## How to Register a Custom Domain (SaaS / Dedicated Cloud)

When a client wants `abcschool.com` (or any domain they own) to serve the ERP:

1. **Client side** — In their DNS registrar (Cloudflare, GoDaddy, Route53, etc.):
   - Set an `A` record: `abcschool.com → [NeelStack Load Balancer IP]`
   - Set a `CNAME` record: `www.abcschool.com → abcschool.com`

2. **NeelStack operator side** — Update the tenant record in the admin database:
   ```sql
   UPDATE tenant
   SET custom_domain = 'abcschool.com'
   WHERE slug = 'abcschool';
   ```
   Or via the Tenant Provisioning API (once available):
   ```http
   PATCH /admin/tenants/abcschool
   Content-Type: application/json
   { "custom_domain": "abcschool.com" }
   ```

3. **TLS** — cert-manager (Kubernetes) or Traefik (self-hosted Docker) issues a
   Let's Encrypt certificate for `abcschool.com` and `www.abcschool.com` automatically.
   No manual certificate steps. No downtime.

## Self-Hosted: No NeelStack Admin DB Required

When `DEPLOYMENT_CONTEXT=self_hosted`, the middleware does NOT query any NeelStack database.
The client is fully autonomous. Their tenant identity comes from `.env`:

```bash
# .env (client fills this in)
DEPLOYMENT_CONTEXT=self_hosted
TENANT_DOMAIN=abcschool.com     # or erp.abcschool.com — any format
TENANT_NAME=ABC School
TENANT_SLUG=abcschool
TENANT_APP_NAME=ABC School ERP
TENANT_PRIMARY_COLOR=#1A3C6E
```

The middleware builds the `TenantContext` from these vars **once at startup**,
caches it in memory, and reuses it on every request — zero database overhead per request.

## Domain Coexistence: Apex + NeelStack subdomain simultaneously

A client can have BOTH domains active at the same time during a DNS migration:

```sql
-- Tenant has both domains — requests on either work identically
SELECT subdomain, custom_domain FROM tenant WHERE slug = 'abcschool';
-- Result: abcschool.neelstack.com | abcschool.com
```

Traffic from `abcschool.neelstack.com` → matches `subdomain` column  
Traffic from `abcschool.com` → matches `custom_domain` column  
Both resolve to the same tenant record — same data, same session, same features.

This enables zero-downtime domain migration:
1. Set `custom_domain = 'abcschool.com'` while keeping `subdomain` active
2. Client updates DNS to point to NeelStack
3. Verify the new domain works
4. Decommission the `neelstack.com` subdomain (optional)

## Relational Feature Modularity (ADR-011)

NeelStack EduOS separates feature access from both deployment contexts and billing plan tiers through an orthogonal module manager. Instead of hardcoding feature gates, we represent features as rows in a `modules` relation:

- **SaaS Modularity**: The backend mounts API routers, event routes, and webhooks dynamically based on the tenant's `tenant_modules` registry entries.
- **Resource Footprint Optimization**: For self-hosted instances, if AI modules are disabled in the manifest, the deployment scripts skip provisioning the Ollama sidecar and AI Gateway container entirely.
- **Client Navigation**: Dynamic sidebar navigation matrices are fetched via `GET /api/v1/tenant/modules`, ensuring that only enabled modules show up in the parent, teacher, student, or admin portals.

## Database & pgvector RLS Hardening (ADR-012)

Data isolation is guaranteed through transactional safety bounds at the database level:

- **Transaction Scope**: To prevent data leakages in shared connection pools, the middleware executes database session parameters inside explicit transaction scopes (`SET LOCAL app.current_tenant_id`) which are discarded when transactions exit.
- **Vector Isolation**: Active database-level row-level security (RLS) policies apply to the `document_vectors` table:
  ```sql
  ALTER TABLE document_vectors ENABLE ROW LEVEL SECURITY;
  ALTER TABLE document_vectors FORCE ROW LEVEL SECURITY;
  ```
- **Envelope Encryption**: High-value credentials (like dedicated database links) are encrypted via per-tenant Data Encryption Keys (DEKs) wrapped by a KMS master key.

---

# Document Status

**Document:** NES-111 — Multi-Tenant Deployment Strategy  
**Version:** 2.0.0  
**Status:** Approved  
**Owner:** Chief Solution Architect  
**Last Updated:** July 2026 — Integrated Relational Feature Modularity (ADR-011) and Database RLS Hardening (ADR-012) standards.  
**Next Review:** January 2027  
**Next Document:** **NES-112 — API Gateway Standards**
