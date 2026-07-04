---
document_id: TECH-011
title: Kubernetes Standard
subtitle: Kubernetes is the container orchestration platform for all NeelStack production workloads
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Technology Standard
parent_document: TECH-010 Docker
next_document: TECH-012 Terraform
---

# TECH-011 — Kubernetes Standard

---

## Approved Version

**Kubernetes 1.29+** via **AWS EKS**.

## Namespace Structure

```
namespaces/
├── neelstack-prod      # Production workloads
├── neelstack-staging   # Staging workloads
├── neelstack-infra     # Shared infrastructure (monitoring, etc.)
└── neelstack-dev       # Developer preview environments
```

## Resource Requirements

Every deployment MUST define resource requests and limits:

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

Pods without resource limits are rejected by admission webhook.

## Health Probes

All services MUST define liveness and readiness probes:

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
```

## Security Policies

- All pods run as non-root (securityContext)
- Network policies restrict inter-namespace traffic
- Secrets stored in Vault, synced via External Secrets Operator
- RBAC configured per team with least-privilege access

## Related Standards

- NES-502 — Kubernetes
- NES-505 — GitOps
- NES-506 — ArgoCD
- TECH-001 — Technology Stack

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-07-04 | Initial publication |
