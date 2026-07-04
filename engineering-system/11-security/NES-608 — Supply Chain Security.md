---
document_id: NES-608
title: Supply Chain Security
subtitle: Enterprise Software Bill of Materials (SBOM) & Dependency Security Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Security Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-607 Vulnerability Management
next_document: NES-609 Security Compliance Framework
---

# NES-608 — Supply Chain Security

> **"Third-party packages represent code we did not write but must trust. We secure our software supply chain by pinning dependencies, auditing manifests, and generating SBOMs."**

---

# Executive Summary

Modern applications rely on thousands of third-party open-source packages (e.g. via npm, pip, go modules).

Attackers frequently target developer ecosystems through malicious updates, typo-squatting, package hijacking, and hidden dependencies.

This standard establishes our dependency verification rules, lockfile enforcement policies, Software Bill of Materials (SBOM) standards, and registry access controls.

---

# Purpose

This standard defines:

- Dependency Selection and Approval
- Lockfile Enforcement and Integrity Checks
- Software Bill of Materials (SBOM) Generation
- Dependency Pinning and Upgrades
- Private Registry Configuration

---

# Dependency Selection Criteria

Before importing any new third-party package into a code repository:

- **Vetting Checklist**: Developers must verify:
  - The package is actively maintained (last release within 6 months).
  - It has a large adoption base (high weekly downloads).
  - Open issues are triaged and security warnings are patched quickly.
- **License Compliance**: Prohibit licenses that require open-sourcing our proprietary code (e.g. GPL, AGPL). Vetted licenses include MIT, Apache 2.0, and BSD.

---

# Lockfile Enforcement & Integrity

Lockfiles ensure that every build utilizes identical dependency code versions.

- **Mandatory Lockfiles**: All repositories must check in lockfiles (`package-lock.json`, `uv.lock`, `go.sum`).
- **Integrity Validation**: CI pipelines must verify lockfile integrity. Any mismatch between package files and lock definitions must cause build termination.
- **Command Lock**: Run installations using frozen flags (e.g., `npm ci` for Node, `uv pip install --frozen` for Python).

---

# Software Bill of Materials (SBOM)

To maintain complete inventory visibility of all deployed libraries:

- **SBOM Generation**: Build pipelines must output a Software Bill of Materials (SBOM) in a machine-readable format (CycloneDX or SPDX) for every production container release.
- **Utility**: Store SBOM outputs in central configuration logs to support rapid search audits when new zero-day vulnerabilities are announced in upstream modules.

```yaml
# GitHub Actions snippet to generate CycloneDX SBOM
- name: Generate SBOM
  uses: CycloneDX/gh-node-sbom@v1
  with:
    output: bom.json
```

---

# Dependency Pinning & Upgrades

- **Strict Pinning**: Pin all top-level dependencies to specific versions (avoid wildcard symbols like `*` or loose version matches like `^`).
- **Automated Upgrades**: Use **Renovate** or **Dependabot** to scan dependencies weekly, generating automated pull requests for minor patches.
- **Merge Gate**: Automated dependency updates must pass complete unit and integration test blocks before merge approval.

---

# Private Registries & Proxying

- **Secure Proxy**: Configure CI and developer environments to pull packages through our private registry proxy (e.g. AWS CodeArtifact or Nexus).
- **Vulnerability Block**: The private registry proxy must block downloads of packages with active, critical CVEs.

---

# Anti-Patterns

❌ **Importing Untracked Dependencies**: Installing npm or pip libraries directly during production builds without updating lockfiles, causing dynamic runtime code mutations.

❌ **GPL License Leaks**: Importing libraries with GPL or copyleft licenses, which exposes our proprietary intellectual property to compliance risks.

❌ **Manual Upgrades in Large Blocks**: Postponing library updates for years and then attempting to upgrade hundreds of packages at once, which causes massive regression testing issues.

---

# Production Checklist

- [ ] All dependency lockfiles are checked into Git.
- [ ] CI pipeline runs dependency license auditing checks.
- [ ] SBOM generation is active on release pipelines.
- [ ] Dependabot/Renovate is configured for weekly dependency sweeps.
- [ ] Local configurations use CodeArtifact proxy destinations.

---

# Success Criteria

The Supply Chain Security program is successful when:
- 100% of deployed packages are recorded in the central SBOM registry.
- Vulnerable third-party modules are identified and upgraded before exploits occur.
- Unauthorized license formats are blocked from entering integration branches.

---

# Document Status

**Document:** NES-608 — Supply Chain Security
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-609 — Security Compliance Framework**
