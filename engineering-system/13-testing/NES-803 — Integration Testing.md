---
document_id: NES-803
title: Integration Testing
subtitle: Enterprise Integration Testing, API Contract & Testcontainers Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Engineering Quality Board
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-802 Unit Testing
next_document: NES-804 E2E Testing
---

# NES-803 — Integration Testing

> **"Services must communicate reliably. We test integrations using real ephemeral databases, verify API contracts, and run isolated network test suites."**

---

# Executive Summary

While unit tests prove individual function logic, applications often fail due to integration issues, such as mismatched database schemas, broken API parameters, or incorrect message broker headers.

Mocking external systems (like Postgres or Redis) inside unit tests can mask these integration errors.

We mandate the execution of **Integration Testing** for all backend services.

This standard establishes our API contract checks, ephemeral database testing rules (**Testcontainers**), and messaging queue validation standards.

---

# Purpose

This standard defines:

- Integration Testing Scope and Boundaries
- Ephemeral Database Testing (Testcontainers)
- API Contract Testing (Schemathesis / MSW)
- Message Broker Testing Standards
- Test Isolation in Integration Runs

---

# Integration Testing Scope

Integration tests verify the execution paths between our application code and active external system dependencies:

- **Database integration**: Validating query outputs against actual databases.
- **API integrations**: Verifying client endpoints return payloads matching the schema schema specifications.
- **Event queues**: Confirming messages publish and consume correctly from brokers.

---

# Ephemeral Databases (Testcontainers)

We prohibit integration tests from sharing static database instances, which can cause test data contamination.

- **Standard**: Use **Testcontainers** (in Python, Node, or Go) to spin up clean, ephemeral Docker containers (e.g. Postgres, Redis) dynamically at test startup.
- **Execution**: The test runner launches the container, executes database migrations, runs tests, and terminates the container automatically.

```python
# Reference Testcontainers configuration in Pytest
import pytest
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def database_connection():
    # Spin up an ephemeral Postgres container
    with PostgresContainer("postgres:16-alpine") as postgres:
        conn_url = postgres.get_connection_url()
        # Initialize database tables and run migrations...
        yield conn_url
```

---

# API Contract Testing

Verify that API endpoints match open specifications:

- **Schemathesis (Contract Testing)**: Run **Schemathesis** in CI to automatically generate and execute HTTP test requests against backend API routes, verifying inputs conform to the OpenAPI schema.
- **Mock Service Worker (MSW)**: In web and mobile frontends, use **MSW** to intercept network calls and return mock payloads, allowing frontend integration tests to run without active backends (NES-312).

---

# Message Broker Testing

Verify asynchronous communications:

- **Scope**: Spin up local Apache Kafka or RabbitMQ instances in Docker containers using Testcontainers.
- **Validation**: Confirm the producer publishes messages containing correct schemas, and verify the consumer processes payloads and updates database states correctly.

---

# Anti-Patterns

❌ **Connecting to Shared Staging DBs**: Running integration tests that read or write to active shared staging databases, which causes flaky test runs.

❌ **Omitting Database Migrations in Tests**: Running queries against databases initialized with static mock structures instead of executing the active migration scripts, which masks schema mismatches.

❌ **Exposing Cloud Secrets in Test Runs**: Committing private AWS keys to repositories to test S3 upload integration. Use LocalStack to mock AWS services locally.

---

# Production Checklist

- [ ] Testcontainers is integrated with integration testing runners.
- [ ] LocalStack is configured for local AWS integrations.
- [ ] API routes pass Schemathesis contract checks.
- [ ] MSW intercept mappings are active for frontend tests.
- [ ] Database migrations execute prior to database test runs.

---

# Success Criteria

The Integration Testing program is successful when:
- Mismatched database schemas or API contracts are caught and blocked in CI before merge.
- Integration tests execute in isolated environments with zero cross-test state dependencies.
- Local tests run without requiring access keys or active internet connections.

---

# Document Status

**Document:** NES-803 — Integration Testing
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-804 — E2E Testing**
