# NeelStack Engineering Documentation

**The official NeelStack Engineering Constitution — standards, principles, laws, and reference architectures governing all NeelStack products.**

[![Validate Docs](https://github.com/NeelStack/docs/actions/workflows/validate.yml/badge.svg)](https://github.com/NeelStack/docs/actions/workflows/validate.yml)

---

## Repository Structure

```text
docs/
│
├── README.md                                  # This file
├── CONTRIBUTING.md                            # How to contribute
├── CHANGELOG.md                               # Documentation changelog
├── LICENSE.md                                 # Repository license
│
├── engineering-system/                        # ⭐ Engineering Constitution
│   ├── 00-foundation/                         # Vision, Mission, Culture, KPIs, Glossary
│   ├── 01-architecture/                       # Architecture Principles & Patterns
│   ├── 02-engineering-laws/                   # Non-negotiable Engineering Laws (LAW-001..010)
│   ├── 03-technology/                         # Approved Technology Stack (TECH-001..013)
│   ├── 04-repository/                         # Repository Standards (REPO-001..008)
│   ├── 05-backend/                            # Backend Engineering (NES-200..217)
│   ├── 06-frontend/                           # Frontend Engineering (NES-300..320)
│   ├── 07-mobile/                             # Mobile Engineering (NES-400..416)
│   ├── 08-platform/                           # Platform & DevOps (NES-500..520)
│   ├── 09-ai/                                 # AI Platform Standards (NES-218..230)
│   ├── 10-database/                           # Data Platform (NES-700..712)
│   ├── 11-security/                           # Security & Compliance (NES-600..616)
│   ├── 12-devops/                             # Platform Governance (NES-1100..1107)
│   ├── 13-testing/                            # Quality Assurance (NES-800..812)
│   ├── 14-production/                         # Operations & Releases (NES-900..911)
│   ├── 15-development/                        # Product Engineering (NES-1000..1008)
│   ├── 16-design-system/                      # Design System Standard (NES-DS-001)
│   ├── 17-templates/                          # Starter Kit Templates (NES-1300..1309)
│   ├── 18-checklists/                         # Production Checklists (NSC-001..005)
│   ├── 19-adrs/                               # Architecture Decision Records (ADR-001..005)
│   ├── 20-rfcs/                               # Requests for Comments (RFC-001..003)
│   ├── 21-reference-implementation/           # Diagrams & Reference Architectures
│   └── appendix/                              # Acronyms, Index, Bibliography, References
│
└── product-docs/                              # Product-specific documentation
    ├── toolvines/                             # Toolvines documentation
    ├── dhruvaos/                              # DhruvaOS documentation
    │   └── README.md                          # [DhruvaOS Architecture & Features Overview](file:///d:/NeelStack/docs/product-docs/dhruvaos/README.md)
    ├── naukarimitra/                          # NaukariMitra documentation
    ├── sarkarimitra/                          # SarkariMitra documentation
    └── shared-platform/                       # Shared platform documentation
```

---

## Documentation Hierarchy

```
Vision → Mission → Engineering Laws → Architecture Principles →
Technology Stack → Engineering Standards → Templates → Reference Architectures
```

**Nothing below can violate anything above.**

---

## Document Taxonomy

| Prefix | Meaning | Location |
|---|---|---|
| **NES** | NeelStack Engineering Standard | `05-backend` through `17-templates` |
| **LAW** | Engineering Law (non-negotiable) | `02-engineering-laws/` |
| **TECH** | Technology Standard | `03-technology/` |
| **REPO** | Repository Standard | `04-repository/` |
| **ADR** | Architecture Decision Record | `19-adrs/` |
| **RFC** | Request for Comments | `20-rfcs/` |
| **NSC** | NeelStack Standard Checklist | `18-checklists/` |
| **NST** | NeelStack Standard Template | `17-templates/` |

---

## Engineering Maturity Levels

| Level | Label | Meaning |
|---|---|---|
| **L0** | Draft | Initial draft, not ready for use |
| **L1** | Working | Functional, used by one team |
| **L2** | Production | Validated, used in production |
| **L3** | Enterprise | Reviewed by ARB, cross-team standard |
| **L4** | Platform | Core platform standard |
| **L5** | Gold Standard | Definitive — no planned changes |

Every document must eventually reach **L3 minimum** for production use.

---

## Quick Links

- 📋 [Engineering Laws](engineering-system/02-engineering-laws/) — Start here for non-negotiable rules
- 🏛️ [Architecture Principles](engineering-system/01-architecture/NES-100-Architecture-Principles.md) — Core architecture guidelines
- 🔧 [Technology Stack](engineering-system/03-technology/TECH-001-Technology-Stack.md) — Approved tools and technologies
- ✅ [PR Checklist](engineering-system/18-checklists/NSC-001-PR-Checklist.md) — Before submitting a PR
- 📖 [Master Index](engineering-system/appendix/index.md) — Complete list of all standards

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add or update documents.

All changes require a PR with at least one reviewer from the relevant CODEOWNERS group.
