---
document_id: LAW-001
title: Business Logic
subtitle: All business logic must live in the domain layer — never in controllers, APIs, or databases
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Chief Architect
review_cycle: Annual
document_type: Engineering Law
next_document: LAW-002 Domain Ownership
---

# LAW-001 — Business Logic

> **"Business logic belongs in the domain. If you put it anywhere else, you have already violated the architecture."**

---

## Law Statement

**All business logic, domain rules, and decision-making algorithms MUST reside exclusively in the domain layer.**

Business logic is PROHIBITED from existing in:
- HTTP controllers or route handlers
- API gateway layers
- Database stored procedures or triggers
- Frontend components
- Background job workers (except domain calls)
- Infrastructure adapters

---

## Definition of Business Logic

Business logic is any code that:
- Enforces a business rule (e.g. "a student cannot enroll in more than 8 courses")
- Makes a domain decision (e.g. "eligible for scholarship if GPA > 3.5")
- Calculates a business value (e.g. "total fee = base fee × tax rate × discount")
- Validates domain constraints (e.g. "invoice total cannot be negative")
- Orchestrates domain workflows (e.g. "approval requires two signatories above INR 1 lakh")

---

## Correct Pattern

```python
# ✅ CORRECT — Business logic in domain service
class EnrollmentService:
    def enroll_student(self, student_id: UUID, course_id: UUID) -> Enrollment:
        student = self.student_repo.get(student_id)
        course = self.course_repo.get(course_id)

        # Domain rule enforced here
        if student.active_enrollments >= 8:
            raise EnrollmentLimitExceeded("Student cannot enroll in more than 8 courses")

        if not course.has_capacity():
            raise CourseCapacityExceeded("Course is full")

        return Enrollment.create(student_id, course_id)
```

```python
# ❌ WRONG — Business logic in API controller
@router.post("/enroll")
async def enroll(student_id: UUID, course_id: UUID, db: Session):
    student = db.query(Student).filter(Student.id == student_id).first()
    if len(student.enrollments) >= 8:  # Business rule in controller!
        raise HTTPException(400, "Too many enrollments")
    ...
```

---

## Why This Law Exists

1. **Testability**: Domain logic in the domain layer can be unit-tested without HTTP, databases, or infrastructure.
2. **Reusability**: The same rule enforced in one place applies to all callers — API, background jobs, CLI.
3. **Maintainability**: Business rules change. If they live in the domain, you change them once.
4. **Auditability**: Business decisions are traceable to specific domain methods with clear intent.
5. **Architecture Integrity**: Controllers that contain business logic violate Clean Architecture and cannot be reasoned about independently.

---

## Enforcement

| Level | Enforcement Method |
|---|---|
| Code Review | Reviewers must reject PRs that contain business logic outside the domain |
| Architecture Tests | ArchUnit / import-linter tests must validate layer boundaries |
| CI Pipeline | Automated dependency direction checks block merges |

---

## Related Standards

- NES-104 — Clean Architecture
- NES-103 — Domain-Driven Design
- LAW-002 — Domain Ownership
- NES-200 — Python Engineering Standards

---

## Version History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2026-07-04 | NeelStack Engineering | Initial publication |
