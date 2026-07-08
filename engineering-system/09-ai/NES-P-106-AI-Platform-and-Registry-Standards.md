---
document_id: NES-P-106
title: AI Platform & Registry Standards
version: 1.0.0
status: Approved
owner: Chief AI Architect
---

# NES-P-106 — AI Platform & Registry Standards

> **"DhruvaOS AI features are governed by a dynamic registry model. Hardcoded agent and tool dispatches are prohibited."**

---

# 1. Purpose

This document outlines the **unified registry architecture, safety guardrails, prompt governance, and evaluation standards** for AI components inside DhruvaOS. It coordinates with the implementation details in our AI core library (`services/ai/src/app/ai/registry.py`).

---

# 2. Expanded AI Registry Hierarchy

The AI service operates an integrated register containing ten dedicated management blocks:

```text
                                  AI Registry
                                       │
        ┌──────────────┬───────────────┼──────────────┬──────────────┐
        ▼              ▼               ▼              ▼              ▼
     Models        Providers        Prompts         Agents         Tools
  (Catalog)      (LLM Connect)     (Templates)    (Orchestrate)  (Functions)
        │              │               │              │              │
        ├──────────────┼───────────────┼──────────────┼──────────────┤
        ▼              ▼               ▼              ▼              ▼
   Evaluations       Memory       Knowledge        Policies     Guardrails
   (QA Test)      (Redis Cache)  (RAG Index)      (Budgets)     (Moderation)
        │
        ▼
  Observability
   (Telemetry)
```

---

# 3. Registry Specifications & Integration

## 3.1 Model & Provider Registry
Decouples LLM capabilities from implementation endpoints. Allows changing default LLM providers via configurations without modifying core application code:

```python
# Registration Pattern
@ModelRegistry.register_model("gpt-4o-mini", provider="OpenAI", capabilities=["chat", "tools"])
class GPT4oMiniConfig:
    temperature = 0.2
    max_tokens = 2048
```

## 3.2 Prompt Registry
Provides dynamic loading and runtime compiling of versioned system instructions:

```python
@PromptRegistry.register_prompt("attendance_alert_v1", version="1.0.0")
class AttendanceAlertPrompt:
    template = "You are an assistant. Flag attendance drops for student {{ student_name }}..."
```

## 3.3 Agent Registry
Maps intent patterns to execution entry-points. Replaces static conditional routers inside the orchestrator engine:

```python
# Class Registration
@AgentRegistry.register_agent("fee_collection", "Processes fee invoices")
class FeeCollectionAgent:
    @classmethod
    async def execute(cls, tenant_context, payload):
        # business logic execution
```

## 3.4 Tool Registry
Compiles Python signatures into JSON schemas dynamically so LLM interfaces can execute native domain commands securely:

```python
@ToolRegistry.register_tool("attendance_lookup", "Retrieves student attendance rate")
def get_attendance(student_id: str) -> float:
    # SQL query returns attendance percentage
```

## 3.5 Evaluation Registry
Exposes automated verification tests to evaluate model outputs (relevance, accuracy) before merging changes to system templates:

```python
@EvaluationRegistry.register_evaluator("relevance_score")
def evaluate_relevance(output: str, reference: str) -> dict:
    # returns score between 0.0 and 1.0
```

## 3.6 Memory Registry
Wraps Redis key storage to query conversation histories and store user-profile contexts under isolated tenant namespaces:

```text
User Memory Store  →  redis:6379/1 → "user:preferences:<tenant>:<user_id>"
Session History    →  redis:6379/2 → "chat:history:<tenant>:<session_id>"
```

## 3.7 Knowledge Registry
Catalogs semantic RAG search sources, document chunk mappings, and vector database indexes:

```python
@KnowledgeRegistry.register_index("admissions_policy", "Standard rules for registration")
class AdmissionsPolicyIndex:
    collection = "admissions_vector_store"
    distance = "cosine"
```

## 3.8 Policy Registry
Enforces limits, daily spending budgets, and permitted models lists:
- Default Tenant Quota: $5.00/day.
- If quota is exceeded, requests raise a standard `402 Quota Exceeded` exception.

## 3.9 Guardrails Registry
Intercepts inputs and outputs to filter unsafe, off-policy, or hallucinated responses:

```python
@GuardrailRegistry.register_guardrail("pii_filter", phase="output")
def block_pii(text: str) -> dict:
    # regex matches emails/phones; returns {"safe": False} if violation detected
```

## 3.10 Observability Registry
Logs token consumption counts, execution times, and calculated inference costs to standard outputs for telemetry collection.

---

# 4. Adding AI Components

Engineers must decorate new agents and functions with their respective registries. Direct integration into main routing handlers is forbidden.
All new prompt classes require a matching evaluation score file in tests to prevent regressions.
