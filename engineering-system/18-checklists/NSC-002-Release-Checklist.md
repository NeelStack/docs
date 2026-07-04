---
document_id: NSC-002
title: Production Release Checklist
subtitle: Mandatory steps before any release is deployed to production
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Engineering Leadership
document_type: Checklist
---

# NSC-002 — Production Release Checklist

This checklist must be completed before any service version is deployed to production. The release manager signs off on each item.

---

## Pre-Release Validation

### Code Quality
- [ ] All CI checks passing on the release branch
- [ ] Test coverage ≥ thresholds (see LAW-006)
- [ ] No open P1 bugs on the milestone
- [ ] Security scan (Trivy, Bandit, npm audit) — no HIGH/CRITICAL findings

### Testing
- [ ] Unit tests: 100% passing
- [ ] Integration tests: 100% passing
- [ ] E2E tests on staging: 100% passing for critical user journeys
- [ ] Load test completed (if new feature changes traffic patterns)
- [ ] Regression test suite executed

### Infrastructure
- [ ] Staging deployment successful with no errors
- [ ] Database migrations tested on staging with production data snapshot
- [ ] Rollback plan documented and tested
- [ ] Feature flags configured (if using feature flags for this release)

## Release Preparation

- [ ] CHANGELOG.md updated with this version's changes
- [ ] Git tag created (`v{MAJOR}.{MINOR}.{PATCH}`)
- [ ] GitHub Release created with release notes
- [ ] Migration guide written (if MAJOR version)
- [ ] Communication sent to affected teams

## Deployment

- [ ] Deployment performed via CI/CD (no manual `kubectl apply` in production)
- [ ] Canary deployment initiated (5% traffic → 25% → 100%)
- [ ] Health checks passing at each canary stage
- [ ] Error rate monitored during rollout (< 0.1% acceptable)
- [ ] p99 latency monitored during rollout (≤ pre-release baseline)

## Post-Release Verification

- [ ] All services healthy in Kubernetes (kubectl get pods)
- [ ] Grafana dashboards showing normal metrics
- [ ] No spike in error logs (OpenSearch/CloudWatch)
- [ ] Smoke tests executed against production
- [ ] On-call engineer notified and monitoring for 1 hour post-deploy

## Sign-off

| Role | Name | Signature | Date |
|---|---|---|---|
| Release Manager | | | |
| QA Lead | | | |
| On-call Engineer | | | |

---

*Related: NES-900 — Release Management | NES-904 — Blue-Green Deployments | NES-906 — Rollback Playbook*
