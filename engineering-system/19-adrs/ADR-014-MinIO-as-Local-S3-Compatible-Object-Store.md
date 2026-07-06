# ADR-014 — MinIO as Local S3-Compatible Object Store

## Status
**Accepted** — In effect as of 2026-07-06

## Context
DhruvaOS plugins store user-generated files (admission forms, student photos, report PDFs). To keep the code cloud-agnostic, we require an object storage interface that works identically in local development and production.

We evaluated:
1. **Local Filesystem Storage**: Writes files directly to local disks. Simple, but breaks when scaling to multiple app nodes or serverless containers.
2. **MinIO**: High-performance, self-hosted, S3-compatible object storage. It runs as a lightweight Docker container locally and exposes standard S3 APIs.
3. **AWS S3 Direct**: Excellent for production, but incurs cost and requires active credentials during local development, breaking offline capabilities.

## Decision
We chose **MinIO** for local development and self-hosted environments, configured to use standard S3 APIs. In cloud production environments, the application connects to managed cloud services (e.g., AWS S3) without any changes to the code.

## Consequences
- **Local Dev**: Fully functional offline document uploading.
- **Portability**: Code uses S3 protocols globally. Switching to S3, Google Cloud Storage, or Backblaze in production is purely a configuration variable change.
