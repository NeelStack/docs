---
document_id: NES-517
title: Logging
subtitle: Enterprise Platform Logging, Log Shipping & OpenSearch Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-516 Monitoring
next_document: NES-518 Incident Response
---

# NES-517 — Logging

> **"Unstructured logs are write-only data. We write structured JSON logs, ship them automatically, and query them via OpenSearch."**

---

# Executive Summary

When debugging system issues or auditing transactions, raw unstructured console logs are difficult to search at scale.

We mandate that all application components write **structured JSON logs** to standard output (`stdout`).

This standard defines the log formats, logging levels, shipping architectures (Vector/FluentBit), and log index retention rules using **OpenSearch**.

---

# Purpose

This standard defines:

- Structured Logging Format (JSON Schema)
- Log Levels (Debug, Info, Warn, Error, Fatal)
- Log Shipping Pipeline (FluentBit to OpenSearch)
- PII and Sensitive Data Scrubbing Policies
- Retention and Archival Budgets

---

# Structured JSON Log Format

All services must output log streams in JSON format to `stdout`.

- **No Writing to Local Files**: Containers are ephemeral. Writing logs to local files causes disk exhaustion and data loss.
- **Trace Correlation**: Every log statement must include a `traceId` and `correlationId` to track requests across microservices.

### Standard JSON Schema:

```json
{
  "timestamp": "2026-07-04T12:00:00.000Z",
  "level": "INFO",
  "service": "portal-api",
  "version": "1.2.0",
  "traceId": "t-83a74e-9876",
  "correlationId": "c-1234-5678",
  "userId": "usr_9999",
  "message": "Document successfully compiled",
  "context": {
    "documentId": "doc_456",
    "documentType": "certificate"
  }
}
```

---

# Log Levels

Use log levels consistently to prevent log noise:

| Level | Usage | Performance Impact |
|---|---|---|
| **DEBUG** | Detailed diagnostic information. Disabled in production. | High overhead, disable by default. |
| **INFO** | Core system updates (startups, success transactions). | Low overhead. |
| **WARNING** | Unexpected issues that don't block requests (e.g. slow DB connection). | Minimal. |
| **ERROR** | Operation failures that block the active request. | Requires attention, logs full stack trace. |
| **FATAL** | System crashes that force the container to reboot. | Immediate alert triggers. |

---

# Log Shipping Pipeline

We decouple log generation from shipping to protect application performance.

```text
  App writes to stdout (JSON)
              │
              ▼
   FluentBit Daemon (scrapes)
              │
              ▼
  Vector Aggregator (scrubs)
              │
              ▼
    OpenSearch Index
```

- **FluentBit**: Runs as a daemonset on Kubernetes hosts to gather container logs from filesystems.
- **Vector**: Performs filtering, parses JSON structures, and scrubs data.
- **OpenSearch**: Stores indexes for search and dashboard visualization.

---

# PII & Data Scrubbing Policy

Never store passwords, PINs, bank accounts, or customer PII inside search indexes.

- **Client Filters**: Sanitise all user inputs before logging parameters.
- **Gateway Filters**: Configure the Vector aggregator with regex filters to automatically mask values matching patterns for credit cards, emails, or JWTs:

```yaml
# Vector configuration snippet
transforms:
  scrub_secrets:
    type: "remap"
    inputs: ["parse_logs"]
    source: |
      .message = replace(.message, r'bearer [A-Za-z0-9\-\._~\+\/]+=*', "bearer [REDACTED]")
```

---

# Retention and Archiving

To control database storage costs, we enforce index retention schedules:

- **Staging / Dev Logs**: Retained in OpenSearch for **7 days**, then deleted.
- **Production Performance Logs**: Retained for **30 days**.
- **Audit Logs (Security access)**: Retained for **365 days** (moved to secure Glacier S3 buckets after 30 days).

---

# Anti-Patterns

❌ **Plaintext Console Statements**: Writing logs using raw strings:
   ```python
   logger.info(f"User {user_id} logged in") # WRONG: Hard to query
   ```
   Always use structured values:
   ```python
   logger.info("User logged in", extra={"userId": user_id}) # RIGHT
   ```

❌ **Logging Large Payloads**: Printing complete API response payloads or large HTML pages.

❌ **Over-Logging inside Loops**: Logging debug rows inside fast rendering loops, which exhausts disk limits and degrades performance.

---

# Production Checklist

- [ ] All APIs are configured to write structured JSON to standard output.
- [ ] Debug logging is disabled in production settings.
- [ ] Correlation IDs propagate across all internal HTTP headers.
- [ ] Vector scrubbing regex patterns are verified.
- [ ] Index lifecycle management (ILM) policies are active in OpenSearch.

---

# Success Criteria

The Logging pipeline is successful when:
- Developers can trace a complete request path across 5 microservices in less than 10 seconds using a single `traceId`.
- Automated checks block deployment of code containing cleartext passwords in logs.
- Index storage footprint remains within monthly budget targets.

---

# Document Status

**Document:** NES-517 — Logging
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-518 — Incident Response**
