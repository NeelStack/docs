---
document_id: NES-412
title: Release
subtitle: Enterprise EAS Submit, App Store Deployment & OTA Updates Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Mobile Operations Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-411 Testing
next_document: NES-413 Analytics
---

# NES-412 — Release

> **"App stores require predictable deployment pipelines. We automate store delivery, manage code signing securely, and control OTA updates dynamically."**

---

# Executive Summary

Mobile releases require deployment to the Apple App Store and Google Play Store.

Manual compilation, code signing profile generation, and build uploads from developer workstations are insecure, slow, and prone to errors.

This standard defines the deployment workflow, EAS Submit automation, OTA (Over-The-Air) update policies, and code signing credential security.

---

# Purpose

This standard defines:

- Versioning Scheme (Semantic Versioning + Build Numbers)
- Multi-Environment Builds (Dev, Staging, Prod)
- EAS Submit Automated Store Delivery
- CodePush and Expo Updates (OTA Policy)
- Build Credential Security (App Store Connect / Play Console APIs)

---

# Semantic Versioning & Build Numbers

All mobile releases must follow a strict versioning scheme:

- **Marketing Version (`version` in `app.json`)**: SemVer structure (`Major.Minor.Patch` e.g. `1.2.0`). This version is visible to customers in stores.
- **Build Number (`ios.buildNumber` / `android.versionCode`)**: Monotonically increasing integers (e.g. `24`). This number is internal and must increment on every build upload.

```json
{
  "expo": {
    "version": "1.0.0",
    "ios": {
      "buildNumber": "1"
    },
    "android": {
      "versionCode": 1
    }
  }
}
```

---

# Deployment Pipeline

We utilize **EAS Submit** to automate the delivery of built packages (`.ipa` for iOS, `.aab` for Android) to App Store Connect TestFlight and Google Play Console Internal Track.

```text
  Developer Commits Code
            │
            ▼
    CI/CD Tests Run
            │
            ▼
   EAS Build Pipeline
            │
      ┌─────┴─────┐
      ▼           ▼
  Build iOS   Build Android
    (.ipa)       (.aab)
      │           │
      └─────┬─────┘
            ▼
  EAS Submit Auto-Upload
      ┌─────┴─────┐
      ▼           ▼
  TestFlight   Google Play
```

---

# CodePush & Over-The-Air (OTA) Updates

We use **Expo Updates** for OTA deployment to fix critical bugs or update content without requiring full store review.

### OTA Guidelines:

- **Allowed Changes**: Styling fixes, wording changes, minor JS logic fixes.
- **Prohibited Changes**: Native module configuration updates, major dependencies changes, core navigation shifts. Any native-level modification requires a full store build submission.
- **Channel Routing**: Updates are directed via runtime channels (`development`, `staging`, `production`) configured in `eas.json`.

```json
{
  "updates": {
    "url": "https://u.expo.dev/xxxx-xxxx-xxxx"
  },
  "runtimeVersion": {
    "policy": "appVersion"
  }
}
```

---

# Build Credential Security

We do not store code-signing keystores, provisioning profiles, or production passwords on developer machines or public repositories.

- **EAS Credentials**: Configure EAS to securely hold Apple distribution certificates and Google Play keystores in its encrypted vault.
- **Service Accounts**: Generate Google Play API service keys and Apple App Store API keys to authorize automated EAS submissions without manual login steps.

---

# Environments & Release Channels

We compile separate app configurations for each deployment stage to keep test data isolated:

- **Development**: Connects to localhost APIs or developer sandboxes. Builds are configured as `development` profiles.
- **Staging**: Connects to `https://api.staging.neelstack.com`. Shared via TestFlight Internal or Google Play Internal Sharing.
- **Production**: Connects to `https://api.neelstack.com`. Published to public stores.

---

# Anti-Patterns

❌ **Manual Build Uploads**: Building and archiving `.ipa` or `.apk` files inside Xcode or Android Studio on local machines to upload via Transporter or browser.

❌ **Pushing Native Updates via OTA**: Pushing javascript updates that rely on a new native package dependency via Expo Updates, causing immediate app crashes on customer devices.

❌ **Using Same Bundle ID**: Using `com.neelstack.portal` for dev, staging, and prod builds. Use suffixes: `com.neelstack.portal.dev` and `com.neelstack.portal.staging`.

---

# Production Checklist

- [ ] Version and build numbers have been incremented.
- [ ] Staging tests are validated and approved by QA.
- [ ] Keystores and Apple certificates are active and unexpired.
- [ ] Privacy policies, terms of service links, and store assets are updated.
- [ ] Release notes are localized and formatted.

---

# Success Criteria

The Release pipeline is successful when:
- App store builds are triggered, compiled, and uploaded to store internal tracks in a single step from GitHub Actions.
- OTA updates deploy to production users in less than 5 minutes for urgent bug patches.
- Non-technical release managers can promote TestFlight builds to production via store dashboards without developer intervention.

---

# Document Status

**Document:** NES-412 — Release
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-413 — Analytics**
