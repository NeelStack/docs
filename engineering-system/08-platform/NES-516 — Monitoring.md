---
document_id: NES-516
title: Monitoring
subtitle: Enterprise Platform Monitoring, Prometheus, Grafana & Metrics Standard
version: 1.0.0
status: Draft
classification: Internal
owner: SRE & Operations Board
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-515 Infrastructure Security
next_document: NES-517 Logging
---

# NES-516 — Monitoring

> **"If it is not measured, it is not monitored. We track system metrics, define dashboards, and measure performance using Prometheus and Grafana."**

---

# Executive Summary

Operations teams must monitor application health, compute performance, and resource constraints to identify outages before they affect users.

Relying on reactive customer bug reports to identify crashes indicates operational failure.

We standardize on **Prometheus** for metrics collection and **Grafana** for visualization across all NeelStack environments.

This standard defines the metrics framework, the four golden signals, dashboard conventions, and telemetry collections.

---

# Purpose

This standard defines:

- Metrics Collector Tooling (Prometheus)
- Visualization Standard (Grafana)
- The Four Golden Signals
- Core Dashboard Configurations
- Service Level Indicator (SLI) and Objective (SLO) Metrics

---

# Monitoring Stack Architecture

Our telemetry pipeline uses a pull-based metrics collection pattern:

```text
 ┌─────────────────┐        ┌─────────────────┐
 │   FastAPI App   │ ◄──────│ Prometheus Pull │ ◄─── Grafana
 ├─────────────────┤        ├─────────────────┤
 │ /metrics (JSON) │        │ TSDB Database   │
 └─────────────────┘        └─────────────────┘
```

- **Metrics Exporters**: Every service must expose a `/metrics` HTTP endpoint returning Prometheus formatted text.
- **Node Exporter**: Collects system metrics (CPU, Memory, Disk, Network) from physical Kubernetes hosts.

---

# The Four Golden Signals

Every service dashboard must display the **Four Golden Signals** of site reliability engineering:

| Signal | Metric Description | Prometheus Query Example |
|---|---|---|
| **Latency** | Time taken to service a request. | `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))` |
| **Traffic** | A measure of demand on the system (e.g. requests/sec). | `sum(rate(http_requests_total[5m]))` |
| **Errors** | Rate of requests that fail (e.g. HTTP 5xx responses). | `sum(rate(http_requests_total{status=~"5.."}[5m]))` |
| **Saturation** | System utilization limits (e.g. memory fraction). | `container_memory_working_set_bytes / container_spec_memory_limit_bytes` |

---

# Grafana Dashboard Standards

Grafana dashboards must follow a uniform, structured format to support quick triage during incidents:

- **Folder isolation**: Dashboards must be grouped into folders matching environments (e.g. `Production-APIs`, `Infrastructure-Nodes`).
- **Core Layout**: Place the critical service health variables (SLAs, Uptime, Error Rates) at the top of the dashboard. Place CPU, memory, and database connection pools below them.
- **Variables**: Make dashboards dynamic using dropdown variables for namespaces, pod IDs, and instances.

---

# Service Level Objectives (SLOs)

Metric definitions must map directly to business-defined objectives:

- **SLI (Service Level Indicator)**: A quantitative measure of service performance (e.g. "Ratio of HTTP responses returning status < 500").
- **SLO (Service Level Objective)**: Target reliability percentage (e.g. "99.9% of HTTP requests return success over a rolling 30-day window").
- **Error Budget**: The allowed downtime fraction (e.g., 0.1% for a 99.9% SLO). Operations teams track the remaining error budget to determine if releases should be halted.

---

# Anti-Patterns

❌ **High-Cardinality Metrics**: Injecting highly unique parameters (like user IDs, email addresses, or transaction values) as labels in Prometheus metrics, which bloats the time-series database and crashes the monitoring system.

❌ **Dashboard Clutter**: Designing dashboards containing dozens of charts, gauges, and graphs on a single view, which makes identifying failures difficult during outages.

❌ **Ignoring Alert Silence Policies**: Leaving broken or flapping alerts active indefinitely, which leads to alert fatigue and causes teams to ignore real critical notifications.

---

# Production Checklist

- [ ] Every production API exposes a `/metrics` scrape endpoint.
- [ ] Prometheus is configured to scrape applications at 15-second intervals.
- [ ] The Four Golden Signals are configured at the top of Grafana dashboards.
- [ ] Dashboards are declared as code (JSON configuration files stored in Git).
- [ ] Target SLIs and SLOs are documented and active.

---

# Success Criteria

The Monitoring platform is successful when:
- Dashboard graphs load and update in less than 2.0 seconds during user traffic spikes.
- Service degradations are visible on dashboards before user connections fail.
- Memory leak patterns are detected and flagged automatically via saturation trends.

---

# Document Status

**Document:** NES-516 — Monitoring
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-517 — Logging**
