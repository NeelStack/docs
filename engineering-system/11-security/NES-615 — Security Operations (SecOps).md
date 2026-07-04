---
document_id: NES-615
title: Security Operations (SecOps)
subtitle: Enterprise Threat Monitoring, Incident Containment & SecOps Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Security Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-614 GDPR Compliance
next_document: NES-616 Security Reference Architecture
---

# NES-615 — Security Operations (SecOps)

> **"Detection is the first step in containment. We monitor security events, deploy active threat scanning, and execute automated response playbooks."**

---

# Executive Summary

Even the most secure configurations cannot prevent every cyber threat.

When a security incident occurs (e.g. brute force access, data extraction, host compromise), operations teams must detect, isolate, and remediate the issue before it spreads.

This standard establishes the Security Operations (SecOps) guidelines, threat monitoring dashboards, containment playbooks, and security response SLA targets.

---

# Purpose

This standard defines:

- Threat Detection and Log Monitoring
- Incident Containment Playbooks (isolation steps)
- Compromised Credentials Rotation Playbook
- SecOps Tools Integration
- Security Operations SLA Targets

---

# Threat Monitoring & Logging

We centralize threat metrics using **OpenSearch Security Analytics** and AWS GuardDuty.

- **Continuous Scans**: AWS GuardDuty scans VPC network flow logs, DNS queries, and AWS CloudTrail logs continuously for anomalies (e.g. host communicating with a known command-and-control server).
- **Log Injection**: All security logs are shipped dynamically to our SIEM via the immutable logging pipeline (NES-610).

---

# Incident Containment Playbook

If a host node or container pod is suspected of being compromised, SRE and SecOps teams must follow a strict **Containment Playbook**:

```text
  Compromise Detected
          │
          ▼
 1. Isolate the Node/Pod
 ├── Remove from Load Balancer
 ├── Apply NetworkPolicy block
 └── Take VM snapshots
          │
          ▼
 2. Capture memory state
          │
          ▼
 3. Terminate compromised Pod
          │
          ▼
 4. Forensic analysis on snapshots
```

1. **Network Isolation**: Do not delete the pod or instance immediately. This wipes memory states needed for diagnostics. Apply a Kubernetes NetworkPolicy to block all ingress and egress network traffic to the pod.
2. **Remove from Service Routing**: Update labels to remove the pod from active service endpoints, preventing users from routing to the node.
3. **Capture Memory Snapshot**: Take a snapshot of the virtual machine disk and dump core memory for forensic analysis.
4. **Kill and Replace**: Terminate the compromised node and let the auto-scaler spin up a fresh instance.

---

# Compromised Credentials Playbook

If developer access keys or API credentials are leaked or compromised:

- **Disable Key**: Revoke the key state in Microsoft Entra ID or AWS IAM immediately.
- **Audit Trails Check**: Run CloudTrail queries for the compromised user ID to list all API actions taken during the compromise window.
- **Force Session Reset**: Terminate all active administrative sessions and force a rotation of all passwords and MFA tokens.

---

# Security Operations SLAs

We enforce strict SLAs for responding to security alerts:

- **Critical Alert (SEV-1 Security)**: On-call response in **under 15 minutes**.
- **Host Containment**: Complete network isolation of a compromised container in **under 30 minutes** from detection.
- **Incident Post-Mortem**: Documented within 24 hours of resolution.

---

# Anti-Patterns

❌ **Deleting Compromised Containers Immediately**: Deleting instances immediately upon breach detection, which wipes out malware binary files and memory states needed to determine how the breach occurred.

❌ **Excluding Staging from GuardDuty**: Restricting threat monitoring to production VPCs, allowing attackers to pivot through compromised staging configurations.

❌ **Ignoring Alert Swarms**: Failing to tune alerts, leading to hundreds of false warnings that drown out real critical signals.

---

# Production Checklist

- [ ] AWS GuardDuty is active in all accounts.
- [ ] Central SIEM alerts are configured in PagerDuty.
- [ ] NetworkPolicy isolation templates are verified.
- [ ] Credentials rotation playbook has been tested.
- [ ] Security incident response contacts matrix is updated.

---

# Success Criteria

The SecOps implementation is successful when:
- Virtual hosts or container compromises are detected and network-isolated in under 15 minutes.
- Incident logs provide a complete history of the compromise path.
- Security drills (simulated breaches) confirm SRE containment readiness.

---

# Document Status

**Document:** NES-615 — Security Operations (SecOps)
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-616 — Security Reference Architecture**
