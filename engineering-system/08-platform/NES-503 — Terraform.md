---
document_id: NES-503
title: Terraform
subtitle: Enterprise Infrastructure as Code, State Management & Module Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-502 Kubernetes
next_document: NES-504 GitHub Actions
---

# NES-503 — Terraform

> **"Infrastructure must be versioned, reviewed, and declared. We write modular, formatted, and linted Terraform code with remote state locking."**

---

# Executive Summary

Manual cloud infrastructure modification ("ClickOps") results in untracked configurations, drift, security gaps, and unrepeatable deployments.

We mandate **Terraform** as the standard tool for provisioning cloud infrastructure.

This document defines the layout rules, state locking mechanisms, module boundaries, and formatting gates for writing Terraform code at NeelStack.

---

# Purpose

This standard defines:

- Directory Layout Blueprint
- Remote State Management and Locking
- Module Development Standards
- Secrets Handling inside IaC
- Formatting, Linting, and Compliance Gates

---

# Directory Layout Blueprint

To keep cloud infrastructure modules isolated and prevent single-file blast radius failures:

```text
terraform/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── backend.tf
│   ├── staging/
│   └── prod/
│
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── eks/
│   └── database/
```

- **Environments Directory**: Separates Dev, Staging, and Prod configurations. No environment can import resources directly from another environment's tfstate file without explicit data interfaces.

---

# Remote State & Locking

We prohibit local state files (`terraform.tfstate`) for any production or shared environments.

- **Standard**: Remote state files must be stored in secure, versioned, and encrypted object storage (e.g. AWS S3) with Server-Side Encryption (SSE) active.
- **State Locking**: Enforce state locking using a distributed database (e.g. DynamoDB) to prevent concurrent executions from corrupting the state file.

```hcl
terraform {
  backend "s3" {
    bucket         = "neelstack-terraform-state"
    key            = "environments/prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "neelstack-terraform-locks"
    encrypt        = true
  }
}
```

---

# Module Standards

To prevent code duplication, build reusable modules for common infrastructure stacks:

- **Version Pinning**: Always pin module versions in environment files.
- **No Hardcoded Values**: Modules must receive values via `variables.tf` and expose resources via `outputs.tf`.
- **Resource Naming**: Use standard tags (e.g. `Environment`, `Owner`, `Project`) for all provisioned resources:

```hcl
module "vpc" {
  source = "../../modules/vpc"

  cidr_block      = "10.0.0.0/16"
  environment     = "prod"
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]

  tags = {
    Environment = "production"
    Owner       = "PlatformTeam"
    Project     = "NeelStackPortal"
  }
}
```

---

# Secrets Management in Terraform

Never hardcode database passwords, API tokens, or SSL certificates inside Terraform configurations.

- **Environment Vars**: Use environment variables prefixed with `TF_VAR_` to pass sensitive configuration parameters during execution.
- **Dynamic Secrets**: Retrieve active secrets from a secure configuration manager (like AWS Secrets Manager or HashiCorp Vault) dynamically during compilation:

```hcl
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "prod/database/password"
}

resource "aws_db_instance" "postgres" {
  # ... other configurations
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
}
```

---

# Formatting, Linting & Compliance

Automate Terraform quality checks inside the CI/CD pipeline:

- **Format**: All files must pass formatting check: `terraform fmt -check`.
- **Lint**: Run `tflint` to catch provider configuration issues.
- **Security Scans**: Run security scans (e.g., `tfsec` or `checkov`) to detect open ports, unencrypted storage, or over-privileged IAM settings.

---

# Anti-Patterns

❌ **Storing Secrets in Terraform Variables**: Hardcoding values like `default = "SuperSecretPassword123"` inside `variables.tf` files and committing them to Git.

❌ **Monolithic States**: Provisioning VPCs, EKS clusters, RDS databases, and individual application resources inside a single configuration directory. This creates large dependency graphs and high risk during updates.

❌ **ClickOps Modifications**: Manually editing resources in the cloud console (e.g., adding an IP to a security group) and leaving the Terraform state out of sync.

---

# Production Checklist

- [ ] Remote state backend with DynamoDB locking is initialized.
- [ ] Version constraints are set for Terraform and all providers.
- [ ] Security scan passes with zero critical/high issues.
- [ ] Resource tagging policy is enforced.
- [ ] `terraform plan` is reviewed and logged prior to application.

---

# Success Criteria

The IaC standard is successful when:
- Cloud environments can be torn down and rebuilt completely from configuration files.
- The `terraform plan` output matches the changes applied to the cloud infrastructure (zero manual config drift).
- CI/CD checks automatically block configuration errors before deployment changes are made.

---

# Document Status

**Document:** NES-503 — Terraform
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-504 — GitHub Actions**
