---
document_id: NES-601
title: OWASP Security Standards
subtitle: Enterprise OWASP Top 10 Web & API Mitigation Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Security Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-600 Secure SDLC
next_document: NES-602 Threat Modeling
---

# NES-601 — OWASP Security Standards

> **"Code must defend itself against input threats. We implement secure coding practices to mitigate the OWASP Top 10 Web and API vulnerabilities."**

---

# Executive Summary

Web applications and API endpoints are exposed to constant automated attacks seeking to exploit coding mistakes.

These include SQL injections, cross-site scripting (XSS), broken object-level authorization, and security misconfigurations.

We mandate compliance with **OWASP (Open Web Application Security Project) secure coding practices** across all NeelStack projects.

This standard outlines the mitigation rules, input validations, output encodings, and session management configurations required to protect our services.

---

# Purpose

This standard defines:

- Injection Defenses (SQLi, XSS, Command Injection)
- Broken Authorization Mitigations (BOLA, BFLA)
- Input Validation and Output Encoding Standards
- Sensitive Data Exposure Protections
- Security Configuration Baselines

---

# Injection Mitigation (SQLi & XSS)

Injection occurs when untrusted user input is executed as commands.

- **SQL Injection Defense**: Never construct raw SQL strings by concatenating variables. Always use parameterized queries (Object-Relational Mapping - ORM) or prepared statements (NES-207).
- **Cross-Site Scripting (XSS) Defense**: Sanitize and HTML-encode all user-generated content on the server side before storing it, and escape data output inside React/Next.js components.
- **Command Injection Defense**: Avoid using system execution APIs (e.g. `exec`, `spawn` or python `os.system`) with parameters derived from client inputs.

```python
# Correct Parameterized Query using SQLAlchemy ORM
from sqlalchemy import text

def get_student_by_email(email: str):
    # Parameterized input binds values safely
    query = text("SELECT * FROM students WHERE email = :email")
    return db.execute(query, {"email": email}).first()
```

---

# Broken Object-Level Authorization (BOLA)

BOLA (or IDOR) occurs when an endpoint accepts user-provided resource IDs (e.g., `/api/documents/123`) without verifying if the requesting user owns that resource.

- **Mitigation**: Every database query that fetches resources based on client parameters must include a tenancy/ownership filter:
  - *Wrong*: `SELECT * FROM documents WHERE id = :id`
  - *Correct*: `SELECT * FROM documents WHERE id = :id AND tenant_id = :tenant_id AND user_id = :user_id`
- **Universally Unique IDs (UUIDs)**: Use random UUIDv4 identifiers instead of sequential auto-incrementing integers for resource primary keys to prevent ID enumeration scans.

---

# Input Validation & Output Encoding

Never assume client inputs (URLs, HTTP headers, cookies, JSON bodies) are formatted correctly.

- **Schema Validation**: Validate all inbound payloads against schemas (e.g., Pydantic in FastAPI, Zod in Next.js).
- **Type, Length, Format**: Enforce strict length limits and regex matches (e.g., email format, numeric-only phone fields).
- **Sanitisation**: Strip HTML tags and control characters from text parameters prior to saving them.

---

# Sensitive Data Exposure & Session Security

Protect user sessions and access tokens:

- **HttpOnly Cookies**: Store session identifiers or access tokens in **HttpOnly, Secure, SameSite=Strict** cookies. This blocks client-side JavaScript access, mitigating XSS token theft.
- **Payload Encryption**: Sensitive fields (like Social Security Numbers, tax identifiers, or medical codes) must be encrypted in memory before database insert actions.

---

# Anti-Patterns

❌ **Client-Side Validation Only**: Relying solely on React forms to check input lengths. A attacker can bypass the UI entirely and send malicious HTTP requests directly to the API endpoints.

❌ **Sequential Database Primary Keys**: Utilizing auto-incrementing integers (e.g. `/user/1`, `/user/2`) which allow attackers to scrape all users by scripting increments.

❌ **Exposing Stack Traces**: Returning raw exception strings or traceback stack dumps inside HTTP 500 error payloads, which exposes internal database names and libraries to attackers.

---

# Production Checklist

- [ ] Prepared statements are used for all database access pathways.
- [ ] Schema validation (Pydantic/Zod) is active on all input routes.
- [ ] API endpoints enforce tenant ownership filters.
- [ ] Session cookies use HttpOnly, Secure, and SameSite parameters.
- [ ] Error handlers catch raw exceptions and return masked generic message strings.

---

# Success Criteria

The OWASP security standards are successful when:
- Vulnerability scans (SAST/DAST) confirm zero active injection flaws in codebase repositories.
- Pen testing evaluations confirm BOLA validation is active across all resource endpoints.
- XSS filter audits show client-side browser cookies are protected from access.

---

# Document Status

**Document:** NES-601 — OWASP Security Standards
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-602 — Threat Modeling**
