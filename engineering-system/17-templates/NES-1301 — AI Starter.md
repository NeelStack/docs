---
document_id: NES-1301
title: AI Starter
subtitle: Enterprise AI & LLM Inference Starter Kit & Template Specification
version: 1.0.0
status: Draft
classification: Internal
owner: AI & Data Science Board
review_cycle: Every 6 Months
document_type: Starter Kit
parent_document: NES-1300 SaaS Starter
next_document: NES-1302 ERP Starter
---

# NES-1301 — AI Starter

> **"Accelerate AI features with pre-configured inference. This starter kit provides a production-ready repository built on PyTorch, vLLM, pgvector, and FastAPI."**

---

# Executive Summary

To help data scientists and developers build and deploy Large Language Models (LLMs), RAG pipelines, and custom AI agents quickly while maintaining architectural alignment and security compliance, we provide the **AI Starter Kit**.

This starter kit contains a pre-configured template containing model routing, vector search, embedding generations, and inference serving out-of-the-box.

This document establishes the repository structure, approved tech stack, quick start guide, and verification steps for the AI Starter template.

---

# Purpose

This standard defines:

- AI Starter Repository Directory Structure
- Pre-Configured Tech Stack
- Quick Start Guide for Developers
- Pre-Integrated Security and CI/CD Gates

---

# Repository Directory Structure

The AI Starter repository utilizes a monorepo structure separating frontend, backend, and platform tooling:

```text
ai-starter/
├── apps/
│   ├── ui/                # Next.js Chat Frontend (React, Tailwind)
│   └── inference-api/     # FastAPI Model Serving Backend (Python)
│
├── packages/
│   ├── vector-store/      # pgvector schema & migration configurations
│   └── models/            # Quantized embedding models configurations
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
- **Backend**: FastAPI (Python 3.13), vLLM / Triton Server configs, pgvector, Qdrant SDK.
- **Database**: PostgreSQL (with pgvector extension), Qdrant.
- **Platform**: Dockerfiles (multi-stage, non-root), GPU configurations, GitHub Actions pipelines.

---

# Quick Start Guide

Developers can spin up the local development sandbox inside 2 minutes:

1. **Clone Template**: Create a new repository using the AI Starter template.
2. **Environment Variables**: Copy `.env.example` to `.env` inside `apps/ui` and `apps/inference-api`.
3. **Spin Up Docker**: Run the docker-compose command to launch PostgreSQL and Qdrant containers locally:
   ```bash
   docker-compose up -d
   ```
4. **Run Backend**: Initialize virtual environments, apply database migrations, and start the FastAPI server:
   ```bash
   cd apps/inference-api
   poetry install
   poetry run alembic upgrade head
   poetry run uvicorn main:app --reload
   ```
5. **Run Frontend**: Install node packages and start the Next.js development server:
   ```bash
   cd apps/ui
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

❌ **Hardcoding API Keys in Clients**: Storing external AI model API keys inside web frontend code, exposing keys to attackers.

❌ **Exposing GPU Nodes Directly**: Direct routing to Triton/vLLM backend ports, bypassing the AI Gateway rate limiter.

❌ **Omitting Token Caching**: Querying external APIs for identical, repetitive queries, causing high monthly cloud bills.

---

# Production Checklist

- [ ] Template repository clone completes cleanly.
- [ ] Local database migrations run successfully.
- [ ] Frontend page loads and queries backend APIs.
- [ ] CI pipeline linting and unit tests pass.
- [ ] Multi-stage Docker compiles complete under size limits.

---

# Success Criteria

The AI Starter template is successful when:
- Teams can spin up a new feature environment in less than 5 minutes.
- The template codebase passes security scans with zero active issues.
- Deployed containers conform to platform engineering standards.

---

# Document Status

**Document:** NES-1301 — AI Starter
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1302 — ERP Starter**
