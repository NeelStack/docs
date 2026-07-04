---
document_id: NES-409
title: Storage
subtitle: Enterprise Mobile Storage, SQLite, AsyncStorage & Migration Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Mobile Architecture Board
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-408 Background Sync
next_document: NES-410 Mobile Performance
---

# NES-409 — Storage

> **"Data integrity requires structured local persistence. We use AsyncStorage for light key-value configs and SQLite/WatermelonDB for relational datasets."**

---

# Executive Summary

Mobile applications must store user profiles, app configurations, offline mutation queues, and large sets of synchronized database records.

Using unstructured JSON files or flat file writers causes data corruption, blocking UI performance, and memory bloat.

This standard establishes the data storage layers for NeelStack mobile apps, defining when to use key-value storage vs. relational databases, alongside migration and security rules.

---

# Purpose

This standard defines:

- Local Storage Tiering (Key-Value vs. Relational)
- Key-Value Storage (AsyncStorage)
- Relational Databases (Expo SQLite / WatermelonDB)
- Database Migrations
- Storage Security and Performance

---

# Local Storage Tiering

We use two distinct tiers of local storage depending on dataset size and structure:

| Tier | Technology | Best For | Max Size |
|---|---|---|---|
| **Key-Value** | `@react-native-async-storage/async-storage` | Simple configs, theme preferences, non-sensitive states. | 6MB |
| **Relational** | `expo-sqlite` / `WatermelonDB` | Document tables, offline sync datasets, relational records. | Device Limit |

---

# Key-Value Storage (AsyncStorage)

AsyncStorage is a simple, unencrypted key-value store.

- **Rule**: Never store sensitive data (e.g. access tokens, keys, PII) in AsyncStorage.
- **Access Wrapper**: Always wrap AsyncStorage keys in a helper utility to enforce type safety.

```typescript
import AsyncStorage from '@react-native-async-storage/async-storage';

type StorageKey = 'user_theme' | 'app_language' | 'has_seen_onboarding';

export async function setStorageItem(key: StorageKey, value: string): Promise<void> {
  await AsyncStorage.setItem(key, value);
}

export async function getStorageItem(key: StorageKey): Promise<string | null> {
  return await AsyncStorage.getItem(key);
}
```

---

# Relational Database (Expo SQLite)

For structured, relational data (e.g. a list of student records, certificates, and invoices), use **Expo SQLite** with SQLite engine.

- **Database Helper**: Use parameters in all queries to prevent SQL injection.
- **Transaction Safety**: Always perform writes inside transactions to ensure data consistency in case of crash.

```typescript
import * as SQLite from 'expo-sqlite';

const db = SQLite.openDatabaseSync('neelstack_portal.db');

export async function initializeDatabase() {
  await db.execAsync(`
    PRAGMA journal_mode = WAL;
    CREATE TABLE IF NOT EXISTS documents (
      id TEXT PRIMARY KEY NOT NULL,
      title TEXT NOT NULL,
      status TEXT NOT NULL,
      updated_at INTEGER NOT NULL
    );
  `);
}

export async function insertDocument(doc: { id: string; title: string; status: string }) {
  await db.runAsync(
    'INSERT OR REPLACE INTO documents (id, title, status, updated_at) VALUES (?, ?, ?, ?);',
    [doc.id, doc.title, doc.status, Date.now()]
  );
}
```

---

# Database Migrations

When upgrading local schemas (e.g. adding a new column to a table), we must run safe schema migrations to avoid deleting existing user data.

- **Standard**: Define schema versions and execute migrations incrementally.
- **Rule**: Never execute raw `DROP TABLE` statements on production devices unless explicitly approved by the Architecture Board.

```typescript
const SCHEMA_VERSION = 2;

export async function runMigrations() {
  const currentVersion = await db.getFirstAsync<{ user_version: number }>('PRAGMA user_version;');
  let version = currentVersion?.user_version ?? 0;

  if (version < 1) {
    // Initial schema
    await db.execAsync(`
      CREATE TABLE documents (id TEXT PRIMARY KEY, title TEXT);
    `);
    version = 1;
  }

  if (version < 2) {
    // Upgrade schema
    await db.execAsync(`
      ALTER TABLE documents ADD COLUMN status TEXT DEFAULT 'draft';
    `);
    version = 2;
  }

  await db.execAsync(`PRAGMA user_version = ${SCHEMA_VERSION};`);
}
```

---

# Storage Security

For applications with high-security profiles (e.g. enterprise healthcare apps), the SQL database must be encrypted.

- **Standard**: Use SQLCipher (via Expo custom plugins or expo-sqlite bindings) to secure the database file using an AES-256 key generated and stored inside the iOS/Android hardware keychains.

---

# Anti-Patterns

❌ **Storing Large JSON Blobs**: Saving raw API payloads (larger than 100KB) under a single key in AsyncStorage, which slows down application load times due to JSON serialization bottlenecks.

❌ **Running DB Queries on UI Thread**: Triggering synchronous database reads inside components during UI rendering. Always fetch asynchronous using React Hooks or Zustands store integrations.

❌ **Forgetting Database Indexes**: Querying large local SQLite tables (thousands of rows) without indexes on foreign keys, leading to sluggish search features.

---

# Production Checklist

- [ ] WAL journal mode is enabled for expo-sqlite to optimize read/write concurrency.
- [ ] Database initialization and migrations run on application startup before mounting UI.
- [ ] Error boundary handles database initialization failures.
- [ ] Storage constraints check is implemented for large sync configurations.

---

# Success Criteria

The Storage implementation is successful when:
- Local database queries complete in less than 16ms (within one frame limit).
- Schema updates run successfully without user data loss during app store upgrades.
- Storage memory leaks are prevented by closing query cursors and indexing databases correctly.

---

# Document Status

**Document:** NES-409 — Storage
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-410 — Mobile Performance**
