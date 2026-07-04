---
document_id: NES-602
title: Threat Modeling
subtitle: Enterprise STRIDE Threat Assessment & Trust Boundary Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Security Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-601 OWASP Security Standards
next_document: NES-603 Zero Trust Architecture
---

# NES-602 — Threat Modeling

> **"If we do not catalog threats, we cannot defend against them. We map boundaries and model attack vectors before writing system code."**

---

# Executive Summary

Designing software without modeling potential threats leads to architectural security flaws.

These are difficult to fix once code is implemented and deployed.

We mandate the execution of **Threat Modeling** during the design phase of all major features, microservices, and network integrations at NeelStack.

This standard establishes the threat assessment process, the STRIDE methodology, trust boundary mapping, and risk categorization rules.

---

# Purpose

This standard defines:

- Threat Modeling Timelines
- The STRIDE Methodology
- Data Flow Diagrams (DFDs) & Trust Boundaries
- Risk Scoring and Prioritization (DREAD / CVSS)
- Mitigation Verification Rules

---

# Threat Modeling Lifecycle

Threat modeling occurs during the **design phase** (NES-600) before backend database tables or ingress API endpoints are provisioned.

- **Trigger**: Required when creating a new application, adding an integration endpoint, shifting authentication architectures, or exposing internal data stores.
- **Artifact**: The resulting Threat Model Document must be versioned and checked into the service repository under `docs/security/threat_model.md`.

---

# The STRIDE Methodology

We use the **STRIDE** model to analyze threats systematically:

| Threat | Definition | Mitigation Standard |
|---|---|---|
| **Spoofing** | Pretending to be someone else. | Enforce strong authentication, OIDC tokens, and certificate checks. |
| **Tampering** | Modifying data on disk or in transit. | Enforce SSL pinning, data signatures, and read-only databases. |
| **Repudiation** | Claiming you did not perform an action. | Maintain immutable audit trails (SIEM), sign log hashes. |
| **Information Leak** | Exposing sensitive data. | Encrypt data at rest (TDE), use CORS, enforce transit encryption. |
| **Denial of Service** | Exhausting resources to block users. | Rate limiting, auto-scaling clusters, Cloudflare WAF filters. |
| **Elevation of Priv** | Gaining unauthorized access levels. | Enforce RBAC/ABAC check rules, run rootless containers. |

---

# Trust Boundaries & Data Flow Diagrams

A threat model requires a detailed **Data Flow Diagram (DFD)** mapping how information crosses **Trust Boundaries**.

- **Trust Boundary**: A boundary representing a shift in trust or privilege level (e.g. between a web browser and an ALB, or between a container pod and a database).
- **DFD Rules**: Every connection crossing a boundary must be explicitly identified, listing the protocols, encryption levels, and authentication methods.

```text
  [ Client Web App ]
         │ (HTTP Session Cookie) ──► Public Boundary
         ▼
  [ Istio Ingress Gateway ]
         │ (mTLS strict) ──► Pod Namespace Boundary
         ▼
  [ Backend Portal Service ]
         │ (IAM Role authentication) ──► Data Subnet Boundary
         ▼
  [ Amazon RDS Database ]
```

---

# Risk Scoring and Prioritization

Not all threats present the same level of risk. We calculate threat priority using a simplified **CVSS (Common Vulnerability Scoring System)** metrics model based on two vectors:

```text
Risk Score = Likelihood × Impact
```

- **Likelihood**: Ease of exploit, presence of default access points, lack of authentication gates.
- **Impact**: Level of data loss, operational disruption, compliance violation.
- **Mitigation Requirement**:
  - **High Risk (Score 7-10)**: Deployment blocker. Must be mitigated prior to code merge.
  - **Medium Risk (Score 4-6)**: Must be remediated within 30 days of release.
  - **Low Risk (Score 1-3)**: Documented with formal risk acceptance.

---

# Anti-Patterns

❌ **Retrospective Threat Modeling**: Writing the threat model post-deployment to satisfy compliance logs, which fails to catch design flaws during development.

❌ **Omitting Trust Boundaries**: Mapping data flow diagrams that assume everything inside the cloud network is universally trusted, violating Zero Trust principles.

❌ **Vague Threats**: Stating threats like "Hacker breaks system" without defining the specific input vector, affected service, or target data.

---

# Production Checklist

- [ ] Data Flow Diagram with defined Trust Boundaries is complete.
- [ ] STRIDE analysis has been executed for all crossed boundaries.
- [ ] Risk scores are calculated for all identified threats.
- [ ] Mitigations are linked to actionable ticketing items.
- [ ] Threat model is signed off by the Security Architect.

---

# Success Criteria

The Threat Modeling process is successful when:
- 100% of new microservice designs have a logged threat model file.
- Architecture design reviews catch and remediate logical access flaws before code is written.
- Game day audits show no exploits succeeding via threat vectors that were marked as "Mitigated."

---

# Document Status

**Document:** NES-602 — Threat Modeling
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-603 — Zero Trust Architecture**
