# PRD-004 — Notification Center Engine

## 1. Problem Statement
The platform lacks a central message routing framework. Every domain module (Attendance, Accounts, Exam) implements its own notification logic, leading to duplicate notification codes, inconsistent template layouts, and multiple integrations with third-party SMS/email providers. There is no tracking for delivery status, open rates, or parent subscription preferences.

## 2. Target Users & Personas
- **Parent/Student/Staff**: Receives critical platform updates across multiple channels (Email, SMS, FCM Push, In-App).
- **Domain Developer**: Needs a simple backend API call to trigger alerts without manually implementing mail templates or channel logic.

## 3. User Stories (Gherkin format)
```gherkin
Feature: Centralized Notification Dispatching

  Scenario: System routes event notification to multiple channels
    Given An event is triggered in the Core API (e.g. STUDENT_ABSENT)
    When The notification engine consumes the event payload
    Then It determines the user's channel preferences
    And Dispatches an SMS via Twilio/MSG91 and a push notification via Firebase Cloud Messaging (FCM)
    And Stores the alert in the database for the parent's in-app notification center feed

  Scenario: User updates channel notification preferences
    Given A parent is on the mobile setting screen
    When They toggle "Disable SMS Reminders"
    Then The system updates their channel preference map
    And Subsequent non-critical fee alerts bypass the SMS gateway
```

## 4. Technical Dependencies & Integrations
- **Message Broker**: RabbitMQ queues for asynchronous worker consumers.
- **Background Workers**: Python `celery` / `rq` or Node `BullMQ` workers.
- **SMS Providers**: MSG91 or Twilio API interfaces.
- **Email Gateway**: Standard SMTP client (`fastapi-mail` or AWS SES).
- **Push Service**: Firebase Cloud Messaging (FCM) server SDK.

## 5. Success Metrics
- **Delivery Rate**: Target > 99.5% delivery success across active email/SMS gateways.
- **Dispatch Latency**: Keep message delivery latency under 2 seconds from API event trigger to user handset.
- **Developer Overhead**: Reduce notification implementation time for new features from 4 hours to a single function call.
