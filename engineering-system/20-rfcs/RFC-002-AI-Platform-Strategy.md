---
document_id: RFC-002
title: NeelStack AI Platform Strategy
status: Draft
date: 2026-07-04
author: AI Architecture Team
reviewers: CTO, Chief AI Architect, Backend Lead
discussion_deadline: 2026-08-15
---

# RFC-002 — NeelStack AI Platform Strategy

## Summary

This RFC defines the strategic direction for building the NeelStack AI Platform — a shared, multi-tenant AI infrastructure layer powering all NeelStack products with RAG, agents, and knowledge management.

## Motivation

Each product (EduOS, Toolvines, DhruvaOS) is independently implementing AI features. This creates:
- Duplicate LLM integration code across products
- No shared prompt management
- No cross-product knowledge reuse
- Inconsistent AI observability
- Cost inefficiency from duplicate model calls

## Proposal

Build a **centralized AI Platform Service** that all products consume via API:

```
EduOS / Toolvines / DhruvaOS
         │
         ▼
AI Platform Service
├── Knowledge Ingestion API
├── RAG Query API  
├── Agent Orchestration API
├── Prompt Registry
├── Model Router (multi-LLM)
├── Cost Tracker
└── Observability (Langfuse)
         │
         ▼
LLM Providers (OpenAI, Gemini, Claude)
Vector DB (pgvector / Qdrant)
```

### Phase 1 (Q3 2026): Foundation
- Unified LLM abstraction layer
- Centralized prompt registry (Langfuse)
- Basic RAG pipeline (pgvector + OpenAI embeddings)
- Cost tracking per tenant

### Phase 2 (Q4 2026): Knowledge Platform
- Multi-tenant knowledge ingestion
- Hybrid search (vector + keyword)
- Knowledge graph foundations

### Phase 3 (Q1 2027): Agents
- Agent framework (LangGraph)
- MCP server implementations
- Multi-agent coordination

## Open Questions

1. Should the AI Platform be a separate deployable service or a shared library?
2. What is the SLA for the AI Platform given LLM latency variability?
3. How do we handle LLM provider outages (fallback strategy)?

## Related Standards

- NES-218 — AI Knowledge Platform
- NES-219 — AI Agent Architecture
- NES-220 — MCP Standards
- TECH-013 — AI Stack Standard
