---
document_id: NES-1306
title: Admin Starter
subtitle: Enterprise Admin Dashboard Starter Kit & Template Specification
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Starter Kit
parent_document: NES-1305 Mobile Starter
next_document: NES-1307 Design System Starter
---

# NES-1306 — Admin Starter

> **"Secure administration consoles start with standards. This starter kit provides a production-ready Admin console built on Next.js, tailwind theme tokens, and Entra ID SSO."**

---

# Executive Summary

To help developer teams launch new admin features, portal consoles, customer support dashboards, and reporting tables quickly while maintaining security permissions (RBAC) and layout design consistency, we provide the **Admin Starter Kit**.

This starter kit contains a pre-configured template containing corporate SSO logons, dashboard metrics layouts, searchable table modules, and audit-logged operations out-of-the-box.

This document establishes the repository structure, approved tech stack, quick start guide, and verification steps for the Admin Starter template.

---

# Purpose

This standard defines:

- Admin Starter Repository Directory Structure
- Pre-Configured Tech Stack
- Quick Start Guide for Developers
- Pre-Integrated Security and CI/CD Gates

---

# Repository Directory Structure

The Admin Starter repository utilizes a clean Next.js monorepo structure:

```text
admin-starter/
├── app/
│   ├── (auth)/            # SSO login and redirect routes
│   ├── (dashboard)/       # Admin metric dashboards and console layout
│   │   ├── users/         # User management tables
│   │   └── settings/      # System parameters controls
│
├── components/            # Reusable UI dashboard elements (charts, tables)
├── hooks/                 # Custom state and API hook query files
├── .github/
│   └── workflows/         # CI/CD pipelines
├── tailwind.config.js     # Admin dashboard color theme config
└── README.md
```

---

# Pre-Configured Tech Stack

The template includes our approved technology stack configured for production:

- **Framework**: Next.js (App Router), React.
- **Styling**: Tailwind CSS, Lucide icons.
- **State Management**: TanStack Query v5.
- **Authentication**: NextAuth.js configured with Microsoft Entra ID (OIDC) SSO provider.
- **Charts**: Recharts.

---

# Quick Start Guide

Developers can spin up the local development sandbox inside 2 minutes:

1. **Clone Template**: Create a new repository using the Admin Starter template.
2. **Environment Variables**: Copy `.env.example` to `.env` in the root folder.
3. **Install Dependencies**: Run package installations:
   ```bash
   npm install
   ```
4. **Start Development Server**: Launch Next.js local server:
   ```bash
   npm run dev
   ```
5. **Open Browser**: Route browser connections to `http://localhost:3000` to verify page loads.

---

# Pre-Integrated Security & CI/CD Gates

The template includes built-in security features to prevent vulnerability leakage:

- **Entra ID SSO**: Out-of-the-box integration for corporate directory logons.
- **Role-Based Routing**: Middleware constraints pre-configured to block users without administrative access flags.
- **Audit Logs**: Automatically generates audit logs for all data modification clicks (NES-610).

---

# Anti-Patterns

❌ **Hardcoded Admin Credentials**: Setting local development passwords (e.g., `admin/admin`) inside code files.

❌ **Exposing Client Data on Public Paths**: Fetching metrics or patient files without verifying token permissions in server components.

❌ **Bypassing Ingress Security**: Allowing admin portals to run on public subdomains without IP whitelisting.

---

# Production Checklist

- [ ] Template repository clone completes cleanly.
- [ ] Local Next.js development server runs successfully.
- [ ] Entra ID OIDC configurations are mapped.
- [ ] Role-based access rules block non-admin logins.
- [ ] CI pipeline checks pass cleanly.

---

# Success Criteria

The Admin Starter template is successful when:
- Teams can spin up a new admin table in less than 5 minutes.
- The template codebase passes local Jest unit checks with zero failures.
- System metrics demonstrate page render speeds under 1.5 seconds.

---

# Document Status

**Document:** NES-1306 — Admin Starter
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1307 — Design System Starter**
