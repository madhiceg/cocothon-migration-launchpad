-- =============================================================
-- AI READINESS ASSESSMENT: DATA GOVERNANCE PROBES
-- =============================================================

-- PROBE 1: Object Documentation Coverage
SELECT
    'table_comments' AS metric,
    COUNT(CASE WHEN comment IS NOT NULL AND comment != '' THEN 1 END) AS documented,
    COUNT(*) AS total,
    ROUND(COUNT(CASE WHEN comment IS NOT NULL AND comment != '' THEN 1 END) / NULLIF(COUNT(*), 0) * 100, 2) AS coverage_pct
FROM information_schema.tables
WHERE table_schema NOT IN ('INFORMATION_SCHEMA')
UNION ALL
SELECT
    'column_comments' AS metric,
    COUNT(CASE WHEN comment IS NOT NULL AND comment != '' THEN 1 END) AS documented,
    COUNT(*) AS total,
    ROUND(COUNT(CASE WHEN comment IS NOT NULL AND comment != '' THEN 1 END) / NULLIF(COUNT(*), 0) * 100, 2) AS coverage_pct
FROM information_schema.columns
WHERE table_schema NOT IN ('INFORMATION_SCHEMA');

-- PROBE 2: Tag Coverage
SELECT
    tag_database,
    tag_schema,
    tag_name,
    COUNT(*) AS tagged_objects
FROM snowflake.account_usage.tag_references
WHERE tag_database != 'SNOWFLAKE'
GROUP BY tag_database, tag_schema, tag_name
ORDER BY tagged_objects DESC;

-- PROBE 3: Masking Policy Coverage
SELECT
    'masking_policies' AS policy_type,
    COUNT(DISTINCT policy_name) AS policy_count,
    COUNT(*) AS total_attachments
FROM snowflake.account_usage.policy_references
WHERE policy_kind = 'MASKING_POLICY'
    AND deleted IS NULL
UNION ALL
SELECT
    'row_access_policies' AS policy_type,
    COUNT(DISTINCT policy_name) AS policy_count,
    COUNT(*) AS total_attachments
FROM snowflake.account_usage.policy_references
WHERE policy_kind = 'ROW_ACCESS_POLICY'
    AND deleted IS NULL;

-- PROBE 4: Classification Status
SELECT
    table_catalog AS database_name,
    table_schema AS schema_name,
    table_name,
    column_name,
    classification_result
FROM TABLE(
    snowflake.local.data_classification_latest()
)
LIMIT 100;

-- PROBE 5: Ownership Tag Coverage
SELECT
    COUNT(DISTINCT CONCAT(ref_entity_database, '.', ref_entity_schema, '.', ref_entity_name)) AS objects_with_ownership_tag,
    (SELECT COUNT(*) FROM snowflake.account_usage.tables WHERE deleted IS NULL) AS total_objects
FROM snowflake.account_usage.tag_references
WHERE LOWER(tag_name) IN ('owner', 'data_owner', 'steward', 'data_steward');
