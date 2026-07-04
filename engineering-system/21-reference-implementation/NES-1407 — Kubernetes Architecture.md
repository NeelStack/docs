---
document_id: NES-1407
title: Kubernetes Architecture
subtitle: Enterprise Kubernetes Cluster Architecture & Resource Topology
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Reference Implementation
parent_document: NES-1406 — Deployment Diagrams.md
next_document: NES-1408 — AWS Architecture.md
---

# NES-1407 — Kubernetes Architecture

> **"Orchestration requires structure. We model our EKS namespaces, pod allocations, service routes, and ingress controllers using Kubernetes Architecture maps."**

---

# Executive Summary

To operate a highly available, secure Kubernetes cluster (EKS) that hosts multiple tenant microservices, we must enforce a structured cluster topology.

This document establishes the official **NeelStack Kubernetes Cluster Architecture** blueprint.

It defines our namespace organization, ingress control routing, internal service communication, and auto-scaling boundaries.

---

# Purpose

This standard defines:

- Unified Kubernetes Cluster Topology Map
- Namespace and Resource Isolation (Free vs. Enterprise)
- Ingress Controller and Routing (Nginx / Istio)
- Horizontal Pod Auto-scaler (HPA) Limits

---

# Kubernetes Architecture Map

The Kubernetes Architecture separates ingress routing, services, and storage zones:

```text
               Public Ingress (HTTPS Requests via AWS ALB)
                               │
                               ▼
        Ingress Controller (Nginx Ingress / Istio Gateway)
                               │
       ┌───────────────────────┴───────────────────────┐
       ▼ (Free Namespace)                              ▼ (Enterprise Namespace)
  Service A Pods (Shared nodes)                   Service A Pods (Dedicated nodes)
  ├── Resource Limits: 500m CPU / 512Mi           ├── Resource Limits: 2000m CPU / 2Gi
  └── HPA: Min 2 / Max 10 pods                    └── HPA: Min 3 / Max 50 pods
       │                                               │
       └───────────────────────┬───────────────────────┘
                               ▼
            Persistent Volume Claim (PVC / EBS mount)
```

---

# Namespace & Resource Isolation

Isolate cluster resources based on tenant profiles:

- **Free Tier Namespace (`ns-free`)**: Shared compute nodes host free tier applications. Enforce strict CPU/Memory resource quotas to prevent tenant resource starvation.
- **Enterprise Namespace (`ns-enterprise`)**: Dedicated node groups host enterprise workloads.

---

# Ingress Control & Routing

- **Ingress Controller**: Use **Nginx Inginx** or **Istio Gateway** as the cluster ingress controller.
- **Routing Rules**: Route incoming requests to target services based on URL paths (e.g. `/api/v1/users` routes to `user-service`).

---

# Horizontal Pod Auto-scaling (HPA)

Protect application availability:

- **HPA Configurations**: Enforce HPA rules on all deployment manifests:
  - **Scale Trigger**: Trigger pod scaling when CPU utilization exceeds **70%** or Memory exceeds **80%**.
  - **Limits**: Configure minimum and maximum pod counts to prevent container resource exhaustion.

---

# Anti-Patterns

❌ **Running Pods without Resource Limits**: Deploying containers without CPU or memory configurations, risking host node starvation.

❌ **Shared namespaces for Development and Production**: Hosting dev test pods in the production namespace.

❌ **Exposing Kubernetes APIs Publicly**: Leaving the cluster API server port open to the public internet without IP whitelist restrictions.

---

# Production Checklist

- [ ] Cluster namespaces conform to the isolation blueprint.
- [ ] Ingress routing configurations are active.
- [ ] Resource quotas are enforced on all namespace boundaries.
- [ ] HPA auto-scaling configurations are verified.
- [ ] Node group metrics are integrated with Prometheus.

---

# Success Criteria

The Kubernetes Cluster Architecture is successful when:
- Deployments scale automatically to handle traffic spikes.
- Tenant applications operate within defined resource quotas.
- Public ingress routes traffic cleanly to target pods.

---

# Document Status

**Document:** NES-1407 — Kubernetes Architecture
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1408 — AWS Architecture.md**
