---
document_id: NES-1308
title: Microservice Starter
subtitle: Enterprise Microservice Starter Kit & Template Specification
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Starter Kit
parent_document: NES-1307 Design System Starter
next_document: NES-1309 Event-Driven Starter
---

# NES-1308 — Microservice Starter

> **"Microservices must be lightweight and standardized. This starter kit provides a production-ready template built on FastAPI, Docker multi-stage builds, and Prometheus."**

---

# Executive Summary

To help backend developer teams launch new microservices quickly while maintaining architectural alignment, performance metrics, and security compliance, the Platform Team provides the **Microservice Starter Kit**.

This starter kit contains a pre-configured template containing API endpoints, database connection pools, health probes, Docker compile scripts, and observability metrics.

This document establishes the repository structure, approved tech stack, quick start guide, and verification steps for the Microservice Starter template.

---

# Purpose

This standard defines:

- Microservice Starter Repository Directory Structure
- Pre-Configured Tech Stack
- Quick Start Guide for Developers
- Pre-Integrated Security and CI/CD Gates

---

# Repository Directory Structure

The Microservice Starter repository utilizes a clean directory structure separating configurations, routes, and business logic:

```text
microservice-starter/
├── config/                # Environment variables and system configurations
├── src/
│   ├── api/               # API routers and endpoints
│   ├── core/              # Business logic and services
│   └── models/            # Database schemas and schemas schemas
│
├── .github/
│   └── workflows/         # CI/CD pipelines
├── Dockerfile             # Multi-stage container compilation
└── README.md
```

---

# Pre-Configured Tech Stack

The template includes our approved technology stack configured for production:

- **Language**: Python 3.13.
- **Framework**: FastAPI.
- **Database**: PostgreSQL (SQLAlchemy ORM).
- **Observability**: Prometheus metrics client, Vector log formatting.
- **Testing**: pytest.

---

# Quick Start Guide

Developers can spin up the local development sandbox inside 2 minutes:

1. **Clone Template**: Create a new repository using the Microservice Starter template.
2. **Environment Variables**: Copy `.env.example` to `.env` in the root folder.
3. **Spin Up Docker**: Run the docker-compose command to launch PostgreSQL:
   ```bash
   docker-compose up -d
   ```
4. **Install Dependencies**: Run package installations:
   ```bash
   poetry install
   ```
5. **Run Service**: Start the FastAPI server locally:
   ```bash
   poetry run uvicorn main:app --reload
   ```

---

# Pre-Integrated Security & CI/CD Gates

The template includes built-in security features to prevent vulnerability leakage:

- **Liveness Probes**: Configured endpoints (`/healthz`, `/ready`) matching Kubernetes deployment specs.
- **Secrets Injection**: Integrated with External Secrets Operator (ESO) specs to fetch vault credentials.
- **Trivy Image Scan**: Blocks CI docker compiles containing critical vulnerabilities.

---

# Anti-Patterns

❌ **Hardcoded Database Connections**: Setting production database configurations inside repository files instead of utilizing env parameters.

❌ **Exposing Debug Endpoints**: Leaving Swagger UI endpoints accessible in production namespaces.

❌ **Omitting API Rate Limiting**: Deploying public endpoints without rate limits, risking denial-of-service outages.

---

# Production Checklist

- [ ] Template repository clone completes cleanly.
- [ ] Local database connection tests succeed.
- [ ] API health endpoints return valid response codes.
- [ ] CI pipeline linting and unit tests pass.
- [ ] Container compile size fits within 150MB limits.

---

# Success Criteria

The Microservice Starter template is successful when:
- Teams can spin up a new microservice backend in less than 5 minutes.
- Deployed containers boot up and registers health status in EKS namespaces.
- Average endpoint response times remain under 200ms in load tests.

---

# Document Status

**Document:** NES-1308 — Microservice Starter
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1309 — Event-Driven Starter**
