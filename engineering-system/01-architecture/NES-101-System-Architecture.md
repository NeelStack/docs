---
document_id: NES-101
title: System Architecture
subtitle: Enterprise Reference Architecture for the NeelStack Ecosystem
version: 2.0.0
status: Approved
classification: Internal
owner: Chief Solution Architect
review_cycle: Every 6 Months
document_type: Architecture Standard
parent_document: NES-100 Architecture Principles
next_document: NES-102 Monorepo Architecture
---

# NES-101 — System Architecture

> **"Architecture is the blueprint that allows hundreds of engineers to build one coherent platform."**

---

# Executive Summary

The NeelStack System Architecture defines the target reference architecture for every application, platform service, AI capability, mobile application, and shared component built within the NeelStack ecosystem.

Rather than designing each product independently, NeelStack adopts a **Platform-First, AI-Native, Cloud-Native** architecture where reusable capabilities are centralized and products consume shared platform services.

This architecture enables:

- Consistent engineering practices
- Faster product delivery
- High platform reuse
- Strong security
- Operational excellence
- AI integration by design

---

# Purpose

This document establishes the reference architecture that all products must follow.

It defines:

- System boundaries
- Core architectural layers
- Shared platform services
- Communication patterns
- Deployment models
- Technology boundaries
- Operational architecture

---

# Architectural Goals

Every NeelStack system should optimize for:

- Maintainability
- Scalability
- Reliability
- Security
- Performance
- Developer Productivity
- AI Readiness
- Platform Reuse
- Cost Efficiency
- Operational Simplicity

---

# Non-Goals

This document does **not** define:

- Programming standards
- API conventions
- Database schema design
- CI/CD implementation
- Security implementation details

Those are covered in later standards.

---

# System Vision

```text
                                  Customers
                                      │
                             Web • Mobile • API
                                      │
                                Traefik Proxy
                                      │
                              Next.js Web Portal
                                      │
                        Core API Gateway (FastAPI)
                                      │
       ┌─────────────────────────────────────────────────────────────┐
       │                   Platform Service Layer                    │
       │-------------------------------------------------------------│
       │ Identity (OIDC)   │ Local & Remote AI │ Billing (Checkout)  │
       │ Webhooks Registry │ GDPR / DPDP Act   │ Uptime SLA Tracker  │
       └─────────────────────────────────────────────────────────────┘
                                      │
                         Domain Application Services
                                      │
                     EduOS │ Future Platform Applications
                                      │
                     Event Bus (RabbitMQ / Socket.io)
                                      │
                  Background Workers & Async Processing
                                      │
             PostgreSQL (pgvector) │ Redis │ Object Storage
                                      │
                 Structured Mutation Audit & Telemetry
```

---

# Architectural Layers

The NeelStack platform consists of eight logical layers.

### Layer 1 — Experience Layer

Responsible for user interaction.

Includes:

- Next.js Web
- Capacitor Mobile (React/Vite)
- Public APIs
- Admin Portal

Responsibilities:

- UI Rendering
- Client Validation
- Session Management
- Accessibility

---

### Layer 2 — Edge Layer

Provides external protection.

Components:

- CDN
- Traefik Reverse Proxy
- Rate Limiting
- DNS
- SSL
- Caching

No business logic exists at this layer.

---

### Layer 3 — Gateway Layer

Acts as the single entry point.

Responsibilities:

- Tenant Domain Normalization (`normalise_domain()` stripping www and ports)
- OIDC / SAML 2.0 SSO Authentication
- API Routing
- Redis Sliding-Window Rate Limiting
- Security Headers Injection (HSTS, CSP, X-Frame)

---

### Layer 4 — Platform Layer

Provides reusable capabilities.

Examples:

- Identity (Zitadel / OAuth)
- Webhooks Registry (HMAC signatures + retries)
- Uptime SLA Credit Engine
- Central Licensing Validator (grace period management)
- Central Billing Manager (Stripe / Razorpay)

Every product consumes these services.

---

### Layer 5 — Domain Layer

Contains product-specific business capabilities.

Examples:

- Student Management
- Course Management
- Attendance Logging
- Exam Management

Business rules live only here.

---

### Layer 6 — Integration Layer

Responsible for communication.

Includes:

- REST
- Webhooks Dispatcher
- Real-time Socket.io channels
- Queues (RabbitMQ)

---

### Layer 7 — Data Layer

Provides persistence.

Technologies:

- PostgreSQL (SaaS RLS, Schema Isolation, or Dedicated Decrypted DB connections)
- Redis Cache
- Object Storage
- Vector Database (Postgres pgvector with school_id composite keys)

---

### Layer 8 — Operations Layer

Responsible for production operations.

Includes:

- Monitoring (Prometheus)
- Logging (Structured mutation audits)
- Metrics
- OpenTelemetry Tracing

---

# The Four-Model Deployment Topology

NeelStack is built on a single unified codebase that dynamically configures itself to target:

1. **SaaS Multi-Tenant**: Shared PostgreSQL database instance with dynamic row-level security (RLS) filtering logic.
2. **White Label**: Per-tenant styling custom CSS variables and custom domain routing (matching both subdomains and apex hosts).
3. **Dedicated Cloud**: Isolated physical database instances. Connection parameters decrypted dynamically via AES Fernet `EncryptedString` type decorators.
4. **Self-Hosted (On-Premise)**: Deployment container bundle configured via env variables. Leverages local sidecars for offline speech-to-text (Whisper) and chat/embedding engines (Ollama).

---

# 9-Layer AI Gateway Architecture

NeelStack features a dedicated async AI Gateway microservice (`dhruva-ai`) decoupled from relational database schemas:

1. **Layer 1 — Infrastructure**: pgvector schema mapping and database connection pooling.
2. **Layer 2 — AI Content Generation**: Lesson planning and comment generation.
3. **Layer 3 — Persona Gateways**: Interfaces optimized for student tutoring, parent questions, admin overviews, and CFO cash flow models.
4. **Layer 4 — Ingestion Pipeline**: Document text extraction, semantic chunking, and index upsert runs.
5. **Layer 5 — Predictive early warnings**: Grade decline, dropout risk, and payment default projections.
6. **Layer 7 — Multimodal Integration**: Voice class registers and optical sheet assessment.
7. **Layer 8 — Agentic Workflows**: Event-driven task orchestrators mapping specialized workers.
8. **Layer 9 — AI Governance**: Disparate impact audits, bias checks, and immutable cryptographically signed logs.

---

# Document Status

**Document:** NES-101 — System Architecture

**Version:** 2.0.0 (Approved)

**Status:** Active Reference Standard

**Next Document:** **NES-102 — Monorepo Architecture**
