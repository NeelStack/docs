---
document_id: NES-412
title: Release
subtitle: Enterprise Native Building, Fastlane & Live Updates Standard
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

> **"App stores require predictable deployment pipelines. We automate native building, manage signing certificates securely, and deploy web updates instantly using Live Updates."**

---

# Executive Summary

Mobile releases require publishing compiled native binaries (`.ipa` for iOS, `.aab` for Android) to Apple TestFlight and the Google Play Console.

We automate binary compiling using **Fastlane** and deploy JavaScript/CSS layout hotfixes instantly using **Capawesome Capacitor Live Update** to bypass store reviews for minor updates.

---

# Purpose

This standard defines:

- Semantic Versioning and native build increments
- Compiling native workspaces using Fastlane
- Live Updates (OTA updates) deployment rules
- Secure signing credential storage

---

# Versioning Standards

All Capacitor applications must synchronize version declarations between the web configuration and native workspaces:

- **Marketing Version (SemVer)**: Configured in `package.json` and mirrored to iOS `CFBundleShortVersionString` and Android `versionName` (e.g. `1.2.0`).
- **Build Number**: Monotonically increasing integers mapped to iOS `CFBundleVersion` and Android `versionCode` (e.g. `45`).

---

# Release and Build Automation (Fastlane)

We enforce the use of **Fastlane** inside native directories (`/ios/fastlane` and `/android/fastlane`) to sign, build, and deploy packages to app store test tracks.

```text
    Developer Commits Code
              │
              ▼
    Vite Web Compiles (dist)
              │
              ▼
   npx cap sync (sync to wrapper)
              │
              ▼
     Fastlane Lane Invoked
        ┌─────┴─────┐
        ▼           ▼
   Fastlane iOS  Fastlane Android
    (Match certificates) (Decrypt keystore)
        │           │
        ▼           ▼
    Xcode Build   Gradle Build
      (.ipa)       (.aab)
        │           │
        └─────┬─────┘
              ▼
    TestFlight / Google Play Pushes
```

### Fastlane iOS Lane Example:
```ruby
desc "Submit build to TestFlight"
lane :beta do
  setup_ci
  match(type: "appstore") # Fetch certificate profiles from secure git vault
  increment_build_number(build_number: ENV["GITHUB_RUN_NUMBER"])
  gym(scheme: "App") # Compile .ipa
  pilot # Upload to TestFlight
end
```

---

# Live Updates (Over-The-Air)

We use **`@capawesome/capacitor-live-update`** (or approved alternatives) to push JS/CSS bundle patches to devices without requiring a full App Store review.

### Live Update Guidelines:
- **Allowed Updates**: Bug fixes, style adjustments, text/content edits.
- **Prohibited Updates**: Native package modifications (adding Capacitor plugins), significant structural flow changes. Any changes containing native code additions require compiling a new native binary.

```typescript
import { LiveUpdate } from '@capawesome/capacitor-live-update';

export async function checkApplicationUpdates() {
  const result = await LiveUpdate.sync();
  if (result.activeBundleChanged) {
    // Prompt user to reload or reload automatically
    await LiveUpdate.reload();
  }
}
```

---

# Build Credentials Security

Keystore certificates, iOS `.p8` distribution files, and signing keys must never be committed to the application repository.

- **Fastlane Match**: iOS certificates are encrypted and stored in a private repository managed by the core infrastructure team.
- **CI Environments**: Store keystores and API authentication tokens inside GitHub Actions Encrypted Secrets, decrypting them dynamically during CI runs.

---

# Anti-Patterns

❌ **Manual Xcode Archive Submissions**: Creating release archives locally in Xcode or Android Studio on developer laptops, which leads to inconsistent compilation setups.

❌ **Deploying Native Plugins via Live Update**: Pushing web code containing new native plugins to devices running older binaries, triggering app crashes on user launch.

---

# Production Checklist

- [ ] Web production assets build completes cleanly before `npx cap sync`.
- [ ] iOS profiles are verified via Fastlane Match.
- [ ] Android signing keystore is decrypted successfully on CI.
- [ ] Version and build numbers are incremented.

---

# Success Criteria

The Release pipeline is successful when:
- Releases can be built and pushed to TestFlight and Google Play via a single GitHub Actions commit push.
- Live updates deploy to production environments within 5 minutes.
- Android and iOS packages build cleanly without developer signing setups.

---

# Document Status

**Document:** NES-412 — Release
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-413 — Analytics**
