---
document_id: NES-520
title: Platform Reference Architecture
subtitle: Enterprise Platform Reference Architecture, Cluster Topology & Traffic Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Architecture Board
review_cycle: Every 6 Months
document_type: Reference Architecture
parent_document: NES-519 Disaster Recovery
next_document: NES-600 Secure SDLC Standards
---

# NES-520 — Platform Reference Architecture

> **"A unified architecture creates predictable platform operations. This reference blueprint details the cluster structures, traffic pathways, and core integration patterns."**

---

# Executive Summary

To operate a reliable, secure, and compliant SaaS infrastructure, we must maintain a unified architectural model across all cloud clusters.

This document establishes the official **NeelStack Platform Reference Architecture** blueprint.

It defines our EKS cluster structures, ingress and egress gateways, secure database integrations, secrets management, and telemetry pathways.

---

# Purpose

This standard defines:

- Unified Platform Architecture Blueprint
- Ingress and Egress Traffic Flows
- Security Boundaries and Trust Zones
- Telemetry and Observability Mappings
- Reference Architecture Checklist

---

# Platform Architecture Blueprint

The NeelStack Platform Reference Architecture divides resources into five layers:

```text
                  Cloudflare Edge (WAF, DNS, CDN)
                                │
                                ▼ (HTTPS)
                 AWS Ingress (Application Load Balancer)
                                │
                                ▼
                       EKS Cluster VPC Boundary
  ┌─────────────────────────────────────────────────────────────┐
  │  Ingress Gateway Namespace (Istio Ingress Proxy)            │
  │                             │                               │
  │                             ▼ (mTLS STRICT)                 │
  │  Application Namespace (portal-api Pods)                    │
  │      ├── CSI Secrets Driver (Mounts AWS Secrets)             │
  │      └── Sidecar Proxy (Traces outbound logs via Vector)    │
  │                             │                               │
  │                             ▼ (mTLS STRICT)                 │
  │  Egress Gateway Namespace (Istio Egress Proxy)               │
  └─────────────────────────────┬───────────────────────────────┘
                                │
      ┌─────────────────────────┼─────────────────────────┐
      ▼                         ▼                         ▼
  AWS RDS (Postgres)     AWS ElastiCache (Redis)    AWS S3 Buckets
  (Isolated Subnets)     (Isolated Subnets)         (Object Lock)
```

---

# Traffic Flow Patterns

To secure network routing inside the EKS cluster VPC:

- **Ingress Path**:
  1. Client connections hit Cloudflare for WAF filtering, rate limiting, and SSL termination.
  2. Traffic routes to the AWS Application Load Balancer (ALB).
  3. ALB forwards requests to the Istio Ingress Gateway proxy pods inside the EKS cluster.
  4. Ingress proxy routes requests to target application pods (e.g. `portal-api`) using strict mTLS.
- **Egress Path**:
  1. Application pods requiring external connection (e.g. OpenAI API, payment gateways) query the Istio proxy.
  2. Proxy forwards requests to the centralized Istio Egress Gateway.
  3. Egress Gateway validates the destination DNS, audits the call, and proxies traffic to the public endpoint.

---

# Security & Isolation Boundaries

Maintain strict runtime boundaries to prevent lateral movement in the event of pod compromises:

- **Namespace Segments**: Isolate core services by namespace (e.g. `system`, `auth`, `data`, `apps`).
- **Network Policies**: Restrict inter-namespace communication using Kubernetes NetworkPolicies.
  - *Rule*: Pods in the `default` namespace are blocked from connecting to namespaces housing system configurations (`kube-system`, `argocd`, `vault`) unless explicitly whitelisted.

---

# Integrated Telemetry Architecture

All telemetry data (Metrics, Logs, Traces) must map to our central observability pipeline:

- **Metrics**: Scraped by Prometheus, stored in local database engines, and queried via Grafana.
- **Logs**: FluentBit forwards stdout log streams to Vector. Vector cleans, formats, and index-maps logs inside OpenSearch.
- **Traces**: OpenTelemetry SDKs inside application containers forward tracing headers via sidecars to Jaeger/Zipkin collectors for end-to-end trace mapping.

---

# Anti-Patterns

❌ **Direct Pod Node Exposure**: Routing public connections directly to Kubernetes worker node IPs without load balancers.

❌ **Bypassing Service Mesh Encryption**: Allowing internal services to communicate directly via unencrypted HTTP/TCP protocols instead of Istio proxy routes.

❌ **Shared Dev-Prod Clusters**: Running development workspaces and production workloads on the same physical Kubernetes cluster. This risks accidental service overrides and resource starvation.

---

# Production Checklist

- [ ] Cluster infrastructure matches the Platform Reference Architecture blueprint.
- [ ] Ingress and Egress gateways are active.
- [ ] Kubernetes NetworkPolicies are enforced.
- [ ] Vault secrets integration is operational.
- [ ] Telemetry collectors are forwarding metrics and logs.

---

# Success Criteria

The Platform Reference Architecture is successful when:
- The entire platform infrastructure conforms to a single, easily auditable design pattern.
- Outages or compromises in one namespace are contained and cannot spread to neighboring networks.
- Developers can deploy new microservices that integrate with database, caching, security, and logging layers out-of-the-box.

---

# Document Status

**Document:** NES-520 — Platform Reference Architecture
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-600 — Secure SDLC Standards**
