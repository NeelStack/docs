---
document_id: NES-010
title: Glossary
subtitle: Standard Engineering, Product, Platform, AI, and Business Terminology
version: 1.0.0
status: Active
classification: Internal
owner: NeelStack Architecture Team
approver: Chief Solution Architect
created: 2026-07-04
last_updated: 2026-07-04
review_cycle: Every 12 Months
maturity: L5 (Gold Standard)
document_type: Reference
parent_document: NES-009 Engineering Maturity Model
next_document: NES-011 FAQ
---

# NeelStack Engineering Glossary

> **"A shared language creates shared understanding. Shared understanding creates better engineering."**

---

# Executive Summary

As NeelStack grows, engineers, architects, product managers, designers, AI systems, and business stakeholders must communicate using a consistent vocabulary.

The purpose of this glossary is to establish standard definitions for commonly used terms throughout the NeelStack Engineering System (NES).

Every engineering document should use terminology defined in this glossary.

When ambiguity exists, the definitions in this document take precedence.

---

# Purpose

This glossary provides a common language for:

- Engineering
- Architecture
- Product Development
- Platform Engineering
- Artificial Intelligence
- Security
- DevOps
- Operations
- Business
- Governance

Consistent terminology reduces misunderstandings and improves decision-making.

---

# How to Use This Glossary

Definitions should be:

- Concise
- Consistent
- Technology-agnostic where possible
- Aligned with the NeelStack Engineering System

Terms are organized alphabetically.

---

# A

## ADR (Architecture Decision Record)

A structured document that records significant architectural decisions, their context, alternatives, rationale, and consequences.

Every major architectural decision should have an associated ADR.

---

## API (Application Programming Interface)

A defined contract that enables communication between software systems.

APIs should be versioned, documented, secure, and backward compatible whenever practical.

---

## Architecture

The fundamental organization of a software system, including its components, relationships, constraints, and guiding principles.

Architecture governs long-term system evolution.

---

## Authentication

The process of verifying the identity of a user, service, or system.

Authentication answers:

> "Who are you?"

---

## Authorization

The process of determining what an authenticated user or system is allowed to do.

Authorization answers:

> "What are you allowed to access?"

---

## Audit Log

A chronological record of significant system activities used for security, compliance, debugging, and operational visibility.

---

# B

## Backend

The server-side software responsible for business logic, data processing, APIs, integrations, and system workflows.

---

## Business Capability

A reusable business function that delivers value independently of implementation technology.

Examples:

- Student Management
- Billing
- Notifications
- Reporting

---

## Business Domain

A logical area of responsibility representing a distinct business problem.

Domains own business rules and related data.

---

# C

## CI/CD

Continuous Integration and Continuous Delivery/Deployment.

A set of engineering practices that automate software building, testing, and deployment.

---

## Clean Architecture

An architectural approach emphasizing separation of concerns, dependency inversion, maintainability, and testability.

Business rules remain independent of frameworks.

---

## Component

A reusable software building block with a clearly defined responsibility.

Components should be cohesive and loosely coupled.

---

## Continuous Improvement

An ongoing process of making incremental enhancements to products, engineering practices, documentation, and operations.

---

# D

## Database

A structured repository for persistent data.

Each business domain should own its data.

---

## Deployment

The process of making software available in an operational environment.

Deployments should be automated and repeatable.

---

## DevOps

A culture and engineering practice that integrates software development with operational responsibilities through automation and collaboration.

---

## Domain

A distinct business area with clearly defined ownership, responsibilities, and boundaries.

---

# E

## Engineering Standard

A documented requirement describing how engineering work should be performed within NeelStack.

Engineering standards ensure consistency across products and teams.

---

## Event

A record that something significant has occurred within the system.

Events enable loosely coupled communication between services.

---

## Event-Driven Architecture (EDA)

An architectural style where systems communicate through events rather than direct synchronous interactions.

---

# F

## Feature

A customer-visible capability that solves a specific business problem.

Features should always create measurable value.

---

## Frontend

The client-facing portion of an application responsible for user interaction and presentation.

---

# G

## Governance

The framework of policies, standards, reviews, and decision-making processes that guide engineering activities.

Governance protects long-term quality.

---

# H

## Health Check

An endpoint or mechanism used to determine whether a service is functioning correctly.

Health checks support monitoring and automated recovery.

---

## High Availability (HA)

A system design objective ensuring services remain operational despite failures.

---

# I

## Infrastructure as Code (IaC)

Managing infrastructure using version-controlled code rather than manual configuration.

Examples include Terraform and OpenTofu.

---

## Integration

Communication between systems through APIs, events, queues, or other interfaces.

---

## Incident

An unplanned event that negatively affects service quality, reliability, security, or availability.

Every significant incident should result in a post-incident review.

---

# J

## Journey

The complete sequence of interactions a user performs to achieve a business goal.

Products should optimize end-to-end journeys rather than isolated screens.

---

# K

## KPI (Key Performance Indicator)

A measurable indicator used to evaluate progress toward a strategic objective.

KPIs should be objective, actionable, and reviewed regularly.

---

## Knowledge Base

A structured repository of documentation, standards, playbooks, FAQs, and organizational knowledge.

Knowledge should be accessible to both humans and AI systems.

---

# L

## Logging

The structured recording of application and infrastructure events.

Logs support debugging, monitoring, auditing, and incident investigation.

---

## Long-Term Support (LTS)

A release strategy providing extended maintenance, security updates, and stability.

---

# M

## Microservice

An independently deployable service responsible for a specific business capability.

Microservices should communicate through well-defined APIs or events.

---

## Monorepo

A repository containing multiple related projects managed within a single version-control repository.

NeelStack adopts a monorepo strategy for platform consistency and developer productivity.

---

## Monitoring

The continuous observation of systems through metrics, logs, traces, and alerts.

Monitoring enables proactive operations.

---

# N

## Notification

A mechanism for informing users or systems of important events.

Examples:

- Email
- SMS
- Push Notifications
- In-App Messages

---

## Non-Functional Requirement (NFR)

A quality attribute describing how a system should operate.

Examples:

- Performance
- Reliability
- Security
- Scalability
- Accessibility

---

# O

## Observability

The ability to understand internal system behavior through logs, metrics, traces, and telemetry.

Observability extends beyond traditional monitoring.

---

## Ownership

Clear responsibility for a product, service, document, capability, or process.

Every engineering artifact should have an identified owner.

---

# P

## Platform

A collection of reusable technical capabilities shared across multiple products.

The platform provides common services, tooling, and infrastructure.

---

## Product

A software solution that delivers measurable value to customers by solving defined business problems.

Products should evolve continuously.

---

## Pull Request (PR)

A proposed set of code changes submitted for review before merging into the primary branch.

PRs support collaboration and quality assurance.

---

## Production

The live environment where customers use software.

Production systems require the highest engineering discipline.

---

# Q

## Quality Gate

A mandatory checkpoint that software must satisfy before progressing to the next stage.

Examples:

- Code Review
- Security Review
- Testing
- Documentation

---

# R

## Repository

A version-controlled storage location containing source code, documentation, configuration, and engineering artifacts.

---

## Reliability

The ability of a system to consistently perform its intended function over time.

Reliability directly influences customer trust.

---

## Roadmap

A strategic plan describing the evolution of products, platforms, engineering capabilities, and organizational goals.

Roadmaps communicate direction rather than detailed implementation plans.

---

# S

## Scalability

The ability of a system to support increasing workloads without significant degradation in performance or maintainability.

---

## Service

A software component that provides a well-defined business or technical capability.

Services should have clear ownership and documented interfaces.

---

## SLO (Service Level Objective)

A target level of service performance used internally to guide operational excellence.

---

## SLA (Service Level Agreement)

A customer-facing commitment describing expected service performance.

---

## Sprint

A fixed period during which a team completes a defined set of planned work items.

---

## Standard

A documented and approved engineering requirement that must be followed across the organization.

---

# T

## Technical Debt

The future cost incurred by choosing an easier or faster solution instead of a more maintainable one.

Technical debt should be visible, documented, and actively managed.

---

## Telemetry

Operational data collected from software systems, including metrics, logs, traces, and events.

Telemetry supports observability and operational decision-making.

---

## Test Coverage

The percentage of software exercised by automated tests.

Coverage is one indicator of testing completeness but not a guarantee of quality.

---

## U

## User Experience (UX)

The overall experience users have while interacting with a product.

UX includes usability, accessibility, performance, and satisfaction.

---

## User Interface (UI)

The visual and interactive elements through which users interact with software.

UI contributes to—but does not fully define—the user experience.

---

# V

## Versioning

A systematic approach to managing changes in software or APIs.

NeelStack adopts Semantic Versioning for software and engineering standards.

---

## Vision

A long-term description of the future state the organization seeks to achieve.

The vision provides strategic direction.

---

# W

## Workflow

A defined sequence of activities performed to achieve a business or technical objective.

Workflows should be automated whenever practical.

---

# X

No standard engineering terms currently defined.

Reserved for future expansion.

---

# Y

No standard engineering terms currently defined.

Reserved for future expansion.

---

# Z

## Zero Downtime Deployment

A deployment strategy that updates software without interrupting service availability.

This is the preferred deployment model for production systems.

---

# Naming Conventions

Throughout the NeelStack Engineering System, the following naming conventions apply.

| Prefix | Meaning |
|---------|---------|
| NES | NeelStack Engineering Standard |
| ADR | Architecture Decision Record |
| RFC | Request for Comments |
| API | Application Programming Interface |
| KPI | Key Performance Indicator |
| SLO | Service Level Objective |
| SLA | Service Level Agreement |
| SLI | Service Level Indicator |
| AI | Artificial Intelligence |
| IDP | Internal Developer Platform |

---

# Glossary Governance

This glossary is a living document.

New terminology should:

- Be approved through engineering governance.
- Remain consistent with existing definitions.
- Avoid duplicate or conflicting meanings.
- Be referenced by future engineering standards.

Changes should be reviewed annually or when significant architectural concepts are introduced.



# Acronym Dictionary

To ensure consistent communication across engineering, architecture, product, AI, security, and operations, NeelStack standardizes the following acronyms.

| Acronym | Meaning |
|----------|---------|
| ADR | Architecture Decision Record |
| API | Application Programming Interface |
| CI | Continuous Integration |
| CD | Continuous Delivery / Continuous Deployment |
| CI/CD | Continuous Integration & Delivery |
| CRUD | Create, Read, Update, Delete |
| DDD | Domain-Driven Design |
| DoD | Definition of Done |
| DoR | Definition of Ready |
| EDA | Event-Driven Architecture |
| EHS | Engineering Health Score |
| IaC | Infrastructure as Code |
| IDP | Internal Developer Platform |
| KPI | Key Performance Indicator |
| LLM | Large Language Model |
| MTTR | Mean Time to Recovery |
| MVP | Minimum Viable Product |
| NFR | Non-Functional Requirement |
| OKR | Objectives and Key Results |
| PR | Pull Request |
| RBAC | Role-Based Access Control |
| RFC | Request for Comments |
| SDK | Software Development Kit |
| SLA | Service Level Agreement |
| SLI | Service Level Indicator |
| SLO | Service Level Objective |
| SRE | Site Reliability Engineering |
| UI | User Interface |
| UX | User Experience |

These acronyms should be used consistently throughout all engineering documentation.

---

# Product Terminology

The following terms describe concepts commonly used across all NeelStack products.

---

## Capability

A reusable business or technical function.

Examples:

- Authentication
- Search
- Reporting
- Workflow

Capabilities are reusable across multiple products.

---

## Module

A cohesive collection of related functionality within a product.

Examples:

- Student Module
- Billing Module
- HR Module

Modules should own their business logic.

---

## Workspace

A logical environment where users perform related activities.

Workspaces improve organization and user productivity.

---

## Tenant

An independent customer organization within a multi-tenant platform.

Each tenant should have isolated:

- Data
- Configuration
- Security
- Permissions

---

## Organization

A business entity using one or more NeelStack products.

Organizations may contain multiple users, roles, departments, and workspaces.

---

## Workspace Member

A user with access to a specific workspace.

Permissions are controlled through roles.

---

# Platform Terminology

---

## Platform Capability

A reusable service provided by the NeelStack Platform.

Examples:

- Identity
- Notification
- Billing
- Search
- AI Gateway

Capabilities should be consumed rather than duplicated.

---

## Platform Service

A deployable service providing one or more platform capabilities.

Platform services expose APIs or events.

---

## Shared Component

A reusable frontend or backend component shared across multiple products.

Examples include:

- UI Components
- Authentication Middleware
- Email Templates

---

## Internal Developer Platform (IDP)

A platform that improves developer productivity through automation, tooling, templates, infrastructure, and self-service capabilities.

---

# AI Terminology

---

## AI Gateway

A centralized platform service responsible for routing requests to supported AI models.

Responsibilities include:

- Authentication
- Rate limiting
- Prompt routing
- Cost monitoring
- Model selection

---

## Prompt

Instructions provided to an AI model to generate a response.

Prompts should be version-controlled when used in production.

---

## Prompt Template

A reusable prompt containing placeholders for dynamic values.

Templates improve consistency and maintainability.

---

## AI Agent

An autonomous software component capable of performing multi-step tasks using AI models and external tools.

Agents should operate within defined governance boundaries.

---

## Embedding

A numerical representation of text used for semantic search and retrieval.

---

## Vector Database

A database optimized for storing and searching embeddings.

Typically used in Retrieval-Augmented Generation (RAG) systems.

---

## RAG (Retrieval-Augmented Generation)

An AI architecture where external knowledge is retrieved and supplied to an AI model before generating a response.

This improves factual accuracy and reduces hallucinations.

---

## Hallucination

An incorrect or fabricated AI-generated response.

Critical business decisions should never rely solely on AI output.

---

# Security Terminology

---

## Least Privilege

Users and systems receive only the permissions required to perform their responsibilities.

---

## Secret

Sensitive information that must never be exposed publicly.

Examples:

- API Keys
- Passwords
- Private Keys
- Tokens

---

## Threat Model

A structured analysis identifying potential security threats, vulnerabilities, attack vectors, and mitigation strategies.

Threat modeling should occur during system design.

---

## Vulnerability

A weakness that may be exploited to compromise confidentiality, integrity, or availability.

Vulnerabilities should be prioritized based on risk.

---

## Zero Trust

A security model where no user, device, or service is automatically trusted.

Verification is required for every request.

---

# Database Terminology

---

## Entity

A business object represented in the data model.

Examples:

- Student
- Course
- Teacher
- Invoice

---

## Aggregate

A cluster of related entities treated as a single consistency boundary.

The aggregate root controls modifications.

---

## Migration

A controlled change to the database schema.

Every schema modification should be version-controlled.

---

## Read Model

A data structure optimized for queries rather than updates.

Frequently used in CQRS architectures.

---

## Transaction

A group of operations executed as a single atomic unit.

Transactions preserve data consistency.

---

# Cloud Terminology

---

## Availability Zone

An isolated data center within a cloud region.

Multiple zones improve resilience.

---

## Region

A geographic location containing one or more availability zones.

Regions support low latency and disaster recovery.

---

## Container

A lightweight execution environment packaging an application and its dependencies.

Containers improve portability and deployment consistency.

---

## Kubernetes Cluster

A collection of nodes that run containerized workloads.

Clusters provide orchestration, scaling, and resilience.

---

## Infrastructure Stack

A collection of infrastructure resources managed as a single unit.

Stacks should be defined using Infrastructure as Code.

---

# Documentation Terminology

---

## Standard

A mandatory engineering requirement.

---

## Guideline

A recommended engineering practice.

---

## Policy

An organizational rule that governs behavior.

---

## Playbook

A step-by-step operational guide for performing repeatable activities.

---

## Runbook

An operational document describing how to execute or recover a production process.

---

## Checklist

A verification document used before completing an engineering activity.

---

## Template

A reusable document or implementation structure.

Templates improve consistency and productivity.

---

# Reference Index

The glossary supports all NeelStack Engineering Standards.

| Standard | Reference |
|----------|-----------|
| NES-000 | Engineering Handbook |
| NES-001 | Company Vision |
| NES-002 | Mission |
| NES-003 | Core Values |
| NES-004 | Engineering Culture |
| NES-005 | Product Philosophy |
| NES-006 | Company Roadmap |
| NES-007 | Engineering KPIs |
| NES-008 | Success Principles |
| NES-009 | Engineering Maturity Model |
| NES-010 | Glossary |
| NES-011 | FAQ |

Future engineering standards should reference this glossary rather than redefining terminology.

---

# Glossary Maintenance Process

The glossary evolves alongside the NeelStack Engineering System.

When introducing a new term:

1. Verify it does not duplicate an existing definition.
2. Use clear, technology-agnostic language where practical.
3. Define ownership if applicable.
4. Cross-reference related standards.
5. Submit the addition through engineering governance.
6. Update the glossary version.

The glossary should remain the single source of truth for engineering terminology.

---

# Closing Statement

A shared vocabulary is one of the foundations of a mature engineering organization.

By standardizing terminology across engineering, architecture, product management, AI, operations, and leadership, NeelStack reduces ambiguity, improves communication, and strengthens collaboration.

As the organization grows, this glossary should evolve carefully while maintaining consistency with the NeelStack Engineering System.



