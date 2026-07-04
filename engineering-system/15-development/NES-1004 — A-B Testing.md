---
document_id: NES-1004
title: A-B Testing
subtitle: Enterprise A-B Testing, User Assignment & SRM Check Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Product Analytics Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-1003 Experimentation
next_document: NES-1005 Product Analytics
---

# NES-1004 — A-B Testing

> **"Randomization ensures experiment validity. We distribute users across A-B testing cohorts using hash-based bucketing and monitor Sample Ratio Mismatch."**

---

# Executive Summary

To execute the product experimentation standards (NES-1003) successfully, we must ensure that users are distributed randomly and consistently across control and treatment cohorts.

If user assignment is skewed, or if users experience different variations during a single session, the experiment data will be corrupted.

We mandate the adoption of a standardized **A-B Testing Assignment** pipeline.

This standard establishes our user assignment bucketing, hash-based allocations, telemetry tracking requirements, and Sample Ratio Mismatch (SRM) checks.

---

# Purpose

This standard defines:

- User Assignment Bucketing (Control vs. Treatment)
- Hash-Based Allocation Algorithms (MD5/MurmurHash)
- Event Tracking and Session Persistence
- Sample Ratio Mismatch (SRM) Validation Checks
- Feature Flag Integrations (LaunchDarkly)

---

# Hash-Based User Assignment

To ensure user cohort assignments are deterministic, persistent, and do not require server-side state databases:

- **Algorithm**: Hash the combination of the `user_id` (or `anonymous_id`) and the `experiment_id` using a non-cryptographic hashing algorithm (e.g. **MurmurHash3** or **MD5**).
- **Modulo Split**: Convert the resulting hash to an integer value, apply modulo `100`, and route the user based on the target percentage splits:
  - *Control (A)*: Modulo values `0 – 49`.
  - *Treatment (B)*: Modulo values `50 – 99`.
- **Benefit**: Ensures that the same user always receives the identical variant across web, mobile, and backend nodes.

```typescript
// Correct Hash-Based User Assignment implementation
import murmurhash from 'murmurhash';

export function getExperimentVariant(userId: string, experimentId: string): 'A' | 'B' {
  const hashInput = `${userId}-${experimentId}`;
  const hashValue = murmurhash.v3(hashInput);
  const bucket = hashValue % 100;

  return bucket < 50 ? 'A' : 'B';
}
```

---

# Sample Ratio Mismatch (SRM) Checks

Sample Ratio Mismatch occurs when the actual ratio of users assigned to cohorts deviates from the pre-designed allocation split (e.g. designing a 50/50 split but receiving 48/52 in logs).

- **SRM Validation**: Run a **Chi-Square Goodness-of-Fit test** daily on cohort counts.
- **Alert Trigger**: If the Chi-Square calculation returns a p-value less than **0.001**, flag the experiment as having active SRM. This indicates assignment bias, invalidates the data, and requires immediate termination and audit of the assignment code.

---

# Telemetry and Event Tracking

Every event generated during an active experiment must include cohort identifiers:

- **Required Fields**: Inbound analytics events (NES-705) must contain the `experiment_id` and the assigned `variant_id` (A or B) in their headers or payloads.
- **Exposure Event**: Log a specific `experiment_exposed` event the exact millisecond a user first views a variant interface, establishing the cohort entry point.

---

# Anti-Patterns

❌ **Static Group Allocations**: Allocating users to cohorts based on user ID ranges (e.g., users 1-1000 in control, 1001-2000 in treatment), introducing demographic registration bias.

❌ **Variant Mutability**: Changing a user's variant assignment during an active experiment (e.g. user sees A on web and B on mobile), which invalidates session diagnostics.

❌ **Running Experiments without SRM monitoring**: Analyzing results without running Chi-Square checks, leading to business decisions based on biased user selections.

---

# Production Checklist

- [ ] Assignment scripts use MurmurHash3 modulo math.
- [ ] Analytics events include active experiment context.
- [ ] SRM automated check calculators run daily.
- [ ] LaunchDarkly targeting allocations match planned splits.
- [ ] Outbound event logs are verified as active.

---

# Success Criteria

The A-B Testing implementation is successful when:
- Chi-Square goodness-of-fit validation returns p-values > 0.05 (confirming zero SRM).
- User variant assignments remain consistent across different devices.
- Telemetry events capture the exact point of variant exposure.

---

# Document Status

**Document:** NES-1004 — A-B Testing
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1005 — Product Analytics**
