-- =============================================================
-- AI READINESS ASSESSMENT: METADATA & LINEAGE PROBES
-- =============================================================

-- PROBE 1: Object Dependencies — DAG depth
SELECT
    referencing_database,
    referencing_schema,
    referencing_object_name,
    referencing_object_type,
    referenced_database,
    referenced_schema,
    referenced_object_name,
    referenced_object_type
FROM snowflake.account_usage.object_dependencies
ORDER BY referencing_database, referencing_schema;

-- PROBE 2: Documentation Coverage Summary
SELECT
    'databases' AS object_type,
    COUNT(CASE WHEN comment IS NOT NULL AND comment != '' THEN 1 END) AS documented,
    COUNT(*) AS total,
    ROUND(COUNT(CASE WHEN comment IS NOT NULL AND comment != '' THEN 1 END) / NULLIF(COUNT(*), 0) * 100, 2) AS pct
FROM snowflake.account_usage.databases
WHERE deleted IS NULL
UNION ALL
SELECT
    'schemas' AS object_type,
    COUNT(CASE WHEN comment IS NOT NULL AND comment != '' THEN 1 END) AS documented,
    COUNT(*) AS total,
    ROUND(COUNT(CASE WHEN comment IS NOT NULL AND comment != '' THEN 1 END) / NULLIF(COUNT(*), 0) * 100, 2) AS pct
FROM information_schema.schemata
WHERE schema_name NOT IN ('INFORMATION_SCHEMA')
UNION ALL
SELECT
    'tables' AS object_type,
    COUNT(CASE WHEN comment IS NOT NULL AND comment != '' THEN 1 END) AS documented,
    COUNT(*) AS total,
    ROUND(COUNT(CASE WHEN comment IS NOT NULL AND comment != '' THEN 1 END) / NULLIF(COUNT(*), 0) * 100, 2) AS pct
FROM information_schema.tables
WHERE table_schema NOT IN ('INFORMATION_SCHEMA');

-- PROBE 3: Custom Tags Inventory
SELECT
    tag_database,
    tag_schema,
    tag_name,
    tag_owner,
    COUNT(*) AS reference_count
FROM snowflake.account_usage.tag_references
GROUP BY tag_database, tag_schema, tag_name, tag_owner
ORDER BY reference_count DESC;

-- PROBE 4: Access History — Column-Level Lineage Availability
SELECT
    COUNT(*) AS lineage_records_30d
FROM snowflake.account_usage.access_history
WHERE query_start_time >= DATEADD(day, -30, CURRENT_TIMESTAMP())
    AND ARRAY_SIZE(base_objects_accessed) > 0;

-- PROBE 5: Git Integration Repositories
SELECT
    repository_name,
    created_on,
    owner
FROM snowflake.account_usage.git_repositories
WHERE deleted_on IS NULL;
