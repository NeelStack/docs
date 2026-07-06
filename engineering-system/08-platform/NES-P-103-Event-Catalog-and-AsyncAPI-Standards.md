---
document_id: NES-P-103
title: Event Catalog & AsyncAPI Standards
version: 1.0.0
status: Approved
owner: Platform Architecture Team
---

# NES-P-103 — Event Catalog & AsyncAPI Standards

> **"Events are first-class platform API contracts. Every cross-plugin message flow must be declared, versioned, and schema-validated."**

---

# 1. Purpose

This document defines the **schema governance, publishing contracts, and runtime validation criteria** for event-driven flows inside the DhruvaOS architecture. It establishes how event-catalog manifest schemas are declared under the `events/` repository root and governed by the `PlatformSDK.events` publisher middleware.

---

# 2. Schema Location & Naming Conventions

All events must compile standard AsyncAPI specifications. They are organized within the main monorepo under a unified directory:

```text
neelstack-foundation/
└── events/
    ├── student.created.v1.yaml
    ├── student.deactivated.v1.yaml
    ├── attendance.marked.v1.yaml
    ├── exam.completed.v1.yaml
    └── fee.paid.v1.yaml
```

**Naming Standard**: `<entity>.<action>.v<N>.yaml`
- `<entity>`: The domain entity name in singular snake_case (e.g., `student`, `attendance`, `fee`).
- `<action>`: The past-tense mutation descriptor (e.g., `created`, `marked`, `paid`).
- `v<N>`: The integer version identifier representing schema layouts (e.g., `v1`, `v2`).

---

# 3. Schema Manifest Structure

Each event contract file must define the payload, producer, consumers, schema version, retry policies, and idempotency keys. 

### YAML Contract Template Example:
```yaml
# AsyncAPI Event Schema Contract
event: student.created
version: 1.0.0
description: Dispatched when a student is successfully admitted to the system.

# Governance Metadata
metadata:
  producer: app.modules.admission
  consumers:
    - app.modules.attendance
    - app.modules.accounts
    - app.modules.library
  schema_version: 1.0.0

# Operations Governance
policy:
  retry_policy:
    max_attempts: 5
    backoff: exponential
    initial_delay_seconds: 2
    dead_letter_queue: dlq.student.created.v1
  idempotency:
    required: true
    key_path: "payload.student_id" # Path inside payload to compute signature hash

# Payload Specification
payload:
  type: object
  properties:
    student_id:
      type: string
      format: uuid
      description: The unique global identifier of the student.
    tenant_id:
      type: string
      description: The tenant schema identifier.
    first_name:
      type: string
    last_name:
      type: string
    email:
      type: string
      format: email
    admission_date:
      type: string
      format: date-time
  required:
    - student_id
    - tenant_id
    - first_name
    - last_name
    - admission_date
```

---

# 4. Message Broker (NATS JetStream) Mapping

The SDK translates namespaces into NATS hierarchical subject topics dynamically:

- **NATS Subject Prefix**: `dhruvaos.<event_name>.<version>`
- **Example NATS Subject**: `dhruvaos.student.created.v1`

---

# 5. Core Operational Requirements

## 5.1 Retry Policies
Every consumer must specify its retry boundaries:
- **Exponential Backoff**: Backoff multipliers double the delay between attempts (`2s`, `4s`, `8s`, `16s`, `32s`).
- **Dead Letter Queue (DLQ)**: If all retries fail, payloads are pushed to the DLQ for diagnostic review and manual replay triggers.

## 5.2 Idempotency Requirements
Network retries are expected. Consumers **MUST** ensure operations are idempotent:
1. Extract the designated `idempotency.key_path` value (e.g., `payload.student_id`) from incoming message contexts.
2. Query a Redis lock-table (`idempotent:event:<hash_key>`) with a lease time of `86400` seconds (24 hours).
3. Reject or skip execution if the lock has already been set, returning a successful ACK to prevent duplicate processing.

---

# 6. Schema Governance & Breaking Changes

1. **Non-breaking modifications**: Adding optional fields or metadata annotations does not warrant a subject change. Only the minor version property in the YAML description updates.
2. **Breaking modifications**: Removing mandatory fields, changing types, or altering logic triggers a schema major version upgrade (e.g., `student.created.v2.yaml`).
3. **Deprecation**: When a new major version is released, consumers have a minimum of **2 Sprints** to migrate to the new subject stream before the legacy topic is deactivated.
