---
document_id: NSC-003
title: Security Review Checklist
subtitle: Security review checklist for all new services, features, and API endpoints
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Security Team
document_type: Checklist
---

# NSC-003 — Security Review Checklist

This checklist must be completed by the Security team or a trained Security Champion before any new service or major feature goes to production.

---

## Authentication & Authorization
- [ ] All endpoints (except explicitly public) require authentication
- [ ] JWT tokens validated on every request (algorithm, expiry, signature)
- [ ] RBAC authorization checks implemented per NES-204
- [ ] Multi-tenant isolation enforced (`tenant_id` on all queries)
- [ ] Privilege escalation is impossible (e.g. user cannot access admin endpoints)

## Input Validation
- [ ] All user inputs validated and sanitized at the API boundary
- [ ] File uploads validated for type, MIME type, and size
- [ ] SQL queries use parameterized statements exclusively
- [ ] No eval(), exec(), or dynamic code execution with user input
- [ ] XSS prevention: all output properly escaped

## Secrets & Credentials
- [ ] No hardcoded secrets in code or config files
- [ ] All secrets stored in Vault / AWS Secrets Manager
- [ ] `.env` files are gitignored
- [ ] Service accounts have least-privilege permissions
- [ ] API keys rotated and have expiry set

## Data Protection
- [ ] PII identified and documented
- [ ] PII access logged for audit
- [ ] Data at rest encrypted (database-level encryption enabled)
- [ ] Data in transit over TLS 1.2+ (TLS 1.3 preferred)
- [ ] Data retention policy applied

## Infrastructure Security
- [ ] Network policies restrict traffic to required ports only
- [ ] Pods running as non-root user
- [ ] Container images scanned for vulnerabilities (Trivy)
- [ ] Security groups follow least-privilege (no 0.0.0.0/0)

## Dependency Security
- [ ] `pip-audit` / `npm audit` — no HIGH/CRITICAL CVEs
- [ ] All dependencies from trusted sources
- [ ] Supply chain security reviewed for new dependencies

## Threat Modeling
- [ ] Threat model reviewed for new service (STRIDE methodology)
- [ ] Attack vectors documented
- [ ] Mitigations in place for identified threats

## Sign-off

| Reviewer | Role | Date |
|---|---|---|
| | Security Champion | |
| | Security Lead (if required) | |

---

*Related: NES-600 — Secure SDLC | NES-601 — OWASP | NES-602 — Threat Modeling | LAW-007 — Security*
