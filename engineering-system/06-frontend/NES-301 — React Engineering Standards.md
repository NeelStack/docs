---
document_id: NES-301
title: React Engineering Standards
subtitle: Enterprise React Architecture, Component Engineering & Best Practices Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Frontend Architecture Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-300 Frontend Engineering Standards
next_document: NES-302 Next.js Architecture
---

# NES-301 — React Engineering Standards

> **"React is not a UI library in NeelStack. It is the foundation of our enterprise frontend platform."**

---

# Executive Summary

This document defines the official React engineering standards for every NeelStack application.

It standardizes

- React Architecture
- Component Design
- Hooks
- State Management
- Performance
- Rendering Strategy
- Error Handling
- Testing
- Accessibility
- Security
- Code Organization

Every React application across the NeelStack ecosystem must follow these standards.

---

# Purpose

This document defines

- React Architecture
- Component Standards
- Hook Standards
- Rendering Strategy
- State Management
- Performance Optimization
- Error Handling
- Testing
- Security
- Best Practices

---

# Vision

Build enterprise React applications that are

- Fast
- Predictable
- Type Safe
- Maintainable
- Scalable
- AI Ready
- Accessible

for products serving millions of users.

---

# React Philosophy

```text
Application

↓

Feature

↓

Components

↓

Hooks

↓

State

↓

Services

↓

Backend APIs
```

Components render UI.

Hooks manage behavior.

Services communicate with APIs.

---

# Official React Version

Official Version

```
React Latest Stable
```

Always upgrade after enterprise validation.

---

# Core Principles

Every React application must be

✓ Functional

✓ Component Driven

✓ Declarative

✓ Type Safe

✓ Testable

✓ Performant

✓ Accessible

✓ Reusable

✓ Predictable

---

# Enterprise React Architecture

```text
App

↓

Layout

↓

Feature

↓

Container

↓

Presentational Component

↓

Primitive Component
```

Each layer has one responsibility.

---

# Rendering Philosophy

Prefer

Server Components

↓

Client Components only when required

↓

Streaming

↓

Suspense

↓

Progressive Rendering

---

# Component Hierarchy

```text
Page

↓

Feature

↓

Container

↓

Business Component

↓

Shared Component

↓

Primitive Component
```

---

# Component Rules

Every component

- Has one responsibility
- Has typed props
- Is reusable
- Has predictable rendering
- Avoids hidden side effects

---

# Component Classification

Primitive

Shared

Business

Feature

Page

Layout

Provider

AI Components

---

# Component Naming

Good

```text
UserCard

ProjectList

InvoiceTable

LoginForm
```

Avoid

```text
Component1

Test

Card2

TempComponent
```

---

# Component Size

Recommended

```
<200 Lines
```

Maximum

```
400 Lines
```

Split large components.

---

# Props Standards

Always

Type Props

Keep Immutable

Use Interfaces

Prefer Composition

Avoid Boolean Explosion

---

# Example

Good

```tsx
<UserCard
    user={user}
    editable
/>
```

Avoid

```tsx
<UserCard
    data={data}
    mode={1}
    flag={true}
/>
```

---

# Children

Prefer

Composition

```tsx
<Card>

    <CardHeader/>

    <CardBody/>

</Card>
```

Avoid deeply nested conditional rendering.

---

# Hooks

Prefer built-in hooks

useState

useEffect

useMemo

useCallback

useReducer

useRef

useId

useTransition

---

# Custom Hooks

Business logic belongs inside hooks.

Example

```text
useUsers()

useProjects()

useInvoice()

useChat()

useAI()
```

---

# Hook Rules

Never

Call conditionally

Call inside loops

Call inside callbacks

Mutate hook state directly

Rules of Hooks are mandatory.

---

# State Management

Local

```
useState
```

Complex Local

```
useReducer
```

Global

```
Redux Toolkit
```

Server

```
TanStack Query
```

---

# Derived State

Always compute

Never duplicate

Example

Good

```tsx
const total = items.length
```

Avoid

```tsx
const [total,setTotal]
```

when derivable.

---

# Effects

Effects synchronize with external systems.

Effects should never replace business logic.

---

# useEffect Rules

Avoid

Fetching without cleanup

Infinite loops

Complex business logic

Large dependency arrays

Prefer custom hooks.

---

# Memoization

Use

useMemo

useCallback

React.memo

only when profiling demonstrates value.

Do not prematurely optimize.

---

# Context API

Use only for

Theme

Authentication

Localization

Feature Flags

Configuration

Avoid global business state.

---

# Forms

Official stack

React Hook Form

+

Zod

Never build custom form state unless required.

---

# Error Boundaries

Every application includes

Global Error Boundary

Feature Error Boundary

Async Error Handling

Fallback UI

---

# Suspense

Use

Lazy Loading

Streaming

Async Components

Never block entire pages.

---

# Data Fetching

Always through

TanStack Query

or

Server Components

Never call fetch inside UI components repeatedly.

---

# API Layer

```text
Component

↓

Hook

↓

Service

↓

API Client
```

Components never know HTTP implementation.

---

# Performance

Optimize

Code Splitting

Memoization

Virtualization

Suspense

Streaming

Lazy Components

Image Optimization

---

# Lists

Always use

Stable Keys

Virtualization

Pagination

Infinite Scroll

for large datasets.

---

# Accessibility

Support

Keyboard Navigation

ARIA

Semantic HTML

Focus Management

Screen Readers

Accessible forms

---

# Security

Protect against

XSS

Unsafe HTML

Token Leakage

Client Secrets

Prototype Pollution

Never trust browser input.

---

# AI Components

AI components support

Streaming

Markdown

Code Blocks

Citations

Tool Status

Reasoning Status

Human Approval

Following NES-218 through NES-230.

---

# Styling

Official

Tailwind CSS

shadcn/ui

Never use inline styles except dynamic calculations.

---

# File Naming

Components

```
PascalCase.tsx
```

Hooks

```
use*.ts
```

Utilities

```
camelCase.ts
```

Types

```
*.types.ts
```

---

# Folder Structure

```text
feature/

├── components/

├── hooks/

├── services/

├── types/

├── validation/

├── constants/

├── tests/

└── index.ts
```

---

# Testing

Support

Unit Tests

Hook Tests

Component Tests

Accessibility Tests

Snapshot Tests (minimal)

E2E Tests

---

# Observability

Capture

Rendering Errors

Performance

User Actions

API Failures

AI Events

OpenTelemetry Browser SDK is recommended.

---

# React Performance Budget

Initial Bundle

```
<250 KB (gzip target)
```

Component Render

```
<16ms
```

Interaction Response

```
<100ms
```

Core Web Vitals must meet Google's "Good" thresholds.

---

# CI/CD Quality Gates

Every PR must pass

TypeScript

ESLint

Unit Tests

Accessibility

Build

Bundle Analysis

Security Scan

---

# Folder Structure

```text
react/

├── app/

├── features/

├── components/

├── hooks/

├── providers/

├── services/

├── store/

├── lib/

├── types/

├── utils/

├── tests/

└── docs/
```

---

# Anti-Patterns

Avoid

❌ Class Components

❌ Business Logic Inside JSX

❌ Massive Components

❌ Prop Drilling

❌ Unnecessary Context

❌ Duplicate State

❌ Direct API Calls

❌ Inline Anonymous Functions Everywhere

❌ useEffect Abuse

❌ Uncontrolled Re-renders

---

# Production Checklist

Before production

- [ ] Components follow architecture
- [ ] Props fully typed
- [ ] Hooks extracted
- [ ] Performance validated
- [ ] Accessibility tested
- [ ] Security review completed
- [ ] Error boundaries configured
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Architecture review approved

---

# Success Criteria

React Engineering is successful when

- Components are small, reusable, and composable.
- Business logic remains outside presentation.
- Rendering is predictable and performant.
- Applications remain accessible and secure.
- State management is simple and maintainable.
- Testing is straightforward.
- AI interfaces integrate naturally.
- Developers can confidently scale the codebase.

---

# Future Evolution

Version 2.0 will include

- React Compiler Adoption Guide
- React Server Components Handbook
- Suspense Architecture Patterns
- Enterprise Hook Library
- Advanced Performance Optimization Guide
- Accessibility Component Catalog
- AI UI Component Standards
- Storybook Integration Guide
- React Performance Benchmark Suite
- Frontend ADRs for React
- C4 React Architecture Diagrams
- Architecture Fitness Rules for React
- Production React Starter Repository

---

# React Engineering Standards Checklist

- [x] React Architecture Defined
- [x] Component Standards Established
- [x] Hook Standards Defined
- [x] State Management Strategy Included
- [x] Performance Standards Added
- [x] Accessibility Requirements Included
- [x] Security Standards Defined
- [x] Testing Strategy Established
- [x] Production Checklist Added
- [x] Success Criteria Defined

---

# Document Status

**Document:** NES-301 — React Engineering Standards

**Version:** 1.0.0

**Status:** Ready for Architecture Review

**Next Document:** **NES-302 — Next.js Architecture**

---

# Revision Queue for Version 2.0 (Enterprise Edition)

Future enhancements will include

- React 20 Enterprise Adoption Guide
- React Compiler Migration Strategy
- Server Components Deep Dive
- Enterprise Hook & Utility Library
- Component Composition Patterns
- Streaming UI & Suspense Blueprint
- Storybook Reference Architecture
- AI-Native React Components
- Enterprise Performance Profiling Guide
- C4 Context, Container & Component Diagrams
- UML Component Interaction Diagrams
- Architecture Fitness Tests for React Applications
- Production React Enterprise Starter Repository

These enhancements will establish the definitive React Engineering Standard for the NeelStack ecosystem, ensuring every React application is scalable, maintainable, performant, accessible, secure, and consistent across all enterprise products while supporting long-term evolution of the platform.