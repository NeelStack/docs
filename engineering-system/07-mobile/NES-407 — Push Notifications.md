---
document_id: NES-407
title: Push Notifications
subtitle: Enterprise APNs, FCM & Capacitor Push Standards
version: 1.0.0
status: Draft
classification: Internal
owner: Mobile Platform Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-406 Mobile Security
next_document: NES-408 Background Sync
---

# NES-407 — Push Notifications

> **"Push notifications re-engage users. We implement a secure, low-latency notification delivery channel using APNs, FCM, and Capacitor native handlers."**

---

# Executive Summary

Mobile push notifications require native platform registrations, credential exchanges, and platform-specific background receiver hooks.

We standardize on **`@capacitor/push-notifications`** to coordinate device registration and trigger push receivers inside our hybrid web application.

Our backend coordinates notification deliveries using Apple Push Notification service (APNs) for iOS and Firebase Cloud Messaging (FCM) for Android.

---

# Purpose

This standard defines:

- Native Device Token registration lifecycle
- APNs and FCM setup
- Permission request flow rules
- Foreground and background notification tap handling
- Payload security schemas

---

# Push Notification Architecture

```text
  Backend Service (FastAPI)
             │
      Send Payload with Token
             │
             ▼
     ┌───────┴───────┐
     ▼               ▼
 Apple APNs      Google FCM
     │               │
     └───────┬───────┘
             ▼
      Target Device (iOS/Android)
             │
             ▼
  Capacitor Push Notifications
```

---

# Device Registration Lifecycle

Register the device on app startup or post-login, retrieving the registration token and transmitting it to the NeelStack Backend Database.

- **Library**: `@capacitor/push-notifications`.
- **Implementation**: Request permissions and register listeners:

```typescript
import { PushNotifications, Token } from '@capacitor/push-notifications';
import { api } from '@/lib/api';

export async function registerPushNotifications() {
  let permStatus = await PushNotifications.checkPermissions();

  if (permStatus.receive === 'prompt') {
    permStatus = await PushNotifications.requestPermissions();
  }

  if (permStatus.receive !== 'granted') {
    return null; // User denied permissions
  }

  // Register with Apple/Google push services
  await PushNotifications.register();

  // Listeners
  PushNotifications.addListener('registration', async (token: Token) => {
    // Send token to backend API
    await api.post('/device/register', { token: token.value });
  });

  PushNotifications.addListener('registrationError', (error: any) => {
    console.error('Push registration error: ', error);
  });
}
```

---

# Foreground & Background Interaction Handlers

Manage how the application handles incoming messages when active, or when a user taps a notification banner to launch the app.

- **Foreground**: Capture notifications dynamically without necessarily throwing an alert:

```typescript
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { PushNotifications, ActionPerformed } from '@capacitor/push-notifications';

export function usePushNotificationRouter() {
  const navigate = useNavigate();

  useEffect(() => {
    // Triggered when a notification action (tap) is performed
    const actionListener = PushNotifications.addListener(
      'pushNotificationActionPerformed',
      (action: ActionPerformed) => {
        const data = action.notification.data;
        if (data?.deepLink) {
          navigate(data.deepLink);
        }
      }
    );

    return () => {
      actionListener.then(h => h.remove());
    };
  }, [navigate]);
}
```

---

# Payload Security Standards

To meet privacy standards, notification payloads must never contain raw client records or PII (e.g., student names, grades).

- **Payload Schema**: Only transmit resource IDs and route names. Force the client to pull records via authenticated, secure APIs post-launch.

```json
{
  "title": "Document Verification Completed",
  "body": "A new status update has been registered on your file.",
  "data": {
    "deepLink": "/app/document/489f-8fb2",
    "resourceId": "489f-8fb2",
    "category": "DOCUMENT_STATUS"
  }
}
```

---

# Anti-Patterns

❌ **Registering on Boot Unconditionally**: Triggering the iOS push notification consent dialog immediately on first boot. Delay registration prompts until the user has authenticated or activated a feature requiring alerts.

❌ **Raw PII in Notification Text**: Writing sensitive patient or customer names inside push titles, where they display on public lock screens.

---

# Production Checklist

- [ ] APNs distribution certificates are validated in the Apple Developer Portal.
- [ ] Firebase credentials are set inside the `/android/app/google-services.json` file.
- [ ] Registration tokens are refreshed on every app launch to handle OS-driven rotations.
- [ ] Custom action paths resolve to active React Router routes.

---

# Success Criteria

The Push Notification standard is successful when:
- Device push registrations compile and generate registration tokens on iOS and Android emulators.
- Tapping a push notification banner opens the app and routes directly to the referenced record.
- Notifications arrive on active test devices within 5 seconds of backend dispatch.

---

# Document Status

**Document:** NES-407 — Push Notifications
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-408 — Background Sync**
