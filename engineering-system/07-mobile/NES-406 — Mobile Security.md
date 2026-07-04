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

> **"Mobile devices are vulnerable to physical access and intercept threats. We protect all enterprise data at rest, in transit, and in memory."**

---

# Executive Summary

Mobile applications handle sensitive client credentials, access tokens, customer databases, and proprietary business logic. 

A compromise of a mobile device must not lead to a breach of backend databases or client data.

This document establishes the mandatory security standards for data storage, network transport, biometrics, runtime environment analysis, and code integrity.

---

# Purpose

This standard defines:

- Data at Rest Encryption (Expo SecureStore)
- Network Transport Security (SSL Pinning)
- Biometric Authentication Integration
- Runtime Security (Root / Jailbreak Detection)
- Source Code Obfuscation and Application Hardening

---

# Data at Rest (Secure Storage)

Never store plaintext credentials, JWTs, OAuth tokens, or personally identifiable information (PII) in AsyncStorage or SQLite.

- **Standard**: Use `expo-secure-store`. This API utilizes iOS Keychain services and Android Keystore system.
- **Size Constraint**: Expo SecureStore has a value limit of 2048 bytes. For larger datasets (e.g. encrypted local SQLite database), use `expo-secure-store` to store a generated 256-bit AES encryption key, and encrypt the database file using that key.

### Secure Write/Read Example:

```typescript
import * as SecureStore from 'expo-secure-store';

export async function saveAuthToken(token: string) {
  await SecureStore.setItemAsync('auth_token', token, {
    keychainAccessible: SecureStore.WHEN_UNLOCKED_THIS_DEVICE_ONLY,
  });
}

export async function getAuthToken(): Promise<string | null> {
  return await SecureStore.getItemAsync('auth_token');
}
```

---

# Network Transport (SSL Pinning)

To protect applications from Man-in-the-Middle (MITM) proxy attacks, we enforce SSL/Certificate pinning for all production API connections.

- **Tooling**: Configure certificate pinning using `expo-build-properties` or custom config plugins.
- **Verification**: Extract SHA-256 fingerprints from production endpoint certificates and declare them in `app.config.js`:

```json
{
  "expo": {
    "plugins": [
      [
        "expo-build-properties",
        {
          "ios": {
            "networkConfigurations": {
              "api.neelstack.com": {
                "publicKeyHashes": ["sha256/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx="]
              }
            }
          }
        }
      ]
    ]
  }
}
```

---

# Biometric Authentication

Enterprise applications must support biometric unlock (Face ID, Touch ID, Android Biometric Prompt) for quick session reactivation.

- **Library**: Use `expo-local-authentication`.
- **Implementation**: Biometrics must serve as an unlock shortcut for a locally encrypted token; it must *never* replace backend token expiration validation.

```typescript
import * as LocalAuthentication from 'expo-local-authentication';

export async function authenticateWithBiometrics(): Promise<boolean> {
  const hasHardware = await LocalAuthentication.hasHardwareAsync();
  const isEnrolled = await LocalAuthentication.isEnrolledAsync();

  if (!hasHardware || !isEnrolled) return false;

  const result = await LocalAuthentication.authenticateAsync({
    promptMessage: 'Unlock NeelStack Portal',
    fallbackLabel: 'Use PIN',
    disableDeviceFallback: false,
  });

  return result.success;
}
```

---

# Runtime Security & Jailbreak Detection

Ensure the application is running in a secure, non-compromised environment.

- **Detection**: Integrate jailbreak and root detection packages (e.g. `react-native-jail-monkey` or custom native modules).
- **Rule**: If a device is detected as jailbroken/rooted:
  - Log a security warning to the telemetry portal.
  - Disable offline database caching.
  - Prevent execution of high-risk business flows (e.g. financial transactions, administrator approvals).

---

# Obfuscation and Application Hardening

JavaScript code compiled into React Native bundles is readable unless hardened.

- **obfuscation**: Run code obfuscation as part of the EAS Build pipeline (e.g. using `javascript-obfuscator` during metro bundle builds).
- **Android ProGuard**: Enable ProGuard rules in `eas.json` for Android builds to obfuscate compiled Java/Kotlin bytecode.

---

# Anti-Patterns

❌ **Storing Tokens in Plaintext**: Saving tokens in standard AsyncStorage, which is readable in plaintext on jailbroken or filesystem-accessed devices.

❌ **Committing API Secrets**: Hardcoding API keys, client secrets, or private keys inside React Native components. All configs must pass through environment variables.

❌ **Bypassing SSL Errors**: Disabling certificate check constraints in development and leaving the flag active in production code.

---

# Production Checklist

- [ ] Cleartext HTTP connections are completely disabled (`cleartextTrafficPermitted: false` in Android network security configuration).
- [ ] iOS Keychain configuration has accessibility constraints set to `WHEN_UNLOCKED_THIS_DEVICE_ONLY`.
- [ ] Certificate pinning SHA hashes are updated and verified against production domain certs.
- [ ] Source maps are uploaded to crash reporters and removed from public bundles.
- [ ] Jailbreak/Root checks are integrated and functional.

---

# Success Criteria

The Security design is successful when:
- The app refuses to boot or function on jailbroken/compromised devices if enterprise security flags are set.
- Intercepting APIs with tools like Charles Proxy or Fiddler fails due to SSL pinning constraints.
- Sensitive access keys are stored encrypted within hardware keychains.

---

# Document Status

**Document:** NES-406 — Mobile Security
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-407 — Push Notifications**
