---
document_id: NES-406
title: Mobile Security
subtitle: Enterprise Mobile Security, Encryption, Biometrics & Obfuscation Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Mobile Architecture Board
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-405 Offline Architecture
next_document: NES-407 Push Notifications
---

# NES-406 — Mobile Security

> **"Mobile devices are vulnerable to physical access and intercept threats. We protect all enterprise data at rest, in transit, and in memory using industry-standard native encryption wrappers."**

---

# Executive Summary

Capacitor applications handle sensitive user tokens, client databases, and intellectual business parameters.

We secure data at rest inside native keychain wrappers, enforce SSL certificate pinning to prevent Man-in-the-Middle (MITM) proxies, implement biometric unlock, inspect the runtime environment for root privileges, and obfuscate production web bundles.

---

# Purpose

This standard defines:

- Data at Rest encryption (Secure Storage)
- SSL Certificate Pinning for network requests
- Biometric Authentication using Face ID / Android Biometric Prompt
- Jailbreak and Root detection rules
- Vite bundle obfuscation and Android ProGuard hardening

---

# Data at Rest (Secure Storage)

Plaintext credentials, JWTs, OAuth tokens, and personally identifiable information (PII) must never be written to unencrypted storage.

- **Standard**: Secure keys must be stored in the native iOS Keychain and Android Keystore.
- **Implementation**: We use **`@capacitor-community/secure-storage`** (or a similar hardware-backed bridge).

```typescript
import { SecureStoragePlugin } from '@capacitor-community/secure-storage';

export async function saveSecureToken(key: string, value: string): Promise<void> {
  await SecureStoragePlugin.set({ key, value });
}

export async function getSecureToken(key: string): Promise<string | null> {
  const { value } = await SecureStoragePlugin.get({ key });
  return value;
}
```

- **For SQLite**: When using relational databases, store a dynamically generated 256-bit database encryption key inside the Secure Storage keychain and open the SQLite database in encrypted mode using SQLCipher bindings.

---

# Network Transport (SSL Pinning)

We block interception proxies (e.g., Fiddler, Charles Proxy) by enforcing SSL certificate pinning on all production endpoints.

- **Tooling**: We utilize native network configurations or plugins such as `@capacitor-community/http` with certificate configurations.
- **Platform Setup**:
  - **Android**: Declare SHA-256 certificate hashes inside `res/xml/network_security_config.xml`.
  - **iOS**: Declare domains and public key hashes in the `Info.plist` file under `NSAppTransportSecurity`.

---

# Biometric Authentication

We support biometrics (Face ID, Touch ID, Android Biometric Prompt) for quick session unlock.

- **Library**: `@capacitor-community/face-id`.
- **Constraint**: Biometrics must only serve as a shortcut to read a locally encrypted token from the secure storage keychain. It must never substitute backend token validation.

```typescript
import { FaceId } from '@capacitor-community/face-id';

export async function authenticateBiometrics(): Promise<boolean> {
  const isAvailable = await FaceId.isAvailable();
  if (!isAvailable.value) return false;

  try {
    await FaceId.auth({
      reason: 'Access your NeelStack account',
    });
    return true;
  } catch (error) {
    return false;
  }
}
```

---

# Runtime Security & Jailbreak Detection

To protect enterprise workflows, the application must verify the integrity of the host OS environment.

- **Detection**: Integrate a community-approved root/jailbreak detection plugin (e.g. `irroot` or a custom native Capacitor plugin).
- **Security Policy**: If a compromised state is detected:
  - Transmit a security warning log to the central telemetry database.
  - Disable local offline databases.
  - Disable high-risk features (e.g., administrator approvals, document signs).

---

# Bundle Obfuscation and ProGuard

Web source files compiled in Capacitor are stored inside application asset folders. We must harden this bundle to make decompilation difficult.

- **Vite Obfuscation**: Integrate `javascript-obfuscator` during the Vite production compilation phase inside `vite.config.ts`.
- **Android ProGuard**: Enable ProGuard rules inside the `/android/app/proguard-rules.pro` file to optimize and obfuscate native Java/Kotlin classes.

---

# Anti-Patterns

❌ **Storing Tokens in localStorage**: Saving access keys or user PII in standard browser localStorage, which is readable in plaintext on jailbroken/compromised systems.

❌ **Exposing Keys in Code**: Committing API keys or secret salts inside front-end web components. Resolve keys dynamically via environment variables injected at build time.

---

# Production Checklist

- [ ] Cleartext HTTP connections are disabled in Android and iOS app configurations.
- [ ] Certificate hashes are updated and verified for production endpoints.
- [ ] Obfuscator plugin is enabled in the Vite production build chain.
- [ ] Keychain items are marked as device-locked (accessible only when device is unlocked).

---

# Success Criteria

The Security implementation is successful when:
- Sensitive variables remain encrypted in native hardware containers.
- Intercepting HTTP endpoints fails unless using a valid, pinned certificate.
- The app flags jailbroken environments and executes corresponding security actions.

---

# Document Status

**Document:** NES-406 — Mobile Security
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-407 — Push Notifications**
