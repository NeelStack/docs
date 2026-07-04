---
document_id: NES-512
title: Networking
subtitle: Enterprise VPC Topology, Subnet Segments & Traffic Control Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-511 CDN
next_document: NES-513 Service Mesh
---

# NES-512 — Networking

> **"Network boundaries isolate potential threats. We run our services inside private subnets, control traffic flow via VPC security groups, and enforce strict ingress paths."**

---

# Executive Summary

Flat network topologies where any resource can communicate with any other resource are insecure.

If a single web server is compromised, an attacker can pivot to private databases or internal services.

We mandate the isolation of resources using Virtual Private Clouds (VPCs) separated into strict network subnet segments.

This standard defines the IP addressing layouts, subnet configurations, routing policies, and security group rules for NeelStack cloud networks.

---

# Purpose

This standard defines:

- VPC IP Allocation and Layout
- Subnet Segments (Public, Private, Isolated)
- Ingress and Egress Routing Rules
- Security Groups and Network ACLs (NACLs)
- Secure VPC Peering and Endpoints

---

# VPC IP Allocation & Layout

To prevent routing conflicts during cross-region replication or VPN connections, VPC IP blocks must be planned and allocated centrally.

- **Primary VPC Block**: Use private Classless Inter-Domain Routing (CIDR) blocks from the RFC 1918 space (e.g. `10.0.0.0/16`).
- **No Overlapping CIDRs**: Dev, Staging, and Production VPCs must be assigned distinct CIDR ranges to support secure peering (e.g. Dev: `10.10.0.0/16`, Prod: `10.20.0.0/16`).

---

# Subnet Segmentation

Every VPC must be divided into three distinct subnet layers across multiple Availability Zones (AZs) for high availability:

```text
 ┌────────────────────────────────────────────────────────┐
 │  Public Subnet (ALBs, Nat Gateways, Edge Ingress)     │
 ├────────────────────────────────────────────────────────┤
 │  Private Subnet (EKS Nodes, Backend APIs, Workers)     │
 ├────────────────────────────────────────────────────────┤
 │  Isolated Subnet (RDS Databases, Redis Caches)         │
 └────────────────────────────────────────────────────────┘
```

- **Public Subnet**: Directly connected to the Internet Gateway. Only Load Balancers and NAT Gateways reside here.
- **Private Subnet**: No direct public access. Outbound connections to the internet (e.g. for package updates or API calls) pass through the public NAT Gateway.
- **Isolated Subnet**: No internet access. Completely blocked from routing to NAT Gateways. Reserved for databases and caches.

---

# Security Groups & Least Privilege

Security Groups act as virtual firewalls control traffic to individual resources:

- **Restrict Ingress**: Never open ports like `22` (SSH), `5432` (Postgres), or `6379` (Redis) to public CIDR ranges (`0.0.0.0/0`).
- **Chain Rules**: Configure security groups to allow ingress traffic only from specific source security groups rather than static IP blocks.
  - *Example*: The RDS PostgreSQL security group only accepts traffic from the EKS Node security group.

---

# VPC Endpoints (PrivateLink)

When accessing managed cloud services (e.g. S3, DynamoDB, Secrets Manager) from EKS Pods inside private subnets, do not route traffic over the public NAT Gateway.

- **Standard**: Configure VPC Gateway or Interface Endpoints (AWS PrivateLink).
- **Benefit**: Ensures traffic to AWS services remains entirely within the private AWS fiber backbone, reducing egress data charges and latency.

---

# Anti-Patterns

❌ **Placing Databases in Public Subnets**: Exposing RDS instances to public subnets, even if protected by passwords.

❌ **Overusing NAT Gateways for AWS Internal APIs**: Routing heavy container log uploads or secrets pulls to AWS endpoints over NAT gateways, driving up data billing costs.

❌ **Allow-All Security Rules**: Creating security groups with rules like `All Traffic` allowed from `0.0.0.0/0` to simplify setup.

---

# Production Checklist

- [ ] Subnets are divided across at least 3 Availability Zones.
- [ ] No database resides in a subnet with a route to an Internet Gateway.
- [ ] VPC Gateway Endpoints are configured for S3 and DynamoDB.
- [ ] NAT Gateways are mapped to static Elastic IPs in public subnets.
- [ ] Security groups restrict administrative ports (22, 3389) globally.

---

# Success Criteria

The Network configuration is successful when:
- Internal databases are unreachable from any external connection outside the VPC.
- Outbound traffic from private nodes is consolidated through NAT gateways for monitoring.
- VPC network latency metrics remain low during inter-service operations.

---

# Document Status

**Document:** NES-512 — Networking
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-513 — Service Mesh**
