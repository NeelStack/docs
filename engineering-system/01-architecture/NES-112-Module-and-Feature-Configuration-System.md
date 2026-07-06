---
document_id: NES-112
title: Module & Feature Configuration System
subtitle: Decoupling Feature Availability from Plan and Deployment Model
version: 1.0.0
status: Draft — Pending Review
classification: Internal
owner: Chief Solution Architect
review_cycle: Every 6 Months
document_type: Architecture Decision Record (ADR)
parent_document: NES-111 Multi-Tenant Deployment Strategy
next_document: NES-113 Security & Isolation Hardening Standard
supersedes_next_doc_number: "NES-112 was previously reserved for API Gateway Standards, which is renumbered to NES-114"
---

# NES-112 — Module & Feature Configuration System

> **"Every feature is optional. Every customer's platform looks exactly as complex as they need it to be — no more, no less."**

---

# 1. Problem Statement

The current design (NES-111) ties feature availability to a single `plan` enum (`saas_free`, `saas_standard`, `saas_enterprise`, `white_label`, `dedicated_cloud`, `self_hosted`), resolved into a `FeatureFlags` object via `PLAN_FEATURE_MAP`, with a secondary `tenants.feature_overrides` JSONB column for per-tenant exceptions.

This conflates three things that are actually independent:

1. **Deployment model** — where and how the tenant is hosted (SaaS / white label / dedicated / self-hosted)
2. **Commercial plan** — what the customer is billed for
3. **Feature/module selection** — which capabilities are actually switched on for this tenant

Real customer requirements don't map cleanly onto a plan enum:

- A small school wants a simple public website + admissions form, nothing else — no AI, no fee management, no transport module.
- A mid-size self-hosted school wants the full operational ERP but explicitly does **not** want AI features (data sensitivity, cost, or trust reasons).
- A large enterprise SaaS tenant wants AI + custom fee logic but not transport or hostel modules, plus one bespoke module built for them specifically.

Under the current model, satisfying all three requires either plan proliferation (a new plan enum value per combination) or silent divergence via `feature_overrides` with no clear precedence rules, no dependency validation, and no audit trail of who enabled what.

**Decision:** Introduce a relational **Module System** as a first-class, independent axis. Plan determines commercial entitlement ceiling (which modules a tenant is *allowed* to enable); the module system determines what is actually *running* for that tenant.

---

# 2. Core Principle

> [!IMPORTANT]
> **The Golden Rule (extended from NES-111):** Business logic MUST NEVER check `plan` or `deployment_model` to decide whether a feature is available. It checks **module enablement** only.
>
> ❌ **WRONG:** `if tenant.plan == "saas_enterprise": show_ai_assistant()`
>
> ✅ **CORRECT:** `if tenant.modules.is_enabled("ai_assistant"): show_ai_assistant()`

Plan governs *what a tenant is entitled to enable*. Modules govern *what is actually enabled*. A tenant can be entitled to AI under their plan and still have it switched off.

---

# 3. Data Model

```sql
-- Master module catalog — one row per feature module the platform supports
CREATE TABLE modules (
    id                  VARCHAR(50) PRIMARY KEY,        -- 'ai_assistant', 'fees', 'transport', 'website_cms'
    name                VARCHAR(100) NOT NULL,
    description         TEXT,
    category            VARCHAR(50) NOT NULL,            -- 'ai' | 'academic' | 'operations' | 'communication' | 'core'
    depends_on          VARCHAR(50)[] DEFAULT '{}',       -- e.g. grade_prediction depends on exams
    requires_service    VARCHAR(50),                      -- 'ai-gateway' | 'sockets' | NULL — informs compose generation
    is_core             BOOLEAN NOT NULL DEFAULT FALSE,   -- cannot be disabled (auth, tenant admin, billing)
    config_schema       JSONB,                            -- JSON Schema describing valid `config` shape for this module
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Per-tenant module state
CREATE TABLE tenant_modules (
    tenant_id       UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    module_id       VARCHAR(50) NOT NULL REFERENCES modules(id),
    enabled         BOOLEAN NOT NULL DEFAULT FALSE,
    config          JSONB NOT NULL DEFAULT '{}'::jsonb,   -- e.g. {"provider": "openai", "monthly_cap_usd": 200}
    enabled_at      TIMESTAMPTZ,
    enabled_by      UUID,                                  -- references admin_users.id — audit trail
    disabled_at     TIMESTAMPTZ,
    disabled_by     UUID,
    PRIMARY KEY (tenant_id, module_id)
);

-- Which modules a given commercial plan entitles a tenant to enable (ceiling, not floor)
CREATE TABLE plan_module_entitlements (
    plan            VARCHAR(50) NOT NULL,
    module_id       VARCHAR(50) NOT NULL REFERENCES modules(id),
    included        BOOLEAN NOT NULL DEFAULT TRUE,          -- included in base plan price
    addon_price_usd NUMERIC(10,2),                          -- if not included, price to add it
    PRIMARY KEY (plan, module_id)
);

CREATE INDEX idx_tenant_modules_tenant ON tenant_modules(tenant_id) WHERE enabled = TRUE;
```

## Resolution Order (single source of truth)

1. Look up `plan_module_entitlements` for the tenant's plan → gives the *ceiling* (what they're commercially allowed to turn on, and at what cost if it's an add-on).
2. Look up `tenant_modules` → gives the *actual* state (on/off + config) for this specific tenant.
3. A module can only be `enabled = true` in `tenant_modules` if it has a corresponding entitlement row (included or paid add-on) for the tenant's current plan. Enforced via application-layer check on the enable endpoint, not a DB constraint, since plan changes shouldn't retroactively force-disable modules already running — instead a plan downgrade flags modules as "enabled but not entitled" for a support conversation, rather than silently breaking a tenant mid-session.

This replaces `PLAN_FEATURE_MAP` and `tenants.feature_overrides` entirely. Both are deprecated on adoption of this ADR.

---

# 4. Module Loader — Runtime Behavior

```python
# services/core/src/app/shared/module_registry.py

from functools import lru_cache
from app.shared.models import TenantContext

class ModuleRegistry:
    """
    Resolves the effective set of enabled modules + their config for a tenant.
    This is the ONLY place business logic should query module state.
    """

    @classmethod
    async def get_enabled_modules(cls, tenant_id: str) -> dict[str, dict]:
        """
        Returns: { "ai_assistant": {"provider": "openai", "monthly_cap_usd": 200}, ... }
        Only includes modules where enabled = true.
        Cached in Redis with short TTL (60s) — module toggles should feel near-instant to admins.
        """
        cache_key = f"tenant_modules:{tenant_id}"
        cached = await redis_client.get(cache_key)
        if cached:
            return json.loads(cached)

        async with get_admin_db() as db:
            rows = await db.execute(
                "SELECT module_id, config FROM tenant_modules WHERE tenant_id = $1 AND enabled = true",
                tenant_id
            )
        result = {row.module_id: row.config for row in rows}
        await redis_client.setex(cache_key, 60, json.dumps(result))
        return result

    @classmethod
    async def is_enabled(cls, tenant: TenantContext, module_id: str) -> bool:
        modules = await cls.get_enabled_modules(tenant.id)
        return module_id in modules

    @classmethod
    async def validate_dependencies(cls, tenant_id: str, module_id: str) -> list[str]:
        """
        Returns list of unmet dependencies. Empty list = safe to enable.
        Called by the admin enable-module endpoint before writing enabled=true.
        """
        module = await cls._get_module_definition(module_id)
        enabled = await cls.get_enabled_modules(tenant_id)
        return [dep for dep in module.depends_on if dep not in enabled]
```

### API surface

```http
GET  /api/v1/tenant/modules              # frontend nav-building — public per-tenant, cached
GET  /api/v1/admin/modules                # full catalog + entitlement + current state, for settings screen
POST /api/v1/admin/tenants/{id}/modules/{module_id}/enable
POST /api/v1/admin/tenants/{id}/modules/{module_id}/disable
```

`enable` rejects with `409 Conflict` and the list of unmet dependencies if `validate_dependencies` returns non-empty. `disable` on a module other modules depend on returns `409` with the list of dependents, requiring the admin to disable those first or confirm a cascade.

---

# 5. Frontend Integration — No Hardcoded Navigation

```typescript
// apps/web/lib/modules.ts

export interface EnabledModule {
  id: string;
  config: Record<string, unknown>;
}

export async function fetchEnabledModules(): Promise<EnabledModule[]> {
  const res = await fetch('/api/v1/tenant/modules', { next: { revalidate: 60 } });
  return res.json();
}
```

Sidebar, dashboard widgets, and mobile app tab bars are all built by iterating the enabled-module list — never by a hardcoded switch on plan or deployment model. A "simple site" tenant with only `website_cms` and `admissions` enabled sees exactly two nav items and nothing else; this is a rendering consequence of module state, not a special UI mode.

---

# 6. Infrastructure Consequence — Compose Generation

NES-111 keyed Docker Compose profiles to *deployment model* only (`saas` / `selfhosted`). That is necessary but not sufficient: a self-hosted tenant with AI disabled should not run the Ollama sidecar or AI gateway container at all.

```python
# scripts/generate_compose.py (self-hosted installer step, run before `docker compose up`)

def generate_compose(deployment_model: str, enabled_modules: list[str]) -> str:
    services = load_base_services(deployment_model)  # core-api, postgres, redis always present

    if any(m in enabled_modules for m in ("ai_assistant", "grade_prediction", "plagiarism_detection")):
        services += load_service_fragment("ai-gateway")
        if deployment_model == "self_hosted":
            services += load_service_fragment("ollama-sidecar")

    if "transport" in enabled_modules:
        services += load_service_fragment("transport-worker")

    return render_compose_yaml(services)
```

The self-hosted installer (`install.sh` from NES-111) runs this generation step using the tenant's module selection captured during setup, rather than shipping one fixed compose file per deployment model. This keeps a "simple site" self-hosted install genuinely lightweight — no AI gateway, no vector store, no wasted RAM on an 8GB box.

---

# 7. Anti-Patterns

> [!CAUTION]

❌ **Checking plan directly for feature gating:**
```python
# WRONG
if tenant.plan in ("saas_enterprise", "dedicated_cloud"):
    enable_saml()

# CORRECT
if await ModuleRegistry.is_enabled(tenant, "saml_sso"):
    enable_saml()
```

❌ **Enabling a module without dependency validation:**
```python
# WRONG — directly flips the flag
await db.execute("UPDATE tenant_modules SET enabled = true WHERE ...")

# CORRECT — goes through the validated endpoint
unmet = await ModuleRegistry.validate_dependencies(tenant_id, "grade_prediction")
if unmet:
    raise HTTPException(409, detail={"unmet_dependencies": unmet})
```

❌ **Silent divergence via ad-hoc JSONB overrides** — the `tenants.feature_overrides` pattern from NES-111 is deprecated by this ADR precisely because it has no audit trail and no dependency checking. All module state changes go through `tenant_modules` with `enabled_by`/`disabled_at` populated.

---

# 8. Migration Plan (from NES-111's PLAN_FEATURE_MAP)

1. Populate `modules` table with the current fixed flag set (`ai_academic_assistant` → `ai_assistant`, `saml_sso_enabled` → `saml_sso`, etc.) — one-time mapping.
2. Populate `plan_module_entitlements` from the existing `PLAN_FEATURE_MAP` dict — this preserves current behavior exactly on day one.
3. Backfill `tenant_modules` for every existing tenant based on their current plan's entitlements (enabled = entitlement default).
4. Deploy `ModuleRegistry` alongside the old flag resolution, running both in parallel with a comparison log for one release cycle to catch discrepancies before cutover.
5. Cut business logic over to `ModuleRegistry.is_enabled()` calls, module by module, starting with the lowest-risk (`website_cms`, `admissions`) and ending with AI and billing-adjacent modules last.
6. Remove `PLAN_FEATURE_MAP` and `tenants.feature_overrides` once cutover is verified in production for all tenants.

---

# 9. Production Checklist

- [ ] `modules`, `tenant_modules`, `plan_module_entitlements` tables created and backfilled
- [ ] Dependency validation rejects enabling a module with unmet dependencies (tested)
- [ ] Disabling a depended-upon module is blocked or requires explicit cascade confirmation (tested)
- [ ] Compose generator produces a minimal self-hosted stack for a module set with AI disabled — verified no Ollama/AI-gateway container starts
- [ ] Frontend nav renders correctly for a tenant with only 2 modules enabled ("simple site" case) and for a tenant with all modules enabled
- [ ] Admin Settings → Modules screen supports enable/disable with audit trail visible (`enabled_by`, `enabled_at`)
- [ ] Old `PLAN_FEATURE_MAP` / `feature_overrides` code paths fully removed post-migration, no dual-read remaining
- [ ] Downgrade-plan scenario tested: tenant with a module enabled beyond their new plan's entitlement is flagged, not force-disabled without notice

---

# 10. Success Criteria

1. A "simple site" self-hosted school runs with zero AI infrastructure provisioned — no wasted RAM, no unnecessary attack surface.
2. An enterprise tenant can enable AI and fees while leaving transport and hostel modules off, with no plan proliferation required.
3. A new module can be added to the catalog and enabled for a single pilot tenant without a code deploy touching any other tenant's runtime behavior.
4. Support can answer "why does this tenant have feature X" by reading one row in `tenant_modules`, including who enabled it and when.

---

# Document Status

**Document:** NES-112 — Module & Feature Configuration System
**Version:** 1.0.0
**Status:** Draft — Pending Review
**Owner:** Chief Solution Architect
**Next Review:** Prior to Phase 2 implementation kickoff
**Next Document:** NES-113 — Security & Isolation Hardening Standard
