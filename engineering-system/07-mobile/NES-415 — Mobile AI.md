---
document_id: NES-415
title: Mobile AI
subtitle: Enterprise Mobile AI Orchestration & Speech Standards
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

Mobile devices possess specialized hardware (NPUs, Neural Engines) that can run models directly in local WebViews via WebAssembly or native plug bindings.

Additionally, our mobile applications connect to LLM web APIs for summarizations, visual document parsing, and educational chatbots.

This standard outlines rules for task division, on-device AI runtimes, secure gateway access, and speech APIs inside WebView wrappers.

---

# Purpose

This standard defines:

- Local vs. Remote task division guidelines
- On-device AI utilizing WebAssembly (Wasm) and ONNX
- Cloud AI gateway patterns
- Speech Integration (TTS/STT) via web standard APIs
- PII sanitization constraints

---

# Local vs. Remote Task Division

| Task Type | Environment | Technology | Rationale |
|---|---|---|---|
| Image OCR pre-processing, text tokenizations, simple models | **On-Device (Local)** | ONNX Runtime Web (Wasm) | Low latency, no network cost, data stays local. |
| Chatbots, document summarizations, RAG search | **Cloud (Remote)** | OpenAI / Gemini via Gateway | Requires high compute resource; prompt security. |

---

# On-Device Machine Learning (ONNX Web)

We use **ONNX Runtime Web** (WebAssembly backed) to execute client-side classifiers inside the WebView.

- **Size Threshold**: Local model binaries must remain under **15MB** to prevent slow application starts.
- **Background Workers**: Run inference tasks inside standard Web Workers to prevent blocking the WebView UI main thread:

```typescript
// worker.ts
import { InferenceSession } from 'onnxruntime-web';

addEventListener('message', async (event) => {
  const { modelUrl, inputs } = event.data;
  const session = await InferenceSession.create(modelUrl);
  const results = await session.run(inputs);
  postMessage(results);
});
```

---

# Cloud LLM Gateway

Mobile clients must **never** store third-party LLM API keys (e.g. Anthropic, OpenAI) inside front-end source files, as packages can be easily extracted from WebViews.

- **Gateway Rule**: Route all AI queries through the central **NeelStack AI Gateway (NES-218)**.

```typescript
import { api } from '@/lib/api';

export async function askAgent(prompt: string, documentId: string): Promise<string> {
  const { data } = await api.post('/ai/agent/query', {
    prompt,
    documentId,
  });
  return data.answer;
}
```

---

# Speech Integration (TTS / STT)

We leverage standard browser web APIs supported inside iOS and Android WebViews to handle audio operations.

- **Text-to-Speech (TTS)**: Use standard **`window.speechSynthesis`**:

```typescript
export function speakInstructions(text: string) {
  if ('speechSynthesis' in window) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    utterance.rate = 0.9;
    window.speechSynthesis.speak(utterance);
  }
}
```

- **Speech-to-Text (STT)**: Use the Web Speech API's **`SpeechRecognition`** interface (checking for webkit prefixed instances on iOS):

```typescript
export function startVoiceRecognition(onResult: (text: string) => void) {
  const SpeechRecognition = window.SpeechRecognition || (window as any).webkitSpeechRecognition;
  if (!SpeechRecognition) return null;

  const recognition = new SpeechRecognition();
  recognition.lang = 'en-US';
  recognition.interimResults = false;

  recognition.onresult = (event: any) => {
    const text = event.results[0][0].transcript;
    onResult(text);
  };

  recognition.start();
  return recognition;
}
```

---

# Anti-Patterns

❌ **Hardcoded Prompt Logic in Web Views**: Committing system instructions inside client scripts. Prompts must reside on the backend database.

❌ **Sending Uncompressed Documents**: Posting raw multi-megabyte text payloads directly to remote API gateways, causing heavy data consumption.

---

# Production Checklist

- [ ] Private API keys are removed from the client code.
- [ ] Large model files are loaded dynamically post-boot.
- [ ] Speech permissions are declared with user-facing descriptions.
- [ ] PII attributes are cleaned before sending text to external nodes.

---

# Success Criteria

The Mobile AI standard is successful when:
- Speech recognition translates voices within 1.5 seconds.
- Local processing runs without blocking animations or inputs.
- Telemetry logs confirm zero raw credentials leaked in bundles.

---

# Document Status

**Document:** NES-415 — Mobile AI
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-416 — Mobile Reference Architecture**
