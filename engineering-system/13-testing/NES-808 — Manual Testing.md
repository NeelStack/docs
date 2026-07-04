---
document_id: NES-808
title: Manual Testing
subtitle: Enterprise Manual Testing, Exploratory & Accessibility (WCAG) Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Quality Assurance Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-807 Security Testing
next_document: NES-809 UAT
---

# NES-808 — Manual Testing

> **"Manual testing is exploratory, not mechanical. We focus manual validation on user experience, design alignment, and accessibility standards."**

---

# Executive Summary

While automated scripts are excellent at verifying regressions, they cannot evaluate interface aesthetics, logical user journeys, or accessibility compatibility.

However, running unstructured manual verification where QA engineers click menus randomly is inefficient and fails to document test coverage.

We standardize on **Exploratory Manual Testing** for visual, design, and accessibility validations.

This standard establishes our exploratory test structures, accessibility audits (**WCAG 2.1 AA**), and defect documentation formats.

---

# Purpose

This standard defines:

- Scope of Manual Testing vs. Automation
- Structured Exploratory Sessions (Test Charters)
- Accessibility (WCAG 2.1 AA) Auditing
- Visual Sanity Checks & Design Verification
- Bug Writing Standards

---

# Scope of Manual Testing

Manual verification is restricted to areas that require human judgment:

- **Exploratory Testing**: Testing features to find edge cases that automated test scripts missed.
- **Design Verification**: Verifying that UI layouts, spacings, and animations match Figma specifications.
- **Accessibility Checks**: Verifying screen reader compatibility, keyboard navigation flows, and color contrast ratios.

---

# Structured Exploratory Sessions

To prevent unstructured testing, manual checks must run in time-boxed **Exploratory Sessions**:

- **Session Charter**: Every session must have a defined charter (e.g. "Explore student registration flow using safari on mobile screen sizes").
- **Time Box**: Sessions are limited to **60 – 90 minutes**.
- **Execution Log**: The QA engineer documents the paths explored, screenshots of visual anomalies, and logs any bugs found.

---

# Accessibility Audits (WCAG 2.1 AA)

All user-facing applications must comply with **WCAG 2.1 AA** accessibility standards:

- **Keyboard Navigation**: Verify users can navigate pages using only the `Tab` and `Enter` keys.
- **Screen Reader Verification**: Verify all interactive elements have correct `aria-label` attributes.
- **Color Contrast**: Verify text elements have a minimum contrast ratio of **4.5:1** against backgrounds.
- **Automated QA Checkers**: Use browser audit tools (e.g. axe-core, WAVE) to scan for accessibility issues before manual tests.

---

# Bug Writing Standards

When manual testing exposes a defect, write clear, actionable bug reports in Jira:

- **Title**: Clear, descriptive summary (e.g. "Mobile login: Submit button overflows screen on iPhone SE").
- **Environment**: Detail the device OS, browser version, and test tier.
- **Steps to Reproduce**: Step-by-step instructions.
- **Expected vs. Actual**: Contrast the expected layout with actual behavior.
- **Attachments**: Include screenshots, video recordings, and browser console error logs.

---

# Anti-Patterns

❌ **Manual Regression Testing**: Manually executing repetitive regression test cases on every release cycle, wasting QA resources. Automate regression tests.

❌ **Undocumented Manual Passes**: Completing manual verification runs without logging what browser version or steps were tested, making bug replication impossible.

❌ **Excluding Accessibility from QA**: Treating accessibility as a post-release compliance issue instead of auditing it during feature validation runs.

---

# Production Checklist

- [ ] Manual test sessions utilize structured Charters.
- [ ] Accessibility scans (axe-core) are integrated into development workflows.
- [ ] Keyboard-only navigation paths are verified.
- [ ] Bug report template is configured in Jira.
- [ ] Visual audits check design alignment against Figma specifications.

---

# Success Criteria

The Manual Testing program is successful when:
- Visual and user experience issues are caught before releases are deployed.
- 100% of user-facing pages comply with WCAG 2.1 AA accessibility guidelines.
- Bug reports contain all details needed for developers to reproduce issues.

---

# Document Status

**Document:** NES-808 — Manual Testing
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-809 — UAT**
