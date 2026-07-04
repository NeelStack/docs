---
document_id: NES-506
title: ArgoCD
subtitle: Enterprise ArgoCD, App-of-Apps Pattern & Synchronization Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-505 GitOps
next_document: NES-507 Helm
---

# NES-506 — ArgoCD

> **"We use ArgoCD to automate kubernetes reconciliation. We deploy using the Application-of-Applications pattern and declare strict synchronization settings."**

---

# Executive Summary

To execute our GitOps standard (NES-505) inside Kubernetes clusters, we standardize on **ArgoCD** as our continuous delivery reconciliation engine.

ArgoCD monitors the repository containing our declared infrastructure states and synchronizes resources dynamically.

This standard establishes the deployment structure, application topologies, sync policies, and security isolation rules for ArgoCD.

---

# Purpose

This standard defines:

- ArgoCD Cluster Architecture
- The Application-of-Applications pattern
- Synchronization Settings (Auto-Sync, Prune, Self-Heal)
- Multi-Tenant Access Control (RBAC)
- Resource Health Customizations

---

# ArgoCD Cluster Architecture

ArgoCD runs inside a dedicated `argocd` namespace in the management cluster.

- **Standard Isolation**: ArgoCD uses service accounts with minimal roles constrained to target namespaces—avoid cluster-wide root administrator access where possible.
- **Repository Connections**: Access configuration repositories using secure Deploy Keys (SSH keys with read-only access) or GitHub Apps credentials.

---

# The App-of-Apps Pattern

For managing multiple microservices and database resources without creating dozens of separate root configurations manually, we enforce the **Application-of-Applications** pattern.

- **Root Application**: A single master ArgoCD Application resource that points to a directory of other Application definitions in Git.
- **Benefits**: Creating a new service simply requires committing a new deployment YAML file to the master directory. ArgoCD detects the file and provisions the sub-application automatically.

```yaml
# Root Application example
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: root-application
  namespace: argocd
spec:
  project: default
  source:
    repoURL: 'git@github.com:neelstack/gitops-infra.git'
    targetRevision: HEAD
    path: apps-master
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

---

# Synchronization Policies

All Application configurations must declare explicit synchronization parameters inside their specs to prevent orphaned resources.

### Standard settings:

- **`prune: true`**: Automatically delete resources in Kubernetes if they are deleted from Git. This prevents resource accumulation.
- **`selfHeal: true`**: Overwrite manual changes inside the cluster (drift) to match Git configuration.
- **`allowEmpty: false`**: Block synchronization if Git becomes empty (prevents accidental cluster-wide wipes if Git configuration is deleted by mistake).

```yaml
syncPolicy:
  automated:
    prune: true
    selfHeal: true
  syncOptions:
  - CreateNamespace=true  # Auto create destination namespace
  - PrunePropagationPolicy=foreground
  - PruneLast=true
```

---

# ArgoCD RBAC & Multi-Tenancy

In multi-tenant SaaS environments, restrict team access permissions.

- **Projects**: Group applications into distinct **ArgoCD Projects** (`AppProject`).
- **Permissions**: Grant developer teams read-only access to their respective projects in the ArgoCD UI/CLI, restricting cluster access modification to the GitOps system.

---

# Anti-Patterns

❌ **Manual App Creation via Web UI**: Creating application configurations directly using the ArgoCD browser dashboard. All App configurations must be declared in Git to match GitOps rules.

❌ **Syncing to Static Revision Tags**: Linking ArgoCD to mutable Git tags (e.g. `latest`). Always pin targeting to specific branches (e.g. `main`, `production`) or commit hashes.

❌ **Ignoring Application Health Warnings**: Leaving ArgoCD resources in a perpetual "Degraded" or "Progressing" health state due to missing check definitions.

---

# Production Checklist

- [ ] Root Application-of-Applications is initialized.
- [ ] SSH Deploy keys are configured with read-only permissions in GitHub.
- [ ] Sync policy includes automated `prune` and `selfHeal`.
- [ ] Cluster connection configurations use OIDC auth patterns where possible.
- [ ] Destination namespaces are locked.

---

# Success Criteria

The ArgoCD implementation is successful when:
- Adding a new microservice is accomplished solely by committing code to Git.
- Application configurations sync and report "Healthy" status in less than 30 seconds.
- Manual cluster changes are detected and corrected automatically.

---

# Document Status

**Document:** NES-506 — ArgoCD
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-507 — Helm**
