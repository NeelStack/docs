---
document_id: NES-703
title: ELT
subtitle: Enterprise Extract, Load, Transform (ELT) & dbt Standards
version: 1.0.0
status: Draft
classification: Internal
owner: Data Engineering Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-702 ETL
next_document: NES-704 Lakehouse
---

# NES-703 — ELT

> **"Load raw data, transform at scale. We standardize on dbt to build modular, tested, and version-controlled SQL transformations inside our data warehouse."**

---

# Executive Summary

Traditional ETL frameworks transform data on separate mid-tier compute servers before writing it to database disks.

With high-performance, columnar cloud warehouses (Snowflake, BigQuery), we decouple ingestion from transformation.

We mandate the **ELT (Extract, Load, Transform)** pattern.

We standardize on **dbt (data build tool)** to write SQL-based transformations that compile and execute directly inside our data warehouse.

This standard establishes our dbt model conventions, schema structures, testing configurations, and version control guidelines.

---

# Purpose

This standard defines:

- ELT Architecture Principles
- dbt Directory and Model Layouts
- Schema Tiering (Staging, Marts)
- dbt Test Configurations and Data Quality
- CI/CD Pull Request Validation Gates

---

# dbt Project Layout

All database transformations must be declared in a version-controlled dbt project:

```text
dbt_project/
├── dbt_project.yml        # Project configuration and model materialization
├── models/
│   ├── staging/           # Raw data clean-up and type casting
│   │   ├── eduos/
│   │   │   ├── stg_eduos__students.sql
│   │   │   └── schema.yml # YAML validations for staging sources
│   │
│   ├── intermediate/      # Complex joins and logical aggregations
│   │
│   └── marts/             # Business ready tables (Fact & Dimensions)
│       ├── finance/
│       │   └── dim_invoices.sql
│       └── core/
│           └── dim_students.sql
```

---

# Schema Tiering Standards

Data flows through three distinct schema transformation zones inside the warehouse:

- **Staging (`stg_`)**: Simple views that clean column names, cast string datatypes to correct formats, and enforce timezone consistency. Avoid joins in this zone.
- **Intermediate (`int_`)**: Ephemeral or table models that execute entity joins, calculate logical aggregates, and parse JSON payloads.
- **Marts (`dim_` / `fct_`)**: Final tables structured in star schemas (NES-701) ready to be queried by BI dashboards and reporting tools.

---

# Model Code Standards

- **Use CTEs (Common Table Expressions)**: All model files must use CTEs for readability, structuring inputs at the top and the final select statement at the bottom.
- **Use `ref` and `source` Functions**: Never hardcode database table names. Always use the `{{ ref('model_name') }}` or `{{ source('source_name', 'table_name') }}` functions to build the data lineage graph automatically.

### Reference dbt Model:

```sql
with source_students as (
    select * from {{ ref('stg_eduos__students') }}
),

active_students as (
    select
        student_id,
        first_name,
        last_name,
        email,
        registration_date
    from source_students
    where status = 'active'
)

select * from active_students
```

---

# Data Quality Testing

Every dbt model must contain testing assertions declared in the schema YAML configuration:

- **Primary Keys**: Must pass `unique` and `not_null` assertions.
- **Foreign Keys**: Must validate references to dimension parent tables using `relationships` checks.
- **Enumerations**: Fields containing status strings must pass `accepted_values` validation (e.g. `['active', 'inactive', 'pending']`).

```yaml
version: 2

models:
  - name: stg_eduos__students
    columns:
      - name: student_id
        tests:
          - unique
          - not_null
      - name: email
        tests:
          - not_null
      - name: status
        tests:
          - accepted_values:
              values: ['active', 'inactive', 'pending']
```

---

# CI/CD Validation Gates

All dbt pull requests must pass automated validation runs before merging:

- **dbt compile**: Compiles SQL templates to verify syntax correctness.
- **Slim CI**: Runs `dbt run --select state:modified+` to build and test only the modified models and their downstream dependencies inside a temporary PR schema sandbox, protecting production data.

---

# Anti-Patterns

❌ **Hardcoded Database Paths**: Referencing tables directly in models like `SELECT * FROM prod_db.raw_schema.users`, which prevents compile runs from targeting dev or staging schemas during testing.

❌ **Over-Materializing Models**: Configuring every model as a physical `table` inside the warehouse, driving up storage write costs. Use `view` or `ephemeral` modes by default.

❌ **Performing Transforms in BI Dashboards**: Writing complex calculation logic inside visualization tools (e.g. Looker custom formulas) instead of centralizing them in the dbt transform layer.

---

# Production Checklist

- [ ] Project compiles cleanly via `dbt compile`.
- [ ] Staging models use `stg_` prefix naming conventions.
- [ ] YAML tests are configured for all key fields.
- [ ] Target schemas utilize OIDC key authorizations.
- [ ] Slim CI pipeline is active on the repository.

---

# Success Criteria

The ELT transform platform is successful when:
- 100% of data transformations are defined as SQL code and checked into Git.
- Schema changes propagate safely across environments without user intervention.
- Automated tests identify and block invalid data payloads before they reach business reports.

---

# Document Status

**Document:** NES-703 — ELT
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-704 — Lakehouse**
