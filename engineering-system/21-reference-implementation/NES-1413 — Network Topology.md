---
document_id: NES-1413
title: Network Topology
subtitle: Enterprise Network Topology & VPC Segmentation Blueprint
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Reference Implementation
parent_document: NES-1412 — MCP Communication Diagrams.md
next_document: NES-1414 — Security Trust Boundaries.md
---

# NES-1413 — Network Topology

> **"Infrastructure security starts with network borders. We diagram our VPC configurations, subnet splits, NAT Gateways, and ALB routings using Network Topology maps."**

---

# Executive Summary

To operate a highly available, secure SaaS platform across cloud regions, we must enforce a structured network topology.

This document establishes the official **NeelStack Network Topology** blueprint.

It defines our VPC configuration, public/private subnet segmentation, NAT Gateway placements, Application Load Balancers (ALB) ingress routes, and security group boundaries.

---

# Purpose

This standard defines:

- Unified Network VPC and Subnet Topology Map
- Public, Private, and Database Isolated Subnet Routing
- Gateway Ingress and Cloudflare Edge Proxying
- Security Group Rules and Traffic Direction Constraints

---

# Network Topology Map

The Network Topology organizes compute and database resources across isolated network segments:

```text
  Edge Gateway (Cloudflare WAF / Orange Cloud proxy active)
                           │
                           ▼ (Ingress Traffic via Port 443 / HTTPS)
  AWS VPC Boundary (10.10.0.0/16)
  ┌─────────────────────────────────────────────────────────────┐
  │  Public Subnets (NAT Gateway, ALB Ingress)                  │
  │  ├── Subnet Zone A (10.10.1.0/24)                           │
  │  └── Subnet Zone B (10.10.2.0/24)                           │
  │                                                             │
  │  Private Subnets (EKS Compute Nodes, App Pods)              │
  │  ├── Subnet Zone A (10.10.10.0/24)                          │
  │  └── Subnet Zone B (10.10.20.0/24)                          │
  │                                                             │
  │  Database Isolated Subnets (RDS instances, Redis cache)     │
  │  ├── Subnet Zone A (10.10.100.0/24)                         │
  │  └── Subnet Zone B (10.10.200.0/24)                         │
  └─────────────────────────────────────────────────────────────┘
```

---

# Subnet Routing & Security Rules

Enforce strict isolation across network boundaries:

- **Public Subnet Routing**: Host ALBs and NAT Gateways. Route inbound traffic from edge proxies to target Private Subnet ports. Direct compute host deployment is prohibited.
- **Private Subnet Routing**: Host compute instances (EKS nodes). Pods route outbound queries to the public internet exclusively via NAT Gateways in public subnets.
- **Database Isolated Subnet Routing**: Host RDS Postgres instances. Route tables must block routes to internet gateways or NAT hosts.

---

# Ingress Traffic & Cloudflare Proxying

- **Edge Proxying**: Inbound client traffic must pass through Cloudflare proxies (Orange Cloud active) before hitting ALBs.
- **WAF Enforcement**: Configure Cloudflare Web Application Firewall (WAF) rules to filter malicious payloads, SQL injections, and DDoS spikes at the network edge.

---

# Anti-Patterns

❌ **Direct Internet Routing to DBs**: Assigning databases public IP addresses, bypassing Private Subnet isolations.

❌ **Shared Dev-Prod Networks**: Bridging developer test subnets directly to production database environments.

❌ **Over-Permissive Security Groups**: Allowing wildcard security groups (`0.0.0.0/0`) ingress rights to database ports.

---

# Production Checklist

- [ ] Subnets conform to the Network Topology map.
- [ ] NAT Gateways are provisioned in public subnets.
- [ ] Database subnets lack routes to internet gateways.
- [ ] Cloudflare edge WAF rules are active.
- [ ] Security group rules restrict lateral port routing.

---

# Success Criteria

The Network Topology implementation is successful when:
- Internal databases are completely isolated from direct public routing.
- Inbound client queries are verified at the edge before hitting ALB ports.
- Infrastructure provisioning scripts (Terraform) match target subnets.

---

# Document Status

**Document:** NES-1413 — Network Topology
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1414 — Security Trust Boundaries.md**
