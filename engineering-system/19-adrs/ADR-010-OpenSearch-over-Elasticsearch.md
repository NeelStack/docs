# ADR-010 — OpenSearch over Elasticsearch

## Status
**Accepted** — In effect as of 2026-07-04

## Context
DhruvaOS requires full-text search capability for large catalog entities (students, staff, books) and centralized system log aggregation.

We evaluated:
1. **Elasticsearch**: The industry standard, but subject to restrictive licensing terms (SSPL) which limit open SaaS redistribution.
2. **OpenSearch**: Community-driven, fully open-source fork (Apache 2.0 license) maintained by AWS.

## Decision
We chose **OpenSearch** as our primary text indexer. Its open-source license aligns with our platform values, and it integrates seamlessly with AWS managed OpenSearch services when deploying to production.

## Consequences
- **License Compliance**: 100% compliant under Apache 2.0, avoiding downstream legal/licensing liability.
- **Observability**: Acts as our central log storage backend for Prometheus and Grafana traces.
