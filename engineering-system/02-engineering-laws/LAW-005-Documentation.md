---
document_id: LAW-005
title: Documentation
subtitle: All public APIs, domain models, and architectural decisions must be documented before merging
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Chief Architect
review_cycle: Annual
document_type: Engineering Law
parent_document: LAW-004 Observability
next_document: LAW-006 Testing
---

# LAW-005 — Documentation

> **"Code without documentation is a black box. APIs without documentation are liabilities. Architecture without records is archaeology."**

---

## Law Statement

**All public APIs, domain models, architectural decisions, and engineering standards MUST be documented. Documentation is not optional — it is a deliverable. No feature is complete until its documentation is merged.**

---

## Documentation Requirements by Artifact Type

### API Endpoints
Every API endpoint must have:
- OpenAPI/Swagger specification (auto-generated or hand-authored)
- Request/response schema with field descriptions
- Error codes and their meanings
- Authentication requirements
- Rate limiting information
- At least one example request/response

### Domain Models
Every domain aggregate and entity must have:
- Field-level descriptions in code (docstrings/comments)
- Business rules documented in the domain service
- State transitions documented (if stateful)

### Architectural Decisions
Every significant architectural decision must be recorded as an **ADR** (Architecture Decision Record) in `19-adrs/` using the standard template:
- Context
- Decision
- Consequences
- Alternatives Considered

### Engineering Standards
Any new platform pattern, framework adoption, or process must be captured as a **NES document** in the appropriate folder of `engineering-system/`.

---

## "Definition of Done" for Documentation

A feature is not done until:
- [ ] API docs updated (if API changed)
- [ ] README updated (if behavior changed)
- [ ] ADR created (if architectural decision made)
- [ ] NES updated or created (if new engineering standard established)
- [ ] CHANGELOG entry added

---

## Anti-Patterns

❌ "The code is the documentation."  
❌ Documenting after the fact — documentation written six months later is often wrong.  
❌ Documentation in Confluence/Notion that is never linked from the repo.  
❌ Undocumented breaking changes in APIs.

---

## Related Standards

- NES-109 — Architecture Decision Records
- NES-318 — Frontend Documentation Standards
- LAW-003 — API Versioning
- CONTRIBUTING.md

---

## Version History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2026-07-04 | NeelStack Engineering | Initial publication |
