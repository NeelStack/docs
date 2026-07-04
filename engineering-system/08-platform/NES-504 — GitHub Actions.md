---
document_id: NES-504
title: GitHub Actions
subtitle: Enterprise CI Pipelines, Reusable Workflows & Runner Security Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-503 Terraform
next_document: NES-505 GitOps
---

# NES-504 — GitHub Actions

> **"Code must pass verification before integration. We write fast, modular, and secure CI pipelines using GitHub Actions."**

---

# Executive Summary

Continuous Integration (CI) validates code quality, security posture, and test compliance on every repository modification.

Slow, unoptimized, or insecure workflows block developer productivity, leak infrastructure credentials, and deploy unverified code.

This standard establishes the pipeline structure, reusable workflow configurations, dependency caching rules, and runner security guidelines.

---

# Purpose

This standard defines:

- Pipeline Architecture (Lint, Test, Build, Scan)
- Reusable Workflows
- Dependency Caching (Node, Python, Go)
- Workflow Permissions and Secrets Handling
- Runner Security Policies

---

# Pipeline Architecture

Every repository must declare a validation workflow (typically named `.github/workflows/ci.yml`) that executes on all pull requests and merges to integration branches.

The pipeline follows a strict staged sequence:

```text
  Trigger (PR/Commit)
          │
  ┌───────┼───────┐
  ▼       ▼       ▼
Lint    Type    Security (SAST)
  │       │       │
  └───────┼───────┘
          ▼
   Unit/Component Tests
          │
          ▼
  Build & Container Scan
```

- **Fail-Fast**: If linting or formatting steps fail, the pipeline terminates immediately, conserving runner hours.

---

# Reusable Workflows

To prevent workflow duplication and enforce consistent security checks across hundreds of applications, the Platform Team provides central, reusable workflows:

- **Referenced Workflows**: Feature repositories call central templates using the `uses` keyword:

```yaml
jobs:
  validate:
    uses: neelstack/github-workflows/.github/workflows/python-ci.yml@v1
    with:
      python-version: '3.13'
    secrets:
      API_TOKEN: ${{ secrets.ORGANIZATION_API_TOKEN }}
```

---

# Cache Optimization

Slow builds waste runner minutes and delay developer validation feedback. We require caching package manager dependencies across runs:

- **Python (uv)**: Cache the uv cache directory.
- **Node.js (npm/yarn)**: Utilize standard action caching keys:

```yaml
- name: Set up Node.js
  uses: actions/setup-node@v4
  with:
    node-color: true
    node-version: '22'
    cache: 'npm' # Automatically configures package caching
```

---

# Pipeline Permission Security

Workflows must operate under the principle of **least privilege**.

- **Restrict Permissions**: Avoid global read-write permissions. Define permissions explicitly for each job inside the workflow file.
- **Example**: A standard validation runner only requires read access to the repository:

```yaml
permissions:
  contents: read
  id-token: write # Required for secure OIDC auth to AWS/GCP
```

- **OIDC Integration**: Do not store static cloud credentials (like AWS ACCESS KEY ID) inside GitHub Secrets. Use OpenID Connect (OIDC) to authenticate runners to AWS/GCP dynamically.

---

# Anti-Patterns

❌ **Hardcoded Workflows**: Copying identical 200-line shell compilation workflows into every project repo. Use centralized reusable templates.

❌ **Running Untrusted Actions**: Importing third-party actions from unknown marketplaces without locking them to a specific commit SHA:
   ```yaml
   uses: unknown-user/action@v3 # WRONG: Tag can change
   uses: unknown-user/action@d38a74e... # RIGHT: Static SHA
   ```

❌ **Mutable Environment Secrets**: Hardcoding configurations that differ across deployments inside the workflow steps.

---

# Production Checklist

- [ ] Pipeline runs execute lint, type-check, test, and container scan stages.
- [ ] Dependencies cache key is verified.
- [ ] OIDC trust relation configurations are active for cloud deployments.
- [ ] All third-party actions are locked to specific commit SHAs.
- [ ] Workflow checks are configured as "Required Status Checks" in GitHub branch protection rules.

---

# Success Criteria

The GitHub Actions configuration is successful when:
- Average CI execution time remains under 5 minutes for pull requests.
- Credentials and cloud keys are never exposed in logs or settings.
- Integration branches are completely protected from compiling errors or failing test runs.

---

# Document Status

**Document:** NES-504 — GitHub Actions
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-505 — GitOps**
