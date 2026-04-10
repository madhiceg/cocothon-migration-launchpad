# Source System Migration Playbooks

## Oracle to Snowflake

### Complexity Drivers
- PL/SQL packages and standalone procedures (high conversion effort)
- Oracle-specific features: Advanced Queuing (AQ), DBMS_SCHEDULER, UTL_FILE, DBMS_LOB, XMLDB
- DB Links → Replace with Snowflake cross-database references or Data Sharing
- Materialized Views → Dynamic Tables or dbt incremental models
- Partitioning → Snowflake micro-partitions (automatic, no manual partitioning needed)
- RAC → Not needed; Snowflake handles concurrency natively with multi-cluster warehouses
- Synonyms → Snowflake does not support synonyms; use views or fully qualified names
- Sequences → Snowflake sequences or AUTOINCREMENT
- Triggers → Rewrite as Streams + Tasks or application-layer logic
- Oracle Text → Snowflake SEARCH OPTIMIZATION SERVICE or Cortex AI functions
- Flashback → Snowflake Time Travel (up to 90 days on Enterprise+)
- Data Guard → Snowflake Replication and Failover

### Migration Tools
- **SnowConvert AI**: Automated PL/SQL → Snowflake Scripting conversion. Handles ~70-80% of standard PL/SQL. Manual review needed for Oracle-specific features.
- **Data Loading**: Export via Oracle Data Pump → cloud storage → COPY INTO Snowflake
- **CDC**: Replace Oracle GoldenGate with Debezium (open-source) or Fivetran/Hevo CDC connectors
- **Large Tables**: Use parallel unload from Oracle with multiple threads → multiple files in S3/Azure Blob → parallel COPY INTO

### Common Pitfalls
- Oracle DATE includes time; Snowflake DATE does not. Map Oracle DATE → TIMESTAMP_NTZ.
- Oracle empty strings and NULLs are equivalent; Snowflake treats them differently.
- Oracle PL/SQL BULK COLLECT has no direct equivalent; use Snowflake Scripting RESULTSET.
- Oracle hierarchical queries (CONNECT BY) → Snowflake recursive CTEs.
- Oracle ROWNUM → Snowflake ROW_NUMBER() or LIMIT.
- Oracle NVL → Snowflake NVL or COALESCE (both supported).

---

## Teradata to Snowflake

### Complexity Drivers
- BTEQ scripts (batch SQL execution with conditional logic)
- FastLoad / MultiLoad / TPump (bulk and continuous loading utilities)
- Macros (parameterized SQL blocks)
- Teradata-specific SQL: QUALIFY, SAMPLE, NORMALIZE, EXPAND ON, temporal tables
- Join Indexes → No direct equivalent; use materialized views or Dynamic Tables
- Queue Tables → Streams + Tasks pattern
- Teradata Columnar → Snowflake is columnar by default
- COLLECT STATISTICS → Not needed; Snowflake uses automatic query optimization

### Migration Tools
- **SnowConvert AI**: BTEQ → SnowSQL/Snowflake Scripting, Teradata SQL → Snowflake SQL. Handles QUALIFY natively (Snowflake supports QUALIFY).
- **Data Loading**: Teradata Parallel Transporter (TPT) export → cloud storage → COPY INTO. For very large tables, use multiple TPT sessions.
- **FastLoad/MultiLoad replacement**: COPY INTO with parallel file loading
- **TPump replacement**: Snowpipe (continuous) or Snowpipe Streaming (real-time)

### Teradata SQL Compatibility
- QUALIFY: Natively supported in Snowflake (one of the few platforms that supports it)
- SAMPLE: Use TABLESAMPLE or random sampling
- NORMALIZE/EXPAND ON (temporal): Rewrite using window functions or Snowflake Scripting
- SEL (shorthand for SELECT): Not supported; use full SELECT
- TITLE clause: Not supported; use column aliases
- FORMAT clause: Not supported; handle in BI layer or with TO_CHAR
- Teradata date arithmetic (DATE + INTEGER): Use DATEADD function

### Common Pitfalls
- Teradata uses 1-based day-of-week; Snowflake uses 0-based by default (configurable via WEEK_START)
- Teradata CASESPECIFIC/NOT CASESPECIFIC: Snowflake is case-insensitive by default for comparisons; use COLLATE for case-sensitive
- Teradata PI (Primary Index) distribution: No equivalent needed; Snowflake auto-clusters
- Teradata VOLATILE tables → Snowflake TEMPORARY tables
- Teradata FALLBACK tables → Not needed; Snowflake handles replication natively

---

## SQL Server to Snowflake

### Complexity Drivers
- SSIS packages (complex ETL control flows with error handling)
- SSRS reports (need BI tool replacement)
- SSAS cubes/models (need analytical replacement)
- SQL Agent Jobs (scheduling)
- Linked Servers (cross-database queries)
- CLR Integration (custom .NET code in database)
- Service Broker (async messaging)
- Change Data Capture (CDC) / Change Tracking
- Temporal Tables (system-versioned)
- In-Memory OLTP (memory-optimized tables)

### Migration Tools
- **SnowConvert AI**: T-SQL → Snowflake SQL, stored procedures conversion
- **SSIS Replacement**: Do NOT attempt 1:1 conversion. Re-architect as:
  - Simple data flows → Snowflake COPY INTO + Tasks
  - Complex orchestration → Apache Airflow / Prefect DAGs
  - Transformation logic → dbt models
- **SSRS Replacement**: Sigma Computing, Tableau, Power BI, or Streamlit
- **SSAS Replacement**: Snowflake serves as the analytical engine; use BI tool for OLAP-style analysis
- **SQL Agent Jobs**: Snowflake Tasks or Airflow scheduler
- **CDC**: Snowflake Streams (for Snowflake-native CDC) or Debezium for source-side CDC from SQL Server

### T-SQL Compatibility
- Most T-SQL syntax works in Snowflake with minor adjustments
- TOP N → LIMIT N
- GETDATE() → CURRENT_TIMESTAMP()
- ISNULL() → NVL() or COALESCE()
- @@IDENTITY → Use sequences or AUTOINCREMENT
- CROSS APPLY / OUTER APPLY → LATERAL JOIN / LATERAL FLATTEN
- STRING_AGG → LISTAGG
- TRY_CONVERT → TRY_CAST
- MERGE: Supported in Snowflake with slightly different syntax

### Common Pitfalls
- SQL Server collation-dependent behavior: Snowflake uses UTF-8 by default
- SQL Server IDENTITY columns: Use AUTOINCREMENT or sequences in Snowflake
- Temp tables (#table): Use CREATE TEMPORARY TABLE (session-scoped)
- SQL Server XML operations: Use Snowflake's native semi-structured data handling (PARSE_XML, XMLGET)
- SQL Server PIVOT/UNPIVOT: Supported in Snowflake

---

## Amazon Redshift to Snowflake

### Complexity Drivers
- Redshift-specific SQL (DISTKEY, SORTKEY, DISTSTYLE)
- Redshift Spectrum (external tables querying S3)
- Redshift ML (machine learning models)
- Late-binding views
- Stored procedures (PL/pgSQL)
- User-defined functions (Python/SQL)
- Workload Management (WLM) queues

### Migration Tools
- **SnowConvert AI**: Redshift SQL → Snowflake SQL. Handles most syntax differences.
- **Data Loading**: UNLOAD from Redshift → S3 → COPY INTO Snowflake (most efficient path)
- **Redshift Spectrum replacement**: External Tables or Iceberg Tables in Snowflake

### Redshift SQL Compatibility
- DISTKEY/SORTKEY/DISTSTYLE: Remove entirely. Snowflake handles distribution and clustering automatically.
- ENCODE: Remove. Snowflake handles compression automatically.
- GETDATE() → CURRENT_TIMESTAMP()
- STRTOL() → No direct equivalent; use JavaScript UDF
- LISTAGG: Supported natively
- APPROXIMATE COUNT(DISTINCT) → APPROX_COUNT_DISTINCT
- SUPER type: Map to VARIANT

### Common Pitfalls
- Redshift vacuum/analyze: Not needed in Snowflake
- Redshift concurrency limitations (WLM slots): Snowflake multi-cluster warehouses handle this
- Redshift node types and sizing: Map to Snowflake warehouse T-shirt sizes based on workload

---

## Databricks to Snowflake

### Complexity Drivers
- Delta Tables (versioned, ACID tables on cloud storage)
- Notebooks (mix of Python, SQL, Scala)
- Unity Catalog (governance)
- MLflow (experiment tracking, model registry)
- Structured Streaming jobs
- Databricks Workflows/Jobs

### Migration Strategy
- **Delta Tables → Snowflake Tables**: Export as Parquet → COPY INTO, or use Iceberg Tables for interoperability
- **Notebooks → dbt models + Snowpark notebooks**: SQL logic → dbt models, Python logic → Snowpark
- **Unity Catalog → Snowflake Horizon**: Governance migration
- **MLflow → Snowflake Model Registry**: If using Snowpark ML
- **Structured Streaming → Snowpipe Streaming or Kafka Connector**
- **Workflows → Snowflake Tasks or Airflow**

### Common Pitfalls
- Databricks Delta format is not directly readable; export as Parquet or use delta-sharing
- Databricks notebooks with mixed SQL/Python: Split into dbt (SQL) and Snowpark (Python)
- Databricks cluster auto-scaling: Map to Snowflake multi-cluster warehouse auto-scaling
- Databricks DBU pricing unpredictability: Snowflake warehouse-based pricing is more predictable

---

## Google BigQuery to Snowflake

### Complexity Drivers
- BigQuery SQL dialect differences
- BigQuery ML models
- Scheduled queries
- BigQuery BI Engine (caching)
- Datasets (namespace concept)
- Streaming inserts
- BigQuery Omni (cross-cloud)

### Migration Tools
- **SnowConvert AI**: BigQuery SQL → Snowflake SQL
- **Data Loading**: BigQuery EXPORT → GCS → COPY INTO Snowflake (via external stage or cross-cloud replication)
- **Cross-cloud data transfer**: GCS → S3/Azure Blob transfer, then COPY INTO

### BigQuery SQL Compatibility
- STRUCT/ARRAY: Map to VARIANT/ARRAY in Snowflake
- UNNEST: Use FLATTEN in Snowflake
- SAFE_DIVIDE: Use DIV0 or TRY_TO_NUMBER
- FORMAT_TIMESTAMP: Use TO_CHAR
- PARTITION BY (table partitioning): Not needed; Snowflake auto-clusters
- BigQuery ML: Migrate to Snowpark ML or Cortex ML functions
- Scheduled queries: Snowflake Tasks

---

## MongoDB to Snowflake

### Migration Strategy
- MongoDB documents → Snowflake VARIANT columns or flattened relational tables
- Use MongoDB Atlas export → JSON files → cloud storage → COPY INTO with VARIANT
- For large collections, use `mongoexport` with `--type=json` → stage → COPY INTO
- Post-load flattening: Use FLATTEN + LATERAL to create relational views over VARIANT data

### Key Considerations
- Deeply nested documents: Decide between storing as VARIANT (flexible) vs flattening (performant for BI)
- Recommendation: Store raw in Bronze (VARIANT), flatten in Silver (relational)
- MongoDB ObjectId: Store as VARCHAR in Snowflake
- MongoDB date types: Map to TIMESTAMP_NTZ
- Embedded arrays: Use FLATTEN for analytical queries

---

## MySQL / PostgreSQL to Snowflake

### Migration Strategy
- Relatively straightforward SQL migration
- Use Airbyte, Fivetran, or Hevo for continuous sync
- For one-time migration: `pg_dump` / `mysqldump` → cloud storage → COPY INTO
- Most SQL syntax is compatible with minor adjustments

### Key Differences
- PostgreSQL JSONB → Snowflake VARIANT
- PostgreSQL array types → Snowflake ARRAY
- MySQL AUTO_INCREMENT → Snowflake AUTOINCREMENT
- PostgreSQL hstore → Snowflake OBJECT or VARIANT
- PostgreSQL ILIKE → Snowflake ILIKE (same)
- MySQL ENUM types → VARCHAR with CHECK constraints or reference tables
