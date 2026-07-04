---
document_id: NES-513
title: Service Mesh
subtitle: Enterprise Service Mesh, Mutual TLS (mTLS) & Traffic Routing Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-512 Networking
next_document: NES-514 Secrets
---

# NES-513 — Service Mesh

> **"Microservice communication requires secure authentication and observable connections. We encrypt and control all internal mesh traffic using Istio and mTLS."**

---

# Executive Summary

As the number of microservices inside our Kubernetes clusters grows, managing service-to-service communication, load balancing, security certificates, and request tracing becomes highly complex.

If developers are forced to write custom code for encryption, retry loops, and telemetry in every API, implementation gets inconsistent and prone to gaps.

We standardize on **Istio** as our service mesh layer to decouple network routing and security from application code.

---

# Purpose

This standard defines:

- Service Mesh Selection (Istio)
- Mutual TLS (mTLS) Encryption
- Traffic Splitting and Canary Releases
- Service-to-Service Authorization Policies
- Telemetry and Distributed Tracing

---

# Service Mesh Architecture (Istio)

Istio operates using a **Control Plane** (`istiod`) and a **Data Plane**.

- **Sidecar Injection**: The Data Plane consists of Envoy proxy containers injected as sidecars alongside our application containers. All inbound and outbound traffic passes through the proxy.
- **Auto-Injection**: Enable sidecar auto-injection at the namespace level via label tagging:

```bash
kubectl label namespace portal-prod istio-injection=enabled
```

---

# Mutual TLS (mTLS)

To protect inter-service communications from snooping or spoofing within the cluster:

- **Strict mTLS**: Enforce strict mTLS cluster-wide.
- **Rule**: All connections between services must be encrypted using TLS. Non-encrypted connections must be rejected.
- **Certificates**: Istio Control Plane handles automatic generation, injection, and rotation of short-lived certificates.

### PeerAuthentication Configuration:

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: portal-prod
spec:
  mtls:
    mode: STRICT # Rejects cleartext traffic
```

---

# Traffic Splitting & Canary Releases

Service Mesh enables declarative traffic routing to support safe canary deployments.

- **VirtualService**: Expose endpoints via VirtualServices.
- **DestinationRule**: Define subsets (e.g. `v1` vs `v2`) and specify traffic split ratios (e.g. 90% to stable, 10% to canary) during release validations:

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: portal-api
spec:
  hosts:
  - api.neelstack.com
  http:
  - route:
    - destination:
        host: portal-api-service
        subset: v1
      weight: 90
    - destination:
        host: portal-api-service
        subset: v2
      weight: 10
```

---

# Ingress & Egress Control

Control connection boundaries to block unauthorized traffic.

- **Ingress Gateway**: All external traffic entering the cluster must pass through the Istio Ingress Gateway.
- **Egress Gateway**: Block pods from calling external services directly. All outbound API requests to external databases or payment systems must pass through the Egress Gateway to enforce auditing and DNS validation.

---

# Anti-Patterns

❌ **Permissive mTLS**: Leaving mTLS mode set to `PERMISSIVE`. This allows both encrypted and cleartext traffic to co-exist, which security audits reject.

❌ **Application-Level Retries**: Coding retry logic directly inside application modules, which can lead to "retry storms" that crash struggling backend databases. Let the mesh proxies handle retry policies.

❌ **Exposing Control Plane**: Exposing `istiod` administration ports on public paths.

---

# Production Checklist

- [ ] PeerAuthentication is configured with `STRICT` mode.
- [ ] Sidecar injection is active on all application namespaces.
- [ ] VirtualService mappings have default fallback subsets.
- [ ] Egress gateways are active for external API integrations.
- [ ] OpenTelemetry trace header propagation is validated in all applications.

---

# Success Criteria

The Service Mesh implementation is successful when:
- 100% of inter-pod communications inside the cluster are encrypted via mTLS.
- Teams can verify canary code deployments in production without affecting the main user base.
- Network latencies introduced by sidecar proxies remain under 2ms.

---

# Document Status

**Document:** NES-513 — Service Mesh
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-514 — Secrets**
