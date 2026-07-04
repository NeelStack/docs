---
document_id: NES-600
title: Secure SDLC
subtitle: Enterprise Secure Software Development Lifecycle & Security Gates Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Security Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-520 Platform Reference Architecture
next_document: NES-601 OWASP Security Standards
---

# NES-600 — Secure SDLC

> **"Security is built-in, not bolted-on. We inject security requirements at every phase of the software development lifecycle."**

---

# Executive Summary

Waiting until software is fully built before conducting a security review is a failed operational model.

Remediating security vulnerabilities post-release is slow, expensive, and risks exposing active production data.

We mandate the adoption of a **Secure Software Development Lifecycle (Secure SDLC)** across all NeelStack products.

This standard defines the security gates, code scanning requirements, threat assessment timelines, and verification criteria that code must satisfy before merge and release.

---

# Purpose

This standard defines:

- Secure SDLC Phases and Gates
- Static Application Security Testing (SAST)
- Software Composition Analysis (SCA)
- Secret Scanning gates
- Security Approval Workflows

---

# Secure SDLC Phases & Security Gates

Our development pipeline injects security criteria into every phase:

```text
 Requirements  ──►  Design  ──►  Development  ──►  Testing  ──►  Deployment
      │               │               │               │               │
  Security         Threat           SAST /          DAST /          Secure
  Training        Modeling        Dependency       Pen Test         Config
```

No code can bypass a phase gating check without manual override authorization from the Security Board.

---

# Design Gate: Threat Modeling

Before writing any code for a major feature or new microservice:

- **Mandatory Threat Model**: Developers must document a STRIDE threat model (NES-602) identifying data flows, trust boundaries, and potential attack vectors.
- **Security Review**: The security architecture team must review and sign off on the design before work tickets are committed to sprint queues.

---

# Development Gate: Automated Code Scans

The CI/CD pipeline executes three categories of automated security scans on every pull request:

### 1. Static Application Security Testing (SAST)
- **Tooling**: Use Semgrep or SonarQube.
- **Rule**: Catch code-level errors (e.g. SQL injections, hardcoded keys, insecure random generators) automatically.

### 2. Software Composition Analysis (SCA)
- **Tooling**: Use Snyk or npm audit / pip audit.
- **Rule**: Scan third-party packages for known CVEs. Block builds with active critical CVEs.

### 3. Secret Scanning
- **Tooling**: Use GitGuardian or TruffleHog.
- **Rule**: Detect credentials (AWS keys, database passwords, JWT tokens) in commits. Block PR merges if a secret is found.

---

# Testing Gate: Dynamic Auditing (DAST)

Prior to releasing staging packages to public channels:

- **Dynamic Application Security Testing (DAST)**: Run automated vulnerability crawlers (e.g., OWASP ZAP) against staging API endpoints to identify runtime injection flaws, broken authentication cookies, or transport security errors.
- **Penetration Testing**: Enforce a full-scale external third-party penetration test at least **once per year** for all core web and mobile platforms.

---

# Deployment Gate: Compliance Sign-off

Before promoting any release branch to production:

- [ ] All SAST, SCA, and secret scan runs pass with zero critical issues.
- [ ] DAST runs report no active session vulnerability alerts.
- [ ] Docker container security scans (Trivy) pass cleanly.
- [ ] Infrastructure modifications are declared in Terraform modules and verified.
- [ ] Platform Security Team signs off on the release manifest.

---

# Anti-Patterns

❌ **Bypassing Scans for "Hotfixes"**: Disabling GitHub Action security checks to force emergency patches into production.

❌ **Scanning Only in Production**: Running vulnerability scans only against active production environments, exposing customers to risks during the gap.

❌ **Ignoring Deprecated Package Flags**: Overriding dependency warnings to use outdated, vulnerable modules because updating them "takes too much time."

---

# Success Criteria

The Secure SDLC program is successful when:
- 100% of production code releases pass automated security scans.
- Critical vulnerabilities are identified and remediated in the design or code phase before compilation.
- The average time to resolve a discovered code vulnerability is reduced.

---

# Document Status

**Document:** NES-600 — Secure SDLC
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-601 — OWASP Security Standards**
