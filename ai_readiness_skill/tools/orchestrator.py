"""
AI Readiness Advisor — Orchestrator
Runs the full assessment pipeline: probes -> scoring -> action plan.
Designed to be invoked from a Snowflake Notebook or Streamlit app.
"""

def run_assessment(session):
    from tools.assessment.scoring_engine import score_from_probe_results, format_report
    from tools.assessment.probe_interpreters import (
        interpret_data_quality_probes,
        interpret_governance_probes,
        interpret_security_probes,
        interpret_freshness_probes,
        interpret_metadata_probes,
        interpret_ai_consumption_probes,
        interpret_infrastructure_probes,
    )
    from tools.action_plan.plan_generator import generate_action_plan, generate_executive_summary

    probe_results = {}

    print("=" * 70)
    print("  AI READINESS ADVISOR — Running Assessment")
    print("=" * 70)
    print()

    # --- Data Quality ---
    print("  [1/8] Assessing Data Quality...")
    try:
        nullable_df = session.sql("""
            SELECT
                ROUND(AVG(CASE WHEN c.is_nullable = 'YES' THEN 1 ELSE 0 END) * 100, 2) AS avg_nullable_pct
            FROM information_schema.columns c
            JOIN information_schema.tables t
                ON c.table_catalog = t.table_catalog
                AND c.table_schema = t.table_schema
                AND c.table_name = t.table_name
            WHERE t.table_schema NOT IN ('INFORMATION_SCHEMA')
                AND t.table_type = 'BASE TABLE'
        """).collect()
        nullable_pct = float(nullable_df[0]["AVG_NULLABLE_PCT"]) if nullable_df else 50

        dmf_coverage = 0
        constraint_pct = 0
        dup_dmf = 0

        probe_results["data_quality"] = interpret_data_quality_probes(
            nullable_pct, dmf_coverage, constraint_pct, dup_dmf
        )
    except Exception as e:
        print(f"    Warning: Data quality probe error — {e}")
        probe_results["data_quality"] = {"completeness": 30, "accuracy": 30, "consistency": 30, "validity": 30, "timeliness_quality": 10}

    # --- Data Governance ---
    print("  [2/8] Assessing Data Governance...")
    try:
        doc_df = session.sql("""
            SELECT
                ROUND(COUNT(CASE WHEN comment IS NOT NULL AND comment != '' THEN 1 END) / NULLIF(COUNT(*), 0) * 100, 2) AS tbl_pct
            FROM information_schema.tables
            WHERE table_schema NOT IN ('INFORMATION_SCHEMA')
        """).collect()
        tbl_pct = float(doc_df[0]["TBL_PCT"]) if doc_df else 0

        col_df = session.sql("""
            SELECT
                ROUND(COUNT(CASE WHEN comment IS NOT NULL AND comment != '' THEN 1 END) / NULLIF(COUNT(*), 0) * 100, 2) AS col_pct
            FROM information_schema.columns
            WHERE table_schema NOT IN ('INFORMATION_SCHEMA')
        """).collect()
        col_pct = float(col_df[0]["COL_PCT"]) if col_df else 0

        tag_df = session.sql("""
            SELECT COUNT(*) AS cnt FROM snowflake.account_usage.tag_references WHERE tag_database != 'SNOWFLAKE'
        """).collect()
        tag_count = int(tag_df[0]["CNT"]) if tag_df else 0

        policy_df = session.sql("""
            SELECT COUNT(DISTINCT policy_name) AS cnt
            FROM snowflake.account_usage.policy_references WHERE policy_kind = 'MASKING_POLICY' AND deleted IS NULL
        """).collect()
        policy_count = int(policy_df[0]["CNT"]) if policy_df else 0

        probe_results["data_governance"] = interpret_governance_probes(
            tbl_pct, col_pct, tag_count, policy_count, 0, 0
        )
    except Exception as e:
        print(f"    Warning: Governance probe error — {e}")
        probe_results["data_governance"] = {"ownership": 20, "cataloging": 20, "policy_coverage": 20, "classification": 20, "access_audit": 30}

    # --- Security & Compliance ---
    print("  [3/8] Assessing Security & Compliance...")
    try:
        admin_df = session.sql("""
            SELECT COUNT(DISTINCT user_name) AS cnt
            FROM snowflake.account_usage.query_history
            WHERE role_name = 'ACCOUNTADMIN' AND start_time >= DATEADD(day, -30, CURRENT_TIMESTAMP())
        """).collect()
        admin_users = int(admin_df[0]["CNT"]) if admin_df else 0

        mfa_df = session.sql("""
            SELECT
                ROUND(COUNT(CASE WHEN ext_authn_duo = TRUE THEN 1 END) / NULLIF(COUNT(*), 0) * 100, 2) AS mfa_pct
            FROM snowflake.account_usage.users WHERE deleted_on IS NULL AND disabled = 'false'
        """).collect()
        mfa_pct = float(mfa_df[0]["MFA_PCT"]) if mfa_df else 0

        net_df = session.sql("""
            SELECT COUNT(*) AS cnt FROM snowflake.account_usage.network_policies WHERE deleted_on IS NULL
        """).collect()
        net_count = int(net_df[0]["CNT"]) if net_df else 0

        probe_results["security_compliance"] = interpret_security_probes(
            admin_users, mfa_pct, net_count, 0.0, 0
        )
    except Exception as e:
        print(f"    Warning: Security probe error — {e}")
        probe_results["security_compliance"] = {"rbac_maturity": 30, "encryption": 50, "network_security": 20, "mfa_auth": 20, "compliance_posture": 20, "data_masking": 10}

    # --- Data Freshness ---
    print("  [4/8] Assessing Data Freshness...")
    try:
        dt_df = session.sql("""
            SELECT COUNT(*) AS cnt FROM snowflake.account_usage.dynamic_tables WHERE deleted IS NULL
        """).collect()
        dt_count = int(dt_df[0]["CNT"]) if dt_df else 0

        task_df = session.sql("""
            SELECT COUNT(*) AS cnt FROM snowflake.account_usage.tasks WHERE deleted_on IS NULL AND state = 'started'
        """).collect()
        task_count = int(task_df[0]["CNT"]) if task_df else 0

        probe_results["data_freshness"] = interpret_freshness_probes(
            24, dt_count, 0, task_count, 0, 0
        )
    except Exception as e:
        print(f"    Warning: Freshness probe error — {e}")
        probe_results["data_freshness"] = {"pipeline_latency": 30, "staleness_detection": 10, "refresh_strategy": 20, "historical_availability": 50}

    # --- Metadata & Lineage ---
    print("  [5/8] Assessing Metadata & Lineage...")
    try:
        lineage_df = session.sql("""
            SELECT COUNT(*) AS cnt FROM snowflake.account_usage.access_history
            WHERE query_start_time >= DATEADD(day, -30, CURRENT_TIMESTAMP()) AND ARRAY_SIZE(base_objects_accessed) > 0
        """).collect()
        lineage_count = int(lineage_df[0]["CNT"]) if lineage_df else 0

        avg_doc = (tbl_pct + col_pct) / 2 if 'tbl_pct' in dir() else 10

        probe_results["metadata_lineage"] = interpret_metadata_probes(
            avg_doc, tag_count if 'tag_count' in dir() else 0, lineage_count, 0
        )
    except Exception as e:
        print(f"    Warning: Metadata probe error — {e}")
        probe_results["metadata_lineage"] = {"column_lineage": 30, "documentation": 20, "tagging_coverage": 10, "impact_analysis": 20, "schema_evolution": 15}

    # --- AI Consumption ---
    print("  [6/8] Assessing AI Consumption Readiness...")
    try:
        cortex_df = session.sql("""
            SELECT COUNT(*) AS cnt, COUNT(DISTINCT user_name) AS users
            FROM snowflake.account_usage.query_history
            WHERE query_text ILIKE '%SNOWFLAKE.CORTEX.%' AND start_time >= DATEADD(day, -30, CURRENT_TIMESTAMP())
        """).collect()
        cortex_count = int(cortex_df[0]["CNT"]) if cortex_df else 0
        cortex_users = int(cortex_df[0]["USERS"]) if cortex_df else 0

        snowpark_df = session.sql("""
            SELECT COUNT(*) AS cnt FROM snowflake.account_usage.query_history
            WHERE client_application_id ILIKE '%Snowpark%' AND start_time >= DATEADD(day, -30, CURRENT_TIMESTAMP())
        """).collect()
        snowpark_count = int(snowpark_df[0]["CNT"]) if snowpark_df else 0

        probe_results["ai_consumption_readiness"] = interpret_ai_consumption_probes(
            cortex_count, cortex_users, 0, 0, 0, snowpark_count
        )
    except Exception as e:
        print(f"    Warning: AI consumption probe error — {e}")
        probe_results["ai_consumption_readiness"] = {"feature_engineering": 10, "vector_readiness": 10, "cortex_integration": 10, "ml_model_registry": 10, "data_schema_ml_friendly": 10}

    # --- Infrastructure ---
    print("  [7/8] Assessing Infrastructure & Scalability...")
    try:
        wh_df = session.sql("""
            SELECT COUNT(*) AS cnt, AVG(auto_suspend) AS avg_suspend
            FROM snowflake.account_usage.warehouses WHERE deleted IS NULL
        """).collect()
        wh_count = int(wh_df[0]["CNT"]) if wh_df else 1
        avg_suspend = float(wh_df[0]["AVG_SUSPEND"]) if wh_df and wh_df[0]["AVG_SUSPEND"] else 600

        rm_df = session.sql("""
            SELECT COUNT(*) AS cnt FROM snowflake.account_usage.resource_monitors
        """).collect()
        rm_count = int(rm_df[0]["CNT"]) if rm_df else 0

        probe_results["infrastructure_scalability"] = interpret_infrastructure_probes(
            wh_count, avg_suspend, False, rm_count, 0, False
        )
    except Exception as e:
        print(f"    Warning: Infrastructure probe error — {e}")
        probe_results["infrastructure_scalability"] = {"warehouse_optimization": 35, "cost_governance": 20, "compute_pools": 15, "storage_optimization": 35}

    # --- Organizational (survey-based, defaults) ---
    print("  [8/8] Organizational Readiness (survey-based defaults)...")
    probe_results["organizational_readiness"] = {
        "ai_literacy": 40,
        "mlops_culture": 30,
        "cross_functional": 35,
        "ai_strategy": 30,
    }

    # --- Compute Scores ---
    print()
    print("  Computing scores...")
    report = score_from_probe_results(probe_results)

    score_report = format_report(report)
    print(score_report)

    # --- Generate Action Plan ---
    print()
    action_plan = generate_action_plan(report)
    print(action_plan)

    # --- Executive Summary ---
    print()
    exec_summary = generate_executive_summary(report)
    print(exec_summary)

    return {
        "report": report,
        "score_text": score_report,
        "action_plan_text": action_plan,
        "executive_summary": exec_summary,
    }


if __name__ == "__main__":
    print("AI Readiness Advisor")
    print("This module requires a Snowpark session. Run from a Snowflake Notebook.")
    print()
    print("Usage:")
    print("  from tools.orchestrator import run_assessment")
    print("  results = run_assessment(session)")
