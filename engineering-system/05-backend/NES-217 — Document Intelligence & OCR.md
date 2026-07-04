---
document_id: NES-217
title: Document Intelligence & OCR
subtitle: Enterprise Document Parsing, OCR Extraction & Data Structuring Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Data Platform Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-216 File Processing Architecture
next_document: NES-218 AI Knowledge Platform
---

# NES-1217 — Document Intelligence & OCR

> **"Unstructured files are pools of dark data. We extract text, parse tables, and structure document metadata using standardized optical character recognition (OCR) pipelines."**

---

# Executive Summary

Organizations process massive volumes of unstructured document files (PDFs, TIFF images, scanned receipts, academic transcripts).

If files are stored without text extraction or metadata indexing, their content remains unsearchable.

We mandate the use of the **Document Intelligence & OCR Pipeline** across all NeelStack services.

This standard establishes our optical character recognition models (Tesseract, AWS Textract), parsing standards, processing formats, and database search integrations.

---

# Purpose

This standard defines:

- Document Parsing Architecture
- Approved OCR Tooling (Tesseract, AWS Textract)
- Table Extraction and Layout Analysis (LayoutLM)
- Structured Output Formatting (JSON Schemas)
- Search Indexing Pipelines (OpenSearch)

---

# Document Parsing Pipeline

The Document Intelligence pipeline processes inbound files through structured validation stages:

```text
  Inbound File (PDF / Image) ──► PDF Metadata Extraction (PyMuPDF)
                                       │
                              (Text missing / Scanned)
                                       │
                                       ▼
                             OCR Engine (AWS Textract)
                                       │
                                       ▼
                       Layout Analysis (LayoutLM table parse)
                                       │
                                       ▼
                      JSON Metadata Compilation & Indexing
```

---

# Approved OCR Tooling & Engines

Select OCR engines based on resource and accuracy requirements:

- **Local Processing (Tesseract OCR)**: Use Tesseract for low-cost, high-volume basic text extraction tasks. Ensure languages packs are pre-installed in docker base layers.
- **Cloud Processing (AWS Textract / Azure Document Intelligence)**: Use managed cloud services for complex documents, multi-page PDFs, handwritten text, and multi-column tables.

---

# Table & Layout Extraction (LayoutLM)

To extract structural meaning from documents (like forms, invoices, and transcripts):

- **Layout Analysis**: Use layout-aware models (e.g. LayoutLM v3) to identify headers, footers, paragraphs, and list items.
- **Table Parsing**: Extract tables into structured arrays. Every cell must retain its column/row index and text alignment.

---

# Structured JSON Outputs

OCR results must be compiled into structured JSON conforming to target schemas:

```json
{
  "document_id": "doc-83a74e98",
  "ocr_engine": "aws-textract",
  "metadata": {
    "page_count": 1,
    "confidence_score": 0.985
  },
  "content": {
    "paragraphs": [
      {
        "page": 1,
        "text": "NeelStack educational transcripts register..."
      }
    ],
    "tables": [
      {
        "id": "table-1",
        "rows": [
          ["Subject", "Grade", "Status"],
          ["Mathematics", "A", "Pass"]
        ]
      }
    ]
  }
}
```

---

# OpenSearch Indexing & Search

- **Search Indexing**: Stream JSON outputs to OpenSearch.
- **Scrubbing**: Scrub customer PII (names, phone numbers) before writing logs to search indexes.

---

# Anti-Patterns

❌ **Table Scraping via Regular Expressions**: Using simple regex models to scrape columns from multi-column layout files, causing data formatting errors.

❌ **Exposing Plaintext PII in Search Indices**: Indexing raw personal student records or medical history notes without privacy scrubbing gates (NES-710).

❌ **Direct DB Blobs Storage**: Storing extracted OCR JSON strings directly inside relational database blobs, which slows down transactional queries.

---

# Production Checklist

- [ ] PDF parser pipelines check metadata before initiating OCR.
- [ ] AWS Textract / Azure Document Intelligence credentials are secure.
- [ ] Table extraction helpers validate layout structures.
- [ ] Output JSON follows schema guidelines.
- [ ] OpenSearch indexing pipelines scrub PII.

---

# Success Criteria

The Document Intelligence & OCR program is successful when:
- Text is extracted and indexed from 100% of uploaded document scans.
- Table parsing accuracy exceeds 95% in validation checks.
- Extracted document text is searchable in under 1.5 seconds.

---

# Document Status

**Document:** NES-217 — Document Intelligence & OCR
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-218 — AI Knowledge Platform**