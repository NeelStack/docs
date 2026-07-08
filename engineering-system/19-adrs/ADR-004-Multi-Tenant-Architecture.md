---
ADR-004: Schema-per-Tenant as Default Tenancy Isolation
Status: Accepted
Date: 2026-07-06

Context:
DhruvaOS serves diverse educational customers ranging from small local schools to regional school chains and national government systems. The isolation model must balance strict data segregation security mandates (assuring that schools cannot query other schools' data) with high resource efficiency and minimal database operational cost. Running database-per-tenant clusters for every small pilot tenant creates massive memory/connection socket overhead, while pure shared-table pool models increase noisy-neighbor risk and schema migration friction.

Decision:
We chose Postgres schema-per-tenant (`schema_isolated` mode) using dynamic search_path connection pooling as our default multi-tenancy isolation tier, with escalation triggers to database-per-tenant and dedicated clusters for high-compliance workloads.

Alternatives Considered:
- Shared Pool Table with RLS: Rejected because schema migrations affect all tenants simultaneously, preventing database customization per school, and noisy-neighbor query starvation is high.
- Database-per-tenant by Default: Rejected because it wastes database connection sockets, requires dynamic provisioning of Postgres instances for small pilot schools, and increases cold-start latency.
- Completely Siloed VM-per-Tenant: Rejected due to the extreme operational cost of compute overhead for small-scale educational institutions.

Consequences:
We commit to schema-based routing where connections are bound dynamically using `SET LOCAL search_path = tenant_slug`. We accept the tradeoff that PgBouncer transaction pooling limits must be carefully managed to prevent noisy-neighbor pool starvation.

Revisit Triggers:
- If Postgres schema management count on a single database instance exceeds 10,000 schemas, causing system catalog table access delays.
- If data compliance mandates require physical storage filesystem isolation for a specific tenant.
---
