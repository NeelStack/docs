---
document_id: NES-401
title: Expo Architecture
subtitle: Enterprise Expo Config, Development Workflows & EAS Standards
version: 1.0.0
status: Draft
classification: Internal
owner: Mobile Architecture Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-400 React Native Standards
next_document: NES-402 Navigation
---

# NES-401 — Expo Architecture

> **"Expo is the standard platform runtime for NeelStack mobile applications. We use Expo to automate builds, simplify configuration, and optimize development workflows."**

---

# Executive Summary

Historically, managing React Native projects required complex manual configurations of Xcode projects and Android Studio build files.

To simplify dependency upgrades, speed up development, and centralize build infrastructure, NeelStack standardizes on the **Expo Ecosystem** using the **Managed Workflow**.

This standard establishes the configuration rules, build guidelines, and release flows using Expo and Expo Application Services (EAS).

---

# Purpose

This standard defines:

- Expo Configuration (`app.json` / `app.config.js`)
- Managed Workflow standards
- Development Builds vs. Expo Go
- EAS Build configuration and credential management
- EAS Submit automated store delivery
- Config Plugins for native code modification

---

# Managed Workflow Standards

All NeelStack mobile applications must use the **Expo Managed Workflow**.

- **No Manual Native Folder Modification**: Do not edit the `/ios` or `/android` directories directly. Any changes required in native projects must be configured through `app.json` config files or **Config Plugins**.
- **The Prebuild Process**: Native folders are treated as build artifacts. They are excluded from git check-ins (`/ios` and `/android` must be in `.gitignore`). They are generated dynamically on-demand using the `npx expo prebuild` command.

---

# Configuration Standard (`app.json` vs `app.config.js`)

We use `app.config.js` or `app.config.ts` for dynamic configurations (e.g. injecting environment variables or keys) instead of static `app.json`.

### Recommended Structure:

```typescript
import { ExpoConfig, ConfigContext } from 'expo/config';

export default ({ config }: ConfigContext): ExpoConfig => ({
  ...config,
  name: 'NeelStack Portal',
  slug: 'neelstack-portal',
  version: '1.0.0',
  orientation: 'portrait',
  icon: './assets/images/icon.png',
  scheme: 'neelstack',
  userInterfaceStyle: 'automatic',
  splash: {
    image: './assets/images/splash.png',
    resizeMode: 'contain',
    backgroundColor: '#ffffff',
  },
  ios: {
    supportsTablet: false,
    bundleIdentifier: 'com.neelstack.portal',
  },
  android: {
    adaptiveIcon: {
      foregroundImage: './assets/images/adaptive-icon.png',
      backgroundColor: '#ffffff',
    },
    package: 'com.neelstack.portal',
  },
  plugins: [
    ['expo-build-properties', {
      ios: { useFrameworks: 'static' },
      android: { kotlinVersion: '1.9.0' },
    }],
  ],
});
```

---

# Development Builds

We do **not** use the standard Expo Go client app for testing features that require custom native modules (e.g. customized storage, authentication SDKs, Bluetooth, or camera).

- **Standard**: Generate a custom **Development Build** (`expo-dev-client`) for each environment (Development, Staging).
- **Execution**: Create custom builds using:
  ```bash
  npx expo run:ios
  npx expo run:android
  ```
- This launches a native development shell on the emulator that connects directly to the local metro bundler, keeping the native dependencies identical to production.

---

# EAS Build Configuration (`eas.json`)

All app bundles submitted to testers or stores must be built using **EAS Build** to ensure consistent build environments.

### Structure:

```json
{
  "cli": {
    "version": ">= 9.0.0"
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "preview": {
      "distribution": "internal"
    },
    "production": {}
  },
  "submit": {
    "production": {}
  }
}
```

Credentials for signing apps (iOS profiles, Android Keystores) must be managed within the secure EAS dashboard or AWS Secrets Manager—never committed to the code repository.

---

# Config Plugins

Config Plugins are JavaScript wrappers that execute during `expo prebuild` to configure native code without ejecting.

- **Usage**: Always check if a library has a first-party Config Plugin before using it.
- **Example**: If custom native configuration is required for an SDK (like a third-party payment gateway or deep link router), write a custom local Config Plugin under `./plugins` and import it in `app.config.js`.

---

# Anti-Patterns

❌ **Committing /ios or /android**: Never check native directories into git. This defeats the purpose of the Expo Prebuild system.

❌ **Using Expo Go for Native Customizations**: Trying to debug custom native libraries in the standard Expo Go client app, leading to runtime failures.

❌ **Local Native Signing**: Manually signing release builds on developer machines instead of using a unified EAS Build pipeline.

---

# Production Checklist

- [ ] `app.config.ts` version matches the release payload version.
- [ ] iOS `bundleIdentifier` and Android `package` are configured.
- [ ] Asset assets (icon, splash screen, adaptive icons) are correctly sized.
- [ ] All custom native plugins are declared in the `plugins` array.
- [ ] `eas.json` profiles are validated.
- [ ] Test builds are compiled successfully via `eas build --profile preview`.

---

# Success Criteria

The Expo setup is successful when:
- Native build directories are completely ephemeral and can be generated successfully from scratch.
- Product builds can be initiated by any developer using `eas build` without needing local Xcode or Android Studio installations.
- Production submissions are triggered automatically from the main CI/CD pipeline via `eas submit`.

---

# Document Status

**Document:** NES-401 — Expo Architecture
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-402 — Navigation**
