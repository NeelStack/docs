---
document_id: NES-P-102
title: Platform SDK Specification
version: 1.0.0
status: Approved
owner: Platform Architecture Team
---

# NES-P-102 — Platform SDK Specification

> **"Domain plugins should never know what storage engine, message broker, or SMS provider is running underneath. The Platform SDK is the only interface they ever need."**

---

# 1. Purpose

This document defines the **official specification for the DhruvaOS Platform SDK** (`services/core/src/app/sdk/platform.py`). It describes every namespace, its contract, and the rules governing how domain plugins interact with infrastructure.

---

# 2. Design Principles

1. **Infrastructure independence**: Domain code never imports low-level drivers (nats, minio, redis, twilio).
2. **Single import**: Every plugin imports only `from app.sdk.platform import platform`.
3. **Async-first**: All SDK methods are `async`.
4. **Tenant-aware**: Methods that touch persistent state accept `tenant_id`.
5. **Replaceable**: Each SDK class can be swapped for a different backend implementation without changing domain code.

---

# 3. Full SDK Namespace Reference

```text
platform
├── auth          → Zitadel OIDC / SSO
├── events        → NATS JetStream event bus
├── storage       → MinIO / S3 object storage
├── audit         → Loki structured audit trail
├── notifications → Push / In-App / Email / SMS
├── search        → Full-text & vector search
├── ai            → AI Gateway (chat, embed, summarise)
├── cache         → Redis key-value store
├── queue         → Arq background jobs
├── config        → Feature flags & tenant settings
├── files         → High-level document management
├── mail          → Transactional email relay
├── sms           → SMS routing
├── payments      → Razorpay / Stripe orders
└── scheduler     → Cron and recurring jobs scheduling
```

---

# 4. Namespace Contracts

## 4.1 `platform.auth`

| Method | Signature | Description |
| --- | --- | --- |
| `introspect_token` | `(token: str) → Dict` | Validates bearer token against OIDC provider |
| `create_user` | `(email, name, tenant_id) → Dict` | Provisions user in tenant organization |

## 4.2 `platform.events`

| Method | Signature | Description |
| --- | --- | --- |
| `publish` | `(event_name, payload, version="v1") → None` | Publishes versioned event to NATS |
| `subscribe` | `(event_name, handler, version="v1") → None` | Registers async handler for event stream |

Event topics follow the format: `dhruvaos.<event_name>.<version>`

## 4.3 `platform.storage`

| Method | Signature | Description |
| --- | --- | --- |
| `upload` | `(bucket, object_name, data, content_type) → str` | Uploads bytes; returns object URL |
| `download` | `(bucket, object_name) → bytes` | Downloads object bytes |
| `delete` | `(bucket, object_name) → None` | Removes object from bucket |

## 4.4 `platform.audit`

| Method | Signature | Description |
| --- | --- | --- |
| `log_action` | `(user_id, action, details, tenant_id) → None` | Emits structured audit trace |

## 4.5 `platform.notifications`

| Method | Signature | Description |
| --- | --- | --- |
| `send_push` | `(user_id, title, body, data?) → None` | Mobile push notification |
| `send_in_app` | `(user_id, message, link?) → None` | In-app notification |
| `send_email` | `(to, subject, html_body) → None` | Transactional email |
| `send_sms` | `(phone, message) → None` | SMS |

## 4.6 `platform.search`

| Method | Signature | Description |
| --- | --- | --- |
| `index` | `(index_name, document_id, document) → None` | Adds/updates document in search index (e.g. Postgres FTS / OpenSearch) |
| `query` | `(index_name, query_text, filters?) → List[Dict]` | Full-text search query over abstract search provider |

## 4.7 `platform.ai`

| Method | Signature | Description |
| --- | --- | --- |
| `chat` | `(session_id, user_message, tenant_id) → str` | Chat completion |
| `summarise` | `(text, max_tokens?) → str` | Text summarisation |
| `embed` | `(text) → List[float]` | Vector embedding |

## 4.8 `platform.cache`

| Method | Signature | Description |
| --- | --- | --- |
| `get` | `(key) → Any \| None` | Redis GET |
| `set` | `(key, value, ttl=3600) → None` | Redis SET with TTL |
| `delete` | `(key) → None` | Redis DEL |

## 4.9 `platform.queue`

| Method | Signature | Description |
| --- | --- | --- |
| `enqueue` | `(task_name, *args, **kwargs) → str` | Enqueues Arq background job; returns job ID |

## 4.10 `platform.config`

| Method | Signature | Description |
| --- | --- | --- |
| `get_flag` | `(tenant_id, flag, default=False) → bool` | Resolves feature flag for tenant |
| `get_setting` | `(tenant_id, key, default=None) → Any` | Resolves tenant runtime setting |

## 4.11 `platform.files`

| Method | Signature | Description |
| --- | --- | --- |
| `upload_document` | `(tenant_id, category, filename, data) → Dict` | Uploads document; returns metadata + URL |

## 4.12 `platform.mail`

| Method | Signature | Description |
| --- | --- | --- |
| `send` | `(to, subject, template, variables) → None` | Sends transactional email via SMTP relay |

## 4.13 `platform.sms`

| Method | Signature | Description |
| --- | --- | --- |
| `send` | `(phone, message) → None` | Routes SMS via MSG91 / Twilio |

## 4.14 `platform.payments`

| Method | Signature | Description |
| --- | --- | --- |
| `create_order` | `(tenant_id, amount_paise, currency="INR") → Dict` | Creates Razorpay/Stripe order |
| `verify_signature` | `(order_id, payment_id, signature) → bool` | Verifies webhook signature |

## 4.15 `platform.scheduler`

| Method | Signature | Description |
| --- | --- | --- |
| `schedule_cron` | `(task_name, cron_expression, *args, **kwargs) → str` | Schedules cron tasks; returns job ID |
| `schedule_delayed` | `(task_name, delay_seconds, *args, **kwargs) → str` | Schedules delayed tasks; returns job ID |
| `cancel_job` | `(job_id) → None` | Cancels a scheduled recurring job |

---

# 5. Usage Pattern

```python
from app.sdk.platform import platform

# ✅ Event publishing
await platform.events.publish("attendance.marked", {"student_id": "abc123", "status": "Present"})

# ✅ Caching
cached = await platform.cache.get(f"student:{student_id}")
if not cached:
    student = await db.fetch_student(student_id)
    await platform.cache.set(f"student:{student_id}", student, ttl=600)

# ✅ Notifications
await platform.notifications.send_sms("+919876543210", "Your ward is absent today.")

# ✅ File upload
result = await platform.files.upload_document(tenant_id, "report_cards", "John_Q1.pdf", pdf_bytes)
```

---

# 6. Adding a New SDK Namespace

1. Create the implementation class in `platform.py` with `async` methods.
2. Add it as a class attribute on `PlatformSDK`.
3. Update the global `platform` singleton.
4. Update this document with the namespace reference.
5. No domain code changes required — just start using `platform.<namespace>`.
