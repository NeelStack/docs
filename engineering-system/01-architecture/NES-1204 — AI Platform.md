---
document_id: NES-1204
title: AI Platform
subtitle: Enterprise AI & LLM Inference Platform Reference Architecture Blueprint
version: 1.0.0
status: Draft
classification: Internal
owner: AI & Data Science Board
review_cycle: Every 6 Months
document_type: Reference Architecture
parent_document: NES-1203 CRM
next_document: NES-1205 Marketplace
---

# NES-1204 — AI Platform

> **"AI scale requires low-latency inference. This reference blueprint details our GPU node configurations, model routing layers, and vector search stores."**

---

# Executive Summary

To deploy, manage, and monitor Large Language Models (LLMs) and custom AI agents at scale while maintaining security, compliance, and latency SLAs, we must enforce a unified architecture.

This document establishes the official **NeelStack AI Platform Reference Architecture** blueprint.

It defines our AI Gateway routing configurations, GPU resource orchestration, Vector Database standards, and security guardrail layers.

---

# Purpose

This standard defines:

- Unified AI Platform Reference Architecture Map
- AI Gateway and Model Routing Configs
- GPU and Compute Node Orchestrations
- Vector Database Integrations (pgvector / Qdrant)
- Safety and Guardrails Gating

---

# AI Platform Reference Architecture Map

The AI Platform separates request validations, inference runs, and storage layers:

```text
               Public Ingress (Client API queries, HTTPS)
                               │
                               ▼
        AI Gateway (Rate limits, token caching, routing)
                               │
       ┌───────────────────────┴───────────────────────┐
       ▼ (Passes validation)                           ▼ (Fails guardrails)
  Inference Compute Zone                      Block Request (HTTP 400)
  ├── GPU Node Groups (EKS managed)
  │    └── vLLM / Triton Server
  └── CPU Node Groups (Embedding models)
                               │
                               ▼
  Data Layer (AWS RDS pgvector / Qdrant cluster)
  └── Context vector storage (1536-dim embeddings)
```

---

# AI Gateway & Model Routing Standards

All application queries targeting AI models must pass through the **AI Gateway**:

- **Model Routing**: The gateway routes incoming prompts to the appropriate backend model based on performance requirements (e.g. routing simple classifications to local models, and complex reasoning tasks to external LLMs).
- **Token Caching**: Cache model outputs for identical input prompt hashes inside Redis (NES-208), reducing GPU compute costs.

---

# GPU Compute & Inference Optimization

Optimize compute allocations:

- **EKS GPU Groups**: Host model inference tasks on AWS EKS GPU node groups (using NVIDIA Tensor Core instances).
- **Inference Engines**: Run optimized inference servers (vLLM or Triton Inference Server) that support continuous batching and quantization to maximize throughput.

---

# Vector Database Standards

For Retrieval-Augmented Generation (RAG) context caching:

- **Vector Store**: Use **pgvector** inside Amazon RDS PostgreSQL for standard application search context, and dedicated **Qdrant** clusters for high-scale vector lookups.
- **Dimensionality**: Standardize on **1536-dimensional** vector configurations (compatible with OpenAI text-embedding-3-small or similar models) using Cosine distance indexes.

---

# Safety & Guardrail Gates

Protect models from prompt injection and prevent sensitive data leaks:

- **Input Guardrails**: Run lightweight scanners to check inputs for prompt injection or malicious scripts before forwarding queries to models.
- **Output Guardrails**: Verify that model outputs do not contain plaintext PII or violation language strings before returning them to users.

---

# Anti-Patterns

❌ **Hardcoding API Keys in Clients**: Storing external AI model API keys inside web frontend code, exposing keys to attackers.

❌ **Exposing GPU Nodes Directly**: Direct routing to Triton/vLLM backend ports, bypassing the AI Gateway rate limiter.

❌ **Omitting Token Caching**: Querying external APIs for identical, repetitive queries, causing high monthly cloud bills.

---

# Production Checklist

- [ ] AI Gateway is active and enforcing rate limits.
- [ ] GPU node groups use vLLM/Triton.
- [ ] Vector database index uses pgvector/Qdrant.
- [ ] Input and output guardrails are verified.
- [ ] Token cache policies are active in Redis.

---

# Success Criteria

The AI Platform Reference Architecture is successful when:
- Inference API response times (Time-To-First-Token) remain under 500ms.
- Token caching strategies reduce external API costs by 30% or more.
- Security filters intercept and block all prompt injection attempts.

---

# Document Status

**Document:** NES-1204 — AI Platform
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1205 — Marketplace**
