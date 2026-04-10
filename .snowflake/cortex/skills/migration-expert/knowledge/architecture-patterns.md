# Snowflake Architecture Patterns for Migration

## 1. Medallion Architecture (Bronze / Silver / Gold)

### When to Recommend
- Customer wants layered ELT with clear data quality progression
- dbt is the transformation tool of choice
- Team has SQL expertise
- Data architecture vision mentions "Medallion" or "Bronze/Silver/Gold"

### Structure
```
DATABASE: <CUSTOMER>_DW
├── SCHEMA: BRONZE (raw ingested data, no transformations)
│   ├── Source-conformed tables (1:1 with source)
│   ├── VARIANT columns for semi-structured data
│   └── Metadata columns: _LOADED_AT, _SOURCE_FILE, _SOURCE_SYSTEM
│
├── SCHEMA: SILVER (cleaned, conformed, enriched)
│   ├── Deduplication applied
│   ├── Data types standardized
│   ├── Business keys resolved
│   ├── Cross-source entity resolution
│   └── Data quality checks passed
│
├── SCHEMA: GOLD (business-ready, consumption-optimized)
│   ├── Data marts (star schema / wide tables)
│   ├── Aggregated metrics tables
│   ├── Feature stores for ML
│   └── Reporting-ready datasets
│
└── SCHEMA: SANDBOX (exploration, data science)
    ├── Temporary analysis tables
    └── ML experiment datasets
```

### Implementation with dbt
- Bronze: dbt sources + staging models (1:1 source mapping)
- Silver: dbt intermediate models (business logic, joins, dedup)
- Gold: dbt marts (dimensional models, aggregations)
- Use dbt tags for layer management: `+tags: ["bronze"]`

### Snowflake Features to Leverage
- **Dynamic Tables**: Can replace simple Silver layer transformations
- **Streams**: Track changes in Bronze for incremental Silver processing
- **Tasks**: Schedule Silver → Gold transformations
- **Object Tagging**: Tag tables with layer metadata (BRONZE, SILVER, GOLD)

---

## 2. Data Vault 2.0

### When to Recommend
- Financial services or healthcare with heavy audit requirements
- Need full historization and traceability of every data change
- Multiple source systems feeding the same business entities
- Regulatory compliance requires immutable audit trail
- Large-scale enterprise with 10+ source systems

### Structure
```
DATABASE: <CUSTOMER>_RAW_VAULT
├── SCHEMA: RAW_VAULT
│   ├── HUBS (business keys: HUB_CUSTOMER, HUB_ACCOUNT, HUB_PRODUCT)
│   ├── LINKS (relationships: LNK_CUSTOMER_ACCOUNT, LNK_ORDER_PRODUCT)
│   ├── SATELLITES (descriptive data with history: SAT_CUSTOMER_DETAILS, SAT_CUSTOMER_PII)
│   └── Reference tables
│
├── SCHEMA: BUSINESS_VAULT
│   ├── Point-in-time tables (PIT)
│   ├── Bridge tables
│   ├── Calculated satellites (business rules applied)
│   └── Same-As Links (entity resolution)
│
└── SCHEMA: INFORMATION_MART
    ├── Dimensional views / tables
    └── Reporting aggregations
```

### Implementation
- Use dbt with `dbtvault` package (AutomateDV)
- Hash keys using MD5 or SHA-256 for Hub/Link/Satellite keys
- Load date and record source columns on every table
- Effectivity satellites for tracking relationship changes

---

## 3. Star Schema / Dimensional Modeling

### When to Recommend
- BI-heavy workloads with well-understood business domains
- Simpler transformation requirements
- Team familiar with Kimball methodology
- Customer's vision doesn't mention Medallion or Data Vault

### Structure
```
DATABASE: <CUSTOMER>_DW
├── SCHEMA: DIM (dimension tables)
│   ├── DIM_CUSTOMER (SCD Type 2 for slowly changing)
│   ├── DIM_PRODUCT
│   ├── DIM_DATE
│   ├── DIM_GEOGRAPHY
│   └── DIM_EMPLOYEE
│
├── SCHEMA: FACT (fact tables)
│   ├── FACT_SALES (transactional grain)
│   ├── FACT_INVENTORY (periodic snapshot)
│   └── FACT_DAILY_REVENUE (aggregate)
│
└── SCHEMA: STAGING (raw data loading area)
    └── STG_* tables
```

---

## 4. Data Mesh (Domain-Oriented)

### When to Recommend
- Large organizations with autonomous domain teams
- Customer mentions "data products" or "domain ownership"
- Multiple business units with independent data needs
- Data sharing between domains is a key requirement

### Structure
```
ACCOUNT: <CUSTOMER>_SNOWFLAKE

DATABASE: SALES_DOMAIN
├── SCHEMA: RAW (domain-owned ingestion)
├── SCHEMA: CURATED (domain business logic)
├── SCHEMA: DATA_PRODUCTS (published, shareable)
└── SCHEMA: INTERNAL (domain-only analytics)

DATABASE: MARKETING_DOMAIN
├── (same pattern)

DATABASE: FINANCE_DOMAIN
├── (same pattern)

DATABASE: SHARED_SERVICES
├── SCHEMA: REFERENCE_DATA (shared dimensions)
└── SCHEMA: GOVERNANCE (policies, tags, classifiers)
```

### Snowflake Features to Leverage
- **Data Sharing**: Cross-domain data product consumption (zero-copy)
- **Snowflake Marketplace**: External data product distribution
- **Object Tagging**: Domain ownership and classification
- **Row Access Policies**: Cross-domain access control
- **Listings**: Internal data marketplace for domain data products

---

## 5. Warehouse Strategy Patterns

### Standard Pattern (most customers)
```
├── WH_LOADING (X-Small to Small, auto-suspend 60s)
│   └── Purpose: COPY INTO, Snowpipe, bulk data loading
│
├── WH_TRANSFORM (Small to Medium, auto-suspend 300s)
│   └── Purpose: dbt runs, stored procedure execution, Dynamic Table refresh
│
├── WH_ANALYTICS (Small to Large, multi-cluster 1-3, auto-suspend 300s)
│   └── Purpose: BI tool queries, dashboard refresh, ad-hoc analysis
│
├── WH_DATASCIENCE (Medium, auto-suspend 60s)
│   └── Purpose: Snowpark ML, Cortex functions, exploratory analysis
│
└── WH_DEV (X-Small, auto-suspend 60s)
    └── Purpose: Development, testing, CI/CD
```

### Cost-Sensitive Pattern
```
├── WH_ETL (X-Small, auto-suspend 60s)
│   └── All loading + transformation
│
├── WH_ANALYTICS (X-Small to Small, auto-suspend 60s)
│   └── All BI + ad-hoc queries
│
└── Resource Monitor: Hard limit at monthly credit budget
```

### High-Performance Pattern
```
├── WH_STREAMING (X-Small, always-on for Snowpipe Streaming)
├── WH_LOADING (Medium, auto-suspend 120s)
├── WH_TRANSFORM (Large, auto-suspend 300s)
├── WH_ANALYTICS (Large, multi-cluster 1-10, auto-suspend 300s)
├── WH_REALTIME (Small, multi-cluster 1-5, auto-suspend 60s)
│   └── Sub-second dashboard queries
└── WH_ML (XL to 2XL, auto-suspend 60s)
    └── Model training, Snowpark ML
```

---

## 6. RBAC (Role-Based Access Control) Pattern

### Recommended Hierarchy
```
ACCOUNTADMIN
└── SYSADMIN
    ├── DB_ADMIN (DDL privileges)
    │
    ├── DATA_ENGINEER (DML on raw/staging, read on all)
    │   ├── DE_<TEAM_A>
    │   └── DE_<TEAM_B>
    │
    ├── ANALYTICS_ENGINEER (DML on transform schemas, read on raw)
    │
    ├── DATA_ANALYST (read-only on gold/mart schemas)
    │   ├── ANALYST_FINANCE
    │   ├── ANALYST_MARKETING
    │   └── ANALYST_SALES
    │
    ├── DATA_SCIENTIST (read on all, write on sandbox)
    │
    └── APPLICATION_SERVICE (service accounts for BI/ETL tools)
        ├── SVC_DBT
        ├── SVC_FIVETRAN
        ├── SVC_TABLEAU
        └── SVC_AIRFLOW

SECURITYADMIN
└── Manages role grants and masking policies

USERADMIN
└── Manages user creation
```

### Best Practices
- Never grant privileges to users directly; always through roles
- Use functional roles (DATA_ENGINEER) granted to access roles (DE_TEAM_A)
- Implement least-privilege principle
- Use FUTURE GRANTS for automatic privilege propagation
- Document role hierarchy in a RBAC matrix spreadsheet

---

## 7. CI/CD Pattern for Snowflake

### Recommended Stack
```
GitHub/GitLab
├── Feature branch → PR → Code review
├── CI pipeline (GitHub Actions / GitLab CI):
│   ├── dbt compile + dbt test (schema tests)
│   ├── SQL linting (sqlfluff)
│   ├── SnowConvert validation (for migration projects)
│   └── Unit tests (dbt unit tests or pytest)
│
├── CD pipeline (on merge to main):
│   ├── dbt run --target staging
│   ├── dbt test --target staging
│   ├── Integration tests
│   └── Promote to production (dbt run --target prod)
│
└── Environments:
    ├── DEV: Developer-specific schemas (DEV_<USERNAME>)
    ├── STAGING: Pre-production validation
    └── PROD: Production
```

### Snowflake-Specific CI/CD
- Use schemachange or Flyway for DDL migrations
- dbt Cloud has built-in CI/CD with slim CI (only run changed models)
- Snowflake Git integration for version-controlled stored procedures
- Use CLONE for zero-copy dev/test environments
