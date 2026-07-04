---
document_id: NES-107
title: Event-Driven Architecture
subtitle: Enterprise Event-Driven Architecture Standard for the NeelStack Platform
version: 1.0.0
status: Draft
classification: Internal
owner: Chief Solution Architect
review_cycle: Every 6 Months
document_type: Architecture Standard
parent_document: NES-106 Microservice Guidelines
next_document: NES-108 Service Communication
---

# NES-107 — Event-Driven Architecture (EDA)

> **"Events represent facts. Facts cannot be undone. Systems should react—not depend."**

---

# Executive Summary

NeelStack adopts **Event-Driven Architecture (EDA)** as the primary asynchronous communication model between modules, platform services, AI systems, and future microservices.

Instead of tightly coupling services through synchronous API calls, systems communicate using immutable business events.

EDA provides:

- Loose coupling
- Independent scalability
- High resilience
- Better observability
- Easier integrations
- Event replay
- AI workflow automation
- Auditability

Synchronous APIs remain important for request-response operations.

Business workflows spanning multiple domains should prefer events.

---

# Purpose

This document defines:

- Event Architecture
- Event Lifecycle
- Event Standards
- Event Contracts
- Event Naming
- Event Versioning
- Event Routing
- Message Broker Standards
- Reliability Patterns
- Governance

All asynchronous communication within NeelStack must follow this standard.

---

# Core Philosophy

```
Business Action

↓

Business Event

↓

Message Broker

↓

Interested Consumers

↓

Independent Processing
```

Systems publish facts.

Other systems decide how to react.

---

# Why Event-Driven?

Without EDA

```
Student Service

↓

Notification Service

↓

Analytics

↓

Audit

↓

Search

↓

Email
```

Every dependency increases coupling.

---

With EDA

```
Student Service

↓

StudentRegistered Event

↓

Kafka

↓

Notification

Analytics

Audit

Search

Email

AI
```

One producer.

Many independent consumers.

---

# Event Principles

---

## Principle 1

### Events Represent Facts

Examples

```
StudentRegistered

InvoicePaid

CoursePublished

OrderCompleted

PasswordChanged
```

Events describe something that has already happened.

---

## Principle 2

### Events Are Immutable

Never modify published events.

Corrections generate new events.

Example

```
InvoiceCreated

↓

InvoiceCancelled
```

Not

```
Update InvoiceCreated
```

---

## Principle 3

### Business Language

Event names use business terminology.

Good

```
EnrollmentCompleted
```

Bad

```
InsertStudentRecord
```

---

## Principle 4

### Publish Once

A producer publishes exactly one event describing one business fact.

Avoid combining multiple business concepts into one event.

---

## Principle 5

### Consumers Are Independent

Publishers never know who consumes events.

Consumers may be added without modifying publishers.

---

# Event Architecture

```
          FastAPI

             │

      Business Module

             │

      Domain Event

             │

      Event Publisher

             │

      Kafka / RabbitMQ / NATS

             │

 ┌──────────┼──────────┬───────────┐

 Notification

 Analytics

 Audit

 AI

 Search

 Workflow
```

The producer never calls consumers directly.

---

# Event Lifecycle

```
Business Action

↓

Business Rule

↓

Domain Event

↓

Event Publisher

↓

Message Broker

↓

Consumer

↓

Business Processing

↓

New Events
```

Each stage is observable.

---

# Event Types

---

## Domain Events

Represent business facts.

Examples

```
StudentRegistered

CourseCreated

InvoicePaid
```

---

## Integration Events

Expose information to other systems.

Examples

```
CRMContactCreated

PaymentSucceeded

EmailDelivered
```

---

## System Events

Represent infrastructure changes.

Examples

```
DeploymentCompleted

CacheInvalidated

NodeStarted
```

---

## AI Events

Represent AI activities.

Examples

```
PromptExecuted

ModelSelected

InferenceCompleted

EmbeddingCreated
```

---

# Event Naming Convention

Standard

```
<Entity><PastTenseVerb>
```

Examples

```
StudentRegistered

UserActivated

InvoiceGenerated

CourseArchived

TeacherAssigned
```

Avoid technical names.

---

# Event Structure

Every event must contain:

```json
{
  "eventId": "uuid",
  "eventType": "StudentRegistered",
  "eventVersion": "1.0",
  "occurredAt": "ISO8601",
  "producer": "student-service",
  "tenantId": "...",
  "correlationId": "...",
  "causationId": "...",
  "payload": {}
}
```

Every event follows the same envelope.

---

# Event Metadata

Mandatory fields:

- Event ID
- Event Type
- Version
- Timestamp
- Producer
- Correlation ID
- Causation ID
- Tenant ID
- Trace ID

Optional:

- User ID
- Region
- Source IP

---

# Event Versioning

Events follow Semantic Versioning.

```
Major

Minor

Patch
```

Breaking payload changes require a major version.

Consumers should remain backward compatible whenever practical.

---

# Message Broker

Approved brokers:

Primary

- Apache Kafka

Secondary

- NATS JetStream

Specialized

- RabbitMQ (workflow-specific use cases)

Broker selection requires an ADR.

---

# Topics

Naming standard

```
domain.entity.event

Examples

student.registered

student.updated

billing.invoice_paid

identity.user_created

workflow.task_completed
```

Names should remain stable.

---

# Event Routing

```
Topic

↓

Consumer Group

↓

Consumer

↓

Business Logic
```

Routing logic belongs in the broker—not in producers.

---

# Delivery Guarantees

Supported models

At Least Once

Preferred

Exactly Once

Where business-critical and supported

At Most Once

Avoid for important business events

Consumers must be idempotent.

---

# Idempotency

Consumers must safely process duplicate events.

Example

```
Event Received

↓

Already Processed?

↓

Yes → Ignore

↓

No → Process
```

Duplicate processing must not create inconsistent state.

---

# Ordering

Ordering guarantees exist only within a partition.

Applications should avoid relying on global ordering.

Business workflows should tolerate out-of-order delivery when possible.

---

# Retry Strategy

```
Failure

↓

Retry

↓

Retry

↓

Retry

↓

Dead Letter Queue
```

Retries should use exponential backoff.

---

# Dead Letter Queue (DLQ)

Every critical topic must have a DLQ.

DLQ messages require:

- Monitoring
- Investigation
- Replay capability

---

# Event Replay

Replay enables:

- Data recovery
- Analytics rebuilding
- AI model retraining
- Search re-indexing
- Debugging

Events should remain replayable.

---

# Saga Pattern

Long-running business workflows use Sagas.

Example

```
Student Registered

↓

Fee Generated

↓

Welcome Email

↓

Analytics Updated

↓

Search Indexed
```

Failures trigger compensating actions.

---

# Event Choreography

Preferred for loosely coupled workflows.

```
Service A

↓

Event

↓

Service B

↓

Event

↓

Service C
```

No central coordinator.

---

# Event Orchestration

Used when centralized workflow control is required.

```
Workflow Engine

↓

Step 1

↓

Step 2

↓

Step 3
```

Examples:

- Admissions
- Billing
- Complex approvals

---

# Event Schema Registry

Every production event must be registered.

Registry includes:

- Event Name
- Version
- Payload Schema
- Producer
- Consumers
- Documentation
- Examples

---

# Security

Events must never expose:

- Passwords
- Secrets
- Tokens
- Private Keys
- Sensitive personal information unless encrypted

Sensitive payloads require encryption.

---

# Observability

Track:

- Published Events
- Failed Events
- Consumer Lag
- Processing Time
- Retry Count
- DLQ Count
- Replay Count

Every event is traceable.

---

# AI Integration

AI systems consume events such as:

```
DocumentUploaded

↓

OCR

↓

Embedding

↓

Vector Storage

↓

AI Response

↓

Notification
```

AI should integrate through the event platform rather than direct coupling.

---

# Folder Structure

```
events/

├── schemas/

├── producers/

├── consumers/

├── handlers/

├── registry/

├── replay/

├── testing/

└── README.md
```

Every event implementation follows this structure.

---

# Anti-Patterns

Avoid

❌ Chatty Events

❌ Shared Event Payloads

❌ Generic Event Names

❌ Synchronous Chains

❌ Event Loops

❌ Missing Versioning

❌ Missing Correlation IDs

❌ Business Logic in Broker

❌ Event Without Documentation

---

# Production Checklist

Before introducing a new event:

- [ ] Business event identified
- [ ] Event name follows convention
- [ ] Schema documented
- [ ] Version assigned
- [ ] Topic approved
- [ ] Consumers identified
- [ ] Idempotency implemented
- [ ] Retry policy configured
- [ ] DLQ configured
- [ ] Monitoring enabled
- [ ] Architecture review completed

---

# Success Criteria

The Event-Driven Architecture is successful when:

- Business domains remain loosely coupled.
- New consumers are added without modifying producers.
- Event contracts remain stable.
- Consumers are idempotent.
- Event replay supports recovery.
- AI workflows integrate through events.
- Business processes scale independently.
- Platform observability provides complete event traceability.

---

# Future Evolution

Future versions will include:

- C4 Event Architecture Diagram
- UML Sequence Diagrams
- Kafka Topic Design Standards
- Event Catalog
- Schema Registry Implementation
- Saga Orchestration Examples
- Choreography vs Orchestration Decision Matrix
- Outbox Pattern
- Inbox Pattern
- CDC (Change Data Capture)
- Event Sourcing Evaluation
- FastAPI + Kafka Reference Implementation
- OpenTelemetry Trace Propagation
- Event Testing Framework
- AI Event Pipeline Reference Architecture

---

# Event-Driven Architecture Checklist

- [x] Purpose Defined
- [x] Event Principles Established
- [x] Event Lifecycle Defined
- [x] Event Types Standardized
- [x] Naming Convention Added
- [x] Event Envelope Defined
- [x] Versioning Strategy Added
- [x] Broker Standards Established
- [x] Delivery Guarantees Defined
- [x] Idempotency Requirements Added
- [x] Retry & DLQ Strategy Defined
- [x] Saga Guidance Included
- [x] Security Requirements Added
- [x] Observability Standards Defined
- [x] AI Integration Guidance Added
- [x] Production Checklist Added
- [x] Success Criteria Defined

---

# Document Status

**Document:** NES-107 — Event-Driven Architecture

**Version:** 1.0.0

**Status:** Ready for Architecture Review

**Next Document:** **NES-108 — Service Communication**

---

# Revision Queue for Version 2.0 (Enterprise Edition)

Future enhancements will include:

- C4 Context, Container & Component Diagrams
- Event Storming Workshop Guide
- Complete Kafka Topic Taxonomy
- AsyncAPI Specifications
- CloudEvents Standard Adoption
- Outbox & Inbox Pattern Reference Implementations
- Event Version Migration Strategy
- Event Contract Testing Framework
- Distributed Trace Correlation Examples
- Multi-Region Event Streaming
- Event Governance Dashboard
- Event Retention & Archival Policy
- AI Event Processing Pipeline
- Production FastAPI + Kafka + OpenTelemetry Reference Architecture
- Event Maturity Assessment Model

These enhancements will establish the definitive enterprise Event-Driven Architecture standard for all NeelStack products, platform services, AI systems, and future distributed applications.
