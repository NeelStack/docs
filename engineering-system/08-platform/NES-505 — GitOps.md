---
document_id: NES-505
title: GitOps
subtitle: Enterprise GitOps, Infrastructure Repository & State Reconciliation Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-504 GitHub Actions
next_document: NES-506 ArgoCD
---

# NES-505 — GitOps

> **"Git is the single source of truth for our infrastructure state. We deploy and configure services using declarative configurations and automated pull reconciliations."**

---

# Executive Summary

Traditional deployment pipelines ("Push pipelines") rely on CI runners having full administrator access to cloud clusters to run commands like `kubectl apply` or `helm install`.

This introduces security risks (credentials leaked in CI) and allows manual cluster changes to drift undetected.

NeelStack standardizes on **GitOps** for all application deployments.

This standard establishes the repository architecture, release flow, and cluster state reconciliation rules.

---

# Purpose

This standard defines:

- GitOps Principles and Advantages
- Repository Architecture (Application vs. Configuration)
- The Pull-based Reconciliation Loop
- Drift Detection and Self-Healing
- Promotion Pipeline Conventions

---

# GitOps Principles

Every service deploy pipeline must adhere to four GitOps principles:

✓ **Declarative State**: The entire system state (deployments, ingress, services, policies) must be declared in Git configuration files.

✓ **Versioned Single Source of Truth**: Git commits represent the approved state. What is merged is what runs.

✓ **Automated Pull Reconciliation**: Software agents running inside the target cluster pull configuration updates from Git—no external server pushes configurations.

✓ **Continuous Drift Detection**: The system monitors runtime state and automatically alerts or self-heals if manual changes deviate from Git declarations.

---

# Repository Architecture

To isolate deployment triggers from code iteration, we separate application source code from deployment configurations:

```text
 ┌──────────────────────┐        ┌──────────────────────┐
 │   Application Repo   │        │  Configuration Repo  │
 ├──────────────────────┤        ├──────────────────────┤
 │  - Application Code  │        │  - Helm Values       │
 │  - Dockerfile        │        │  - K8s Manifests     │
 │  - Unit/E2E Tests    │        │  - Environment Config│
 └──────────┬───────────┘        └──────────▲───────────┘
            │                               │
       Triggers CI                     Pulls Updates
            │                               │
            ▼                               │
    GitHub Actions Build                    │
    & Push Image   ─────────────────────────┘
```

- **Application Repository**: Houses code and compiles Docker images. On success, it submits a pull request to update the target tag in the Configuration Repository.
- **Configuration Repository**: Contains actual cluster environment settings (Helm values, Kustomize overrides). This is the only repository accessed by the GitOps operator.

---

# Promotion Pipeline Conventions

Deploying across environments (Dev -> Staging -> Prod) requires explicit Git operations:

1. **Dev Deployment**: Automated on merge to `main` branch inside the application repo. Writes to `/environments/dev` in the config repo.
2. **Staging Deployment**: Triggered via a release tag (e.g. `v1.2.0-rc1`). Updates `/environments/staging`.
3. **Production Deployment**: Triggered via a pull request merging Staging configurations into the `production` branch in the configuration repository. This requires manual peer reviews and platform approval.

---

# Drift Detection & Self-Healing

The GitOps controller monitors the cluster continuously.

- **Drift Identification**: If a developer manually edits a Deployment resource (e.g., changes replica counts using `kubectl scale`), the controller flags the discrepancy.
- **Reconciliation Mode**:
  - **Dev/Staging**: Self-healing is enabled. The controller automatically overwrites manual cluster overrides to match the Git configuration.
  - **Production**: Self-healing is disabled, but drift triggers critical Slack alerts, allowing teams to review changes before applying synchronization.

---

# Anti-Patterns

❌ **CI Runner Cluster Admin Access**: Storing Kubernetes administrative credentials (e.g. `KUBECONFIG` file contents) in GitHub Secrets to run deployment commands directly.

❌ **Monolithic Code-Infra Repositories**: Mixing application code and infrastructure manifests in a single folder, which triggers infinite loops (e.g. code build updates config file, which triggers another code build).

❌ **Manual Hotfixes in Cluster**: Modifying environment variables or configurations inside the cluster during an incident without merging the change to Git.

---

# Production Checklist

- [ ] Configuration repository is separated from application code repositories.
- [ ] SSH deployment keys or OIDC tokens have read-only access to the config repository.
- [ ] Branch protection rules require approvals for merges to the `production` config branch.
- [ ] Slack alerts are configured for sync failure states.
- [ ] Drift tracking alerts are verified as active.

---

# Success Criteria

The GitOps architecture is successful when:
- The entire Kubernetes cluster state can be restored within 10 minutes by pointing the controller to the configuration repository.
- No developer or CI system requires direct write access to the production cluster API to deploy apps.
- Manual cluster configurations are detected and reconciled automatically.

---

# Document Status

**Document:** NES-505 — GitOps
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-506 — ArgoCD**
