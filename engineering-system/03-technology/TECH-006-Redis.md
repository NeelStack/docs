---
document_id: TECH-006
title: Redis Standard
subtitle: Redis is the approved caching, session, and pub/sub platform across all NeelStack services
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Backend Platform Team
review_cycle: Every 6 Months
document_type: Technology Standard
parent_document: TECH-005 PostgreSQL
next_document: TECH-007 RabbitMQ and Kafka
---

# TECH-006 — Redis Standard

---

## Approved Version

**Redis 7+** — Cluster mode in production, standalone in development.

## Approved Use Cases

| Use Case | Key Pattern | TTL |
|---|---|---|
| API response cache | `cache:{tenant}:{resource}:{id}` | 5–60 min |
| Session storage | `session:{session_id}` | 15 min |
| Rate limiting | `ratelimit:{ip}:{endpoint}` | 1 min |
| Distributed lock | `lock:{resource_id}` | 30 sec |
| Job queue (Celery) | `celery:{queue_name}` | — |
| Pub/Sub channels | `events:{domain}:{event}` | — |

## Key Naming Convention

All Redis keys MUST follow the pattern: `{service}:{type}:{identifier}`

```
# ✅ Correct
enrollment:cache:student:uuid-123
auth:session:sess-abc456
billing:lock:invoice:uuid-789

# ❌ Wrong
user123
temp_data
cache
```

## Required TTL Policy

**Every key MUST have an explicit TTL.** No key may be stored without an expiry. Unbounded keys cause memory exhaustion.

```python
# ✅ Correct
redis.setex(key, 300, value)  # 5-minute TTL

# ❌ Wrong
redis.set(key, value)  # No TTL = memory leak
```

## Related Standards

- NES-208 — Redis Standards
- TECH-001 — Technology Stack

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-07-04 | Initial publication |
