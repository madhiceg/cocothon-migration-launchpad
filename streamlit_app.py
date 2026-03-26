import streamlit as st
from snowflake.snowpark.context import get_active_session
import json
from datetime import datetime

session = get_active_session()

SCHEMA_VERSION = "2.0"

DB = "MIGRATION_ASSESSMENTS"
SCHEMA = "INTAKE"
ASSESSMENTS_TABLE = f"{DB}.{SCHEMA}.ASSESSMENTS"
REFERENCE_ARCH_TABLE = f"{DB}.{SCHEMA}.REFERENCE_ARCHITECTURES"
SOURCE_SYSTEMS_TABLE = f"{DB}.{SCHEMA}.ASSESSMENT_SOURCE_SYSTEMS"
ETL_TOOLS_TABLE = f"{DB}.{SCHEMA}.ASSESSMENT_ETL_TOOLS"
VERSION_HISTORY_TABLE = f"{DB}.{SCHEMA}.ASSESSMENT_VERSION_HISTORY"

SOURCE_SYSTEMS = [
    "Oracle",
    "Teradata",
    "SQL Server",
    "Azure Synapse",
    "Amazon Redshift",
    "Google BigQuery",
    "Databricks",
    "MySQL",
    "PostgreSQL",
    "IBM DB2",
    "SAP HANA",
    "Netezza",
    "Greenplum",
    "Vertica",
    "Apache Hive",
    "Apache Spark SQL",
    "Sybase / SAP ASE",
    "MongoDB",
    "Cassandra",
    "Snowflake (consolidation)",
]

ETL_TOOLS = [
    "Fivetran",
    "Matillion",
    "Hevo Data",
    "Talend",
    "Informatica PowerCenter",
    "Informatica Cloud (IDMC)",
    "Apache Airflow",
    "AWS Glue",
    "Azure Data Factory (ADF)",
    "Google Cloud Dataflow",
    "Stitch Data",
    "Airbyte",
    "Rivery",
    "Apache NiFi",
    "Pentaho",
    "SSIS (SQL Server Integration Services)",
    "Oracle Data Integrator (ODI)",
    "Ab Initio",
    "DataStage (IBM)",
    "Custom Scripts (Python/Spark)",
    "None / Not Applicable",
]

TRANSFORMATION_TOOLS = [
    "dbt (data build tool)",
    "dbt Cloud",
    "Coalesce",
    "Matillion (ELT)",
    "Dataform",
    "SQLMesh",
    "Snowpark (Python / Java / Scala)",
    "Stored Procedures (in-database)",
    "Apache Spark",
    "Custom Python / PySpark",
    "None / To Be Decided",
]

ORCHESTRATION_TOOLS = [
    "Apache Airflow / MWAA",
    "Prefect",
    "Dagster",
    "Snowflake Tasks & Streams",
    "Azure Data Factory",
    "AWS Step Functions",
    "Google Cloud Composer",
    "Control-M",
    "AutoSys",
    "Cron / Custom Scheduler",
    "dbt Cloud Scheduler",
    "None / To Be Decided",
]

BI_TOOLS = [
    "Tableau",
    "Power BI",
    "Looker",
    "Sigma Computing",
    "ThoughtSpot",
    "Qlik Sense",
    "MicroStrategy",
    "Metabase",
    "Apache Superset",
    "Streamlit",
    "Mode Analytics",
    "Sisense",
    "None / To Be Decided",
]

DATA_GOVERNANCE_TOOLS = [
    "Alation",
    "Collibra",
    "Atlan",
    "Monte Carlo",
    "Snowflake Horizon (native)",
    "Great Expectations",
    "Soda",
    "Apache Atlas",
    "Informatica Data Governance",
    "None / To Be Decided",
]

DATA_CATALOG_TOOLS = [
    "Alation",
    "Collibra",
    "Atlan",
    "DataHub (LinkedIn OSS)",
    "Apache Atlas",
    "Snowflake Horizon Catalog (native)",
    "AWS Glue Data Catalog",
    "Azure Purview / Microsoft Purview",
    "Google Data Catalog",
    "Informatica Enterprise Data Catalog",
    "None / To Be Decided",
]

SNOWFLAKE_EDITIONS = [
    "Standard",
    "Enterprise",
    "Business Critical",
    "Virtual Private Snowflake (VPS)",
    "Not Sure / Need Guidance",
]

CLOUD_PROVIDERS = ["AWS", "Azure", "GCP", "On-Premises", "Hybrid / Multi-Cloud"]

MIGRATION_DRIVERS = [
    "Cost reduction",
    "Performance improvement",
    "Scalability / Elasticity",
    "Cloud-first strategy",
    "End-of-life / License expiry",
    "Consolidation of multiple platforms",
    "Real-time / near-real-time requirements",
    "Data sharing / marketplace needs",
    "AI / ML enablement",
    "Regulatory / Compliance",
    "Vendor lock-in reduction",
    "Modernize data architecture",
]

COMPLIANCE_FRAMEWORKS = [
    "HIPAA",
    "GDPR",
    "SOC 2",
    "PCI DSS",
    "FedRAMP",
    "ISO 27001",
    "CCPA",
    "SOX",
    "None / Not Applicable",
]

INDUSTRY_INTELLIGENCE = {
    "Financial Services / Banking": {
        "top_use_cases": ["Real-Time Fraud Detection", "Regulatory Reporting (Basel/SOX/IFRS)", "Customer 360 / KYC", "Risk Analytics & Stress Testing", "Credit Decisioning"],
        "peer_companies": ["Capital One", "Western Union", "Nasdaq", "Ally Financial"],
        "data_model": "Dimensional Model (Kimball) with Compliance Vault",
        "key_features": ["Snowpipe Streaming", "Cortex ML", "Dynamic Tables", "Time Travel", "Horizon (lineage + classification)"],
    },
    "Healthcare & Life Sciences": {
        "top_use_cases": ["Clinical Data Warehouse", "Real-World Evidence (RWE)", "Claims Analytics & Fraud Detection", "Patient 360", "HIPAA-Compliant Data Sharing"],
        "peer_companies": ["Providence Health", "Anthem (Elevance Health)", "Novartis", "Tempus"],
        "data_model": "OMOP Common Data Model with PHI Isolation Layers",
        "key_features": ["Data Clean Rooms", "Dynamic Data Masking", "Horizon (HIPAA classification)", "Marketplace (health data)"],
    },
    "Retail & E-commerce": {
        "top_use_cases": ["Customer 360 & Personalization", "Demand Forecasting", "Real-Time Pricing", "Supply Chain Visibility", "Unified Commerce Analytics"],
        "peer_companies": ["Instacart", "PepsiCo", "Albertsons", "DoorDash"],
        "data_model": "Kimball Star Schema with Real-Time Overlay (Dynamic Tables)",
        "key_features": ["Snowpipe Streaming", "Cortex ML", "Marketplace (weather/foot traffic)", "Data Sharing"],
    },
    "Technology / SaaS": {
        "top_use_cases": ["Product Analytics", "Multi-Tenant Analytics", "Usage-Based Billing", "ML Feature Store", "Customer Health Scoring"],
        "peer_companies": ["Figma", "Notion", "Grammarly", "LiveRamp"],
        "data_model": "Event-Driven Medallion with Multi-Tenant Isolation",
        "key_features": ["Snowpipe Streaming", "Secure Data Sharing", "Reader Accounts", "Marketplace (Provider)"],
    },
    "Manufacturing": {
        "top_use_cases": ["Predictive Maintenance", "Production Quality Analytics", "OEE Monitoring", "Supply Chain Optimization", "Energy & Sustainability"],
        "peer_companies": ["Siemens", "Yamaha Motor", "Honeywell", "HP Inc."],
        "data_model": "Medallion with IoT Time-Series Optimization",
        "key_features": ["Snowpipe Streaming (IoT)", "Dynamic Tables", "Auto-clustering", "Marketplace (energy/weather)"],
    },
    "Telecommunications": {
        "top_use_cases": ["Network Performance Analytics", "Churn Prediction", "Revenue Assurance", "5G / IoT Analytics", "Customer 360"],
        "peer_companies": ["AT&T", "T-Mobile", "Vodafone", "DISH Network"],
        "data_model": "Medallion with CDR/Event Optimization",
        "key_features": ["Snowpipe Streaming", "Iceberg Tables", "Auto-clustering", "Cortex ML"],
    },
    "Media & Entertainment": {
        "top_use_cases": ["Content Performance Analytics", "Audience Segmentation", "Ad Revenue Optimization", "Royalty Calculations", "Content Recommendations"],
        "peer_companies": ["Warner Bros. Discovery", "NBC Universal", "Riot Games", "Sony Music"],
        "data_model": "Event-Driven Star Schema with Content Catalog",
        "key_features": ["Snowpipe Streaming", "Data Clean Rooms", "Marketplace (demographic data)", "Cortex ML"],
    },
    "Energy & Utilities": {
        "top_use_cases": ["Smart Grid Analytics", "Predictive Maintenance", "Energy Trading Analytics", "Regulatory Compliance (NERC/FERC)", "ESG Reporting"],
        "peer_companies": ["AES Corporation", "Constellation Energy", "Southern Company", "Duke Energy"],
        "data_model": "Time-Series Optimized with IoT Layer",
        "key_features": ["Snowpipe Streaming", "Dynamic Tables", "Marketplace (weather/commodity)", "Horizon"],
    },
    "Government / Public Sector": {
        "top_use_cases": ["Citizen 360", "Fraud, Waste & Abuse Detection", "Open Data Platform", "Emergency Management", "FedRAMP-Compliant Analytics"],
        "peer_companies": ["US Department of Defense", "State of Tennessee", "UK NHS"],
        "data_model": "Medallion with Agency Isolation",
        "key_features": ["Snowflake Government (FedRAMP)", "Secure Data Sharing", "Horizon", "Network Policies"],
    },
    "Education": {
        "top_use_cases": ["Student Success Analytics", "Learning Analytics", "Enrollment Yield Optimization", "Institutional Research", "Research Data Platform"],
        "peer_companies": ["Western Governors University", "2U / edX", "Chegg"],
        "data_model": "Dimensional Model with Student-Centric Schema",
        "key_features": ["Cortex ML", "Snowpark", "Data Sharing (inter-institutional)", "Streamlit dashboards"],
    },
    "Insurance": {
        "top_use_cases": ["Claims Analytics & Fraud Detection", "Actuarial Modeling", "Policyholder 360", "Regulatory Reporting (Solvency II/IFRS 17)", "Telematics / Usage-Based Insurance"],
        "peer_companies": ["Zurich Insurance", "Nationwide", "Swiss Re", "AXA"],
        "data_model": "Dimensional Model with Actuarial Overlay",
        "key_features": ["Cortex ML", "Snowpark Python", "Time Travel", "Horizon (lineage)"],
    },
    "Logistics & Supply Chain": {
        "top_use_cases": ["Route Optimization", "Fleet Telematics", "Shipment Visibility", "Warehouse Analytics", "Demand Planning"],
        "peer_companies": ["FedEx", "Maersk", "C.H. Robinson"],
        "data_model": "Event-Driven with GPS/IoT Time-Series Layer",
        "key_features": ["Snowpipe Streaming (GPS/IoT)", "Marketplace (traffic/weather)", "Cortex ML", "Data Sharing"],
    },
}

st.set_page_config(layout="wide", page_title="Snowflake Migration Launchpad")

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 0.5rem 0 0.8rem;">
        <div style="font-size:1.4rem; font-weight:800; color:#29B5E8; letter-spacing:-0.5px;">CoCoDuo</div>
        <div style="font-size:0.6rem; color:#888; letter-spacing:1.5px; margin-top:2px;">MIGRATION LAUNCHPAD</div>
        <div style="font-size:0.65rem; color:#aaa; margin-top:4px;">by <span style="color:#B3D943;font-weight:700;">kipi.ai</span></div>
    </div>
    """, unsafe_allow_html=True)

    app_mode = st.radio("Assessment Mode", ["New Assessment", "Edit Existing"], key="app_mode", label_visibility="collapsed")
    is_edit_mode_selected = "Edit" in app_mode

    if is_edit_mode_selected:
        st.markdown("---")
        st.markdown("##### Find Assessment")
        search_term = st.text_input("Customer name or ID", key="edit_search", placeholder="e.g. Pinnacle or assess-002")
        search_btn = st.button("Search", key="edit_search_btn", use_container_width=True)

        if search_btn and search_term:
            safe_search = search_term.replace("'", "''")
            results = session.sql(f"""
                SELECT ASSESSMENT_ID, CUSTOMER_NAME, INDUSTRY, SA_NAME,
                       COALESCE(VERSION_NUMBER, 1) AS VERSION_NUMBER,
                       COMPLETENESS_PCT, STATUS, SUBMITTED_AT
                FROM {ASSESSMENTS_TABLE}
                WHERE UPPER(CUSTOMER_NAME) LIKE UPPER('%{safe_search}%')
                   OR UPPER(ASSESSMENT_ID) LIKE UPPER('%{safe_search}%')
                ORDER BY SUBMITTED_AT DESC
                LIMIT 20
            """).collect()
            st.session_state["search_results"] = results

        if "search_results" in st.session_state and st.session_state["search_results"]:
            results = st.session_state["search_results"]
            st.caption(f"{len(results)} result(s) found")
            options = {f"{r['CUSTOMER_NAME']}  v{r['VERSION_NUMBER']}": r['ASSESSMENT_ID'] for r in results}
            selected = st.selectbox("Select assessment", list(options.keys()), key="edit_select", label_visibility="collapsed")
            load_btn = st.button("Load into Form", key="edit_load_btn", type="primary", use_container_width=True)

            if load_btn and selected:
                aid = options[selected]
                row = session.sql(f"SELECT * FROM {ASSESSMENTS_TABLE} WHERE ASSESSMENT_ID = '{aid}'").collect()
                if row:
                    r = row[0].asDict()
                    st.session_state["edit_mode"] = True
                    st.session_state["edit_assessment_id"] = aid
                    st.session_state["edit_version"] = r.get("VERSION_NUMBER", 1) or 1
                    st.session_state["edit_customer_name"] = r.get("CUSTOMER_NAME", "")

                    loaded_data = {}
                    def _parse_variant(val):
                        if val is None:
                            return {}
                        if isinstance(val, dict):
                            return val
                        if isinstance(val, str):
                            try:
                                return json.loads(val)
                            except (json.JSONDecodeError, TypeError):
                                return {}
                        return {}

                    def _parse_array(val):
                        if val is None:
                            return []
                        if isinstance(val, list):
                            return val
                        if isinstance(val, str):
                            try:
                                parsed = json.loads(val)
                                return parsed if isinstance(parsed, list) else []
                            except (json.JSONDecodeError, TypeError):
                                return []
                        return []

                    cust_data = _parse_variant(r.get("CUSTOMER_DATA"))
                    vol_data = _parse_variant(r.get("VOLUME_DATA"))
                    etl_d = _parse_variant(r.get("ETL_DATA"))
                    trans_d = _parse_variant(r.get("TRANSFORMATION_DATA"))
                    nuances_d = _parse_variant(r.get("NUANCES_DATA"))
                    src_det = _parse_variant(r.get("SOURCE_DETAILS"))
                    src_sys = _parse_array(r.get("SOURCE_SYSTEMS"))

                    loaded_data["customer"] = cust_data
                    loaded_data["volume"] = vol_data
                    loaded_data["etl"] = etl_d
                    loaded_data["transformation"] = trans_d
                    loaded_data["nuances"] = nuances_d
                    loaded_data["source_details"] = src_det
                    loaded_data["source_systems"] = src_sys

                    st.session_state["loaded_assessment"] = loaded_data

                    st.session_state["tooling_concerns"] = nuances_d.get("tooling_concerns", "")
                    st.session_state["cost_priorities"] = nuances_d.get("cost_priorities", "")
                    st.session_state["technical_debt"] = nuances_d.get("technical_debt", "")
                    st.session_state["arch_vision"] = nuances_d.get("data_architecture_vision", "")
                    st.session_state["perf_reqs"] = nuances_d.get("performance_requirements", "")
                    st.session_state["security_reqs"] = nuances_d.get("security_requirements", "")
                    st.session_state["risks"] = nuances_d.get("migration_risks", "")
                    st.session_state["additional"] = nuances_d.get("additional_context", "")

                    _src_list = [s for s in src_sys if s in SOURCE_SYSTEMS]
                    st.session_state["source_systems_select"] = _src_list

                    _etl_tools = list(etl_d.get("tool_details", {}).keys())
                    _etl_current = etl_d.get("current_tools", _etl_tools)
                    st.session_state["current_etl"] = [t for t in _etl_current if t in ETL_TOOLS]
                    _ingestion = etl_d.get("ingestion_preferences", [])
                    if _ingestion:
                        st.session_state["ingestion_prefs"] = _ingestion
                    st.session_state["annual_etl_cost"] = etl_d.get("annual_etl_cost", "")
                    st.session_state["annual_infra_cost"] = etl_d.get("annual_infra_cost", "")
                    _cdc_mechs = etl_d.get("current_cdc", [])
                    if _cdc_mechs:
                        st.session_state["current_cdc"] = _cdc_mechs
                    st.session_state["cdc_table_count"] = int(etl_d.get("cdc_tables", 0) or 0)
                    _cdc_lat = etl_d.get("cdc_latency", "")
                    if _cdc_lat:
                        st.session_state["cdc_latency"] = _cdc_lat

                    _key_map = {
                        "current_orch": "current_orchestration",
                        "target_orch": "target_orchestration",
                        "current_gov": "current_governance",
                        "target_gov": "target_governance",
                    }
                    for _td_key, _td_opts in [
                        ("current_transform", TRANSFORMATION_TOOLS),
                        ("target_transform", TRANSFORMATION_TOOLS),
                        ("current_orch", ORCHESTRATION_TOOLS),
                        ("target_orch", ORCHESTRATION_TOOLS),
                        ("current_bi", BI_TOOLS),
                        ("target_bi", BI_TOOLS),
                        ("current_gov", DATA_GOVERNANCE_TOOLS),
                        ("target_gov", DATA_GOVERNANCE_TOOLS),
                        ("current_catalog", DATA_CATALOG_TOOLS),
                        ("target_catalog", DATA_CATALOG_TOOLS),
                    ]:
                        _alt_key = _key_map.get(_td_key, _td_key)
                        _vals = trans_d.get(_td_key, trans_d.get(_alt_key, []))
                        if _vals:
                            st.session_state[_td_key] = [v for v in _vals if v in _td_opts]
                    _vs = trans_d.get("validation_strategy", [])
                    if _vs:
                        st.session_state["validation_strategy"] = _vs
                    _pd = trans_d.get("parallel_run_duration", "")
                    if _pd:
                        st.session_state["parallel_duration"] = _pd
                    _rb = trans_d.get("rollback_plan", "")
                    if _rb:
                        st.session_state["rollback"] = _rb

                    st.toast(f"Loaded {r.get('CUSTOMER_NAME', '')} v{r.get('VERSION_NUMBER', 1)}")
                    st.rerun()

        if st.session_state.get("edit_mode"):
            st.markdown("---")
            _ecn = st.session_state.get('edit_customer_name', '')
            _ev = st.session_state.get('edit_version', 1)
            _eid = st.session_state.get('edit_assessment_id', '')
            st.markdown(f"""
            <div style="background:rgba(255,107,53,0.08); border:1px solid rgba(255,107,53,0.3); border-radius:8px; padding:12px; margin-bottom:8px;">
                <div style="font-weight:700; color:#FF6B35; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px;">EDITING</div>
                <div style="font-size:1rem; font-weight:600; margin:4px 0;">{_ecn}</div>
                <div style="font-size:0.75rem; color:#888;">Version {_ev} &nbsp;·&nbsp; <code>{_eid[:16]}...</code></div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Cancel Edit", key="cancel_edit", use_container_width=True):
                for k in ["edit_mode", "edit_assessment_id", "edit_version", "edit_customer_name", "loaded_assessment", "search_results"]:
                    st.session_state.pop(k, None)
                st.rerun()
        elif not st.session_state.get("search_results"):
            st.info("Search for an existing assessment above to edit it.")

    if "New" in app_mode and st.session_state.get("edit_mode"):
        for k in ["edit_mode", "edit_assessment_id", "edit_version", "edit_customer_name", "loaded_assessment", "search_results"]:
            st.session_state.pop(k, None)

    st.markdown("---")
    st.markdown(
        '<div style="font-size:0.72rem;color:#888;text-align:center;">'
        '<span style="color:#B3D943;font-weight:700;">kipi.ai</span> · CoCoDuo v2.0'
        '</div>',
        unsafe_allow_html=True,
    )

edit_mode = st.session_state.get("edit_mode", False)
loaded = st.session_state.get("loaded_assessment", {})
loaded_cust = loaded.get("customer", {}) if edit_mode else {}
loaded_vol = loaded.get("volume", {}) if edit_mode else {}
loaded_etl = loaded.get("etl", {}) if edit_mode else {}
loaded_trans = loaded.get("transformation", {}) if edit_mode else {}
loaded_nuances = loaded.get("nuances", {}) if edit_mode else {}
loaded_src_det = loaded.get("source_details", {}) if edit_mode else {}
loaded_src_sys = loaded.get("source_systems", []) if edit_mode else []

st.markdown(
    """
    <style>
    .main-header {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #29B5E8 0%, #1E88E5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 0.3rem;
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }
    .main-sub {
        font-size: 0.85rem;
        color: #888;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.05rem;
        font-weight: 700;
        color: #29B5E8;
        margin-top: 1.4rem;
        margin-bottom: 0.5rem;
        padding-bottom: 0.35rem;
        border-bottom: 2px solid rgba(41, 181, 232, 0.15);
        letter-spacing: -0.2px;
    }
    .info-box {
        padding: 14px 18px;
        border-radius: 8px;
        margin-bottom: 1rem;
        font-size: 0.88rem;
        line-height: 1.5;
        border-left: 4px solid #29B5E8;
        background: rgba(41, 181, 232, 0.06);
    }
    .info-box.edit-mode {
        border-left-color: #FF6B35;
        background: rgba(255, 107, 53, 0.06);
    }
    .stNumberInput > div > div > input {
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        border-bottom: 2px solid rgba(41, 181, 232, 0.12);
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.01em;
    }
    div[data-testid="stExpander"] {
        border: 1px solid rgba(41, 181, 232, 0.15);
        border-radius: 8px;
        margin-bottom: 8px;
    }
    div[data-testid="stExpander"] summary span {
        font-weight: 600 !important;
    }
    .progress-bar-container {
        background: #E8E8E8;
        border-radius: 10px;
        height: 8px;
        margin: 6px 0 16px;
        overflow: hidden;
    }
    .progress-bar-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.4s ease;
    }
    .review-card {
        padding: 12px 16px;
        border-radius: 8px;
        border: 1px solid rgba(41, 181, 232, 0.12);
        margin-bottom: 8px;
    }
    .review-card .rc-label {
        font-size: 0.72rem;
        font-weight: 600;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 2px;
    }
    .review-card .rc-value {
        font-size: 0.95rem;
        font-weight: 600;
        color: inherit;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-header">Snowflake Migration Launchpad</div>'
    '<div class="main-sub">Capture customer migration details for CoCo to generate tailored architecture plans</div>',
    unsafe_allow_html=True,
)

if edit_mode:
    _ecn = st.session_state.get("edit_customer_name", "")
    _ev = st.session_state.get("edit_version", 1)
    st.markdown(
        f'<div class="info-box edit-mode">'
        f'<strong>✏️ Edit Mode</strong> — You are editing <strong>{_ecn}</strong> '
        f'(Version {_ev}). '
        f'Make your changes across any tab, then click <strong>Update Assessment</strong> on the Review tab. '
        f'The current version will be automatically preserved in version history.'
        f'</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<div class="info-box">'
        "Welcome kipian! Fill in each section as completely as possible. Once submitted, "
        "the data is persisted to Snowflake for <strong>CoCo</strong> (Cortex Code) to generate "
        "a tailored migration solution architecture."
        "</div>",
        unsafe_allow_html=True,
    )

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "Customer Profile",
        "Source Systems",
        "Data & Volume",
        "ETL & Tools",
        "Transform & Orchestrate",
        "Architecture Nuances",
        "Review & Submit",
    ]
)

if "assessment" not in st.session_state:
    st.session_state.assessment = {}

# ─────────────────────────────────────────────────────────
# TAB 1 : CUSTOMER PROFILE
# ─────────────────────────────────────────────────────────
with tab1:
    st.markdown(
        '<div class="section-header">Customer Information</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        customer_name = st.text_input(
            "Customer Name *", value=loaded_cust.get("name", ""), placeholder="e.g. Acme Corporation"
        )
        customer_website = st.text_input(
            "Customer Website URL", value=loaded_cust.get("website", ""), placeholder="https://www.example.com"
        )
        _ind_options = [
                "",
                "Financial Services / Banking",
                "Healthcare & Life Sciences",
                "Retail & E-commerce",
                "Technology / SaaS",
                "Manufacturing",
                "Telecommunications",
                "Media & Entertainment",
                "Energy & Utilities",
                "Government / Public Sector",
                "Education",
                "Insurance",
                "Logistics & Supply Chain",
                "Real Estate",
                "Other",
            ]
        _ind_default = loaded_cust.get("industry", "")
        _ind_idx = _ind_options.index(_ind_default) if _ind_default in _ind_options else 0
        industry = st.selectbox(
            "Industry Vertical *",
            _ind_options,
            index=_ind_idx,
        )
        if industry == "Other":
            industry = st.text_input(
                "Please specify Industry Vertical *",
                placeholder="e.g. Aerospace & Defense",
                key="custom_industry",
            )

    with col2:
        sa_name = st.text_input(
            "Solutions Architect Name *", value=loaded_cust.get("sa_name", ""), placeholder="Your name"
        )
        sa_email = st.text_input("Solutions Architect Email", value=loaded_cust.get("sa_email", ""), placeholder="name@kipi.ai")
        _eng_options = [
                "New Customer (Greenfield)",
                "Existing Customer (Expansion)",
                "POC / Proof of Concept",
            ]
        _eng_default = loaded_cust.get("engagement_type", _eng_options[0])
        _eng_idx = _eng_options.index(_eng_default) if _eng_default in _eng_options else 0
        engagement_type = st.radio(
            "Engagement Type *",
            _eng_options,
            index=_eng_idx,
            horizontal=True,
        )

    st.markdown(
        '<div class="section-header">Cloud & Region</div>', unsafe_allow_html=True
    )
    col3, col4 = st.columns(2)
    with col3:
        current_cloud = st.multiselect(
            "Customer's Current Cloud Provider(s)", CLOUD_PROVIDERS,
            default=[c for c in loaded_cust.get("current_cloud", []) if c in CLOUD_PROVIDERS]
        )
        _tc_options = [
                "",
                "AWS - US East (N. Virginia)",
                "AWS - US West (Oregon)",
                "AWS - EU (Frankfurt)",
                "AWS - EU (Ireland)",
                "AWS - AP (Sydney)",
                "AWS - AP (Tokyo)",
                "Azure - East US 2",
                "Azure - West Europe",
                "Azure - Southeast Asia",
                "GCP - US Central1",
                "GCP - Europe West2",
                "Other / TBD",
            ]
        _tc_default = loaded_cust.get("target_cloud", "")
        _tc_idx = _tc_options.index(_tc_default) if _tc_default in _tc_options else 0
        target_cloud = st.selectbox(
            "Target Snowflake Cloud / Region",
            _tc_options,
            index=_tc_idx,
        )
    with col4:
        migration_drivers = st.multiselect(
            "Primary Migration Drivers (select all that apply) *", MIGRATION_DRIVERS,
            default=[d for d in loaded_cust.get("migration_drivers", []) if d in MIGRATION_DRIVERS]
        )
        compliance_reqs = st.multiselect(
            "Compliance / Regulatory Requirements", COMPLIANCE_FRAMEWORKS,
            default=[c for c in loaded_cust.get("compliance", []) if c in COMPLIANCE_FRAMEWORKS]
        )

    st.markdown(
        '<div class="section-header">Timeline & Budget</div>', unsafe_allow_html=True
    )
    col5, col6, col7 = st.columns(3)
    with col5:
        _tl_options = [
                "< 1 month",
                "1-3 months",
                "3-6 months",
                "6-12 months",
                "12-18 months",
                "18-24 months",
                "> 24 months",
            ]
        _tl_default = loaded_cust.get("timeline", "6-12 months")
        if _tl_default not in _tl_options:
            _tl_default = "6-12 months"
        timeline = st.select_slider(
            "Expected Migration Timeline",
            options=_tl_options,
            value=_tl_default,
        )
    with col6:
        _bs_options = [
                "Very Flexible",
                "Moderate",
                "Cost Conscious",
                "Highly Cost Sensitive",
                "Open Source Only",
            ]
        _bs_default = loaded_cust.get("budget_sensitivity", "Moderate")
        if _bs_default not in _bs_options:
            _bs_default = "Moderate"
        budget_sensitivity = st.select_slider(
            "Budget Sensitivity",
            options=_bs_options,
            value=_bs_default,
        )
    with col7:
        team_size = st.number_input(
            "Customer's Data Engineering Team Size",
            min_value=0,
            max_value=500,
            value=int(loaded_cust.get("team_size", 5) or 5),
            step=1,
        )

    st.markdown(
        '<div class="section-header">Snowflake Target Configuration</div>',
        unsafe_allow_html=True,
    )
    col8, col9, col10 = st.columns(3)
    with col8:
        _sf_idx = SNOWFLAKE_EDITIONS.index(loaded_cust.get("snowflake_edition", SNOWFLAKE_EDITIONS[0])) if loaded_cust.get("snowflake_edition") in SNOWFLAKE_EDITIONS else 0
        sf_edition = st.selectbox("Preferred Snowflake Edition", SNOWFLAKE_EDITIONS, index=_sf_idx)
    with col9:
        _ma_opts = ["Big Bang (all at once)", "Phased / Incremental", "Parallel Run", "Undecided"]
        _ma_default = loaded_cust.get("migration_approach", _ma_opts[0])
        _ma_idx = _ma_opts.index(_ma_default) if _ma_default in _ma_opts else 0
        migration_approach = st.radio(
            "Migration Approach",
            _ma_opts,
            index=_ma_idx,
        )
    with col10:
        data_sharing_needed = st.checkbox("Requires Snowflake Data Sharing / Marketplace", value=bool(loaded_cust.get("data_sharing_needed", False)))
        iceberg_interest = st.checkbox("Interested in Apache Iceberg Tables", value=bool(loaded_cust.get("iceberg_interest", False)))
        snowpark_interest = st.checkbox("Interested in Snowpark (Python / Java / Scala)", value=bool(loaded_cust.get("snowpark_interest", False)))

    st.session_state.assessment["customer"] = {
        "name": customer_name,
        "website": customer_website,
        "industry": industry,
        "sa_name": sa_name,
        "sa_email": sa_email,
        "engagement_type": engagement_type,
        "current_cloud": current_cloud,
        "target_cloud": target_cloud,
        "migration_drivers": migration_drivers,
        "compliance": compliance_reqs,
        "timeline": timeline,
        "budget_sensitivity": budget_sensitivity,
        "team_size": team_size,
        "snowflake_edition": sf_edition,
        "migration_approach": migration_approach,
        "data_sharing_needed": data_sharing_needed,
        "iceberg_interest": iceberg_interest,
        "snowpark_interest": snowpark_interest,
    }

# ─────────────────────────────────────────────────────────
# TAB 2 : SOURCE SYSTEMS
# ─────────────────────────────────────────────────────────
with tab2:
    st.markdown(
        '<div class="section-header">Source Database Systems</div>',
        unsafe_allow_html=True,
    )
    st.caption("Select all source systems involved in this migration. Detail panels appear dynamically for each.")

    _src_default = [s for s in loaded_src_sys if s in SOURCE_SYSTEMS] if edit_mode else []
    source_systems = st.multiselect(
        "Source Database Systems *", SOURCE_SYSTEMS, default=_src_default, key="source_systems_select"
    )

    source_details = {}

    for src in source_systems:
        _sd = loaded_src_det.get(src, {}) if edit_mode else {}
        with st.expander(f"{src}", expanded=True):
            cols = st.columns(3)
            with cols[0]:
                version = st.text_input(
                    f"{src} - Version / Edition",
                    value=str(_sd.get("version", "")),
                    key=f"ver_{src}",
                    placeholder="e.g. 19c, 2019 Enterprise",
                )
            with cols[1]:
                _host_opts = ["On-Premises", "Cloud-hosted (IaaS)", "Managed Service (PaaS)", "SaaS"]
                _host_val = _sd.get("hosting", _host_opts[0])
                _host_idx = _host_opts.index(_host_val) if _host_val in _host_opts else 0
                hosting = st.selectbox(
                    f"{src} - Hosting",
                    _host_opts,
                    index=_host_idx,
                    key=f"host_{src}",
                )
            with cols[2]:
                _conn_opts = [
                        "Public Internet",
                        "VPN / VPC Peering",
                        "Private Link",
                        "Direct Connect / ExpressRoute",
                        "TBD",
                    ]
                _conn_val = _sd.get("connectivity", _conn_opts[0])
                _conn_idx = _conn_opts.index(_conn_val) if _conn_val in _conn_opts else 0
                connectivity = st.selectbox(
                    f"{src} - Network Connectivity",
                    _conn_opts,
                    index=_conn_idx,
                    key=f"conn_{src}",
                )

            scol1, scol2, scol3 = st.columns(3)
            with scol1:
                src_data_size = st.number_input(
                    f"{src} - Estimated Data Size (GB)",
                    min_value=0.0,
                    max_value=10000000.0,
                    value=float(_sd.get("data_size_gb", 0) or 0),
                    step=100.0,
                    key=f"size_{src}",
                )
            with scol2:
                src_table_count = st.number_input(
                    f"{src} - No. of Tables",
                    min_value=0,
                    max_value=1000000,
                    value=int(_sd.get("table_count", 0) or 0),
                    step=50,
                    key=f"tbl_{src}",
                )
            with scol3:
                src_largest_table = st.text_input(
                    f"{src} - Largest Table Size (approx)",
                    value=str(_sd.get("largest_table", "")),
                    key=f"lgtbl_{src}",
                    placeholder="e.g. 500 GB, 2 billion rows",
                )

            detail = {
                "version": version,
                "hosting": hosting,
                "connectivity": connectivity,
                "data_size_gb": src_data_size,
                "table_count": src_table_count,
                "largest_table": src_largest_table,
            }

            if src == "Oracle":
                st.markdown("**Oracle-Specific Details**")
                oc1, oc2, oc3 = st.columns(3)
                with oc1:
                    detail["rac_enabled"] = st.checkbox(
                        "RAC (Real Application Clusters)?", key="oracle_rac"
                    )
                    detail["partitioning"] = st.checkbox(
                        "Uses Partitioning?", key="oracle_part"
                    )
                with oc2:
                    detail["plsql_packages"] = st.number_input(
                        "No. of PL/SQL Packages",
                        min_value=0,
                        max_value=50000,
                        value=0,
                        step=10,
                        key="oracle_pkg",
                    )
                    detail["plsql_procedures"] = st.number_input(
                        "No. of Standalone Procedures / Functions",
                        min_value=0,
                        max_value=50000,
                        value=0,
                        step=10,
                        key="oracle_proc",
                    )
                with oc3:
                    detail["materialized_views"] = st.number_input(
                        "No. of Materialized Views",
                        min_value=0,
                        max_value=50000,
                        value=0,
                        step=10,
                        key="oracle_mv",
                    )
                    detail["dblinks"] = st.number_input(
                        "No. of DB Links",
                        min_value=0,
                        max_value=5000,
                        value=0,
                        step=1,
                        key="oracle_dblinks",
                    )
                oc4, oc5 = st.columns(2)
                with oc4:
                    detail["triggers"] = st.number_input(
                        "No. of Triggers",
                        min_value=0,
                        max_value=50000,
                        value=0,
                        step=10,
                        key="oracle_triggers",
                    )
                with oc5:
                    detail["synonyms"] = st.number_input(
                        "No. of Synonyms",
                        min_value=0,
                        max_value=50000,
                        value=0,
                        step=10,
                        key="oracle_synonyms",
                    )
                detail["oracle_features"] = st.multiselect(
                    "Oracle Features in Use",
                    [
                        "Advanced Queuing (AQ)",
                        "Spatial / GIS",
                        "XMLDB",
                        "Oracle Text",
                        "Flashback",
                        "Data Guard",
                        "Golden Gate",
                        "Exadata",
                        "Autonomous DB",
                    ],
                    key="oracle_features",
                )

            elif src == "Teradata":
                st.markdown("**Teradata-Specific Details**")
                tc1, tc2, tc3 = st.columns(3)
                with tc1:
                    detail["bteq_scripts"] = st.number_input(
                        "No. of BTEQ Scripts",
                        min_value=0,
                        max_value=50000,
                        value=0,
                        step=10,
                        key="td_bteq",
                    )
                    detail["fastload_mload"] = st.number_input(
                        "No. of FastLoad / MultiLoad Scripts",
                        min_value=0,
                        max_value=50000,
                        value=0,
                        step=10,
                        key="td_fl",
                    )
                with tc2:
                    detail["tpump_scripts"] = st.number_input(
                        "No. of TPump Scripts",
                        min_value=0,
                        max_value=50000,
                        value=0,
                        step=10,
                        key="td_tpump",
                    )
                    detail["stored_procedures"] = st.number_input(
                        "No. of Stored Procedures",
                        min_value=0,
                        max_value=50000,
                        value=0,
                        step=10,
                        key="td_sp",
                    )
                with tc3:
                    detail["macros"] = st.number_input(
                        "No. of Macros",
                        min_value=0,
                        max_value=50000,
                        value=0,
                        step=10,
                        key="td_macros",
                    )
                detail["teradata_features"] = st.multiselect(
                    "Teradata Features in Use",
                    [
                        "Temporal Tables",
                        "Queue Tables",
                        "Join Index",
                        "Teradata Columnar",
                        "UDFs (C/C++)",
                        "Teradata Unity",
                        "Teradata QueryGrid",
                    ],
                    key="td_features",
                )

            elif src == "SQL Server":
                st.markdown("**SQL Server-Specific Details**")
                sc1, sc2, sc3 = st.columns(3)
                with sc1:
                    detail["ssis_packages"] = st.number_input(
                        "No. of SSIS Packages",
                        min_value=0,
                        max_value=50000,
                        value=0,
                        step=10,
                        key="ss_ssis",
                    )
                    detail["ssrs_reports"] = st.number_input(
                        "No. of SSRS Reports",
                        min_value=0,
                        max_value=50000,
                        value=0,
                        step=10,
                        key="ss_ssrs",
                    )
                with sc2:
                    detail["ssas_cubes"] = st.number_input(
                        "No. of SSAS Cubes / Models",
                        min_value=0,
                        max_value=5000,
                        value=0,
                        step=1,
                        key="ss_ssas",
                    )
                    detail["stored_procedures"] = st.number_input(
                        "No. of Stored Procedures",
                        min_value=0,
                        max_value=50000,
                        value=0,
                        step=10,
                        key="ss_sp",
                    )
                with sc3:
                    detail["agent_jobs"] = st.number_input(
                        "No. of SQL Agent Jobs",
                        min_value=0,
                        max_value=10000,
                        value=0,
                        step=5,
                        key="ss_jobs",
                    )
                    detail["linked_servers"] = st.number_input(
                        "No. of Linked Servers",
                        min_value=0,
                        max_value=500,
                        value=0,
                        step=1,
                        key="ss_linked",
                    )
                detail["sql_server_features"] = st.multiselect(
                    "SQL Server Features in Use",
                    [
                        "Always On AG",
                        "Replication (Transactional/Merge)",
                        "Change Data Capture (CDC)",
                        "Change Tracking",
                        "Full-Text Search",
                        "CLR Integration",
                        "Service Broker",
                        "In-Memory OLTP",
                        "PolyBase",
                        "Temporal Tables",
                    ],
                    key="ss_features",
                )

            elif src in ("Amazon Redshift", "Azure Synapse"):
                st.markdown(f"**{src}-Specific Details**")
                rc1, rc2 = st.columns(2)
                prefix = src.replace(" ", "_").lower()
                with rc1:
                    detail["stored_procedures"] = st.number_input(
                        "No. of Stored Procedures",
                        min_value=0,
                        max_value=50000,
                        value=0,
                        step=10,
                        key=f"{prefix}_sp",
                    )
                    detail["external_tables"] = st.number_input(
                        "No. of External Tables (Spectrum / External Data)",
                        min_value=0,
                        max_value=50000,
                        value=0,
                        step=10,
                        key=f"{prefix}_ext",
                    )
                with rc2:
                    detail["udfs"] = st.number_input(
                        "No. of UDFs",
                        min_value=0,
                        max_value=10000,
                        value=0,
                        step=5,
                        key=f"{prefix}_udf",
                    )
                    detail["materialized_views"] = st.number_input(
                        "No. of Materialized Views",
                        min_value=0,
                        max_value=10000,
                        value=0,
                        step=5,
                        key=f"{prefix}_mv",
                    )

            elif src == "Google BigQuery":
                st.markdown("**BigQuery-Specific Details**")
                bc1, bc2 = st.columns(2)
                with bc1:
                    detail["datasets"] = st.number_input(
                        "No. of Datasets",
                        min_value=0,
                        max_value=10000,
                        value=0,
                        step=5,
                        key="bq_ds",
                    )
                    detail["scheduled_queries"] = st.number_input(
                        "No. of Scheduled Queries",
                        min_value=0,
                        max_value=10000,
                        value=0,
                        step=5,
                        key="bq_sq",
                    )
                with bc2:
                    detail["stored_procedures"] = st.number_input(
                        "No. of Routines (Procedures / Functions)",
                        min_value=0,
                        max_value=10000,
                        value=0,
                        step=5,
                        key="bq_sp",
                    )
                    detail["ml_models"] = st.number_input(
                        "No. of BigQuery ML Models",
                        min_value=0,
                        max_value=1000,
                        value=0,
                        step=1,
                        key="bq_ml",
                    )

            elif src == "Databricks":
                st.markdown("**Databricks-Specific Details**")
                dc1, dc2 = st.columns(2)
                with dc1:
                    detail["notebooks"] = st.number_input(
                        "No. of Notebooks",
                        min_value=0,
                        max_value=50000,
                        value=0,
                        step=10,
                        key="db_nb",
                    )
                    detail["delta_tables"] = st.number_input(
                        "No. of Delta Tables",
                        min_value=0,
                        max_value=50000,
                        value=0,
                        step=10,
                        key="db_delta",
                    )
                with dc2:
                    detail["jobs"] = st.number_input(
                        "No. of Scheduled Jobs / Workflows",
                        min_value=0,
                        max_value=10000,
                        value=0,
                        step=5,
                        key="db_jobs",
                    )
                    detail["unity_catalog"] = st.checkbox(
                        "Uses Unity Catalog?", key="db_uc"
                    )

            else:
                gc1, gc2 = st.columns(2)
                with gc1:
                    detail["stored_procedures"] = st.number_input(
                        "No. of Stored Procedures / Functions",
                        min_value=0,
                        max_value=50000,
                        value=0,
                        step=10,
                        key=f"{src}_sp_generic",
                    )
                with gc2:
                    detail["custom_objects"] = st.number_input(
                        "No. of Custom / Proprietary Objects",
                        min_value=0,
                        max_value=50000,
                        value=0,
                        step=10,
                        key=f"{src}_custom_generic",
                    )

            detail["notes"] = st.text_area(
                f"Additional notes for {src}",
                value=str(_sd.get("notes", "")),
                key=f"notes_{src}",
                height=80,
                placeholder=f"Any special considerations for {src} migration...",
            )
            source_details[src] = detail

    st.session_state.assessment["source_systems"] = source_systems
    st.session_state.assessment["source_details"] = source_details

# ─────────────────────────────────────────────────────────
# TAB 3 : DATA & VOLUME
# ─────────────────────────────────────────────────────────
with tab3:
    st.markdown(
        '<div class="section-header">Data Volume & Complexity</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        total_data_size = st.number_input(
            "Total Data Size (TB)", min_value=0.0, max_value=100000.0,
            value=float(loaded_vol.get("total_data_size", 1.0) or 1.0), step=0.5
        )
        _dsu_opts = ["TB", "GB", "PB"]
        _dsu_val = loaded_vol.get("data_size_unit", "TB")
        _dsu_idx = _dsu_opts.index(_dsu_val) if _dsu_val in _dsu_opts else 0
        data_size_unit = st.selectbox("Size Unit", _dsu_opts, index=_dsu_idx)
    with col2:
        total_tables = st.number_input(
            "Total No. of Tables", min_value=0, max_value=1000000,
            value=int(loaded_vol.get("total_tables", 100) or 100), step=50
        )
        total_views = st.number_input(
            "Total No. of Views", min_value=0, max_value=500000,
            value=int(loaded_vol.get("total_views", 50) or 50), step=10
        )
    with col3:
        total_databases = st.number_input(
            "Total No. of Databases / Schemas",
            min_value=0, max_value=10000,
            value=int(loaded_vol.get("total_databases", 5) or 5), step=1,
        )
        total_users = st.number_input(
            "Total No. of Active Users / Consumers",
            min_value=0, max_value=100000,
            value=int(loaded_vol.get("total_users", 50) or 50), step=10,
        )

    st.markdown(
        '<div class="section-header">Data Characteristics</div>',
        unsafe_allow_html=True,
    )

    col4, col5 = st.columns(2)
    with col4:
        _dt_all = [
                "Structured (relational tables)",
                "Semi-structured (JSON, XML, Avro, Parquet, ORC)",
                "Unstructured (images, PDFs, videos, audio)",
                "Geospatial data",
                "Time-series data",
                "Graph / Network data",
            ]
        data_types = st.multiselect(
            "Data Types Present", _dt_all,
            default=[d for d in loaded_vol.get("data_types", []) if d in _dt_all],
        )
        _df_opts = [
                "Batch (daily/weekly)",
                "Micro-batch (hourly)",
                "Near Real-Time (minutes)",
                "Real-Time (seconds)",
                "Streaming (sub-second)",
            ]
        _df_val = loaded_vol.get("data_freshness", "Batch (daily/weekly)")
        if _df_val not in _df_opts: _df_val = "Batch (daily/weekly)"
        data_freshness = st.select_slider("Data Freshness Requirement", options=_df_opts, value=_df_val)
    with col5:
        _ds_all = [
                "Public",
                "Internal / Confidential",
                "PII (Personally Identifiable Information)",
                "PHI (Protected Health Information)",
                "PCI (Payment Card Industry)",
                "Financial / Trading Data",
                "Classified / Government",
            ]
        data_sensitivity = st.multiselect(
            "Data Sensitivity Classification", _ds_all,
            default=[d for d in loaded_vol.get("data_sensitivity", []) if d in _ds_all],
        )
        _dr_opts = ["< 1 year", "1-3 years", "3-5 years", "5-7 years", "7-10 years", "> 10 years"]
        _dr_val = loaded_vol.get("data_retention", "3-5 years")
        if _dr_val not in _dr_opts: _dr_val = "3-5 years"
        data_retention = st.select_slider("Data Retention Requirement", options=_dr_opts, value=_dr_val)

    st.markdown(
        '<div class="section-header">Workload Profile</div>', unsafe_allow_html=True
    )
    col6, col7, col8 = st.columns(3)
    with col6:
        daily_queries = st.number_input(
            "Avg Daily Query Volume", min_value=0, max_value=100000000,
            value=int(loaded_vol.get("daily_queries", 10000) or 10000), step=1000,
        )
        concurrent_users = st.number_input(
            "Peak Concurrent Users / Queries", min_value=0, max_value=10000,
            value=int(loaded_vol.get("concurrent_users", 50) or 50), step=10,
        )
    with col7:
        _wm_opts = ["Heavy Write (80%+)", "Write-Heavy (60-80%)", "Balanced", "Read-Heavy (60-80%)", "Heavy Read (80%+)"]
        _wm_val = loaded_vol.get("workload_mix", "Read-Heavy (60-80%)")
        if _wm_val not in _wm_opts: _wm_val = "Read-Heavy (60-80%)"
        workload_mix = st.select_slider("Workload Mix (Read vs Write)", options=_wm_opts, value=_wm_val)
    with col8:
        _ew_opts = ["No batch window (24/7)", "< 2 hours", "2-4 hours", "4-8 hours", "8-12 hours", "> 12 hours"]
        _ew_val = loaded_vol.get("etl_window", _ew_opts[0])
        _ew_idx = _ew_opts.index(_ew_val) if _ew_val in _ew_opts else 0
        etl_window = st.selectbox("Current ETL / Batch Window", _ew_opts, index=_ew_idx)

    _dg_opts = ["< 10%", "10-25%", "25-50%", "50-100%", "100-200%", "> 200%"]
    _dg_val = loaded_vol.get("data_growth", "25-50%")
    if _dg_val not in _dg_opts: _dg_val = "25-50%"
    data_growth = st.select_slider("Annual Data Growth Rate", options=_dg_opts, value=_dg_val)

    st.markdown(
        '<div class="section-header">Scheduled Jobs & Reports</div>',
        unsafe_allow_html=True,
    )
    jcol1, jcol2, jcol3 = st.columns(3)
    with jcol1:
        scheduled_jobs = st.number_input(
            "Total Scheduled Jobs / ETL Pipelines", min_value=0, max_value=100000,
            value=int(loaded_vol.get("scheduled_jobs", 0) or 0), step=10,
        )
    with jcol2:
        scheduled_reports = st.number_input(
            "Total Scheduled Reports", min_value=0, max_value=100000,
            value=int(loaded_vol.get("scheduled_reports", 0) or 0), step=10,
        )
    with jcol3:
        data_feeds = st.number_input(
            "Inbound / Outbound Data Feeds", min_value=0, max_value=10000,
            value=int(loaded_vol.get("data_feeds", 0) or 0), step=5,
        )

    st.session_state.assessment["volume"] = {
        "total_data_size": total_data_size,
        "data_size_unit": data_size_unit,
        "total_tables": total_tables,
        "total_views": total_views,
        "total_databases": total_databases,
        "total_users": total_users,
        "data_types": data_types,
        "data_freshness": data_freshness,
        "data_sensitivity": data_sensitivity,
        "data_retention": data_retention,
        "daily_queries": daily_queries,
        "concurrent_users": concurrent_users,
        "workload_mix": workload_mix,
        "etl_window": etl_window,
        "data_growth": data_growth,
        "scheduled_jobs": scheduled_jobs,
        "scheduled_reports": scheduled_reports,
        "data_feeds": data_feeds,
    }

# ─────────────────────────────────────────────────────────
# TAB 4 : ETL & INGESTION TOOLS
# ─────────────────────────────────────────────────────────
with tab4:
    st.markdown(
        '<div class="section-header">Current ETL / ELT / Data Integration Tools</div>',
        unsafe_allow_html=True,
    )

    current_etl = st.multiselect(
        "Current ETL / ELT Tools in Use", ETL_TOOLS, key="current_etl"
    )

    etl_details = {}
    for tool in current_etl:
        if tool not in ("None / Not Applicable",):
            with st.expander(f"Details for: {tool}", expanded=True):
                tc1, tc2 = st.columns(2)
                with tc1:
                    pipeline_count = st.number_input(
                        f"{tool} - No. of Pipelines / Jobs",
                        min_value=0,
                        max_value=100000,
                        value=0,
                        step=10,
                        key=f"etl_pipe_{tool}",
                    )
                    satisfaction = st.select_slider(
                        f"{tool} - Satisfaction Level",
                        options=[
                            "Very Dissatisfied",
                            "Dissatisfied",
                            "Neutral",
                            "Satisfied",
                            "Very Satisfied",
                        ],
                        value="Neutral",
                        key=f"etl_sat_{tool}",
                    )
                with tc2:
                    etl_retention = st.radio(
                        f"Plan for {tool} post-migration?",
                        ["Keep as-is", "Replace", "Considering alternatives", "Undecided"],
                        key=f"etl_plan_{tool}",
                    )
                etl_notes = st.text_area(
                    f"Notes / Concerns about {tool}",
                    key=f"etl_notes_{tool}",
                    height=80,
                    placeholder=f"E.g., licensing costs, performance issues, considering alternatives...",
                )
                etl_details[tool] = {
                    "pipeline_count": pipeline_count,
                    "satisfaction": satisfaction,
                    "plan": etl_retention,
                    "notes": etl_notes,
                }

    st.markdown(
        '<div class="section-header">Annual Tooling Costs</div>',
        unsafe_allow_html=True,
    )
    cost_col1, cost_col2 = st.columns(2)
    with cost_col1:
        annual_etl_cost = st.text_input(
            "Annual ETL / ELT Tool Licensing Cost (approx)",
            placeholder="e.g. $120,000 / year for Fivetran",
            key="annual_etl_cost",
        )
    with cost_col2:
        annual_infra_cost = st.text_input(
            "Annual Legacy Infrastructure Cost (approx)",
            placeholder="e.g. $500,000 / year for Oracle licensing + hardware",
            key="annual_infra_cost",
        )

    st.markdown(
        '<div class="section-header">Change Data Capture (CDC) Requirements</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="info-box">'
        "CDC is critical for incremental data loading and real-time sync. Understanding current "
        "CDC mechanisms helps design the target Snowflake ingestion pipeline."
        "</div>",
        unsafe_allow_html=True,
    )
    cdc_col1, cdc_col2 = st.columns(2)
    with cdc_col1:
        current_cdc = st.multiselect(
            "Current CDC Mechanisms in Use",
            [
                "None (full refresh only)",
                "Timestamp-based (watermark columns)",
                "Database-native CDC (Oracle LogMiner, SQL Server CDC, etc.)",
                "Trigger-based CDC",
                "Log-based CDC (Debezium / Kafka Connect)",
                "Fivetran / Hevo CDC connectors",
                "Golden Gate (Oracle)",
                "Qlik Replicate / Attunity",
                "AWS DMS",
                "Custom scripts",
            ],
            key="current_cdc",
        )
    with cdc_col2:
        cdc_tables = st.number_input(
            "No. of Tables Requiring CDC / Incremental Sync",
            min_value=0,
            max_value=100000,
            value=0,
            step=10,
            key="cdc_table_count",
        )
        cdc_latency = st.selectbox(
            "Required CDC Latency",
            [
                "Daily batch is sufficient",
                "Hourly",
                "Minutes (near real-time)",
                "Seconds (real-time)",
                "Sub-second (streaming)",
            ],
            key="cdc_latency",
        )

    st.markdown(
        '<div class="section-header">Snowflake-Native Ingestion Preferences</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="info-box">'
        "Snowflake offers several native ingestion approaches: COPY INTO (bulk), Snowpipe (continuous), "
        "Snowpipe Streaming (real-time API), and the Kafka Connector. Select preferences below."
        "</div>",
        unsafe_allow_html=True,
    )

    ingestion_prefs = st.multiselect(
        "Preferred Snowflake Ingestion Methods (select all of interest)",
        [
            "COPY INTO (Bulk Loading)",
            "Snowpipe (Auto-ingest via cloud notifications)",
            "Snowpipe Streaming (Low-latency API)",
            "Kafka Connector for Snowflake",
            "External Tables (query-in-place)",
            "Dynamic Tables (declarative pipelines)",
            "Streams & Tasks (CDC + scheduling)",
            "Not sure / Need guidance",
        ],
        key="ingestion_prefs",
    )

    st.session_state.assessment["etl"] = {
        "current_tools": current_etl,
        "tool_details": etl_details,
        "ingestion_preferences": ingestion_prefs,
        "annual_etl_cost": annual_etl_cost,
        "annual_infra_cost": annual_infra_cost,
        "current_cdc": current_cdc,
        "cdc_tables": cdc_tables,
        "cdc_latency": cdc_latency,
    }

# ─────────────────────────────────────────────────────────
# TAB 5 : TRANSFORMATION & ORCHESTRATION
# ─────────────────────────────────────────────────────────
with tab5:
    st.markdown(
        '<div class="section-header">Data Transformation</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        current_transform = st.multiselect(
            "Current Transformation Tools", TRANSFORMATION_TOOLS, key="current_transform"
        )
        target_transform = st.multiselect(
            "Preferred Transformation Tools for Snowflake",
            TRANSFORMATION_TOOLS,
            key="target_transform",
        )
    with col2:
        _tc_opts = ["Simple (SQL-based)", "Moderate", "Complex (multi-step, ML features)", "Very Complex (custom code, UDFs)"]
        _tc_val = loaded_trans.get("complexity", "Moderate") if edit_mode else "Moderate"
        if _tc_val not in _tc_opts: _tc_val = "Moderate"
        transform_complexity = st.select_slider(
            "Transformation Complexity", options=_tc_opts, value=_tc_val,
        )
        _sp_opts = [
                "SnowConvert AI (Snowflake-native tool)",
                "Manual rewrite to Snowflake Scripting",
                "Convert to dbt models",
                "Rewrite as Python / Java UDFs",
                "Hybrid approach",
                "Not Applicable",
            ]
        _sp_val = loaded_trans.get("sp_conversion_strategy", _sp_opts[0]) if edit_mode else _sp_opts[0]
        _sp_idx = _sp_opts.index(_sp_val) if _sp_val in _sp_opts else 0
        sp_conversion = st.radio(
            "Stored Procedure Conversion Strategy", _sp_opts, index=_sp_idx,
        )

    st.markdown(
        '<div class="section-header">Orchestration & Scheduling</div>',
        unsafe_allow_html=True,
    )
    col3, col4 = st.columns(2)
    with col3:
        current_orch = st.multiselect(
            "Current Orchestration Tools", ORCHESTRATION_TOOLS, key="current_orch"
        )
    with col4:
        target_orch = st.multiselect(
            "Target Orchestration for Snowflake", ORCHESTRATION_TOOLS, key="target_orch"
        )

    st.markdown(
        '<div class="section-header">BI & Analytics</div>', unsafe_allow_html=True
    )
    col5, col6 = st.columns(2)
    with col5:
        current_bi = st.multiselect("Current BI Tools", BI_TOOLS, key="current_bi")
    with col6:
        target_bi = st.multiselect(
            "Target BI Tools with Snowflake", BI_TOOLS, key="target_bi"
        )

    st.markdown(
        '<div class="section-header">Data Governance & Quality</div>',
        unsafe_allow_html=True,
    )
    col7, col8 = st.columns(2)
    with col7:
        current_gov = st.multiselect(
            "Current Data Governance Tools", DATA_GOVERNANCE_TOOLS, key="current_gov"
        )
    with col8:
        target_gov = st.multiselect(
            "Target Governance for Snowflake",
            DATA_GOVERNANCE_TOOLS,
            key="target_gov",
        )

    st.markdown(
        '<div class="section-header">Data Catalog</div>',
        unsafe_allow_html=True,
    )
    cat_col1, cat_col2 = st.columns(2)
    with cat_col1:
        current_catalog = st.multiselect(
            "Current Data Catalog Tools", DATA_CATALOG_TOOLS, key="current_catalog"
        )
    with cat_col2:
        target_catalog = st.multiselect(
            "Target Catalog for Snowflake", DATA_CATALOG_TOOLS, key="target_catalog"
        )

    st.markdown(
        '<div class="section-header">Migration Validation & Testing Strategy</div>',
        unsafe_allow_html=True,
    )
    val_col1, val_col2 = st.columns(2)
    with val_col1:
        validation_strategy = st.multiselect(
            "Planned Validation Approaches",
            [
                "Row count comparison",
                "Checksum / Hash validation",
                "Column-level data comparison",
                "Business logic / KPI reconciliation",
                "Parallel run (source + Snowflake)",
                "Automated regression testing",
                "User acceptance testing (UAT)",
                "Performance benchmarking",
                "Not yet planned",
            ],
            key="validation_strategy",
        )
    with val_col2:
        parallel_run_duration = st.selectbox(
            "Planned Parallel Run Duration",
            [
                "No parallel run",
                "1 week",
                "2 weeks",
                "1 month",
                "2-3 months",
                "Until stakeholder sign-off",
                "TBD",
            ],
            key="parallel_duration",
        )
        rollback_plan = st.radio(
            "Rollback Plan Required?",
            ["Yes - full rollback capability needed", "Partial rollback", "No - one-way migration", "TBD"],
            key="rollback",
        )

    st.session_state.assessment["transformation"] = {
        "current_transform": current_transform,
        "target_transform": target_transform,
        "complexity": transform_complexity,
        "sp_conversion_strategy": sp_conversion,
        "current_orchestration": current_orch,
        "target_orchestration": target_orch,
        "current_bi": current_bi,
        "target_bi": target_bi,
        "current_governance": current_gov,
        "target_governance": target_gov,
        "current_catalog": current_catalog,
        "target_catalog": target_catalog,
        "validation_strategy": validation_strategy,
        "parallel_run_duration": parallel_run_duration,
        "rollback_plan": rollback_plan,
    }

# ─────────────────────────────────────────────────────────
# TAB 6 : ARCHITECTURE NUANCES (FREE TEXT)
# ─────────────────────────────────────────────────────────
with tab6:
    st.markdown(
        '<div class="section-header">Architecture Nuances & Customer Priorities</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="info-box">'
        "These free-text fields capture qualitative insights that help CoCo generate a truly tailored "
        "architecture. <strong>The more context you provide, the better the recommendations.</strong>"
        "</div>",
        unsafe_allow_html=True,
    )

    tooling_concerns = st.text_area(
        "Tooling Concerns & Vendor Preferences",
        value=loaded_nuances.get("tooling_concerns", ""),
        height=120,
        placeholder=(
            "Example: Customer currently uses Fivetran but is considering moving off due to "
            "high licensing costs. They prefer open-source alternatives like Airbyte. They have "
            "strong dbt expertise in-house and want to maximize its use."
        ),
        key="tooling_concerns",
    )

    cost_priorities = st.text_area(
        "Cost Priorities & Budget Constraints",
        value=loaded_nuances.get("cost_priorities", ""),
        height=120,
        placeholder=(
            "Example: Customer is highly cost-conscious. They want to minimize Snowflake credit "
            "consumption and prefer open-source solutions over commercial tools. They are open "
            "to investing engineering time to avoid recurring license costs."
        ),
        key="cost_priorities",
    )

    technical_debt = st.text_area(
        "Technical Debt & Legacy Challenges",
        value=loaded_nuances.get("technical_debt", ""),
        height=120,
        placeholder=(
            "Example: The Oracle database has 500+ PL/SQL packages with deep cross-dependencies. "
            "Many procedures use Oracle-specific features like DBMS_SCHEDULER and UTL_FILE. "
            "The codebase has 15+ years of accumulated technical debt with minimal documentation."
        ),
        key="technical_debt",
    )

    data_architecture_vision = st.text_area(
        "Target Data Architecture Vision",
        value=loaded_nuances.get("data_architecture_vision", ""),
        height=120,
        placeholder=(
            "Example: Customer wants to implement a Medallion Architecture (Bronze/Silver/Gold) "
            "with dbt for transformations. They want to leverage Snowflake's Data Sharing for "
            "cross-department collaboration and eventually build a data marketplace."
        ),
        key="arch_vision",
    )

    performance_requirements = st.text_area(
        "Performance & SLA Requirements",
        value=loaded_nuances.get("performance_requirements", ""),
        height=120,
        placeholder=(
            "Example: Dashboard queries must return within 5 seconds. ETL jobs currently take "
            "8 hours and must complete within a 4-hour window in Snowflake. They need sub-minute "
            "latency for real-time fraud detection pipeline."
        ),
        key="perf_reqs",
    )

    security_requirements = st.text_area(
        "Security & Compliance Requirements",
        value=loaded_nuances.get("security_requirements", ""),
        height=120,
        placeholder=(
            "Example: All PII must be dynamically masked based on user role. Data must be "
            "encrypted at rest and in transit. Row-level security is required for multi-tenant "
            "data. HIPAA BAA needed. Audit logging for all data access."
        ),
        key="security_reqs",
    )

    migration_risks = st.text_area(
        "Known Risks, Blockers & Dependencies",
        value=loaded_nuances.get("migration_risks", ""),
        height=120,
        placeholder=(
            "Example: Network team needs 4 weeks for VPN setup. DBA team has limited availability "
            "in Q4. Legacy system has undocumented tribal knowledge. Some stored procedures "
            "use vendor-specific features with no direct Snowflake equivalent."
        ),
        key="risks",
    )

    additional_context = st.text_area(
        "Any Other Context or Special Requirements",
        value=loaded_nuances.get("additional_context", ""),
        height=120,
        placeholder=(
            "Example: Customer is also evaluating Snowflake for AI/ML workloads using Snowpark. "
            "They want a phased approach starting with the data warehouse and later migrating "
            "data science workloads. They need Snowflake's Cortex LLM functions for NLP tasks."
        ),
        key="additional",
    )

    st.session_state.assessment["nuances"] = {
        "tooling_concerns": tooling_concerns,
        "cost_priorities": cost_priorities,
        "technical_debt": technical_debt,
        "data_architecture_vision": data_architecture_vision,
        "performance_requirements": performance_requirements,
        "security_requirements": security_requirements,
        "migration_risks": migration_risks,
        "additional_context": additional_context,
    }

# ─────────────────────────────────────────────────────────
# TAB 7 : REVIEW & SUBMIT
# ─────────────────────────────────────────────────────────
with tab7:
    st.markdown(
        '<div class="section-header">Review Your Assessment</div>',
        unsafe_allow_html=True,
    )

    if edit_mode:
        st.markdown(
            f'<div class="info-box edit-mode" style="margin-bottom:1rem;">'
            f'Reviewing edits for <strong>{st.session_state.get("edit_customer_name","")}</strong>. '
            f'Current version: <strong>v{st.session_state.get("edit_version",1)}</strong> → '
            f'Will become <strong>v{st.session_state.get("edit_version",1)+1}</strong> on update.'
            f'</div>',
            unsafe_allow_html=True,
        )

    data = st.session_state.assessment
    cust = data.get("customer", {})
    vol = data.get("volume", {})
    etl_data = data.get("etl", {})
    trans_data = data.get("transformation", {})
    nuances = data.get("nuances", {})

    checks = {
        "Customer Name": bool(cust.get("name")),
        "Industry Vertical": bool(cust.get("industry")),
        "SA Name": bool(cust.get("sa_name")),
        "Migration Drivers": bool(cust.get("migration_drivers")),
        "Source Systems": bool(data.get("source_systems")),
        "Data Size Provided": vol.get("total_data_size", 0) > 0,
        "Table Count Provided": vol.get("total_tables", 0) > 0,
        "ETL Tools Selected": bool(etl_data.get("current_tools")),
        "Ingestion Preferences": bool(etl_data.get("ingestion_preferences")),
        "Transformation Tools": bool(trans_data.get("current_transform") or trans_data.get("target_transform")),
        "Validation Strategy": bool(trans_data.get("validation_strategy")),
        "Architecture Nuances": any(v for v in nuances.values() if v),
    }
    completed = sum(checks.values())
    total = len(checks)
    pct = int((completed / total) * 100)

    st.markdown(
        '<div class="section-header">Assessment Completeness</div>',
        unsafe_allow_html=True,
    )
    _bar_color = '#2ECC71' if pct >= 80 else ('#F39C12' if pct >= 50 else '#E74C3C')
    st.markdown(
        f'<div class="progress-bar-container">'
        f'<div class="progress-bar-fill" style="width:{pct}%; background:{_bar_color};"></div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown(f"**{pct}% Complete** &mdash; {completed} of {total} sections filled", unsafe_allow_html=True)

    if pct < 100:
        missing = [k for k, v in checks.items() if not v]
        st.warning(f"Missing: {', '.join(missing)}")

    st.divider()

    if cust.get("name"):
        c1, c2, c3, c4 = st.columns(4)
        def _rc(label, value):
            return f'<div class="review-card"><div class="rc-label">{label}</div><div class="rc-value">{value}</div></div>'
        with c1:
            st.markdown(_rc("Customer", cust['name']), unsafe_allow_html=True)
            st.markdown(_rc("Industry", cust.get('industry', 'N/A')), unsafe_allow_html=True)
            st.markdown(_rc("Engagement", cust.get('engagement_type', 'N/A')), unsafe_allow_html=True)
        with c2:
            st.markdown(_rc("Solutions Architect", cust.get('sa_name', 'N/A')), unsafe_allow_html=True)
            st.markdown(_rc("Timeline", cust.get('timeline', 'N/A')), unsafe_allow_html=True)
            st.markdown(_rc("Budget Sensitivity", cust.get('budget_sensitivity', 'N/A')), unsafe_allow_html=True)
        with c3:
            st.markdown(_rc("Migration Approach", cust.get('migration_approach', 'N/A')), unsafe_allow_html=True)
            st.markdown(_rc("Snowflake Edition", cust.get('snowflake_edition', 'N/A')), unsafe_allow_html=True)
            st.markdown(_rc("Team Size", cust.get('team_size', 'N/A')), unsafe_allow_html=True)
        with c4:
            st.markdown(_rc("Data Sharing", "Yes" if cust.get('data_sharing_needed') else "No"), unsafe_allow_html=True)
            st.markdown(_rc("Iceberg Interest", "Yes" if cust.get('iceberg_interest') else "No"), unsafe_allow_html=True)
            st.markdown(_rc("Snowpark Interest", "Yes" if cust.get('snowpark_interest') else "No"), unsafe_allow_html=True)
    else:
        st.warning("Please fill in the Customer Profile tab first.")

    st.divider()

    rcol1, rcol2, rcol3, rcol4 = st.columns(4)
    with rcol1:
        st.metric("Source Systems", len(data.get("source_systems", [])))
        st.metric("Total Tables", vol.get("total_tables", 0))
    with rcol2:
        st.metric(
            "Data Size",
            f"{vol.get('total_data_size', 0)} {vol.get('data_size_unit', 'TB')}",
        )
        st.metric("ETL Tools", len(etl_data.get("current_tools", [])))
    with rcol3:
        st.metric("Active Users", vol.get("total_users", 0))
        st.metric("Daily Queries", vol.get("daily_queries", 0))
    with rcol4:
        st.metric("Scheduled Jobs", vol.get("scheduled_jobs", 0))
        st.metric("CDC Tables", etl_data.get("cdc_tables", 0))

    st.divider()

    st.markdown("**Source Systems:** " + ", ".join(data.get("source_systems", ["None selected"])))
    st.markdown(
        "**Migration Drivers:** " + ", ".join(cust.get("migration_drivers", ["None selected"]))
    )
    st.markdown(
        "**Data Freshness:** " + vol.get("data_freshness", "N/A")
        + "  |  **CDC Latency:** " + etl_data.get("cdc_latency", "N/A")
    )
    st.markdown(
        "**Validation:** " + ", ".join(trans_data.get("validation_strategy", ["Not planned"]))
        + "  |  **Parallel Run:** " + trans_data.get("parallel_run_duration", "N/A")
    )

    if etl_data.get("annual_etl_cost") or etl_data.get("annual_infra_cost"):
        st.markdown(
            f"**Annual ETL Cost:** {etl_data.get('annual_etl_cost', 'N/A')}"
            f"  |  **Annual Infra Cost:** {etl_data.get('annual_infra_cost', 'N/A')}"
        )

    st.divider()

    has_nuances = any(v for v in nuances.values() if v)
    if has_nuances:
        st.markdown("**Architecture Nuances Provided:**")
        nuance_labels = {
            "tooling_concerns": "Tooling Concerns",
            "cost_priorities": "Cost Priorities",
            "technical_debt": "Technical Debt",
            "data_architecture_vision": "Architecture Vision",
            "performance_requirements": "Performance Requirements",
            "security_requirements": "Security Requirements",
            "migration_risks": "Risks & Blockers",
            "additional_context": "Additional Context",
        }
        for key, label in nuance_labels.items():
            val = nuances.get(key, "")
            if val:
                st.markdown(f"- **{label}:** {val[:200]}{'...' if len(val) > 200 else ''}")
    else:
        st.info("No architecture nuances provided yet. Consider filling in Tab 6.")

    st.divider()

    _ind_val = cust.get("industry", "")
    _ind_intel = INDUSTRY_INTELLIGENCE.get(_ind_val)
    if _ind_intel:
        st.markdown(
            '<div class="section-header">Industry Intelligence Preview</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div style="padding:14px 18px;border-radius:8px;margin-bottom:1rem;font-size:0.88rem;'
            f'line-height:1.5;border-left:4px solid #B3D943;background:rgba(179,217,67,0.06);">'
            f'Based on the <strong>{_ind_val}</strong> vertical, CoCo will include industry-specific '
            f'use cases, peer customer stories, and a tailored data model in the migration plan. '
            f'Companies like <strong>{", ".join(_ind_intel["peer_companies"][:3])}</strong> have '
            f'successfully migrated to Snowflake from similar source systems.</div>',
            unsafe_allow_html=True,
        )

        _uc_col, _peer_col = st.columns(2)
        with _uc_col:
            st.markdown("**Post-Migration Use Cases CoCo Will Recommend:**")
            for _uc in _ind_intel["top_use_cases"]:
                st.markdown(f"- {_uc}")
        with _peer_col:
            st.markdown("**Peer Companies on Snowflake:**")
            for _pc in _ind_intel["peer_companies"]:
                st.markdown(f"- {_pc}")

        _dm_col, _feat_col = st.columns(2)
        with _dm_col:
            st.markdown(f'**Recommended Data Model:** {_ind_intel["data_model"]}')
        with _feat_col:
            st.markdown(f'**Key Snowflake Features:** {", ".join(_ind_intel["key_features"][:4])}')
    elif _ind_val:
        st.markdown(
            '<div class="section-header">Industry Intelligence Preview</div>',
            unsafe_allow_html=True,
        )
        st.info(
            f'Industry "{_ind_val}" will be matched to the closest vertical in CoCo\'s knowledge base '
            f'when generating the migration plan.'
        )

    st.divider()

    with st.expander("Full Assessment JSON (for debugging)", expanded=False):
        st.json(data)

    st.markdown("---")

    col_submit, col_status = st.columns([1, 3])
    with col_submit:
        if edit_mode:
            submit = st.button("Update Assessment", type="primary", use_container_width=True)
        else:
            submit = st.button("Submit Assessment", type="primary", use_container_width=True)

    if submit:
        if not cust.get("name"):
            st.error("Customer Name is required. Please fill in Tab 1.")
        elif not data.get("source_systems"):
            st.error("At least one Source System is required. Please fill in Tab 2.")
        else:
            try:
                data["_metadata"] = {
                    "schema_version": SCHEMA_VERSION,
                    "submitted_by": cust.get("sa_name", ""),
                    "submitted_at": datetime.utcnow().isoformat(),
                    "app_version": "2.0",
                    "completeness_pct": pct,
                }

                assessment_json = json.dumps(data, default=str)
                safe_name = cust["name"].replace("'", "''")
                safe_sa = cust.get("sa_name", "").replace("'", "''")
                safe_industry = (cust.get("industry") or "").replace("'", "''")
                safe_engagement = (cust.get("engagement_type") or "").replace("'", "''")
                source_array = ", ".join([f"'{s.replace(chr(39), chr(39)+chr(39))}'" for s in data.get("source_systems", [])])
                driver_array = ", ".join([f"'{d.replace(chr(39), chr(39)+chr(39))}'" for d in cust.get("migration_drivers", [])])

                size_val = vol.get("total_data_size", 0)
                size_unit = vol.get("data_size_unit", "TB")
                if size_unit == "GB":
                    size_tb = size_val / 1024
                elif size_unit == "PB":
                    size_tb = size_val * 1024
                else:
                    size_tb = size_val

                customer_json = json.dumps(data.get("customer", {}), default=str)
                volume_json = json.dumps(data.get("volume", {}), default=str)
                etl_json = json.dumps(data.get("etl", {}), default=str)
                transform_json = json.dumps(data.get("transformation", {}), default=str)
                nuances_json = json.dumps(data.get("nuances", {}), default=str)
                source_details_json = json.dumps(data.get("source_details", {}), default=str)

                if edit_mode:
                    old_aid = st.session_state["edit_assessment_id"]
                    old_version = st.session_state.get("edit_version", 1)
                    new_version = old_version + 1

                    session.sql(f"""
                        INSERT INTO {VERSION_HISTORY_TABLE}
                        (ASSESSMENT_ID, VERSION_NUMBER, CUSTOMER_NAME, SA_NAME, CHANGE_SUMMARY,
                         FULL_SNAPSHOT, CUSTOMER_DATA, VOLUME_DATA, ETL_DATA,
                         TRANSFORMATION_DATA, NUANCES_DATA, SOURCE_DETAILS,
                         COMPLETENESS_PCT, STATUS, CREATED_BY)
                        SELECT
                            ASSESSMENT_ID, COALESCE(VERSION_NUMBER, 1), CUSTOMER_NAME, SA_NAME,
                            'Snapshot before v{new_version} update',
                            FULL_ASSESSMENT, CUSTOMER_DATA, VOLUME_DATA, ETL_DATA,
                            TRANSFORMATION_DATA, NUANCES_DATA, SOURCE_DETAILS,
                            COMPLETENESS_PCT, STATUS, '{safe_sa}'
                        FROM {ASSESSMENTS_TABLE}
                        WHERE ASSESSMENT_ID = '{old_aid}'
                    """).collect()

                    cloud_arr = ", ".join([f"''{c.replace(chr(39), chr(39)+chr(39))}''" for c in cust.get("current_cloud", [])])
                    comp_arr = ", ".join([f"''{c.replace(chr(39), chr(39)+chr(39))}''" for c in cust.get("compliance", [])])

                    session.sql(f"""
                        UPDATE {ASSESSMENTS_TABLE} SET
                            CUSTOMER_NAME = '{safe_name}',
                            SA_NAME = '{safe_sa}',
                            SA_EMAIL = '{(cust.get("sa_email") or "").replace("'", "''")}',
                            CUSTOMER_WEBSITE = '{(cust.get("website") or "").replace("'", "''")}',
                            INDUSTRY = '{safe_industry}',
                            ENGAGEMENT_TYPE = '{safe_engagement}',
                            COMPLETENESS_PCT = {pct},
                            SOURCE_SYSTEMS = ARRAY_CONSTRUCT({source_array}),
                            MIGRATION_DRIVERS = ARRAY_CONSTRUCT({driver_array}),
                            BUDGET_SENSITIVITY = '{(cust.get("budget_sensitivity") or "").replace("'", "''")}',
                            TIMELINE = '{(cust.get("timeline") or "").replace("'", "''")}',
                            MIGRATION_APPROACH = '{(cust.get("migration_approach") or "").replace("'", "''")}',
                            SNOWFLAKE_EDITION = '{(cust.get("snowflake_edition") or "").replace("'", "''")}',
                            CURRENT_CLOUD = ARRAY_CONSTRUCT({cloud_arr}),
                            TARGET_CLOUD = '{(cust.get("target_cloud") or "").replace("'", "''")}',
                            COMPLIANCE_REQS = ARRAY_CONSTRUCT({comp_arr}),
                            TEAM_SIZE = {cust.get("team_size", 0)},
                            DATA_SHARING_NEEDED = {str(cust.get("data_sharing_needed", False)).upper()},
                            ICEBERG_INTEREST = {str(cust.get("iceberg_interest", False)).upper()},
                            SNOWPARK_INTEREST = {str(cust.get("snowpark_interest", False)).upper()},
                            TOTAL_DATA_SIZE_TB = {size_tb},
                            TOTAL_TABLES = {vol.get("total_tables", 0)},
                            TOTAL_USERS = {vol.get("total_users", 0)},
                            CUSTOMER_DATA = PARSE_JSON('{customer_json.replace(chr(39), chr(39)+chr(39))}'),
                            VOLUME_DATA = PARSE_JSON('{volume_json.replace(chr(39), chr(39)+chr(39))}'),
                            ETL_DATA = PARSE_JSON('{etl_json.replace(chr(39), chr(39)+chr(39))}'),
                            TRANSFORMATION_DATA = PARSE_JSON('{transform_json.replace(chr(39), chr(39)+chr(39))}'),
                            NUANCES_DATA = PARSE_JSON('{nuances_json.replace(chr(39), chr(39)+chr(39))}'),
                            SOURCE_DETAILS = PARSE_JSON('{source_details_json.replace(chr(39), chr(39)+chr(39))}'),
                            FULL_ASSESSMENT = PARSE_JSON('{assessment_json.replace(chr(39), chr(39)+chr(39))}'),
                            VERSION_NUMBER = {new_version},
                            UPDATED_AT = CURRENT_TIMESTAMP(),
                            STATUS = 'UPDATED'
                        WHERE ASSESSMENT_ID = '{old_aid}'
                    """).collect()

                    session.sql(f"DELETE FROM {SOURCE_SYSTEMS_TABLE} WHERE ASSESSMENT_ID = '{old_aid}'").collect()
                    session.sql(f"DELETE FROM {ETL_TOOLS_TABLE} WHERE ASSESSMENT_ID = '{old_aid}'").collect()

                    source_details = data.get("source_details", {})
                    for src_name, details in source_details.items():
                        safe_src = src_name.replace("'", "''")
                        specific_keys = {k: v for k, v in details.items()
                                         if k not in ("version", "hosting", "connectivity",
                                                       "data_size_gb", "table_count", "largest_table", "notes")}
                        specific_json = json.dumps(specific_keys, default=str)
                        session.sql(f"""
                            INSERT INTO {SOURCE_SYSTEMS_TABLE}
                            (ASSESSMENT_ID, SOURCE_SYSTEM, VERSION, HOSTING, CONNECTIVITY,
                             DATA_SIZE_GB, TABLE_COUNT, LARGEST_TABLE, SYSTEM_SPECIFIC_DETAILS, NOTES)
                            SELECT
                                '{old_aid}',
                                '{safe_src}',
                                '{str(details.get("version", "")).replace("'", "''")}',
                                '{str(details.get("hosting", "")).replace("'", "''")}',
                                '{str(details.get("connectivity", "")).replace("'", "''")}',
                                {details.get("data_size_gb", 0)},
                                {details.get("table_count", 0)},
                                '{str(details.get("largest_table", "")).replace("'", "''")}',
                                PARSE_JSON('{specific_json.replace(chr(39), chr(39)+chr(39))}'),
                                '{str(details.get("notes", "")).replace("'", "''")}'
                        """).collect()

                    etl_details = data.get("etl", {}).get("tool_details", {})
                    for tool_name, tool_info in etl_details.items():
                        safe_tool = tool_name.replace("'", "''")
                        session.sql(f"""
                            INSERT INTO {ETL_TOOLS_TABLE}
                            (ASSESSMENT_ID, TOOL_NAME, PIPELINE_COUNT, SATISFACTION,
                             POST_MIGRATION_PLAN, NOTES)
                            SELECT
                                '{old_aid}',
                                '{safe_tool}',
                                {tool_info.get("pipeline_count", 0)},
                                '{str(tool_info.get("satisfaction", "")).replace("'", "''")}',
                                '{str(tool_info.get("plan", "")).replace("'", "''")}',
                                '{str(tool_info.get("notes", "")).replace("'", "''")}'
                        """).collect()

                    with col_status:
                        st.success(
                            f"Assessment for **{cust['name']}** updated to **Version {new_version}**! "
                            f"Previous version (v{old_version}) preserved in history. "
                            f"Assessment ID: `{old_aid}`"
                        )
                        st.markdown(
                            f"**Version history** saved to `{VERSION_HISTORY_TABLE}`.\n\n"
                            f"You can now ask **CoCo** to regenerate the migration plan "
                            f"using assessment ID `{old_aid}`."
                        )

                else:
                    session.sql(f"CREATE DATABASE IF NOT EXISTS {DB}").collect()
                    session.sql(f"CREATE SCHEMA IF NOT EXISTS {DB}.{SCHEMA}").collect()

                    session.sql(f"""
                        CREATE TABLE IF NOT EXISTS {ASSESSMENTS_TABLE} (
                            ASSESSMENT_ID VARCHAR DEFAULT UUID_STRING(),
                            CUSTOMER_NAME VARCHAR NOT NULL,
                            SA_NAME VARCHAR,
                            SA_EMAIL VARCHAR,
                            CUSTOMER_WEBSITE VARCHAR,
                            INDUSTRY VARCHAR,
                            ENGAGEMENT_TYPE VARCHAR,
                            SCHEMA_VERSION VARCHAR DEFAULT '{SCHEMA_VERSION}',
                            STATUS VARCHAR DEFAULT 'SUBMITTED',
                            COMPLETENESS_PCT NUMBER(5,2),
                            SOURCE_SYSTEMS ARRAY,
                            MIGRATION_DRIVERS ARRAY,
                            BUDGET_SENSITIVITY VARCHAR,
                            TIMELINE VARCHAR,
                            MIGRATION_APPROACH VARCHAR,
                            SNOWFLAKE_EDITION VARCHAR,
                            CURRENT_CLOUD ARRAY,
                            TARGET_CLOUD VARCHAR,
                            COMPLIANCE_REQS ARRAY,
                            TEAM_SIZE NUMBER,
                            DATA_SHARING_NEEDED BOOLEAN DEFAULT FALSE,
                            ICEBERG_INTEREST BOOLEAN DEFAULT FALSE,
                            SNOWPARK_INTEREST BOOLEAN DEFAULT FALSE,
                            TOTAL_DATA_SIZE_TB FLOAT,
                            TOTAL_TABLES NUMBER,
                            TOTAL_USERS NUMBER,
                            CUSTOMER_DATA VARIANT,
                            VOLUME_DATA VARIANT,
                            ETL_DATA VARIANT,
                            TRANSFORMATION_DATA VARIANT,
                            NUANCES_DATA VARIANT,
                            SOURCE_DETAILS VARIANT,
                            FULL_ASSESSMENT VARIANT,
                            SUBMITTED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
                            UPDATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
                            ARCHITECTURE_GENERATED_AT TIMESTAMP_NTZ,
                            ARCHITECTURE_PLAN VARIANT,
                            VERSION_NUMBER NUMBER DEFAULT 1,
                            PARENT_ASSESSMENT_ID VARCHAR
                        )
                    """).collect()

                    session.sql(f"""
                        CREATE TABLE IF NOT EXISTS {SOURCE_SYSTEMS_TABLE} (
                            ID VARCHAR DEFAULT UUID_STRING(),
                            ASSESSMENT_ID VARCHAR,
                            SOURCE_SYSTEM VARCHAR,
                            VERSION VARCHAR,
                            HOSTING VARCHAR,
                            CONNECTIVITY VARCHAR,
                            DATA_SIZE_GB FLOAT,
                            TABLE_COUNT NUMBER,
                            LARGEST_TABLE VARCHAR,
                            SYSTEM_SPECIFIC_DETAILS VARIANT,
                            NOTES VARCHAR,
                            CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
                        )
                    """).collect()

                    session.sql(f"""
                        CREATE TABLE IF NOT EXISTS {ETL_TOOLS_TABLE} (
                            ID VARCHAR DEFAULT UUID_STRING(),
                            ASSESSMENT_ID VARCHAR,
                            TOOL_NAME VARCHAR,
                            PIPELINE_COUNT NUMBER,
                            SATISFACTION VARCHAR,
                            POST_MIGRATION_PLAN VARCHAR,
                            NOTES VARCHAR,
                            CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
                        )
                    """).collect()

                    session.sql(f"""
                        CREATE TABLE IF NOT EXISTS {REFERENCE_ARCH_TABLE} (
                            REFERENCE_ID VARCHAR DEFAULT UUID_STRING(),
                            CUSTOMER_NAME VARCHAR,
                            INDUSTRY VARCHAR,
                            SOURCE_SYSTEMS ARRAY,
                            SOLUTION_SUMMARY VARCHAR,
                            ARCHITECTURE_DETAILS VARIANT,
                            LESSONS_LEARNED VARCHAR,
                            SUCCESS_METRICS VARIANT,
                            TAGS ARRAY,
                            ADDED_BY VARCHAR,
                            CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
                        )
                    """).collect()

                    insert_sql = f"""
                        INSERT INTO {ASSESSMENTS_TABLE}
                        (CUSTOMER_NAME, SA_NAME, SA_EMAIL, CUSTOMER_WEBSITE, INDUSTRY, ENGAGEMENT_TYPE,
                         SCHEMA_VERSION, COMPLETENESS_PCT, SOURCE_SYSTEMS, MIGRATION_DRIVERS,
                         BUDGET_SENSITIVITY, TIMELINE, MIGRATION_APPROACH, SNOWFLAKE_EDITION,
                         CURRENT_CLOUD, TARGET_CLOUD, COMPLIANCE_REQS, TEAM_SIZE,
                         DATA_SHARING_NEEDED, ICEBERG_INTEREST, SNOWPARK_INTEREST,
                         TOTAL_DATA_SIZE_TB, TOTAL_TABLES, TOTAL_USERS,
                         CUSTOMER_DATA, VOLUME_DATA, ETL_DATA, TRANSFORMATION_DATA,
                         NUANCES_DATA, SOURCE_DETAILS, FULL_ASSESSMENT, VERSION_NUMBER)
                        SELECT
                            '{safe_name}',
                            '{safe_sa}',
                            '{(cust.get("sa_email") or "").replace("'", "''")}',
                            '{(cust.get("website") or "").replace("'", "''")}',
                            '{safe_industry}',
                            '{safe_engagement}',
                            '{SCHEMA_VERSION}',
                            {pct},
                            ARRAY_CONSTRUCT({source_array}),
                            ARRAY_CONSTRUCT({driver_array}),
                            '{(cust.get("budget_sensitivity") or "").replace("'", "''")}',
                            '{(cust.get("timeline") or "").replace("'", "''")}',
                            '{(cust.get("migration_approach") or "").replace("'", "''")}',
                            '{(cust.get("snowflake_edition") or "").replace("'", "''")}',
                            ARRAY_CONSTRUCT({", ".join([f"''{c.replace(chr(39), chr(39)+chr(39))}''" for c in cust.get("current_cloud", [])])}),
                            '{(cust.get("target_cloud") or "").replace("'", "''")}',
                            ARRAY_CONSTRUCT({", ".join([f"''{c.replace(chr(39), chr(39)+chr(39))}''" for c in cust.get("compliance", [])])}),
                            {cust.get("team_size", 0)},
                            {str(cust.get("data_sharing_needed", False)).upper()},
                            {str(cust.get("iceberg_interest", False)).upper()},
                            {str(cust.get("snowpark_interest", False)).upper()},
                            {size_tb},
                            {vol.get("total_tables", 0)},
                            {vol.get("total_users", 0)},
                            PARSE_JSON('{customer_json.replace(chr(39), chr(39)+chr(39))}'),
                            PARSE_JSON('{volume_json.replace(chr(39), chr(39)+chr(39))}'),
                            PARSE_JSON('{etl_json.replace(chr(39), chr(39)+chr(39))}'),
                            PARSE_JSON('{transform_json.replace(chr(39), chr(39)+chr(39))}'),
                            PARSE_JSON('{nuances_json.replace(chr(39), chr(39)+chr(39))}'),
                            PARSE_JSON('{source_details_json.replace(chr(39), chr(39)+chr(39))}'),
                            PARSE_JSON('{assessment_json.replace(chr(39), chr(39)+chr(39))}'),
                            1
                    """
                    session.sql(insert_sql).collect()

                    result = session.sql(f"""
                        SELECT ASSESSMENT_ID FROM {ASSESSMENTS_TABLE}
                        WHERE CUSTOMER_NAME = '{safe_name}'
                        ORDER BY SUBMITTED_AT DESC LIMIT 1
                    """).collect()
                    assessment_id = result[0]["ASSESSMENT_ID"] if result else None

                    if assessment_id:
                        source_details = data.get("source_details", {})
                        for src_name, details in source_details.items():
                            safe_src = src_name.replace("'", "''")
                            specific_keys = {k: v for k, v in details.items()
                                             if k not in ("version", "hosting", "connectivity",
                                                           "data_size_gb", "table_count", "largest_table", "notes")}
                            specific_json = json.dumps(specific_keys, default=str)
                            session.sql(f"""
                                INSERT INTO {SOURCE_SYSTEMS_TABLE}
                                (ASSESSMENT_ID, SOURCE_SYSTEM, VERSION, HOSTING, CONNECTIVITY,
                                 DATA_SIZE_GB, TABLE_COUNT, LARGEST_TABLE, SYSTEM_SPECIFIC_DETAILS, NOTES)
                                SELECT
                                    '{assessment_id}',
                                    '{safe_src}',
                                    '{str(details.get("version", "")).replace("'", "''")}',
                                    '{str(details.get("hosting", "")).replace("'", "''")}',
                                    '{str(details.get("connectivity", "")).replace("'", "''")}',
                                    {details.get("data_size_gb", 0)},
                                    {details.get("table_count", 0)},
                                    '{str(details.get("largest_table", "")).replace("'", "''")}',
                                    PARSE_JSON('{specific_json.replace(chr(39), chr(39)+chr(39))}'),
                                    '{str(details.get("notes", "")).replace("'", "''")}'
                            """).collect()

                        etl_details = data.get("etl", {}).get("tool_details", {})
                        for tool_name, tool_info in etl_details.items():
                            safe_tool = tool_name.replace("'", "''")
                            session.sql(f"""
                                INSERT INTO {ETL_TOOLS_TABLE}
                                (ASSESSMENT_ID, TOOL_NAME, PIPELINE_COUNT, SATISFACTION,
                                 POST_MIGRATION_PLAN, NOTES)
                                SELECT
                                    '{assessment_id}',
                                    '{safe_tool}',
                                    {tool_info.get("pipeline_count", 0)},
                                    '{str(tool_info.get("satisfaction", "")).replace("'", "''")}',
                                    '{str(tool_info.get("plan", "")).replace("'", "''")}',
                                    '{str(tool_info.get("notes", "")).replace("'", "''")}'
                            """).collect()

                    with col_status:
                        st.success(
                            f"Assessment for **{cust['name']}** submitted successfully! "
                            f"Assessment ID: `{assessment_id}`"
                        )
                        st.markdown(
                            f"**Data saved to:**\n"
                            f"- `{ASSESSMENTS_TABLE}` — master assessment (denormalized + full VARIANT)\n"
                            f"- `{SOURCE_SYSTEMS_TABLE}` — one row per source system\n"
                            f"- `{ETL_TOOLS_TABLE}` — one row per ETL tool\n"
                            f"- `{REFERENCE_ARCH_TABLE}` — ready for reference architectures\n\n"
                            f"You can now ask **CoCo** to generate a tailored migration architecture "
                            f"by referencing assessment ID `{assessment_id}`."
                        )
            except Exception as e:
                with col_status:
                    st.error(f"Error saving assessment: {str(e)}")
                    st.code(str(e))
