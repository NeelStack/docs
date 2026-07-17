# Changelog

All notable changes to the NeelStack documentation repository are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [2.2.0] — 2026-07-18

### Added
- Created `catalogues.py` specifying dynamic industry configurations for `education` and `pharma` modules.
- Created `pharma` core database models and scaffolding configurations under `app.platform.models` and `app.modules.pharma`.
- Documented multi-industry catalogues onboarding and dynamic seeder structures inside `NES-P-108` and product architecture guides.

### Changed
- Updated system architecture to run as a multi-industry SaaS operating platform.
- Refactored tenant models, routes, and provisioning dependencies to decouple from hardcoded Education-specific schemas (e.g. RLS verification on `tenant` table instead of `student`).

## [2.1.0] — 2026-07-06

### Changed
- Updated system architecture and PRD documentation to reflect the removal of legacy Node.js/Express `sockets` and `jobs` services.
- Updated `NES-101-System-Architecture.md`, `NES-111-Multi-Tenant-Deployment-Strategy.md`, `NES-112-Module-and-Feature-Configuration-System.md`, `pricing-strategy.md`, and `PRD-002-Parent-Portal.md` to reference native FastAPI WebSockets and Scheduler instead of Socket.io and Node.js-based services.

### Added
- Created `NES-231 — AI Development Guide.md` under `09-ai/` specifying backend AI microservice architectures, directory layout trees, orchestrator intent routing rules, custom module creation, and pgvector database integrations.

## [2.0.0] — 2026-07-04

### Added — Phase 15 (Diagrams & Reference Implementations)
- NES-1400 to NES-1419: 20 Mermaid diagram standards (C4 L1-L4, UML, deployment, network, CI/CD, ERDs, domain maps)

### Added — Phase 14 (Starter Kits & Templates)
- NES-1300 to NES-1309: 10 Starter Kit templates (SaaS, AI, ERP, CRM, Healthcare, Mobile, Admin, Design System, Microservice, Event-Driven)

### Added — Phase 13 (Enterprise Reference Architectures)
- NES-1200 to NES-1210: 11 Enterprise Architecture blueprints (SaaS, Healthcare, ERP, CRM, AI Platform, Marketplace, CMS, E-commerce, Analytics, Events, Enterprise Blueprint)

### Added — Phase 12 (Platform Governance)
- NES-1100 to NES-1107: Platform Governance standards (Enterprise Governance, Tech Debt, Engineering Metrics, ARB, Capability Maturity, Internal Certifications, Career Ladder, Platform Roadmap)

### Added — Phase 11 (Product Engineering)
- NES-1000 to NES-1008: Product Engineering standards (Discovery, Roadmaps, Feature Lifecycle, Experimentation, A/B Testing, Product Analytics, UX Research, Design Review, Product Governance)

### Added — Phase 10 (Operations & Release Management)
- NES-900 to NES-911: Operations standards (Release Management, SemVer, Changelogs, Feature Flags, Blue-Green, Canary, Rollback, SLA/SLO, Runbooks, Post-Mortems, Chaos Engineering, Reference Architecture)

### Added — Phase 9 (Quality Assurance)
- NES-800 to NES-812: QA standards (QA Principles, Test Strategy, Unit, Integration, E2E, Performance, Load, Security, Manual, UAT, Bug Tracking, Test Automation, Reference Architecture)

### Added — Phase 8 (Data Platform)
- NES-700 to NES-712: Data Platform standards (Data Platform, Warehousing, ETL, ELT, Lakehouse, Analytics, BI, ML Pipelines, Feature Store, Data Governance, Data Security, Lineage, Reference Architecture)

### Added — Phase 7 (Security & Compliance)
- NES-600 to NES-616: Security standards (Secure SDLC, OWASP, Threat Modeling, Zero Trust, IAM, Secrets, Encryption, Vulnerability Management, Supply Chain, Compliance Framework, Auditing, SOC2, ISO 27001, HIPAA, GDPR, SecOps, Security Reference Architecture)

### Added — Phase 6 (Platform Engineering)
- NES-500 to NES-520: Platform standards (Docker, Kubernetes, Terraform, GitHub Actions, GitOps, ArgoCD, Helm, Cloudflare, AWS, Multi-Cloud, CDN, Networking, Service Mesh, Secrets, Infrastructure Security, Monitoring, Logging, Incident Response, Disaster Recovery, Reference Architecture)

## [1.5.0] — 2026-07-04

### Added — Phase 5 (AI Platform)
- NES-218 to NES-230: AI Platform standards migrated to 09-ai/ (AI Knowledge Platform, AI Agent Architecture, MCP, Prompt Engineering, Model Management, AI Evaluation, AI Observability, AI Security, Responsible AI, AI Compliance, AI Platform Operations, AI Platform DR, AI Platform Reference Architecture)

### Added — Phase 4 (Frontend Engineering)
- NES-300 to NES-320: Frontend standards in 06-frontend/ (21 documents)

### Added — Phase 3 (Backend Engineering)
- NES-200 to NES-217: Backend standards in 05-backend/ (18 documents)
- NES-217: Document Intelligence & OCR (new, filling gap)

## [1.0.0] — 2026-07-04

### Added — Repository Structure
- Initialized v1.0 frozen repository structure with 24-folder hierarchy
- Root files: README.md, CONTRIBUTING.md, CHANGELOG.md, LICENSE.md

### Added — Phase 1 (Foundation)
- NES-000 to NES-011: Foundation standards in 00-foundation/

### Added — Phase 2 (Architecture)
- NES-100 to NES-110: Architecture standards in 01-architecture/
- NES-1200 to NES-1210: Enterprise Reference Architectures in 01-architecture/

### Added — Engineering Laws
- LAW-001 to LAW-010: All 10 Engineering Laws in 02-engineering-laws/

### Added — Technology Standards
- TECH-001 to TECH-013: Technology Stack standards in 03-technology/

### Added — Repository Standards
- REPO-001 to REPO-008: Repository governance standards in 04-repository/

### Added — Governance Documents
- ADR-001 to ADR-005: Architecture Decision Records in 19-adrs/
- RFC-001 to RFC-003: Requests for Comments in 20-rfcs/
- NSC-001 to NSC-005: Production checklists in 18-checklists/
- NES-DS-001: Design System Standard in 16-design-system/
- Appendix: acronyms.md, bibliography.md, index.md, references.md

### Added — GitHub Automation
- .github/CODEOWNERS: Code ownership declarations
- .github/PULL_REQUEST_TEMPLATE.md: PR template
- .github/ISSUE_TEMPLATE/document_request.md: Issue template
- .github/workflows/validate.yml: CI validation pipeline
