---
ADR-015: Platform Kernel + Plugin Architecture over Monolith and Microservices
Status: Accepted
Date: 2026-07-06

Context:
DhruvaOS manages highly diverse educational workflows (enrollment, grading, attendance, payroll) across thousands of multi-tenant school entities. A monolithic design leads to code bloating and tight couplings that break deployment cycles. A pure microservices model introduces massive network latencies, complex data consistency sagas, high operational hosting costs, and resource sprawl that conflicts with our lightweight local-first development goals.

Decision:
We chose a modular Platform Kernel + Dynamic Plugin loading architecture (mounted at boot via a shared core runtime).

Alternatives Considered:
- Pure Microservices: Rejected due to high memory overhead of running 10+ Python containers, network serialization latencies, and complex distributed transaction management requirements.
- Standard Monolith: Rejected because domain modules become tightly coupled, making it impossible to enable/disable features per tenant or deploy isolated client extensions securely.
- Serverless Functions (FaaS): Rejected because it eliminates local offline developer execution, prevents state caching, and increases runtime latency under cold starts.

Consequences:
We commit to building domain modules as isolated plugins that declare routes, events, and permissions inside YAML manifests (`module.yaml`). We accept the tradeoff that all modules share the same Python virtual machine process memory and CPU space locally, meaning a memory leak or crash inside a single plugin (e.g., grading) can bring down the entire kernel service.

Revisit Triggers:
- If a plugin's resource consumption (e.g. CPU spikes during analytics generation) regularly starves other core services in the same runtime instance.
- If the development team expands past 50 engineers, causing merge bottlenecks and deployment schedule friction inside the core monorepo.
---
