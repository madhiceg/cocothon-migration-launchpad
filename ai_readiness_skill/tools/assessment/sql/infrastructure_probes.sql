-- =============================================================
-- AI READINESS ASSESSMENT: INFRASTRUCTURE & SCALABILITY PROBES
-- =============================================================

-- PROBE 1: Warehouse Inventory & Configuration
SELECT
    name AS warehouse_name,
    size,
    min_cluster_count,
    max_cluster_count,
    auto_suspend,
    auto_resume,
    scaling_policy,
    enable_query_acceleration,
    resource_monitor,
    owner
FROM snowflake.account_usage.warehouses
WHERE deleted IS NULL
ORDER BY name;

-- PROBE 2: Warehouse Utilization (last 30 days)
SELECT
    warehouse_name,
    SUM(credits_used) AS total_credits_30d,
    COUNT(DISTINCT DATE(start_time)) AS active_days,
    ROUND(SUM(credits_used) / NULLIF(COUNT(DISTINCT DATE(start_time)), 0), 2) AS avg_daily_credits
FROM snowflake.account_usage.warehouse_metering_history
WHERE start_time >= DATEADD(day, -30, CURRENT_TIMESTAMP())
GROUP BY warehouse_name
ORDER BY total_credits_30d DESC;

-- PROBE 3: Resource Monitors
SELECT
    name AS monitor_name,
    credit_quota,
    frequency,
    notify_at,
    suspend_at,
    suspend_immediately_at,
    created_on
FROM snowflake.account_usage.resource_monitors;

-- PROBE 4: Storage Metrics — Clustering & Optimization
SELECT
    table_catalog AS database_name,
    table_schema AS schema_name,
    table_name,
    active_bytes,
    time_travel_bytes,
    failsafe_bytes,
    retained_for_clone_bytes,
    is_transient
FROM snowflake.account_usage.table_storage_metrics
WHERE active_bytes > 0
    AND table_dropped IS NULL
ORDER BY active_bytes DESC
LIMIT 50;

-- PROBE 5: Search Optimization Status
SELECT
    table_catalog AS database_name,
    table_schema AS schema_name,
    table_name,
    search_optimization,
    search_optimization_bytes
FROM information_schema.tables
WHERE search_optimization = 'ON';

-- PROBE 6: Credit Consumption by Service Type
SELECT
    service_type,
    SUM(credits_used) AS total_credits_30d
FROM snowflake.account_usage.metering_daily_history
WHERE usage_date >= DATEADD(day, -30, CURRENT_DATE())
GROUP BY service_type
ORDER BY total_credits_30d DESC;
