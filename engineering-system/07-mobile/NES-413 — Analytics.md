---
document_id: NES-413
title: Analytics
subtitle: Enterprise Mobile Telemetry, Tracking Consent & Event Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Product Analytics Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-412 Release
next_document: NES-414 Crash Reporting
---

# NES-413 — Analytics

> **"Product decisions require data evidence. We implement type-safe, user-consented behavioral tracking across all mobile applications."**

---

# Executive Summary

To improve our products, optimize user journeys, and identify usability bottlenecks, we must capture user actions and interface performance data.

However, unregulated analytics leads to app store rejections (due to privacy violations), UI performance lags, and inconsistent event schemas.

This standard establishes the mobile analytics lifecycle, tracking consent compliance (App Tracking Transparency - ATT), event naming structures, and toolsets.

---

# Purpose

This standard defines:

- Privacy Compliance & ATT Consent (iOS/Android rules)
- Analytics Integration Tooling (Segment / Firebase)
- Event Naming Schemes and Payload Typings
- Session and Identity Tracking
- Performance Impact Optimizations

---

# Privacy and User Consent (ATT)

Apple and Google enforce strict user privacy controls.

- **iOS App Tracking Transparency (ATT)**: On iOS, if you collect IDFA (Identifier for Advertisers) or track users across external apps, you must display the ATT prompt.
- **Rule**: Minimize tracking scope to avoid displaying the ATT prompt where possible. If tracking is required, request permission contextually.

```typescript
import * as Device from 'expo-device';
import { requestTrackingPermissionsAsync, getTrackingPermissionsAsync } from 'expo-tracking-transparency';

export async function checkTrackingConsent() {
  const { status } = await getTrackingPermissionsAsync();
  if (status === 'undetermined') {
    // Request tracking permission
    const { status: newStatus } = await requestTrackingPermissionsAsync();
    return newStatus === 'granted';
  }
  return status === 'granted';
}
```

---

# Tooling Standards

We standardize on a single wrapper interface connected to our backend data platform or **Segment / Firebase Analytics** SDKs.

- Avoid importing analytics functions directly into layout files. Implement a centralized telemetry service.

```typescript
// Centralized Telemetry Wrapper
export const TelemetryService = {
  identify: (userId: string, traits: Record<string, any>) => {
    // Log user identity to backend analytics
  },
  
  track: (eventName: string, properties?: Record<string, any>) => {
    // Dispatch event payload
  },

  screen: (screenName: string) => {
    // Log page view
  }
};
```

---

# Event Naming Conventions

To prevent analytics pollution, all event names must follow a strict **Object-Action** naming scheme using uppercase letters:

- **Auth**: `USER_LOGIN`, `USER_LOGOUT`
- **Actions**: `DOCUMENT_DOWNLOAD`, `CERTIFICATE_UPLOAD`
- **Errors**: `API_CONNECTION_FAIL`, `BIOMETRIC_ERROR`

### Payload Schema Typing:

Every tracked event must be typed to ensure that product managers receive predictable variables.

```typescript
interface EventMap {
  DOCUMENT_DOWNLOAD: {
    documentId: string;
    documentType: string;
    fileSizeKb: number;
  };
  USER_LOGIN: {
    authMethod: 'password' | 'biometric' | 'sso';
  };
}

export function trackEvent<K extends keyof EventMap>(
  event: K,
  properties: EventMap[K]
) {
  TelemetryService.track(event, properties);
}
```

---

# Session & User Identity Tracking

Associate analytics events with a unique, encrypted ID once the user is authenticated.

- **Rule**: Never pass raw passwords, credit cards, or personal PII keys (phone, email) as custom traits in identify calls.
- **Clear on Logout**: Clear the identity and session data in the telemetry service immediately when the user logs out to prevent cross-account session pollution.

---

# Performance Impact Optimization

Analytics dispatches require network resources.

- **Batching**: Configure analytics clients to buffer event queues locally and send batches every 30 seconds or when the queue hits 20 events.
- **Thread Priority**: Run telemetry dispatches off the primary JS thread execution path.

---

# Anti-Patterns

❌ **Tracking Sensitive Key Presses**: Capturing letters typed in secure input fields (e.g. passwords, pins, credit card numbers).

❌ **Freeform String Event Names**: Creating arbitrary events like `tapped_submit_button_new` or `user_clicked_here`, which breaks analytics dashboards.

❌ **Over-tracking Screens**: Logging page views on simple tab switches or modal scrolls, leading to excessive network requests and distorted engagement data.

---

# Production Checklist

- [ ] Privacy Policy documents list all third-party analytics SDKs.
- [ ] ATT permission key is configured in Info.plist (`NSUserTrackingUsageDescription`).
- [ ] Centralized telemetry service is verified as working on test builds.
- [ ] Event dispatch is verified as disabled in development environments.
- [ ] Session cleanup is triggered on logout actions.

---

# Success Criteria

The Analytics configuration is successful when:
- Product dashboards receive consistent, type-safe events.
- App store submissions pass privacy compliance reviews on the first attempt.
- The analytics SDK consumes less than 1% of mobile processor cycles under continuous usage.

---

# Document Status

**Document:** NES-413 — Analytics
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-414 — Crash Reporting**
