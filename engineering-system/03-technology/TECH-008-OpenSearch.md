---
document_id: TECH-008
title: OpenSearch Standard
subtitle: OpenSearch is the approved full-text search and log analytics platform
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Data Platform Team
review_cycle: Every 6 Months
document_type: Technology Standard
parent_document: TECH-007 RabbitMQ
next_document: TECH-009 AWS
---

# TECH-008 — OpenSearch Standard

---

## Approved Version

**OpenSearch 2.x** — self-hosted on Kubernetes or AWS OpenSearch Managed Service.

## Use Cases

| Use Case | Index Pattern |
|---|---|
| Product/Course search | `{tenant}-courses-{env}` |
| User search | `{tenant}-users-{env}` |
| Application logs | `logs-{service}-{date}` |
| Audit events | `audit-{tenant}-{date}` |
| AI document search | `knowledge-{tenant}-{env}` |

## Index Lifecycle Management (ILM)

All log indices must have ILM policies:
- **Hot**: 0–7 days (SSD storage)
- **Warm**: 7–30 days (HDD storage)
- **Cold**: 30–90 days (object storage)
- **Delete**: After 90 days (or per data retention policy)

## Required Index Mappings

```json
{
  "mappings": {
    "properties": {
      "tenant_id": { "type": "keyword" },
      "created_at": { "type": "date" },
      "title": {
        "type": "text",
        "analyzer": "standard",
        "fields": { "keyword": { "type": "keyword" } }
      }
    }
  }
}
```

## Security

- Tenant isolation via index-per-tenant or document-level security
- No cross-tenant queries permitted
- Fine-grained access control (FGAC) enabled in production

## Related Standards

- NES-210 — Search Architecture
- TECH-001 — Technology Stack

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-07-04 | Initial publication |
