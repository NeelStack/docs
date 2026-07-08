---
document_id: NES-P-101
title: Plugin Framework Standard
version: 1.0.0
status: Approved
owner: Platform Architecture Team
---

# NES-P-101 — Plugin Framework Standard

> **"Every feature in DhruvaOS is a plugin. The platform provides the kernel; plugins provide the value."**

---

# 1. Purpose

This document defines the **official standard for building, registering, and deploying domain plugins** inside the DhruvaOS platform. It covers plugin anatomy, the module manifest specification, lifecycle hooks, dependency declarations, event contracts, and governance rules.

All engineers adding new domain features must follow this standard.

---

# 2. What is a Plugin?

A **plugin** is an independently loadable domain module that:

- Declares its own routes, permissions, events, and sidebar navigation
- Registers itself via a `module.yaml` manifest at startup
- Consumes platform capabilities through `PlatformSDK` — never by importing drivers directly
- Emits and consumes domain events through the NATS JetStream bus
- Can be enabled/disabled per tenant through feature flags

---

# 3. Plugin Directory Layout

```text
services/core/src/app/modules/<plugin-name>/
├── module.yaml          ← Plugin manifest (required)
├── router.py            ← FastAPI router (required)
├── service.py           ← Business logic
├── schema.py            ← Pydantic request/response models
├── models.py            ← SQLAlchemy ORM models
├── events.py            ← Event producers and consumers
├── ai_tools.py          ← Registered AI tools for this domain
├── tasks.py             ← Background Arq task definitions
└── tests/
    ├── test_router.py
    └── test_service.py
```

---

# 4. Module Manifest Specification (`module.yaml`)

Every plugin must contain a `module.yaml` file at its root. This is the complete, authoritative specification:

```yaml
# Unique identifier (snake_case)
id: attendance

# Human-readable name
name: Attendance

# Semantic version
version: 1.0.0

# Module description
description: >
  Manages daily student and staff attendance logging, biometric integrations,
  SMS alerts for absent students, and attendance analytics.

# Python import path to the FastAPI router object
entry_point: app.modules.attendance.router.router

# HTTP routing configuration
routes:
  prefix: /api/v1/attendance
  tags:
    - attendance

# RBAC permission identifiers for this module
permissions:
  - attendance.view
  - attendance.create
  - attendance.edit
  - attendance.delete
  - attendance.export

# NATS JetStream event contracts
events:
  produces:
    - attendance.marked
    - attendance.bulk_updated
  consumes:
    - student.created
    - student.deactivated

# AI tools exposed by this module to the AI Gateway registry
ai_tools:
  - attendance_lookup
  - attendance_summary_report

# Sidebar navigation configuration for the web portal
sidebar:
  parent: Academics         # Top-level nav group
  label: Attendance
  icon: calendar-check      # Icon identifier from the design system
  route: /workspace/attendance
  order: 2                  # Position within parent group

# Modules that must be loaded before this plugin
dependencies:
  - students
  - classes

# Feature flags that guard optional capabilities in this module
feature_flags:
  - biometric_integration
  - bulk_sms_alerts
  - auto_report_generation
```

All fields marked **required** will cause the Plugin Loader to reject the manifest at startup if absent.

| Field          | Required | Description                                            |
| -------------- | :------: | ------------------------------------------------------ |
| `id`           | ✅       | Snake-case unique identifier                          |
| `name`         | ✅       | Display name                                          |
| `version`      | ✅       | Semantic version                                      |
| `entry_point`  | ✅       | Python dotted path to the FastAPI router              |
| `routes`       | ✅       | HTTP prefix and tags                                  |
| `permissions`  | ✅       | RBAC permission list                                  |
| `events`       | ❌       | Produced and consumed NATS event topics               |
| `ai_tools`     | ❌       | AI Registry tool identifiers                          |
| `sidebar`      | ❌       | Navigation config for web portal                      |
| `dependencies` | ❌       | Other module IDs required before this one loads       |
| `feature_flags`| ❌       | Tenant-level flags guarding optional behaviours       |

---

# 5. Plugin Loader Runtime

The `PluginLoader` (`services/core/src/app/kernel/plugin_loader.py`) operates at application startup:

```text
Application Start
      │
      ▼
Scan /modules/ and /plugins/ directories
      │
      ▼
Parse each module.yaml manifest
      │
      ▼
Resolve dependency order (topological sort)
      │
      ▼
For each plugin (in dependency order):
  1. Validate manifest schema
  2. importlib.import_module(entry_point)
  3. app.include_router(router, prefix=routes.prefix)
  4. Register permissions in RBAC store
  5. Register AI tools in ToolRegistry
  6. Subscribe to consumed events in NATS
      │
      ▼
Server Ready
```

---

# 6. Event Contract Rules

- Every event listed in `events.produces` must have a corresponding YAML schema file in `/events/`.
- Schema filename format: `<event-name>.v<N>.yaml`
- Producers own the schema; consumers must validate against it.
- Breaking schema changes require a new version: `attendance.marked.v2.yaml`.

---

# 7. Platform SDK Usage Rules

Domain plugin code **must** access infrastructure through `PlatformSDK`. Direct driver imports are forbidden.

```python
# ✅ Correct
from app.sdk.platform import platform
await platform.events.publish("attendance.marked", payload)
await platform.notifications.send_sms(phone, message)

# ❌ Forbidden — never import drivers directly in domain code
import nats
from twilio.rest import Client
```

---

# 8. Platform & Plugin Versioning

To evolve the core services without causing regression breaks in active domain modules, the system establishes a strict version governance framework:

1. **FastAPI Routes Versioning**: All plugin endpoints must be explicitly versioned in their path prefixes (e.g., `/api/v1/attendance`). Breaking endpoint contract adjustments must bump to `/api/v2/` and keep the v1 router mounted during a deprecation window (minimum of 2 sprints).
2. **SDK and Kernel Bindings (`requires_sdk`)**: Plugins declare compatibility ranges inside `module.yaml`:
   ```yaml
   requires_sdk: ">=1.2.0, <2.0.0"
   ```
   If a plugin is loaded on a kernel that falls outside of this compatibility limit, the `PluginLoader` raises a boot exception.
3. **SDK Version Adapters**: If changes are made to the `PlatformSDK` interfaces, the SDK classes must deploy backward-compatibility wrappers/adapters rather than immediate deprecations, allowing legacy plugins to continue operation.

---

# 9. Feature Flags

Optional capabilities inside a plugin must be guarded by a feature flag resolved through the Platform SDK:

```python
from app.sdk.platform import platform

enabled = await platform.config.get_flag(tenant_id, "biometric_integration")
if enabled:
    # execute biometric sync
```

Feature flags are declared in `module.yaml` under `feature_flags` and managed through the Admin Portal per tenant.

---

# 10. Governance

- Every new plugin requires a **Plugin Review** before merging to `main`.
- Plugin manifests must pass automated schema validation in CI.
- Plugins may not access other plugins' internal services directly — only through Platform SDK or NATS events.
- Every plugin must have at least 80% test coverage of its service layer.
