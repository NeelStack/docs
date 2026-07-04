---
document_id: NES-502
title: Kubernetes
subtitle: Enterprise Kubernetes Orchestration, Probes, Resources & Manifest Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-501 Docker
next_document: NES-503 Terraform
---

# NES-502 — Kubernetes

> **"Kubernetes coordinates our service scale. We write declarative, structured manifests with strict resource limits and automated health checks."**

---

# Executive Summary

Kubernetes is the core runtime platform for all NeelStack backend services, APIs, databases, and AI pipelines.

Unconfigured deployment manifests can cause resource starvation, cluster-wide node failure, slow recoveries, and application downtime during releases.

This standard establishes the mandatory manifest structures, resource constraints, scaling policies, and health monitoring guidelines.

---

# Purpose

This standard defines:

- Resource Requests and Limits
- Health Probes (Startup, Liveness, Readiness)
- Pod Security Context Settings
- Horizontal Pod Autoscaler (HPA) Rules
- Manifest Naming and Annotations

---

# Resource Requests & Limits

Every Pod container configuration must declare resource `requests` (what the scheduler guarantees the container on boot) and `limits` (the maximum resources the container can consume before termination).

- **Requests**: Serves as the basis for node scheduling. Set requests based on average CPU/Memory consumption.
- **Limits**: Prevents resource starvation on host nodes.
  - **Memory**: Limits must equal requests where possible to prevent OOM-killing (Out-Of-Memory) due to unexpected node swapping.
  - **CPU**: Limit throttling is acceptable, but requests should be set high enough to handle normal application loads.

### Reference YAML snippet:

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

---

# Health Probes

Probes tell Kubernetes if a container is running, ready to accept traffic, or needs a reboot.

- **Startup Probe**: Tracks slow-starting applications. Kubernetes pauses other probes until this completes.
- **Readiness Probe**: Determines if the container can receive network traffic. If this fails, the container is removed from the service endpoints.
- **Liveness Probe**: Determines if the container needs a reboot. If this fails, Kubernetes kills and restarts the Pod.

### Probe Configuration:

```yaml
startupProbe:
  httpGet:
    path: /health/startup
    port: 8000
  failureThreshold: 30
  periodSeconds: 10
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 10
livenessProbe:
  httpGet:
    path: /health/live
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 15
```

---

# Pod Security Context

To secure the host cluster nodes, pods must run with restricted security settings.

- **Non-Root**: Set `runAsNonRoot: true`.
- **Privilege Escalation**: Disable privilege escalation.
- **Read-Only Root Filesystem**: Configure the container root filesystem as read-only. Use temporary volumes (`emptyDir`) for write directories like `/tmp`.

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 10001
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop:
      - ALL
```

---

# Autoscaling Policy (HPA)

Every production deployment must include a **HorizontalPodAutoscaler (HPA)** configuration to adapt to traffic spikes automatically.

- **Target Metric**: Scale based on CPU and Memory usage benchmarks.
- **Minimum Replica Limit**: 3 instances (ensures high availability across different cloud availability zones).
- **Scale Up Target**: Trigger scaling when average usage exceeds 75%.

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: portal-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: portal-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 75
```

---

# Anti-Patterns

❌ **Omitting Resource Constraints**: Deploying Pods without CPU/Memory resource boundaries, which can cause a single leaky container to consume all node memory and crash the host.

❌ **Using Liveness Probe as Readiness**: Pointing the liveness probe to database status endpoints. If the database goes down, all your web pods will reboot repeatedly, worsening the outage. Liveness should only monitor container shell responsiveness.

❌ **Binding directly to Host Network Ports**: Deploying containers that bind directly to host network ports, which blocks multi-replica deployments on the same node.

---

# Production Checklist

- [ ] All deployments have defined CPU and Memory requests and limits.
- [ ] Startup, readiness, and liveness probes are configured.
- [ ] `runAsNonRoot` is set to `true` inside the pod spec.
- [ ] Deployments include an active HPA resource configuration.
- [ ] Pod Anti-Affinity is defined (prevents multiple copies of the same service from rendering on the same physical node).

---

# Success Criteria

The Kubernetes configuration is successful when:
- Clusters handle node failures seamlessly without application downtime.
- Pods autoscale within 60 seconds of traffic spikes.
- Restarts from resource leaks (OOM) occur safely without affecting active customer sessions.

---

# Document Status

**Document:** NES-502 — Kubernetes
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-503 — Terraform**
