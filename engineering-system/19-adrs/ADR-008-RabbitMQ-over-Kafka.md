---
ADR-008: NATS + JetStream over Kafka and RabbitMQ
Status: Accepted
Date: 2026-07-06

Context:
DhruvaOS plugins require high-throughput asynchronous event communication (enrollment alerts, attendance logs, webhook distributions). We need a messaging broker that provides message persistence (streaming and replay capabilities) while running on local developer laptops with zero performance overhead. Our team size is small, which constraints our ability to maintain complex message clustering technologies.

Decision:
We chose NATS + JetStream as our primary event broker and message streaming system.

Alternatives Considered:
- Apache Kafka: Rejected due to the operational complexity of KRaft/ZooKeeper node management, heavy memory overhead (requires JVM), and steep setup costs relative to our team's operational capacity.
- RabbitMQ: Rejected because its native broker configurations do not support stream persistence or message replay out-of-the-box, requiring specialized management extensions.
- AWS SQS: Rejected because it introduces AWS platform lock-in, lacks local offline support, and does not provide unified pub/sub topic patterns.

Consequences:
We commit to using NATS JetStream protocols via the unified `PlatformSDK.events` namespace. We accept the tradeoff that NATS has a smaller developer ecosystem and fewer pre-built integrations than Kafka or RabbitMQ, meaning we must construct schema validation pipelines and backpressure buffering layers manually inside our kernel code.

Revisit Triggers:
- If our event processing pipeline grows to ingest more than 100,000 events per second and requires Kafka-style partitioned logs disk scaling.
- If we merge with or deploy onto a customer environment where NATS ports are completely restricted by internal networking compliance rules.
---
