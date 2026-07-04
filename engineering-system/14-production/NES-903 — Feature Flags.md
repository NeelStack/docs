---
document_id: NES-903
title: Feature Flags
subtitle: Enterprise Feature Flagging, LaunchDarkly & Code Pruning Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-902 Changelogs
next_document: NES-904 Blue-Green Deployments
---

# NES-903 — Feature Flags

> **"Deploy safely, release dynamically. We decouple code releases from customer activation using LaunchDarkly feature flags."**

---

# Executive Summary

Pushing massive feature updates in a single, large deployment exposes platforms to high risk.

If a feature contains a critical bug, rollback requires redeploying old application code packages, which is slow and can cause data corruption.

We standardize on **Feature Flags** to decouple technical code deployments from business releases.

This standard establishes our feature flag platform (**LaunchDarkly / Unleash**), coding rules, flag categorization, and flag clean-up processes.

---

# Purpose

This standard defines:

- Feature Flag Platform (LaunchDarkly)
- Feature Flag Categorization (Release, Experiment, Permission)
- Coding with Fallbacks (Conditional Execution)
- Automated Flag Clean-up (Code Pruning)
- Staging and Testing Flags configurations

---

# Feature Flag Platform

We use **LaunchDarkly** (or **Unleash** as local backup) as our centralized feature flag management system:

- **Edge SDKs**: Applications initialize LaunchDarkly SDKs. Flags are evaluated locally within milliseconds using cached configurations.
- **SSO Integration**: Access to the LaunchDarkly control panel requires SSO authentication (NES-604) with strict RBAC rules.

---

# Flag Categorization

We classify feature flags into three categories to determine their lifecycle parameters:

| Category | Lifetime | Description | Owner |
|---|---|---|---|
| **Release Flags** | Short (< 6 Weeks) | Decouples deploy from launch. Delete after stable rollout. | Developer Team |
| **Experiment Flags** | Short (< 8 Weeks) | Used for A/B testing user behaviors. Delete after analysis. | Product Manager |
| **Permission Flags** | Long-Lived | Grants access to premium tiers or specific tenants (SaaS). | Customer Success |

---

# Coding Standards with Fallbacks

When wrapping application features in flags, developers must write robust fallbacks to ensure availability if connection to the flag manager fails.

- **Default False**: If the flag state lookup fails, the code must default to the stable, existing code path.
- **Clean Fallbacks**: Maintain code formatting guidelines:

```typescript
// Correct LaunchDarkly React integration with fallback configuration
import { useLDClient } from 'launchdarkly-react-client-sdk';

export function OnboardingDashboard() {
  const ldClient = useLDClient();
  // Check flag state; default to 'false' if offline or unavailable
  const showNewDashboard = ldClient?.variation('new-onboarding-ui', false);

  if (showNewDashboard) {
    return <NewOnboardingLayout />;
  }
  return <LegacyOnboardingLayout />;
}
```

---

# Automated Code Pruning

Accumulating retired feature flags in the codebase creates technical debt ("flag rot") and makes code difficult to maintain.

- **Flag SLA**: Release flags must be pruned from the code within **2 weeks** of achieving 100% stable rollout.
- **Automation**: Configure scripts (e.g., using `ld-find-code-refs`) to scan repositories weekly, flagging code references to deleted flags and creating tickets to remove conditional blocks.

---

# Anti-Patterns

❌ **Long-Lived Release Flags**: Keeping release flags in codebases for months because "it might be needed to turn off." This complicates debugging.

❌ **Exposing Client Flags**: Failing to filter flags sent to browser clients, allowing users to discover unreleased feature codes by inspecting scripts.

❌ **Synchronous Flag Calls**: Making blocking network queries to flag servers during database transactions, slowing down APIs.

---

# Production Checklist

- [ ] LaunchDarkly SDK is active with local caching.
- [ ] Fallback paths are declared for all flag queries.
- [ ] Security rules restrict flag dashboard write permissions.
- [ ] Code refs crawler scans repositories weekly.
- [ ] Flags are configured and verified in staging before production runs.

---

# Success Criteria

The Feature Flag program is successful when:
- Features can be turned off instantly during outages without redeploying code.
- A/B experiment rollouts are targeted by tenant, region, or user profile.
- Retired flag references are cleaned up systematically from codebase files.

---

# Document Status

**Document:** NES-903 — Feature Flags
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-904 — Blue-Green Deployments**
