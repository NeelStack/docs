---
document_id: NES-209
title: Object Storage Standards
subtitle: Enterprise Object Storage Architecture & File Management Standard for the NeelStack Platform
version: 1.0.0
status: Draft
classification: Internal
owner: Chief Solution Architect
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-208 Redis Standards
next_document: NES-210 Search Architecture
---

# NES-209 — Object Storage Standards

> **"Databases store structured business data. Object storage stores everything else."**

---

# Executive Summary

Object Storage is the official storage platform for all binary assets across the NeelStack ecosystem.

It stores:

- Documents
- PDFs
- Images
- Videos
- Audio
- Reports
- Backups
- AI Datasets
- Static Assets
- User Uploads
- Application Exports

Object Storage is designed for:

- Unlimited scalability
- High durability
- Global accessibility
- Low operational cost
- Secure access
- Multi-tenant isolation

Object Storage is **not a database**.

Metadata belongs in PostgreSQL.

---

# Purpose

This standard defines:

- Object Storage Architecture
- Bucket Organization
- Object Naming
- Metadata Management
- Upload Architecture
- Download Architecture
- Security
- Lifecycle Management
- Versioning
- CDN Integration
- AI Integration
- Backup Strategy

---

# Vision

Create a unified object storage platform capable of managing:

- Billions of Files
- Petabytes of Data
- Global CDN Distribution
- AI Asset Pipelines
- Multi-Tenant SaaS
- Enterprise Compliance

without redesign.

---

# Object Storage Philosophy

```text
Client

↓

API

↓

Validation

↓

Object Storage

↓

Metadata

↓

PostgreSQL
```

Binary files live in Object Storage.

Business metadata lives in PostgreSQL.

---

# Guiding Principles

Every storage system must be:

✓ Secure

✓ Durable

✓ Multi-Tenant

✓ Versioned

✓ Observable

✓ Cost Efficient

✓ Globally Accessible

✓ Cloud Native

---

# Approved Storage Providers

Primary

```
Cloudflare R2
```

Secondary

```
AWS S3
```

Compatible

```
MinIO

Backblaze B2

DigitalOcean Spaces

Google Cloud Storage

Azure Blob Storage
```

The platform uses the **S3-compatible API** abstraction.

---

# Storage Architecture

```text
Client

↓

FastAPI

↓

Upload Service

↓

Virus Scan

↓

Image/PDF Processing

↓

Object Storage

↓

CDN

↓

Download
```

Business services never communicate directly with storage providers.

---

# Storage Components

```
Application

↓

Storage Service

↓

S3 SDK

↓

Object Storage

↓

CDN
```

The Storage Service abstracts provider-specific implementations.

---

# Bucket Strategy

Recommended buckets

```
documents

images

videos

audio

avatars

reports

backups

exports

imports

ai-assets

logs

temporary
```

Separate buckets by lifecycle and security requirements.

---

# Bucket Naming

Lowercase only.

Examples

```
neelstack-documents

neelstack-images

toolvines-exports

eduos-backups
```

Avoid environment names inside bucket names.

---

# Object Naming

Never use user-supplied filenames.

Standard

```
tenant_id/

resource/

year/

month/

uuid.ext
```

Example

```
tenant-123/

students/

2026/

07/

018fa2c4.pdf
```

Predictable.

Globally unique.

---

# Object Metadata

Store metadata in PostgreSQL.

Example

```text
Object ID

Tenant ID

File Name

Original Name

Mime Type

Size

Checksum

Storage Key

Bucket

Version

Created At

Created By
```

Object Storage stores binary content only.

---

# Upload Flow

```text
Client

↓

Authentication

↓

Authorization

↓

Upload Validation

↓

Virus Scan

↓

Object Storage

↓

Metadata Saved

↓

Response
```

Metadata is written only after successful upload.

---

# Download Flow

```text
Client

↓

Authorization

↓

Metadata Lookup

↓

Signed URL

↓

Object Storage

↓

Download
```

Applications should not proxy large downloads.

---

# Signed URLs

All private objects are accessed through pre-signed URLs.

Benefits

- Temporary Access
- Reduced Backend Load
- CDN Optimization

Default expiration

```
15 Minutes
```

---

# Access Levels

Objects are classified as:

Public

Internal

Private

Restricted

Access determines URL generation and security policies.

---

# Multi-Tenant Isolation

Every object belongs to exactly one tenant.

Storage key includes

```
tenant_id
```

Cross-tenant access is prohibited.

---

# File Validation

Validate

- MIME Type
- Extension
- Size
- Malware
- File Signature

Never trust client-provided metadata.

---

# File Size Limits

Default limits

| File Type | Maximum |
|-----------|----------|
| Image | 25 MB |
| PDF | 100 MB |
| Video | 5 GB |
| Audio | 500 MB |
| Archive | 2 GB |

Overrides require architecture approval.

---

# Virus Scanning

Every uploaded file passes through:

```text
Upload

↓

Virus Scanner

↓

Quarantine (if infected)

↓

Storage
```

Infected files are never exposed.

---

# Image Processing

Supported

- Resize
- Thumbnail
- Compression
- WebP Conversion
- Metadata Removal

Original file is preserved.

---

# PDF Processing

Supported

- OCR
- Thumbnail Generation
- Text Extraction
- Digital Signature Verification
- Page Count

Processing occurs asynchronously.

---

# Video Processing

Supported

- Transcoding
- Thumbnail Generation
- Streaming Formats
- Compression

Background workers perform processing.

---

# AI Asset Storage

AI assets include

- Training Data
- Embeddings
- Prompt Files
- Knowledge Documents
- Model Artifacts

AI datasets follow tenant isolation policies.

---

# CDN Integration

Static assets served through CDN.

Flow

```text
Storage

↓

CDN

↓

Client
```

Benefits

- Lower Latency
- Reduced Costs
- Global Distribution

---

# Object Versioning

Enable object versioning for

- Documents
- Reports
- Contracts
- Templates

Supports rollback and audit requirements.

---

# Lifecycle Policies

Example

Temporary Uploads

```
30 Days
```

Exports

```
90 Days
```

Backups

```
365 Days
```

AI Temporary Files

```
7 Days
```

Lifecycle management reduces storage costs.

---

# Encryption

Mandatory

Encryption at Rest

↓

AES-256

Encryption in Transit

↓

TLS 1.3

Client-side encryption may be required for restricted datasets.

---

# Checksums

Store

```
SHA-256
```

Checksum verifies

- Integrity
- Duplicate Detection
- Corruption Detection

---

# Backup Strategy

Support

- Cross-Region Replication
- Object Versioning
- Immutable Backups
- Lifecycle Snapshots

Critical assets require geographic redundancy.

---

# Disaster Recovery

Objectives

RPO

```
≤15 Minutes
```

RTO

```
≤1 Hour
```

Mission-critical buckets may require stronger objectives.

---

# Cost Optimization

Optimize through

- Lifecycle Policies
- Compression
- Deduplication
- CDN
- Archive Storage
- Tiered Storage

Storage growth should be monitored continuously.

---

# Monitoring

Track

- Upload Rate
- Download Rate
- Storage Growth
- Bucket Size
- Object Count
- Error Rate
- Virus Scan Failures
- CDN Hit Ratio

---

# Observability

Every storage operation logs

- Trace ID
- Tenant ID
- Object ID
- User ID
- Operation
- Duration
- Storage Provider

OpenTelemetry integration is mandatory.

---

# Storage Service Interface

Every application interacts through:

```text
StorageService

↓

Upload

Download

Delete

Copy

Move

GenerateSignedURL

Exists

Metadata
```

Applications never call provider SDKs directly.

---

# Folder Structure

```text
storage/

├── api/

├── application/

├── providers/

├── metadata/

├── uploads/

├── downloads/

├── processing/

├── virus_scan/

├── lifecycle/

├── cdn/

├── backups/

└── tests/
```

---

# Anti-Patterns

Avoid

❌ Files Stored in PostgreSQL

❌ Public Storage Buckets

❌ Predictable File Names

❌ Missing Virus Scans

❌ Hardcoded Bucket Names

❌ Missing Checksums

❌ Unlimited Upload Size

❌ Cross-Tenant Storage Paths

❌ Direct Client Access Without Authorization

❌ Provider-Specific Logic in Business Code

---

# Production Checklist

Before production

- [ ] Buckets created
- [ ] Encryption enabled
- [ ] Signed URLs implemented
- [ ] Virus scanning configured
- [ ] Lifecycle policies applied
- [ ] CDN integrated
- [ ] Metadata persistence implemented
- [ ] Multi-tenant isolation verified
- [ ] Backup strategy configured
- [ ] Monitoring enabled
- [ ] Security review completed

---

# Success Criteria

Object Storage is successful when:

- Binary assets are never stored in PostgreSQL.
- Object metadata remains synchronized with business records.
- Multi-tenant isolation is guaranteed.
- Uploads are validated and scanned automatically.
- CDN accelerates global delivery.
- Lifecycle policies optimize storage costs.
- AI assets are securely managed.
- Disaster recovery objectives are consistently achieved.

---

# Future Evolution

Version 2.0 will include:

- Complete Cloudflare R2 Architecture
- AWS S3 Reference Implementation
- MinIO On-Premises Deployment
- Multipart Upload Standards
- Resumable Upload Architecture (TUS Protocol)
- Image & Video Processing Pipelines
- OCR & Document AI Integration
- Object Storage Cost Optimization Framework
- Multi-Region Replication Strategy
- Immutable Storage & Legal Hold Policies
- AI Dataset Management Architecture
- C4 Storage Architecture Diagrams
- Storage Performance Benchmark Suite
- Architecture Fitness Rules for File Management
- Production Storage Service Reference Implementation

---

# Object Storage Checklist

- [x] Storage Architecture Defined
- [x] Bucket Strategy Established
- [x] Object Naming Standardized
- [x] Metadata Model Defined
- [x] Upload & Download Flows Defined
- [x] Security Standards Added
- [x] Multi-Tenant Isolation Included
- [x] Lifecycle Policies Defined
- [x] CDN Integration Added
- [x] AI Storage Strategy Included
- [x] Monitoring & Observability Defined
- [x] Production Checklist Added
- [x] Success Criteria Defined

---

# Document Status

**Document:** NES-209 — Object Storage Standards**

**Version:** 1.0.0

**Status:** Ready for Architecture Review

**Next Document:** **NES-210 — Search Architecture**

---

# Revision Queue for Version 2.0 (Enterprise Edition)

Future enhancements will include:

- Cloudflare R2 Production Blueprint
- S3-Compatible Storage Abstraction Layer
- Multipart & Resumable Upload Standards
- Enterprise File Processing Pipeline
- AI Document Ingestion Architecture
- OCR & Vision Processing Workflow
- Storage Lifecycle Cost Modeling
- Content Deduplication Framework
- Object Retention & Legal Hold Policies
- Multi-Region Disaster Recovery Architecture
- CDN Optimization & Edge Caching Guide
- C4 Storage & CDN Diagrams
- OpenTelemetry Storage Instrumentation
- Architecture Fitness Tests for Object Storage
- Production Storage Service Starter Repository

These enhancements will establish the definitive object storage standard for the NeelStack platform, ensuring secure, scalable, cloud-native, multi-tenant, and AI-ready management of all binary assets across web, mobile, backend, and platform services.