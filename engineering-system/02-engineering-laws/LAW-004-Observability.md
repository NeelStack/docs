---
document_id: LAW-004
title: Observability
subtitle: Every production service must be observable — no service ships to production without metrics, logs, and traces
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Chief Architect
review_cycle: Annual
document_type: Engineering Law
parent_document: LAW-003 API Versioning
next_document: LAW-005 Documentation
---

# LAW-004 — Observability

> **"If you cannot measure it, you cannot manage it. If you cannot observe it, you cannot operate it."**

---

## Law Statement

**Every production service MUST emit the three pillars of observability: structured logs, metrics, and distributed traces. No service may be deployed to production without all three pillars configured, tested, and connected to the observability platform.**

---

## The Three Pillars

### 1. Structured Logs
All log output must be:
- **JSON-formatted** (machine-parseable)
- Include `request_id`, `tenant_id`, `user_id` (where applicable)
- Include `service_name`, `environment`, `timestamp`
- Follow severity levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

```json
{
  "timestamp": "2026-07-04T10:00:00Z",
  "level": "ERROR",
  "service": "enrollment-service",
  "request_id": "req-abc123",
  "tenant_id": "tenant-xyz",
  "message": "Enrollment failed: course capacity exceeded",
  "course_id": "course-456",
  "error_code": "ENROLLMENT_CAPACITY_EXCEEDED"
}
```

### 2. Metrics
All services must expose Prometheus-compatible metrics:
- **RED metrics**: Request Rate, Error Rate, Duration
- **USE metrics**: Utilization, Saturation, Errors (for infrastructure)
- Business metrics: domain-specific KPIs (e.g. enrollments per minute)

### 3. Distributed Traces
All inter-service calls must propagate trace context using **OpenTelemetry** W3C TraceContext headers:
- `traceparent`: Trace ID + Span ID
- `tracestate`: Vendor-specific metadata

---

## Pre-Production Checklist

Before any service is promoted to production:

- [ ] Structured JSON logging configured
- [ ] Log correlation IDs (`request_id`, `trace_id`) injected in all log lines
- [ ] Prometheus `/metrics` endpoint exposed and scraped
- [ ] RED metrics dashboards created in Grafana
- [ ] OpenTelemetry SDK integrated and traces visible in Jaeger/Tempo
- [ ] Alert rules defined for error rate > 1%, p99 latency > SLA threshold
- [ ] Runbook linked from each alert

---

## Anti-Patterns

❌ `print()` statements instead of structured logging.  
❌ Logging only errors — missing INFO-level business events.  
❌ Logging PII (names, emails, phone numbers) in plain text.  
❌ No trace propagation — orphaned spans that cannot be correlated.  
❌ Deploying with "we'll add monitoring later."

---

## Related Standards

- NES-516 — Platform Monitoring
- NES-517 — Platform Logging
- NES-224 — AI Observability & Telemetry
- NES-313 — Frontend Observability
- LAW-008 — Performance

---

## Version History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2026-07-04 | NeelStack Engineering | Initial publication |
