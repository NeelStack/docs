---
document_id: NES-1207
title: E-commerce
subtitle: Enterprise E-commerce Platform Reference Architecture Blueprint
version: 1.0.0
status: Draft
classification: Internal
owner: Enterprise Platforms Board
review_cycle: Every 6 Months
document_type: Reference Architecture
parent_document: NES-1206 CMS
next_document: NES-1208 Analytics Platform
---

# NES-1207 — E-commerce

> **"Checkout checkout flows require transaction guarantees. This reference blueprint details our shopping cart caches, inventory locks, and payment gateway integrations."**

---

# Executive Summary

To operate a reliable E-commerce platform that handles shopping carts, catalog searches, order updates, payment processing, and stock levels, we must manage transactional safety.

This document establishes the official **NeelStack E-commerce Platform Reference Architecture** blueprint.

It defines our data schema structures, shopping cart session caches (Redis), payment gateways (Stripe), and inventory locking strategies.

---

# Purpose

This standard defines:

- Unified E-commerce Platform Reference Architecture Map
- Shopping Cart Session Caching (Redis)
- Inventory Locking and Race Condition Prevention
- Payment Gateway Integrations (Stripe)

---

# E-commerce Reference Architecture Map

The E-commerce Reference Architecture separates catalog queries, cart sessions, and payment checkouts:

```text
               Public Ingress (Client App Integrations, HTTPS)
                               │
                               ▼
        API Gateway (CORS and rate limiting integrations)
                               │
                               ▼
        Private EKS Compute VPC (Order Orchestrators)
         ├── Cart Manager Pods (Connects to Redis)
         └── Payment Processing Workers (Stripe hooks)
                               │
                               ▼
        Data Layer (RDS Postgres, Multi-AZ)
         ├── Stripe API (Handles card auth and charge processing)
         └── Redis Cache (Cart session states, 5ms lookup)
```

---

# Shopping Cart Session Caching

Optimize cart response times:

- **Cart Caches**: Store active shopping cart states inside **Redis** with a **14-day expiry**.
- **Database Write**: Sync cart contents to the primary PostgreSQL database only when the user transitions to the checkout phase or updates items.

---

# Inventory Locking Standards

To prevent duplicate stock sales during high-volume sales:

- **Pessimistic Locking**: Use database-level locking (`SELECT ... FOR UPDATE`) during the checkout phase to verify stock levels and lock inventory records before processing payments.
- **Auto Release**: Configure locks to expire and release inventory back to the catalog if the payment transaction is not completed within **10 minutes**.

```sql
-- PostgreSQL inventory check with pessimistic lock
SELECT stock_count FROM product_inventory 
WHERE product_id = :product_id 
FOR UPDATE;
```

---

# Payment Gateway Integrations (Stripe)

Ensure secure payment operations:

- **Tokenized Payments**: Process transactions using **Stripe hosted fields** or payment intents. Raw credit card details must never touch our application servers (PCI-DSS compliance).
- **Idempotency Keys**: Submit unique idempotency keys with every Stripe API request to prevent duplicate charges.

---

# Anti-Patterns

❌ **Storing Carts exclusively in Local Storage**: Relying solely on client browser local storage, which prevents cart sharing across devices.

❌ **Payment Processing without Idempotency Keys**: Submitting checkout transactions without tracking keys, allowing users to be charged twice if connections drop.

❌ **Exposing Raw Card Details**: Writing payment inputs to system log files.

---

# Production Checklist

- [ ] Stripe API connections utilize OIDC keys.
- [ ] Cart session caches use Redis.
- [ ] Inventory locks follow pessimistic transaction boundaries.
- [ ] PCI-DSS compliance audits pass cleanly.
- [ ] Ingress APIs have active rate limits.

---

# Success Criteria

The E-commerce Reference Architecture is successful when:
- Transactions process cleanly without duplicate card charges.
- Product inventory levels are locked and released automatically.
- Shopping cart actions respond under 100ms.

---

# Document Status

**Document:** NES-1207 — E-commerce
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1208 — Analytics Platform**
