# ADR-006 — Turborepo over Nx/Lerna

## Status
**Accepted** — In effect as of 2026-07-04

## Context
As we scale the DhruvaOS foundation monorepo (comprising client apps, mobile portals, backend microservices, and shared libraries), we require a build toolchain that minimizes compile times, handles execution caching, and is simple for developers to learn.

We evaluated three tools:
1. **Lerna**: Legacy monorepo manager. Slow build caching, configuration drift.
2. **Nx**: Rich plugin ecosystem, but highly opinionated and complex. Steep onboarding curve.
3. **Turborepo**: Zero-config caching, K8s/Docker-friendly build graphs, and extremely fast execution pipelines written in Go.

## Decision
We chose **Turborepo** because of its native pnpm workspace integration, zero-config task cache mechanism, and visual execution pipeline (defined in `turbo.json`). 

## Consequences
- **Build Speeds**: Local and CI build speeds reduced by up to 50% through caching of unchanged packages.
- **Onboarding**: Simple structure allows new developers to understand the project using simple workspace dependencies.
