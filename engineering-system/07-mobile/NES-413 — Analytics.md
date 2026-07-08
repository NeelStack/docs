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

> **"Product decisions require data evidence. We implement type-safe, user-consented telemetry tracking across all mobile applications."**

---

# Executive Summary

To optimize user pathways and identify rendering errors, our mobile applications capture client-side events.

To comply with App Store privacy laws, we request permissions contextually and integrate telemetry wrappers that buffer data, minimizing performance overhead in our WebView.

---

# Purpose

This standard defines:

- Privacy compliance and tracking permission checks (ATT)
- Telemetry integrations via Firebase or Segment
- Event naming conventions and typing schemas
- Performance footprint optimizations

---

# Privacy and User Consent (ATT)

Apple and Google enforce strict user tracking regulations.

- **iOS App Tracking Transparency (ATT)**: If the application tracks user behaviors, you must display the ATT prompt.
- **Library**: `capacitor-plugin-app-tracking-transparency` (or custom native plugin).

```typescript
import { AppTrackingTransparency } from 'capacitor-plugin-app-tracking-transparency';

export async function requestTrackingConsent(): Promise<boolean> {
  const statusRes = await AppTrackingTransparency.getStatus();
  
  if (statusRes.status === 'unrequested') {
    const requestRes = await AppTrackingTransparency.requestPermission();
    return requestRes.status === 'authorized';
  }
  
  return statusRes.status === 'authorized';
}
```

- **iOS setup**: Declare `NSUserTrackingUsageDescription` inside `Info.plist`.

---

# Analytics Integration (Firebase Analytics)

We standardize on **`@capacitor-community/firebase-analytics`** for device behavioral logs.

- **Standard Wrapper**: All tracking calls must flow through a unified service class instead of calling SDK methods directly inside views.

```typescript
import { FirebaseAnalytics } from '@capacitor-community/firebase-analytics';

export const TelemetryService = {
  identify: async (userId: string, traits: Record<string, any>) => {
    await FirebaseAnalytics.setUserId({ userId });
    await FirebaseAnalytics.setUserProperty({ name: 'traits', value: JSON.stringify(traits) });
  },

  track: async (eventName: string, params?: Record<string, any>) => {
    await FirebaseAnalytics.logEvent({ name: eventName, params });
  },

  screen: async (screenName: string) => {
    await FirebaseAnalytics.setScreenName({ screenName });
  }
};
```

---

# Event Naming Standards

We enforce a strict **Object-Action** structure utilizing UPPERCASE formatting:

- `USER_LOGIN`
- `DOCUMENT_DOWNLOAD`
- `BIOMETRIC_ERROR`

### Event Typings:
```typescript
interface EventMap {
  DOCUMENT_DOWNLOAD: {
    documentId: string;
    fileSizeKb: number;
  };
  USER_LOGIN: {
    authMethod: 'password' | 'biometrics';
  };
}

export async function trackEvent<K extends keyof EventMap>(event: K, properties: EventMap[K]) {
  await TelemetryService.track(event, properties);
}
```

---

# Anti-Patterns

❌ **Hardcoded PII Logging**: Transmitting customer emails, passwords, or credit card inputs inside analytics payloads, leading to store blockages and security audits.

❌ **Freeform Event String Labels**: Creating descriptive names like `clicked_red_button_final_v2` which corrupt analytical reporting dashboards.

---

# Production Checklist

- [ ] Privacy Policy documents specify analytics SDK dependencies.
- [ ] ATT permission keys are declared in native configs.
- [ ] Analytics logs are disabled in development environments.
- [ ] Identity profiles are cleared on user logout.

---

# Success Criteria

The Analytics setup is successful when:
- Native apps pass iOS App Store privacy reviews.
- Analytics execution tracks less than 1% CPU utilization in our WebView profile.
- Event names align to uppercase schemas automatically via type validation checks.

---

# Document Status

**Document:** NES-413 — Analytics
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-414 — Crash Reporting**
