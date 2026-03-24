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

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #29B5E8;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #29B5E8;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #29B5E8;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    @media (prefers-color-scheme: dark) {
        .info-box {
            background-color: rgba(41, 181, 232, 0.1);
            border-left: 4px solid #29B5E8;
            color: #FAFAFA;
        }
    }
    @media (prefers-color-scheme: light) {
        .info-box {
            background-color: rgba(30, 136, 229, 0.08);
            border-left: 4px solid #1E88E5;
            color: #1A1A1A;
        }
    }
    .info-box {
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 1rem;
        font-size: 0.9rem;
    }
    .stNumberInput > div > div > input {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-header">Snowflake Migration Assessment Portal</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="info-box">'
    "Welcome kipian! This portal captures all inputs for a customer's migration project onto Snowflake. "
    "Fill in each section as completely as possible. Once submitted, the data is persisted to Snowflake for CoCo "
    "(Cortex Code) to generate a tailored migration solution architecture."
    "</div>",
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "1. Customer Profile",
        "2. Source Systems",
        "3. Data & Volume",
        "4. ETL & Tools",
        "5. Transformation & Orchestration",
        "6. Architecture Nuances",
        "7. Review & Submit",
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
            "Customer Name *", placeholder="e.g. Acme Corporation"
        )
        customer_website = st.text_input(
            "Customer Website URL", placeholder="https://www.example.com"
        )
        industry = st.selectbox(
            "Industry Vertical *",
            [
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
            ],
        )
        if industry == "Other":
            industry = st.text_input(
                "Please specify Industry Vertical *",
                placeholder="e.g. Aerospace & Defense",
                key="custom_industry",
            )

    with col2:
        sa_name = st.text_input(
            "Solutions Architect Name *", placeholder="Your name"
        )
        sa_email = st.text_input("Solutions Architect Email", placeholder="name@kipi.ai")
        engagement_type = st.radio(
            "Engagement Type *",
            [
                "New Customer (Greenfield)",
                "Existing Customer (Expansion)",
                "POC / Proof of Concept",
            ],
            horizontal=True,
        )

    st.markdown(
        '<div class="section-header">Cloud & Region</div>', unsafe_allow_html=True
    )
    col3, col4 = st.columns(2)
    with col3:
        current_cloud = st.multiselect(
            "Customer's Current Cloud Provider(s)", CLOUD_PROVIDERS
        )
        target_cloud = st.selectbox(
            "Target Snowflake Cloud / Region",
            [
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
            ],
        )
    with col4:
        migration_drivers = st.multiselect(
            "Primary Migration Drivers (select all that apply) *", MIGRATION_DRIVERS
        )
        compliance_reqs = st.multiselect(
            "Compliance / Regulatory Requirements", COMPLIANCE_FRAMEWORKS
        )

    st.markdown(
        '<div class="section-header">Timeline & Budget</div>', unsafe_allow_html=True
    )
    col5, col6, col7 = st.columns(3)
    with col5:
        timeline = st.select_slider(
            "Expected Migration Timeline",
            options=[
                "< 1 month",
                "1-3 months",
                "3-6 months",
                "6-12 months",
                "12-18 months",
                "18-24 months",
                "> 24 months",
            ],
            value="6-12 months",
        )
    with col6:
        budget_sensitivity = st.select_slider(
            "Budget Sensitivity",
            options=[
                "Very Flexible",
                "Moderate",
                "Cost Conscious",
                "Highly Cost Sensitive",
                "Open Source Only",
            ],
            value="Moderate",
        )
    with col7:
        team_size = st.number_input(
            "Customer's Data Engineering Team Size",
            min_value=0,
            max_value=500,
            value=5,
            step=1,
        )

    st.markdown(
        '<div class="section-header">Snowflake Target Configuration</div>',
        unsafe_allow_html=True,
    )
    col8, col9, col10 = st.columns(3)
    with col8:
        sf_edition = st.selectbox("Preferred Snowflake Edition", SNOWFLAKE_EDITIONS)
    with col9:
        migration_approach = st.radio(
            "Migration Approach",
            ["Big Bang (all at once)", "Phased / Incremental", "Parallel Run", "Undecided"],
        )
    with col10:
        data_sharing_needed = st.checkbox("Requires Snowflake Data Sharing / Marketplace")
        iceberg_interest = st.checkbox("Interested in Apache Iceberg Tables")
        snowpark_interest = st.checkbox("Interested in Snowpark (Python / Java / Scala)")

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
    st.markdown(
        '<div class="info-box">'
        "Select all source systems involved in this migration. Additional fields will appear dynamically "
        "based on your selections."
        "</div>",
        unsafe_allow_html=True,
    )

    source_systems = st.multiselect(
        "Source Database Systems *", SOURCE_SYSTEMS, key="source_systems_select"
    )

    source_details = {}

    for src in source_systems:
        with st.expander(f"Details for: {src}", expanded=True):
            cols = st.columns(3)
            with cols[0]:
                version = st.text_input(
                    f"{src} - Version / Edition",
                    key=f"ver_{src}",
                    placeholder="e.g. 19c, 2019 Enterprise",
                )
            with cols[1]:
                hosting = st.selectbox(
                    f"{src} - Hosting",
                    ["On-Premises", "Cloud-hosted (IaaS)", "Managed Service (PaaS)", "SaaS"],
                    key=f"host_{src}",
                )
            with cols[2]:
                connectivity = st.selectbox(
                    f"{src} - Network Connectivity",
                    [
                        "Public Internet",
                        "VPN / VPC Peering",
                        "Private Link",
                        "Direct Connect / ExpressRoute",
                        "TBD",
                    ],
                    key=f"conn_{src}",
                )

            scol1, scol2, scol3 = st.columns(3)
            with scol1:
                src_data_size = st.number_input(
                    f"{src} - Estimated Data Size (GB)",
                    min_value=0.0,
                    max_value=10000000.0,
                    value=0.0,
                    step=100.0,
                    key=f"size_{src}",
                )
            with scol2:
                src_table_count = st.number_input(
                    f"{src} - No. of Tables",
                    min_value=0,
                    max_value=1000000,
                    value=0,
                    step=50,
                    key=f"tbl_{src}",
                )
            with scol3:
                src_largest_table = st.text_input(
                    f"{src} - Largest Table Size (approx)",
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
            "Total Data Size (TB)", min_value=0.0, max_value=100000.0, value=1.0, step=0.5
        )
        data_size_unit = st.selectbox("Size Unit", ["TB", "GB", "PB"])
    with col2:
        total_tables = st.number_input(
            "Total No. of Tables", min_value=0, max_value=1000000, value=100, step=50
        )
        total_views = st.number_input(
            "Total No. of Views", min_value=0, max_value=500000, value=50, step=10
        )
    with col3:
        total_databases = st.number_input(
            "Total No. of Databases / Schemas",
            min_value=0,
            max_value=10000,
            value=5,
            step=1,
        )
        total_users = st.number_input(
            "Total No. of Active Users / Consumers",
            min_value=0,
            max_value=100000,
            value=50,
            step=10,
        )

    st.markdown(
        '<div class="section-header">Data Characteristics</div>',
        unsafe_allow_html=True,
    )

    col4, col5 = st.columns(2)
    with col4:
        data_types = st.multiselect(
            "Data Types Present",
            [
                "Structured (relational tables)",
                "Semi-structured (JSON, XML, Avro, Parquet, ORC)",
                "Unstructured (images, PDFs, videos, audio)",
                "Geospatial data",
                "Time-series data",
                "Graph / Network data",
            ],
        )
        data_freshness = st.select_slider(
            "Data Freshness Requirement",
            options=[
                "Batch (daily/weekly)",
                "Micro-batch (hourly)",
                "Near Real-Time (minutes)",
                "Real-Time (seconds)",
                "Streaming (sub-second)",
            ],
            value="Batch (daily/weekly)",
        )
    with col5:
        data_sensitivity = st.multiselect(
            "Data Sensitivity Classification",
            [
                "Public",
                "Internal / Confidential",
                "PII (Personally Identifiable Information)",
                "PHI (Protected Health Information)",
                "PCI (Payment Card Industry)",
                "Financial / Trading Data",
                "Classified / Government",
            ],
        )
        data_retention = st.select_slider(
            "Data Retention Requirement",
            options=["< 1 year", "1-3 years", "3-5 years", "5-7 years", "7-10 years", "> 10 years"],
            value="3-5 years",
        )

    st.markdown(
        '<div class="section-header">Workload Profile</div>', unsafe_allow_html=True
    )
    col6, col7, col8 = st.columns(3)
    with col6:
        daily_queries = st.number_input(
            "Avg Daily Query Volume",
            min_value=0,
            max_value=100000000,
            value=10000,
            step=1000,
        )
        concurrent_users = st.number_input(
            "Peak Concurrent Users / Queries",
            min_value=0,
            max_value=10000,
            value=50,
            step=10,
        )
    with col7:
        workload_mix = st.select_slider(
            "Workload Mix (Read vs Write)",
            options=[
                "Heavy Write (80%+)",
                "Write-Heavy (60-80%)",
                "Balanced",
                "Read-Heavy (60-80%)",
                "Heavy Read (80%+)",
            ],
            value="Read-Heavy (60-80%)",
        )
    with col8:
        etl_window = st.selectbox(
            "Current ETL / Batch Window",
            [
                "No batch window (24/7)",
                "< 2 hours",
                "2-4 hours",
                "4-8 hours",
                "8-12 hours",
                "> 12 hours",
            ],
        )

    data_growth = st.select_slider(
        "Annual Data Growth Rate",
        options=["< 10%", "10-25%", "25-50%", "50-100%", "100-200%", "> 200%"],
        value="25-50%",
    )

    st.markdown(
        '<div class="section-header">Scheduled Jobs & Reports</div>',
        unsafe_allow_html=True,
    )
    jcol1, jcol2, jcol3 = st.columns(3)
    with jcol1:
        scheduled_jobs = st.number_input(
            "Total Scheduled Jobs / ETL Pipelines",
            min_value=0,
            max_value=100000,
            value=0,
            step=10,
        )
    with jcol2:
        scheduled_reports = st.number_input(
            "Total Scheduled Reports",
            min_value=0,
            max_value=100000,
            value=0,
            step=10,
        )
    with jcol3:
        data_feeds = st.number_input(
            "Inbound / Outbound Data Feeds",
            min_value=0,
            max_value=10000,
            value=0,
            step=5,
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
        transform_complexity = st.select_slider(
            "Transformation Complexity",
            options=["Simple (SQL-based)", "Moderate", "Complex (multi-step, ML features)", "Very Complex (custom code, UDFs)"],
            value="Moderate",
        )
        sp_conversion = st.radio(
            "Stored Procedure Conversion Strategy",
            [
                "SnowConvert AI (Snowflake-native tool)",
                "Manual rewrite to Snowflake Scripting",
                "Convert to dbt models",
                "Rewrite as Python / Java UDFs",
                "Hybrid approach",
                "Not Applicable",
            ],
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
        "These free-text fields capture qualitative insights that help CoCo (Cortex Code) "
        "generate a truly tailored solution architecture. The more context you provide, the "
        "better the recommendations will be."
        "</div>",
        unsafe_allow_html=True,
    )

    tooling_concerns = st.text_area(
        "Tooling Concerns & Vendor Preferences",
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
    st.progress(pct / 100, text=f"{pct}% Complete ({completed}/{total} sections filled)")

    if pct < 100:
        missing = [k for k, v in checks.items() if not v]
        st.warning(f"Missing: {', '.join(missing)}")

    st.divider()

    if cust.get("name"):
        st.markdown(f"**Customer:** {cust['name']}  |  **Industry:** {cust.get('industry', 'N/A')}")
        st.markdown(f"**SA:** {cust.get('sa_name', 'N/A')}  |  **Engagement:** {cust.get('engagement_type', 'N/A')}")
        st.markdown(f"**Timeline:** {cust.get('timeline', 'N/A')}  |  **Budget:** {cust.get('budget_sensitivity', 'N/A')}  |  **Approach:** {cust.get('migration_approach', 'N/A')}")
        st.markdown(f"**Snowflake Edition:** {cust.get('snowflake_edition', 'N/A')}  |  **Team Size:** {cust.get('team_size', 'N/A')}")
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

    with st.expander("Full Assessment JSON (for debugging)", expanded=False):
        st.json(data)

    st.markdown("---")

    col_submit, col_status = st.columns([1, 3])
    with col_submit:
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
                        ARCHITECTURE_PLAN VARIANT
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

                insert_sql = f"""
                    INSERT INTO {ASSESSMENTS_TABLE}
                    (CUSTOMER_NAME, SA_NAME, SA_EMAIL, CUSTOMER_WEBSITE, INDUSTRY, ENGAGEMENT_TYPE,
                     SCHEMA_VERSION, COMPLETENESS_PCT, SOURCE_SYSTEMS, MIGRATION_DRIVERS,
                     BUDGET_SENSITIVITY, TIMELINE, MIGRATION_APPROACH, SNOWFLAKE_EDITION,
                     CURRENT_CLOUD, TARGET_CLOUD, COMPLIANCE_REQS, TEAM_SIZE,
                     DATA_SHARING_NEEDED, ICEBERG_INTEREST, SNOWPARK_INTEREST,
                     TOTAL_DATA_SIZE_TB, TOTAL_TABLES, TOTAL_USERS,
                     CUSTOMER_DATA, VOLUME_DATA, ETL_DATA, TRANSFORMATION_DATA,
                     NUANCES_DATA, SOURCE_DETAILS, FULL_ASSESSMENT)
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
                        PARSE_JSON('{assessment_json.replace(chr(39), chr(39)+chr(39))}')
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
