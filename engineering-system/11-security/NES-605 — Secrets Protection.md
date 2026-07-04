---
document_id: NES-605
title: Secrets Protection
subtitle: Enterprise Developer Secret Hygiene & Incident Playbook Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Security Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-604 IAM & Access Control
next_document: NES-606 Encryption & Key Management
---

# NES-605 — Secrets Protection

> **"Secrets do not belong in developer workspaces or local file stores. We enforce strict credential hygiene and maintain active response playbooks for leak events."**

---

# Executive Summary

Leaked application credentials, API tokens, SSH keys, and database passwords on developer local drives or public forums represent a severe operational threat.

While cloud systems use secure vaults (NES-514), developers frequently handle credentials in local environments during debugging.

This standard establishes the mandatory rules for developer credential hygiene, local file management, workstation security, SSH keys, and the emergency response playbook for leaked secrets.

---

# Purpose

This standard defines:

- Developer Workstation Secret Hygiene
- SSH Key Security and Management
- Hardened Configuration for Local Environments
- Leaked Secrets Response Playbook
- Automated Pre-Commit Gating

---

# Workstation Secret Hygiene

Developer computers are endpoint targets. We enforce strict data storage rules:

- **No Plaintext Tokens**: Never save API keys, AWS credentials, or database passwords in cleartext files on local desktops or unencrypted folders.
- **Hardware-backed Storage**: Access keys and developer credentials must reside inside secure, system-provided vaults (macOS Keychain, Windows Credential Manager).
- **Environment Vars**: Access local environment parameters via system environment variables—never hardcode them into application config files.

---

# SSH Key Security

SSH keys grant access to repositories and staging servers.

- **Key Generation**: All developer SSH keys must use **Ed25519** algorithm configurations. RSA keys are deprecated.
- **Passphrase Mandatory**: Every private SSH key must be protected with a strong passphrase.
- **Hardware Keys (FIDO2)**: For access to production environments, SSH keys must be bound to hardware security keys (e.g. `ssh-keygen -t ed25519-sk`).

```bash
# Correct SSH Key Generation (Ed25519 with strong passphrase)
ssh-keygen -t ed25519 -C "developer@neelstack.com"
```

---

# Pre-Commit Secret Scanning

Prevent secrets from ever reaching repository logs:

- **Pre-Commit Hook**: Developers must install and configure **gitleaks** or **trufflehog** locally in their repositories before pushing changes.
- **Rule**: If a script detects a secret (e.g. AWS access key, private certificate) inside a staged file change, the pre-commit hook automatically aborts the commit.

---

# Leaked Secrets Response Playbook

If a secret is leaked (e.g. committed to a public repository by accident):

```text
  Secret Leaked
        │
        ▼
 1. Identify & Locate Leak
        │
        ▼
 2. Revoke and Invalidate Secret immediately
        │
        ▼
 3. Generate New Secret in Vault
        │
        ▼
 4. Deploy Updated Configurations
        │
        ▼
 5. Purge Git History (using BFG Repo-Cleaner)
```

1. **Revoke Instantly**: Do not waste time deleting the commit or file. The secret must be treated as fully compromised. **Revoke and invalidate the credential at the provider level immediately.**
2. **Rotate and Update**: Generate a new credential in AWS Secrets Manager, deploy, and verify.
3. **Clean Git History**: Use tools like `git-filter-repo` or `BFG Repo-Cleaner` to completely purge the compromised commit hash from all remote repository histories.

---

# Anti-Patterns

❌ **Storing Keys in git-ignored `.env`**: Relying solely on `.env` files inside repositories. While git-ignored, these files can still be backed up to insecure personal clouds or shared via chat apps.

❌ **Shared Team Passwords**: Sharing single AWS IAM access keys or database passwords across multiple developer profiles.

❌ **Excluding Key Passphrases**: Generating SSH keys without passphrases to simplify automated script execution.

---

# Production Checklist

- [ ] Ed25519 is the enforced standard for developer SSH access.
- [ ] Pre-commit secret scanning hooks are active in developer environments.
- [ ] Leaked secrets incident response team contact protocols are active.
- [ ] GitGuardian is integrated with GitHub to scan all incoming pushes.
- [ ] Workstation disk encryption (BitLocker/FileVault) is verified via MDM.

---

# Success Criteria

The Secrets Protection guidelines are successful when:
- Zero credentials or private keys reach the public repository logs.
- Discovered leaks trigger automated revocation and notifications within 60 seconds.
- Developers utilize hardware-backed keys for all repository and environment access.

---

# Document Status

**Document:** NES-605 — Secrets Protection
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-606 — Encryption & Key Management**
