---
ADR-001: FastAPI as Primary Backend Framework
Status: Accepted
Date: 2026-07-06

Context:
NeelStack requires a high-performance web framework for the DhruvaOS backend to serve AI-native microservices and concurrent database operations under a small platform engineering team. We need native async/await capabilities to prevent thread blocking during long-running LLM API calls, alongside automatic documentation generation to support dynamic plugin client bindings. The framework must utilize Python due to existing developer skills and machine learning integrations.

Decision:
We chose FastAPI as our primary backend framework for core API and AI Gateway services.

Alternatives Considered:
- Django / DRF: Rejected due to its synchronous-first design which creates connection starvation when orchestrating concurrent async AI requests, and its heavy monolithic database models overhead.
- Flask: Rejected because it lacks built-in async routing support, data validation schemas (Pydantic), and auto-generated OpenAPI, requiring too many third-party packages to maintain.
- Node.js (Express/NestJS): Rejected because it separates the web service runtime from our primary Python-based machine learning libraries, necessitating complex IPC/gRPC layers for AI features.

Consequences:
FastAPI commits us to utilizing SQLAlchemy/Pydantic for database and validation patterns rather than an integrated ORM. We accept the tradeoff of having to manually orchestrate code layouts and service configurations due to FastAPI's unopinionated micro-framework structure.

Revisit Triggers:
- If microservice count scales past 50 and API compilation times/auto-docs generation bottleneck container startup performance.
- If node/rust backend technologies develop native, high-performance direct bindings to our core ML pipelines.
---
