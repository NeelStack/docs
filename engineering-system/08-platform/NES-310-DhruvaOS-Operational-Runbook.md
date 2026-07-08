---
document_id: NES-310
title: DhruvaOS Operational Runbook
version: 1.0.0
status: Approved
owner: Platform Engineering Team
---

# DhruvaOS Operational Runbook (NES-310)

This runbook defines the **operationally-tunable parameters, cluster configuration thresholds, and step-by-step manual procedures** for the DhruvaOS platform.

---

## 1. Gateway & Ingress Tuning (§10.1)

### 1.1 Traefik Health Check Config
- **Probe Interval**: 5 seconds
- **Timeout Threshold**: 2 seconds
- **Fail Threshold**: 3 retries
- **Pass Threshold**: 1 retry
- **Ingress Scalability Limit**: Scale up replica counts manually or via autoscaler when CPU usage exceeds **90%** for 2 consecutive minutes.

---

## 2. Event Bus & Backpressure Spools (§10.2)

### 2.1 NATS JetStream Limits
- **Lag Threshold**: Trigger alert if consumer lag > **5000** messages.
- **Publisher Block Timeout (`max_pub_ack_wait`)**: 5000 milliseconds.
- **Gateway In-Memory Buffer Limit**: 100 Megabytes (MB). If exceeded, spools raw payload JSONs to local disk temp folders.

### 2.2 Retry Parameters
- **Backoff Base**: 1.5 seconds (exponential)
- **Max Retries**: 5 attempts
- **Timeout Threshold**: 3000 milliseconds

---

## 3. Database Pooling & Starvation Protection (§10.3)

### 3.1 PgBouncer Limits
- **Max User Connections (`max_user_connections`)**: Capped at **50** concurrency slots per tenant schema.
- **Gateway Rate Limiter**: 100 requests per minute per tenant (sliding window algorithm).

### 3.2 Retry Parameters
- **Backoff Base**: 2.0 seconds (exponential)
- **Max Retries**: 3 attempts
- **Timeout Threshold**: 5000 milliseconds

---

## 4. Cache Evictions & Failovers (§10.4)

### 4.1 Redis Configuration
- **Max Memory Eviction Policy**: `allkeys-lru`
- **Ping Interval Response Timeout**: 1000 milliseconds

### 4.2 Retry Parameters
- **Backoff Base**: 500 milliseconds (flat)
- **Max Retries**: 5 attempts
- **Timeout Threshold**: 1000 milliseconds

---

## 5. Object Store Resilience (§10.5)

### 5.1 MinIO Retry Parameters
- **Backoff Base**: 1.0 second (exponential)
- **Max Retries**: 4 attempts
- **Timeout Threshold**: 3000 milliseconds

---

## 6. Tenant Resource Migration Runbook (§12.1)

### 6.1 Automated Migration Alerts
- **Observability Registry Triggers**: If a tenant consistently breaches the resource utilization baseline:
  - CPU usage exceeds **70%** for 3 consecutive days.
  - LLM expenditure exceeds **$10.00/day** for 3 consecutive days.

### 6.2 Manual CLI Migration Commands
To migrate a tenant from **Schema-isolated** to a standalone **Database-isolated** server:

1. **Lock Tenant Write Actions**: Update tenant metadata flags inside Redis to read-only status:
   ```bash
   redis-cli -h $REDIS_HOST set "tenant:read_only:$TENANT_SLUG" "true"
   ```
2. **Execute Logical Dump**: Export the isolated PostgreSQL schema:
   ```bash
   pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME -n "tenant_$TENANT_SLUG" -Fd -f "/tmp/tenant_$TENANT_SLUG.dump"
   ```
3. **Restore on Standalone Target**: Create database and restore logical schema:
   ```bash
   psql -h $TARGET_HOST -U $TARGET_USER -d postgres -c "CREATE DATABASE db_$TENANT_SLUG;"
   pg_restore -h $TARGET_HOST -U $TARGET_USER -d "db_$TENANT_SLUG" --no-owner --no-privileges "/tmp/tenant_$TENANT_SLUG.dump"
   ```
4. **Consistency Verification**: Run SHA-256 table hashing and compare row counts:
   ```bash
   psql -h $TARGET_HOST -U $TARGET_USER -d "db_$TENANT_SLUG" -c "SELECT count(*) FROM students;"
   ```
5. **Update Routing Maps**: Update Traefik routing rules and Zitadel OIDC metadata variables to bind traffic to the new database URL target.
6. **Unlock Tenant**: Remove read-only status:
   ```bash
   redis-cli -h $REDIS_HOST del "tenant:read_only:$TENANT_SLUG"
   ```

### 6.3 Rollback Commands
If validation checksum checks fail at Step 4:
1. Revert Traefik routing rules and Zitadel metadata parameters to original database source variables.
2. Drop target database:
   ```bash
   psql -h $TARGET_HOST -U $TARGET_USER -d postgres -c "DROP DATABASE db_$TENANT_SLUG;"
   ```
3. Unlock original tenant schema write capability:
   ```bash
   redis-cli -h $REDIS_HOST del "tenant:read_only:$TENANT_SLUG"
   ```
