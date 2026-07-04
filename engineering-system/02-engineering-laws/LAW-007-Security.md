---
document_id: LAW-007
title: Security
subtitle: Security is a first-class engineering requirement — not an afterthought
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Chief Security Architect
review_cycle: Annual
document_type: Engineering Law
parent_document: LAW-006 Testing
next_document: LAW-008 Performance
---

# LAW-007 — Security

> **"Security is not a feature you add at the end. It is the foundation you build everything on top of."**

---

## Law Statement

**Security controls MUST be designed into every system from the start. No feature may be deployed to production without a completed security review. All secrets, credentials, and sensitive data must be managed using approved secret management tools.**

---

## Non-Negotiable Security Requirements

### Authentication & Authorization
- Every API endpoint (except explicitly public ones) requires authentication.
- Authorization checks use RBAC defined in NES-204.
- JWT tokens expire within 15 minutes (access) / 7 days (refresh).
- Multi-tenant systems enforce `tenant_id` isolation on every query.

### Secrets Management
- **NO** secrets in source code, environment files, or Docker images.
- All secrets stored in **HashiCorp Vault** or **AWS Secrets Manager**.
- Secrets rotated automatically on a schedule (minimum annually, never more than 90 days for sensitive secrets).
- `.env` files are gitignored and never committed.

### Data Protection
- All data at rest encrypted (AES-256 minimum).
- All data in transit over TLS 1.2+ (TLS 1.3 preferred).
- PII data identified, classified, and access-logged.
- Data retention policies applied to all personal data stores.

### Input Validation
- All user input sanitized and validated at the API boundary.
- SQL queries use parameterized statements only (no string concatenation).
- File uploads validated for type, size, and content (not just extension).

---

## Security Review Gates

| Gate | When | Reviewer |
|---|---|---|
| Threat Model | Before design is finalized | Security Architect |
| Dependency Scan | Every PR (automated) | CI Pipeline |
| SAST | Every PR (automated) | CI Pipeline |
| Penetration Test | Before each major release | External or Internal Red Team |
| Compliance Review | Annual | Compliance Team |

---

## Incident Response

Any security incident must be reported within **1 hour** of discovery to the Security Team. See NES-518 — Incident Response for the full protocol.

---

## Anti-Patterns

❌ Hardcoded API keys, passwords, or tokens in source code.  
❌ Using HTTP instead of HTTPS in any environment.  
❌ Storing passwords in plaintext or with MD5/SHA1.  
❌ Bypassing authorization for "internal" endpoints.  
❌ "We'll fix security before we go to prod."

---

## Related Standards

- NES-600 — Secure SDLC
- NES-601 — OWASP Security Standards
- NES-602 — Threat Modeling
- NES-603 — Zero Trust Architecture
- NES-605 — Secrets Protection
- NES-203 — Authentication & Identity
- NES-204 — Authorization

---

## Version History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2026-07-04 | NeelStack Engineering | Initial publication |
