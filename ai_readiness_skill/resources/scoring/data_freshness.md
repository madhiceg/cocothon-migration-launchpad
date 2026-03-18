# Data Freshness

**Weight:** 10% of overall AI Readiness Score
**Max Score:** 100

Stale data leads to stale predictions. AI models must be trained and served on timely data to deliver value. This dimension measures ingestion latency, staleness detection, and refresh strategy maturity.

---

## Criteria

### 1. Pipeline Latency (Weight: 30%)

Time between source event and Snowflake availability.

| Score | Condition |
|-------|-----------|
| 0-20 | Batch loads >24h old; no SLA tracking |
| 21-40 | Daily batch loads with known lag |
| 41-60 | Hourly loads or Snowpipe with moderate lag |
| 61-80 | Near-real-time Snowpipe Streaming or continuous tasks |
| 81-100 | Sub-minute ingestion with Dynamic Tables auto-refresh |

**Snowflake Signals:**
- `COPY_HISTORY` view — load timestamps
- `PIPE_USAGE_HISTORY`
- `DYNAMIC_TABLE_REFRESH_HISTORY`

---

### 2. Staleness Detection (Weight: 25%)

Automated detection of stale or outdated tables.

| Score | Condition |
|-------|-----------|
| 0-20 | No staleness monitoring |
| 21-40 | Manual checks on key tables |
| 41-60 | `SNOWFLAKE.CORE.FRESHNESS` DMF on critical tables |
| 61-80 | Freshness DMF + anomaly detection on most tables |
| 81-100 | Full freshness coverage with automated alerting and SLA enforcement |

**Snowflake Signals:**
- `SNOWFLAKE.CORE.FRESHNESS` DMF
- `DATA_QUALITY_MONITORING_USAGE_HISTORY`

---

### 3. Refresh Strategy (Weight: 25%)

Tables use appropriate refresh patterns (Dynamic Tables, Tasks, Streams).

| Score | Condition |
|-------|-----------|
| 0-20 | Manual COPY INTO only |
| 21-40 | Scheduled tasks with basic CRON |
| 41-60 | Streams + tasks for CDC on key tables |
| 61-80 | Dynamic Tables for declarative pipelines |
| 81-100 | Full DAG of Dynamic Tables with target lag optimization |

**Snowflake Signals:**
- `DYNAMIC_TABLES` view
- `STREAMS` view
- `TASKS` view

---

### 4. Historical Data Availability (Weight: 20%)

Time Travel and Fail-safe ensure data recoverability and point-in-time access.

| Score | Condition |
|-------|-----------|
| 0-20 | Default 1-day retention, transient tables everywhere |
| 21-40 | Awareness of Time Travel, default settings |
| 41-60 | 14-day retention on critical tables |
| 61-80 | 90-day retention on production, replication for DR |
| 81-100 | Optimized retention per tier + cross-region replication + Fail-safe |

**Snowflake Signals:**
- `TABLE_STORAGE_METRICS` — retention_time
- `REPLICATION_GROUPS`
