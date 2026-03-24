-- =============================================================
-- AI READINESS ASSESSMENT: AI CONSUMPTION READINESS PROBES
-- =============================================================

-- PROBE 1: Cortex Function Usage (last 30 days)
SELECT
    'cortex_usage' AS metric,
    COUNT(*) AS query_count,
    COUNT(DISTINCT user_name) AS distinct_users
FROM snowflake.account_usage.query_history
WHERE query_text ILIKE '%SNOWFLAKE.CORTEX.%'
    AND start_time >= DATEADD(day, -30, CURRENT_TIMESTAMP());

-- PROBE 2: Cortex Function Breakdown
SELECT
    CASE
        WHEN query_text ILIKE '%CORTEX.COMPLETE%' THEN 'COMPLETE'
        WHEN query_text ILIKE '%CORTEX.SENTIMENT%' THEN 'SENTIMENT'
        WHEN query_text ILIKE '%CORTEX.SUMMARIZE%' THEN 'SUMMARIZE'
        WHEN query_text ILIKE '%CORTEX.TRANSLATE%' THEN 'TRANSLATE'
        WHEN query_text ILIKE '%CORTEX.EXTRACT%' THEN 'EXTRACT_ANSWER'
        WHEN query_text ILIKE '%CORTEX.EMBED%' THEN 'EMBED'
        WHEN query_text ILIKE '%CORTEX.CLASSIFY%' THEN 'CLASSIFY'
        WHEN query_text ILIKE '%CORTEX.PARSE_DOCUMENT%' THEN 'PARSE_DOCUMENT'
        ELSE 'OTHER_CORTEX'
    END AS cortex_function,
    COUNT(*) AS usage_count
FROM snowflake.account_usage.query_history
WHERE query_text ILIKE '%SNOWFLAKE.CORTEX.%'
    AND start_time >= DATEADD(day, -30, CURRENT_TIMESTAMP())
GROUP BY cortex_function
ORDER BY usage_count DESC;

-- PROBE 3: VECTOR Column Usage
SELECT
    table_catalog AS database_name,
    table_schema AS schema_name,
    table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE data_type ILIKE '%VECTOR%'
ORDER BY table_catalog, table_schema, table_name;

-- PROBE 4: ML Model Registry Objects
SELECT
    table_catalog AS database_name,
    table_schema AS schema_name,
    table_name,
    table_type,
    comment
FROM information_schema.tables
WHERE table_type = 'MODEL'
    OR (comment ILIKE '%model%' AND table_type IN ('VIEW', 'BASE TABLE'));

-- PROBE 5: Compute Pool Inventory (for ML workloads)
SELECT
    name AS compute_pool_name,
    state,
    min_nodes,
    max_nodes,
    instance_family,
    created_on
FROM snowflake.account_usage.compute_pools
WHERE deleted_on IS NULL;

-- PROBE 6: Snowpark Usage (ML library adoption signal)
SELECT
    'snowpark_queries' AS metric,
    COUNT(*) AS query_count
FROM snowflake.account_usage.query_history
WHERE client_application_id ILIKE '%Snowpark%'
    AND start_time >= DATEADD(day, -30, CURRENT_TIMESTAMP());
