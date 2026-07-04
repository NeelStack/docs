---
document_id: NES-606
title: Encryption & Key Management
subtitle: Enterprise Cryptography, Key Rotation & Envelope Encryption Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Security Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-605 Secrets Protection
next_document: NES-607 Vulnerability Management
---

# NES-606 — Encryption & Key Management

> **"Data must be protected at rest and in transit. We use standard cryptographic primitives, rotate KMS keys, and enforce envelope encryption."**

---

# Executive Summary

Unauthorized access to datastores or message payloads can lead to severe data breaches.

To ensure data remains unreadable even if physical disks or network streams are intercepted, we enforce strict cryptography and key management standards.

This standard defines our approved cryptographic algorithms, encryption-at-rest policies, envelope encryption patterns, and KMS key rotation guidelines.

---

# Purpose

This standard defines:

- Approved Cryptographic Algorithms
- Encryption in Transit Standards (TLS 1.3)
- Encryption at Rest Standards (TDE, Volume Encryption)
- Envelope Encryption Architecture
- Key Management Service (KMS) Policies

---

# Approved Cryptographic Algorithms

We restrict cryptographic algorithms to modern, vetted primitives:

| Category | Standard Algorithm | Rationale |
|---|---|---|
| Symmetric Encryption | **AES-256-GCM** | High security, built-in integrity check (AEAD). |
| Asymmetric Encryption | **RSA-4096** / **ECC (secp256r1)** | Secure key exchange and signing. |
| Hashing (Passwords) | **Argon2id** / **bcrypt** | High computation cost, protects against GPU attacks. |
| Hashing (Data integrity) | **SHA-256** / **SHA-512** | Cryptographic hash checks. |

- Avoid MD5, SHA-1, DES, and AES-ECB algorithms. They are insecure and prohibited.

---

# Encryption in Transit (TLS 1.3)

All network traffic must be encrypted in transit.

- **HTTPS Enforced**: Cleartext HTTP is prohibited in production.
- **Protocols**: We mandate **TLS 1.3** as the primary encryption protocol (TLS 1.2 is permitted as a fallback for verified legacy clients).
- **Cipher Suites**: Disable weak cipher suites. Enforce perfect forward secrecy (PFS) ciphers.

---

# Encryption at Rest (TDE)

All database records, cache dumps, log indexes, and file volumes must be encrypted at rest:

- **Storage Volumes**: Enable Transparent Data Encryption (TDE) on all cloud RDS PostgreSQL databases, S3 buckets, and EBS/EFS volumes.
- **Keys**: Cryptographic encryption keys must be managed by the secure Key Management Service (KMS).

---

# Envelope Encryption Architecture

For high-security datasets (e.g. encrypting specific columns containing user PII keys in a database), we use the **Envelope Encryption** pattern.

- **Data Encryption Key (DEK)**: A unique AES-256 key generated to encrypt the target data payload locally.
- **Key Encryption Key (KEK)**: The KMS Customer Managed Key used to encrypt the DEK.
- **Storage**: The encrypted DEK is stored alongside the encrypted data. The plaintext DEK is discarded from memory immediately after usage.

```text
  Plaintext Data + Plaintext DEK ──► Encrypt ──► Encrypted Data
                                                      ▲
  KMS Master Key + Plaintext DEK ──► Encrypt ──► Encrypted DEK
                                                      │
                                           Stored Together on Disk
```

---

# KMS Key Rotation Policies

Cryptographic master keys must be rotated regularly to limit the volume of data encrypted under a single key state.

- **Automated Rotation**: Customer Managed Keys (CMKs) in AWS KMS must have annual automated rotation active.
- **Manual Rotation Playbook**: Maintain a documented script to re-encrypt archived databases under a new master key in case of compromised access concerns.

---

# Anti-Patterns

❌ **Hardcoded Hashing Salts**: Using static salt strings inside password hashing scripts. Salts must be unique and generated randomly using cryptographically secure random number generators (CSPRNG).

❌ **Symmetric Encryption without Integrity Checks**: Using AES in CBC mode instead of GCM, which is vulnerable to padding oracle attacks.

❌ **Exposing Plaintext Keys in Logs**: Printing DEKs or KMS access tokens inside log streams or crash report variables.

---

# Production Checklist

- [ ] TLS 1.3 is active on all ingress gateways.
- [ ] Database volumes use KMS SSE encryption.
- [ ] Envelope encryption helper modules utilize AES-256-GCM.
- [ ] Annual KMS key rotation is active.
- [ ] Insecure algorithms (MD5, SHA-1) are removed from codebases.

---

# Success Criteria

The Encryption and Key Management system is successful when:
- Intercepted datastores or backup volumes are unreadable without active KMS authorization.
- Performance overhead introduced by envelope encryption loops remains under 10ms.
- Vulnerability scanners report zero usage of deprecated cryptographic algorithms.

---

# Document Status

**Document:** NES-606 — Encryption & Key Management
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-607 — Vulnerability Management**
