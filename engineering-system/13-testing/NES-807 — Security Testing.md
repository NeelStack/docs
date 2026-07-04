---
document_id: NES-807
title: Security Testing
subtitle: Enterprise QA Security Scanning, OWASP ZAP & Vulnerability Sweeps
version: 1.0.0
status: Draft
classification: Internal
owner: Quality Assurance & Security Board
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-806 Load Testing
next_document: NES-808 Manual Testing
---

# NES-807 — Security Testing

> **"Verification must include threat analysis. We integrate automated security scanners and input validation rules directly into our daily QA pipelines."**

---

# Executive Summary

While dedicated security teams run audits (NES-600), developers and QA teams must catch common security coding bugs during code verification cycles.

Relying solely on external annual penetration testing to find vulnerabilities like missing authorization checks, exposed debug cookies, or un-sanitized inputs is a risk.

We mandate the execution of **Security Testing** inside our daily Quality Assurance pipelines.

This standard establishes our QA security scanning standard, automated scanning tools (**OWASP ZAP**), and input validation checks.

---

# Purpose

This standard defines:

- Automated Security Scanning (OWASP ZAP)
- Input Validation Gating
- Authentication Check Audits
- Dependency Scanning Gates (Snyk)
- Security Verification Checklist

---

# Automated Security Scanning (OWASP ZAP)

We integrate vulnerability scanning directly into our automated E2E pipelines:

- **Tooling**: Configure **OWASP Zed Attack Proxy (ZAP)** to crawl staging routes during test runs.
- **Workflow**: As E2E UI tests run, ZAP proxies the traffic, intercepts parameters, and runs scans to identify security gaps:
  - Cross-Site Scripting (XSS) inputs.
  - SQL Injection vulnerabilities.
  - Insecure HTTP headers (missing HSTS, CSP, or CORS parameters).

---

# Input Validation Gating

Verify that API boundaries drop invalid or malicious inputs:

- **Negative Testing**: All integration test suites must contain negative validation test cases (e.g. sending SQL keywords inside login forms, passing massive payload sizes, or inputting negative integers into price APIs).
- **Rule**: APIs must return standard validation error codes (HTTP 400 or 422) for invalid parameters—not internal database server stack traces (HTTP 500).

```python
# Reference Integration Test validating input restrictions
def test_student_registration_rejects_sql_keyword(client):
    # Send a malicious string inside a registration endpoint
    payload = {"email": "test'; DROP TABLE students;--", "name": "Hack"}
    response = client.post("/v1/students/register", json=payload)
    
    # Assert the system caught the invalid input safely
    assert response.status_code == 422
    assert "detail" in response.json()
```

---

# Dependency Security Sweeps

Prevent importing compromised packages:

- **Snyk Integration**: Run Snyk sweeps automatically during build tests.
- **SLA Enforcement**: Block build compilation tasks if third-party modules contain critical or high-priority vulnerabilities.

---

# Authentication Controls Auditing

Verify session behaviors:

- **Token Expirations**: Integration tests must confirm that expired JWT tokens are rejected.
- **Dynamic Session Invalidation**: Verify that password reset actions invalidate all active session tokens across devices immediately.

---

# Anti-Patterns

❌ **Disabling CORS Rules**: Configuring API CORS rules to accept wildcards (`*`) to simplify staging tests, exposing production resources to CSRF attacks.

❌ **Exposing Exception Context**: Returning traceback details inside client error payloads, exposing table names or library paths.

❌ **Ignoring Deprecated Security Warnings**: Overriding dependency scanning alerts without implementing compensating controls.

---

# Production Checklist

- [ ] OWASP ZAP is integrated with staging CI pipelines.
- [ ] API validation tests check boundary values and negative inputs.
- [ ] Dependency scanners (Snyk) run on all code repositories.
- [ ] JWT tokens include expiry checks.
- [ ] Error handlers log exceptions internally and mask output error messages.

---

# Success Criteria

The Security Testing program is successful when:
- 100% of pull requests pass dependency security scans.
- SQL or parameter injection bugs are caught and blocked in CI before merge.
- Staging environment test suites verify CORS and security header compliance.

---

# Document Status

**Document:** NES-807 — Security Testing
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-808 — Manual Testing**
