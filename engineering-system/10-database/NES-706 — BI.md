---
document_id: NES-706
title: BI
subtitle: Enterprise Business Intelligence, Semantic Layers & Dashboard Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Business Intelligence Board
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-705 Analytics
next_document: NES-707 ML Pipelines
---

# NES-706 — BI

> **"Data visualization must reflect a single source of truth. We build standardized business intelligence dashboards using semantic modeling layers."**

---

# Executive Summary

Organizations require reports, charts, and key performance indicator (KPI) dashboards to guide operational decisions.

If individual analysts define their own metrics, query raw databases directly, or build custom dashboards without version control, metric inconsistencies emerge (e.g. Finance defines "active customer" differently than Marketing).

We mandate the centralization of all BI reports under a unified **Semantic Modeling Layer** (powered by **Looker LookML / CubeJS**).

This standard defines our metric governance rules, visualization standards, and dashboard access controls.

---

# Purpose

This standard defines:

- Business Intelligence Tooling (Looker / Apache Superset)
- The Semantic Modeling Layer (LookML)
- Metric Definitions Governance
- Dashboard Design and Cache Policies
- Row-Level Access Security (RLS)

---

# Centralized Semantic Layer (LookML)

We prohibit BI tools from writing raw SQL queries directly against warehouse tables. All dashboards must query a centralized **Semantic Layer**.

- **Definition**: The Semantic Layer maps raw database schemas to user-friendly attributes and metrics (e.g. defining `revenue` once as `sum(invoice_amount - tax_amount)`).
- **Version Control**: Semantic models (LookML files) must be version-controlled in Git and undergo peer review before deployment.

---

# Metric Definitions Governance

To prevent metric inconsistencies:

- **The Metric Registry**: Core business KPIs (e.g., Monthly Active Users, Revenue, Customer Acquisition Cost) must be documented in the central data registry.
- **Single Owner**: Metric changes require approval from the data domain owner. Developers must not implement custom variations of standard metrics for specific dashboards.

---

# Dashboard Cache Policies

Analytical queries are expensive and compute-intensive.

- **Aggressive Caching**: Enforce default **24-hour cache** windows on all executive and non-real-time dashboards.
- **Cache Warming**: Configure automated scripts to pre-warm dashboard caches during early morning hours so reports load instantly when users log in.

---

# Row-Level Security (RLS)

Protect tenant data privacy in multi-tenant BI dashboards.

- **Standard**: Configure Row-Level Security (RLS) inside the semantic layer.
- **Mechanism**: Dynamically inject user attributes (e.g. `tenant_id`) into SQL queries at runtime, ensuring tenant users can only see metrics belonging to their organization.

```lookml
# Example LookML Row-Level Security filter
access_filter: {
  user_attribute: tenant_id
  field: customer.tenant_id
}
```

---

# Anti-Patterns

❌ **Hardcoded Dashboard Metrics**: Defining KPI formulas directly inside a single visualization chart, making the metric unavailable or inconsistent across other reports.

❌ **Exposing PII in BI Reports**: Displaying customer phone numbers, home addresses, or emails on public corporate dashboards without business justification or encryption.

❌ **Real-Time Queries for Large Reports**: Configuring dashboards to query the warehouse live on every browser refresh, driving up cloud compute costs.

---

# Production Checklist

- [ ] LookML files are version-controlled and pass linting checks.
- [ ] Row-Level Security (RLS) is active for multi-tenant dashboards.
- [ ] Cache policies are defined and verified.
- [ ] Core metrics map to the central business glossary.
- [ ] SSO integration is active for all BI tools.

---

# Success Criteria

The Business Intelligence program is successful when:
- Different dashboards show identical values for shared business KPIs.
- Dashboard pages render in less than 3.0 seconds due to cached queries.
- Tenant data isolation is preserved in all multi-tenant reports.

---

# Document Status

**Document:** NES-706 — BI
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-707 — ML Pipelines**
