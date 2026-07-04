---
document_id: NES-909
title: Incident Post-Mortems
subtitle: Enterprise Blame-Free Post-Mortem & Root Cause Analysis (RCA) Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Operations Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-908 Runbooks & Playbooks
next_document: NES-910 Game Days & Chaos Engineering
---

# NES-909 — Incident Post-Mortems

> **"Failure is an opportunity to learn. We conduct blame-free post-mortems to identify system vulnerabilities, document root causes, and prevent regressions."**

---

# Executive Summary

Outages and system degradation present opportunities to improve platform resilience.

If incidents are resolved without documenting lessons, or if post-mortem reviews focus on assigning blame, engineering teams will hide mistakes, and similar failures will recur.

We mandate a **Blame-Free Post-Mortem** process for all SEV-1 and SEV-2 operational incidents (NES-518).

This standard defines the root cause analysis (RCA) meeting schedules, reporting templates, timeline reconstructions, and corrective task tracking.

---

# Purpose

This standard defines:

- Blame-Free Post-Mortem Culture
- Post-Mortem Timeline and Review Schedules (SLA: 48 Hours)
- Standardized RCA Document Template
- Timeline Reconstruction Guidelines
- Action Item Tracking and SLA Gates

---

# Blame-Free Culture

We focus post-mortem reviews on systems and processes, not human errors:

- **Systemic Analysis**: We assume that engineers act in good faith with the information available. We ask: "Why did the system allow this action?" or "How can we improve diagnostic logging?" rather than "Who caused the crash?".
- **Psychological Safety**: By removing blame, engineers can report and analyze errors transparently.

---

# Post-Mortem Schedule & SLA

To capture accurate details while memory is fresh:

- **SLA**: A formal Post-Mortem Review meeting must occur within **48 hours** of resolving any SEV-1 incident.
- **Audience**: Required attendees include the Incident Commander, developers involved in diagnostics, data stewards, and the domain Product Manager.

---

# Standardized Post-Mortem Template

All post-mortem documents must be stored in the central operations registry and follow the standard structure:

```markdown
# Incident Post-Mortem: [Incident ID / Date]

## Executive Summary
A 3-sentence summary detailing what failed, the customer impact, and the resolution.

## Incident Metrics
- **Severity**: SEV-1
- **Time to Detect (MTTD)**: 5 Minutes
- **Time to Resolve (MTTR)**: 45 Minutes
- **Total Customer Impact**: 1,200 users experienced checkout failures.

## Root Cause Analysis (The 5 Whys)
Detailed analysis explaining *why* the failure occurred (using 5 Whys framework).

## Timeline Reconstruction
- **12:00 UTC**: Deployment pipeline runs.
- **12:05 UTC**: Alert DatabaseCPUSpike triggers.
- **12:10 UTC**: Incident Commander initiates rollback.
- **12:15 UTC**: Rollback completes, metrics normalize.

## Corrective Actions
List of Jira action items to prevent recurrence.
```

---

# Timeline Reconstruction

Timelines must be rebuilt using absolute timestamps derived from system logs, metrics databases, and chat history.

- Document the exact time the deployment ran, the first alert triggered, the SRE team acknowledged, routing changed, and metrics normalized.
- Include links to specific OpenSearch logs or Grafana dashboards to verify timeline events.

---

# Action Item Tracking & SLAs

A post-mortem is successful only if it results in actionable system improvements:

- **Action Prefix**: All corrective tickets in Jira must be prefixed with `RCA-FIX` (e.g. `RCA-FIX-987: Add db index to user email search`).
- **SLA**: `RCA-FIX` tickets must be scheduled, built, and deployed within **two sprint cycles** of the post-mortem.

---

# Anti-Patterns

❌ **Skipping Minor Incidents**: Omitting post-mortems for SEV-2 failures because "the database didn't crash," missing early indicators of larger failures.

❌ **Focusing on Operator Actions**: Listing "Engineer typed wrong command" as the root cause instead of identifying why the interface permitted invalid inputs.

❌ **Leaving Action Items Unresolved**: Logging corrective tickets but leaving them in the backlog indefinitely, leading to recurring outages.

---

# Production Checklist

- [ ] Post-Mortem meetings schedule is active.
- [ ] RCA template is configured in the operations database.
- [ ] Timeline metrics compile logs automatically.
- [ ] `RCA-FIX` tickets are tracked in Jira.
- [ ] Post-mortem reviews are published to the engineering team.

---

# Success Criteria

The Incident Post-Mortem program is successful when:
- 100% of SEV-1 incidents have a completed post-mortem within 48 hours of resolution.
- Engineering teams can demonstrate that repeat failures are prevented by previous corrective actions.
- Post-mortem reports are shared openly to support organization-wide learning.

---

# Document Status

**Document:** NES-909 — Incident Post-Mortems
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-910 — Game Days & Chaos Engineering**
