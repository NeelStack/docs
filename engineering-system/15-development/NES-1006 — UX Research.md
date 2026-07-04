---
document_id: NES-1006
title: UX Research
subtitle: Enterprise User Experience Research, Usability Testing & SUS Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Design & UX Board
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-1005 Product Analytics
next_document: NES-1007 Design Review
---

# NES-1006 — UX Research

> **"Interface design must be validated by user interaction. We conduct structured usability tests and measure user satisfaction metrics systematically."**

---

# Executive Summary

A beautifully designed user interface can still fail if it introduces high cognitive load, confusing workflows, or hard-to-read elements.

Developing layouts without observing real users navigate them leads to costly post-release design revisions.

We mandate the integration of **User Experience (UX) Research** during product discovery and validation phases.

This standard establishes our usability testing guidelines, user interview schedules, and satisfaction measurement protocols (System Usability Scale).

---

# Purpose

This standard defines:

- UX Research Methods (Qualitative vs. Quantitative)
- Moderated and Unmoderated Usability Testing
- System Usability Scale (SUS) Metrics
- User Interview Schedules and Recruitment
- Research Artifact Logging

---

# UX Research Methods

We apply two research models depending on the product stage:

- **Generative (Qualitative)**: Conducted during the discovery phase (NES-1000) using user interviews, card sorting, and field studies to identify user pain points.
- **Evaluative (Quantitative)**: Conducted during validation phases using usability testing, click tests, and A/B test logs to measure design performance.

---

# Usability Testing Standards

Usability tests observe users interacting with our app prototypes:

- **Moderated Testing**: A researcher guides the user through specific scenarios (e.g. "Onboard a new student"), asking them to "think out loud" to capture cognitive barriers.
- **Unmoderated Testing**: Users complete tasks independently using remote platforms (e.g. UserTesting.com) while screen recordings and click logs are captured automatically.
- **Target Audience**: Run tests with a minimum of **5 representative users** per target segment, which catches up to 85% of usability issues.

---

# System Usability Scale (SUS)

We measure product usability using the industry-standard **System Usability Scale (SUS)** survey:

- **SUS Survey**: A 10-item questionnaire with 5 response options (Strongly Disagree to Strongly Agree).
- **Target Score**: All core products must achieve an average SUS score exceeding **75** (Good/Excellent).
- **Remediation**: Product flows scoring below 68 are flagged for usability audits and redesign sprints.

---

# User Interview & Research Operations

Maintain standard operations for research tasks:

- **Recruitment**: Recruit users matching our target personas (NES-1000). Ensure participants sign non-disclosure agreements (NDAs) and privacy consent forms.
- **Repository**: Store research recordings, interview summaries, and usability insights in the centralized **UX Research Repository** for team reference.

---

# Anti-Patterns

❌ **Testing Only with Colleagues**: Running usability tests exclusively with internal staff or developers, who have high bias and familiarity with the system.

❌ **Leading Questions during Interviews**: Asking users questions like "Do you find this new layout easier to use?" which biases feedback. Use neutral prompts instead (e.g., "Walk me through how you would complete this task").

❌ **Omitting User Consent Forms**: Recording user interviews, faces, or screens without obtaining written GDPR/HIPAA compliance consents.

---

# Production Checklist

- [ ] UX Research plan is documented.
- [ ] NDAs and privacy consents are active.
- [ ] Usability testing scenarios are prepared.
- [ ] SUS surveys are integrated with feedback loops.
- [ ] Research repo is populated with findings.

---

# Success Criteria

The UX Research program is successful when:
- Usability issues are identified and resolved in prototype phases before code is written.
- Core product flows maintain average SUS scores above 75.
- Research insights are documented and guide roadmap prioritization.

---

# Document Status

**Document:** NES-1006 — UX Research
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1007 — Design Review**
