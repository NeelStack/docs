---
document_id: NES-204
title: Authorization (RBAC & Permissions)
subtitle: Enterprise Authorization, Role-Based Access Control (RBAC), Permission & Policy Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Chief Solution Architect
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-203 Authentication & Identity
next_document: NES-205 Multi-Tenancy Architecture
---

# NES-204 — Authorization (RBAC & Permissions)

> **"Authentication identifies who you are. Authorization determines what you are allowed to do."**

---

# Executive Summary

Authorization is the mechanism that determines whether an authenticated identity can perform a specific action on a specific resource.

NeelStack adopts a **Policy-Based Role-Based Access Control (RBAC)** model that combines:

- Role-Based Access Control (RBAC)
- Fine-Grained Permissions
- Resource-Level Authorization
- Attribute-Based Rules (ABAC where required)
- Multi-Tenant Isolation
- API Authorization
- Service Authorization

Authorization must be:

- Consistent
- Centralized
- Auditable
- Extensible
- Secure

---

# Purpose

This standard defines:

- Authorization Architecture
- RBAC Model
- Permission Model
- Policy Engine
- Resource Ownership
- Tenant Isolation
- API Authorization
- Service Authorization
- Permission Evaluation
- Audit & Governance

---

# Authorization Philosophy

```
Identity

↓

Authentication

↓

Roles

↓

Permissions

↓

Policies

↓

Business Rules

↓

Access Decision
```

Authentication proves identity.

Authorization grants capability.

---

# Core Principles

Every authorization system must be:

✓ Least Privilege

✓ Deny by Default

✓ Explicit

✓ Auditable

✓ Centralized

✓ Extensible

✓ Fast

✓ Stateless

---

# Authorization Architecture

```text
                User

                  │

          Authentication

                  │

             JWT Claims

                  │

        Authorization Layer

                  │

        Policy Evaluation Engine

                  │

        Resource Permission Check

                  │

            Business Logic
```

Authorization occurs before business execution.

---

# Authorization Flow

```text
HTTP Request

↓

Authentication

↓

Extract Roles

↓

Extract Permissions

↓

Evaluate Policies

↓

Evaluate Tenant

↓

Evaluate Ownership

↓

Access Granted / Denied
```

Every request follows this flow.

---

# RBAC Model

NeelStack follows a hierarchical RBAC model.

```text
Platform

↓

Organization

↓

Workspace

↓

Project

↓

Resource
```

Permissions cascade downward unless explicitly restricted.

---

# Role Hierarchy

Example

```text
Platform Owner

↓

Platform Admin

↓

Organization Owner

↓

Organization Admin

↓

Manager

↓

Editor

↓

Contributor

↓

Viewer

↓

Guest
```

Roles inherit permissions from lower levels only where explicitly configured.

---

# Permission Structure

Permission naming convention

```text
resource.action
```

Examples

```text
student.read

student.create

student.update

student.delete

course.publish

invoice.approve

user.invite

role.assign
```

All permissions follow this convention.

---

# Permission Categories

Business

```text
student.*

teacher.*

course.*

finance.*
```

Platform

```text
user.*

role.*

tenant.*

audit.*
```

Infrastructure

```text
deployment.*

monitoring.*

logs.*

backup.*
```

---

# Resource Model

Authorization evaluates:

```text
Subject

↓

Action

↓

Resource

↓

Context

↓

Decision
```

Example

```text
User

↓

Update

↓

Student

↓

Tenant

↓

Allowed
```

---

# Ownership Rules

Some resources belong to specific users.

Example

```text
User

↓

Own Profile

↓

Allowed

User

↓

Other Profile

↓

Denied
```

Ownership is evaluated after permission checks.

---

# Policy Engine

The authorization engine evaluates:

- Role
- Permission
- Tenant
- Ownership
- Resource State
- Business Rules
- Time (optional)
- Location (optional)

Policies remain independent of application code.

---

# RBAC vs ABAC

RBAC

```
Role

↓

Permission

↓

Decision
```

ABAC

```
User Attributes

↓

Resource Attributes

↓

Environment

↓

Decision
```

RBAC is the default.

ABAC is used for advanced enterprise scenarios.

---

# JWT Claims

Example

```json
{
  "sub":"user-123",
  "tenant":"tenant-1",
  "roles":[
      "manager"
  ],
  "permissions":[
      "student.read",
      "student.update"
  ]
}
```

Permissions should remain compact.

Large permission sets should be resolved server-side.

---

# API Authorization

Every endpoint defines required permissions.

Example

```python
@require_permission(
    "student.create"
)
```

Authorization should remain declarative.

---

# Service Authorization

Internal services authenticate using service identities.

Each service has its own permissions.

Example

```text
notification.send

analytics.read

audit.write

workflow.execute
```

Never use administrator permissions for services.

---

# Tenant Isolation

Every request verifies:

```text
Authenticated User

↓

Tenant

↓

Resource Tenant

↓

Match?

↓

Allowed
```

Cross-tenant access is prohibited.

---

# Resource-Level Authorization

Permission alone is insufficient.

Example

```text
Can Update Student

AND

Student belongs to Tenant

AND

Student is Active
```

Business rules remain in the domain layer.

---

# Temporary Permissions

Support:

- Time-limited access
- Emergency access
- Approval-based access
- Break-glass access

Temporary permissions expire automatically.

---

# Delegation

Users may delegate permissions.

Example

```text
Manager

↓

Delegate

↓

Approver

↓

7 Days
```

Delegation must be audited.

---

# Permission Resolution

Evaluation order

```text
Authentication

↓

Tenant

↓

Role

↓

Permission

↓

Policy

↓

Ownership

↓

Business Rule

↓

Decision
```

---

# Deny by Default

If no rule grants access

↓

Access Denied

Never assume permission.

---

# Permission Caching

Cache

- Roles
- Policies
- Permissions

Invalidate immediately after changes.

Security always overrides cache performance.

---

# Administration

Platform administrators manage

- Roles
- Permissions
- Policies
- Assignments
- Delegation

All changes require audit logging.

---

# Audit Logging

Record

- Permission Granted
- Permission Revoked
- Role Assigned
- Role Removed
- Access Denied
- Policy Updated
- Delegation Created
- Emergency Access

Audit records are immutable.

---

# Observability

Track

- Authorization Latency
- Access Denials
- Permission Usage
- Policy Evaluations
- Role Distribution
- Failed Authorization Attempts

Authorization should be measurable.

---

# Performance

Target

Authorization evaluation

```
<10ms
```

Permission cache hit

```
>95%
```

---

# Folder Structure

```text
authorization/

├── api/

├── application/

├── domain/

├── policies/

├── permissions/

├── roles/

├── evaluators/

├── cache/

├── events/

└── tests/
```

---

# Example Permission Matrix

| Resource | Viewer | Editor | Manager | Admin |
|----------|--------|--------|---------|-------|
| Student | Read | CRUD | CRUD | CRUD |
| Course | Read | Update | CRUD | CRUD |
| Users | None | None | Read | CRUD |
| Roles | None | None | None | CRUD |
| Audit Logs | None | Read | Read | CRUD |

---

# Anti-Patterns

Avoid

❌ Hardcoded Role Checks

❌ if user.is_admin

❌ Permission Logic in Controllers

❌ Duplicate Permission Names

❌ Cross-Tenant Access

❌ Shared Admin Accounts

❌ Missing Audit Logs

❌ Business Rules Inside Middleware

❌ Wildcard Permissions

❌ Permission Checks in Frontend Only

---

# Production Checklist

Before production

- [ ] RBAC implemented
- [ ] Permission model documented
- [ ] Policies reviewed
- [ ] Tenant isolation verified
- [ ] Ownership rules implemented
- [ ] Service permissions defined
- [ ] Audit logging enabled
- [ ] Permission cache configured
- [ ] Security review completed
- [ ] Authorization tests passing

---

# Success Criteria

Authorization is successful when:

- Least privilege is enforced.
- Every request undergoes authorization.
- Tenant isolation is guaranteed.
- Roles remain simple.
- Permissions remain granular.
- Policies remain maintainable.
- Service identities follow least privilege.
- All authorization decisions are auditable.

---

# Future Evolution

Version 2.0 will include:

- Open Policy Agent (OPA) Integration
- Cedar Policy Language Evaluation
- Zanzibar-Style Authorization Model
- Relationship-Based Access Control (ReBAC)
- Fine-Grained Object-Level Security
- Dynamic Policy Engine
- Graph-Based Permission Evaluation
- Multi-Region Authorization Architecture
- Policy Simulation & Testing Tools
- Authorization Administration Portal
- Enterprise Approval Workflows
- AI-Assisted Policy Generation
- C4 Authorization Architecture
- Authorization Sequence Diagrams
- FastAPI Authorization Reference Implementation

---

# Authorization Checklist

- [x] Authorization Architecture Defined
- [x] RBAC Model Established
- [x] Permission Standards Defined
- [x] Policy Engine Defined
- [x] Resource Ownership Model Added
- [x] Tenant Isolation Included
- [x] Service Authorization Defined
- [x] Audit & Observability Included
- [x] Performance Targets Added
- [x] Anti-Patterns Listed
- [x] Production Checklist Added
- [x] Success Criteria Defined

---

# Document Status

**Document:** NES-204 — Authorization (RBAC & Permissions)

**Version:** 1.0.0

**Status:** Ready for Architecture Review

**Next Document:** **NES-205 — Multi-Tenancy Architecture**

---

# Revision Queue for Version 2.0 (Enterprise Edition)

Future enhancements will include:

- Complete RBAC Database Schema
- Permission Registry & Naming Guide
- OPA/Cedar Integration Blueprint
- Google Zanzibar-inspired Authorization Model
- Relationship-Based Access Control (ReBAC)
- Multi-Tenant Permission Inheritance
- Policy Versioning & Lifecycle Management
- Permission Dependency Graph
- Authorization Performance Benchmark Suite
- AI Authorization Governance
- Enterprise Admin Portal for Role Management
- C4 Component & Deployment Diagrams
- UML Sequence Diagrams for Permission Evaluation
- Architecture Fitness Tests for Authorization
- Production FastAPI Authorization Reference Project

These enhancements will establish the definitive authorization framework for every NeelStack application, ensuring secure, scalable, auditable, and enterprise-grade access control across web, mobile, APIs, AI services, and platform infrastructure.