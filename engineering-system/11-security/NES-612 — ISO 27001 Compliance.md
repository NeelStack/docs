---
document_id: NES-612
title: ISO 27001 Compliance
subtitle: Enterprise ISMS, Risk Assessment & Annex A Controls Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Governance & Compliance Board
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-611 SOC2 Compliance
next_document: NES-613 HIPAA Compliance
---

# NES-612 — ISO 27001 Compliance

> **"Security is governed by management processes. We design our Information Security Management System (ISMS) to satisfy ISO 27001 controls."**

---

# Executive Summary

International customers require validation that our security practices conform to recognized global standards.

**ISO/IEC 27001** defines the standards for establishing, implementing, operating, monitoring, reviewing, maintaining, and improving an **Information Security Management System (ISMS)**.

This standard establishes our ISMS governance framework, risk assessment criteria, and Annex A controls.

---

# Purpose

This standard defines:

- The Information Security Management System (ISMS) Framework
- Threat and Risk Assessment Guidelines
- Annex A Security Controls Mapping
- Internal Audit Schedules
- Security Training and Awareness Requirements

---

# The ISMS Framework

Our ISMS is structured using the Plan-Do-Check-Act (PDCA) lifecycle model:

- **Plan**: Define security policies, identify assets, assess risks, and select controls.
- **Do**: Implement and operate security controls and policies.
- **Check**: Monitor, review, and measure control performance against targets.
- **Act**: Apply corrective actions to continuously improve security posture.

---

# Risk Assessment & Treatment

We execute a formal Information Security Risk Assessment at least **once per year**.

- **Risk Registry**: The Compliance Officer maintains the Risk Registry, documenting potential security risks, likelihood, impact, and owners.
- **Risk Treatment**: All risks must be addressed by one of four actions:
  - **Mitigate**: Apply engineering or operational controls to reduce risk.
  - **Avoid**: Stop the operational process that creates the risk.
  - **Transfer**: Transfer the risk (e.g., purchasing cyber insurance).
  - **Accept**: Formally accept the risk with executive sign-off.

---

# Annex A Controls Mapping

NeelStack engineering standards satisfy the security controls of ISO 27001 Annex A:

- **A.9 Access Control**: Satisfied by AWS SSO, Entra ID integration, and strict MFA (NES-604).
- **A.12 Operations Security**: Satisfied by Prometheus/Grafana monitoring, structured logging, and incident response playbooks (NES-516, NES-518).
- **A.14 System Acquisition, Development & Maintenance**: Satisfied by our Secure SDLC code scanning pipelines and threat modeling (NES-600, NES-602).

---

# Internal Audits & Management Reviews

Ensure the ISMS remains effective through regular reviews:

- **Internal Audit**: Schedule an independent internal audit of our security controls every **6 months** to detect non-conformances before the external certification audit.
- **Management Review**: Present security metrics, audit findings, and risk statuses to the executive leadership team annually to verify alignment with business goals.

---

# Anti-Patterns

❌ **Compliance in Isolation**: Developing an ISMS that exists only in documents, while developers continue to run insecure systems in practice.

❌ **Excluding Risk Owners**: Identifying risks without assigning active accountability, leading to unresolved items in the Risk Registry.

❌ **Omitting Continual Improvement**: Treating ISO 27001 as a static check-box target rather than a process of continuous security improvement.

---

# Production Checklist

- [ ] ISMS policies are versioned and published to staff.
- [ ] Risk Registry is updated and reviewed by management.
- [ ] Statement of Applicability (SoA) is signed.
- [ ] Internal security audit schedule is active.
- [ ] ISO 27001 compliance logs are stored securely.

---

# Success Criteria

The ISO 27001 compliance program is successful when:
- NeelStack successfully achieves and maintains ISO/IEC 27001:2022 certification.
- Non-conformances identified in internal audits are resolved within 30 days.
- Employees complete the annual security awareness training.

---

# Document Status

**Document:** NES-612 — ISO 27001 Compliance
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-613 — HIPAA Compliance**
