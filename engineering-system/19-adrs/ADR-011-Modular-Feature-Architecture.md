# ADR-011 — Modular Feature Architecture

## Context
NeelStack EduOS historically coupled features and capability access directly to plan tiers (e.g., `saas_free`, `saas_premium`, `self_hosted`). This represents a single-axis model that fails to support real-world customer segmentation where:
- A small self-hosted school wants a lightweight website and zero AI capabilities.
- An enterprise SaaS tenant wants standard operations plus specific RAG modules, but has no use for library or transport logistics.
- Custom modules must be provisioned and billed individually as à la carte add-ons.

We require a second, orthogonal axis representing **modules** that decouple capability enablement from both the billing plan and the hosting environment context.

## Decision
We will transition from the fixed plan-linked enum system and the unstructured `feature_overrides` JSONB column to a formal relational schema.

### 1. Database Schema Specifications

We will introduce `modules` and `tenant_modules` tables:

```sql
CREATE TABLE modules (
    id              VARCHAR(50) PRIMARY KEY,      -- e.g. 'ai_assistant', 'fees', 'transport', 'library'
    name            VARCHAR(100) NOT NULL,
    category        VARCHAR(50) NOT NULL,         -- 'ai' | 'academic' | 'operations' | 'communication'
    depends_on      VARCHAR(50)[],                 -- ['exams'] — grade prediction needs exams module
    requires_service VARCHAR(50),                  -- 'ai-gateway' — tracks service sidecars
    is_core         BOOLEAN DEFAULT FALSE          -- true for auth, settings, core admins
);

CREATE TABLE tenant_modules (
    tenant_id   UUID NOT NULL,
    module_id   VARCHAR(50) REFERENCES modules(id),
    enabled     BOOLEAN NOT NULL DEFAULT FALSE,
    config      JSONB DEFAULT '{}'::jsonb,          -- e.g. AI: {provider: "openai", monthly_cap_usd: 200}
    enabled_at  TIMESTAMPTZ DEFAULT NOW(),
    enabled_by  UUID,                               -- admin audit ID
    PRIMARY KEY (tenant_id, module_id)
);
```

### 2. Runtime Execution & Core Loading
- **Dynamic API Mounting**: The Core FastAPI application will read the resolved tenant's module catalog upon middleware entry and conditionally mount routers, middleware, and websocket event buses based on active modules.
- **Compose Manifest Generation**: For self-hosted and dedicated setups, deployment scripts will fetch the tenant modules manifest and construct a pruned `docker-compose.yml` file. If no AI modules are enabled, the Ollama and AI Gateway containers are completely omitted from the startup runtime footprint.
- **Frontend Navigation Generation**: The experience portal will dynamically fetch the tenant's module configuration list (`GET /api/v1/tenant/modules`) during initial hydration to build sidebars and UI navigation panels, replacing client-side static route tables.

## Consequences
- **Positive**: High efficiency on self-hosted boxes (reduces CPU/RAM overhead by skipping containers that are not needed).
- **Positive**: Modular à la carte subscription billing and pricing are natively supported.
- **Positive**: Server-side validation of module dependencies prevents invalid configurations (e.g. enabling predictive analytics without examinations enabled).
- **Negative**: Extra query during resolution phase. Mitigated by caching the tenant module manifest as part of the primary Redis tenant cache block.
