---
document_id: NES-P-104
title: Infrastructure & Deployment Standards
version: 1.0.0
status: Approved
owner: Platform Operations Team
---

# NES-P-104 — Infrastructure & Deployment Standards

> **"The application architecture remains constant; only the deployment topology scales to match tenant volume and SLA tiers."**

---

# 1. Purpose

This document outlines the **standard infrastructure progression, environment profiles, and scaling pathways** for DhruvaOS. It guarantees that the system remains cloud-agnostic, low-cost at boot, and easily migratable to high-availability cluster setups.

---

# 2. Environment Delivery Pipeline

DhruvaOS standardizes a structured delivery pipeline composed of five environments, ensuring seamless migration from local code iteration to global SaaS scale:

```text
  ┌──────────────┐
  │    Local     │  Developer laptop environment utilizing local containers.
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │ Development  │  Clustered shared target for automated daily team builds.
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │   Testing    │  Isolated regression workspace for QA snapshot validations.
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │     UAT      │  User Acceptance Testing mimicking real production load.
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │  Production  │  High-availability SLA target running live tenant workloads.
  └──────────────┘
```

### 2.1 Configuration Isolation & Profiles
- **Local / Dev**: Configured using environment defaults or local `.env` files pointing to local hostnames. Runs via:
  ```bash
  docker compose -f infrastructure/docker/docker-compose.dev.yml --profile dev up
  ```
- **Testing / UAT / Prod**: Configured using production-grade orchestration config maps or secure container injection variables. Never uses hardcoded defaults.

### 2.2 Infrastructure Mapping
| Capability | Dev Environment | Prod Environment |
| --- | --- | --- |
| **Database** | Single Docker PG instance with pgvector | Clustered Managed DB (Aurora PG / Azure SQL) with read replicas |
| **Object Storage** | Local MinIO storage container | AWS S3 / Google Cloud Storage with CDN caching |
| **SSO / Identity** | Local Zitadel Docker container | Clustered Enterprise Zitadel Identity Provider |
| **Message Broker** | Single-node local NATS JetStream container | Clustered, high-availability NATS JetStream nodes |
### 2.3 Environment Flexibility & Extension (e.g., adding Staging / UAT)
The architecture is designed to be environment-agnostic. While only two primary environments (`dev` and `prod`) are operated by default, adding a third or fourth environment (e.g., `staging`, `testing`, `uat`) requires **zero application code changes**:
1. **Pydantic Configs**: Application settings are completely defined via environment variables.
2. **Infrastructure Binding**: A new environment is created simply by instantiating new instances of the backing services (Database, NATS, Zitadel) and injecting their URLs/credentials as configurations into the container runtime.
3. **No Branching**: Avoid branching the code repository for different environments; control all runtime differences using environment variables.

---

# 3. Deployment Evolution Path

The progression of DhruvaOS deployment topologies grows in phases with tenant requirements:

```text
  ┌──────────────┐
  │    Laptop    │  Local dev environment using native runtimes.
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │Docker Compose│  Isolated multi-container developer footprint.
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │  Single VPS  │  Single virtual instance hosting compose layers.
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │ Multiple VPS │  Divided compute, DB cluster, and NATS queue.
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │  Kubernetes  │  Enterprise orchestrator for multi-tenant SaaS.
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │ Multi-Region │  Any-cast global edge routing with replication.
  └──────────────┘
```

---

# 3. Environment Profiles & Configurations

DhruvaOS standardizes six infrastructure configurations, mapped via Docker Compose profiles and Kubernetes Helm charts:

### 3.1 Development Profile (`dev`)
- **Compute footprint**: Laptop / local virtual machine (0 cost).
- **Core services**: Postgres, Redis, NATS, MinIO, Zitadel, Core, AI.
- **Goal**: Rapid hot-reload local iteration.

### 3.2 Single VPS Profile (`vps`)
- **Compute footprint**: Single 4 vCPU / 8GB RAM virtual server ($20-$40/month).
- **Setup**: Docker Compose using systemd watchdogs and Traefik reverse proxies mapping ports `80`/`443`.
- **Target**: Small-scale pilot testing.

### 3.3 SaaS Profile (`saas`)
- **Compute footprint**: Shared cloud virtual compute instances.
- **Setup**: Exposes monitoring logs (`loki`), event triggers (`n8n`), metrics (`prometheus`), and visualization (`grafana`).
- **Target**: Multi-tenant subscription services.

### 3.4 Dedicated Cloud Profile (`dedicated`)
- **Compute footprint**: Dedicated, isolated tenant instances.
- **Setup**: Automated Terraform deployment spinning up single-tenant instances under custom domains.
- **Target**: Enterprise-level school chains.

### 3.5 Self-Hosted Profile (`selfhosted`)
- **Compute footprint**: Customer on-premise hardware.
- **Setup**: Docker Compose package bundled with offline Zitadel configurations.
- **Target**: High-security institutions without open web access.

### 3.6 Kubernetes Profile (`k8s`)
- **Compute footprint**: Cloud-managed or self-hosted Kubernetes clusters.
- **Setup**: Helm charts deploying pods with automated horizontal autoscalers (HPA) and cert-manager routing.
- **Target**: Large-scale production deployments.

---

# 4. Database Strategy & Isolation Triggers

Instead of linking data isolation strictly to the number of tenants, DhruvaOS maps its database topology dynamically based on business requirements, security SLAs, and compliance triggers:

| Business / Compliance Trigger | Data Isolation Strategy | Expected Infrastructure Topology |
| --- | --- | --- |
| **Standard SaaS Tiers** | **Schema-per-tenant** | Shared PostgreSQL instance; dynamic `search_path` middleware isolation. |
| **Data Compliance SLAs** | **Database-per-tenant** | Dedicated logical databases on shared or dedicated Postgres clusters. |
| **Enterprise SLA & Performance** | **Dedicated Cluster** | Completely isolated compute, memory, and database servers. |
| **Sovereign Cloud & Residency** | **Regional Deployment** | Region-locked Kubernetes clusters and regional PostgreSQL replicates. |

---

# 5. Infrastructure Code Guidelines

1. **Infrastructure as Code (IaC)**: All physical resources must be provisioned via Terraform modules located in `/infrastructure/terraform/`.
2. **Secrets Security**: No secrets may be hardcoded. Production workloads must inject secrets via Kubernetes Secrets, HashiCorp Vault, or AWS Secrets Manager.
3. **Storage Rules**: Persisted files (e.g., student documents, system backups) must use S3/MinIO APIs. Directly writing files to container local volumes is forbidden.
