---
document_id: NES-1409
title: Azure Architecture
subtitle: Enterprise Azure Infrastructure & Identity Blueprint
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Reference Implementation
parent_document: NES-1408 — AWS Architecture.md
next_document: NES-1410 — Event Flow Diagrams.md
---

# NES-1409 — Azure Architecture

> **"Identity and cloud networks must integrate. This reference blueprint details our Azure tenant structures, Entra ID alignments, and AKS cluster deployments."**

---

# Executive Summary

To operate a highly available, secure corporate infrastructure on Azure, we must enforce a structured cloud topology.

This document establishes the official **NeelStack Azure Infrastructure Architecture** blueprint.

It defines our subscription boundaries, Microsoft Entra ID (OIDC) sync models, Azure Kubernetes Service (AKS) setups, virtual networks, and database integrations.

---

# Purpose

This standard defines:

- Unified Azure Subscription and Virtual Network Map
- Microsoft Entra ID SSO Integration
- AKS Cluster Node Placements
- Azure Storage Account Configurations

---

# Azure Architecture Map

The Azure Architecture organizes resources into secure resource groups:

```text
  Azure Tenant (Enterprise Hub)
  ┌─────────────────────────────────────────────────────────────┐
  │  VNet Boundary (10.100.0.0/16)                              │
  │                                                             │
  │  Subnet: Ingress-Subnet (Azure App Gateway / WAF)           │
  │  ├── VM Zone A (10.100.1.0/24)                              │
  │  └── VM Zone B (10.100.2.0/24)                              │
  │                                                             │
  │  Subnet: AKS-Subnet (AKS compute nodes)                     │
  │  ├── Agent Nodes (10.100.10.0/24)                           │
  │  └── System Pods (10.100.20.0/24)                           │
  │                                                             │
  │  Subnet: Database-Subnet (Azure SQL Database, Redis)        │
  │  ├── Database endpoints (10.100.100.0/24)                   │
  │  └── Redis Cache instances (10.100.200.0/24)                │
  └─────────────────────────────────────────────────────────────┘
```

---

# Microsoft Entra ID SSO Integration

Manage identity federation on Azure:

- **SSO Mappings**: Configure Microsoft Entra ID (Azure AD) as the primary identity provider for the organization (NES-604).
- **Federated Identities**: Map corporate roles (e.g. `Developer`, `Operator`, `Finance`) directly to Entra ID security groups to authorize console access.

---

# AKS Cluster Node Placements

Secure compute nodes on AKS:

- **Private Cluster Mode**: Deploy AKS in **Private Cluster Mode**. The Kubernetes API server endpoint must resolve inside the private virtual network (VNet).
- **System & User Node Pools**: Separate node pools to ensure cluster stability:
  - *System Pool*: Executes core cluster controllers (kube-dns, ingress).
  - *User Pool*: Runs target application pods.

---

# Azure Storage Account Settings

- **Encryption**: Enforce Infrastructure Encryption (double encryption at rest using customer-managed keys in Key Vault).
- **Private Endpoints**: Access storage accounts exclusively via Private Endpoints inside the virtual network subnet.

---

# Anti-Patterns

❌ **Direct Public Storage Access**: Leaving Azure Storage Account public access options enabled, exposing media files.

❌ **Exposing AKS API Server**: Leaving AKS cluster public API points active without network IP whitelists.

❌ **Omitting Key Vault Encryption**: Storing application secrets in cleartext config files instead of resolving them dynamically using Azure Key Vault.

---

# Production Checklist

- [ ] VNet subnets conform to the Azure architecture blueprint.
- [ ] Entra ID OIDC configurations are active.
- [ ] AKS private cluster mode is enabled.
- [ ] Storage accounts use private endpoint routes.
- [ ] Key Vault configurations use customer-managed keys.

---

# Success Criteria

The Azure Infrastructure Architecture is successful when:
- AKS workloads scale automatically across target availability zones.
- Access permissions map directly to Entra ID security groups.
- Azure database storage comply with envelope encryption standards.

---

# Document Status

**Document:** NES-1409 — Azure Architecture
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1410 — Event Flow Diagrams.md**
