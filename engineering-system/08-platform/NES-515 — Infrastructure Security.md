---
document_id: NES-515
title: Infrastructure Security
subtitle: Enterprise Host Hardening, Vulnerability Scanning & Compliance Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Security Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-514 Secrets
next_document: NES-516 Monitoring
---

# NES-515 — Infrastructure Security

> **"Security is built in depth. We harden virtual hosts, scan containers, and audit host activity continuously."**

---

# Executive Summary

Cloud infrastructure security cannot rely solely on firewalls or access controls.

If an attacker breaches a public container, the underlying host operating system, virtualization layer, and neighboring containers must remain protected.

We enforce a defense-in-depth model across all virtual hosts, compute clusters, and runtime containers.

This standard establishes our host hardening guidelines, vulnerability scanning thresholds, host monitoring, and security compliance baselines.

---

# Purpose

This standard defines:

- Host OS Hardening Rules
- Container Vulnerability Scanning (Trivy / Grype)
- Runtime Threat Detection (Falco)
- CIS Benchmark Compliance
- Network Trust Boundaries and Access Segments

---

# Host OS Hardening

All virtual machine nodes (EC2 instances, Kubernetes worker nodes) must run on verified, minimal operating system configurations.

- **Vetted OS**: Standardize on **Bottlerocket OS** or **Amazon Linux 2 (Minimal)** for EKS nodes.
- **Bottlerocket Advantages**: Has no package manager, no SSH shell by default, and a read-only root file system, which eliminates major vectors of host compromise.
- **Kernel Tuning**: Disable unused kernel modules (e.g. firewire, USB storage, legacy protocols) and restrict access to the kernel log buffer (`kernel.dmesg_restrict = 1`).

---

# Vulnerability Scanning (Trivy)

Every container image and IaC module must pass vulnerability audits before reaching staging or production.

- **Container Scan**: Run **Trivy** against final container builds.
- **Blocking Rules**:
  - Zero **CRITICAL** severity vulnerabilities allowed.
  - Zero **HIGH** severity vulnerabilities without active remediation plans allowed.
- **IaC Scan**: Run **tfsec** or **checkov** on Terraform modules to prevent configuration errors.

---

# Runtime Threat Detection (Falco)

Secure the runtime environment by monitoring active system calls inside the host node kernel.

- **Tooling**: Deploy **Falco** as a daemonset across all Kubernetes clusters.
- **Alert Rules**: Configure Falco rules to alert on suspicious activity, including:
  - Spawned shell inside a production container.
  - Unexpected write operations in system folders (like `/bin` or `/sbin`).
  - Access to sensitive files (like `/etc/shadow` or `/var/run/secrets/`).

```yaml
# Sample Falco alert rule
- rule: Shell in Container
  desc: A shell was spawned inside a container in production
  condition: container.id != host and proc.name = sh and evt.type = execve
  output: "Shell spawned in container (user=%user.name container=%container.id proc=%proc.name)"
  priority: WARNING
```

---

# CIS Benchmarks Compliance

All cloud environments must be evaluated against the Center for Internet Security (CIS) Benchmarks:

- **EKS CIS Benchmark**: Run **Kube-bench** monthly to check cluster node configurations against CIS targets.
- **AWS CIS Foundation**: Run monthly audits using AWS Security Hub to check AWS IAM, logging, and VPC settings.
- **Target**: Maintain a compliance score exceeding **95%** across all cloud environments.

---

# Anti-Patterns

❌ **Running Debug Shells in Production**: Leaving active SSH keys or console utilities running on host nodes. Use session managers (like AWS SSM Session Manager) with identity logging instead.

❌ **Ignoring Deprecated Base Images**: Running container stacks on old base images (e.g., Node 16) that contain unpatched CVEs, exposing the runtime environment to exploits.

❌ **Running Containers with `--privileged` Flag**: Deploying containers with administrative capabilities, which bypasses container isolation boundaries entirely.

---

# Production Checklist

- [ ] Host nodes run Bottlerocket OS or minimal hardened configurations.
- [ ] Container images have passed Trivy scans with zero critical errors.
- [ ] Falco is active and routing alert logs to PagerDuty.
- [ ] Automated CIS Compliance checks run monthly.
- [ ] Privileged containers are blocked by OPA Gatekeeper policy rules.

---

# Success Criteria

The Infrastructure Security program is successful when:
- Vulnerabilities are identified and patched in CI/CD before reaching deployment.
- Intrusions or unauthorized file changes trigger automatic alerts in less than 5 seconds.
- EKS clusters maintain 100% compliance with CIS benchmark profiles.

---

# Document Status

**Document:** NES-515 — Infrastructure Security
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-516 — Platform Observability & Monitoring**
