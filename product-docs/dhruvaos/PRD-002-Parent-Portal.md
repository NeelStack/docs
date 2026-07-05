# PRD-002 — Parent Portal Mobile Portal

## 1. Problem Statement
Parents currently lack real-time visibility into their child's daily school lifecycle. To check attendance, view exam marks, ask questions to teachers, or view due fees, parents must write diary notes, call the front desk, or wait for physical parent-teacher meetings. This delays intervention when a child is absent or struggling academically.

## 2. Target Users & Personas
- **Parent**: Guardian of one or more active students in the school system. Wants quick, single-click updates on their mobile device.

## 3. User Stories (Gherkin format)
```gherkin
Feature: Parent Mobile Dashboard

  Scenario: Parent views child's attendance summary
    Given A parent is authenticated in the Mobile Portal
    When They view the Dashboard page
    Then The system shows the child's overall attendance ratio (e.g. 92%)
    And Lists a calendar marking days as Present, Absent, or Late

  Scenario: Parent submits a leave request
    Given A parent is authenticated in the Mobile Portal
    When They navigate to the "Request Leave" screen
    And Enter start date, end date, reason, and click "Submit"
    Then A leave request is created in the database with status "Pending"
    And A push notification is sent to the child's class mentor
```

## 4. Technical Dependencies & Integrations
- **Mobile Client**: Capacitor 7 wrapped React Native/Web client.
- **Attendance Module**: Reads raw date listings from the `attendance` table.
- **Accounts/Payments Module**: Fetches outstanding fee ledgers and initiates payments.
- **WebSocket Gateway**: Socket.io connection for real-time chat messages.
- **FCM Push Notification**: Custom deep linking URL scheme (`dhruvaos://`) integration on mobile.

## 5. Success Metrics
- **Parent Engagement**: Target > 65% Daily Active Users / Monthly Active Users (DAU/MAU) ratio.
- **Feedback Loop**: Reduce teacher-parent response loop time from 24 hours to under 2 hours.
- **NPS Score**: Target parent Net Promoter Score of > 45.
