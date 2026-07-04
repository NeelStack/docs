---
document_id: NES-211
title: Event Streaming (Kafka) Standards
subtitle: Enterprise Event Streaming, Messaging & Kafka Architecture Standard for the NeelStack Platform
version: 1.0.0
status: Draft
classification: Internal
owner: Chief Solution Architect
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-210 Search Architecture
next_document: NES-212 Background Jobs & Workers
---

# NES-211 — Event Streaming (Kafka) Standards

> **"Events describe what happened. They never describe what should happen."**

---

# Executive Summary

Event Streaming is the backbone of NeelStack's distributed architecture.

Every product across the platform communicates using asynchronous events to achieve:

- Loose Coupling
- High Scalability
- Fault Tolerance
- Auditability
- AI Integration
- Real-Time Processing
- Workflow Automation

Apache Kafka is the official enterprise event streaming platform.

Every event-driven service within NeelStack follows this standard.

---

# Purpose

This document defines

- Event-Driven Architecture
- Kafka Standards
- Event Design
- Topic Strategy
- Producers
- Consumers
- Event Versioning
- Schema Governance
- Reliability
- Ordering
- Replay
- Dead Letter Queues
- Monitoring
- Security

---

# Vision

Build a real-time platform capable of processing

- Millions of Events per Minute

- Thousands of Services

- AI Pipelines

- Business Workflows

- Real-Time Analytics

with predictable latency and enterprise reliability.

---

# Event Philosophy

```
Business Action

↓

Business Event

↓

Kafka Topic

↓

Consumers

↓

Business Outcomes
```

Applications communicate through events.

Not direct dependencies.

---

# Core Principles

Every event system must be

✓ Event Driven

✓ Asynchronous

✓ Loosely Coupled

✓ Immutable

✓ Replayable

✓ Observable

✓ Secure

✓ Versioned

✓ Multi-Tenant

---

# Event Types

NeelStack supports

Business Events

Integration Events

Domain Events

Platform Events

Audit Events

AI Events

Notification Events

System Events

---

# Event Lifecycle

```
Business Action

↓

Transaction

↓

Outbox

↓

Kafka Producer

↓

Kafka Topic

↓

Consumers

↓

Business Processing

↓

Audit
```

The Outbox Pattern is mandatory.

---

# Event Architecture

```
                  FastAPI

                     │

             Business Transaction

                     │

               PostgreSQL

                     │

               Outbox Table

                     │

            Outbox Publisher

                     │

                  Kafka

      ┌──────────┼───────────┐

      │          │           │

 Notifications AI Workers Analytics

```

---

# Kafka Responsibilities

Kafka is responsible for

✓ Reliable Delivery

✓ Event Streaming

✓ Replay

✓ Ordering

✓ Backpressure

✓ Event Retention

✓ Consumer Scaling

Kafka is NOT responsible for

✗ Business Rules

✗ Authorization

✗ Persistent Business Data

✗ Querying

---

# Topic Design

Topics represent business domains.

Examples

```
student.events

course.events

finance.events

user.events

notification.events

audit.events

ai.events

workflow.events
```

Never create generic topics.

---

# Topic Naming

Convention

```
domain.event-type

Examples

student.events

user.events

payment.events

invoice.events
```

Environment prefixes handled by infrastructure.

---

# Event Naming

Past tense.

Examples

```
StudentCreated

StudentUpdated

StudentDeleted

InvoicePaid

UserInvited

OrderPlaced

PaymentCaptured
```

Never use commands.

Incorrect

```
CreateStudent

DeleteUser

SendEmail
```

---

# Event Structure

Every event follows

```json
{
  "eventId": "",
  "eventType": "",
  "eventVersion": "1",
  "tenantId": "",
  "aggregateId": "",
  "correlationId": "",
  "traceId": "",
  "timestamp": "",
  "source": "",
  "payload": {}
}
```

All events share the same envelope.

---

# Event Envelope

Mandatory fields

- Event ID
- Event Type
- Version
- Tenant ID
- Aggregate ID
- Correlation ID
- Trace ID
- Timestamp
- Producer
- Payload

---

# Event Versioning

Never break consumers.

Rules

```
Version 1

↓

Version 2

↓

Parallel Support

↓

Migration

↓

Deprecation
```

Backward compatibility is preferred.

---

# Event Schema

Schemas are version controlled.

Recommended

Apache Avro

Future support

Protocol Buffers

JSON Schema

Every event schema belongs to a registry.

---

# Schema Registry

Responsibilities

- Version Control
- Compatibility Checks
- Validation
- Discovery

Consumers should never infer schemas.

---

# Producer Standards

Producer responsibilities

- Validate Event
- Publish Once
- Handle Retries
- Add Metadata
- Use Outbox

Producers never publish inside business logic.

---

# Consumer Standards

Consumers should

- Be Idempotent
- Handle Retries
- Support Replay
- Log Processing
- Validate Schema
- Handle Failures

Consumers should never assume ordering across topics.

---

# Consumer Groups

Each bounded context owns its own consumer group.

Example

```
student-notifications

student-search

student-analytics

student-ai
```

Independent scaling.

---

# Ordering

Ordering guaranteed only

Within

```
Partition
```

Choose partition key carefully.

Recommended

```
tenantId

aggregateId
```

---

# Partitioning

Partition by

```
aggregateId
```

or

```
tenantId
```

Avoid random partitioning for ordered workflows.

---

# Idempotency

Consumers must tolerate duplicate delivery.

Example

```
Event ID

↓

Already Processed?

↓

Skip

↓

Process
```

Exactly-once business effects.

At-least-once delivery.

---

# Retry Strategy

Retry

Transient Failures

↓

Exponential Backoff

↓

Dead Letter Queue

Never retry validation failures indefinitely.

---

# Dead Letter Queue

Every topic has a DLQ.

Example

```
student.events

↓

student.events.dlq
```

Operations can inspect failed events.

---

# Replay

Kafka enables

Replay

↓

Recovery

↓

Rebuild Search

↓

Rebuild Analytics

↓

Rehydrate Read Models

Replay is a first-class capability.

---

# Event Retention

Recommended

Business Events

```
30 Days
```

Audit Events

```
365 Days
```

AI Events

```
90 Days
```

Retention depends on business requirements.

---

# Multi-Tenancy

Every event contains

```
tenantId
```

Consumers validate tenant context.

Cross-tenant processing prohibited.

---

# Event Security

Mandatory

TLS

SASL Authentication

ACLs

Encryption

Secrets Manager

Private Network

No anonymous producers.

---

# Event Observability

Every event includes

- Trace ID
- Correlation ID
- Event ID
- Tenant ID
- Producer
- Consumer
- Processing Time

Distributed tracing required.

---

# Monitoring

Track

- Topic Lag
- Consumer Lag
- Throughput
- Failed Events
- Retry Count
- DLQ Size
- Processing Latency
- Broker Health

---

# Performance Targets

Producer Latency

```
<10ms
```

Consumer Processing

```
<100ms
```

Event Availability

```
99.99%
```

---

# Event Categories

Business

```
StudentCreated
```

Integration

```
CRMUpdated
```

Audit

```
UserLoggedIn
```

AI

```
EmbeddingGenerated
```

Notification

```
EmailQueued
```

Platform

```
DeploymentCompleted
```

---

# AI Event Pipeline

```
DocumentUploaded

↓

Kafka

↓

Embedding Worker

↓

Vector Database

↓

Search Updated

↓

AI Ready
```

AI processing remains asynchronous.

---

# Outbox Pattern

```
Business Transaction

↓

Commit

↓

Outbox

↓

Publisher

↓

Kafka
```

Never publish events directly from controllers.

---

# Event Replay Use Cases

Replay supports

- Disaster Recovery
- Search Rebuild
- Analytics Rebuild
- AI Reindexing
- Data Migration
- Cache Rebuild

---

# Folder Structure

```
events/

├── producers/

├── consumers/

├── topics/

├── schemas/

├── outbox/

├── retry/

├── dlq/

├── monitoring/

├── replay/

└── tests/
```

---

# Anti-Patterns

Avoid

❌ Commands as Events

❌ Generic Topics

❌ Missing Event Version

❌ Missing Tenant ID

❌ Database Polling

❌ Shared Consumer Groups

❌ Business Logic in Kafka

❌ Infinite Retries

❌ Large Payloads (>1MB)

❌ Direct Service Chaining

❌ Event Mutation

---

# Production Checklist

Before production

- [ ] Topic created
- [ ] Schema registered
- [ ] Event version assigned
- [ ] Outbox implemented
- [ ] Producer tested
- [ ] Consumer idempotent
- [ ] Retry policy configured
- [ ] DLQ configured
- [ ] Monitoring enabled
- [ ] Security reviewed
- [ ] Replay tested

---

# Success Criteria

Event Streaming is successful when

- Services communicate asynchronously.
- Events remain immutable.
- Consumers remain independent.
- Event replay is always possible.
- Outbox guarantees reliable publishing.
- Multi-tenant isolation is preserved.
- AI workflows process events automatically.
- Operational visibility is complete.

---

# Future Evolution

Version 2.0 will include

- Complete Kafka Cluster Architecture
- Apache Avro Schema Registry Standards
- Confluent Platform Deployment Guide
- Kafka Connect Standards
- Kafka Streams Architecture
- Event Sourcing Decision Framework
- CQRS Integration Guide
- Saga Orchestration Patterns
- Exactly-Once Processing Reference
- Kubernetes Kafka Deployment
- Multi-Region Kafka Replication
- Event Catalog Platform
- OpenTelemetry Kafka Integration
- C4 Event Architecture Diagrams
- Production Kafka Reference Repository

---

# Kafka Standards Checklist

- [x] Event Architecture Defined
- [x] Topic Strategy Established
- [x] Event Standards Defined
- [x] Schema Governance Added
- [x] Outbox Pattern Defined
- [x] Producer & Consumer Standards Included
- [x] Retry & DLQ Strategy Added
- [x] Multi-Tenant Support Defined
- [x] Security Standards Added
- [x] Monitoring & Observability Included
- [x] Production Checklist Added
- [x] Success Criteria Defined

---

# Document Status

**Document:** NES-211 — Event Streaming (Kafka) Standards

**Version:** 1.0.0

**Status:** Ready for Architecture Review

**Next Document:** **NES-212 — Background Jobs & Workers**

---

# Revision Queue for Version 2.0 (Enterprise Edition)

Future enhancements will include:

- Enterprise Kafka Reference Architecture
- C4 Context, Container & Component Diagrams
- UML Sequence Diagrams for Event Flows
- Apache Avro Schema Registry Reference
- Kafka Connect & Debezium CDC Standards
- CQRS & Event Sourcing Architecture
- Saga Orchestration & Choreography Patterns
- Event Catalog & Discovery Platform
- Event Governance Dashboard
- Multi-Region Active-Active Kafka Architecture
- AI Event Processing Blueprint
- Kafka Performance Benchmark Suite
- Architecture Fitness Rules for Event-Driven Systems
- Production FastAPI + Kafka Starter Repository

These enhancements will establish the definitive enterprise event streaming standard for the NeelStack platform, enabling reliable, scalable, observable, and AI-ready asynchronous communication across every product, microservice, and distributed workflow.