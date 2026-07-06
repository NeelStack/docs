---
ADR-002: PostgreSQL + pgvector as Primary Datastore
Status: Accepted
Date: 2026-07-06

Context:
DhruvaOS needs a transactional datastore with ACID safety guarantees for complex educational records (enrollments, grading, billing) combined with semantic search capabilities for AI-native workflows (RAG queries and agent tools). Operating a standalone vector database alongside a relational database increases operational overhead, cost, and introduces data synchronization replication lag challenges. The system must remain lightweight enough to run locally in a single Docker container.

Decision:
We chose PostgreSQL with the pgvector extension as our unified transactional and vector datastore.

Alternatives Considered:
- Pinecone: Rejected because it is a closed-source SaaS-only vector database which violates our self-hosted/offline requirement, incurs high external costs, and splits state into two separate systems.
- Weaviate / Milvus: Rejected because running a separate dedicated vector database cluster adds high RAM overhead (minimum 1-2GB per instance) and creates complex transactional boundary issues when synchronizing data updates.
- MongoDB: Rejected because its relational integrity constraints, cross-collection transaction locks, and vector index configurations do not meet the performance requirements of our multi-tenant schemas.

Consequences:
We commit to managing indexes (`HNSW` / `IVFFlat`) within PostgreSQL. We accept the tradeoff that high-dimensional vector search queries share CPU and memory pools with transactional billing/attendance queries, requiring PgBouncer query pooling and limits to prevent resource starvation.

Revisit Triggers:
- If a tenant's vector embedding collection grows beyond 10 million active dimensions and semantic search latency breaches a p99 threshold of 150ms.
- If compliance or security requirements mandate a physically separate, certified vector store.
---
