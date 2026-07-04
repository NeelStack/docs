---
document_id: NES-1300
title: SaaS Starter
subtitle: Enterprise SaaS Starter Kit & Template Specification
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Starter Kit
parent_document: NES-1210 Enterprise Blueprint
next_document: NES-1301 AI Starter
---

# NES-1300 — SaaS Starter

> **"Accelerate development with pre-configured templates. This starter kit provides a production-ready SaaS repository built on Next.js, FastAPI, and Postgres."**

---

# Executive Summary

To help developer teams launch new SaaS features quickly while maintaining architectural alignment, code quality, and security compliance, the Platform Team provides the **SaaS Starter Kit**.

This starter kit contains a pre-configured, audited codebase template containing authentication, multi-tenant databases, API routing, design systems, and CI/CD pipelines out-of-the-box.

This document establishes the repository structure, approved tech stack, quick start guide, and verification steps for the SaaS Starter template.

---

# Purpose

This standard defines:

- SaaS Starter Repository Directory Structure
- Pre-Configured Tech Stack
- Quick Start Guide for Developers
- Pre-Integrated Security and CI/CD Gates

---

# Repository Directory Structure

The SaaS Starter repository utilizes a monorepo structure separating frontend, backend, and platform tooling:

```text
saas-starter/
├── apps/
│   ├── web/               # Next.js Frontend (React, Tailwind)
│   └── api/               # FastAPI Backend (Python)
│
├── packages/
│   ├── design-system/     # Shared UI components library
│   └── database/          # SQL database schemas & migrations
│
├── .github/
│   └── workflows/         # GitHub Actions CI/CD pipelines
│
├── terraform/             # IaC configurations (AWS, EKS)
└── README.md
```

---

# Pre-Configured Tech Stack

The template includes our approved technology stack configured for production:

- **Frontend**: Next.js (App Router), Zod (Validation), Tailwind CSS, TanStack Query.
- **Backend**: FastAPI (Python 3.13), SQLAlchemy ORM, Pydantic, pytest.
- **Database**: PostgreSQL (with migration configurations using Alembic), Redis.
- **Platform**: Dockerfiles (multi-stage, non-root), Terraform configurations, GitHub Actions pipelines.

---

# Quick Start Guide

Developers can spin up the local development sandbox inside 2 minutes:

1. **Clone Template**: Create a new repository using the SaaS Starter template.
2. **Environment Variables**: Copy `.env.example` to `.env` inside `apps/web` and `apps/api`.
3. **Spin Up Docker**: Run the docker-compose command to launch PostgreSQL and Redis containers locally:
   ```bash
   docker-compose up -d
   ```
4. **Run Backend**: Initialize virtual environments, apply database migrations, and start the FastAPI server:
   ```bash
   cd apps/api
   poetry install
   poetry run alembic upgrade head
   poetry run uvicorn main:app --reload
   ```
5. **Run Frontend**: Install node packages and start the Next.js development server:
   ```bash
   cd apps/web
   npm install
   npm run dev
   ```

---

# Pre-Integrated Security & CI/CD Gates

The template includes built-in security features to prevent vulnerability leakage:

- **GitLeaks Hook**: Blocks commits containing keys or tokens.
- **Trivy Image Scan**: Blocks CI docker compiles containing critical vulnerabilities.
- **Strict mTLS Configuration**: App containers are ready to run inside the Istio service mesh out-of-the-box.

---

# Anti-Patterns

❌ **Hardcoding Custom DB Connections**: Modifying SQLAlchemy files to use custom connection strings instead of environment variables.

❌ **Bypassing Alembic Migrations**: Writing raw SQL commands directly to database instances locally without documenting migrations.

❌ **Omitting Unit Tests in New Modules**: Adding new API endpoints without writing corresponding Pytest checks.

---

# Production Checklist

- [ ] Template repository clone completes cleanly.
- [ ] Local database migrations run successfully.
- [ ] Frontend page loads and queries backend APIs.
- [ ] CI pipeline linting and unit tests pass.
- [ ] Multi-stage Docker compiles complete under size limits.

---

# Success Criteria

The SaaS Starter template is successful when:
- Teams can spin up a new feature environment in less than 5 minutes.
- The template codebase passes security scans with zero active issues.
- Deployed containers conform to platform engineering standards.

---

# Document Status

**Document:** NES-1300 — SaaS Starter
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1301 — AI Starter**
