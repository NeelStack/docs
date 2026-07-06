# ADR-010 — Abstracted Search Provider over Direct OpenSearch Dependency

## Status
**Accepted** — In effect as of 2026-07-06 (Replaces legacy OpenSearch-only decision)

## Context
DhruvaOS requires full-text search capability for large entities (students, staff, books). While OpenSearch is a powerful text indexer, running an OpenSearch cluster in local dev or single VPS deployments introduces heavy memory overhead (minimum 1GB RAM) and operational complexity.

We evaluated:
1. **Direct OpenSearch Lock-in**: Hardcodes OpenSearch client drivers inside domain code modules, forcing a running cluster in all environments.
2. **Direct PostgreSQL FTS**: Relies purely on PG's built-in Full Text Search. Lightweight and free, but does not scale as well as standalone clusters under millions of documents.
3. **Abstract Search Provider**: Exposes search operations through `PlatformSDK.search`, allowing the underlying engine to be configured per environment (PostgreSQL FTS by default for dev/single VPS, and OpenSearch/Elasticsearch for production SaaS).

## Decision
We chose the **Abstract Search Provider** pattern. The SDK abstracts all search indexing and query methods, resolving to:
- **Local Dev / VPS**: PostgreSQL Full-Text Search (FTS) (0 cost, no additional JVM server required).
- **Production SaaS / Enterprise**: Standalone OpenSearch cluster for massive search volumes.

## Consequences
- **Memory Footprint**: Developers can run the entire stack on their laptops without spinning up resource-intensive search containers.
- **Independence**: Domain plugins remain isolated from the database indexing strategy.
