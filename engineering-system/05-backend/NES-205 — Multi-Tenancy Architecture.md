---
document_id: NES-205
title: Multi-Tenancy Architecture
subtitle: Enterprise Multi-Tenant Architecture Standard for the NeelStack Platform
version: 1.0.0
status: Draft
classification: Internal
owner: Chief Solution Architect
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-204 Authorization (RBAC & Permissions)
next_document: NES-206 Data Architecture
---

# NES-205 — Multi-Tenancy Architecture

> **"A tenant must behave as though they own the entire platform, while sharing the same infrastructure securely with thousands of others."**

---

# Executive Summary

Every NeelStack product is designed as a **cloud-native multi-tenant SaaS platform**.

Whether serving:

- Schools
- Colleges
- Hospitals
- Enterprises
- Government Organizations
- SMEs
- Individual Businesses

each customer (tenant) must experience complete logical isolation while benefiting from shared infrastructure.

Multi-tenancy is a core architectural capability—not an afterthought.

---

# Purpose

This document defines:

- Multi-Tenant Architecture
- Tenant Isolation
- Tenant Lifecycle
- Data Isolation
- Authentication
- Authorization
- Configuration
- Storage
- Billing
- Deployment
- Scaling
- Security
- Governance

This standard applies to every NeelStack product.

---

# Vision

Build a platform capable of securely serving:

- Millions of Users
- Hundreds of Thousands of Organizations
- Thousands of Custom Domains
- Multiple Geographic Regions

from a unified platform architecture.

---

# Multi-Tenancy Philosophy

```text
Platform

↓

Tenant

↓

Workspace

↓

Users

↓

Resources

↓

Business Data
```

Every resource belongs to exactly one tenant.

---

# Guiding Principles

Every tenant must have:

✓ Complete Data Isolation

✓ Independent Configuration

✓ Independent Branding

✓ Independent Users

✓ Independent Permissions

✓ Independent Billing

✓ Independent Audit Trail

✓ Independent Backups

---

# Tenant Definition

A tenant represents an independent customer organization.

Examples

```
ABC School

XYZ Hospital

ToolVines Customer

LifeAsia Pharmaceuticals

Acme Corporation
```

Each tenant owns its business data.

---

# Multi-Tenant Architecture

```text
                 Platform

                    │

      ┌─────────────┼─────────────┐

      │             │             │

 Tenant A      Tenant B      Tenant C

      │             │             │

 Users        Users        Users

      │             │             │

 Resources    Resources    Resources

      │             │             │

 PostgreSQL (Logical Isolation)
```

Infrastructure is shared.

Business data is isolated.

---

# Tenant Isolation Model

NeelStack adopts:

## Logical Database Isolation

```
Shared PostgreSQL Cluster

↓

Shared Database

↓

Shared Tables

↓

Tenant ID

↓

Row-Level Isolation
```

This is the default architecture.

---

# Future Isolation Options

Support future migration to:

- Database per Tenant
- Schema per Tenant
- Dedicated Cluster
- Dedicated Region

Architecture should support seamless migration.

---

# Tenant Identifier

Every resource includes:

```
tenant_id
```

Example

```text
student

course

invoice

notification

audit_log
```

Tenant ID is mandatory.

---

# Request Flow

```text
Client

↓

Authentication

↓

Tenant Resolution

↓

Authorization

↓

Business Logic

↓

Database Filter

↓

Response
```

Tenant context is established before business logic.

---

# Tenant Resolution

Tenant identification may occur via:

- JWT Claims
- Custom Domain
- Subdomain
- HTTP Header
- API Key
- Service Identity

Priority

```
JWT

↓

Subdomain

↓

Custom Domain

↓

Header
```

---

# Tenant Context

Every request receives a Tenant Context.

Contains

- Tenant ID
- Organization Name
- Region
- Subscription
- Features
- Branding
- Timezone
- Locale

Tenant Context is immutable during request execution.

---

# Data Isolation

Every query automatically filters by:

```sql
tenant_id
```

Developers must never manually bypass tenant filtering.

Repository layer enforces isolation.

---

# Row-Level Security

Recommended future implementation:

PostgreSQL Row-Level Security (RLS)

Benefits

- Database enforcement
- Defense in depth
- Reduced developer error
- Strong isolation

---

# Shared Resources

Platform-wide shared resources

- Identity
- AI Models
- Logging
- Monitoring
- Notification Engine
- Feature Flags

Business data remains tenant-specific.

---

# Tenant Configuration

Every tenant owns configuration.

Examples

- Branding
- Logo
- Theme
- Timezone
- Currency
- Language
- Academic Year
- Fiscal Year
- Business Rules
- Integrations

Configurations are stored separately from business data.

---

# Custom Domains

Supported

```
school.example.com

hospital.example.com

erp.company.com
```

Custom domains map to tenant identities.

---

# Branding

Tenant branding includes

- Logo
- Colors
- Fonts
- Email Templates
- Login Screen
- Reports
- PDFs
- Notifications

Branding should not affect application logic.

---

# Feature Management

Every feature is tenant-aware.

Example

```text
Tenant A

↓

AI Enabled

Tenant B

↓

AI Disabled
```

Feature flags determine platform capabilities.

---

# Subscription Model

Supported plans

```
Free

Starter

Professional

Enterprise

Custom
```

Plans determine:

- Features
- Limits
- Storage
- AI Credits
- API Limits
- Support

---

# Resource Limits

Examples

Users

Projects

Storage

API Requests

AI Tokens

Uploads

Reports

Limits are configurable per subscription.

---

# Tenant Lifecycle

```text
Create

↓

Provision

↓

Activate

↓

Operate

↓

Upgrade

↓

Suspend

↓

Archive

↓

Delete
```

Deletion follows data retention policies.

---

# Tenant Provisioning

Provisioning creates

- Organization
- Admin User
- Default Roles
- Permissions
- Configuration
- Storage
- Feature Flags
- Billing Profile

Provisioning should be automated.

---

# Tenant Migration

Support migration between

- Plans
- Regions
- Databases
- Clusters

Migration should require minimal downtime.

---

# Tenant Backup

Backups support

- Platform Backup
- Tenant Backup
- Point-in-Time Recovery
- Selective Restore

Enterprise customers may request tenant-specific restores.

---

# Multi-Tenant Security

Every request validates

- Identity
- Tenant
- Permissions
- Subscription
- Session

Cross-tenant access is prohibited.

---

# API Design

Every request carries tenant context.

Example

```
Authorization: Bearer ...

↓

Tenant Extracted

↓

Business Execution
```

Client applications should never send arbitrary tenant IDs.

---

# Search

Search indexes remain tenant-isolated.

Search queries automatically filter by tenant.

---

# AI Isolation

AI services receive

- Tenant ID
- Organization Context
- Feature Flags

Tenant prompts and embeddings remain isolated.

No customer data is shared across tenants.

---

# Caching

Cache keys include tenant.

Example

```
tenant:student:123

tenant:dashboard

tenant:config
```

Never share cached business data across tenants.

---

# Event Architecture

Every event contains

```
Tenant ID

Correlation ID

Trace ID
```

Events remain tenant-aware throughout the platform.

---

# Observability

Track

- Tenant Activity
- Active Users
- API Usage
- Storage
- AI Consumption
- Errors
- Performance

Per tenant.

---

# Folder Structure

```text
platform/

└── tenancy/

    ├── api/

    ├── application/

    ├── domain/

    ├── infrastructure/

    ├── middleware/

    ├── provisioning/

    ├── feature_flags/

    ├── billing/

    ├── events/

    └── tests/
```

---

# Anti-Patterns

Avoid

❌ Missing tenant_id

❌ Cross-Tenant Queries

❌ Shared Business Cache

❌ Shared Upload Storage

❌ Shared Search Index

❌ Hardcoded Tenant Logic

❌ Manual Tenant Filtering

❌ Super Admin Database Access

❌ Business Logic Based on Domain Name

❌ Tenant Switching During Request

---

# Production Checklist

Before production

- [ ] Tenant Context implemented
- [ ] Automatic tenant filtering enabled
- [ ] Cross-tenant tests passing
- [ ] Feature flags configured
- [ ] Subscription limits implemented
- [ ] Branding support added
- [ ] Backup strategy verified
- [ ] Tenant-aware caching enabled
- [ ] AI isolation verified
- [ ] Security review completed

---

# Success Criteria

Multi-tenancy is successful when:

- Tenants cannot access each other's data.
- Infrastructure remains efficiently shared.
- New tenants provision automatically.
- Scaling remains linear.
- Tenant customization does not increase code complexity.
- AI features remain tenant-aware.
- Billing and subscriptions operate independently.
- Platform operations remain simple despite large tenant counts.

---

# Future Evolution

Version 2.0 will include:

- Complete Multi-Tenant Database Schema
- PostgreSQL Row-Level Security (RLS) Implementation
- Multi-Tenant FastAPI Middleware
- Tenant Context Propagation
- Multi-Region Tenant Placement
- Enterprise Tenant Provisioning Service
- Organization Hierarchy Model
- White-Label Platform Architecture
- SaaS Subscription Engine
- Tenant Analytics Dashboard
- Tenant Backup & Disaster Recovery Strategy
- C4 Multi-Tenant Architecture
- UML Tenant Lifecycle Diagrams
- AI Multi-Tenant Isolation Architecture
- Production Reference Implementation

---

# Multi-Tenancy Checklist

- [x] Multi-Tenant Architecture Defined
- [x] Tenant Isolation Model Established
- [x] Tenant Context Defined
- [x] Data Isolation Rules Added
- [x] Configuration & Branding Standards Defined
- [x] Subscription & Feature Model Added
- [x] Tenant Lifecycle Defined
- [x] Backup & Migration Strategy Included
- [x] AI Isolation Defined
- [x] Security Requirements Added
- [x] Observability Standards Included
- [x] Production Checklist Added
- [x] Success Criteria Defined

---

# Document Status

**Document:** NES-205 — Multi-Tenancy Architecture

**Version:** 1.0.0

**Status:** Ready for Architecture Review

**Next Document:** **NES-206 — Data Architecture**

---

# Revision Queue for Version 2.0 (Enterprise Edition)

Future enhancements will include:

- SaaS Reference Architecture
- Tenant Resolution Middleware
- PostgreSQL RLS Policies
- Database-per-Tenant Migration Strategy
- Multi-Tenant Redis Strategy
- Multi-Tenant Elasticsearch/OpenSearch Design
- AI Knowledge Isolation Framework
- Multi-Tenant Observability Dashboards
- FinOps & Tenant Cost Allocation
- Kubernetes Namespace Strategy
- Global Multi-Region Tenant Routing
- Enterprise White-Label Platform Blueprint
- Architecture Fitness Rules for Tenant Isolation
- Complete FastAPI Multi-Tenant Reference Project

These enhancements will establish the definitive multi-tenancy standard for all NeelStack products, ensuring secure, scalable, enterprise-grade SaaS architecture capable of serving organizations from small businesses to global enterprises.