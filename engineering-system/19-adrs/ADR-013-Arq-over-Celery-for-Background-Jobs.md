---
ADR-013: Redis + Arq over Celery and other queues
Status: Accepted
Date: 2026-07-06

Context:
DhruvaOS plugins need to delegate slow administrative tasks (biometric integrations syncs, email reports, bulk student uploads) to backend background workers to prevent blocking the web gateway event loop. We already utilize Redis for feature-flags caching, and we want to avoid introducing separate infrastructure components. The queuing system must natively handle Python's `async/await` syntax to prevent thread pooling overhead.

Decision:
We chose Redis + Arq as our primary background worker queue engine.

Alternatives Considered:
- Celery: Rejected because it lacks native async support (forcing blocking sync calls in workers), uses complex serialization logic, and requires a heavy configuration setup that increases maintenance overhead.
- RQ (Redis Queue): Rejected because it does not support native async job execution natively, creating thread lock issues under high concurrency load.
- AWS SQS + Lambda: Rejected because it locks our platform deployment model to AWS serverless configurations, preventing local dev debugging and offline self-hosted deployments.

Consequences:
We commit to utilizing Arq task definitions backend by Redis. We accept the tradeoff that Arq lacks a built-in admin dashboard UI (like Celery Flower) and complex workflow orchestration features (chords/chains), meaning complex task pipelines must be managed manually in code or delegated to n8n triggers.

Revisit Triggers:
- If our background task volumes exceed 50,000 concurrent jobs per minute, saturating Redis single-threaded execution boundaries.
- If we require highly complex workflow chains with distributed transactions that are too complex to manage in code.
---
