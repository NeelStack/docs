---
document_id: NES-105
title: Modular Monolith Architecture
subtitle: Enterprise Modular Monolith Standard for the NeelStack Platform
version: 1.0.0
status: Draft
classification: Internal
owner: Chief Solution Architect
review_cycle: Every 6 Months
document_type: Architecture Standard
parent_document: NES-104 Clean Architecture
next_document: NES-106 Microservice Guidelines
---

# NES-105 — Modular Monolith Architecture

> **"Start modular. Scale intelligently. Split only when business demands it."**

---

# Executive Summary

NeelStack adopts a **Modular Monolith Architecture** as the default architecture for all new backend applications.

Unlike traditional monoliths, a Modular Monolith consists of **independent business modules** living within a single deployable application while maintaining strict architectural boundaries.

This approach provides:

- Simpler development
- Faster deployment
- Easier debugging
- Lower infrastructure cost
- Better developer productivity
- Strong domain isolation
- Straightforward evolution into microservices

A Modular Monolith is **not** a temporary architecture.

It is the preferred architecture until measurable business or technical requirements justify service decomposition.

---

# Purpose

This document defines:

- Modular Monolith principles
- Module boundaries
- Internal communication
- Data ownership
- Dependency rules
- Module lifecycle
- Extraction strategy
- Governance
- Production standards

This standard applies to all NeelStack backend systems unless an approved ADR specifies otherwise.

---

# Why Modular Monolith?

NeelStack values simplicity.

Microservices introduce:

- Distributed transactions
- Network latency
- Service discovery
- Observability complexity
- Operational overhead
- Deployment coordination

These costs should only be accepted when justified.

A Modular Monolith provides:

- One deployment
- One runtime
- One codebase
- One database instance
- Multiple independent business modules

---

# Core Philosophy

```text
Business

↓

Bounded Context

↓

Module

↓

Clean Architecture

↓

Single Deployable

↓

Future Microservices
```

Every module is designed as if it could become an independent service.

---

# Architectural Principles

---

## Principle 1 — Modules Represent Business Domains

Modules mirror business capabilities.

Examples

```text
Identity

Students

Courses

Teachers

Attendance

Billing

Notifications

Reporting

AI
```

Technology should never define module boundaries.

---

## Principle 2 — Strong Module Boundaries

Every module owns:

- Business Rules
- APIs
- Events
- Database Tables
- Validation
- Tests

Modules must never expose internal implementation.

---

## Principle 3 — Independent Development

Engineers should be able to work within one module without understanding the entire application.

---

## Principle 4 — Internal APIs

Modules communicate through explicit interfaces.

Never:

Import internal classes directly.

Instead:

```
Module API

↓

Application Interface

↓

Business Operation
```

---

## Principle 5 — Future Extraction

Every module should be designed so that it can become an independent microservice with minimal refactoring.

---

# High-Level Architecture

```text
                   FastAPI Application

                          │

 ┌──────────────────────────────────────────────────────┐

 │                  Shared Platform                      │

 │------------------------------------------------------│

 │ Auth │ Logger │ Config │ Events │ Cache │ Storage │

 └──────────────────────────────────────────────────────┘

                          │

 ┌──────────────────────────────────────────────────────┐

 │                 Business Modules                      │

 │------------------------------------------------------│

 │ Student │ Course │ Teacher │ Billing │ Notification │

 │ Analytics │ Workflow │ AI │ Reporting │ Identity │

 └──────────────────────────────────────────────────────┘

                          │

                    PostgreSQL Database
```

One deployment.

Multiple isolated modules.

---

# Module Structure

Every module follows exactly the same structure.

```text
student/

├── api/

├── application/

│   ├── commands/

│   ├── queries/

│   ├── dto/

│   └── services/

├── domain/

│   ├── entities/

│   ├── value_objects/

│   ├── repositories/

│   ├── events/

│   ├── services/

│   └── exceptions/

├── infrastructure/

│   ├── persistence/

│   ├── integrations/

│   └── messaging/

├── tests/

└── README.md
```

Consistency enables maintainability.

---

# Module Responsibilities

Every module owns:

- Business Logic
- Validation
- Persistence
- Events
- APIs
- Documentation
- Tests

Modules should never depend upon another module's internals.

---

# Internal Communication

Preferred communication order:

1. Module Interface
2. Domain Event
3. Shared Platform Service

Avoid direct implementation imports.

Example

```text
Student Module

↓

Enrollment API

↓

Course Module
```

Instead of

```text
Student

↓

CourseRepository
```

---

# Data Ownership

Each module owns its schema.

Example

```text
student_*

course_*

teacher_*

billing_*
```

No module may update another module's tables directly.

Shared database.

Private ownership.

---

# Shared Kernel

Some capabilities are shared.

Examples

- Authentication
- RBAC
- Logging
- Configuration
- Notifications
- AI SDK
- Event Bus

These belong to the Platform Layer—not to business modules.

---

# Module Lifecycle

```text
Business Requirement

↓

Domain Discovery

↓

Module Creation

↓

Implementation

↓

Testing

↓

Deployment

↓

Evolution

↓

Possible Extraction
```

Architecture should support continuous evolution.

---

# Module Dependency Rules

Allowed

```text
Module

↓

Platform Package

↓

Infrastructure Interface
```

Allowed

```text
Module

↓

Published Module API
```

Forbidden

```text
Module

↓

Another Module's Domain

↓

Infrastructure

↓

Private Classes
```

---

# Module Registration

Every module should register itself through a central registry.

Example

```python
register_module(
    name="student",
    routes=student_router,
    events=student_events,
    permissions=student_permissions,
)
```

Modules should remain self-contained.

---

# Transactions

Transactions remain local to a module whenever possible.

Cross-module operations should use:

- Domain Events
- Process Managers
- Sagas (when required)

Avoid distributed transactions.

---

# Event Flow

```text
Student Created

↓

Student Module

↓

Domain Event

↓

Notification Module

↓

Analytics Module

↓

Audit Module
```

Loose coupling improves scalability.

---

# Folder Structure (Application)

```text
apps/api/

├── modules/

│   ├── identity/

│   ├── students/

│   ├── teachers/

│   ├── courses/

│   ├── attendance/

│   ├── finance/

│   ├── workflow/

│   ├── notifications/

│   ├── analytics/

│   └── ai/

├── platform/

├── shared/

└── bootstrap/
```

The application assembles modules rather than implementing business logic.

---

# Module Extraction Strategy

A module becomes a microservice only when justified.

Evaluation criteria:

- Independent scaling
- Independent deployment
- Team ownership
- Performance isolation
- Regulatory requirements
- Operational necessity

Premature extraction is prohibited.

---

# Anti-Patterns

Avoid

❌ God Module

❌ Shared Business Logic

❌ Cross-Module SQL

❌ Circular Dependencies

❌ Generic "Utils" Module

❌ Feature Flags Replacing Architecture

❌ Large Shared Libraries

❌ Module Coupling

❌ Business Logic in Shared Package

---

# AI Considerations

A Modular Monolith is ideal for AI-assisted engineering because:

- Modules are small.
- Context windows remain manageable.
- Business boundaries are explicit.
- Folder structures are predictable.
- Code ownership is clear.

AI agents should operate on one module at a time.

---

# Performance Considerations

Modular Monoliths benefit from:

- No network latency
- Local transactions
- Simpler debugging
- Shared memory
- Efficient database access

Optimize modularity before distribution.

---

# Observability

Each module should expose:

- Structured logs
- Metrics
- Domain events
- Health indicators
- Performance counters

Operational visibility should exist at module vocabulary/granularity.

---

# Production Checklist

Before introducing a new module:

- [ ] Business capability identified
- [ ] Module owner assigned
- [ ] Bounded Context documented
- [ ] Public API defined
- [ ] Events documented
- [ ] Database ownership defined
- [ ] Tests implemented
- [ ] Documentation completed
- [ ] Architecture review approved

---

# Success Criteria

The Modular Monolith architecture is successful when:

- Modules remain independently understandable.
- Cross-module dependencies remain minimal.
- Platform services eliminate duplication.
- New business capabilities are added without affecting unrelated modules.
- Engineers can extract a module into a microservice with limited refactoring.
- AI assistants generate code within clear module boundaries.

---

# Future Evolution

Future revisions will include:

- C4 Module Diagram
- UML Package Diagram
- Module Dependency Matrix
- Context Map for EduOS
- Context Map for ToolVines
- Event Catalog Between Modules
- Saga Patterns
- Module Extraction Playbook
- Architecture Fitness Rules
- Automated Boundary Validation
- FastAPI Bootstrap Reference
- Plugin-Based Module Loading
- Feature Module Templates

---

# Modular Monolith Checklist

- [x] Purpose Defined
- [x] Principles Established
- [x] Module Structure Standardized
- [x] Communication Rules Defined
- [x] Data Ownership Rules Added
- [x] Shared Kernel Defined
- [x] Lifecycle Documented
- [x] Dependency Rules Established
- [x] Registration Model Added
- [x] Transaction Strategy Defined
- [x] Event Flow Explained
- [x] Extraction Strategy Defined
- [x] Anti-Patterns Listed
- [x] AI Guidance Included
- [x] Production Checklist Added
- [x] Success Criteria Defined

---

# Document Status

**Document:** NES-105 — Modular Monolith Architecture

**Version:** 1.0.0

**Status:** Ready for Architecture Review

**Next Document:** **NES-106 — Microservice Guidelines**

---

# Revision Queue for Version 2.0 (Enterprise Edition)

This document will be expanded with:

- C4 Module & Component Diagrams
- UML Sequence Diagrams for Module Interactions
- Reference FastAPI Modular Monolith Implementation
- Plugin-Based Module Discovery Architecture
- Module Dependency Heat Maps
- Architecture Fitness Functions (Import Rules)
- Automatic Module Registration Framework
- Event Storming Examples
- EduOS Reference Module Breakdown
- ToolVines Reference Module Breakdown
- Module Extraction Decision Matrix
- Modular Testing Strategy
- Performance Benchmarking Guidelines
- Multi-Team Module Ownership Model
- Migration Guide: Modular Monolith → Microservices
