---
document_id: NES-611
title: SOC2 Compliance
subtitle: Enterprise SOC2 Type II Trust Services Criteria & Evidence Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Governance & Compliance Board
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-610 Security Auditing & Logging
next_document: NES-612 ISO 27001 Compliance
---

# NES-611 — SOC2 Compliance

> **"SOC2 compliance demonstrates system security. We design and enforce control evidence pipelines that prove our operational security continuously."**

---

# Executive Summary

Enterprise customers require validation that their data is stored, processed, and protected securely.

A **SOC2 (System and Organization Controls 2) Type II** audit evaluates our operational controls over a minimum of 6 months.

This standard defines the controls, evidence metrics, and compliance workflows required to achieve and maintain SOC2 Type II compliance for NeelStack platforms.

---

# Purpose

This standard defines:

- SOC2 Trust Services Criteria (TSC) Mapping
- Evidence Verification Logs
- Access Control Evidence
- Change Management Controls
- System Vulnerability Controls

---

# Trust Services Criteria (TSC) Focus

NeelStack's SOC2 audit focuses on three primary Trust Services Criteria:

- **Security (Common Criteria)**: Protecting systems against unauthorized access, disclosure, or damage.
- **Availability**: Ensuring systems remain operational and accessible to support customer SLA targets.
- **Confidentiality**: Restricting access to confidential customer data to authorized systems and staff.

---

# Change Management Evidence Controls

Auditors require proof that all changes to production code have been validated, reviewed, and approved:

- **No Self-Merging**: Pull requests must require at least one peer developer review (two reviews for production config repositories).
- **Automated Tests**: Code must pass unit, integration, and security scans (SAST/Trivy) before merging (NES-600).
- **Git Mapping**: GitHub commits in production must map directly to approved pull requests and Jira engineering tasks.

---

# Logical Access Evidence Controls

Prove that access to production customer databases is restricted:

- **SSO Access**: Maintain logs showing all administrative access passes through Microsoft Entra ID with active MFA.
- **Access Reviews**: Run monthly user access sweeps to ensure that employees who changed roles or left the company have had their permissions revoked (SCIM logs).
- **Device Health Logs**: Maintain logs showing that all devices accessing production are MDM-compliant.

---

# Continuous Evidence Gathering

Do not compile evidence manually before audits:

- **Platform Auditing**: Use automated compliance agents (e.g. Vanta, Drata) to poll and capture configurations for EKS clusters, database backups, code review approvals, and encryption settings dynamically.
- **Auditor Dashboard**: Share read-only access to automated compliance portals with external auditors to show real-time, continuous control compliance.

---

# Anti-Patterns

❌ **Manual SSH Access to Prod Databases**: Allowing developers to access production databases using local SSH tunnels. Access must go through audited gateways (AWS SSM) with temporary session credentials.

❌ **Undocumented Code Changes**: Pushing emergency code adjustments directly to production branches without a pull request or linked ticket.

❌ **Outdated Security Training**: Allowing employees to access internal code repositories without completing annual security training.

---

# Production Checklist

- [ ] Vanta/Drata agents are configured and running.
- [ ] PR reviews require at least one approval.
- [ ] AWS IAM SSO maps to Entra ID groups.
- [ ] Database backup restore checks are verified.
- [ ] Annual security training reminders are active.

---

# Success Criteria

The SOC2 Compliance program is successful when:
- The annual SOC2 Type II audit completes with zero exceptions or qualifications in the auditor's report.
- Continuous monitoring dashboards show 100% compliance with security controls.
- Review approvals, backup runs, and vulnerability sweeps generate automated logs.

---

# Document Status

**Document:** NES-611 — SOC2 Compliance
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-612 — ISO 27001 Compliance**
