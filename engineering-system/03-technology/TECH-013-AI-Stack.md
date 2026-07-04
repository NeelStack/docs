---
document_id: TECH-013
title: AI Stack Standard
subtitle: The approved AI and LLM technology stack for all NeelStack AI-powered features
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Chief AI Architect
review_cycle: Every 3 Months
document_type: Technology Standard
parent_document: TECH-012 Terraform
next_document: REPO-001 Monorepo
---

# TECH-013 — AI Stack Standard

---

## Approved AI Technologies

| Category | Technology | Purpose |
|---|---|---|
| **LLM Providers** | OpenAI GPT-4o, Gemini 1.5 Pro, Anthropic Claude 3.5 | Text generation, reasoning |
| **Embedding Models** | OpenAI text-embedding-3-large, Gemini Embedding | Vector embeddings |
| **Vector DB (primary)** | pgvector | Embedded in PostgreSQL |
| **Vector DB (scale)** | Qdrant | High-volume embedding search |
| **AI Framework** | LangChain, LlamaIndex | RAG pipelines |
| **Agent Framework** | LangGraph, CrewAI | Multi-agent workflows |
| **MCP** | Model Context Protocol SDK | Tool calling standard |
| **Observability** | LangSmith, Langfuse | LLM tracing |
| **Prompt Management** | Langfuse | Version-controlled prompts |

## LLM Abstraction Layer

All LLM calls MUST go through the NeelStack AI abstraction layer — never call provider SDKs directly:

```python
# ✅ Correct — via abstraction
from neelstack.ai import LLMClient

llm = LLMClient(model="gpt-4o", tenant_id=tenant_id)
response = await llm.complete(prompt)

# ❌ Wrong — direct SDK call
from openai import AsyncOpenAI
client = AsyncOpenAI()
```

This ensures: model switching, cost tracking, rate limiting, and observability are applied universally.

## AI Cost Controls

- Cost limits set per tenant per month
- Alerts triggered at 80% of budget
- Automatic model downgrade when cost limit approached
- All LLM calls logged with token counts

## Related Standards

- NES-218 — AI Knowledge Platform
- NES-219 — AI Agent Architecture
- NES-220 — MCP Standards
- NES-221 — Prompt Engineering Standards
- NES-222 — AI Model Management
- TECH-001 — Technology Stack

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-07-04 | Initial publication |
