---
document_id: NES-231
title: AI Development Guide
version: 1.1.0
status: Draft
owner: Chief AI Architect
---

# NES-231 — AI Development Guide

> **"NeelStack standardizes AI integration to ensure intelligence features are decoupled, high-performance, and multi-tenant secure."**

---

# 1. Purpose

This document serves as the **official enterprise development guide and reference architecture** for engineers extending, validating, or deploying AI services inside the NeelStack ecosystem. It outlines the architecture of the dedicated AI Gateway Microservice (`services/ai`), specifies codebase formatting, and provides concrete guidelines for prompt engineering, provider abstraction, autonomous agents, RAG pipelines, streaming, cost governance, and testing.

---

# 2. AI Request Lifecycle

Every inference request flowing through the AI Gateway follows a strict pipeline:

```text
  [Client Request]
         │
         ▼
 1. Authentication          ──► Validates OIDC JWT (Keycloak)
         │
         ▼
 2. Tenant Resolution       ──► Establishes active school_id context
         │
         ▼
 3. Authorization           ──► Verifies RBAC / Feature licensing
         │
         ▼
 4. Rate Limiting           ──► Checks per-tenant / global sliding window
         │
         ▼
 5. AI Cache Lookup         ──► Hits Redis exact/semantic cache
         │
 ┌───────┴───────┐
 │ Cache Miss?   │
 └───────┬───────┘
         │
         ▼
 6. Context Retrieval       ──► Queries pgvector database (school_id filtered)
         │
         ▼
 7. Prompt Construction     ──► Compiles system/user prompts from versioned files
         │
         ▼
 8. LLM Execution           ──► Executes model provider via abstraction interface
         │
         ▼
 9. Output Validation       ──► Sanitizes response and validates schema JSON
         │
         ▼
10. Telemetry & Auditing    ──► Logs cost metrics, token counts, and latency
         │
         ▼
[Client Response] (SSE Stream or JSON)
```

---

# 3. Codebase Directory Layout

The `services/ai` directory is organized modularly to ensure clean separation of concerns and scaling:

```text
services/ai/
│
├── requirements.txt            # Python dependencies
├── pyproject.toml              # Build configurations
│
└── src/
    └── app/
        ├── main.py             # App entry point & router mounting
        │
        ├── core/               # Platform utility core
        │   ├── config.py       # Configuration schemas & environment limits
        │   └── security.py     # Authentication & tenant token parsing
        │
        ├── prompts/            # Centralized external prompt files
        │   ├── attendance/
        │   │   ├── system.md
        │   │   └── user.md
        │   └── report_gen/
        │       └── system.md
        │
        ├── providers/          # Interchangeable LLM model providers
        │   ├── base.py         # BaseLLMProvider interface
        │   ├── openai.py       # OpenAI GPT implementation
        │   ├── gemini.py       # Google Gemini integration
        │   └── anthropic.py    # Anthropic Claude implementation
        │
        ├── knowledge/          # Ingestion and Vector Search (RAG)
        │   ├── chunking.py     # Text splitters & normalization
        │   ├── retrieval.py    # Vector database queries & distance metrics
        │   └── pipeline.py     # PDF parsing & OCR extraction pipelines
        │
        ├── agents/             # Autonomous agent orchestrators
        │   ├── orchestrator.py # Agent coordinator & intent mapping
        │   └── attendance/     # attendance agent bundle
        │       ├── planner.py  # Execution steps planner
        │       ├── tools.py    # Class hooks (e.g. database / email tools)
        │       ├── prompts.md  # Agent specific rules
        │       └── schemas.py  # Validated input/output interfaces
        │
        ├── modules/            # HTTP Routers & Service layers
        │   └── prediction/
        │       ├── router.py   # HTTP router routing requests
        │       └── service.py  # Business logic & provider orchestration
        │
        └── tests/              # Test suites
```

---

# 4. Prompt Management Layer

Prompts **must never** be hardcoded in Python code. Instead, they are defined in separate markdown files under `/app/prompts` to decouple wording updates from application code changes.

### Prompt Rendering Helper

```python
# app/core/prompts.py
import os
from jinja2 import Template

class PromptLoader:
    PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")

    @classmethod
    def load_and_render(cls, domain: str, name: str, **kwargs) -> str:
        filepath = os.path.join(cls.PROMPTS_DIR, domain, f"{name}.md")
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Prompt template not found: {filepath}")
            
        with open(filepath, "r", encoding="utf-8") as file:
            template_content = file.read()
            
        template = Template(template_content)
        return template.render(**kwargs)
```

---

# 5. LLM Provider Abstraction

All model communications are channeled through provider abstractions. This enables plug-and-play swapping of model backends (OpenAI, Anthropic, Gemini, Ollama) without modifying business logic.

### 5.1 Base Provider Interface

```python
# app/providers/base.py
from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, Any

class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate(self, system_prompt: str, user_prompt: str, options: Dict[str, Any] = None) -> str:
        """Executes a standard blocked inference call."""
        pass

    @abstractmethod
    async def stream(self, system_prompt: str, user_prompt: str, options: Dict[str, Any] = None) -> AsyncGenerator[str, None]:
        """Yields chunks of text in real-time as a generator."""
        pass

    @abstractmethod
    async def get_embeddings(self, text: str) -> list[float]:
        """Generates embedding vectors for RAG indexing."""
        pass
```

### 5.2 OpenAI Implementation Example

```python
# app/providers/openai.py
import openai
from app.providers.base import BaseLLMProvider
from app.core.config import settings

class OpenAIProvider(BaseLLMProvider):
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def generate(self, system_prompt: str, user_prompt: str, options: dict = None) -> str:
        opts = options or {}
        response = await self.client.chat.completions.create(
            model=opts.get("model", settings.DEFAULT_CHAT_MODEL),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=opts.get("temperature", 0.2)
        )
        return response.choices[0].message.content

    async def stream(self, system_prompt: str, user_prompt: str, options: dict = None) -> AsyncGenerator[str, None]:
        opts = options or {}
        stream_response = await self.client.chat.completions.create(
            model=opts.get("model", settings.DEFAULT_CHAT_MODEL),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=opts.get("temperature", 0.2),
            stream=True
        )
        async for chunk in stream_response:
            content = chunk.choices[0].delta.content
            if content:
                yield content

    async def get_embeddings(self, text: str) -> list[float]:
        response = await self.client.embeddings.create(
            model=settings.DEFAULT_EMBEDDING_MODEL,
            input=text
        )
        return response.data[0].embedding
```

---

# 6. RAG Ingestion Pipeline

RAG documents are stored inside the `document_vectors` table using `pgvector`. The file ingestion pipeline is structured as follows:

```text
[Raw PDF File]
       │
       ▼
 1. Extract Text       ──► Uses OCR (Tesseract / EasyOCR) for scanned PDFs
       │
       ▼
 2. Clean Text         ──► Removes page numbers, headers, and normalizes space
       │
       ▼
 3. Text Chunking      ──► Split by token count (e.g. 500 tokens with 50 overlap)
       │
       ▼
 4. Add Metadata       ──► Appends school_id, author_id, and document_id tags
       │
       ▼
 5. Vectorise          ──► Passes text chunk to BaseLLMProvider.get_embeddings()
       │
       ▼
 6. DB Persistence     ──► Inserts chunk text and vector into PostgreSQL database
```

---

# 7. Real-Time Streaming (SSE)

Real-time streaming uses Server-Sent Events (SSE). Use `StreamingResponse` from FastAPI yielding formatted event chunks:

```python
# app/modules/prediction/router.py
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.providers.openai import OpenAIProvider

router = APIRouter()

@router.get("/stream-chat")
async def chat_stream(question: str, provider: OpenAIProvider = Depends(OpenAIProvider)):
    async def event_generator():
        system_prompt = "You are a helpful educational assistant."
        async for chunk in provider.stream(system_prompt, question):
            # Send chunks formatted according to SSE standard
            yield f"data: {json.dumps({'content': chunk})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

---

# 8. Caching Strategy (Redis)

To minimize prompt costs and API latencies, inference calls must be cached. NeelStack implements a two-stage Redis caching architecture:

```text
 [Prompt Request]
        │
        ▼
  1. Exact Hash Match  ──► Compute SHA-256 of Prompt ──► Hits Redis Cache? ──► [Return JSON]
        │ (Miss)
        ▼
  2. LLM Inference     ──► Generate Response ──► Save JSON to Redis (TTL 3600s)
```

---

# 9. Observability & Telemetry

Every inference call records detailed usage telemetry into OpenTelemetry and Prometheus collectors:

- **Token Consumption**: Track input, output, and total tokens.
- **Latency Tracker**: Log latency in milliseconds for RAG lookup, Embedding time, and LLM provider time.
- **Cost Accumulation**: Translate token counts directly to USD based on model pricing metadata.
- **System Metrics**: Monitor provider error rates, cache hit ratios, and fallback model activations.

---

# 10. Configuration Parameters

All environment-specific variables are managed inside `app/core/config.py` using `PydanticBaseSettings`:

```python
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "DhruvaOS AI Gateway"
    API_V1_STR: str = "/api/v1"
    
    # Model Configurations
    OPENAI_API_KEY: str
    DEFAULT_CHAT_MODEL: str = "gpt-4o"
    DEFAULT_EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # Hyperparameters
    DEFAULT_TEMPERATURE: float = 0.2
    DEFAULT_MAX_TOKENS: int = 2048
    
    # Limits & Caches
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL_SECONDS: int = 3600
    RATE_LIMIT_PER_TENANT_SEC: int = 10
```

---

# 11. Agent Architecture & Tool Calling

Agents are designed with a clean separation of roles: the **Planner** breaks down objectives, **Tools** execute concrete operations, and the **Executor** handles looping and fallback logic.

### 11.1 Agent Execution Cycle

```text
[Goal Intent] ──► 1. Planner ──► 2. Tool Selection ──► 3. Tool Execution ──► 4. Output validation ──► Response
```

### 11.2 Tool Definition Example

```python
# app/agents/attendance/tools.py
from typing import Dict, Any

class DatabaseTools:
    @classmethod
    async def get_attendance_records(cls, school_id: int, student_id: int) -> Dict[str, Any]:
        """Queries the active PostgreSQL database context for student attendance data."""
        # Simulated database retrieval
        return {"student_id": student_id, "attendance_rate": 78.5}

class CommunicationTools:
    @classmethod
    async def send_warning_notice(cls, parent_email: str, content: str) -> bool:
        """Sends an email notice using SMTP services."""
        return True
```

---

# 12. Error Handling & Fallback Strategy

AI calls must be resilient. When a primary provider experiences failures (rate limits, timeouts, or downtime), the microservice automatically fails over to secondary/fallback models:

```python
# app/modules/prediction/service.py
import logging
from app.providers.openai import OpenAIProvider
from app.providers.gemini import GeminiProvider

logger = logging.getLogger("dhruvaos.prediction")

class CompletionService:
    @classmethod
    async def generate_text_with_fallback(cls, system: str, user: str) -> str:
        # Stage 1: Try Primary Provider (OpenAI GPT-4o)
        try:
            primary = OpenAIProvider()
            return await primary.generate(system, user)
        except Exception as e:
            logger.warning(f"[AI Fallback] OpenAI failed: {e}. Transitioning to Gemini fallback.")
            
            # Stage 2: Fallback Provider (Gemini 1.5 Flash)
            try:
                fallback = GeminiProvider()
                return await fallback.generate(system, user)
            except Exception as fe:
                logger.error(f"[AI Failure] Critical. All providers failed: {fe}")
                raise RuntimeError("Central LLM inference platform currently unavailable.")
```

---

# 13. AI Coding Standards & Software Layering

To prevent tight coupling, code files must adhere to strict software boundaries:

1. **Routers**: Handle request inputs, validate query parameters, parse tenant context headers, and return response formats. **Never** initiate LLM calls directly in router methods.
2. **Services**: Orchestrate operations, compile prompts using `PromptLoader`, fetch RAG vector contexts, manage caching strategies, and handle provider fallbacks.
3. **Providers**: Abstractions managing API call formatting, parsing SDK payloads, and computing raw embedding lists.

---

# 14. Testing Guidelines

AI behaviors are tested across three dimensions:

- **Unit Mock Tests**: Verify schemas, prompt loading, error boundaries, and routers using standard pytest mocks (`unittest.mock.AsyncMock`) instead of hitting live LLM provider endpoints.
- **Snapshot Assertions**: Lock system prompts in snapshots and verify prompt rendering outputs on dynamic input payloads.
- **Embedding Retrieval Tests**: Verify pgvector indexing and cosine similarity query distances using test database migrations.

---

# 15. Cost Governance & Tenant Quotas

To prevent cost overruns in a multi-tenant environment, the platform tracks cost accumulation per tenant:

1. **Daily budget checks**: Every request checks Redis for current daily USD cost.
2. **Quota Enforcement**: If a tenant's daily consumption exceeds their subscribed tier limit, the service raises a `HTTP 402 Payment Required` exception.
3. **Usage logging**: Inference parameters (input/output tokens, models used) are dispatched to the auditing logs for invoice compiling.
