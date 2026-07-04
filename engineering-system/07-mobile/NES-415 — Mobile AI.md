---
document_id: NES-415
title: Mobile AI
subtitle: Enterprise Mobile AI Orchestration, On-Device Models & Speech Standards
version: 1.0.0
status: Draft
classification: Internal
owner: Mobile & AI Architecture Board
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-414 Crash Reporting
next_document: NES-416 Mobile Reference Architecture
---

# NES-415 — Mobile AI

> **"Intelligent mobile apps require balanced processing. We execute lightweight classifiers on-device and orchestrate generative tasks securely via API gateways."**

---

# Executive Summary

Mobile devices possess specialized hardware (Neural Engine on iOS, NPU on Android) capable of executing machine learning models directly on the client.

Additionally, mobile applications consume large language models (LLMs) via cloud APIs for document intelligence, support agents, and code validation.

This standard defines the architecture, security parameters, and performance boundaries for orchestrating AI features on mobile devices.

---

# Purpose

This standard defines:

- Local vs. Remote AI workloads
- On-Device Machine Learning (ONNX, TensorFlow Lite)
- Cloud LLM Orchestration and API Security
- Speech-to-Text (STT) and Text-to-Speech (TTS) integration
- Client Context and Privacy safeguards

---

# Local vs. Remote AI Workload Division

AI features must be partitioned strategically to manage battery usage, device storage limitations, and network latency:

| Workload Type | Execution Location | Technologies | Rationale |
|---|---|---|---|
| Image Classification, OCR Pre-processing, Text Tokenization | **On-Device (Local)** | ONNX Runtime / CoreML | Zero latency, offline support, zero cloud billing. |
| Chat Assistants, Document Summarization, RAG Queries | **Cloud (Remote)** | OpenAI / Anthropic via API Gateway | Heavy computing requirements, proprietary prompts protection. |

---

# On-Device Machine Learning (ONNX Runtime)

We standardize on **ONNX Runtime (or TensorFlow Lite)** for running local, compiled models on mobile.

- **Model size limit**: Local model sizes must be kept below **15MB** to prevent app store download limits.
- **Async Execution**: Models must run inside separate web workers or async native tasks to prevent freezing the UI thread during computation cycles.

---

# Remote LLM Orchestration & API Security

Mobile applications must **never** call third-party LLM providers (e.g. OpenAI, Anthropic) directly using hardcoded API keys.

- **Gateway Pattern**: Route all AI queries through the central **NeelStack AI Gateway (NES-218)**.
- **Benefits**: Enforces rate limiting, token budgets, authentication verification, and prevents API key extraction from decompiled application binaries.

```typescript
import { api } from '@/lib/api';

export async function askAgent(prompt: string, documentId: string): Promise<string> {
  // Call central NeelStack AI gateway instead of third-party APIs directly
  const { data } = await api.post('/ai/agent/query', {
    prompt,
    documentId,
  });

  return data.answer;
}
```

---

# Speech Integration (STT / TTS)

For audio-enabled learning portals and accessibility support, we integrate Speech-to-Text and Text-to-Speech APIs.

- **Standard (TTS)**: Use `expo-speech` for basic text translation. It accesses native iOS and Android speech synthesisers without network overhead.
- **Standard (STT)**: For voice commands, use first-party cloud-based transcription (e.g., Whisper API via AI Gateway) to guarantee accuracy across diverse languages and accents.

```typescript
import * as Speech from 'expo-speech';

export function speakInstructions(text: string) {
  Speech.speak(text, {
    language: 'en-US',
    pitch: 1.0,
    rate: 0.9,
  });
}
```

---

# Context Privacy & Data Security

We protect user data during AI interactions.

- **Context Isolation**: When sharing text context with remote LLMs, ensure all personal identifiable information (PII) is scrubbed or tokenized on the client.
- **Local Cache**: Local AI history, vector databases (like local SQLite vector embeddings), and cached prompts must be stored in secure storage folders (`FileSystem.documentDirectory`) and deleted when the user logs out.

---

# Anti-Patterns

❌ **Hardcoded Prompt Keys**: Committing system instructions and prompt keys inside React Native files. Prompts must be versioned and served dynamically from the backend.

❌ **Running Heavy Models Local**: Attempting to run large multi-million parameter models on low-end budget smartphones, causing thermal throttling and OS crashes.

❌ **Sending Unvalidated Text Blocks**: Sending huge document payloads directly from mobile storage to cloud LLMs, causing high data usage and token billing. Compress and chunk text context first.

---

# Production Checklist

- [ ] All API keys are removed from the client build bundle.
- [ ] Large local models are loaded dynamically post-installation rather than embedded in the application bundle.
- [ ] Speech permissions are declared contextually with explanatory labels.
- [ ] Data sanitization filters run on all user-submitted text fields before gateway dispatch.

---

# Success Criteria

The Mobile AI integration is successful when:
- Voice input transcription displays response options in less than 1.5 seconds.
- Local OCR and layout detection executes successfully without blocking screen rendering.
- Zero raw keys are exposed inside the compiled application files.

---

# Document Status

**Document:** NES-415 — Mobile AI
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-416 — Mobile Reference Architecture**
