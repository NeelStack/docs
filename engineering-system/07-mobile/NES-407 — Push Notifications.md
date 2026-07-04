---
document_id: NES-407
title: Push Notifications
subtitle: Enterprise APNs, FCM & Expo Notifications Standard
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

> **"Push notifications re-engage users. We implement a secure, low-latency notification delivery channel using APNs, FCM, and Expo."**

---

# Executive Summary

Mobile push notifications require complex native registrations, credential exchanges, and platform-specific background handlers.

This standard defines the registration architecture, payload schemas, permission guidelines, and background interceptors for iOS and Android devices.

We utilize the **Expo Notifications** system integrated with Apple Push Notification service (APNs) and Firebase Cloud Messaging (FCM).

---

# Purpose

This standard defines:

- Device token registration lifecycle
- APNs and FCM credential configurations
- Push notification permission request standard
- Foreground and background notification handlers
- Notification payload security rules

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
     Expo Notifications
```

---

# Token Registration Lifecycle

On application mount (or post-login), retrieve the device push token and upload it to the NeelStack Backend Database.

- **Unique Identifier**: Generate a unique token representing the device/user combination.
- **Refresh Policy**: Refresh and upload the token on every app startup, as OS tokens change after system updates or reinstalls.

```typescript
import * as Notifications from 'expo-notifications';
import Constants from 'expo-constants';
import { Platform } from 'react-native';

export async function registerForPushNotificationsAsync(): Promise<string | null> {
  if (!Constants.easConfig?.projectId) {
    throw new Error('EAS Project ID not found');
  }

  if (Platform.OS === 'android') {
    await Notifications.setNotificationChannelAsync('default', {
      name: 'default',
      importance: Notifications.AndroidImportance.MAX,
      vibrationPattern: [0, 250, 250, 250],
      lightColor: '#FF231F7C',
    });
  }

  const { status: existingStatus } = await Notifications.getPermissionsAsync();
  let finalStatus = existingStatus;

  if (existingStatus !== 'granted') {
    const { status } = await Notifications.requestPermissionsAsync();
    finalStatus = status;
  }

  if (finalStatus !== 'granted') {
    return null; // Permission denied
  }

  const tokenData = await Notifications.getExpoPushTokenAsync({
    projectId: Constants.easConfig.projectId,
  });

  return tokenData.data;
}
```

---

# Notification Handlers

Configure how the app responds when a notification is received in different states.

- **Foreground**: Determine if the notification displays an alert or executes logic silently when the app is active.
- **Background/Killed**: Intercept taps on the notification banner to launch the app and navigate to a target deep link.

```typescript
import { useEffect } from 'react';
import * as Notifications from 'expo-notifications';
import { useRouter } from 'expo-router';

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldMutateBadge: true,
  }),
});

export function useNotificationNavigation() {
  const router = useRouter();

  useEffect(() => {
    // Listener for taps on notifications
    const subscription = Notifications.addNotificationResponseReceivedListener((response) => {
      const data = response.notification.request.content.data;
      if (data?.deepLink) {
        router.push(data.deepLink);
      }
    });

    return () => subscription.remove();
  }, []);
}
```

---

# Notification Payload Schema

To maintain consistency and secure data routing, all push payloads must follow a unified JSON schema.

- **Rule**: Never pass sensitive raw data in push notifications. Only pass resource IDs and force the client to fetch data securely after token validation.

```json
{
  "to": "ExponentPushToken[xxxxxxxxxxxxxxxxxxxxxx]",
  "title": "Document Approved",
  "body": "Your student certificate has been approved by the admin.",
  "data": {
    "deepLink": "/document/987",
    "resourceId": "987",
    "category": "DOCUMENT_UPDATE"
  }
}
```

---

# Anti-Patterns

❌ **Intrusive Spamming**: Triggering multiple notifications daily without user configuration settings.

❌ **Forcing Permission on Boot**: Triggering the iOS permission dialog immediately upon the first app launch. Request permission only when the user performs an action that requires notifications (e.g. enabling alerts for a document).

❌ **Logging Plaintext in Payloads**: Including customer names, healthcare details, or personal emails directly in the push text, where it displays on public lockscreens.

---

# Production Checklist

- [ ] APNs Key (.p8 file) is uploaded and configured in Apple Developer Portal and EAS Credentials.
- [ ] FCM Service Account credentials are uploaded to the EAS Dashboard.
- [ ] Notification categories and channels (Android) are declared.
- [ ] Deep linking logic is verified for cold start launches.
- [ ] User notification preference settings are saved to the backend database.

---

# Success Criteria

The Push Notification configuration is successful when:
- Users receive notifications within 5 seconds of backend payload trigger.
- Tapping a notification opens the app and routes immediately to the target resource.
- Permissions are requested contextually and decline cases are handled gracefully.

---

# Document Status

**Document:** NES-407 — Push Notifications
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-408 — Background Sync**
