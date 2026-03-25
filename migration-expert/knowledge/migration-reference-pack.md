# Snowflake Migration Reference Pack — Extracted Knowledge

**Source:** Snowflake_Migration_Reference_Pack.pdf (11 pages)  
**Extracted:** 2026-03-25  
**Purpose:** Pre-digested reference knowledge for migration-expert skill to eliminate runtime PDF parsing

---

## 1. Migration Methodology: 12-Step Framework

### Phase 1: Discovery & Assessment (Weeks 1-3)
1. **Inventory Source Systems** — Catalog all databases, schemas, tables, stored procedures, views, materialized views, ETL jobs, and scheduled tasks
2. **Profile Data** — Volume (TB), row counts, largest tables, growth rate, data types, encoding, compression
3. **Map Dependencies** — Application dependencies, upstream/downstream systems, SLA requirements, access patterns
4. **Assess Complexity** — Proprietary SQL functions, procedural code (PL/SQL, BTEQ, T-SQL), platform-specific features (OLAP functions, temporal tables, partitioning schemes)

### Phase 2: Architecture Design (Weeks 2-4)
5. **Design Target State** — Snowflake account structure, database/schema hierarchy, warehouse sizing strategy, RBAC model
6. **Select Tool Stack** — Ingestion, transformation, orchestration, BI, governance tools based on assessment data
7. **Define Data Architecture** — Medallion layers (Bronze/Silver/Gold), naming conventions, tagging strategy, data classification

### Phase 3: Build & Migrate (Weeks 4-12)
8. **Convert SQL/Code** — Translate source-specific SQL to Snowflake SQL (use SnowConvert for Oracle/Teradata), convert stored procedures to Snowflake Scripting or Snowpark
9. **Build Pipelines** — Implement ingestion (COPY INTO, Snowpipe, CDC), transformation (dbt models), orchestration (Tasks, Airflow)
10. **Migrate Data** — Historical bulk load, incremental sync, parallel load strategy for large tables

### Phase 4: Validate & Cutover (Weeks 10-16)
11. **Validate Data** — Row count reconciliation, checksum validation, statistical sampling, business rule validation, performance benchmarking
12. **Execute Cutover** — Parallel run period, application switchover, monitoring, rollback plan, go-live sign-off

---

## 2. Source System Migration Complexity Matrix

| Source System | SQL Complexity | Data Migration | ETL Rewrite | Typical Timeline | Risk Level |
|---------------|---------------|----------------|-------------|-----------------|------------|
| **Oracle** | High (PL/SQL, packages, types) | Medium (Oracle export tools mature) | High (complex ETL logic) | 12-20 weeks | High |
| **Teradata** | High (BTEQ, TPT, FastLoad) | High (massive volumes, multiset) | High (proprietary utilities) | 16-24 weeks | High |
| **SQL Server** | Medium (T-SQL is closest to Snowflake) | Low-Medium (BCP, SSIS export) | Medium (SSIS/ADF migration) | 8-14 weeks | Medium |
| **Redshift** | Low (PostgreSQL-based, similar SQL) | Medium (UNLOAD to S3, then COPY) | Low (most SQL translates directly) | 6-10 weeks | Low |
| **BigQuery** | Medium (StandardSQL differences, UDFs) | Medium (export to GCS, then COPY) | Medium (Dataflow/Composer migration) | 8-12 weeks | Medium |
| **Databricks** | Medium (Spark SQL, Delta Lake) | Medium (Delta to Iceberg, or export) | Medium-High (notebook migration) | 10-16 weeks | Medium |

### Key Conversion Challenges by Source
- **Oracle:** CONNECT BY → Recursive CTEs; DECODE → CASE; NVL → COALESCE/NVL; ROWNUM → ROW_NUMBER(); Sequences → Snowflake Sequences; PL/SQL packages → Snowflake Scripting + Snowpark
- **Teradata:** QUALIFY → Snowflake QUALIFY (native); BTEQ scripts → Snowflake SQL scripts; MultiSet tables → Standard tables; Teradata date functions → Snowflake equivalents; HASH BY → Snowflake clustering
- **SQL Server:** TOP → LIMIT; IDENTITY → AUTOINCREMENT; CROSS APPLY → LATERAL; Linked servers → External functions; SSRS → Sigma/Tableau/Streamlit
- **Redshift:** DISTKEY/SORTKEY → Clustering keys (optional); INTERLEAVED SORT → Search optimization; Spectrum → External tables; WLM → Warehouse resource monitors
- **BigQuery:** UNNEST → LATERAL FLATTEN; STRUCT → OBJECT/VARIANT; Partitioning → Automatic micro-partitions + clustering; BigQuery ML → Snowpark ML/Cortex

---

## 3. Data Validation Framework

### Level 1: Row Count Reconciliation
```sql
-- Source count (run on source system)
SELECT COUNT(*) FROM source_schema.table_name;

-- Target count (run on Snowflake)
SELECT COUNT(*) FROM target_db.target_schema.table_name;

-- Automated comparison
SELECT 
    'table_name' AS TABLE_NAME,
    source_count,
    target_count,
    CASE WHEN source_count = target_count THEN 'PASS' ELSE 'FAIL' END AS status,
    ABS(source_count - target_count) AS delta
FROM (SELECT <source_count> AS source_count, COUNT(*) AS target_count 
      FROM target_db.target_schema.table_name);
```

### Level 2: Aggregate Validation
```sql
-- Compare SUM, MIN, MAX, AVG for numeric columns
SELECT 
    SUM(amount) AS sum_check,
    MIN(amount) AS min_check,
    MAX(amount) AS max_check,
    AVG(amount) AS avg_check,
    COUNT(DISTINCT customer_id) AS distinct_check
FROM target_db.target_schema.orders;
```

### Level 3: Statistical Sampling
```sql
-- Random sample comparison (1% of rows)
SELECT * FROM target_db.target_schema.large_table
SAMPLE (1)
ORDER BY primary_key_column
LIMIT 1000;
```

### Level 4: Checksum Validation
```sql
-- Hash-based validation for critical tables
SELECT 
    MD5(ARRAY_TO_STRING(ARRAY_AGG(
        COALESCE(col1::VARCHAR,'') || '|' || 
        COALESCE(col2::VARCHAR,'') || '|' || 
        COALESCE(col3::VARCHAR,'')
    ORDER BY primary_key), ',')) AS table_checksum
FROM target_db.target_schema.critical_table;
```

---

## 4. Cost Estimation Framework

### Snowflake Credit Consumption by Warehouse Size

| Warehouse Size | Credits/Hour | Typical Use Case | Auto-suspend Recommendation |
|---------------|-------------|------------------|---------------------------|
| X-Small | 1 | Dev/test, light queries | 60 seconds |
| Small | 2 | Small team analytics, dbt dev | 120 seconds |
| Medium | 4 | Production dbt runs, moderate analytics | 120 seconds |
| Large | 8 | Heavy analytics, data science | 300 seconds |
| X-Large | 16 | Large ELT jobs, complex queries | 300 seconds |
| 2X-Large | 32 | Heavy production workloads | 300 seconds |
| 3X-Large | 64 | Peak processing, time-critical jobs | 600 seconds |
| 4X-Large | 128 | Massive data loading, urgent processing | 600 seconds |

### TCO Comparison Template
- **Legacy Annual Cost:** Hardware + licensing + DBA labor + facility + maintenance
- **Snowflake Annual Cost:** Compute credits + storage + data transfer + tooling licenses + reduced DBA effort
- **ROI Factors:** Reduced maintenance, faster time-to-insight, elastic scaling (no over-provisioning), reduced ETL complexity

### Resource Monitor Template
```sql
CREATE RESOURCE MONITOR migration_monitor
WITH 
    CREDIT_QUOTA = 1000
    FREQUENCY = MONTHLY
    START_TIMESTAMP = IMMEDIATELY
    TRIGGERS 
        ON 75 PERCENT DO NOTIFY
        ON 90 PERCENT DO NOTIFY
        ON 100 PERCENT DO SUSPEND;

ALTER WAREHOUSE compute_wh SET RESOURCE_MONITOR = migration_monitor;
```

---

## 5. Cutover Planning Template

### Pre-Cutover Checklist (T-minus 2 weeks)
- [ ] All data validation tests passing (Level 1-4)
- [ ] Performance benchmarks meeting or exceeding source system
- [ ] All ETL/ELT pipelines tested in production-equivalent environment
- [ ] RBAC roles and permissions validated against source system access
- [ ] Rollback procedure documented and tested
- [ ] Application connection strings updated in staging
- [ ] Monitoring and alerting configured (query history, warehouse utilization, error rates)
- [ ] Stakeholder sign-off on validation results

### Parallel Run Period (T-minus 1 week)
- [ ] Both source and target systems running simultaneously
- [ ] Data reconciliation running daily
- [ ] Applications reading from both systems for comparison
- [ ] Performance monitoring on both platforms
- [ ] Incident response team on standby

### Go-Live Day Checklist
- [ ] Final data sync completed
- [ ] Application switchover executed
- [ ] DNS/connection string cutover
- [ ] Source system set to read-only
- [ ] Monitoring dashboards active
- [ ] War room staffed for first 24 hours
- [ ] Rollback decision point defined (e.g., 4 hours post-cutover)

---

## 6. Risk Assessment Matrix

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| Data loss during migration | Low | Critical | Checksums at every stage, parallel run, source remains read-only until validation |
| SQL conversion errors | Medium | High | SnowConvert for automated conversion, comprehensive test suite, phased migration |
| Performance regression | Medium | High | Benchmark critical queries pre-migration, right-size warehouses, use query acceleration |
| ETL pipeline failures | Medium | Medium | Phased rollout, monitoring, retry logic, alerting |
| Scope creep | High | Medium | Locked scope document, change control process, phased approach |
| Skill gaps | Medium | Medium | Training plan, Snowflake University, kipi.ai SA support |
| Timeline overrun | High | Medium | Buffer weeks built into plan, milestone-based tracking, early risk escalation |
| Security/compliance gaps | Low | Critical | RBAC audit, data classification, encryption validation, compliance checklist |

---

## 7. Migration Success Metrics (KPIs)

### Technical KPIs
- **Data Accuracy:** 100% row count match, <0.01% variance on aggregate checks
- **Query Performance:** P50 and P95 query times meet or exceed source system
- **Pipeline Reliability:** >99.5% pipeline success rate in first 30 days
- **Data Freshness:** Latency targets met (batch: <1 hour, streaming: <5 minutes)

### Business KPIs
- **Time to Insight:** Reduction in report generation time
- **Operational Cost:** TCO reduction vs. legacy platform (target: 30-60%)
- **User Adoption:** % of analysts actively querying Snowflake within 30 days
- **Incident Rate:** <2 P1 incidents in first 30 days post-migration

---

## 8. Implementation Effort Estimation

| Phase | Duration | Team Size | Key Activities |
|-------|----------|-----------|---------------|
| Phase 1: Assessment | 2-3 weeks | 1-2 SA | Discovery, profiling, complexity analysis |
| Phase 2: Architecture | 2-3 weeks | 2 DE + 1 SA | Design, tool selection, environment setup |
| Phase 3: Foundation | 2-4 weeks | 2-3 DE | Snowflake setup, RBAC, networking, monitoring |
| Phase 4: Ingestion | 4-8 weeks | 2-3 DE | Pipeline build, historical load, CDC setup |
| Phase 5: Transformation | 4-8 weeks | 2-4 AE | dbt models, stored procedure conversion, testing |
| Phase 6: BI Migration | 2-4 weeks | 1-2 Analyst | Dashboard recreation, report validation, training |
| Phase 7: Validation | 2-3 weeks | Full team | Data validation, performance testing, UAT |
| Phase 8: Cutover | 1-2 weeks | Full team | Parallel run, go-live, hypercare |

**Total typical range:** 12-24 weeks depending on complexity, data volume, and number of source systems.

---

*Extracted from Snowflake_Migration_Reference_Pack.pdf for migration-expert skill knowledge base*
