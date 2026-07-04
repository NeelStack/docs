---
document_id: NES-1209
title: Event Platform
subtitle: Enterprise Event-Driven Streaming Platform Reference Architecture Blueprint
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Reference Architecture
parent_document: NES-1208 Analytics Platform
next_document: NES-1210 Enterprise Blueprint
---

# NES-1209 — Event Platform

> **"Asynchronous communication requires schema contracts. This reference blueprint details our event streaming topics, Kafka brokers, and schema registries."**

---

# Executive Summary

To operate a reliable Event-Driven Architecture (EDA) that handles asynchronous message exchanges, transactional events, clickstream logs, and notifications, we must enforce a scalable streaming model.

This document establishes the official **NeelStack Event-Driven Streaming Platform Reference Architecture** blueprint.

It defines our event brokers (Apache Kafka), schema registries (Avro/Confluent), consumer group behaviors, and retry/dead-letter queue configurations.

---

# Purpose

This standard defines:

- Unified Event Streaming Platform Architecture Map
- Event Schema Contracts and Registries (Avro)
- Kafka Topic Partitioning and Key Strategies
- Resilient Consumer and Dead-Letter Queue (DLQ) Rules

---

# Event Platform Reference Architecture Map

The Event Platform separates producers, streaming brokers, schema registries, and consumers:

```text
               Event Producers (Application APIs, CDC Streams)
                               │
                               ▼
        Schema Registry (Validates payload structure against Avro specs)
                               │
                               ▼
        Event Streaming Broker (Apache Kafka cluster, KRaft mode)
         ├── Ingestion Topics (Partitioned by entity keys)
         └── Dead-Letter Queue (DLQ) Topics (Failed payloads)
                               │
                               ▼
               Event Consumers (Service workers pods in EKS)
```

---

# Event Schema Contracts & Registries

- **Avro Schema Standard**: Define event structures using **Apache Avro** specifications to support schema evolution checks.
- **Schema Registry**: Integrate all producers and consumers with a central Schema Registry (e.g. Confluent Registry). The registry must reject events that violate active schemas.

---

# Kafka Topic Partitioning & Key Strategies

- **Partition Key**: Always publish events using specific entity identifiers (e.g. `student_id`, `invoice_id`) as the partition key. This guarantees that all events for a specific entity are processed sequentially.
- **Replication Factor**: Set the topic replication factor to **3** in production to ensure high availability across different cloud availability zones.

---

# Dead-Letter Queues (DLQs) & Consumer Resiliency

To prevent a single poisoned message payload from blocking processing queues:

- **DLQ Routing**: If a consumer fails to process an event after 3 retries, write the payload to a dedicated Dead-Letter Queue topic (`[topic-name].dlq`) and log the exception.
- **Alert Rules**: Trigger immediate operations alerts if the DLQ topic receives messages, allowing teams to review payloads.

---

# Anti-Patterns

❌ **Publishing Schema-less JSON**: Sending raw JSON payloads to streaming topics without schema verification, leading to downstream consumer failures when database structures change.

❌ **Excluding Partition Keys**: Publishing events without keys, which causes round-robin distribution and leads to out-of-order processing issues.

❌ **Ignoring Consumer Retries**: Permitting consumer loops to crash repeatedly on single poisoned payloads, blocking the entire queue.

---

# Production Checklist

- [ ] Kafka cluster runs in multi-AZ KRaft mode.
- [ ] Schema Registry validates all published events.
- [ ] Replication factor is set to 3 for all topics.
- [ ] Dead-Letter Queue (DLQ) routing is active.
- [ ] Consumer metrics (lag, CPU) are monitored in Grafana.

---

# Success Criteria

The Event Platform Reference Architecture is successful when:
- Microservices communicate asynchronously with zero message loss.
- Consumers process high-throughput events with latency under 100ms.
- Poisoned payloads are isolated dynamically without blocking message queues.

---

# Document Status

**Document:** NES-1209 — Event Platform
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1210 — Enterprise Blueprint**
