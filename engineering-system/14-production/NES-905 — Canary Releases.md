---
document_id: NES-905
title: Canary Releases
subtitle: Enterprise Canary Routing, Istio VirtualServices & Rollback Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Operations Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-904 Blue-Green Deployments
next_document: NES-906 Rollback Playbook
---

# NES-905 — Canary Releases

> **"Minimize blast radius by routing increments. We roll out updates progressively to limited user percentages and monitor system health using Istio."**

---

# Executive Summary

Even if a release passes staging audits (NES-801), real production workloads can expose hidden bugs, database connection leaks, or memory spikes under scale.

Routing 100% of user traffic to a new version immediately exposes the entire customer base to these risks.

We mandate the use of **Canary Releases** for all high-volume microservices at NeelStack.

This standard establishes our progressive routing rules, telemetry checks, and automated rollback triggers using **Istio**.

---

# Purpose

This standard defines:

- Progressive Traffic Shifting (Canary Steps)
- Canary Routing via Istio VirtualServices
- Automated Health Metrics Monitoring (Prometheus)
- Automated Rollback Triggers (SLA Violation)
- Deployment Verification Windows

---

# Progressive Traffic Shifting

Canary rollouts must follow a structured progressive weight shift over defined verification windows:

```text
  Phase 1 (Deploy): Route 1% of traffic to Canary. Verify for 15 minutes.
  Phase 2 (Promote): Route 10% of traffic to Canary. Verify for 30 minutes.
  Phase 3 (Scale): Route 50% of traffic to Canary. Verify for 1 hour.
  Phase 4 (Complete): Route 100% of traffic to Canary. Retire old version.
```

---

# Canary Routing via Istio

We implement traffic splitting inside the cluster using **Istio VirtualServices** (NES-513):

- **Target Weights**: The pipeline updates target weights inside the VirtualService manifest file dynamically.
- **Header Routing**: For validation runs, route traffic to Canary based on specific request headers (e.g. `X-Developer-Beta: true`) before opening access to general users.

```yaml
# Istio VirtualService Canary Routing example
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
        subset: stable # Production version
      weight: 90
    - destination:
        host: portal-api-service
        subset: canary # New version
      weight: 10
```

---

# Automated Health Monitoring

During canary promotion windows, monitor the **SRE Golden Signals (NES-516)** of the Canary subset dynamically:

- **Error Rates**: Compare Canary error rates against the stable version.
- **Latency (p95)**: Verify response times do not exceed baseline thresholds.
- **Resource Saturation**: Check pod CPU and memory logs for leak indicators.

---

# Automated Rollback Triggers

If a Canary run violates operational thresholds, the controller must abort the release automatically:

- **Trigger Parameters**:
  - HTTP 5xx error rates on Canary exceed **1%** over a 2-minute window.
  - Latency (p95) on Canary exceeds **500ms**.
  - Pod container reboots occur.
- **Reconciliation**: Instantly set VirtualService Canary weight to `0%` and alert the SRE on-call team.

---

# Anti-Patterns

❌ **Manual Traffic Swaps**: Updating canary weights manually via cloud dashboards instead of automating promotions using CI workflows.

❌ **Omitting Evaluation Windows**: Shifting weights from 1% to 100% in a few seconds without verifying performance logs.

❌ **Excluding Ingress Gateways from Canary Rules**: Routing traffic via DNS changes, which bypasses local pod load balancing and results in unequal load distributions.

---

# Production Checklist

- [ ] Istio destination rules define `stable` and `canary` subsets.
- [ ] Automated promotion pipeline scripts are verified.
- [ ] Prometheus metrics queries check Canary error rates.
- [ ] Automated rollback triggers are active.
- [ ] Access logs trace traffic allocation weights.

---

# Success Criteria

The Canary Release program is successful when:
- Buggy releases affect less than 5% of active users before triggering automated rollbacks.
- Automated rollback steps execute and isolate nodes in under 10 seconds.
- Performance regressions are detected and isolated in the EKS cluster.

---

# Document Status

**Document:** NES-905 — Canary Releases
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-906 — Rollback Playbook**
