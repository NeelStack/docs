---
document_id: NES-201
title: FastAPI Architecture
subtitle: Enterprise FastAPI Architecture Standard for the NeelStack Platform
version: 1.0.0
status: Draft
classification: Internal
owner: Chief Solution Architect
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-200 Python Engineering Standards
next_document: NES-202 API Design Standards
---

# NES-201 — FastAPI Architecture

> **"FastAPI is our framework. Clean Architecture is our architecture."**

---

# Executive Summary

FastAPI is the **official backend framework** for all NeelStack products.

It powers:

- REST APIs
- Internal APIs
- AI Gateway
- Platform Services
- Background Workers
- Webhooks
- Internal Admin APIs
- MCP Servers
- Future AI Services

FastAPI provides:

- High performance
- Excellent typing support
- Automatic OpenAPI documentation
- Native async support
- Excellent developer experience

FastAPI **must never contain business logic**.

It is only the Presentation Layer.

---

# Purpose

This document defines:

- FastAPI Architecture
- Project Structure
- Routing
- Dependency Injection
- Middleware
- Exception Handling
- Authentication
- Validation
- Background Tasks
- Startup Lifecycle
- Performance
- Security
- Production Standards

---

# Architecture Philosophy

```
HTTP Request

↓

FastAPI Router

↓

Application Layer

↓

Domain Layer

↓

Infrastructure

↓

Database

↓

Response
```

FastAPI never talks directly to PostgreSQL.

---

# Technology Stack

| Layer | Technology |
|----------|----------------|
| Framework | FastAPI |
| Server | Uvicorn |
| Validation | Pydantic v2 |
| ORM | SQLAlchemy 2 |
| Migrations | Alembic |
| Authentication | JWT + OAuth2 |
| Dependency Injection | FastAPI Depends |
| Documentation | OpenAPI |
| Testing | Pytest |
| Background Jobs | Celery / Dramatiq |
| Cache | Redis |
| Messaging | Kafka |
| Observability | OpenTelemetry |

---

# FastAPI Project Structure

```text
apps/api/

├── app/

│   ├── api/

│   │   ├── v1/

│   │   ├── middleware/

│   │   ├── dependencies/

│   │   └── routers/

│   │

│   ├── modules/

│   │

│   ├── platform/

│   │

│   ├── shared/

│   │

│   ├── config/

│   │

│   ├── bootstrap/

│   │

│   ├── main.py

│   └── lifespan.py

│

├── tests/

├── docs/

└── pyproject.toml
```

---

# Application Startup

Startup Flow

```
Configuration

↓

Logger

↓

Database

↓

Redis

↓

Kafka

↓

Module Registration

↓

Middleware

↓

Routes

↓

Application Ready
```

Initialization should be deterministic.

---

# Lifespan Events

Use FastAPI lifespan.

Never use deprecated startup events.

Example

```
Application Start

↓

Initialize Services

↓

Register Modules

↓

Warm Cache

↓

Ready
```

Shutdown

```
Drain Workers

↓

Close Connections

↓

Flush Logs

↓

Shutdown
```

---

# Module Registration

Each business module registers itself.

Example

```python
register_module(
    student_module
)
```

The bootstrap layer assembles modules.

---

# Router Structure

```
api/

└── v1/

    ├── students.py

    ├── teachers.py

    ├── courses.py

    ├── auth.py

    └── health.py
```

Routers remain thin.

---

# Controller Responsibilities

Controllers may

✓ Validate Requests

✓ Authenticate

✓ Call Use Cases

✓ Return Responses

Controllers must NOT

✗ Execute SQL

✗ Implement Business Rules

✗ Access Redis

✗ Publish Kafka Messages Directly

---

# Dependency Injection

Use

```
Depends()
```

Dependencies include

- Database Session
- Authentication
- Current User
- Tenant
- Configuration

Business services should be injected.

---

# Request Lifecycle

```
HTTP Request

↓

Middleware

↓

Authentication

↓

Authorization

↓

Validation

↓

Router

↓

Application Service

↓

Domain

↓

Repository

↓

Database

↓

Response DTO

↓

JSON Response
```

---

# Response Model

Always use Pydantic models.

Never return ORM models directly.

Example

```
StudentEntity

↓

StudentResponse

↓

JSON
```

---

# Validation

Validation occurs at three levels.

Level 1

Pydantic

↓

Level 2

Application

↓

Level 3

Domain

Business rules belong in the Domain.

---

# Exception Handling

Global exception handlers.

Examples

```
ValidationError

↓

400

StudentNotFound

↓

404

BusinessRuleViolation

↓

422

UnhandledException

↓

500
```

Responses remain consistent.

---

# Authentication

Supported

JWT

OAuth2

Service Tokens

API Keys

Future

OIDC

SSO

Passkeys

Authentication belongs in middleware.

---

# Authorization

RBAC

↓

Permission

↓

Resource

↓

Business Rule

Authorization should occur before business execution.

---

# Middleware Stack

```
Request ID

↓

Logging

↓

Tracing

↓

Rate Limiting

↓

Authentication

↓

Authorization

↓

Compression

↓

Response
```

Middleware order matters.

---

# Logging

Every request logs

- Request ID
- Trace ID
- User ID
- Tenant ID
- Duration
- Status Code

Structured JSON logs only.

---

# OpenAPI

Every endpoint must define

- Summary
- Description
- Tags
- Response Models
- Error Responses
- Authentication

API documentation is mandatory.

---

# Versioning

```
/api/v1/

/api/v2/
```

Breaking changes require new versions.

---

# Pagination

Standard response

```json
{
  "items": [],
  "page":1,
  "size":20,
  "total":250
}
```

All collection endpoints should support pagination.

---

# Filtering

Support

- Filter
- Search
- Sort
- Pagination

Consistent query parameters across all APIs.

---

# File Upload

Uploads go through

```
API

↓

Validation

↓

Virus Scan

↓

Object Storage

↓

Metadata

↓

Response
```

Never store files locally.

---

# Background Tasks

Use background workers for

- Email
- Reports
- AI
- PDF
- OCR
- Notifications

Never block HTTP requests.

---

# Health Endpoints

Mandatory

```
GET /health

GET /ready

GET /live

GET /metrics
```

---

# Caching

Use Redis for

- Sessions
- Query Results
- Feature Flags
- AI Responses
- Configuration

Never cache business-critical mutable state without an invalidation strategy.

---

# Database Sessions

One request

↓

One Session

↓

Automatic Cleanup

Sessions must never leak.

---

# Async Standards

Use async

- Database
- HTTP
- Redis
- AI
- Kafka

Avoid blocking IO.

---

# Performance

Enable

- Compression
- Connection Pooling
- Async IO
- Response Caching
- Query Optimization

Target

```
P95 < 200ms
```

For standard CRUD APIs.

---

# Security

Mandatory

HTTPS

JWT

Rate Limiting

CORS

Input Validation

Output Encoding

Security Headers

Secrets Management

OWASP Top 10 compliance.

---

# Observability

Every endpoint exposes

- Metrics
- Traces
- Logs
- Request IDs
- Error Rates
- Latency

OpenTelemetry required.

---

# Testing

Every endpoint requires

- Unit Tests
- Integration Tests
- API Contract Tests
- Security Tests

Target

```
100%

Critical APIs

90%

Overall
```

---

# Folder Structure Example

```
student/

├── api/

├── application/

├── domain/

├── infrastructure/

├── tests/

├── README.md
```

Every module follows identical structure.

---

# Anti-Patterns

Avoid

❌ Fat Controllers

❌ SQL in Routes

❌ Business Logic in FastAPI

❌ Returning ORM Models

❌ Global Variables

❌ Synchronous HTTP Calls

❌ print()

❌ Hardcoded Secrets

❌ Generic Exception Handling

❌ Missing Response Models

---

# AI Engineering

FastAPI architecture should maximize AI understanding.

Characteristics

- Predictable routing
- Small controllers
- Strong typing
- Clear modules
- Rich OpenAPI
- Clean Architecture

AI should generate

One endpoint

↓

One use case

↓

One business capability

---

# Production Checklist

Before production

- [ ] Architecture compliant
- [ ] OpenAPI complete
- [ ] Authentication enabled
- [ ] Authorization verified
- [ ] Logging implemented
- [ ] Tracing enabled
- [ ] Metrics exposed
- [ ] Health endpoints available
- [ ] Tests passing
- [ ] Documentation complete
- [ ] Performance benchmark passed
- [ ] Security review completed

---

# Success Criteria

FastAPI architecture is successful when

- Controllers remain thin.
- Business logic resides in the Domain.
- APIs remain consistent.
- Documentation is generated automatically.
- Performance remains predictable.
- AI assistants generate compliant endpoints.
- Engineers onboard quickly.
- Framework upgrades require minimal refactoring.

---

# Future Evolution

Version 2.0 will include

- Complete FastAPI Reference Project
- C4 Component Diagrams
- OpenAPI Governance Framework
- Middleware Reference Implementation
- Authentication & Authorization Blueprint
- Async SQLAlchemy Patterns
- Dependency Injection Framework
- Multi-Tenant FastAPI Architecture
- AI Gateway Reference Service
- Background Worker Architecture
- Kubernetes Deployment Guide
- OpenTelemetry Integration
- Performance Tuning Playbook
- Enterprise FastAPI Template Repository

---

# FastAPI Architecture Checklist

- [x] Purpose Defined
- [x] Architecture Flow Defined
- [x] Project Structure Standardized
- [x] Routing Standards Added
- [x] Dependency Injection Defined
- [x] Validation Strategy Added
- [x] Exception Handling Standardized
- [x] Middleware Stack Defined
- [x] Authentication & Authorization Added
- [x] OpenAPI Standards Defined
- [x] Performance & Security Requirements Added
- [x] Observability Included
- [x] AI Engineering Guidance Included
- [x] Production Checklist Added
- [x] Success Criteria Defined

---

# Document Status

**Document:** NES-201 — FastAPI Architecture

**Version:** 1.0.0

**Status:** Ready for Architecture Review

**Next Document:** **NES-202 — API Design Standards**

---

# Revision Queue for Version 2.0 (Enterprise Edition)

Future enhancements will include:

- Production-ready FastAPI Boilerplate
- Complete C4 Architecture & UML Diagrams
- Async SQLAlchemy 2.0 Reference
- Repository & Unit of Work Pattern
- Dependency Injection Container
- API Versioning & Deprecation Policy
- Multi-Tenant FastAPI Reference
- OpenAPI Governance Rules
- OpenTelemetry + Prometheus + Grafana Integration
- JWT, OAuth2, OIDC & SSO Reference Implementations
- AI Gateway & MCP Server Architecture
- Kubernetes Production Deployment
- API Performance Benchmark Suite
- Architecture Fitness Tests
- Enterprise FastAPI Starter Template

These enhancements will make this document the definitive implementation standard for every FastAPI service built within the NeelStack ecosystem and serve as the blueprint for all production backend systems.
