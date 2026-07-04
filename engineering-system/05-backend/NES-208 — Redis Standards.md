---
document_id: NES-208
title: Redis Standards
subtitle: Enterprise Redis Architecture & Caching Standard for the NeelStack Platform
version: 1.0.0
status: Draft
classification: Internal
owner: Chief Solution Architect
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-207 PostgreSQL Standards
next_document: NES-209 Object Storage Standards
---

# NES-208 — Redis Standards

> **"Redis is a performance optimization layer—not a source of truth."**

---

# Executive Summary

Redis is the official **in-memory data platform** for the NeelStack ecosystem.

Redis is used to improve:

- Performance
- Scalability
- Availability
- User Experience
- API Response Time

Redis must **never become the primary data store**.

The authoritative source of business data remains PostgreSQL.

Redis is used only for:

- Caching
- Session Storage
- Distributed Locking
- Rate Limiting
- Job Queues
- Temporary State
- Pub/Sub
- Real-Time Features

---

# Purpose

This standard defines:

- Redis Architecture
- Cache Strategy
- Key Naming
- TTL Standards
- Session Management
- Distributed Locking
- Pub/Sub
- Rate Limiting
- Security
- Monitoring
- Operations

---

# Redis Philosophy

```
Client

↓

FastAPI

↓

Redis

↓

Cache Hit

↓

Return

OR

↓

PostgreSQL

↓

Update Redis

↓

Return
```

Redis accelerates applications.

It never replaces PostgreSQL.

---

# Guiding Principles

Redis must always be:

✓ Fast

✓ Disposable

✓ Observable

✓ Secure

✓ Consistent

✓ Multi-Tenant

✓ Highly Available

✓ Predictable

---

# Redis Responsibilities

Redis is approved for:

✓ API Cache

✓ Session Store

✓ Feature Flags

✓ Distributed Locks

✓ Background Queues

✓ OTP Storage

✓ Rate Limiting

✓ AI Response Cache

✓ Dashboard Cache

✓ Temporary Tokens

---

# Redis Must NOT Store

✗ Permanent Business Data

✗ Financial Records

✗ Audit Logs

✗ Legal Documents

✗ Primary User Profiles

✗ Source of Truth

---

# Architecture

```text
                Client

                  │

              FastAPI

                  │

      ┌───────────┴───────────┐

      │                       │

 PostgreSQL             Redis Cache

      │                       │

 Durable Data        Temporary Data
```

---

# Deployment Architecture

```text
Application

↓

Redis Client

↓

Redis Sentinel / Cluster

↓

Primary

↓

Replica

↓

Persistence
```

Enterprise deployments require High Availability.

---

# Redis Data Types

Approved

| Type | Usage |
|------|-------|
| String | Cache |
| Hash | User Sessions |
| Set | Permissions |
| Sorted Set | Leaderboards |
| List | Queues |
| Stream | Event Streams |
| Bitmap | Analytics |
| HyperLogLog | Approximate Counting |

Choose the smallest appropriate structure.

---

# Cache Strategy

Cache follows

```
Cache Aside Pattern
```

Flow

```
Read

↓

Redis

↓

Hit?

↓

Yes

↓

Return

↓

No

↓

PostgreSQL

↓

Store Redis

↓

Return
```

---

# Write Strategy

```
Write

↓

PostgreSQL

↓

Commit

↓

Invalidate Cache
```

Never write Redis first.

---

# Cache Invalidation

Priority

```
Update

↓

Delete Cache

↓

Next Read

↓

Rebuild Cache
```

Cache invalidation is automatic.

---

# Cache Keys

Standard

```
tenant:{tenant_id}:student:{id}

tenant:{tenant_id}:course:{id}

tenant:{tenant_id}:dashboard

tenant:{tenant_id}:config
```

Keys must always include tenant context.

---

# Key Naming Convention

```
namespace:entity:id

Examples

tenant:school1:user:123

tenant:school1:course:45

platform:feature_flags

session:user:456
```

Use lowercase only.

---

# Time-To-Live (TTL)

Recommended defaults

| Data | TTL |
|------|------|
| Dashboard | 5 Minutes |
| Student Details | 10 Minutes |
| Feature Flags | 1 Hour |
| Sessions | 30 Minutes (Idle) |
| OTP | 5 Minutes |
| Rate Limits | 1 Minute |
| AI Responses | 15 Minutes |
| Configuration | 24 Hours |

Every cache entry must have a TTL unless explicitly justified.

---

# Session Management

Redis stores

```
Session ID

↓

User

↓

Device

↓

Expiration
```

Sessions expire automatically.

---

# Distributed Locking

Use Redis locks for

- Scheduled Jobs
- Background Workers
- Inventory
- Workflow Coordination

Example

```
Acquire Lock

↓

Execute

↓

Release
```

Always define lock timeout.

---

# Rate Limiting

Implementation

```
Client

↓

Redis Counter

↓

Limit?

↓

Allow / Reject
```

Algorithms

- Token Bucket
- Sliding Window
- Fixed Window

Default

Sliding Window.

---

# Feature Flags

Feature flags stored in Redis.

Benefits

- Fast lookup
- Runtime updates
- Low latency

Feature changes propagate without restart.

---

# Pub/Sub

Use for

- Notifications
- Cache Invalidation
- Internal Signaling

Not for durable messaging.

Kafka remains the event platform.

---

# Streams

Redis Streams are allowed for

- Lightweight Work Queues
- Internal Event Processing

Do not replace Kafka for enterprise event streaming.

---

# AI Caching

Cache

- Embeddings
- Prompt Templates
- LLM Responses
- Token Counts

Never cache confidential prompts without encryption.

---

# Multi-Tenancy

Every key contains

```
tenant_id
```

Cross-tenant cache sharing is prohibited.

---

# Serialization

Preferred

```
msgpack

↓

JSON

↓

pickle (Never)
```

Do not use Python pickle.

---

# Compression

Compress values larger than

```
10 KB
```

Recommended

Zstandard (Zstd)

---

# Persistence

Enable

- AOF
- RDB Snapshots

Configuration depends on workload.

Redis persistence supplements—not replaces—database backups.

---

# Eviction Policy

Preferred

```
allkeys-lru
```

Alternative

```
volatile-lru
```

Never allow uncontrolled memory exhaustion.

---

# Memory Management

Monitor

- Memory Usage
- Fragmentation
- Evictions
- Hit Ratio

Memory alerts are mandatory.

---

# High Availability

Production requires

```
Redis Sentinel

OR

Redis Cluster
```

Single-node Redis is for development only.

---

# Security

Mandatory

TLS

Authentication

ACL

Private Network

Secret Rotation

No Public Internet Exposure

Disable Dangerous Commands

---

# Monitoring

Track

- Cache Hit Ratio
- Cache Miss Ratio
- Memory Usage
- Evictions
- Latency
- Connected Clients
- Expired Keys
- Slow Commands

---

# Performance Targets

Cache Lookup

```
<1ms
```

Hit Ratio

```
>90%
```

Memory Fragmentation

```
<1.5
```

---

# Backup

Persist

- AOF
- Daily Snapshots

Backups stored in Object Storage.

---

# Observability

Expose

- Prometheus Metrics
- OpenTelemetry Traces
- Structured Logs

Every Redis operation should be measurable.

---

# Folder Structure

```text
cache/

├── adapters/

├── keys/

├── serializers/

├── locks/

├── sessions/

├── feature_flags/

├── rate_limit/

├── monitoring/

└── tests/
```

---

# Anti-Patterns

Avoid

❌ Business Data in Redis

❌ Infinite TTL

❌ Missing Tenant Prefix

❌ Large Objects (>1MB)

❌ Cache Without Expiration

❌ Manual Cache Clearing

❌ Public Redis

❌ Pickle Serialization

❌ Cache as Database

❌ Cross-Tenant Keys

❌ Long-Lived Distributed Locks

---

# Production Checklist

Before production

- [ ] Redis Cluster configured
- [ ] TLS enabled
- [ ] ACL configured
- [ ] Key naming validated
- [ ] TTL policies implemented
- [ ] Cache invalidation tested
- [ ] Distributed locks reviewed
- [ ] Monitoring configured
- [ ] Backup strategy verified
- [ ] Security review completed

---

# Success Criteria

Redis implementation is successful when:

- Cache hit ratio consistently exceeds 90%.
- PostgreSQL load decreases significantly.
- Sessions remain fast and reliable.
- Cache invalidation is automatic.
- Distributed locks prevent race conditions.
- Multi-tenant isolation is enforced.
- AI response latency improves through caching.
- Redis failures do not cause data loss.

---

# Future Evolution

Version 2.0 will include:

- Redis Cluster Deployment Blueprint
- Redis Sentinel High Availability Guide
- Redis Enterprise Evaluation
- Lua Scripting Standards
- Redis Streams Architecture
- Distributed Locking Patterns
- Cache Warming Strategy
- Cache Consistency Models
- Redis + FastAPI Reference Implementation
- Prometheus & Grafana Dashboards
- Redis Security Hardening Guide
- Multi-Region Redis Strategy
- AI Semantic Cache Architecture
- Architecture Fitness Rules for Cache Usage
- Production Redis Starter Repository

---

# Redis Standards Checklist

- [x] Redis Architecture Defined
- [x] Cache Strategy Established
- [x] Key Naming Standardized
- [x] TTL Policies Defined
- [x] Session Management Included
- [x] Distributed Locking Defined
- [x] Rate Limiting Added
- [x] Feature Flag Strategy Included
- [x] Security Standards Defined
- [x] Monitoring & Observability Added
- [x] Performance Targets Defined
- [x] Production Checklist Added
- [x] Success Criteria Defined

---

# Document Status

**Document:** NES-208 — Redis Standards

**Version:** 1.0.0

**Status:** Ready for Architecture Review

**Next Document:** **NES-209 — Object Storage Standards**

---

# Revision Queue for Version 2.0 (Enterprise Edition)

Future enhancements will include:

- Enterprise Redis Cluster Reference Architecture
- Redis Sentinel & Failover Configuration
- C4 Cache Architecture Diagrams
- Cache-Aside, Write-Through & Write-Behind Pattern Comparison
- Redis Streams vs Kafka Decision Matrix
- Distributed Locking Reference Implementation
- Redis Security & ACL Playbook
- Multi-Tenant Cache Isolation Framework
- AI Semantic Cache Design
- Cache Performance Benchmark Suite
- OpenTelemetry Instrumentation Guide
- Kubernetes Redis Deployment Standards
- Disaster Recovery & Failover Runbooks
- Architecture Fitness Tests for Cache Compliance
- Production FastAPI + Redis Reference Project

These enhancements will establish the definitive Redis engineering standard for the NeelStack platform, ensuring high-performance, secure, observable, and resilient caching infrastructure across all applications, AI services, and platform components.