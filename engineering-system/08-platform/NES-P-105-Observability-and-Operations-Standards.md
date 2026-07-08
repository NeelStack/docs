---
document_id: NES-P-105
title: Observability & Operations Standards
version: 1.0.0
status: Approved
owner: Platform Operations Team
---

# NES-P-105 — Observability & Operations Standards

> **"If it isn't monitored, it isn't running. Every tenant query, job execution, and database connection must emit traces."**

---

# 1. Purpose

This document outlines the **observability specifications, logging criteria, alert thresholds, and operational rules** governing the DhruvaOS platform. It aligns with our chosen open telemetry stack: Prometheus, Grafana, Loki, and custom audit trails.

---

# 2. Observability Stack Components

DhruvaOS relies on a lightweight, open-source telemetry engine to maintain low local footprint while scaling to multi-node clusters:

```text
                  Telemetry Pipeline
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
    Prometheus          Loki            Audit SDK
(Metrics Catalog)  (App Logging)   (Mutation Tracing)
         │                │                │
         └────────────────┼────────────────┘
                          ▼
                       Grafana
                 (Unified Dashboards)
```

1. **Prometheus**: Aggregates time-series performance metrics (CPU, RAM, API latencies, queue depth).
2. **Loki**: Collects stdout logs from application containers using trace correlation IDs.
3. **Audit SDK**: Captures sensitive database mutations for security audits.
4. **Grafana**: Serves as the single pane of glass dashboard for operators.

---

# 3. Logging Standard Layout

All application services must output structured JSON logs to standard output. 

### JSON Log Structure:
```json
{
  "timestamp": "2026-07-06T17:44:00.123Z",
  "level": "INFO",
  "service": "core",
  "trace_id": "8f9a2b3c4d5e6f7a",
  "tenant_id": "school_abc",
  "message": "Processed student attendance records",
  "context": {
    "module": "attendance",
    "records_count": 45,
    "latency_ms": 12.4
  }
}
```

- **Trace IDs**: Every request must compile a unique trace ID using the HTTP Gateway interceptor and propagate it through NATS events and background jobs.
- **Log Levels**:
  - `DEBUG`: Verbose operational traces (disabled in production).
  - `INFO`: Normal application events (e.g., startup, cron triggers).
  - `WARNING`: Recoverable errors (e.g., failed retries, slow queries).
  - `ERROR`: System failures requiring developer attention.

---

# 4. Standard Operational Metrics

Every service exposed to public routes must export a `/metrics` scrape endpoint. Key performance indicators (KPIs) include:

### 4.1 Request Metrics (RED Method)
- **Rate**: Number of HTTP requests per second (`http_requests_total`).
- **Errors**: Count of non-2xx responses (`http_requests_errors_total`).
- **Duration**: Latency percentiles (p50, p95, p99) of request executions.

### 4.2 Queue Metrics (Arq)
- **Queue Depth**: Number of pending background tasks (`arq_queue_depth`).
- **Processing Time**: Job execution latencies (`arq_job_execution_seconds`).
- **Failures**: Count of failed background worker jobs (`arq_job_failures_total`).

### 4.3 Database Connection Metrics
- **Active Connections**: Size of PostgreSQL connection pool (`db_pool_active_connections`).
- **Acquisition Time**: Latency to obtain database sockets.

---

# 5. Alert Guidelines

Alert notifications are classified into three severity levels and dispatched to Slack, PagerDuty, or SMS channels:

| Metric Trigger | Threshold Condition | Severity Level | Target SLA |
| --- | --- | --- | --- |
| **API Error Rate** | > 5% of requests failing (5xx) over 5m | critical | P1 (15m response) |
| **Queue Backlog** | > 1000 tasks pending in Arq | warning | P2 (2h response) |
| **Database Disk** | > 85% disk storage utilization | warning | P2 (2h response) |
| **Core Service Down**| Main instance unreachable | critical | P1 (15m response) |
| **Inference Budget** | Tenant cost limit exceeded | info | Automated email |

---

# 6. Tenant Observability Isolation

To guarantee data privacy under multi-tenant deployments, operators must apply filtering variables in Grafana dashboards:
- All log queries in Loki **MUST** include `{tenant_id="<id>"}` filters.
- Direct visualization of raw database contents across tenants is restricted to database administrators (DBAs) with active auditing sessions.
