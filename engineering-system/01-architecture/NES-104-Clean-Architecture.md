---
document_id: NES-104
title: Clean Architecture
subtitle: Enterprise Clean Architecture Standard for the NeelStack Platform
version: 1.0.0
status: Draft
classification: Internal
owner: Chief Solution Architect
review_cycle: Every 6 Months
document_type: Architecture Standard
parent_document: NES-103 Domain-Driven Design
next_document: NES-105 Modular Monolith Architecture
---

# NES-104 — Clean Architecture

> **"Frameworks are temporary. Business rules are permanent."**
>
> — Inspired by Robert C. Martin (Uncle Bob)

---

# Executive Summary

NeelStack adopts **Clean Architecture** as the standard architectural style for all backend systems.

The objective is simple:

> **Business logic should never depend on technology.**

Frameworks change.

Databases change.

Cloud providers change.

Programming languages evolve.

Business rules survive.

This document defines how every FastAPI application, Platform Service, AI Service, Worker, Scheduler and API should be architected.

---

# Purpose

This standard defines:

- Layered Architecture
- Dependency Rule
- Application Boundaries
- Layer Responsibilities
- Folder Structure
- Dependency Injection
- Data Flow
- Testing Strategy
- Framework Isolation

Every backend service must follow this document.

---

# Core Philosophy

```
Business Rules

↓

Application Rules

↓

Infrastructure

↓

Frameworks

↓

Operating System
```

The center should never know what exists outside.

---

# Goals

The architecture should maximize:

- Maintainability
- Testability
- Scalability
- Readability
- Replaceability
- Independence
- AI Readability

---

# Non Goals

Clean Architecture is NOT intended to:

- Increase abstraction unnecessarily
- Create excessive interfaces
- Reduce developer productivity
- Over-engineer simple applications

Engineering judgment is required.

---

# The Dependency Rule

This is the most important rule.

> Source code dependencies always point inward.

Never outward.

```
Presentation

↓

Application

↓

Domain

↑

Infrastructure
```

The Domain Layer knows nothing.

Everything else depends on it.

---

# Architectural Layers

NeelStack uses four primary layers.

```
Presentation

↓

Application

↓

Domain

↓

Infrastructure
```

---

# Layer 1 — Presentation

Purpose

Communicate with the outside world.

Examples

- FastAPI Routes
- REST APIs
- GraphQL
- CLI
- Workers
- Scheduled Jobs

Responsibilities

- Receive Requests
- Validate Input
- Call Application Layer
- Return Response

Presentation must never contain business logic.

---

# Layer 2 — Application

Purpose

Coordinate business use cases.

Contains

- Use Cases
- Commands
- Queries
- DTOs
- Interfaces
- Application Services

Responsibilities

- Execute workflow
- Coordinate domain
- Publish events
- Call repositories

Application orchestrates.

It does not decide business rules.

---

# Layer 3 — Domain

Purpose

Contains business knowledge.

Contains

- Entities
- Value Objects
- Domain Services
- Domain Events
- Business Rules
- Aggregates

This is the heart of the application.

It has zero framework dependencies.

---

# Layer 4 — Infrastructure

Purpose

Implements technical concerns.

Contains

- PostgreSQL
- Redis
- Kafka
- Email
- File Storage
- FastAPI
- External APIs
- AWS
- Azure

Infrastructure implements interfaces defined by inner layers.

---

# Architecture Diagram

```
             FastAPI

                │

          API Controller

                │

         Application Layer

                │

          Domain Layer

                │

Repository Interface

                │

 Repository Implementation

                │

          PostgreSQL
```

Notice:

The Domain does NOT know PostgreSQL exists.

---

# Layer Responsibilities

## Presentation

Allowed

✓ Validation

✓ Authentication

✓ Serialization

✓ HTTP

Forbidden

✗ SQL

✗ Business Rules

✗ Domain Decisions

---

## Application

Allowed

✓ Transactions

✓ Use Cases

✓ Workflow

✓ Event Publishing

Forbidden

✗ SQL

✗ HTTP

✗ Framework Logic

---

## Domain

Allowed

✓ Business Rules

✓ Validation

✓ Aggregates

✓ Entities

✓ Domain Events

Forbidden

✗ Database

✗ HTTP

✗ Framework

✗ Cloud SDK

---

## Infrastructure

Allowed

✓ SQL

✓ Redis

✓ Storage

✓ Kafka

✓ External APIs

✓ Email

Forbidden

✗ Business Decisions

---

# Folder Structure

```
student/

├── presentation/

│   ├── api/

│   ├── schemas/

│   └── controllers/

│

├── application/

│   ├── commands/

│   ├── queries/

│   ├── dto/

│   ├── interfaces/

│   └── services/

│

├── domain/

│   ├── entities/

│   ├── value_objects/

│   ├── repositories/

│   ├── services/

│   ├── events/

│   └── exceptions/

│

├── infrastructure/

│   ├── database/

│   ├── repositories/

│   ├── cache/

│   ├── email/

│   ├── storage/

│   └── messaging/

│

└── tests/
```

Every domain follows the same structure.

---

# Request Lifecycle

```
HTTP Request

↓

Controller

↓

Use Case

↓

Aggregate

↓

Repository Interface

↓

Repository Implementation

↓

Database

↓

Response
```

Every request follows the same path.

---

# Dependency Injection

Dependencies should be injected.

Never created manually.

Example

```
Controller

↓

Service Interface

↓

Concrete Service

↓

Repository Interface

↓

Repository
```

This enables:

- Testing
- Swapping implementations
- Loose coupling

---

# Interface Ownership

Interfaces belong to the inner layer.

Implementations belong to the outer layer.

Example

```
Domain

↓

StudentRepository

↓

Infrastructure

↓

PostgresStudentRepository
```

Never reverse ownership.

---

# Data Flow

```
HTTP

↓

DTO

↓

Use Case

↓

Entity

↓

Repository

↓

Database

↓

Entity

↓

Response DTO

↓

JSON
```

Database models must never leak into APIs.

---

# Error Handling

Errors originate from the Domain.

Application maps them.

Presentation converts them into HTTP responses.

Infrastructure logs them.

Every layer has one responsibility.

---

# Transactions

Transactions belong inside the Application Layer.

Business entities should not manage transactions.

---

# Validation

Validation occurs at three levels.

Presentation

↓

DTO validation

↓

Domain validation

Presentation validates syntax.

Domain validates business rules.

---

# Testing Strategy

Presentation

Integration Tests

Application

Use Case Tests

Domain

Pure Unit Tests

Infrastructure

Integration Tests

The Domain should be testable without PostgreSQL.

---

# Cross-Cutting Concerns

Handled through middleware or decorators.

Examples

Authentication

Authorization

Logging

Metrics

Tracing

Caching

Rate Limiting

Audit

Business logic remains clean.

---

# Clean Architecture Checklist

Every feature must satisfy:

✓ Business logic inside Domain

✓ No SQL in Controllers

✓ No HTTP in Domain

✓ Repository interfaces in Domain

✓ Infrastructure implements interfaces

✓ Dependency Rule maintained

✓ Domain independently testable

✓ Framework replaceable

---

# Anti-Patterns

Avoid

❌ Fat Controllers

❌ Fat Repositories

❌ Active Record

❌ Database First Design

❌ Business Logic in SQL

❌ Business Logic in FastAPI

❌ Circular Dependencies

❌ Framework Driven Development

❌ Domain importing FastAPI

❌ Domain importing SQLAlchemy

❌ Infrastructure calling Controllers

---

# AI Engineering Considerations

Clean Architecture dramatically improves AI-assisted development.

Benefits

- Predictable structure
- Smaller contexts
- Better code generation
- Easier reasoning
- Better testing
- Consistent architecture

AI agents should generate code inside one architectural layer at a time.

---

# Performance Considerations

Clean Architecture should not become over-engineered.

Guidelines

- Avoid unnecessary abstractions.
- Use interfaces only where beneficial.
- Optimize critical paths.
- Measure before optimizing.
- Keep use cases cohesive.

---

# Production Checklist

Before deployment verify:

- [ ] Dependency Rule satisfied
- [ ] Layer boundaries respected
- [ ] Domain has zero framework imports
- [ ] Repository interfaces defined
- [ ] Infrastructure isolated
- [ ] Tests passing
- [ ] Architecture review completed
- [ ] Documentation updated
- [ ] ADR approved (if applicable)

---

# Success Criteria

Clean Architecture is successful when:

- Framework upgrades require minimal business changes.
- Domain logic remains stable over time.
- Business rules are fully testable.
- Infrastructure can be replaced with minimal effort.
- Engineers can understand feature flow quickly.
- AI assistants generate consistent implementations.
- Technical debt decreases as the platform evolves.

---

# Future Evolution

Future revisions will include:

- Complete C4 Component Diagram
- UML Package Diagram
- Sequence Diagrams for Request Lifecycle
- Dependency Graph Examples
- FastAPI Reference Implementation
- Async Application Service Patterns
- CQRS Integration
- Event-Driven Clean Architecture
- AI Service Clean Architecture
- Worker Architecture
- Background Job Architecture
- Architecture Fitness Tests
- Automated Dependency Validation

---

# Clean Architecture Checklist

- [x] Purpose Defined
- [x] Dependency Rule Defined
- [x] Four Layers Established
- [x] Responsibilities Documented
- [x] Folder Structure Standardized
- [x] Request Lifecycle Explained
- [x] Dependency Injection Standardized
- [x] Interface Ownership Defined
- [x] Validation Strategy Added
- [x] Testing Strategy Added
- [x] Cross-Cutting Concerns Defined
- [x] Anti-Patterns Listed
- [x] AI Engineering Guidance Included
- [x] Production Checklist Added
- [x] Success Criteria Defined

---

# Document Status

**Document:** NES-104 — Clean Architecture

**Version:** 1.0.0

**Status:** Ready for Architecture Review

**Next Document:** **NES-105 — Modular Monolith Architecture**

---

# Revision Queue for Version 2.0 (Enterprise Edition)

Future enhancements will include:

- C4 Component & Code Diagrams
- UML Layer Dependency Diagrams
- Complete FastAPI Reference Project
- Dependency Enforcement with Import Rules
- Example Feature Walkthrough (Student Registration)
- Architecture Fitness Functions
- Layer-by-Layer Code Review Checklist
- Performance Optimization Patterns
- Async & Event-Driven Integration
- AI Code Generation Prompts by Layer
- Migration Guide from Legacy Architectures
- Architectural Smell Detection Guide

These additions will make the Clean Architecture standard a comprehensive implementation guide suitable for enterprise-scale systems and long-term platform evolution.
