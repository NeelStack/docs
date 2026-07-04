---
document_id: NES-809
title: UAT
subtitle: Enterprise User Acceptance Testing & Beta Distribution Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Product Management Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-808 Manual Testing
next_document: NES-810 Bug Tracking
---

# NES-809 — UAT

> **"Software must satisfy business criteria. We validate features using User Acceptance Testing and structured beta feedback loops before public release."**

---

# Executive Summary

Software that passes automated checks and QA tests can still fail if it does not meet business requirements, user expectations, or client workflows.

Deploying features without validation by real business users can lead to feature rejection and design rework post-release.

We mandate the execution of **User Acceptance Testing (UAT)** and beta-testing feedback loops prior to general availability releases.

This standard establishes our UAT guidelines, beta distribution rules, feedback collection, and client sign-off requirements.

---

# Purpose

This standard defines:

- UAT Scope and Timing
- Beta Testing Distribution Channels (TestFlight, Play Console)
- Structured User Feedback Collection
- Client Sign-off Criteria
- UAT Release Gates

---

# UAT Scope & Timing

UAT represents the final stage of feature verification:

- **Timing**: UAT occurs in the pre-production tier (NES-801) after code passes all QA, security, and performance gates.
- **Audience**: Test runs are executed by business stakeholders, client representatives, and product managers.
- **Criteria**: Validation is based on defined business scenarios (e.g. "Create a tenant account, register 10 students, and export a CSV report").

---

# Beta Distribution Channels

We distribute pre-production builds using secure, isolated beta channels:

- **Mobile Applications**:
  - **iOS**: Distribute builds via **Apple TestFlight** to external client user groups.
  - **Android**: Distribute builds using **Google Play Console Internal Testing** tracks.
- **Web Applications**: Route beta testers to isolated preview environments using custom URLs (e.g. `https://preview-pr123.neelstack.local`).

---

# Structured Feedback Collection

To process tester feedback efficiently:

- **Bug Reports**: Provide a simple, in-app feedback tool to capture logs and screenshot details automatically.
- **Surveys**: Use standardized surveys to measure usability metrics (e.g. System Usability Scale - SUS) for major new features.

---

# Client Sign-Off Criteria

Before a custom client release or major SaaS core update is promoted to production:

- [ ] Core business workflows are verified as functional by the client representative.
- [ ] Major feedback items are triaged and logged as bugs or future enhancements.
- [ ] Product Manager signs off on the release manifest.

---

# Anti-Patterns

❌ **Using Live Production for UAT**: Inviting beta testers to validate unreleased features directly in production, risking live data pollution.

❌ **Ignoring Critical Feedback**: Postponing resolution of usability issues raised during UAT to hit release dates, leading to poor customer reviews post-launch.

❌ **Excluding Client Approvals**: Proceeding with customized enterprise releases without obtaining written sign-off from client managers.

---

# Production Checklist

- [ ] Staging preview URLs are active for web applications.
- [ ] TestFlight and Google Play Console beta channels are configured.
- [ ] Business test scenarios are documented and shared.
- [ ] Feedback collection tools are active in beta builds.
- [ ] Sign-off checklists are configured in release tickets.

---

# Success Criteria

The UAT program is successful when:
- Business users confirm that feature workflows satisfy operational requirements.
- Usability issues are resolved prior to general public release.
- Client sign-off is completed and documented for all custom releases.

---

# Document Status

**Document:** NES-809 — UAT
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-810 — Bug Tracking**
