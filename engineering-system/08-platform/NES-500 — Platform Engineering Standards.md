---
document_id: NES-500
title: Platform Engineering Standards
subtitle: Enterprise Platform Engineering, IDP & Golden Paths Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-416 Mobile Reference Architecture
next_document: NES-501 Docker
---

# NES-500 — Platform Engineering Standards

> **"Platform engineering is about reducing cognitive load. We build self-service platforms and golden paths to enable developers to ship code securely and rapidly."**

---

# Executive Summary

As engineering organizations grow, the complexity of managing cloud infrastructure, deployment pipelines, configuration parameters, and monitoring environments increases exponentially.

Forces developers to spend significant time on operational tasks, diverting them from writing core product logic.

Platform Engineering solves this by creating an **Internal Developer Platform (IDP)** that bundles infrastructure operations into type-safe, self-service configurations.

This document establishes the platform standards, principles of self-service, and the creation of **Golden Paths** for the NeelStack developer ecosystem.

---

# Purpose

This standard defines:

- Platform Engineering Principles
- Internal Developer Platform (IDP) Architecture
- Golden Paths and Templates
- Developer Cognitive Load Budgets
- Infrastructure Self-Service Standards

---

# Platform Engineering Principles

Our platform engineering decisions are guided by five core principles:

✓ **Product Mindset**: Treat the platform as a product and developers as our customers. Conduct user research and track Developer Net Promoter Score (DevNPS).

✓ **Cognitive Load Reduction**: Shield developers from low-level Kubernetes, network, and IAM policies unless they explicitly require custom configs.

✓ **Golden Paths over Golden Cages**: Build default, automated, and pre-paved pathways (Golden Paths) for building, testing, and deploying apps, while allowing advanced users to diverge if justified.

✓ **Self-Service**: Enable developers to provision databases, APIs, queues, and workspaces on-demand without writing ticket requests to DevOps.

✓ **Shift-Left Security & Compliance**: Embed security scans, policy checks, and cost limits automatically inside the platform templates.

---

# Internal Developer Platform (IDP)

The NeelStack IDP is a unified platform consisting of five layers:

```text
 ┌───────────────────────────────────────────────┐
 │   Portal Layer (Backstage Dashboard/CLI)     │
 ├───────────────────────────────────────────────┤
 │  Configuration Layer (Score / YAML Templates) │
 ├───────────────────────────────────────────────┤
 │   Orchestration Layer (Terraform / GitOps)    │
 ├───────────────────────────────────────────────┤
 │    Infrastructure Layer (AWS / EKS / RDS)     │
 └───────────────────────────────────────────────┘
```

Every service created on the platform must be registered in the central developer catalog.

---

# Golden Paths & Project Templates

A **Golden Path** is the recommended, fully automated pathway for shipping software. We provide official starter templates for:

- Python FastAPI microservices (NES-201)
- Next.js web applications (NES-302)
- React Native mobile apps (NES-400)
- AI agent models (NES-219)

### Platform Template Standard:
Every official template must pre-integrate:
- Local development configs (Docker, local databases)
- CI pipeline configurations (linting, tests, build checking)
- OpenTelemetry hooks (automatic trace forwarding)
- Secure Dockerfile templates matching container standards (NES-501)

---

# Developer Cognitive Load Budget

Platform team must design toolchains that keep developer cognitive load low.

- **The 10-Minute Target**: A newly onboarded engineer must be able to spin up their local environment and submit their first pull request in less than 10 minutes.
- **Single-Configuration Deployment**: A developer should only need to maintain a single configuration metadata file (e.g. `score.yaml` or a simple app config) to control their application environment, database provisioning, and DNS routing.

---

# Infrastructure Self-Service

Provisioning cloud resources must be fully automated.

- **No Tickets**: Avoid Slack or ticket-based provisioning for dev/staging environments.
- **Standard**: Developers define their infrastructure dependencies declaratively in their repository (e.g., requesting a PostgreSQL database). The IDP orchestrator intercepts this declaration during deployment and provisions the matching cloud resource (e.g. AWS RDS) using Terraform in the background.

---

# Anti-Patterns

❌ **Building Golden Cages**: Forcing strict tools on developers without allowing flexibility. If a team needs a custom database (e.g. Neo4j graph db), the platform should facilitate it rather than blocking it.

❌ **Ticket-Driven Operations**: Maintaining a platform team that functions as a manual operations desk (e.g. "Create ticket to get a new DB").

❌ **Undefined Ownership**: Building platform tools without active product ownership, leading to outdated dashboards, broken scripts, and poor documentation.

---

# Production Checklist

- [ ] DevNPS telemetry monitoring is established.
- [ ] Golden Path templates are maintained and verified against latest library versions.
- [ ] Backstage Catalog has complete metadata registration for all production apps.
- [ ] Auto-provisioning resource limit checks are configured.
- [ ] Onboarding guides are verified.

---

# Success Criteria

The Platform Engineering standard is successful when:
- Average deployment lead time (commit to production) is reduced to less than 15 minutes.
- More than 90% of active projects utilize official Golden Path templates.
- Infrastructure provisioning time is reduced from days to minutes.
- Developers report low friction and high satisfaction levels in quarterly DevNPS surveys.

---

# Document Status

**Document:** NES-500 — Platform Engineering Standards
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-501 — Docker**
