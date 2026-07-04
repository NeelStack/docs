---
document_id: NES-1309
title: Event-Driven Starter
subtitle: Enterprise Event-Driven Platform Starter Kit & Template Specification
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Starter Kit
parent_document: NES-1308 Microservice Starter
next_document: NES-1400 — C4 Context Diagrams.md
---

# NES-1309 — Event-Driven Starter

> **"Asynchronous communication requires pre-configured brokers. This starter kit provides a production-ready template built on Kafka, Avro schemas, and DLQ handlers."**

---

# Executive Summary

To help backend developer teams launch new event-driven streaming features, Kafka consumers, or event producers quickly while maintaining schema compatibility and consumer group stability, we provide the **Event-Driven Starter Kit**.

This starter kit contains a pre-configured template containing event schemas, Confluent schema registry hooks, partition key hash calculations, and dead-letter queue exception handlers.

This document establishes the repository structure, approved tech stack, quick start guide, and verification steps for the Event-Driven Starter template.

---

# Purpose

This standard defines:

- Event-Driven Starter Repository Directory Structure
- Pre-Configured Tech Stack
- Quick Start Guide for Developers
- Pre-Integrated Security and CI/CD Gates

---

# Repository Directory Structure

The Event-Driven Starter repository utilizes a clean event-driven directory structure:

```text
event-driven-starter/
├── schemas/               # Avro schema files definition (*.avsc)
├── src/
│   ├── producers/         # Kafka event producers logic
│   ├── consumers/         # Kafka event consumers and workers
│   └── config/            # Connection configurations (brokers, registry keys)
│
├── .github/
│   └── workflows/         # CI/CD pipelines
├── docker-compose.yml     # Local Kafka and schema registry setup
└── README.md
```

---

# Pre-Configured Tech Stack

The template includes our approved technology stack configured for production:

- **Language**: Python 3.13.
- **Library**: confluent-kafka (leveraging librdkafka for performance).
- **Schema Format**: Apache Avro.
- **Registries**: Confluent Schema Registry.
- **Testing**: pytest.

---

# Quick Start Guide

Developers can spin up the local development sandbox inside 2 minutes:

1. **Clone Template**: Create a new repository using the Event-Driven Starter template.
2. **Environment Variables**: Copy `.env.example` to `.env` in the root folder.
3. **Spin Up Docker**: Run the docker-compose command to launch Kafka and Schema Registry:
   ```bash
   docker-compose up -d
   ```
4. **Install Dependencies**: Run package installations:
   ```bash
   poetry install
   ```
5. **Run Producer**: Publish a test event to the local broker:
   ```bash
   poetry run python src/producers/test_producer.py
   ```
6. **Run Consumer**: Start the listener process:
   ```bash
   poetry run python src/consumers/test_consumer.py
   ```

---

# Pre-Integrated Security & CI/CD Gates

The template includes built-in security features to prevent vulnerability leakage:

- **Schema Check**: CI checks validate Avro changes against the Confluent Schema Registry before permitting merges.
- **DLQ Routing**: Consumers include error handling hooks that route poisoned messages to DLQ topics (`*.dlq`) after 3 failed retries.
- **Replication**: Pre-configured configurations target replication factors of 3 for all production topics.

---

# Anti-Patterns

❌ **Bypassing Schema Registry**: Sending raw JSON payloads to streaming topics without schema verification, leading to downstream consumer failures when database structures change.

❌ **Excluding Partition Keys**: Publishing events without keys, which causes round-robin distribution and leads to out-of-order processing issues.

❌ **Ignoring Consumer Retries**: Permitting consumer loops to crash repeatedly on single poisoned payloads, blocking the entire queue.

---

# Production Checklist

- [ ] Template repository clone completes cleanly.
- [ ] Local Kafka broker connection succeeds.
- [ ] Test events are published and consumed.
- [ ] Schema registry evolution checks pass.
- [ ] DLQ routes are verified.

---

# Success Criteria

The Event-Driven Starter template is successful when:
- Teams can spin up a new event consumer in less than 5 minutes.
- Published events conform to active Avro schemas.
- Consumer lag indicators remain low during high-throughput stress tests.

---

# Document Status

**Document:** NES-1309 — Event-Driven Starter
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1400 — C4 Context Diagrams.md**
