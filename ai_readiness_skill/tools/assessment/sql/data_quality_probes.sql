-- =============================================================
-- AI READINESS ASSESSMENT: DATA QUALITY PROBES
-- Run these queries to collect signals for Data Quality scoring
-- =============================================================

-- PROBE 1: Completeness — Null rate across all columns in all tables
-- Returns: table_name, column_name, total_rows, null_count, null_pct
SELECT
    t.table_catalog AS database_name,
    t.table_schema AS schema_name,
    t.table_name,
    t.row_count AS total_rows,
    SUM(CASE WHEN c.is_nullable = 'YES' THEN 1 ELSE 0 END) AS nullable_column_count,
    COUNT(c.column_name) AS total_columns,
    ROUND(SUM(CASE WHEN c.is_nullable = 'YES' THEN 1 ELSE 0 END) / NULLIF(COUNT(c.column_name), 0) * 100, 2) AS nullable_pct
FROM information_schema.tables t
JOIN information_schema.columns c
    ON t.table_catalog = c.table_catalog
    AND t.table_schema = c.table_schema
    AND t.table_name = c.table_name
WHERE t.table_schema NOT IN ('INFORMATION_SCHEMA')
    AND t.table_type = 'BASE TABLE'
GROUP BY t.table_catalog, t.table_schema, t.table_name, t.row_count
ORDER BY nullable_pct DESC;

-- PROBE 2: DMF Coverage — Tables with Data Metric Functions assigned
SELECT
    COUNT(DISTINCT ref.ref_entity_name) AS tables_with_dmf,
    (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema NOT IN ('INFORMATION_SCHEMA') AND table_type = 'BASE TABLE') AS total_tables,
    ROUND(COUNT(DISTINCT ref.ref_entity_name) /
        NULLIF((SELECT COUNT(*) FROM information_schema.tables WHERE table_schema NOT IN ('INFORMATION_SCHEMA') AND table_type = 'BASE TABLE'), 0) * 100, 2) AS dmf_coverage_pct
FROM TABLE(information_schema.data_metric_function_references()) ref;

-- PROBE 3: Constraint Coverage — Tables with primary keys and foreign keys
SELECT
    COUNT(DISTINCT tc.table_name) AS tables_with_constraints,
    (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema NOT IN ('INFORMATION_SCHEMA') AND table_type = 'BASE TABLE') AS total_tables,
    ROUND(COUNT(DISTINCT tc.table_name) /
        NULLIF((SELECT COUNT(*) FROM information_schema.tables WHERE table_schema NOT IN ('INFORMATION_SCHEMA') AND table_type = 'BASE TABLE'), 0) * 100, 2) AS constraint_coverage_pct
FROM information_schema.table_constraints tc
WHERE tc.constraint_type IN ('PRIMARY KEY', 'FOREIGN KEY', 'UNIQUE');

-- PROBE 4: Duplicate Detection Readiness
SELECT
    'duplicate_dmf_deployed' AS check_name,
    COUNT(*) AS count
FROM TABLE(information_schema.data_metric_function_references())
WHERE metric_name ILIKE '%DUPLICATE%' OR metric_name ILIKE '%UNIQUE%';
