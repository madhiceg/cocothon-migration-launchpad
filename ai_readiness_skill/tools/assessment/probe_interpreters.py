def interpret_data_quality_probes(nullable_pct, dmf_coverage_pct, constraint_coverage_pct, duplicate_dmf_count):
    scores = {}

    if nullable_pct is not None:
        if nullable_pct > 70:
            scores["completeness"] = 20
        elif nullable_pct > 50:
            scores["completeness"] = 40
        elif nullable_pct > 30:
            scores["completeness"] = 60
        elif nullable_pct > 10:
            scores["completeness"] = 80
        else:
            scores["completeness"] = 95

    if constraint_coverage_pct is not None:
        if constraint_coverage_pct < 5:
            scores["accuracy"] = 15
        elif constraint_coverage_pct < 25:
            scores["accuracy"] = 35
        elif constraint_coverage_pct < 50:
            scores["accuracy"] = 55
        elif constraint_coverage_pct < 75:
            scores["accuracy"] = 75
        else:
            scores["accuracy"] = 90

    if duplicate_dmf_count is not None:
        if duplicate_dmf_count == 0:
            scores["consistency"] = 20
        elif duplicate_dmf_count < 5:
            scores["consistency"] = 50
        elif duplicate_dmf_count < 20:
            scores["consistency"] = 75
        else:
            scores["consistency"] = 90

    scores["validity"] = min(scores.get("accuracy", 50), scores.get("consistency", 50))

    if dmf_coverage_pct is not None:
        if dmf_coverage_pct < 5:
            scores["timeliness_quality"] = 10
        elif dmf_coverage_pct < 25:
            scores["timeliness_quality"] = 30
        elif dmf_coverage_pct < 50:
            scores["timeliness_quality"] = 55
        elif dmf_coverage_pct < 80:
            scores["timeliness_quality"] = 75
        else:
            scores["timeliness_quality"] = 95

    return scores


def interpret_governance_probes(table_comment_pct, column_comment_pct, tag_count, policy_count, classification_count, ownership_pct):
    scores = {}

    if ownership_pct is not None:
        if ownership_pct < 5:
            scores["ownership"] = 10
        elif ownership_pct < 25:
            scores["ownership"] = 30
        elif ownership_pct < 60:
            scores["ownership"] = 55
        elif ownership_pct < 85:
            scores["ownership"] = 75
        else:
            scores["ownership"] = 95

    avg_doc = ((table_comment_pct or 0) + (column_comment_pct or 0)) / 2
    if avg_doc < 10:
        scores["cataloging"] = 10
    elif avg_doc < 30:
        scores["cataloging"] = 30
    elif avg_doc < 50:
        scores["cataloging"] = 55
    elif avg_doc < 75:
        scores["cataloging"] = 75
    else:
        scores["cataloging"] = 90

    if policy_count is not None:
        if policy_count == 0:
            scores["policy_coverage"] = 10
        elif policy_count < 5:
            scores["policy_coverage"] = 35
        elif policy_count < 15:
            scores["policy_coverage"] = 55
        elif policy_count < 30:
            scores["policy_coverage"] = 75
        else:
            scores["policy_coverage"] = 90

    if classification_count is not None:
        if classification_count == 0:
            scores["classification"] = 10
        elif classification_count < 20:
            scores["classification"] = 35
        elif classification_count < 50:
            scores["classification"] = 55
        elif classification_count < 100:
            scores["classification"] = 75
        else:
            scores["classification"] = 90

    scores["access_audit"] = 50

    return scores


def interpret_security_probes(accountadmin_users, mfa_pct, network_policy_count, masked_vs_classified, password_only_users):
    scores = {}

    if accountadmin_users is not None:
        if accountadmin_users > 10:
            scores["rbac_maturity"] = 15
        elif accountadmin_users > 5:
            scores["rbac_maturity"] = 30
        elif accountadmin_users > 2:
            scores["rbac_maturity"] = 55
        elif accountadmin_users > 0:
            scores["rbac_maturity"] = 75
        else:
            scores["rbac_maturity"] = 90

    scores["encryption"] = 50

    if network_policy_count is not None:
        if network_policy_count == 0:
            scores["network_security"] = 10
        elif network_policy_count < 3:
            scores["network_security"] = 40
        else:
            scores["network_security"] = 70

    if mfa_pct is not None:
        if mfa_pct < 10:
            scores["mfa_auth"] = 10
        elif mfa_pct < 30:
            scores["mfa_auth"] = 30
        elif mfa_pct < 60:
            scores["mfa_auth"] = 50
        elif mfa_pct < 90:
            scores["mfa_auth"] = 75
        else:
            scores["mfa_auth"] = 95

    scores["compliance_posture"] = min(
        scores.get("rbac_maturity", 50),
        scores.get("mfa_auth", 50)
    )

    if masked_vs_classified is not None:
        ratio = masked_vs_classified
        if ratio < 0.1:
            scores["data_masking"] = 10
        elif ratio < 0.3:
            scores["data_masking"] = 35
        elif ratio < 0.6:
            scores["data_masking"] = 55
        elif ratio < 0.85:
            scores["data_masking"] = 75
        else:
            scores["data_masking"] = 90

    return scores


def interpret_freshness_probes(avg_hours_since_load, dynamic_table_count, stream_count, task_count, freshness_dmf_count, pipe_count):
    scores = {}

    if avg_hours_since_load is not None:
        if avg_hours_since_load > 168:
            scores["pipeline_latency"] = 15
        elif avg_hours_since_load > 48:
            scores["pipeline_latency"] = 30
        elif avg_hours_since_load > 12:
            scores["pipeline_latency"] = 55
        elif avg_hours_since_load > 1:
            scores["pipeline_latency"] = 75
        else:
            scores["pipeline_latency"] = 95

    if freshness_dmf_count is not None:
        if freshness_dmf_count == 0:
            scores["staleness_detection"] = 10
        elif freshness_dmf_count < 5:
            scores["staleness_detection"] = 40
        elif freshness_dmf_count < 20:
            scores["staleness_detection"] = 65
        else:
            scores["staleness_detection"] = 85

    total_modern = (dynamic_table_count or 0) + (stream_count or 0) + (pipe_count or 0)
    if total_modern == 0 and (task_count or 0) == 0:
        scores["refresh_strategy"] = 15
    elif total_modern == 0:
        scores["refresh_strategy"] = 35
    elif (dynamic_table_count or 0) > 0:
        scores["refresh_strategy"] = 70
    else:
        scores["refresh_strategy"] = 55

    scores["historical_availability"] = 50

    return scores


def interpret_metadata_probes(doc_coverage_pct, tag_reference_count, lineage_records, git_repo_count):
    scores = {}

    if lineage_records is not None:
        if lineage_records == 0:
            scores["column_lineage"] = 10
        elif lineage_records < 100:
            scores["column_lineage"] = 35
        elif lineage_records < 10000:
            scores["column_lineage"] = 60
        else:
            scores["column_lineage"] = 80

    if doc_coverage_pct is not None:
        if doc_coverage_pct < 10:
            scores["documentation"] = 10
        elif doc_coverage_pct < 30:
            scores["documentation"] = 30
        elif doc_coverage_pct < 50:
            scores["documentation"] = 55
        elif doc_coverage_pct < 75:
            scores["documentation"] = 75
        else:
            scores["documentation"] = 90

    if tag_reference_count is not None:
        if tag_reference_count == 0:
            scores["tagging_coverage"] = 10
        elif tag_reference_count < 10:
            scores["tagging_coverage"] = 30
        elif tag_reference_count < 50:
            scores["tagging_coverage"] = 55
        elif tag_reference_count < 200:
            scores["tagging_coverage"] = 75
        else:
            scores["tagging_coverage"] = 90

    scores["impact_analysis"] = scores.get("column_lineage", 40)

    if git_repo_count is not None:
        if git_repo_count == 0:
            scores["schema_evolution"] = 15
        elif git_repo_count < 3:
            scores["schema_evolution"] = 50
        else:
            scores["schema_evolution"] = 75

    return scores


def interpret_ai_consumption_probes(cortex_query_count, cortex_user_count, vector_column_count, model_count, compute_pool_count, snowpark_query_count):
    scores = {}

    if (cortex_query_count or 0) == 0 and (snowpark_query_count or 0) == 0:
        scores["feature_engineering"] = 10
    elif (cortex_query_count or 0) < 10:
        scores["feature_engineering"] = 30
    elif (cortex_query_count or 0) < 100:
        scores["feature_engineering"] = 55
    else:
        scores["feature_engineering"] = 75

    if vector_column_count is not None:
        if vector_column_count == 0:
            scores["vector_readiness"] = 10
        elif vector_column_count < 5:
            scores["vector_readiness"] = 45
        elif vector_column_count < 20:
            scores["vector_readiness"] = 70
        else:
            scores["vector_readiness"] = 90

    if cortex_query_count is not None:
        if cortex_query_count == 0:
            scores["cortex_integration"] = 10
        elif cortex_query_count < 10:
            scores["cortex_integration"] = 30
        elif cortex_query_count < 100:
            scores["cortex_integration"] = 55
        elif cortex_query_count < 500:
            scores["cortex_integration"] = 75
        else:
            scores["cortex_integration"] = 90

    if model_count is not None:
        if model_count == 0:
            scores["ml_model_registry"] = 10
        elif model_count < 3:
            scores["ml_model_registry"] = 40
        elif model_count < 10:
            scores["ml_model_registry"] = 65
        else:
            scores["ml_model_registry"] = 85

    scores["data_schema_ml_friendly"] = max(
        scores.get("feature_engineering", 30),
        scores.get("vector_readiness", 30)
    )

    return scores


def interpret_infrastructure_probes(warehouse_count, avg_auto_suspend, has_multi_cluster, resource_monitor_count, compute_pool_count, has_search_opt):
    scores = {}

    if warehouse_count is not None:
        if warehouse_count <= 1:
            scores["warehouse_optimization"] = 20
        elif (avg_auto_suspend or 600) > 600:
            scores["warehouse_optimization"] = 35
        elif has_multi_cluster:
            scores["warehouse_optimization"] = 75
        else:
            scores["warehouse_optimization"] = 55

    if resource_monitor_count is not None:
        if resource_monitor_count == 0:
            scores["cost_governance"] = 10
        elif resource_monitor_count < 3:
            scores["cost_governance"] = 40
        elif resource_monitor_count < 10:
            scores["cost_governance"] = 65
        else:
            scores["cost_governance"] = 85

    if compute_pool_count is not None:
        if compute_pool_count == 0:
            scores["compute_pools"] = 15
        elif compute_pool_count < 3:
            scores["compute_pools"] = 50
        else:
            scores["compute_pools"] = 80

    if has_search_opt:
        scores["storage_optimization"] = 65
    else:
        scores["storage_optimization"] = 35

    return scores
