---
document_id: TECH-007
title: Message Queue Standard
subtitle: RabbitMQ for task queues, Kafka for event streaming — choose based on use case
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Backend Platform Team
review_cycle: Every 6 Months
document_type: Technology Standard
parent_document: TECH-006 Redis
next_document: TECH-008 OpenSearch
---

# TECH-007 — Message Queue Standard

---

## Approved Technologies

| Technology | Use Case |
|---|---|
| **RabbitMQ** | Task queues, background jobs, service-to-service async calls |
| **Kafka** | Event streaming, audit logs, high-throughput event pipelines |

## Decision Guide

**Use RabbitMQ when:**
- Tasks need guaranteed delivery and acknowledgement
- Processing order matters within a queue
- Consumer failures need automatic retry
- Using Celery for background jobs

**Use Kafka when:**
- Event volume exceeds 10,000 events/second
- Events need replay capability (event sourcing)
- Multiple independent consumer groups need the same events
- Building event-driven audit trails

## Topic / Queue Naming

```
# Kafka topic: {domain}.{entity}.{event}
enrollment.student.enrolled
billing.invoice.generated
auth.user.created

# RabbitMQ queue: {service}.{task}
email-service.send-welcome
notification-service.push-notification
```

## Dead Letter Queues

Every queue MUST have a configured Dead Letter Queue (DLQ):
- After 3 retry attempts, message moves to DLQ
- DLQ monitored with alerting
- DLQ messages reviewed within 24 hours

## Related Standards

- NES-211 — Event Streaming (Kafka) Standards
- NES-212 — Background Jobs & Workers
- TECH-001 — Technology Stack

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-07-04 | Initial publication |
