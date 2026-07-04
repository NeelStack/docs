---
document_id: NES-702
title: ETL
subtitle: Enterprise Extract, Transform, Load (ETL) & Orchestration Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Data Engineering Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-701 Warehousing
next_document: NES-703 ELT
---

# NES-702 — ETL

> **"Data movement must be orchestrated and traceable. We build resilient, automated ETL pipelines using DAGs and transaction boundaries."**

---

# Executive Summary

Extracting data from transactional databases, transforming schemas for analysis, and loading them into historical warehouses (ETL) is a core operations workflow.

Ad-hoc cron jobs or cron scripts that run without dependency tracking, error alerts, retry logs, or SLA windows are unreliable.

We mandate the centralization of all data shipping pipelines under a unified **ETL Orchestrator** (powered by **Apache Airflow / Prefect**).

This standard defines the pipeline creation guidelines, DAG configurations, retry policies, and transaction boundaries.

---

# Purpose

This standard defines:

- Workflow Orchestration (Apache Airflow / Prefect)
- Directed Acyclic Graph (DAG) Conventions
- Extraction Methods (Incremental vs. Full)
- Retry Policies and Back-off Strategies
- Transaction Isolation and Write Safety

---

# Workflow Orchestration (Apache Airflow)

All data movement pipelines must be configured as **Directed Acyclic Graphs (DAGs)** inside our centralized orchestration framework.

- **Infrastructure**: Run Airflow schedulers inside the private EKS namespace (`data-platform`). Schedulers scale worker pods dynamically.
- **DAG Definition**: Code DAG definitions in python using declarative operators.

---

# DAG Naming & Code Conventions

To support easy management of hundreds of active pipelines:

- **Naming**: Prefix DAG identifiers with the target domain and pipeline model (e.g. `eduos_postgres_to_s3_daily`, `toolvines_invoice_sync_hourly`).
- **Idempotency**: Every DAG task must be **idempotent**. Running the same task multiple times with the same input date parameters must yield the identical database state.

### Reference DAG Configuration:

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.amazon.aws.transfers.sql_to_s3 import SqlToS3Operator

default_args = {
    "owner": "data_eng",
    "depends_on_past": False,
    "email_on_failure": True,
    "email": ["alerts-data@neelstack.com"],
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "eduos_student_data_sync_daily",
    default_args=default_args,
    description="Syncs Daily Student records from Postgres to S3",
    schedule_interval="0 2 * * *", # Daily at 2:00 AM
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    sync_task = SqlToS3Operator(
        task_id="extract_students",
        query="SELECT * FROM students WHERE updated_at >= '{{ data_interval_start }}'",
        s3_bucket="neelstack-data-lake",
        s3_key="raw/eduos/students/{{ ds }}/data.parquet",
        sql_conn_id="eduos_postgres",
        aws_conn_id="aws_default",
        file_format="parquet",
    )
```

---

# Extraction Standards (Incremental vs. Full)

Data extractions must minimize query loads on transactional source systems:

- **Incremental (Preferred)**: Fetch only records updated since the last pipeline run using execution interval variables (e.g. using `updated_at` filter timestamps).
- **Full Snapshot**: Only perform full database scans on small static tables (like lookup categories, country lists) or when initializing new data nodes.

---

# Retry Policies & Error Alerts

Networks and databases experience temporary failures.

- **Exponential Back-off**: Configure task retries with exponential back-off delays to prevent hammering databases during recovery phases.
- **PagerDuty Alerts**: Task failures must trigger Slack alerts on the first failure, and escalate to PagerDuty voice alerts if a critical pipeline run remains incomplete after 3 retries.

---

# Anti-Patterns

❌ **Hardcoded Connection Strings**: Declaring passwords or secret tokens directly inside Airflow Python script files. Manage connections securely in Airflow Connection variables mapped to AWS Secrets Manager.

❌ **Running Heavy Processing on Airflow Scheduler**: Running memory-intensive pandas dataframe calculations on the primary Airflow scheduler node, which slows down the entire cluster. Offload heavy processing to Spark nodes or database compute engines.

❌ **Omitting DAG Catchup Control**: Leaving `catchup=True` active when creating historical pipelines, which can trigger dozens of concurrent backfill runs and crash source databases.

---

# Production Checklist

- [ ] All DAG tasks are verified as idempotent.
- [ ] Credentials reside inside Secrets Manager rather than scripts.
- [ ] Task retries include exponential delay settings.
- [ ] Catchup is explicitly disabled (`catchup=False`) unless backfilling is required.
- [ ] Log metrics are routed to the OpenSearch index.

---

# Success Criteria

The ETL orchestration system is successful when:
- Pipelines recover automatically from transient database connection drops.
- Daily synchronization runs complete within defined SLA execution windows.
- Code definitions are reviewed, tested, and deployed automatically via CI/CD.

---

# Document Status

**Document:** NES-702 — ETL
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-703 — ELT**
