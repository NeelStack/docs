---
document_id: NES-207
title: PostgreSQL Standards
subtitle: Enterprise PostgreSQL Engineering Standard for the NeelStack Platform
version: 1.0.0
status: Draft
classification: Internal
owner: Chief Solution Architect
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-206 Data Architecture
next_document: NES-208 Redis Standards
---

# NES-207 — PostgreSQL Standards

> **"A database is not just storage—it is the foundation of business integrity."**

---

# Executive Summary

PostgreSQL is the **official transactional database** for all NeelStack products.

It serves as the system of record for:

- Business Data
- Identity
- Multi-Tenant SaaS
- Financial Data
- Audit Logs
- Platform Metadata
- AI Metadata
- Configuration
- Workflow State

PostgreSQL is selected because it provides:

- ACID Compliance
- Excellent Performance
- Enterprise Reliability
- Rich SQL Features
- JSONB Support
- Full Text Search
- Extensions
- Strong Community
- Cloud Portability

Every production database must comply with this standard.

---

# Purpose

This document defines:

- PostgreSQL Architecture
- Database Design Standards
- Schema Standards
- Naming Conventions
- Data Types
- Indexing
- Constraints
- Transactions
- Migrations
- Performance
- Security
- Backups
- Operations

---

# PostgreSQL Philosophy

```
Business Rule

↓

Domain Model

↓

Repository

↓

PostgreSQL

↓

Persistent Truth
```

The database is the **source of truth**.

Never the cache.

Never the search index.

Never the event stream.

---

# Architecture Role

PostgreSQL stores:

✓ Transactional Data

✓ Business Records

✓ Identity

✓ Billing

✓ Audit

✓ Workflow

✓ Metadata

Not intended for:

✗ Cache

✗ Search

✗ Analytics

✗ Blob Storage

---

# Supported Version

Production Standard

```
PostgreSQL 17+
```

Minimum

```
PostgreSQL 16
```

Older versions require architecture approval.

---

# Database Architecture

```text
                 FastAPI

                    │

             Repository Layer

                    │

              SQLAlchemy 2.0

                    │

             PostgreSQL Cluster

                    │

          Primary + Read Replicas

                    │

             Continuous Backup
```

---

# Schema Strategy

NeelStack adopts:

```
Single Database

↓

Shared Schema

↓

Tenant Isolation

↓

Row-Level Security (Future)
```

Business domains remain logically separated.

---

# Database Organization

```
postgres/

├── migrations/

├── seeds/

├── schema/

├── functions/

├── views/

├── triggers/

├── indexes/

├── policies/

├── scripts/

└── tests/
```

---

# Naming Standards

## Tables

Plural

```sql
students

teachers

courses

invoices
```

---

## Columns

snake_case

```sql
first_name

created_at

tenant_id
```

---

## Primary Keys

```
id UUID
```

---

## Foreign Keys

```
student_id

course_id

tenant_id
```

---

## Indexes

```
idx_students_email

idx_courses_status

idx_payments_created_at
```

---

## Constraints

```
pk_students

fk_students_courses

uq_users_email

chk_price_positive
```

---

# Primary Keys

Standard

```
UUIDv7
```

Benefits

- Ordered
- Distributed
- Globally Unique
- Better Index Locality

Sequential IDs are prohibited for public identifiers.

---

# Required Columns

Every business table contains:

```sql
id

tenant_id

created_at

updated_at

created_by

updated_by

version
```

Optional

```sql
deleted_at

deleted_by
```

Consistency simplifies tooling.

---

# Data Types

Preferred

| Data | Type |
|------|------|
| ID | UUID |
| Name | TEXT |
| Email | TEXT |
| Money | NUMERIC(18,2) |
| Boolean | BOOLEAN |
| Date | DATE |
| Timestamp | TIMESTAMPTZ |
| JSON | JSONB |
| Enum | PostgreSQL ENUM (carefully) |

Avoid VARCHAR without justification.

Prefer TEXT.

---

# Timestamp Standards

Use

```
TIMESTAMPTZ
```

Store

UTC only.

Timezone conversion occurs in the application layer.

---

# JSONB Usage

Use JSONB only for:

- Dynamic Metadata
- AI Responses
- Third-Party Payloads
- Configurations

Do NOT store relational data inside JSONB.

---

# Normalization

Default

Third Normal Form (3NF)

Denormalize only when:

- Performance measurements justify it
- Architecture review approves it

---

# Constraints

Mandatory

Primary Key

Foreign Key

Unique

Check Constraint

NOT NULL

Database constraints protect data integrity.

---

# Foreign Keys

Always enforce

```
Enrollment

↓

Student

↓

Course
```

Never disable foreign keys in production.

---

# Indexing Standards

Index

- Foreign Keys
- Frequently Queried Columns
- Tenant ID
- created_at
- Unique Columns

Review indexes quarterly.

---

# Composite Indexes

Example

```sql
(tenant_id, status)

(tenant_id, created_at)

(tenant_id, email)
```

Tenant-first indexing is preferred.

---

# Full-Text Search

Use PostgreSQL FTS for:

- Small datasets
- Internal search

Use OpenSearch for enterprise-scale search.

---

# Transactions

Transactions must be

Short

Atomic

Explicit

Avoid long-running transactions.

---

# Isolation Level

Default

```
READ COMMITTED
```

Higher isolation only when justified.

---

# Optimistic Locking

Use

```
version
```

column for concurrent updates.

Avoid pessimistic locking unless required.

---

# Soft Deletes

Standard

```sql
deleted_at

deleted_by
```

Never permanently delete business-critical data without approval.

---

# Views

Use for:

- Reporting
- Read Models
- Simplified Queries

Never hide business logic inside views.

---

# Functions

Allowed

- Utility Functions
- Calculations
- Reporting

Avoid embedding complex business rules.

Business logic belongs in the Domain Layer.

---

# Triggers

Allowed

- Audit
- Timestamp Updates
- Event Outbox

Avoid business workflow triggers.

---

# Outbox Pattern

Every domain event is stored in

```
outbox_events
```

before publishing.

Benefits

- Reliable Event Delivery
- No Lost Events
- Transactional Consistency

---

# Migrations

Tool

```
Alembic
```

Every schema change requires

- Migration
- Review
- Rollback Plan

Never modify production schema manually.

---

# Seeding

Seed only

- Default Roles
- Permissions
- Countries
- Configuration

Never seed customer business data.

---

# Performance Targets

CRUD Query

```
<50ms
```

Complex Query

```
<200ms
```

Connection Acquisition

```
<5ms
```

---

# Query Standards

Always

- Use indexes
- Limit results
- Select required columns
- Avoid SELECT *

Use EXPLAIN ANALYZE for optimization.

---

# Connection Pooling

Use

PgBouncer

↓

SQLAlchemy Pool

↓

PostgreSQL

Connection pooling is mandatory.

---

# Read Replicas

Support

```
Primary

↓

Read Replica

↓

Analytics

↓

Reporting
```

Writes always go to the primary.

---

# Backup Strategy

Support

- Daily Full Backup
- WAL Archiving
- Point-in-Time Recovery
- Cross-Region Backup

Backups tested regularly.

---

# Disaster Recovery

Target

RPO

```
≤15 Minutes
```

RTO

```
≤1 Hour
```

---

# Security

Mandatory

TLS

Encryption at Rest

Least Privilege

Secrets Manager

Parameterized Queries

SQL Injection Protection

Audit Logging

---

# Multi-Tenancy

Every query automatically filters

```
tenant_id
```

Future

PostgreSQL Row-Level Security.

---

# Monitoring

Monitor

- Slow Queries
- Deadlocks
- Lock Waits
- Replication Lag
- Connections
- Cache Hit Ratio
- WAL Growth
- Index Usage
- Disk Growth

---

# Observability

Every query should be traceable.

Capture

- Query Duration
- Trace ID
- Request ID
- Tenant ID

Integrate with OpenTelemetry.

---

# AI Integration

PostgreSQL stores

- AI Metadata
- Prompt History
- Model Configurations
- Vector References

Embeddings stored using

```
pgvector
```

or a dedicated vector database.

---

# Folder Structure

```text
database/

├── migrations/

├── models/

├── repositories/

├── indexes/

├── policies/

├── outbox/

├── backups/

├── monitoring/

├── seeds/

└── tests/
```

---

# Anti-Patterns

Avoid

❌ SELECT *

❌ Missing Indexes

❌ Long Transactions

❌ Business Logic in SQL

❌ Dynamic SQL

❌ Missing Foreign Keys

❌ Manual Schema Changes

❌ Storing Files in PostgreSQL

❌ JSONB for Relational Data

❌ Cross-Tenant Queries

❌ Unbounded Queries

---

# Production Checklist

Before production

- [ ] Schema reviewed
- [ ] Alembic migration created
- [ ] Rollback tested
- [ ] Foreign keys validated
- [ ] Indexes optimized
- [ ] Query performance benchmarked
- [ ] Backup configured
- [ ] Replication verified
- [ ] Monitoring enabled
- [ ] Security review completed

---

# Success Criteria

PostgreSQL implementation is successful when:

- Data integrity is enforced by the database.
- Business queries remain performant.
- Schema evolution is predictable.
- Tenant isolation is automatic.
- Event publishing is reliable through the Outbox pattern.
- Disaster recovery objectives are met.
- AI metadata integrates seamlessly.
- Operational metrics provide complete visibility.

---

# Future Evolution

Version 2.0 will include:

- Enterprise PostgreSQL Reference Schema
- C4 Database Architecture
- Complete ER Diagrams
- SQLAlchemy 2.0 Mapping Standards
- Alembic Migration Playbook
- PostgreSQL Row-Level Security (RLS) Implementation
- Partitioning & Sharding Strategy
- PgBouncer Production Configuration
- High Availability Architecture (Patroni)
- Backup & Restore Runbooks
- Query Optimization Guide
- pgvector Reference Implementation
- Database Performance Benchmark Suite
- Architecture Fitness Rules for Database Design
- Production PostgreSQL Starter Repository

---

# PostgreSQL Standards Checklist

- [x] Database Architecture Defined
- [x] Schema Standards Established
- [x] Naming Conventions Defined
- [x] Data Types Standardized
- [x] Indexing Strategy Added
- [x] Constraint Standards Defined
- [x] Transaction Rules Established
- [x] Migration Process Defined
- [x] Performance Standards Added
- [x] Security Requirements Included
- [x] Backup & Recovery Strategy Defined
- [x] AI Integration Included
- [x] Production Checklist Added
- [x] Success Criteria Defined

---

# Document Status

**Document:** NES-207 — PostgreSQL Standards

**Version:** 1.0.0

**Status:** Ready for Architecture Review

**Next Document:** **NES-208 — Redis Standards**

---

# Revision Queue for Version 2.0 (Enterprise Edition)

Future enhancements will include:

- Enterprise PostgreSQL Reference Database
- Complete ERD Library
- SQL Style Guide
- Row-Level Security Policy Templates
- Partitioning & Archival Strategy
- Logical Replication & CDC Architecture
- Patroni High Availability Deployment
- PgBouncer Configuration Standards
- Query Performance Review Checklist
- pgvector + AI Knowledge Base Integration
- Database Observability Dashboards
- Automated Schema Governance
- Database Security Hardening Guide
- Architecture Fitness Tests for SQL
- Production PostgreSQL Reference Implementation

These enhancements will establish the definitive PostgreSQL engineering standard for every NeelStack backend service, ensuring secure, scalable, high-performance, multi-tenant, and enterprise-grade data management across the entire platform.