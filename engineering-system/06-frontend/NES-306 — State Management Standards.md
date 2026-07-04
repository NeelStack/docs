---
document_id: NES-306
title: State Management Standards
subtitle: Enterprise State Management, Data Flow & Client State Architecture Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Frontend Architecture Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-305 Tailwind CSS Standards
next_document: NES-307 Data Fetching Standards
---

# NES-306 — State Management Standards

> **"State is one of the hardest problems in frontend engineering. Keep it minimal, predictable, observable, and close to where it belongs."**

---

# Executive Summary

This document defines the official state management architecture used across every NeelStack frontend application.

The objective is to establish a consistent strategy for managing

- Local State
- Server State
- Global State
- URL State
- Form State
- UI State
- AI State
- Session State
- Offline State

This standard eliminates inconsistent state management patterns and enables scalable enterprise frontend applications.

---

# Purpose

This document defines

- State Architecture
- State Classification
- State Ownership
- Redux Standards
- TanStack Query Standards
- Context API Usage
- Local State
- URL State
- AI Conversation State
- Best Practices

---

# Vision

Build frontend applications where

- State has a single owner.
- Data flows predictably.
- Components remain simple.
- Server state stays synchronized.
- Global state remains minimal.
- Applications scale without state complexity.

---

# State Philosophy

```text
Server

↓

Server State

↓

Feature State

↓

Component State

↓

UI
```

The closer state stays to where it is used,
the better the architecture.

---

# Core Principles

Every application must use

✓ Single Source of Truth

✓ Minimal Global State

✓ Predictable Updates

✓ Immutable State

✓ Typed State

✓ Observable State

✓ Testable State

✓ Server-first Data

---

# State Hierarchy

```text
Server State

↓

Application State

↓

Feature State

↓

Component State

↓

Transient UI State
```

Never promote state unnecessarily.

---

# State Categories

## Server State

Examples

- Users
- Projects
- Reports
- AI Responses
- Search Results
- Knowledge

Managed by

```
TanStack Query
```

---

## Global State

Examples

- Authentication
- Current User
- Tenant
- Theme
- Feature Flags
- Sidebar
- Notifications

Managed by

```
Redux Toolkit
```

---

## Feature State

Examples

Wizard Progress

Selected Items

Filters

Sorting

Temporary Selection

Prefer feature-level stores.

---

## Local State

Examples

Modal Open

Input Value

Dropdown

Tooltip

Hover

Accordion

Managed by

```
useState
```

---

## Form State

Managed by

```
React Hook Form
```

Never duplicate form state.

---

## URL State

Examples

Filters

Pagination

Sorting

Search

Tabs

Selected IDs

URL should represent navigable application state.

---

## AI State

Examples

Conversation

Streaming Tokens

Agent Status

Tool Execution

Thinking State

Prompt History

Citation State

AI state follows NES-218 through NES-230.

---

# Official Technologies

Global State

```
Redux Toolkit
```

Server State

```
TanStack Query
```

Forms

```
React Hook Form
```

Validation

```
Zod
```

Local State

```
React Hooks
```

Persistent State

```
LocalStorage (minimal)

IndexedDB (offline)

SessionStorage (temporary)
```

---

# Decision Matrix

| State Type | Technology |
|------------|------------|
| Local UI | useState |
| Complex Local | useReducer |
| Global | Redux Toolkit |
| Server | TanStack Query |
| Forms | React Hook Form |
| URL | Next.js Router |
| Theme | Context API |
| AI Streaming | Feature Store + Query |
| Offline Cache | IndexedDB |

---

# Redux Standards

Redux stores only

Authentication

Tenant

Feature Flags

Preferences

Notifications

Layout

Never store server data.

---

# Redux Architecture

```text
Store

↓

Slice

↓

Selectors

↓

Hooks

↓

Components
```

---

# Slice Structure

```text
store/

├── auth/

├── tenant/

├── layout/

├── notifications/

├── preferences/

└── featureFlags/
```

Feature slices remain isolated.

---

# Selectors

Always use memoized selectors.

Good

```tsx
selectCurrentUser()
```

Avoid

```tsx
state.user.profile.data.user
```

inside components.

---

# Dispatching

Components dispatch

Actions

↓

Reducers

↓

Store

Never mutate state directly.

---

# TanStack Query

Official responsibilities

Fetching

Caching

Pagination

Invalidation

Optimistic Updates

Background Refetch

Retries

Server Synchronization

---

# Query Architecture

```text
Component

↓

Hook

↓

Query

↓

Service

↓

API
```

---

# Query Keys

Structure

```text
["users"]

["projects", id]

["reports", filters]

["seo", website]
```

Keys must be deterministic.

---

# Mutations

Use

Optimistic Updates

Rollback

Invalidation

Retry

Toast Notifications

---

# Cache Strategy

Configure

Stale Time

Cache Time

Retry

Garbage Collection

Background Refresh

Cache intentionally.

---

# Context API

Use only for

Theme

Localization

Configuration

Authentication Provider

Feature Flags

Never replace Redux.

---

# Local State

Use

```
useState()
```

for

Inputs

Dialogs

Hover

Temporary Selection

Animations

---

# useReducer

Use when

Complex UI

Wizard

Editor

Canvas

Nested State

State Machine

---

# URL State

URL controls

Filters

Search

Sorting

Page

View

Selection

Refreshing the page preserves navigation state.

---

# Persistence

Persist only

Theme

Preferences

Language

Sidebar

Remember Me

Never persist sensitive application state.

---

# AI Conversation State

Track

Messages

Streaming

Tool Calls

Citations

Reasoning Timeline

Conversation Metadata

Conversation history remains synchronized with backend.

---

# Offline State

Support

Queued Actions

Retry

Conflict Resolution

Cache

Synchronization

Offline mode is graceful.

---

# Derived State

Always compute

Example

```tsx
const completedTasks =
tasks.filter(...)
```

Avoid storing derived values.

---

# Immutable Updates

Always

Immutable

Predictable

Typed

Use Immer via Redux Toolkit.

---

# State Ownership

Every state has exactly one owner.

```text
Server

↓

Feature

↓

Component
```

Ownership avoids synchronization bugs.

---

# Data Flow

```text
User

↓

Action

↓

Store

↓

Selector

↓

Component

↓

Render
```

Data flows in one direction.

---

# Error State

Every async state includes

Loading

Success

Error

Retry

Empty

Refreshing

---

# Loading Strategy

Support

Skeleton

Spinner

Optimistic UI

Streaming

Progressive Rendering

Avoid blocking UI.

---

# Security

Never store

JWT

Refresh Token

Secrets

Passwords

Sensitive Customer Data

inside client state.

---

# Multi-Tenancy

State includes

Tenant Context

Permissions

Feature Flags

Localization

Theme

Cross-tenant state leakage is prohibited.

---

# Observability

Track

Store Updates

Query Performance

Cache Hits

State Size

Memory Usage

AI State

Render Counts

---

# Performance

Optimize

Selector Memoization

Component Memoization

Lazy Loading

Virtualization

Small Stores

Minimal Re-renders

---

# Testing

Test

Reducers

Selectors

Hooks

Queries

Mutations

State Transitions

Offline Behavior

---

# Folder Structure

```text
store/

├── index.ts

├── auth/

├── tenant/

├── layout/

├── notifications/

├── featureFlags/

├── preferences/

├── middleware/

├── selectors/

└── hooks/
```

---

# Feature Structure

```text
feature/

├── hooks/

├── queries/

├── mutations/

├── selectors/

├── state/

└── types/
```

---

# Enterprise State Flow

```text
Backend

↓

TanStack Query

↓

Feature Hooks

↓

Redux

↓

React Components

↓

UI
```

---

# KPIs

Global State Size

```
Minimal
```

Duplicate State

```
0
```

Query Cache Hit Rate

```
>90%
```

State Synchronization Bugs

```
0 Critical
```

Selector Coverage

```
100%
```

---

# Anti-Patterns

Avoid

❌ Server Data in Redux

❌ Global State for Local UI

❌ Multiple Sources of Truth

❌ Direct State Mutation

❌ Context for Large Stores

❌ Duplicated Derived State

❌ Fetching Inside Components

❌ Massive Redux Stores

❌ Uncontrolled Global State

❌ Persisting Sensitive Data

---

# Production Checklist

Before production

- [ ] State ownership documented
- [ ] Redux limited to global state
- [ ] TanStack Query configured
- [ ] Query keys standardized
- [ ] Cache strategy reviewed
- [ ] State persistence validated
- [ ] Security review completed
- [ ] Tests passing
- [ ] Performance validated
- [ ] Architecture review approved

---

# Success Criteria

State Management is successful when

- Every piece of state has a clear owner.
- Server data is never duplicated.
- Global state remains minimal.
- Components stay simple and predictable.
- Data synchronization is reliable.
- Applications scale without state complexity.
- AI interactions remain responsive and consistent.
- Developers immediately know where any state belongs.

---

# Future Evolution

Version 2.0 will include

- State Machine Architecture (XState)
- Event-Sourced Frontend State
- Offline Synchronization Framework
- Multi-Tab State Synchronization
- AI Conversation State Engine
- Enterprise Query SDK
- Cache Performance Dashboard
- Redux DevTools Enterprise Guide
- State Visualization Platform
- Frontend Event Bus Architecture
- C4 State Management Architecture
- Architecture Fitness Rules for State
- Production State Management Starter Repository

---

# State Management Standards Checklist

- [x] State Architecture Defined
- [x] State Classification Established
- [x] Redux Standards Defined
- [x] TanStack Query Standards Included
- [x] Context API Usage Defined
- [x] URL & Form State Included
- [x] AI State Management Included
- [x] Performance Standards Added
- [x] Production Checklist Added
- [x] Success Criteria Defined

---

# Document Status

**Document:** NES-306 — State Management Standards

**Version:** 1.0.0

**Status:** Ready for Architecture Review

**Next Document:** **NES-307 — Data Fetching Standards**

---

# Revision Queue for Version 2.0 (Enterprise Edition)

Future enhancements will include

- Enterprise State Management Reference Architecture
- XState Integration Guidelines
- Event-Driven Frontend State Architecture
- Offline-First Synchronization Framework
- Multi-Window State Coordination
- AI Conversation State Engine
- Enterprise Query & Cache SDK
- State Analytics Dashboard
- State Debugging & Visualization Toolkit
- Frontend Event Bus Framework
- C4 Context, Container & State Flow Diagrams
- Architecture Fitness Tests for State Management
- Production Enterprise State Management Starter Repository

These enhancements will establish the definitive State Management Standard for the NeelStack ecosystem, ensuring every frontend application maintains predictable, scalable, secure, and high-performance state architecture while minimizing complexity and maximizing long-term maintainability.