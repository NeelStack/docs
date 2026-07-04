---
document_id: TECH-010
title: Docker Standard
subtitle: Docker is the container standard for all NeelStack services
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Technology Standard
parent_document: TECH-009 AWS
next_document: TECH-011 Kubernetes
---

# TECH-010 — Docker Standard

---

## Approved Version

**Docker Engine 25+** with **BuildKit** enabled.

## Base Image Policy

| Service Type | Approved Base Image |
|---|---|
| Python backend | `python:3.12-slim-bookworm` |
| Node.js frontend | `node:22-alpine` |
| Nginx proxy | `nginx:1.27-alpine` |

**Never use**: `latest` tag, `ubuntu:latest`, full OS images for production services.

## Required Dockerfile Practices

```dockerfile
# ✅ Multi-stage build (reduces image size)
FROM python:3.12-slim-bookworm AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim-bookworm AS runtime
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY . .

# Run as non-root user (security requirement)
RUN addgroup --system app && adduser --system --group app
USER app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Security Requirements

- Non-root user inside container (LAW-007)
- No secrets in Docker image layers
- `.dockerignore` excludes `.env`, `*.md`, `tests/`, `.git/`
- Image vulnerability scan in CI (`trivy scan`)
- Images signed and pushed to private ECR only

## Related Standards

- NES-501 — Docker
- NES-515 — Infrastructure Security
- TECH-001 — Technology Stack

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-07-04 | Initial publication |
