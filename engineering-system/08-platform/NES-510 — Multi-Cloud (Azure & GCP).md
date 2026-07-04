---
document_id: NES-510
title: Multi-Cloud (Azure & GCP)
subtitle: Enterprise Azure AD, GCP Analytics & Cross-Cloud Architecture Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-509 AWS
next_document: NES-511 CDN
---

# NES-510 — Multi-Cloud (Azure & GCP)

> **"A resilient enterprise spans multiple clouds. We integrate Azure for corporate identity and GCP for data intelligence, while maintaining AWS as our primary compute cluster."**

---

# Executive Summary

While AWS is our primary cloud provider, enterprise deployments require integrations with other clouds to leverage specialized capabilities:

- **Microsoft Azure**: Powers corporate directory sync, enterprise identity management (Entra ID), and integration with client enterprise networks.
- **Google Cloud Platform (GCP)**: Powers big data warehousing, analytics, and Google Workspace integrations.

This standard establishes the integration patterns, identity provisioning rules, and network boundaries when operating across Azure and GCP.

---

# Purpose

This standard defines:

- Identity Management (Azure Active Directory / Entra ID)
- Data Analytics Integration (GCP BigQuery)
- Cross-Cloud Security and Network Routing
- Multi-Cloud Identity Federation (OIDC)

---

# Microsoft Azure (Identity & Enterprise)

Azure AD (Entra ID) is our primary identity federation source for corporate SSO and enterprise client accounts.

- **SSO Integration**: Integrate all internal applications with Entra ID via SAML 2.0 or OpenID Connect (OIDC).
- **User Provisioning**: Automate user onboarding and offboarding using SCIM (System for Cross-domain Identity Management) protocols synchronized with Entra ID.

```text
  User Access Attempt
           │
           ▼
   NeelStack Portal (AWS)
           │
     Federates Auth (OIDC)
           │
           ▼
 Microsoft Entra ID (Azure) ── Multi-Factor Auth (MFA)
```

---

# Google Cloud Platform (Data & Workspace)

We use GCP for high-scale analytical queries and machine learning data warehousing.

- **Data Warehousing (BigQuery)**: Sync transaction summaries from AWS RDS to GCP BigQuery using secure ETL tasks (NES-702) for business intelligence.
- **Service Accounts**: Do not export JSON key files for GCP Service Accounts. Use **Workload Identity Federation** to allow AWS-hosted workloads to authenticate to GCP resources dynamically using OIDC tokens.

---

# Cross-Cloud Secure Networking

Cross-cloud data transfers must be protected from intercept threats.

- **No Public Routing**: Do not route database sync traffic or authentication callbacks across the public internet.
- **Standard**: Secure cross-cloud connections using IPSec VPN tunnels (running over Cloudflare Magic WAN or AWS VPN Gateway) or dedicated interconnects (AWS Direct Connect to Azure ExpressRoute).

---

# Identity Federation & SSO Keys

SSO signing keys and certificates must be rotated dynamically.

- Enforce automatic Entra ID signing key rotation checks.
- Store multi-cloud federation keys securely inside AWS KMS or HashiCorp Vault.

---

# Anti-Patterns

❌ **Exporting Long-Lived Service Keys**: Saving GCP Service Account JSON key files inside GitHub repositories or AWS S3 buckets. If a key is leaked, it compromises the entire GCP data project.

❌ **Open Cross-Cloud Endpoints**: Exposing database synchronization APIs directly on public endpoints to connect AWS and GCP clusters without IP whitelisting or mutual TLS (mTLS).

❌ **Direct Active Directory Sync**: Attempting to synchronize Active Directory databases using local scripts instead of standard SCIM provisioning APIs.

---

# Production Checklist

- [ ] Entra ID OIDC configurations use TLS 1.3 endpoints.
- [ ] Workload Identity Federation is configured between AWS EKS and GCP BigQuery.
- [ ] Cross-cloud network connections run encrypted via IPSec tunnels.
- [ ] User SCIM provisioning is verified for offboarding cycles.
- [ ] Multi-cloud access logs are centralized in the monitoring dashboard.

---

# Success Criteria

The Multi-Cloud integration is successful when:
- Employee accounts are deactivated in all AWS, GCP, and Azure portals immediately upon disabling their profile in Microsoft Entra ID.
- AWS workloads can read and write data to GCP BigQuery without utilizing static credentials.
- Cross-cloud network latency remains within defined SLAs.

---

# Document Status

**Document:** NES-510 — Multi-Cloud (Azure & GCP)
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-511 — CDN**
