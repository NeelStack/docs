# PRD-003 — Online Fee Payment Integration

## 1. Problem Statement
School fee collection is currently plagued by long queue times at accounting counters, manual processing of checks and drafts, and delayed bank reconciliations. Parents struggle to remember due dates and amounts, leading to outstanding payments. The school's cash flow is unpredictable, and billing staff spend excessive time calling defaulters and writing physical receipts.

## 2. Target Users & Personas
- **Parent**: Guardian who needs to make school fee payments. Prefers UPI, credit/debit card, or net banking.
- **School Accountant**: Sets up fee structures, checks outstanding balances, and issues due notifications.

## 3. User Stories (Gherkin format)
```gherkin
Feature: Razorpay Online Fee Collection

  Scenario: Parent completes a fee transaction
    Given A parent has an outstanding fee balance on the Mobile Portal
    When They select a fee item and click "Pay Now via Razorpay"
    And Complete payment in the secure Razorpay checkout modal
    Then The payment status changes to "Settled"
    And A digital fee receipt is automatically generated and sent via email
    And The student's fee submit status flag is updated in the database

  Scenario: System sends automatic fee due reminder
    Given The system date matches the configured reminder window
    When There are unpaid fee items with due dates approaching
    Then The system triggers an email and SMS alert containing a direct checkout link
```

## 4. Technical Dependencies & Integrations
- **Payment Provider**: Razorpay SDK and API (Razorpay Key ID and Secret configured).
- **Accounts Module**: Updates transaction logs in the `account_transaction` table.
- **Notification Engine**: Dispatches receipts, payment alerts, and due reminders.
- **Auditing**: Records transactional status shifts in `audit_log`.

## 5. Success Metrics
- **Digital Collections**: Target > 90% of fee payments processed online.
- **Collection Cycle**: Reduce average collection window from 15 days to under 3 days from date of issue.
- **Reconciliation Errors**: Reduce manual bookkeeping reconciliation errors to 0%.
