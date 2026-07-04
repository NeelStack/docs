---
document_id: NES-501
title: Docker
subtitle: Enterprise Containerization, Multi-Stage Builds & Dockerfile Standards
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-500 Platform Engineering Standards
next_document: NES-502 Kubernetes
---

# NES-501 — Docker

> **"Secure, lightweight, and predictable containers form the basis of our runtime environment. We write optimized, multi-stage, rootless Dockerfiles."**

---

# Executive Summary

Containers represent our unified deployment unit. A poorly written container can contain critical security vulnerabilities, bloat image sizes (leading to slow deployments), and slow down application startup.

This standard establishes the mandatory guidelines for writing Dockerfiles, selecting base images, managing cache layers, and securing container execution environments.

---

# Purpose

This standard defines:

- Approved Base Images
- Multi-Stage Build Configurations
- Non-Root Execution Policies
- Layer Caching Optimization
- Container Security Hardening

---

# Approved Base Images

To prevent security vulnerabilities and reduce download footprints, we use slim, vetted base images:

| Runtime | Vetted Base Image | Rationale |
|---|---|---|
| Python | `python:3.13-slim` | Light footprint, includes system dependencies. |
| Node.js (Web/App) | `node:22-alpine` or `node:22-slim` | Ultra-lightweight Alpine or debian-slim variants. |
| Go | `golang:1.22-alpine` / `scratch` | Compilation container, scratch for final binary. |
| Static HTML / CDN | `nginx:alpine` | High-performance static asset server. |

---

# Multi-Stage Build Standard

All Dockerfiles must utilize multi-stage builds to isolate compilation dependencies (like compiler tools, git, headers, dev dependencies) from the final runtime image.

### Python Reference Dockerfile:

```dockerfile
# Stage 1: Build dependencies
FROM python:3.13-slim AS builder

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential

COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv && uv pip install --system --target /install -r pyproject.toml

# Stage 2: Final runtime
FROM python:3.13-slim

WORKDIR /app
COPY --from=builder /install /usr/local/lib/python3.13/site-packages
COPY . .

# Run as non-root
USER 10001
EXPOSE 8000
CMD ["python", "main.py"]
```

---

# Non-Root Execution Policy

Containers must **never** execute as the `root` user in production.

- **Risk**: Root execution in containers allows potential container breakout attacks to gain root shell control of the host node.
- **Rule**: Declare a non-root system user inside the Dockerfile using a user ID (UID) greater than `10000`. Ensure app files are owned by this user.

```dockerfile
# Create system group and user
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/sh -m appuser

WORKDIR /app
COPY --chown=appuser:appgroup . .

USER 10001
```

---

# Layer Caching Optimization

Order Dockerfile commands to maximize the Docker builder's layer caching mechanism.

- **Rule**: Place files that change least frequently (like package manifests, dependencies locks) first in the Dockerfile structure. Copy active source files last.
- **Wrong**:
  ```dockerfile
  COPY . .
  RUN pip install -r requirements.txt # Triggers re-install on EVERY code change
  ```
- **Correct**:
  ```dockerfile
  COPY pyproject.toml uv.lock ./
  RUN uv pip install -r pyproject.toml
  COPY src/ ./src/ # Changing code only invalidates this layer
  ```

---

# Container Security

Ensure container security compliance prior to deployment:

- **Secrets**: Never bake private keys, API secrets, or passwords into image layers. Use environment variables injected at runtime.
- **Vulnerability Scan**: All images must pass vulnerability scanner gates (e.g. Trivy) in the CI pipeline with zero CRITICAL or HIGH severity findings.
- **Minimize Installed Tools**: Do not install curl, wget, git, or compiler utilities in the final runtime container layer unless explicitly required.

---

# Anti-Patterns

❌ **Using `latest` Image Tags**: Specifying base images like `FROM node:latest`. Upstream updates can break builds unexpectedly. Always specify exact version numbers.

❌ **Running as Root**: Leaving the default root user active in the container build.

❌ **Massive Image Layers**: Copying temporary dev caches, node_modules, or documentation files. Always include a `.dockerignore` file matching your workspace layout.

---

# Production Checklist

- [ ] `.dockerignore` is present in the repository root.
- [ ] Multi-stage builds are active for all compiled runtimes.
- [ ] `USER` command is explicitly defined with non-root UID.
- [ ] Image version tags are locked (e.g. `node:22.2.0-alpine`).
- [ ] Trivy vulnerability scan passes with zero high/critical errors.

---

# Success Criteria

The Containerization standard is successful when:
- Average production image sizes remain below **150MB** for Python/Node runtimes (excluding database caches).
- Docker builds execute in less than 2 minutes on CI runners utilizing layer cache servers.
- Container security audits report zero active root execution nodes.

---

# Document Status

**Document:** NES-501 — Docker
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-502 — Kubernetes**
