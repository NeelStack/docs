---
document_id: NES-507
title: Helm
subtitle: Enterprise Helm Charts, Values Management & Templating Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-506 ArgoCD
next_document: NES-508 Cloudflare
---

# NES-507 — Helm

> **"Kubernetes configuration requires standard templates. We package, share, and configure our services using Helm Charts and structured values files."**

---

# Executive Summary

As application fleets grow, writing duplicate Kubernetes manifest files (YAMLs) for every service leads to high maintenance overhead and configuration drift.

We standardize on **Helm** as our package manager and template engine for Kubernetes.

This standard defines chart structures, values validation, secrets injection, and private chart repository usage.

---

# Purpose

This standard defines:

- Chart Structure and Naming
- Values Hierarchy (Default, Env Overrides)
- Dynamic Secrets Injection (ExternalSecrets)
- Chart Packaging and Private Repositories
- Versioning Rules

---

# Chart Structure & Naming

NeelStack uses a **Unified Library Chart** pattern. Individual microservices do not write custom templates. Instead, they reference a shared library chart and override parameters in a `values.yaml` file.

### Feature Chart layout:

```text
charts/portal-service/
├── Chart.yaml             # Metadata, version, and library dependencies
├── values.yaml            # Environment default configuration parameters
└── templates/             # Ephemeral templates (or empty if using library chart)
    └── helpers.tpl
```

### Chart.yaml Configuration:

```yaml
apiVersion: v2
name: portal-service
description: A NeelStack microservice helm package
type: application
version: 1.0.0
appVersion: "1.2.0"
dependencies:
  - name: neelstack-microservice
    version: 2.x.x
    repository: https://charts.neelstack.com
```

---

# Values Hierarchy

Separate configurations from template code using a layered values hierarchy.

- **`values.yaml`**: Contains safe, fallback settings used across all environments (e.g. port allocations, probe routes).
- **`values-dev.yaml` / `values-prod.yaml`**: Environment-specific overrides (e.g. higher replica settings, larger memory allocations in production).

---

# Secrets Management (ExternalSecrets)

Never write plaintext passwords, JWT secrets, or DB keys in `values.yaml` files.

- **Standard**: Use the **Kubernetes External Secrets (ESO)** operator.
- **Mechanism**: The Helm chart declares an `ExternalSecret` resource. ESO reads this, fetches the secret value from AWS Secrets Manager or HashiCorp Vault, and creates a native Kubernetes Secret dynamically in the cluster:

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
spec:
  refreshInterval: "1h"
  secretStoreRef:
    name: aws-secretsmanager-store
    kind: ClusterSecretStore
  target:
    name: db-secret-k8s # Created dynamically in K8s
  data:
    - secretKey: password
      remoteRef:
        key: prod/database/password
```

---

# Helm Release & Versioning

All shared charts must be versioned and published to the private Helm Registry.

- **Semantic Versioning**: Chart versioning follows SemVer (`Chart.yaml` `version` field).
- **Automation**: Workflows build, lint, and push charts to our private repository (e.g., AWS ECR or GitHub Packages) on tag creations:
  ```bash
  helm package charts/portal-service
  helm registry login -u AWS -p $TOKEN $REGISTRY_URL
  helm push portal-service-1.0.0.tgz oci://$REGISTRY_URL/helm
  ```

---

# Anti-Patterns

❌ **Hardcoded Values in Templates**: Hardcoding resource limits or ingress hosts inside the chart templates instead of exposing them in `values.yaml`.

❌ **Checking Encrypted Keys in Git**: Committing plaintext or weak encrypted files directly inside values folders. Use ESO or SealedSecrets.

❌ **Ignoring Chart Linting**: Pushing charts without running `helm lint` and template dry-run checks in the integration pipelines.

---

# Production Checklist

- [ ] Helm charts pass `helm lint` and dry-run template verifications.
- [ ] Dependencies version mappings are locked.
- [ ] Environment overrides are isolated.
- [ ] Secrets injection is configured via `ExternalSecret` specifications.
- [ ] Chart versions are incremented prior to registry uploads.

---

# Success Criteria

The Helm configuration is successful when:
- Creating a new deployment config requires writing less than 30 lines of declarative overrides in `values.yaml`.
- Template checks run cleanly without generating invalid manifest syntax.
- Secrets are dynamically injected into Pods at startup without being stored in Git.

---

# Document Status

**Document:** NES-507 — Helm
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-508 — Cloudflare**
