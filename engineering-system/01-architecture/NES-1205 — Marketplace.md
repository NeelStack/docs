---
document_id: NES-1205
title: Marketplace
subtitle: Enterprise Digital Marketplace Platform Reference Architecture Blueprint
version: 1.0.0
status: Draft
classification: Internal
owner: Enterprise Platforms Board
review_cycle: Every 6 Months
document_type: Reference Architecture
parent_document: NES-1204 AI Platform
next_document: NES-1206 CMS
---

# NES-1205 — Marketplace

> **"Marketplace platforms connect sellers and buyers. This reference blueprint details our catalog distribution, payment routing, and transaction isolation structures."**

---

# Executive Summary

To operate a reliable digital marketplace platform (e.g. connecting educational content sellers with school buyers), we must manage catalog distribution, transactional safety, payment split integrations, and seller data isolation.

This document establishes the official **NeelStack Marketplace Platform Reference Architecture** blueprint.

It defines our data schema structures, payment gateways (Stripe Connect), catalog search indexes, and transaction isolation rules.

---

# Purpose

This standard defines:

- Unified Marketplace Platform Reference Architecture Map
- Seller and Buyer Data Isolation
- Payment Routing and Split Transactions (Stripe Connect)
- Product Catalog Search Optimization (OpenSearch)

---

# Marketplace Reference Architecture Map

The Marketplace Reference Architecture divides buyer and seller transaction layers:

```text
               Public Ingress (Marketplace Subdomain: market.neelstack.com)
                               │
                               ▼
        API Gateway (CORS and tenant-level access validations)
                               │
                               ▼
        Private EKS Compute VPC (Transaction Managers)
         ├── Catalog Search API (Connects to OpenSearch)
         └── Payment Processing Workers (Stripe hooks)
                               │
                               ▼
        Data Layer (RDS Postgres, Multi-AZ)
         ├── OpenSearch Database (Fast catalog name searches)
         └── Stripe API (Handles payout split calculations)
```

---

# Buyer & Seller Data Isolation

- **Isolation Strategy**: Group tables into distinct schemas (e.g., `buyers`, `sellers`, `transactions`).
- **Access Limits**: Compute pods managing checkout scripts must only query tables in their target schemas, protecting seller payouts from buyer account session access.

---

# Payment Routing & Split Transactions

- **Standard**: Integrate with **Stripe Connect** (Custom or Express models).
- **Mechanism**: On transaction checkouts, the payment engine processes charges from the buyer, calculates our marketplace platform fee, and routes the remainder to the seller's account.
- **Ledger Auditing**: Log all payment splits, processing fees, and chargebacks inside the immutable ledger (NES-1202).

---

# Catalog Search & Caching

Optimize catalog search speeds:

- **Search Index**: Stream product catalog updates to **OpenSearch** using Debezium CDC.
- **Autocomplete**: Autocomplete searches must return results in under **200ms**. Cache search metrics using Redis.

---

# Anti-Patterns

❌ **Direct Ledger Updates on Refunds**: Running SQL update commands on historical invoice records to handle returns, which violates accounting standards.

❌ **Exposing Payout Details**: Exposing seller bank routing details or payout metrics to buyer role sessions.

❌ **Manual Split Processing**: Processing payouts manually at the end of the month, which increases operational overhead and error rates.

---

# Production Checklist

- [ ] Stripe Connect webhook integrations are active.
- [ ] Catalog search index (OpenSearch) is running.
- [ ] Seller and buyer database access roles are isolated.
- [ ] Ingress APIs have active rate limits.
- [ ] Payment split audit logs are verified.

---

# Success Criteria

The Marketplace Reference Architecture is successful when:
- Transactions process and route payments to sellers automatically.
- Catalog searches return responsive results under 200ms.
- Financial audit logs capture all processing fees and payouts.

---

# Document Status

**Document:** NES-1205 — Marketplace
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1206 — CMS**
