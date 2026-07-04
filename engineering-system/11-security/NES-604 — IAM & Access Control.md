---
document_id: NES-604
title: IAM & Access Control
subtitle: Enterprise Identity Management, RBAC & SSO Access Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Security Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-603 Zero Trust Architecture
next_document: NES-605 Secrets Protection
---

# NES-604 — IAM & Access Control

> **"Access is granted on a need-to-know basis. We enforce centralized identity directories, multi-factor authentication, and strict RBAC controls."**

---

# Executive Summary

Improper user access management, shared credentials, and excessive developer roles are primary vectors of security compromises.

If an account is breached, overly permissive access rights can allow attackers to access database servers, modify code repositories, or delete cloud infrastructures.

We mandate the centralization of all identities and access policies using centralized Identity and Access Management (IAM) systems.

This standard outlines the identity lifecycle, MFA requirements, Role-Based Access Control (RBAC) mapping, and Single Sign-On (SSO) settings.

---

# Purpose

This standard defines:

- Identity Centralization (Microsoft Entra ID)
- Multi-Factor Authentication (MFA) Requirements
- Role-Based Access Control (RBAC) & Attribute-Based Access Control (ABAC)
- IAM Identity Center (AWS SSO) Configuration
- Service Accounts and Machine Access Control

---

# Centralized Identity Management

All employee, contractor, and administrator identity profiles must reside in the central directory (**Microsoft Entra ID / Okta**).

- **Single Directory**: No system or service (AWS, GitHub, Slack, Jira) may maintain isolated local user databases for internal staff. All logins must pass through the SSO directory.
- **SCIM Provisioning**: Automate account lifecycle tasks (onboarding, adjustments, offboarding) using SCIM connectors. When an employee is disabled in Entra ID, their access to all associated systems must terminate instantly.

---

# Multi-Factor Authentication (MFA)

MFA is a non-negotiable security requirement for accessing NeelStack environments.

- **Mandatory Enforcement**: Enable MFA globally for all corporate logins, cloud portals, and developer services.
- **Vetted MFA Methods**:
  - **Preferred**: FIDO2/WebAuthn hardware keys (e.g. YubiKeys) or device-tied biometrics (Windows Hello, FaceID).
  - **Allowed**: Mobile push notifications (Microsoft Authenticator).
  - **Prohibited**: SMS-based codes or cleartext email tokens, due to SIM-swapping vulnerability risks.

---

# Role-Based Access Control (RBAC)

Grant resource access based on defined role profiles, avoiding direct user permissions assignment:

- **Roles mapping**: Define access using roles (e.g. `Developer`, `SRE-Operator`, `Auditor`).
- **Just-In-Time (JIT) Elevation**: For administrative tasks (SEV-1 deployments or changes), SREs must request temporary elevation. Permissions are active only for the duration of the incident (max 4 hours) and require manager validation.

```text
  Developer Account (SSO)
           │
           ▼
   Request Access to Prod
           │
  Just-In-Time Elevation (MFA check)
           │
           ▼
    Active for 4 Hours ──► Automatic Revocation
```

---

# Machine & Service Access Control

Services communicating with other services must authenticate using type-safe API credentials:

- **No Static Service Keys**: Do not generate long-term access keys for microservices.
- **OIDC Federation**: EKS pods must assume AWS IAM roles dynamically using IAM Roles for Service Accounts (IRSA).
- **Service Tokens**: External integration calls must use scoped JWT tokens with short lifetimes (max 1 hour).

---

# Anti-Patterns

❌ **Static Developer Keys**: Exporting AWS access keys (`credentials` file) to local development machines. Use SSO temporary credentials instead.

❌ **Direct User Policies**: Attaching permission policies directly to specific user accounts (e.g. "Grant user John S3 write rights") instead of utilizing group mappings.

❌ **Excluding Git from SSO**: Allowing developers to access GitHub repositories using personal email profiles instead of corporate federated profiles.

---

# Production Checklist

- [ ] Microsoft Entra ID is active as the single source of truth for identities.
- [ ] MFA (FIDO2 or mobile push) is enforced globally.
- [ ] AWS SSO is configured with active session constraints.
- [ ] IRSA configuration is active inside all EKS namespaces.
- [ ] Inactive user check sweeps run weekly to prune abandoned accounts.

---

# Success Criteria

The IAM and Access Control system is successful when:
- 100% of user access requests are validated by the centralized SSO directory.
- Disabling a user in the central directory instantly terminates their access to AWS, GCP, GitHub, and all platforms.
- SRE teams can elevate access privileges dynamically during incidents without requiring permanent root keys.

---

# Document Status

**Document:** NES-604 — IAM & Access Control
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-605 — Secrets Protection**
