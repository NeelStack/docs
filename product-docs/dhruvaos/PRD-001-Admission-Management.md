# PRD-001 — Admission Management Module

## 1. Problem Statement
The school admission process is currently manual, fragmented, and paper-intensive. Parents must physically visit the school, collect brochures, fill out long physical forms, and submit photocopies of documents. School administrators have to manually type student details into legacy database structures, leading to typing errors, lost attachments, and delayed notifications.

## 2. Target Users & Personas
- **School Registrar / Admission Officer**: Responsible for screening applications, reviewing uploaded documents, and admitting or rejecting students.
- **Parent**: Submits the application online, uploads documents (birth certificate, previous report cards), and expects updates.

## 3. User Stories (Gherkin format)
```gherkin
Feature: Online Admission Application

  Scenario: Parent submits online application successfully
    Given A parent is on the public school admission portal
    When They fill out the student details, guardian info, and upload the birth certificate PDF
    And Click "Submit Application"
    Then An admission record is created in "DRAFT" state
    And A confirmation email is dispatched to the parent

  Scenario: Registrar approves a submitted application
    Given A registrar is logged into the Admin Console
    And Views a submitted admission application in "SUBMITTED" state
    When They click "Approve and Enroll"
    Then The application state changes to "APPROVED"
    And A new student profile is automatically created in the core "student" table
    And The system issues a welcome notification to the parent with login credentials
```

## 4. Technical Dependencies & Integrations
- **Core API Gateway**: Relies on file upload APIs.
- **Object Storage Service**: Direct upload of document attachments to AWS S3 (`dhruvaos/{env}/{school_id}/admissions/`).
- **Student Module**: Creates standard `Student` row upon application approval.
- **Notification Engine**: Dispatches emails via SMTP on status changes.
- **Authorization**: Keycloak OIDC authentication is required for Admin API endpoints.
- **AI Verification Service**: Integrates with the AI Gateway service to scan and check submitted identity documents via OCR summaries.
- **Seat Capacity Guard**: Validates that active students do not exceed the target `School` total seats limit before enrollment completion.
- **Automated Class Allocation**: Queries and assigns students to the lowest available `Class` rank (e.g., Grade 1 default).
- **Billing Schedule Integration**: Triggers automated generation of enrollment and tuition invoice structures inside the accounts system.

## 5. Success Metrics
- **Online Conversion**: Target > 80% of admission applications completed online.
- **Time to Onboard**: Reduce registrar enrollment time from 30 minutes (manual entry) to under 2 minutes (one-click approval).
- **Form Drop-off**: Keep application form completion drop-off rate below 15%.
