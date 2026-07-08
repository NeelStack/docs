# PRD-005 — AI Academic Assistant

## 1. Problem Statement
Teachers and school leaders have access to massive amounts of student data (grades, attendance, behavioral logs) but lack the analytical resources to interpret it. They cannot identify students at risk of drop-out, predict attendance failures, or understand grade trends across classes. On the parent side, finding information in school handbooks or asking generic syllabus questions occupies admin staff's time.

## 2. Target Users & Personas
- **School Principal**: Wants high-level dashboards of academic trends and risk profiles.
- **Teacher**: Needs summaries of class performance and predictions of exam outcomes.
- **Parent**: Queries school policies, syllabus requirements, and fee schedules.

## 3. User Stories (Gherkin format)
```gherkin
Feature: AI Academic Assistant & Q&A

  Scenario: Teacher views class risk analysis
    Given A teacher is on the dashboard
    When They view the AI Academic Assistant widget
    Then The system lists students with high risk of failing a subject based on attendance trends
    And Provides automated, actionable intervention recommendations

  Scenario: Parent queries school rules via chatbot
    Given A parent is in the Mobile Portal chat screen
    When They ask: "What is the fee refund policy if we withdraw next month?"
    Then The AI microservice performs semantic search on the uploaded policy PDF
    And Returns a grounded, correct answer with citation references
```

## 4. Technical Dependencies & Integrations
- **AI Microservice**: Dedicated `services/ai` microservice running FastAPI.
- **pgvector**: Database storage for policy documents and syllabus embeddings.
- **LLM API Provider**: Anthropic Claude or OpenAI API.
- **Core Database**: Fetches attendance and grading records from PostgreSQL.

## 5. Success Metrics
- **Accuracy**: Keep RAG answer accuracy and context grounding score > 95%.
- **Teacher Intervention Rate**: Target > 40% of flagged student risk warnings resolved via suggested teacher interventions.
- **Staff Time Saved**: Reduce parent front-office support calls by > 30% through automated rule Q&A.
