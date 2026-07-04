---
document_id: NES-1303
title: CRM Starter
subtitle: Enterprise CRM Starter Kit & Template Specification
version: 1.0.0
status: Draft
classification: Internal
owner: Enterprise Platforms Board
review_cycle: Every 6 Months
document_type: Starter Kit
parent_document: NES-1302 ERP Starter
next_document: NES-1304 Healthcare Starter
---

# NES-1303 — CRM Starter

> **"Customer data integration requires structured code. This starter kit provides a production-ready CRM template built on FastAPI, OpenSearch, and Redis."**

---

# Executive Summary

To help developer teams launch new CRM features quickly while maintaining data integration and query performance, we provide the **CRM Starter Kit**.

This starter kit contains a pre-configured template containing contact history management, sync connector APIs, user activity logs, and OpenSearch search indexes out-of-the-box.

This document establishes the repository structure, approved tech stack, quick start guide, and verification steps for the CRM Starter template.

---

# Purpose

This standard defines:

- CRM Starter Repository Directory Structure
- Pre-Configured Tech Stack
- Quick Start Guide for Developers
- Pre-Integrated Security and CI/CD Gates

---

# Repository Directory Structure

The CRM Starter repository utilizes a monorepo structure separating frontend, backend, and platform tooling:

```text
crm-starter/
├── apps/
│   ├── console/           # Next.js CRM UI (React, Tailwind)
│   └── api/               # FastAPI Contact Backend (Python)
│
├── packages/
│   ├── contacts/          # Contact details schemas & migration configs
│   └── database/          # PostgreSQL & OpenSearch connection configurations
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
- **Backend**: FastAPI (Python 3.13), OpenSearch Py client, SQLAlchemy ORM, pytest.
- **Database**: PostgreSQL, OpenSearch, Redis.
- **Platform**: Dockerfiles (multi-stage, non-root), Terraform configurations, GitHub Actions pipelines.

---

# Quick Start Guide

Developers can spin up the local development sandbox inside 2 minutes:

1. **Clone Template**: Create a new repository using the CRM Starter template.
2. **Environment Variables**: Copy `.env.example` to `.env` inside `apps/console` and `apps/api`.
3. **Spin Up Docker**: Run the docker-compose command to launch PostgreSQL, OpenSearch, and Redis containers locally:
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
   cd apps/console
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

❌ **Hardcoded API Sync Scripts**: Writing custom cron scripts that write to databases directly without schema validation or duplicate entry checks.

❌ **Exposing Client Contact PII**: Exposing customer emails, phone numbers, or notes to un-authorized roles without masking filters (NES-710).

❌ **Slow Table-Scan Queries**: Querying name searches directly on raw PostgreSQL tables using wildcard `LIKE` operators, causing table locks.

---

# Production Checklist

- [ ] Template repository clone completes cleanly.
- [ ] Local database migrations run successfully.
- [ ] Frontend page loads and queries backend APIs.
- [ ] CI pipeline linting and unit tests pass.
- [ ] Multi-stage Docker compiles complete under size limits.

---

# Success Criteria

The CRM Starter template is successful when:
- Teams can spin up a new feature environment in less than 5 minutes.
- The template codebase passes security scans with zero active issues.
- Deployed containers conform to platform engineering standards.

---

# Document Status

**Document:** NES-1303 — CRM Starter
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1304 — Healthcare Starter**
