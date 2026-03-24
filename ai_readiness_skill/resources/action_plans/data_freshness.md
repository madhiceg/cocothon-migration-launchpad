# Action Plan: Data Freshness

## Foundational (Score 0-25)

### ACTION: Deploy FRESHNESS DMFs on Production Tables
- **Effort:** Low | **Impact:** High | **Timeline:** Week 1
- Attach `SNOWFLAKE.CORE.FRESHNESS` DMF to critical tables. Define expected freshness SLAs.
- **SQL Template:** `tools/action_plan/sql/deploy_freshness_dmf.sql`

### ACTION: Inventory All Data Pipelines and Document SLAs
- **Effort:** Medium | **Impact:** Medium | **Timeline:** Week 1-2
- Catalog all COPY INTO, Snowpipe, and Task-based pipelines. Define target latency per table tier.

---

## Developing (Score 26-50)

### ACTION: Migrate Batch Loads to Snowpipe or Snowpipe Streaming
- **Effort:** High | **Impact:** High | **Timeline:** Week 2-4
- Convert daily COPY INTO patterns to continuous Snowpipe for real-time ingestion.

### ACTION: Adopt Dynamic Tables for Transformation Layers
- **Effort:** Medium | **Impact:** High | **Timeline:** Week 3-5
- Replace scheduled Task+CTAS patterns with Dynamic Tables using `target_lag` for declarative freshness.
- **SQL Template:** `tools/action_plan/sql/migrate_to_dynamic_tables.sql`

---

## Advancing (Score 51-75)

### ACTION: Build End-to-End Freshness Monitoring with Alerting
- **Effort:** Medium | **Impact:** High | **Timeline:** Week 4-6
- Combine DMF results with Alert objects to send notifications when freshness SLAs are breached.
