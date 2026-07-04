---
document_id: TECH-012
title: Terraform Standard
subtitle: Terraform is the Infrastructure as Code tool for all NeelStack cloud infrastructure
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Technology Standard
parent_document: TECH-011 Kubernetes
next_document: TECH-013 AI Stack
---

# TECH-012 — Terraform Standard

---

## Approved Version

**Terraform 1.7+** (OpenTofu is an approved alternative).

## Module Structure

```
infrastructure/
├── modules/
│   ├── eks/          # Kubernetes cluster
│   ├── rds/          # PostgreSQL
│   ├── elasticache/  # Redis
│   ├── s3/           # Object storage
│   └── vpc/          # Network
├── environments/
│   ├── production/
│   ├── staging/
│   └── development/
└── global/           # Route53, IAM, etc.
```

## Required Practices

- All infrastructure changes applied via **CI/CD pipeline** (never `terraform apply` locally in production)
- State stored in **S3 + DynamoDB lock table**
- Workspaces used to separate environments
- `terraform plan` output reviewed before `apply`
- Module versions pinned exactly

## Tagging Module

Every module must call the `tags` module to apply standard tags automatically:

```hcl
module "tags" {
  source      = "../../modules/tags"
  environment = var.environment
  product     = var.product
  team        = var.team
}
```

## Related Standards

- NES-503 — Terraform
- NES-505 — GitOps
- TECH-009 — AWS
- TECH-001 — Technology Stack

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-07-04 | Initial publication |
