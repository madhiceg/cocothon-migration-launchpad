-- =============================================================
-- AI READINESS ASSESSMENT: DATA FRESHNESS PROBES
-- =============================================================

-- PROBE 1: Recent Load Activity — Tables loaded in the last 7 days
SELECT
    table_catalog_name AS database_name,
    table_schema_name AS schema_name,
    table_name,
    MAX(last_load_time) AS latest_load,
    DATEDIFF(hour, MAX(last_load_time), CURRENT_TIMESTAMP()) AS hours_since_last_load
FROM snowflake.account_usage.copy_history
WHERE last_load_time >= DATEADD(day, -30, CURRENT_TIMESTAMP())
GROUP BY table_catalog_name, table_schema_name, table_name
ORDER BY hours_since_last_load DESC;

-- PROBE 2: Dynamic Tables — Auto-refresh status
SELECT
    database_name,
    schema_name,
    name AS dynamic_table_name,
    target_lag,
    refresh_mode,
    scheduling_state
FROM snowflake.account_usage.dynamic_tables
WHERE deleted IS NULL
ORDER BY database_name, schema_name, name;

-- PROBE 3: Streams — Active change tracking
SELECT
    table_catalog AS database_name,
    table_schema AS schema_name,
    table_name AS stream_name,
    comment
FROM information_schema.tables
WHERE table_type = 'STREAM';

-- PROBE 4: Tasks — Scheduled pipeline inventory
SELECT
    database_name,
    schema_name,
    name AS task_name,
    schedule,
    state,
    owner,
    condition
FROM snowflake.account_usage.tasks
WHERE deleted_on IS NULL
ORDER BY state, database_name;

-- PROBE 5: Freshness DMF Coverage
SELECT
    COUNT(*) AS freshness_dmf_count
FROM TABLE(information_schema.data_metric_function_references())
WHERE metric_name ILIKE '%FRESHNESS%';

-- PROBE 6: Snowpipe Activity
SELECT
    pipe_catalog_name AS database_name,
    pipe_schema_name AS schema_name,
    pipe_name,
    COUNT(*) AS files_loaded_30d,
    MAX(last_load_time) AS last_activity
FROM snowflake.account_usage.copy_history
WHERE pipe_catalog_name IS NOT NULL
    AND last_load_time >= DATEADD(day, -30, CURRENT_TIMESTAMP())
GROUP BY pipe_catalog_name, pipe_schema_name, pipe_name
ORDER BY last_activity DESC;
