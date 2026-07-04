---
document_id: NES-307
title: Data Fetching Standards
subtitle: Enterprise Data Fetching, API Consumption, Caching & Synchronization Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Frontend Architecture Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-306 State Management Standards
next_document: NES-308 Forms & Validation Standards
---

# NES-307 — Data Fetching Standards

> **"Data fetching is not about making HTTP requests. It is about delivering reliable, performant, synchronized, and observable data experiences."**

---

# Executive Summary

This document defines the official data fetching standards for every NeelStack frontend application.

It standardizes

- API Communication
- Server State
- Fetching Strategies
- Caching
- Synchronization
- Error Handling
- Retry Logic
- Streaming
- Pagination
- Real-Time Updates
- Performance

Server data is never treated as application state.

It is synchronized using enterprise data-fetching architecture.

---

# Purpose

This document defines

- Data Fetching Architecture
- API Communication
- TanStack Query Standards
- Server Components
- Server Actions
- Caching
- Pagination
- Infinite Scroll
- Streaming
- Real-Time Updates
- Error Handling

---

# Vision

Build frontend applications where

- Server data remains synchronized.
- Applications minimize unnecessary requests.
- APIs remain abstracted.
- Caching improves performance.
- Offline experiences remain reliable.
- AI streaming feels real-time.

---

# Data Fetching Philosophy

```text
Backend

↓

API Gateway

↓

API Client

↓

Service Layer

↓

TanStack Query

↓

Hooks

↓

Components
```

Components never communicate directly with HTTP clients.

---

# Core Principles

Every application must be

✓ Server First

✓ Cache Aware

✓ Observable

✓ Predictable

✓ Typed

✓ Retry Safe

✓ Offline Friendly

✓ Performant

✓ AI Ready

---

# Enterprise Architecture

```text
UI

↓

Feature Hook

↓

TanStack Query

↓

Service

↓

API Client

↓

Gateway

↓

Backend
```

---

# Official Technologies

Server State

```
TanStack Query
```

HTTP Client

```
Axios
```

Streaming

```
Fetch API

ReadableStream

SSE
```

Realtime

```
WebSocket

Server-Sent Events
```

Validation

```
Zod
```

---

# Fetching Hierarchy

Preferred order

Server Components

↓

Server Actions

↓

TanStack Query

↓

Streaming

↓

Realtime

↓

Manual Fetching

---

# API Layer

Every API follows

```text
Component

↓

Hook

↓

Query

↓

Service

↓

API Client

↓

Gateway
```

---

# HTTP Client

Applications use one centralized client.

Responsibilities

Authentication

Retry

Logging

Tracing

Headers

Token Refresh

Error Mapping

---

# API Structure

```text
services/

├── auth.service.ts

├── users.service.ts

├── ai.service.ts

├── projects.service.ts

├── seo.service.ts

└── reports.service.ts
```

---

# Query Hooks

Example

```tsx
const { data } = useProjects()
```

Never expose raw API calls inside components.

---

# Query Keys

Structure

```text
["users"]

["users", id]

["projects"]

["projects", filters]

["seo", domain]

["ai", conversationId]
```

Keys must remain deterministic.

---

# Query Standards

Every query defines

Query Key

Query Function

Stale Time

Retry Policy

Error Handler

Select Function (optional)

---

# Cache Strategy

Support

Fresh

↓

Stale

↓

Background Refresh

↓

Garbage Collection

Cache intentionally.

---

# Cache Policies

Short-lived

Search

Notifications

AI Responses

Medium

Projects

Tasks

Reports

Long-lived

Settings

Permissions

Reference Data

---

# Invalidation

Support

Manual

↓

Tag Based

↓

Query Key

↓

Mutation Success

↓

Realtime Events

Never invalidate everything.

---

# Mutations

Workflow

```text
User Action

↓

Mutation

↓

Optimistic Update

↓

API

↓

Success

↓

Invalidate Queries
```

Rollback on failure.

---

# Optimistic Updates

Use for

CRUD

Likes

Bookmarks

Status Changes

Assignments

Avoid optimistic updates for destructive operations unless recoverable.

---

# Error Handling

Handle

400

401

403

404

409

422

429

500

503

Errors are mapped into domain-friendly messages.

---

# Retry Policy

Automatically retry

Network Errors

Timeouts

503

Rate Limits

Do not retry

400

401

403

404

Validation Errors

---

# Loading States

Support

Skeleton

Spinner

Placeholder

Streaming

Progressive Rendering

Avoid blank screens.

---

# Empty States

Support

No Results

No Data

No Access

Offline

Error

First-Time Experience

---

# Pagination

Support

Offset

Cursor

Infinite Scroll

Load More

Large datasets never load completely.

---

# Infinite Scroll

Requirements

Virtualization

Intersection Observer

Prefetch Next Page

Loading Indicators

End of List Indicator

---

# Filtering

Filters belong in

URL

↓

Query Key

↓

Backend

↓

Results

Never filter large datasets entirely in the browser.

---

# Sorting

Server-side sorting preferred.

Client sorting allowed only for small datasets.

---

# Search

Support

Debounce

Cancellation

Pagination

Highlighting

Caching

Search results remain cacheable.

---

# Request Cancellation

Cancel

Search

Navigation

Component Unmount

Duplicate Requests

Use AbortController where supported.

---

# Request Deduplication

TanStack Query automatically deduplicates identical requests.

Avoid manual duplicate fetching.

---

# Streaming

Support

AI Chat

Logs

Notifications

Large Reports

Long Running Tasks

Streaming improves perceived performance.

---

# AI Streaming

Support

Token Streaming

Tool Status

Thinking Indicator

Citation Streaming

Partial Responses

Following NES-218 through NES-230.

---

# Real-Time Updates

Support

WebSocket

SSE

Polling (fallback)

Realtime updates remain event driven.

---

# Offline Support

Support

Cached Queries

Queued Mutations

Retry

Conflict Resolution

Offline Indicators

---

# Background Synchronization

Support

Window Focus

Reconnect

Scheduled Refresh

Mutation Success

Realtime Events

---

# Authentication

Automatically attach

JWT

Tenant Context

Trace ID

Correlation ID

Locale

Headers remain centralized.

---

# Security

Validate

Authorization

CSRF

XSS

Input

Output

Rate Limits

Never expose internal APIs directly.

---

# Observability

Track

Latency

Retries

Cache Hits

Cache Misses

Failures

Streaming Duration

Realtime Events

Every request includes tracing metadata.

---

# Performance

Optimize

Prefetching

Deduplication

Caching

Streaming

Pagination

Compression

Minimal Payloads

---

# Folder Structure

```text
services/

├── api/

├── client/

├── interceptors/

├── queries/

├── mutations/

├── realtime/

├── streaming/

├── types/

├── schemas/

└── utils/
```

---

# Query Folder Structure

```text
queries/

├── users/

├── projects/

├── reports/

├── ai/

├── seo/

└── shared/
```

---

# Enterprise Data Flow

```text
Backend

↓

Gateway

↓

Axios Client

↓

Service

↓

TanStack Query

↓

Feature Hook

↓

React Component

↓

UI
```

---

# KPIs

Cache Hit Rate

```
>90%
```

Average API Latency

```
<300ms
```

Duplicate Requests

```
0
```

Retry Success

```
>95%
```

Streaming Start

```
<500ms
```

---

# Anti-Patterns

Avoid

❌ Fetch Inside useEffect Everywhere

❌ Direct Axios Calls in Components

❌ Server Data in Redux

❌ Duplicate Requests

❌ No Cache Strategy

❌ Fetching Entire Datasets

❌ Missing Loading States

❌ Ignoring Retries

❌ Manual Polling Everywhere

❌ Business Logic Inside Query Functions

---

# Production Checklist

Before production

- [ ] API client centralized
- [ ] Query keys standardized
- [ ] Cache strategy documented
- [ ] Retry policy configured
- [ ] Pagination validated
- [ ] Streaming tested
- [ ] Offline behavior verified
- [ ] Observability enabled
- [ ] Performance benchmarks achieved
- [ ] Architecture review approved

---

# Success Criteria

Data Fetching is successful when

- Components never perform direct HTTP requests.
- Server state remains synchronized automatically.
- API traffic is minimized through intelligent caching.
- Streaming experiences feel instantaneous.
- Retry logic improves reliability without duplication.
- Offline behavior is graceful.
- Real-time updates remain event driven.
- Developers work with predictable, reusable data-fetching patterns.

---

# Future Evolution

Version 2.0 will include

- GraphQL Integration Standards
- gRPC-Web Support
- React Server Components Data Layer
- AI Streaming SDK
- Enterprise API SDK Generator
- Request Coalescing Framework
- Intelligent Cache Analytics
- Offline Synchronization Engine
- Event-Driven Data Synchronization
- Enterprise Data Observability Dashboard
- C4 Data Fetching Architecture
- Architecture Fitness Rules for API Consumption
- Production Data Layer Starter Repository

---

# Data Fetching Standards Checklist

- [x] Data Fetching Architecture Defined
- [x] API Layer Standardized
- [x] TanStack Query Standards Included
- [x] Cache Strategy Defined
- [x] Mutation Strategy Established
- [x] Streaming & Realtime Included
- [x] Security Standards Added
- [x] Performance Standards Defined
- [x] Production Checklist Added
- [x] Success Criteria Defined

---

# Document Status

**Document:** NES-307 — Data Fetching Standards

**Version:** 1.0.0

**Status:** Ready for Architecture Review

**Next Document:** **NES-308 — Forms & Validation Standards**

---

# Revision Queue for Version 2.0 (Enterprise Edition)

Future enhancements will include

- Enterprise Data Layer Reference Architecture
- React Server Components Data Patterns
- GraphQL Federation Standards
- gRPC-Web Architecture Guide
- AI Streaming SDK & Reference Implementation
- Offline-First Synchronization Framework
- Intelligent Cache Optimization Engine
- Enterprise API Client Generator
- Data Fetching Performance Dashboard
- Event-Driven Client Synchronization
- C4 Context, Container & Data Flow Diagrams
- Architecture Fitness Tests for Data Fetching
- Production Enterprise Data Layer Starter Repository

These enhancements will establish the definitive Data Fetching Standard for the NeelStack ecosystem, ensuring every frontend application delivers secure, observable, resilient, high-performance, and scalable data synchronization while maintaining clear architectural boundaries between UI, server state, and backend services.