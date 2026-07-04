---
document_id: REPO-006
title: Code Ownership
subtitle: Every file and domain in NeelStack repositories has an explicitly assigned owner
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Engineering Leadership
review_cycle: Quarterly
document_type: Repository Standard
parent_document: REPO-005 Import Rules
next_document: REPO-007 Versioning
---

# REPO-006 — Code Ownership

---

## Ownership Principle

Every file, directory, and service in NeelStack repositories has an assigned **owner**. Owners are responsible for:
- Review approval of PRs affecting their code
- Maintaining documentation and tests
- Responding to incidents involving their code
- Technical debt management

---

## CODEOWNERS File

Every repository must have a `.github/CODEOWNERS` file defining ownership:

```
# Global fallback
* @NeelStack/engineering-leads

# Engineering System Documentation
/engineering-system/00-foundation/ @NeelStack/cto @NeelStack/architects
/engineering-system/01-architecture/ @NeelStack/architects
/engineering-system/05-backend/ @NeelStack/backend-team
/engineering-system/06-frontend/ @NeelStack/frontend-team
/engineering-system/07-mobile/ @NeelStack/mobile-team
/engineering-system/09-ai/ @NeelStack/ai-team
/engineering-system/11-security/ @NeelStack/security-team

# Infrastructure
/infra/ @NeelStack/platform-team
/.github/ @NeelStack/platform-team
```

## Domain Ownership Registry

| Domain | Owning Team | Lead Engineer |
|---|---|---|
| Identity & Auth | Backend Core | TBD |
| Tenancy | Platform | TBD |
| Enrollment | EduOS Team | TBD |
| Billing | Backend Core | TBD |
| AI Platform | AI Team | TBD |
| Frontend Platform | Frontend Team | TBD |
| Mobile | Mobile Team | TBD |
| Infrastructure | Platform Team | TBD |

## Ownership Transfer

Ownership transfers require:
1. Written approval from Engineering Lead
2. Updated CODEOWNERS file
3. Knowledge transfer session documented
4. 30-day shadow period for the new owner

## Related Standards

- LAW-002 — Domain Ownership
- REPO-001 — Monorepo Architecture
- NES-1106 — Engineering Career Ladder

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-07-04 | Initial publication |
