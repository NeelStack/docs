---
document_id: NES-603
title: Zero Trust Architecture
subtitle: Enterprise Zero Trust, Verification & Identity Federation Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Security Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-602 Threat Modeling
next_document: NES-604 IAM & Access Control
---

# NES-603 — Zero Trust Architecture

> **"Never trust, always verify. We treat all requests as hostile, regardless of whether they originate inside or outside our cloud network."**

---

# Executive Summary

Traditional security models rely on a "castle-and-moat" design, assuming that everything inside the internal corporate network or private cloud VPC is safe and trusted.

This approach fails once an attacker gains access to the internal network.

We mandate the enforcement of **Zero Trust Architecture (ZTA)** across all NeelStack environments, systems, APIs, and developer platforms.

This standard outlines the ZTA principles, explicit verification rules, network segmentation practices, and identity federation criteria.

---

# Purpose

This standard defines:

- Zero Trust Security Principles
- Explicit Identity Verification
- Micro-segmentation and Network Isolation
- Least Privilege Access Controls
- Device State Verification

---

# Zero Trust Core Principles

Our Zero Trust architecture is built on three core guidelines:

1. **Verify Explicitly**: Always authenticate and authorize based on all available data points (e.g. user identity, location, device health, service context, data classification).
2. **Use Least Privilege Access**: Limit user and service access with Just-In-Time (JIT) and Just-Enough-Access (JEA) models, using risk-based adaptive policies.
3. **Assume Breach**: Minimize the blast radius of compromises. Segment networks, encrypt all communications, monitor runtime environments, and employ threat detection continuously.

---

# Explicit Verification Loop

Every request to an API, service endpoint, or resource must pass through an explicit validation loop before execution:

```text
  Connection Request (Client)
              │
              ▼
   Collect Identity & Context
   (OIDC Token, Device State, IP)
              │
              ▼
  Enforce Policy Decision (PDP)
  (Authentication & RBAC checks)
              │
              ▼
   Authorize Resource Access
```

Access tokens (JWTs) must be validated at the receiving service container layer—not just at the edge API gateway.

---

# Micro-segmentation & Network Isolation

Network routing must be segmented to prevent lateral movement:

- **Namespace Isolation**: Microservices reside in isolated namespaces with explicit ingress NetworkPolicies.
- **Strict mTLS**: Enforce Mutual TLS (mTLS) cluster-wide using Istio (NES-513). Pods must validate the identity of calling pods before responding to requests.
- **Service authorization**: Deploy Istio `AuthorizationPolicy` manifests to declare which services are allowed to communicate:

```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: rds-access-policy
  namespace: portal-prod
spec:
  selector:
    matchLabels:
      app: rds-proxy
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/portal-prod/sa/portal-api-sa"]
```

---

# Device State & Session Verification

Access to developer environments, admin panels, or code repositories requires device verification:

- **MDM Enrollment**: Developer machines must be enrolled in corporate Mobile Device Management (MDM) systems to ensure disk encryption, password policies, and OS patches are active.
- **Device Health Check**: Block login attempts to internal consoles if the accessing device fails security posture checks (e.g., firewall disabled, outdated OS).

---

# Anti-Patterns

❌ **IP-Based Authentication**: Trusting a connection because it originates from a private IP range (e.g. `10.x.x.x`), permitting access without token verification.

❌ **Permanent Admin Roles**: Granting developers permanent administrator roles in cloud portals instead of dynamic, session-based role assumption.

❌ **Excluding Internal APIs from mTLS**: Leaving internal cluster communications unencrypted because "it is already behind the VPC firewall."

---

# Production Checklist

- [ ] Strict mTLS is active across all EKS service communication channels.
- [ ] Kubernetes NetworkPolicies block inter-namespace traffic by default.
- [ ] JWT authentication verification runs at the service level.
- [ ] AWS IAM SSO uses session limits (max 4 hours).
- [ ] MDM compliance checks are active for developer logins.

---

# Success Criteria

The Zero Trust Architecture implementation is successful when:
- Outages or compromises in one container are contained and cannot spread to neighboring networks.
- Service-to-service connections fail instantly if certificates are mismatched or missing.
- No resource can be queried from inside or outside the VPC without token verification.

---

# Document Status

**Document:** NES-603 — Zero Trust Architecture
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-604 — IAM & Access Control**
