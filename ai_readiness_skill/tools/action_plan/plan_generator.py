from tools.assessment.scoring_engine import AIReadinessReport, get_band

REMEDIATION_PLAYBOOKS = {
    "data_quality": {
        "dimension_name": "Data Quality",
        "priority_actions": {
            "foundational": [
                {
                    "action": "Deploy system DMFs on all production tables",
                    "reference": "resources/action_plans/data_quality.md",
                    "effort": "Medium",
                    "impact": "High",
                    "timeline": "Week 1-2",
                    "details": "Attach SNOWFLAKE.CORE.NULL_COUNT, DUPLICATE_COUNT, and FRESHNESS to every production table. Start with the top-20 most queried tables from QUERY_HISTORY.",
                },
                {
                    "action": "Add NOT NULL and PRIMARY KEY constraints",
                    "reference": "resources/templates/constraints.md",
                    "effort": "Low",
                    "impact": "Medium",
                    "timeline": "Week 1",
                    "details": "Audit columns that are never NULL in practice and formalize constraints. Use ALTER TABLE ... ALTER COLUMN ... SET NOT NULL.",
                },
                {
                    "action": "Build a Data Quality Dashboard",
                    "effort": "Medium",
                    "impact": "High",
                    "timeline": "Week 2-3",
                    "details": "Query DATA_QUALITY_MONITORING_USAGE_HISTORY to build a Streamlit dashboard showing DMF trends per table.",
                },
            ],
            "developing": [
                {
                    "action": "Create custom DMFs for business-rule validation",
                    "effort": "Medium",
                    "impact": "High",
                    "timeline": "Week 2-4",
                    "details": "Write custom Data Metric Functions for domain-specific rules (e.g., order_total > 0, email format validation).",
                },
                {
                    "action": "Enable anomaly detection on DMF results",
                    "effort": "Low",
                    "impact": "Medium",
                    "timeline": "Week 3",
                    "details": "Configure DMF alert rules to trigger notifications when metric values deviate beyond expected thresholds.",
                },
            ],
            "advancing": [
                {
                    "action": "Implement zero-duplicate guarantee pipelines",
                    "effort": "High",
                    "impact": "High",
                    "timeline": "Week 4-6",
                    "details": "Use MERGE INTO with deduplication logic. Monitor with DUPLICATE_COUNT DMF.",
                },
            ],
        },
    },
    "data_governance": {
        "dimension_name": "Data Governance",
        "priority_actions": {
            "foundational": [
                {
                    "action": "Run SYSTEM$CLASSIFY on all production databases",
                    "reference": "resources/action_plans/data_governance.md",
                    "effort": "Low",
                    "impact": "High",
                    "timeline": "Week 1",
                    "details": "Automatically detect PII, PHI, and PCI data across all tables. Review and approve tag assignments.",
                },
                {
                    "action": "Create ownership and domain tags",
                    "reference": "resources/templates/governance_tags.md",
                    "effort": "Low",
                    "impact": "High",
                    "timeline": "Week 1",
                    "details": "Define tags: data_owner, data_steward, domain, cost_center. Assign to all databases and schemas.",
                },
                {
                    "action": "Add COMMENT ON to all tables and critical columns",
                    "effort": "Medium",
                    "impact": "Medium",
                    "timeline": "Week 1-2",
                    "details": "Use Cortex COMPLETE to auto-generate table descriptions from column names and sample data.",
                },
            ],
            "developing": [
                {
                    "action": "Deploy tag-based masking policies",
                    "reference": "resources/templates/masking_policies.md",
                    "effort": "Medium",
                    "impact": "High",
                    "timeline": "Week 2-3",
                    "details": "Create masking policies that automatically mask columns tagged as EMAIL, PHONE, SSN, etc.",
                },
                {
                    "action": "Set up classification profiles on databases",
                    "effort": "Low",
                    "impact": "High",
                    "timeline": "Week 2",
                    "details": "Enable auto-classification profiles so new tables are classified automatically on creation.",
                },
            ],
            "advancing": [
                {
                    "action": "Implement row access policies for multi-tenant data",
                    "effort": "High",
                    "impact": "High",
                    "timeline": "Week 3-5",
                    "details": "Create row access policies that restrict data visibility based on user role/region/department.",
                },
            ],
        },
    },
    "security_compliance": {
        "dimension_name": "Security & Compliance",
        "priority_actions": {
            "foundational": [
                {
                    "action": "Enforce MFA for all human users",
                    "effort": "Low",
                    "impact": "Critical",
                    "timeline": "Week 1",
                    "details": "Create authentication policy requiring MFA. Assign to account or individual users. Prioritize ACCOUNTADMIN holders.",
                },
                {
                    "action": "Reduce ACCOUNTADMIN usage",
                    "reference": "resources/templates/rbac_hierarchy.md",
                    "effort": "Medium",
                    "impact": "Critical",
                    "timeline": "Week 1-2",
                    "details": "Audit ACCOUNTADMIN query history. Create functional roles (DATA_ENGINEER, ANALYST, etc.) with least-privilege grants.",
                },
                {
                    "action": "Create network policies",
                    "effort": "Low",
                    "impact": "High",
                    "timeline": "Week 1",
                    "details": "Restrict access to known IP ranges. Apply network policy at account level.",
                },
            ],
            "developing": [
                {
                    "action": "Deploy key-pair auth for service accounts",
                    "effort": "Medium",
                    "impact": "High",
                    "timeline": "Week 2-3",
                    "details": "Migrate service accounts from password auth to RSA key-pair authentication.",
                },
                {
                    "action": "Set up access review automation",
                    "effort": "Medium",
                    "impact": "Medium",
                    "timeline": "Week 3-4",
                    "details": "Build scheduled task querying ACCESS_HISTORY to detect unused grants and orphaned roles.",
                },
            ],
            "advancing": [
                {
                    "action": "Evaluate Tri-Secret Secure and private connectivity",
                    "effort": "High",
                    "impact": "High",
                    "timeline": "Week 4-8",
                    "details": "For regulated industries, implement customer-managed encryption keys and private link.",
                },
            ],
        },
    },
    "data_freshness": {
        "dimension_name": "Data Freshness",
        "priority_actions": {
            "foundational": [
                {
                    "action": "Deploy FRESHNESS DMFs on production tables",
                    "reference": "resources/action_plans/data_freshness.md",
                    "effort": "Low",
                    "impact": "High",
                    "timeline": "Week 1",
                    "details": "Attach SNOWFLAKE.CORE.FRESHNESS DMF to critical tables. Define expected freshness SLAs.",
                },
                {
                    "action": "Inventory all data pipelines and document SLAs",
                    "effort": "Medium",
                    "impact": "Medium",
                    "timeline": "Week 1-2",
                    "details": "Catalog all COPY INTO, Snowpipe, and Task-based pipelines. Define target latency per table tier.",
                },
            ],
            "developing": [
                {
                    "action": "Migrate batch loads to Snowpipe or Snowpipe Streaming",
                    "effort": "High",
                    "impact": "High",
                    "timeline": "Week 2-4",
                    "details": "Convert daily COPY INTO patterns to continuous Snowpipe for real-time ingestion.",
                },
                {
                    "action": "Adopt Dynamic Tables for transformation layers",
                    "reference": "resources/action_plans/data_freshness.md",
                    "effort": "Medium",
                    "impact": "High",
                    "timeline": "Week 3-5",
                    "details": "Replace scheduled Task+CTAS patterns with Dynamic Tables using target_lag for declarative freshness.",
                },
            ],
            "advancing": [
                {
                    "action": "Build end-to-end freshness monitoring with alerting",
                    "effort": "Medium",
                    "impact": "High",
                    "timeline": "Week 4-6",
                    "details": "Combine DMF results with Alert objects to send notifications when freshness SLAs are breached.",
                },
            ],
        },
    },
    "metadata_lineage": {
        "dimension_name": "Metadata & Lineage",
        "priority_actions": {
            "foundational": [
                {
                    "action": "Auto-generate table and column descriptions",
                    "effort": "Medium",
                    "impact": "High",
                    "timeline": "Week 1-2",
                    "details": "Use CORTEX.COMPLETE to generate COMMENT ON statements from column names and sample data for all tables.",
                },
                {
                    "action": "Create a tagging taxonomy",
                    "reference": "resources/templates/governance_tags.md",
                    "effort": "Low",
                    "impact": "High",
                    "timeline": "Week 1",
                    "details": "Define standard tags: domain, data_tier (raw/curated/serving), pii_level, cost_center.",
                },
            ],
            "developing": [
                {
                    "action": "Enable Git integration for schema-as-code",
                    "effort": "Medium",
                    "impact": "High",
                    "timeline": "Week 2-3",
                    "details": "Connect Snowflake Git integration to track DDL changes. Use dbt or Snowflake CLI for deployment.",
                },
                {
                    "action": "Build impact analysis queries",
                    "effort": "Medium",
                    "impact": "Medium",
                    "timeline": "Week 3-4",
                    "details": "Query OBJECT_DEPENDENCIES and ACCESS_HISTORY to build downstream impact reports before schema changes.",
                },
            ],
            "advancing": [
                {
                    "action": "Implement automated drift detection",
                    "effort": "High",
                    "impact": "High",
                    "timeline": "Week 4-6",
                    "details": "Create tasks that compare current schema to Git-tracked definitions and alert on unauthorized changes.",
                },
            ],
        },
    },
    "ai_consumption_readiness": {
        "dimension_name": "AI Consumption Readiness",
        "priority_actions": {
            "foundational": [
                {
                    "action": "Start using Cortex AI functions on existing data",
                    "reference": "resources/action_plans/ai_consumption_readiness.md",
                    "effort": "Low",
                    "impact": "High",
                    "timeline": "Week 1",
                    "details": "Run CORTEX.SENTIMENT, CORTEX.SUMMARIZE, and CORTEX.EXTRACT on text columns to demonstrate value.",
                },
                {
                    "action": "Generate embeddings for text-heavy tables",
                    "effort": "Medium",
                    "impact": "High",
                    "timeline": "Week 1-2",
                    "details": "Use CORTEX.EMBED to create VECTOR columns. Build a Cortex Search service for semantic retrieval.",
                },
            ],
            "developing": [
                {
                    "action": "Build feature tables for ML consumption",
                    "effort": "High",
                    "impact": "High",
                    "timeline": "Week 2-4",
                    "details": "Create curated wide tables with proper numeric types, encoded categoricals, and NULL handling for ML.",
                },
                {
                    "action": "Register first model in Snowflake Model Registry",
                    "effort": "Medium",
                    "impact": "High",
                    "timeline": "Week 3-4",
                    "details": "Train a simple model in Snowpark ML and log it to the Model Registry with metrics and sample input.",
                },
            ],
            "advancing": [
                {
                    "action": "Deploy Cortex Agent or Analyst for business users",
                    "effort": "High",
                    "impact": "High",
                    "timeline": "Week 4-8",
                    "details": "Build semantic model YAML for Cortex Analyst or configure Cortex Agent with tool definitions.",
                },
                {
                    "action": "Set up compute pools for GPU-accelerated ML",
                    "effort": "High",
                    "impact": "High",
                    "timeline": "Week 6-10",
                    "details": "Create SPCS compute pools with GPU instances for model training and real-time inference.",
                },
            ],
        },
    },
    "infrastructure_scalability": {
        "dimension_name": "Infrastructure & Scalability",
        "priority_actions": {
            "foundational": [
                {
                    "action": "Right-size warehouses and enable auto-suspend",
                    "reference": "resources/action_plans/infrastructure_scalability.md",
                    "effort": "Low",
                    "impact": "High",
                    "timeline": "Week 1",
                    "details": "Audit warehouse utilization. Set auto_suspend to 60s for interactive, 300s for ETL. Downsize underutilized warehouses.",
                },
                {
                    "action": "Create resource monitors with alerts",
                    "effort": "Low",
                    "impact": "Medium",
                    "timeline": "Week 1",
                    "details": "Add resource monitors at account and warehouse level with 75%/90%/100% notification thresholds.",
                },
            ],
            "developing": [
                {
                    "action": "Separate workloads into dedicated warehouses",
                    "effort": "Medium",
                    "impact": "High",
                    "timeline": "Week 2-3",
                    "details": "Create WH_ETL, WH_ANALYTICS, WH_ML with appropriate sizes. Route queries by workload type.",
                },
                {
                    "action": "Enable clustering and search optimization",
                    "effort": "Medium",
                    "impact": "Medium",
                    "timeline": "Week 3-4",
                    "details": "Add clustering keys to large, frequently filtered tables. Enable search optimization for point lookups.",
                },
            ],
            "advancing": [
                {
                    "action": "Implement FinOps with cost attribution",
                    "effort": "High",
                    "impact": "High",
                    "timeline": "Week 4-8",
                    "details": "Tag warehouses with cost_center. Build chargeback reports from METERING_DAILY_HISTORY.",
                },
            ],
        },
    },
    "organizational_readiness": {
        "dimension_name": "Organizational Readiness",
        "priority_actions": {
            "foundational": [
                {
                    "action": "Conduct AI readiness skills assessment across teams",
                    "effort": "Low",
                    "impact": "Medium",
                    "timeline": "Week 1",
                    "details": "Survey data team on Snowflake ML, Cortex, and Snowpark proficiency. Identify skill gaps.",
                },
                {
                    "action": "Define initial AI use-case backlog",
                    "effort": "Low",
                    "impact": "High",
                    "timeline": "Week 1-2",
                    "details": "Workshop with business stakeholders to identify top-5 AI use cases ranked by value and feasibility.",
                },
            ],
            "developing": [
                {
                    "action": "Establish a data governance council",
                    "effort": "Medium",
                    "impact": "High",
                    "timeline": "Week 2-4",
                    "details": "Form cross-functional governance board with data engineering, security, business, and legal.",
                },
                {
                    "action": "Create AI training program",
                    "effort": "Medium",
                    "impact": "High",
                    "timeline": "Week 3-6",
                    "details": "Enroll team in Snowflake ML and Cortex training. Establish internal knowledge-sharing sessions.",
                },
            ],
            "advancing": [
                {
                    "action": "Build AI Center of Excellence",
                    "effort": "High",
                    "impact": "High",
                    "timeline": "Month 2-4",
                    "details": "Formalize AI CoE with charter, budget, and KPIs. Define federated execution model.",
                },
            ],
        },
    },
}


def generate_action_plan(report: AIReadinessReport) -> str:
    lines = []
    lines.append("=" * 70)
    lines.append("       AI READINESS — DETAILED ACTION PLAN")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"  Current Score: {report.overall_score}/100 ({report.band_label})")
    lines.append("")

    sorted_dims = sorted(report.dimensions, key=lambda d: d.raw_score)

    for idx, dim in enumerate(sorted_dims, 1):
        band = get_band(dim.raw_score)
        playbook = REMEDIATION_PLAYBOOKS.get(dim.dimension_id, {})
        dim_name = playbook.get("dimension_name", dim.dimension_name)

        lines.append(f"  {'─' * 66}")
        lines.append(f"  {idx}. {dim_name.upper()}")
        lines.append(f"     Current Score: {dim.raw_score}/100 ({band['label']})")
        lines.append(f"     Weight: {dim.weight:.0%} of overall score")
        lines.append("")

        lines.append(f"     Criteria Breakdown:")
        for c in sorted(dim.criteria, key=lambda x: x.score):
            status = "✗" if c.score < 40 else ("△" if c.score < 70 else "✓")
            lines.append(f"       {status} {c.criterion_name:<32} {c.score:>5.1f}/100")
        lines.append("")

        priority_actions = playbook.get("priority_actions", {})
        relevant_tier = band["label"].lower()
        tiers_to_show = []
        if relevant_tier == "foundational":
            tiers_to_show = ["foundational"]
        elif relevant_tier == "developing":
            tiers_to_show = ["foundational", "developing"]
        elif relevant_tier == "advancing":
            tiers_to_show = ["developing", "advancing"]
        else:
            tiers_to_show = ["advancing"]

        action_num = 1
        for tier in tiers_to_show:
            actions = priority_actions.get(tier, [])
            for action in actions:
                lines.append(f"     ACTION {idx}.{action_num}: {action['action']}")
                lines.append(f"       Effort: {action['effort']}  |  Impact: {action['impact']}  |  Timeline: {action['timeline']}")
                lines.append(f"       {action['details']}")
                if "reference" in action:
                    lines.append(f"       Reference: {action['reference']}")
                lines.append("")
                action_num += 1

    lines.append("=" * 70)
    lines.append("  RECOMMENDED EXECUTION ORDER")
    lines.append("=" * 70)
    lines.append("")
    lines.append("  Phase 1 (Week 1-2): Quick Wins — Security hardening + DMF deployment")
    lines.append("  Phase 2 (Week 2-4): Foundation — Governance tags + classification + documentation")
    lines.append("  Phase 3 (Week 4-6): Acceleration — Dynamic Tables + Cortex functions + feature tables")
    lines.append("  Phase 4 (Week 6-10): Scale — Model Registry + SPCS + MLOps pipelines")
    lines.append("  Phase 5 (Month 3+): Optimization — AI CoE + continuous monitoring + cost governance")
    lines.append("")
    lines.append("=" * 70)

    return "\n".join(lines)


def generate_executive_summary(report: AIReadinessReport) -> str:
    lines = []
    lines.append("EXECUTIVE SUMMARY — AI READINESS ASSESSMENT")
    lines.append("")
    lines.append(f"Overall Score: {report.overall_score}/100 — {report.band_label}")
    lines.append("")

    strengths = [d for d in report.dimensions if d.raw_score >= 70]
    gaps = [d for d in report.dimensions if d.raw_score < 50]
    moderate = [d for d in report.dimensions if 50 <= d.raw_score < 70]

    if strengths:
        lines.append("STRENGTHS:")
        for d in strengths:
            lines.append(f"  + {d.dimension_name}: {d.raw_score}/100")

    if moderate:
        lines.append("\nNEEDS IMPROVEMENT:")
        for d in moderate:
            lines.append(f"  ~ {d.dimension_name}: {d.raw_score}/100")

    if gaps:
        lines.append("\nCRITICAL GAPS:")
        for d in gaps:
            lines.append(f"  ! {d.dimension_name}: {d.raw_score}/100")

    lines.append("")
    lines.append("There is no AI strategy without a Data Strategy.")
    lines.append("Address data quality and governance gaps before investing in AI tooling.")

    return "\n".join(lines)
