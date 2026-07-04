---
document_id: NSC-004
title: Architecture Review Checklist
subtitle: Checklist for Architecture Review Board sessions and architecture design reviews
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Architecture Review Board
document_type: Checklist
---

# NSC-004 — Architecture Review Checklist

Use this checklist when presenting a new architecture design to the ARB or conducting an architecture review.

---

## Design Completeness
- [ ] C4 Level 1 (Context diagram) present
- [ ] C4 Level 2 (Container diagram) present
- [ ] Data flow diagram showing all data stores and external systems
- [ ] API contracts defined (OpenAPI spec or equivalent)
- [ ] Domain ownership documented — who owns what data?

## Architecture Principles Compliance (NES-100)
- [ ] Follows Clean Architecture layer boundaries (LAW-010)
- [ ] Business logic in domain layer (LAW-001)
- [ ] Single domain owns each entity (LAW-002)
- [ ] API versioning strategy defined (LAW-003)
- [ ] Observability strategy defined (LAW-004)

## Technology Compliance
- [ ] All technologies from approved stack (TECH-001)
- [ ] Any deviations have documented rationale
- [ ] New dependencies evaluated per REPO-004

## Data Architecture
- [ ] Multi-tenant isolation strategy defined (NES-205)
- [ ] Data retention policy defined
- [ ] PII data identified and protection strategy documented
- [ ] Database schema and migration strategy documented

## Scalability & Performance
- [ ] Expected load defined (RPS, concurrent users)
- [ ] Scaling strategy defined (horizontal? vertical?)
- [ ] Performance SLAs defined per LAW-008
- [ ] Bottlenecks identified and mitigation planned

## Resilience
- [ ] Single points of failure identified
- [ ] Failover strategy for each SPOF
- [ ] Disaster recovery plan (RTO/RPO defined)
- [ ] Circuit breaker pattern applied to external dependencies

## Security
- [ ] Threat model completed (NES-602)
- [ ] Authentication strategy defined
- [ ] Network boundaries and trust zones defined
- [ ] Data encryption at rest and in transit

## Operations
- [ ] Monitoring and alerting strategy (LAW-004)
- [ ] Runbook draft available
- [ ] Deployment strategy defined (blue-green, canary)
- [ ] Rollback plan documented

## ADR
- [ ] ADR drafted for this architectural decision
- [ ] Alternatives considered and documented

---

*Related: NES-1103 — Architecture Review Board | NES-100 — Architecture Principles | NES-109 — ADRs*
