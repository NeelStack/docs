---
document_id: NES-1304
title: Healthcare Starter
subtitle: Enterprise Healthcare Starter Kit & Template Specification
version: 1.0.0
status: Draft
classification: Internal
owner: Healthcare Platforms Group
review_cycle: Every 6 Months
document_type: Starter Kit
parent_document: NES-1303 CRM Starter
next_document: NES-1305 Mobile Starter
---

# NES-1304 — Healthcare Starter

> **"Patient data security requires strict architecture. This starter kit provides a production-ready healthcare template built on HIPAA safeguards, PHI encryption, and WORM logging."**

---

# Executive Summary

To help developer teams launch new healthcare platform features (DhruvaOS) quickly while maintaining regulatory compliance (HIPAA/SOC2) and data security, we provide the **Healthcare Starter Kit**.

This starter kit contains a pre-configured template containing Protected Health Information (PHI) encryption, multi-AZ databases, access logging, and container security settings out-of-the-box.

This document establishes the repository structure, approved tech stack, quick start guide, and verification steps for the Healthcare Starter template.

---

# Purpose

This standard defines:

- Healthcare Starter Repository Directory Structure
- Pre-Configured Tech Stack
- Quick Start Guide for Developers
- Pre-Integrated Security and CI/CD Gates

---

# Repository Directory Structure

The Healthcare Starter repository utilizes a monorepo structure separating frontend, backend, and platform tooling:

```text
healthcare-starter/
├── apps/
│   ├── portal/            # Next.js Clinical Portal (React, Tailwind)
│   └── api/               # FastAPI Medical Backend (Python)
│
├── packages/
│   ├── phi-vault/         # Column-level envelope encryption configs
│   └── database/          # PostgreSQL KMS encrypted DB connection pool configs
│
├── .github/
│   └── workflows/         # GitHub Actions CI/CD pipelines
│
├── terraform/             # IaC configurations (AWS, EKS, KMS)
└── README.md
```

---

# Pre-Configured Tech Stack

The template includes our approved technology stack configured for production:

- **Frontend**: Next.js (App Router), Zod (Validation), Tailwind CSS, TanStack Query.
- **Backend**: FastAPI (Python 3.13), cryptography (Envelope Encryption helpers), pytest.
- **Database**: PostgreSQL (KMS encrypted, Multi-AZ), Redis (encrypted sessions).
- **Platform**: Dockerfiles (hardened Bottlerocket base configs), AWS S3 (Object Lock configurations).

---

# Quick Start Guide

Developers can spin up the local development sandbox inside 2 minutes:

1. **Clone Template**: Create a new repository using the Healthcare Starter template.
2. **Environment Variables**: Copy `.env.example` to `.env` inside `apps/portal` and `apps/api`.
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
   cd apps/portal
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

❌ **Plaintext PHI in Log Streams**: Printing patient names, phone numbers, or prescriptions inside standard console logs.

❌ **Exposing Diagnostic APIs to Public Networks**: Exposing internal patient database APIs directly on public endpoints without strict mTLS boundaries.

❌ **Shared Dev-Prod Datastores**: Connecting developer test instances to databases containing real patient files.

---

# Production Checklist

- [ ] Template repository clone completes cleanly.
- [ ] Local database migrations run successfully.
- [ ] Frontend page loads and queries backend APIs.
- [ ] CI pipeline linting and unit tests pass.
- [ ] Multi-stage Docker compiles complete under size limits.

---

# Success Criteria

The Healthcare Starter template is successful when:
- Teams can spin up a new feature environment in less than 5 minutes.
- The template codebase passes security scans with zero active issues.
- Deployed containers conform to platform engineering standards.

---

# Document Status

**Document:** NES-1304 — Healthcare Starter
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1305 — Mobile Starter**
