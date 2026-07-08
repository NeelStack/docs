---
document_id: NES-409
title: Storage
subtitle: Enterprise Mobile Storage, SQLite & Preferences Standard
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

> **"Data integrity requires structured local persistence. We use Capacitor Preferences for configs and Capacitor SQLite for local relational datasets."**

---

# Executive Summary

Mobile applications must store user profiles, app configurations, offline mutation tables, and synchronized database records.

We establish two distinct local storage tiers depending on data size and relational complexity: **Key-Value Storage** (using Preferences) and **Relational Storage** (using SQLite).

This standard defines the tools, initialization methods, schemas, and security standards for local databases.

---

# Purpose

This standard defines:

- Local storage tiering (Key-Value vs. Relational)
- Key-Value Storage (`@capacitor/preferences`)
- Relational Database (`@capacitor-community/sqlite`)
- Schema migrations rules
- Relational storage encryption (SQLCipher)

---

# Local Storage Tiering

| Tier | Technology | Best For | Max Size |
|---|---|---|---|
| **Key-Value** | `@capacitor/preferences` | Simple settings, theme states, session tokens. | 6MB |
| **Relational** | `@capacitor-community/sqlite` | Document tables, offline sync queue, relational assets. | Device Limit |

---

# Key-Value Storage (Capacitor Preferences)

Preferences is an asynchronous, unencrypted key-value store mapping to native system properties (`NSUserDefaults` on iOS, `SharedPreferences` on Android).

- **Rule**: Never write plaintext passwords or secret auth keys to Preferences (use Secure Storage).
- **Access Wrapper**: Use a helper wrapper to maintain type-safe key indexing:

```typescript
import { Preferences } from '@capacitor/preferences';

type StorageKey = 'user_theme' | 'app_language' | 'has_seen_onboarding';

export async function setItem(key: StorageKey, value: string): Promise<void> {
  await Preferences.set({ key, value });
}

export async function getItem(key: StorageKey): Promise<string | null> {
  const { value } = await Preferences.get({ key });
  return value;
}
```

---

# Relational Database (Capacitor SQLite)

For structured local queries, we compile a local SQLite database using the `@capacitor-community/sqlite` plugin.

- **Initialization**: Open and run structural schema definitions on startup.

```typescript
import { CapacitorSQLite, SQLiteConnection, SQLiteDBConnection } from '@capacitor-community/sqlite';

const sqlite = new SQLiteConnection(CapacitorSQLite);

export async function initializeDatabase(): Promise<SQLiteDBConnection> {
  // Create database connection
  const db = await sqlite.createConnection(
    'neelstack_portal',
    false, // Encrypted flag (set true for SQLCipher)
    'no-encryption',
    1,
    false
  );

  await db.open();

  // Create tables inside transaction
  await db.execute(`
    CREATE TABLE IF NOT EXISTS documents (
      id TEXT PRIMARY KEY NOT NULL,
      title TEXT NOT NULL,
      status TEXT NOT NULL,
      updated_at INTEGER NOT NULL
    );
  `);

  return db;
}
```

- **Query execution**: Use parameterized statements to prevent SQL injections:

```typescript
export async function insertDocument(db: SQLiteDBConnection, doc: { id: string; title: string; status: string }) {
  await db.run(
    'INSERT OR REPLACE INTO documents (id, title, status, updated_at) VALUES (?, ?, ?, ?)',
    [doc.id, doc.title, doc.status, Date.now()]
  );
}
```

---

# Database Migrations

When updating local tables (e.g. adding columns during app store upgrades), we run version-controlled schemas migrations sequentially:

- **Rule**: Avoid `DROP TABLE` executions in production upgrade scopes.
- **Migration Script**:

```typescript
export async function runMigrations(db: SQLiteDBConnection) {
  const checkVersion = await db.query('PRAGMA user_version');
  let currentVersion = checkVersion.values?.[0]?.user_version ?? 0;

  if (currentVersion < 2) {
    await db.execute(`
      ALTER TABLE documents ADD COLUMN status TEXT DEFAULT 'draft';
    `);
    currentVersion = 2;
  }

  await db.execute(`PRAGMA user_version = ${currentVersion}`);
}
```

---

# Relational Storage Encryption (SQLCipher)

For high-security compliance (e.g., healthcare credentials), the SQLite database must be encrypted.

- **Standard**: Enable SQLite encryption using the `@capacitor-community/sqlite` SQLCipher option.
- **Key Strategy**: Retrieve a randomly generated key from `@capacitor-community/secure-storage` on startup and pass it during database initialization.

---

# Anti-Patterns

❌ **Storing Large JSON Blobs in Preferences**: Saving API list arrays (larger than 100KB) under a single key in Preferences, causing heavy serialization lags during app mount.

❌ **Running Sync Queries inside render loop**: Triggering database queries during component execution. Perform storage queries inside hooks or Zustand actions to keep rendering smooth.

---

# Production Checklist

- [ ] Database initialization runs before React mounts primary UI components.
- [ ] Database reads/writes are wrapped in error boundaries.
- [ ] DB indexes are declared on foreign key reference columns.

---

# Success Criteria

The Storage implementation is successful when:
- Queries execute within the 16ms render window (preventing UI pauses).
- Relational data updates safely without data loss on app upgrades.
- Memory leak checks verify database connections are closed on logout or app termination.

---

# Document Status

**Document:** NES-409 — Storage
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-410 — Mobile Performance**
