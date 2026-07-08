---
document_id: TECH-001
title: Technology Stack
subtitle: The approved, frozen NeelStack technology stack — all deviations require ARB approval
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Chief Architect
review_cycle: Every 6 Months
document_type: Technology Standard
next_document: TECH-002 Next.js
---

# TECH-001 — NeelStack Technology Stack

> **"Technology choices are architectural decisions. Every dependency we add is a commitment we make."**

---

## Overview

This document defines the **officially approved NeelStack technology stack**. Every project, service, and product built within NeelStack must use the technologies defined here.

Any deviation from this stack requires a formal **ARB (Architecture Review Board) approval** and a corresponding **ADR (Architecture Decision Record)**.

---

## Core Stack Summary

| Layer | Technology | Version Policy |
|---|---|---|
| **Web Frontend** | Next.js 15 + React 19 | LTS, pin exact version |
| **Mobile** | React 19 + Vite + Capacitor 7 | Pin exact SDK |
| **Backend** | FastAPI + Python 3.12+ | Pin minor version |
| **Primary Database** | PostgreSQL 16+ | Pin major version |
| **Cache** | Redis 7+ | Pin major version |
| **Search** | OpenSearch 2+ | Pin major version |
| **Message Queue** | RabbitMQ / Kafka | See TECH-007 |
| **Object Storage** | AWS S3 / MinIO | — |
| **Container Runtime** | Docker 25+ | — |
| **Orchestration** | Kubernetes 1.29+ | — |
| **IaC** | Terraform 1.7+ | Pin minor version |
| **CI/CD** | GitHub Actions | — |
| **AI / LLM** | OpenAI, Gemini, Anthropic | Via abstraction layer |

---

## Stack Rationale

### Why Next.js?
- Full-stack React framework with SSR, SSG, and API routes
- Native TypeScript support
- Vercel deployment optimization
- Strong ecosystem for SaaS and EduTech applications

### Why FastAPI?
- Python 3.12+ async-native
- Automatic OpenAPI generation
- Native Pydantic v2 data validation
- Excellent AI/ML library ecosystem

### Why PostgreSQL?
- Battle-tested ACID compliance
- JSONB for flexible schema
- Native full-text search
- pgvector for AI embeddings
- Multi-tenant row-level security

### Why Redis?
- Sub-millisecond caching
- Session storage
- Pub/Sub messaging
- Rate limiting
- Distributed locks

---

## Approved Package Lists

Approved packages for each layer are documented in their respective technology standards:
- **Frontend**: NES-300 — Frontend Engineering Standards
- **Backend Python**: NES-200 — Python Engineering Standards
- **Mobile**: NES-400 — Capacitor Mobile Standards
- **AI/ML**: NES-218 — AI Knowledge Platform

---

## Adding a New Technology

1. Raise an RFC in `20-rfcs/` documenting the need
2. ARB reviews and votes
3. ARB decision recorded as ADR in `19-adrs/`
4. This document updated to reflect approved addition
5. Corresponding NES standard created

---

## Version History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2026-07-04 | NeelStack Engineering | Initial publication |
