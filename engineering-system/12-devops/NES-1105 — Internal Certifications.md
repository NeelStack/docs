---
document_id: NES-1105
title: Internal Certifications
subtitle: Enterprise Engineering Accreditations, Badges & Training Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Governance Board
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-1104 Capability Maturity
next_document: NES-1106 Engineering Career Ladder
---

# NES-1105 — Internal Certifications

> **"Training validates expertise. We run internal certification pathways to accredit developers on our core architectures, security gates, and deployment systems."**

---

# Executive Summary

In a complex, regulated enterprise software platform, expecting new developers to understand backend architectures, security protocols, or deployment systems without training can lead to system misconfigurations.

We mandate the establishment of **Internal Engineering Certifications** across all developer teams.

This standard establishes our accreditation courses, architectural badges, security gates training, and onboarding paths.

---

# Purpose

This standard defines:

- Internal Certification Pathways
- Architecture and Security Badges
- Developer Onboarding Training Requirements
- Certification Verification Systems
- Continuous Learning Credits

---

# Certification Pathways

We structure our training courses into three specialization tracks:

- **SaaS Architecture Specialist**: Validates knowledge in DDD, modular monoliths, multi-tenant databases, and APIs.
- **Platform & Security Engineer**: Focuses on Docker, Kubernetes, Terraform, IAM, secrets, and vault management (NES-514).
- **Frontend & Mobile Developer**: Covers Next.js, Expo, NativeWind, state management, and mobile release pipelines.

---

# Core Security Badging (Secure Developer)

To ensure all developers follow secure coding practices:

- **Mandatory Badge**: All engineers must pass the **Secure Developer Certification** annually.
- **Course Scope**: Covers OWASP Top 10 mitigations, input validations, secrets hygiene, threat modeling, and regulatory compliance (SOC2/GDPR).
- **Pipeline Check**: Engineers without active security badges are blocked from merging code changes to production configuration branches.

```text
  Developer Profile
        │
        ▼
  Complete Annual Security Training Course
        │
        ▼
  Pass Certification Exam (Score > 85%)
        │
        ▼
  Deploy Permission Active in JIRA/GitHub
```

---

# Developer Onboarding Path

Onboarding new engineers requires structured validation:

- **First 30 Days**: Complete baseline courses in architecture, Git workflows, and coding standards.
- **Onboarding Sandbox Project**: Build and deploy a simple mock service to a staging preview namespace using approved starter kits, demonstrating mastery of deployment pipelines.

---

# Certifications Directory

Maintain a secure, searchable directory of engineering accreditations:

- **Training Portal**: Host training videos, sample code, and exam sheets on our internal developer platform.
- **SSO Integration**: Automatically map developer certification statuses to Entra ID profile attributes to authorize environment write permissions.

---

# Anti-Patterns

❌ **Skip-on-Onboarding**: Throwing new developers straight into production tasks without validating their understanding of architecture and security gates.

❌ **Static Certifications**: Certifying developers once and never requiring re-certification, allowing knowledge to decay as technologies evolve.

❌ **Excluding Contractor Teams**: Permitting third-party contractors to write production code without verifying they have completed security certifications.

---

# Production Checklist

- [ ] Training portal is active with baseline courses.
- [ ] Secure Developer exam questions are verified.
- [ ] Onboarding sandbox environments are configured.
- [ ] Developer certification statuses are integrated with Entra ID.
- [ ] Annual re-certification schedules are active.

---

# Success Criteria

The Internal Certifications program is successful when:
- 100% of active developers hold the Secure Developer badge.
- Onboarding developers successfully deploy sandbox projects within 30 days.
- Outages caused by developer misconfigurations are minimized.

---

# Document Status

**Document:** NES-1105 — Internal Certifications
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1106 — Engineering Career Ladder**
