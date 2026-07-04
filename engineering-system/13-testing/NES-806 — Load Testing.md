---
document_id: NES-806
title: Load Testing
subtitle: Enterprise Load Testing, Stress Profiling & k6 Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Quality Assurance Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-805 Performance Testing
next_document: NES-807 Security Testing
---

# NES-806 — Load Testing

> **"Scale is verified by execution. We write load test scripts using k6, simulate realistic user growth, and determine system failure thresholds."**

---

# Executive Summary

A system that performs correctly under single-user developer tests can fail under heavy load when thousands of concurrent customers query APIs.

Database connection pools, CPU allocations, network routing bandwidths, and caching nodes must be audited under realistic traffic loads.

We mandate the execution of **Load and Stress Testing** prior to any major service release or promotional business event.

This standard defines our load test scripting standard (**k6**), virtual user profiles, metric baselines, and stress testing targets.

---

# Purpose

This standard defines:

- Load Testing Tooling (k6)
- Standard Load Testing Scenarios
- Target Metrics and Thresholds
- Stress and Soak Testing Strategies
- Test Environment isolation

---

# Load Testing Tooling (k6)

We standardize on **k6** (written in JavaScript/Go) as our primary load testing engine.

- **Developer Friendly**: k6 scripts are written in standard Javascript, enabling developers to version test definitions inside application repositories.
- **Resource Efficient**: k6 compiles scripts to Go code, allowing single agent runners to generate thousands of concurrent virtual user (VU) threads without memory bottlenecks.

---

# Standard Load Testing Scenarios

Every load test plan must model realistic traffic patterns using three scenario formats:

1. **Load Test**: Gradually ramp up virtual users to expected normal peak levels (e.g. 1,000 concurrent users), hold for 30 minutes, and ramp down.
2. **Stress Test**: Push virtual users beyond expected limits (e.g. 5,000 concurrent users) to identify system breakdown boundaries, database connection exhaustion, or auto-scaling latencies.
3. **Soak Test**: Run system loads at average capacity (e.g. 500 concurrent users) for extended periods (e.g. 8 – 24 hours) to verify memory stability and catch resource leaks.

### Reference k6 Script:

```javascript
import http from 'k6/http';
import { sleep, check } from 'k6';

export const options = {
  stages: [
    { duration: '5m', target: 500 },  // Ramp-up to 500 users
    { duration: '20m', target: 500 }, // Hold load
    { duration: '5m', target: 0 },    // Ramp-down
  ],
  thresholds: {
    http_req_duration: ['p(95)<200'], // 95% of requests must complete under 200ms
    http_req_failed: ['rate<0.01'],    // Error rate must remain under 1%
  },
};

export default function () {
  const res = http.get('https://api-staging.neelstack.local/v1/students');
  check(res, {
    'status is 200': (r) => r.status === 200,
  });
  sleep(1);
}
```

---

# Performance Metric Thresholds

To pass verification gates, load runs must satisfy the following SLAs:

- **Success Rate**: Minimum **99%** of HTTP requests must return success (2xx/3xx statuses).
- **Latency (p95)**: 95% of API requests must complete in under **200ms**.
- **Error Budget**: Zero database connection drops or system crashes are permitted.

---

# Test Environment Isolation

Do not execute load tests against production clusters unless scheduling specific off-hour disaster recovery tests.

- **Dedicated Namespace**: Run load tests against staging namespaces containing isolated databases containing mock records matching production scale.
- **Third-Party Mocks**: Mock outbound integration endpoints (e.g. payment processors) during load runs to prevent incurring API charges or polluting third-party databases.

---

# Anti-Patterns

❌ **Testing over WAN**: Running load testing generators from personal machines over office Wi-Fi networks. This measures office network bottlenecks rather than backend limits. Execute test scripts from runners inside the target cloud VPC.

❌ **Running Load Tests without Cache Clearing**: Simulating thousands of requests targeting the identical user ID parameter, causing 100% cache hits and masking slow database query paths.

❌ **Omitting Stress Breakdown Audits**: Running load checks without identifying the exact user threshold that causes the system to crash, leaving operations teams blind during traffic spikes.

---

# Production Checklist

- [ ] k6 test scripts are version-controlled.
- [ ] Staging database scale matches production sizing.
- [ ] Third-party integration endpoints are mocked.
- [ ] Auto-scaling metrics are active and monitored during runs.
- [ ] Load results are recorded in the central platform dashboard.

---

# Success Criteria

The Load Testing program is successful when:
- System performance limits are verified under load.
- Auto-scaling rules spin up compute nodes to maintain latency targets under stress.
- Performance regressions are caught in staging prior to production updates.

---

# Document Status

**Document:** NES-806 — Load Testing
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-807 — Security Testing**
