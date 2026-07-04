---
document_id: RFC-001
title: Unified API Gateway Strategy
status: Draft
date: 2026-07-04
author: Architecture Team
reviewers: Backend Lead, Platform Lead, Security Lead
discussion_deadline: 2026-08-04
---

# RFC-001 — Unified API Gateway Strategy

## Summary

This RFC proposes establishing a unified API Gateway layer across all NeelStack services, standardizing authentication, rate limiting, routing, and observability at the edge.

## Motivation

Currently, each service handles authentication and rate limiting independently. This creates:
- Inconsistent auth behavior across services
- Duplicate rate limiting code
- No centralized request logging
- No single point for API versioning enforcement

## Proposal

Deploy **Traefik** or **Kong** as the unified API gateway for all services:

```
Client Request
     │
     ▼
API Gateway (Kong/Traefik)
├── JWT Validation
├── Rate Limiting (per tenant)
├── Request Logging (OpenTelemetry)
├── Route to Service
└── Response Headers (CORS, Security)
     │
     ▼
Upstream Service (FastAPI)
```

### Gateway Responsibilities
- JWT token validation (call identity service once, cache result)
- Rate limiting: per-tenant, per-endpoint configurable limits
- Request/response logging with trace propagation
- API version routing (`/v1/` → v1 deployment, `/v2/` → v2 deployment)
- CORS headers
- Security headers (CSP, HSTS, etc.)

### Service Responsibilities (post-gateway)
- Business authorization (RBAC — who can do what)
- Business logic
- Data access

## Alternatives Considered

| Alternative | Notes |
|---|---|
| AWS API Gateway | Vendor lock-in, complex Terraform management |
| Nginx | Limited plugin ecosystem for dynamic auth |
| Service mesh only (Istio) | Too complex for current team size |

## Open Questions

1. Should we use Kong (plugin-rich) or Traefik (simpler, K8s-native)?
2. Should the gateway validate JWTs or delegate to a dedicated auth service?
3. How do we handle websocket connections through the gateway?

## Next Steps

- [ ] ARB review and vote
- [ ] Proof of concept with top 2 candidates
- [ ] Performance benchmarking under 10,000 RPS load
- [ ] Security review of chosen solution
- [ ] ADR written after decision

## Related Standards

- NES-202 — API Design Standards
- NES-203 — Authentication & Identity
- LAW-003 — API Versioning
- NES-512 — Networking
