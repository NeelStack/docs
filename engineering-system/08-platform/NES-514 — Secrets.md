---
document_id: NES-514
title: Secrets
subtitle: Enterprise Secrets Lifecycle, Rotation & Key Management Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering & Security Board
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-513 Service Mesh
next_document: NES-515 Infrastructure Security
---

# NES-514 — Secrets

> **"Secrets must never reside in source code. We manage, inject, and rotate credentials dynamically using secure enterprise vaults."**

---

# Executive Summary

Hardcoded passwords, leaked API tokens, and static encryption keys are the root cause of many cloud data breaches.

Once a secret is committed to Git history, it must be considered compromised.

We mandate the centralization of all environment credentials, token keys, certificates, and passwords inside secure, audited vault systems.

This standard defines the secret lifecycle, rotation policies, and injection mechanisms for the NeelStack ecosystem.

---

# Purpose

This standard defines:

- Vault Platforms (AWS Secrets Manager / Vault)
- Injection Mechanisms (CSI Driver vs. Env Injector)
- Rotation Policies
- Audit Trails and Access Logs
- Recovery and Emergency Procedures

---

# Secrets Management Platforms

We standardize on two secure storage vaults:

- **Primary Cloud (AWS)**: Use **AWS Secrets Manager** for database credentials, third-party API keys, and certificate storage.
- **On-Premise / Hybrid**: Use **HashiCorp Vault** for multi-cloud deployments and dynamic service credentials.

---

# Secret Injection Patterns

We prohibit developers from copying secret strings directly into `.env` files or committing them to code repositories. We enforce two injection patterns:

### 1. External Secrets Operator (Preferred)
- **Pattern**: Declare `ExternalSecret` configurations (NES-507). The operator fetches secrets from AWS and mounts them as native Kubernetes Secrets.
- **Scope**: Best for database configuration strings and static platform tokens.

### 2. Secrets Store CSI Driver
- **Pattern**: Mount secrets dynamically as a virtual filesystem directory inside the Pod at startup.
- **Benefit**: Secrets reside in memory (`tmpfs` volume) and are never written to disk, preventing access by unauthorized processes.

```yaml
# CSI volume mount configuration
spec:
  containers:
  - name: portal-api
    volumeMounts:
    - name: secrets-store-inline
      mountPath: "/mnt/secrets-store"
      readOnly: true
  volumes:
    - name: secrets-store-inline
      csi:
        driver: secrets-store.csi.k8s.io
        readOnly: true
        volumeAttributes:
          secretProviderClass: "aws-secrets-provider"
```

---

# Secrets Rotation Policy

Static secrets decay in security value over time. We enforce automated rotation schedules:

- **Database Credentials**: Must be rotated automatically every **30 days** using AWS Lambda rotation hooks.
- **Third-Party API Keys**: Must be rotated every **90 days**.
- **Admin Access Keys**: Expire and require rotation every **90 days** (enforced by IAM compliance policies).

---

# Security Auditing & Access Monitoring

Every access request to a secret must be logged.

- **CloudTrail Logging**: Enable AWS CloudTrail logging for all Secrets Manager APIs.
- **Monitoring Alerts**: Trigger immediate security notifications (PagerDuty/Slack) if a secret is accessed by an unauthorized IAM user or service from outside the EKS cluster network.

---

# Anti-Patterns

❌ **Hardcoded Constants**: Committing strings like `const JWT_SECRET = 'my-super-secret-key'` inside JavaScript files or Helm configs.

❌ **Storing Encryption Keys with Data**: Storing database encryption keys on the same storage volume as the database database file itself.

❌ **Using Shared Secrets**: Sharing the same API key or database password across multiple microservices. Every service must have its own isolated, least-privilege credential.

---

# Production Checklist

- [ ] All database connection passwords have active rotation policies.
- [ ] AWS Secrets Manager keys are encrypted using Customer Managed KMS Keys.
- [ ] Secrets CSI driver or External Secrets Operator is verified.
- [ ] Scanning tools (e.g. GitGuardian or Trufflehog) are active in CI to block commits containing secrets.
- [ ] Access logs are routed to OpenSearch for security auditing.

---

# Success Criteria

The Secrets management standard is successful when:
- Git repository history contains zero plaintext passwords, tokens, or encryption keys.
- Secret rotations complete automatically without causing downtime or connection drops in active services.
- Unauthorized access attempts trigger automated security lockdowns.

---

# Document Status

**Document:** NES-514 — Secrets
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-515 — Infrastructure Security**
