-- =============================================================
-- AI READINESS ASSESSMENT: SECURITY & COMPLIANCE PROBES
-- =============================================================

-- PROBE 1: RBAC Analysis — Role usage patterns
SELECT
    r.name AS role_name,
    r.owner AS owned_by,
    COUNT(DISTINCT g.grantee_name) AS users_assigned,
    r.created_on
FROM snowflake.account_usage.roles r
LEFT JOIN snowflake.account_usage.grants_to_users g
    ON r.name = g.role
WHERE r.deleted_on IS NULL
GROUP BY r.name, r.owner, r.created_on
ORDER BY users_assigned DESC;

-- PROBE 2: ACCOUNTADMIN Usage — Who uses ACCOUNTADMIN and how often
SELECT
    user_name,
    role_name,
    COUNT(*) AS query_count,
    MAX(start_time) AS last_used
FROM snowflake.account_usage.query_history
WHERE role_name = 'ACCOUNTADMIN'
    AND start_time >= DATEADD(day, -30, CURRENT_TIMESTAMP())
GROUP BY user_name, role_name
ORDER BY query_count DESC;

-- PROBE 3: MFA Enrollment
SELECT
    COUNT(CASE WHEN ext_authn_duo = TRUE THEN 1 END) AS mfa_enrolled,
    COUNT(*) AS total_users,
    ROUND(COUNT(CASE WHEN ext_authn_duo = TRUE THEN 1 END) / NULLIF(COUNT(*), 0) * 100, 2) AS mfa_pct
FROM snowflake.account_usage.users
WHERE deleted_on IS NULL
    AND disabled = 'false';

-- PROBE 4: Network Policies
SELECT
    name AS policy_name,
    created_on,
    owner
FROM snowflake.account_usage.network_policies
WHERE deleted_on IS NULL;

-- PROBE 5: Masking Policy Attachments vs Classified Sensitive Columns
SELECT
    'classified_sensitive_columns' AS metric,
    COUNT(DISTINCT CONCAT(table_catalog, '.', table_schema, '.', table_name, '.', column_name)) AS count_val
FROM TABLE(snowflake.local.data_classification_latest())
UNION ALL
SELECT
    'masked_columns' AS metric,
    COUNT(DISTINCT CONCAT(ref_entity_database, '.', ref_entity_schema, '.', ref_entity_name, '.', ref_column_name)) AS count_val
FROM snowflake.account_usage.policy_references
WHERE policy_kind = 'MASKING_POLICY'
    AND deleted IS NULL;

-- PROBE 6: Password-Only Users (security risk)
SELECT
    name AS user_name,
    has_password,
    has_rsa_public_key,
    ext_authn_duo AS has_mfa,
    last_success_login,
    disabled
FROM snowflake.account_usage.users
WHERE deleted_on IS NULL
    AND disabled = 'false'
    AND has_password = TRUE
    AND has_rsa_public_key = FALSE
    AND ext_authn_duo = FALSE;
