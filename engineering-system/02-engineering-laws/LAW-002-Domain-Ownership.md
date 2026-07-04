---
document_id: LAW-002
title: Domain Ownership
subtitle: Every piece of data and every business capability must have a single owning domain
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Chief Architect
review_cycle: Annual
document_type: Engineering Law
parent_document: LAW-001 Business Logic
next_document: LAW-003 API Versioning
---

# LAW-002 — Domain Ownership

> **"If two teams own the same data, nobody owns it. Shared ownership is the root of data corruption, inconsistency, and architectural debt."**

---

## Law Statement

**Every entity, aggregate, and business capability MUST have exactly one owning domain. No domain may write to data owned by another domain.**

---

## Ownership Rules

1. **Single Writer**: Only the owning domain may write, update, or delete its entities.
2. **Read by Contract**: Other domains may read cross-domain data only via published APIs or events — never via direct database joins.
3. **No Shared Tables**: Two domains must never share a database table as a write target.
4. **Event-Based Integration**: Cross-domain workflows are coordinated via domain events, not shared state.

---

## Domain Ownership Map (NeelStack Reference)

| Domain | Owns | Published Events |
|---|---|---|
| **Identity** | Users, Roles, Sessions, Permissions | UserCreated, RoleAssigned |
| **Tenancy** | Tenants, Plans, Subscriptions | TenantProvisioned, PlanChanged |
| **Enrollment** | Enrollments, CourseRegistrations | StudentEnrolled, CourseCompleted |
| **Billing** | Invoices, Payments, Subscriptions | InvoiceGenerated, PaymentProcessed |
| **Notifications** | Notification templates, Delivery logs | NotificationSent |
| **Content** | Courses, Lessons, Assessments | CoursePublished, LessonUpdated |
| **Analytics** | Events, Aggregations, Reports | (read-only, no writes to other domains) |

---

## Anti-Patterns

❌ **Cross-domain DB JOIN**: `SELECT u.name, e.course FROM users u JOIN enrollments e` — Users table is owned by Identity, Enrollments by Enrollment domain.

❌ **Shared Write Table**: Both Billing and Enrollment writing to the same `student_courses` table.

❌ **Implicit Ownership**: No documented owner — "everyone can modify it."

---

## Enforcement

- Domain boundaries must be documented in the Context Map (NES-1419).
- Architecture Review Board (NES-1103) approves any new cross-domain data access pattern.
- All database tables must have a `domain_owner` label in schema migrations.

---

## Related Standards

- NES-103 — Domain-Driven Design
- NES-1419 — Domain Context Maps
- LAW-001 — Business Logic
- NES-1103 — Architecture Review Board

---

## Version History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2026-07-04 | NeelStack Engineering | Initial publication |
