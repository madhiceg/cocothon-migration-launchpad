# Snowflake Multi-Tenancy Architecture Patterns

Reference: Snowflake Multi-Tenancy Whitepaper — MTT, OPT, APT

## Overview

Multi-tenancy in Snowflake refers to how a SaaS provider or enterprise with multiple business units/clients isolates and manages data for different tenants. Snowflake supports three primary patterns:

1. **MTT — Multi-Tenant Table** (shared everything)
2. **OPT — One Schema Per Tenant** (shared database, separate schemas)
3. **APT — Account Per Tenant** (complete isolation)

## Pattern 1: MTT (Multi-Tenant Table)

### Architecture
```
SNOWFLAKE ACCOUNT
└── DATABASE: APP_DB
    └── SCHEMA: SHARED
        ├── CUSTOMERS (TENANT_ID, customer_id, name, ...)
        ├── ORDERS (TENANT_ID, order_id, customer_id, ...)
        ├── PRODUCTS (TENANT_ID, product_id, name, ...)
        └── ... all tables include TENANT_ID column
```

### How It Works
- All tenants share the same tables
- Every table has a `TENANT_ID` (or `ORG_ID`) column
- **Row Access Policies (RAP)** enforce tenant isolation at the query level
- Single set of ETL pipelines, dbt models, and BI dashboards

### Row Access Policy Example
```sql
CREATE OR REPLACE ROW ACCESS POLICY tenant_isolation AS (tenant_id VARCHAR)
RETURNS BOOLEAN ->
    tenant_id = CURRENT_SESSION_TENANT_ID()
    OR IS_ROLE_IN_SESSION('SUPER_ADMIN');

ALTER TABLE orders ADD ROW ACCESS POLICY tenant_isolation ON (tenant_id);
```

### When to Use MTT
- **Large number of tenants** (100s to 1000s)
- **Small to medium data per tenant**
- **Cost optimization is critical** — single infrastructure, shared compute
- **Uniform schema** across all tenants (no custom columns per tenant)
- **SaaS products** with standardized data models
- **Budget sensitivity = "Highly Cost Sensitive" or "Open Source Only"**

### Advantages
- Lowest cost (shared storage, shared compute, single pipeline)
- Simplest to manage (one schema, one set of dbt models)
- Easiest to onboard new tenants (just add a TENANT_ID value)
- Aggregation across tenants is trivial (cross-tenant analytics)
- Single CI/CD pipeline

### Disadvantages
- Logical isolation only (no physical separation)
- Noisy neighbor risk if one tenant has large queries (mitigate with per-tenant warehouse routing)
- Row Access Policy overhead on every query
- Schema changes affect ALL tenants simultaneously
- May not satisfy strict compliance requirements (HIPAA, SOX with strict audit)
- Tenant-specific customizations are difficult

### Snowflake Features to Leverage
- **Row Access Policies**: Core isolation mechanism
- **Session Variables**: Set TENANT_ID at session initialization
- **Resource Monitors**: Per-tenant credit monitoring (if using separate warehouses)
- **Tagging**: Tag objects with tenant metadata for governance

---

## Pattern 2: OPT (One Schema Per Tenant)

### Architecture
```
SNOWFLAKE ACCOUNT
└── DATABASE: APP_DB
    ├── SCHEMA: TENANT_ACME
    │   ├── CUSTOMERS
    │   ├── ORDERS
    │   └── PRODUCTS
    │
    ├── SCHEMA: TENANT_GLOBEX
    │   ├── CUSTOMERS
    │   ├── ORDERS
    │   └── PRODUCTS
    │
    ├── SCHEMA: TENANT_INITECH
    │   ├── CUSTOMERS
    │   ├── ORDERS
    │   └── PRODUCTS
    │
    └── SCHEMA: SHARED (reference data, lookups)
        ├── REF_COUNTRIES
        └── REF_CURRENCIES
```

### How It Works
- Each tenant gets their own schema with identical table structure
- RBAC controls access: each tenant role can only access their schema
- Shared reference data lives in a common schema
- ETL pipelines are parameterized by tenant/schema name

### When to Use OPT
- **Moderate number of tenants** (10 to ~100)
- **Medium data per tenant**
- **Some compliance requirements** that benefit from schema-level separation
- **Tenant-specific customizations** needed (extra columns, custom tables)
- **Customer wants per-tenant visibility** into storage and compute
- **Budget sensitivity = "Moderate" or "Cost Conscious"**

### Advantages
- Stronger isolation than MTT (schema-level RBAC)
- Tenant-specific schema customizations possible
- Per-tenant CLONE for fast environment provisioning
- Easier compliance narrative ("each client's data is in a separate schema")
- Can use FUTURE GRANTS for automated access management
- No Row Access Policy overhead on queries

### Disadvantages
- Schema proliferation (100 tenants = 100 schemas × N tables each)
- ETL pipelines must be parameterized or duplicated per schema
- dbt models need macro-driven schema routing (more complex)
- Cross-tenant analytics requires UNION ALL across schemas
- Onboarding new tenants requires schema + table + RBAC creation
- More Snowflake DDL management overhead

### Snowflake Features to Leverage
- **CLONE**: Zero-copy schema cloning for tenant provisioning
- **FUTURE GRANTS**: Automatic privilege propagation for new objects
- **Information Schema**: Query tenant schemas programmatically
- **Tasks**: Per-tenant scheduled processing
- **Stored Procedures**: Parameterized tenant provisioning scripts

### dbt Pattern for OPT
```yaml
# dbt_project.yml - use generate_schema_name macro
# models/staging/schema.yml
# Custom macro to route models to tenant-specific schemas
```

---

## Pattern 3: APT (Account Per Tenant)

### Architecture
```
SNOWFLAKE ORGANIZATION
├── ACCOUNT: ACME_PROD (Region: AWS US-EAST-1)
│   └── DATABASE: APP_DB
│       └── SCHEMA: DATA
│           ├── CUSTOMERS
│           ├── ORDERS
│           └── PRODUCTS
│
├── ACCOUNT: GLOBEX_PROD (Region: AZURE EAST-US-2)
│   └── DATABASE: APP_DB
│       └── SCHEMA: DATA
│
├── ACCOUNT: INITECH_PROD (Region: AWS EU-WEST-1)
│   └── DATABASE: APP_DB
│       └── SCHEMA: DATA
│
└── ACCOUNT: PLATFORM_MGMT (management account)
    └── Cross-account monitoring, billing aggregation
```

### How It Works
- Each tenant gets their own Snowflake account
- Complete physical isolation (separate storage, separate compute)
- Managed via **Snowflake Organizations** for centralized billing and account management
- **Data Sharing** or **Replication** for cross-account data movement

### When to Use APT
- **Small number of high-value tenants** (< 50)
- **Large data per tenant**
- **Strict regulatory compliance** (HIPAA with BAA per tenant, SOX, FedRAMP)
- **Multi-region requirements** (tenants in different geographic regions)
- **Complete data isolation** is a contractual or legal requirement
- **Tenant-specific Snowflake configuration** (network policies, security integrations)
- **Budget sensitivity = "Very Flexible" or "Moderate"** (APT is the most expensive pattern)

### Advantages
- Strongest possible isolation (separate account, separate encryption keys)
- Per-tenant Snowflake configuration (network policies, SSO, MFA)
- Per-tenant billing and credit tracking (native)
- Tenant can be in different cloud regions for data residency compliance
- No noisy neighbor risk (dedicated compute)
- Simplest compliance narrative ("each client has their own Snowflake instance")
- Tenant offboarding is clean (drop the account)

### Disadvantages
- Most expensive (per-account overhead, no storage sharing)
- Most complex to manage (N accounts × all operations)
- Cross-tenant analytics requires Data Sharing + replication
- CI/CD must deploy to N accounts
- Onboarding new tenants requires full account provisioning
- Snowflake Organizations required for centralized management

### Snowflake Features to Leverage
- **Organizations**: Centralized account management, billing
- **Data Sharing**: Share reference data from management account to tenant accounts
- **Replication**: Cross-account, cross-region data replication
- **Account-level Network Policies**: Per-tenant network isolation
- **Tri-Secret Secure**: Per-tenant customer-managed encryption keys

---

## Decision Framework

Use this decision tree when recommending a multi-tenancy pattern:

```
START
│
├── Is strict physical data isolation required (regulatory/contractual)?
│   ├── YES → APT
│   └── NO ↓
│
├── How many tenants?
│   ├── > 100 tenants → MTT
│   ├── 10-100 tenants ↓
│   │   ├── Need per-tenant schema customizations? → OPT
│   │   └── Uniform schema, cost-focused? → MTT
│   └── < 10 tenants ↓
│       ├── Budget flexible + compliance needs? → APT
│       └── Budget constrained? → OPT
│
└── Special considerations:
    ├── Multi-region data residency required? → APT
    ├── Per-tenant encryption keys needed? → APT
    ├── Cross-tenant analytics critical? → MTT (easiest)
    └── Tenant-specific BI dashboards? → OPT or APT
```

## Hybrid Patterns

In practice, many implementations use hybrid approaches:

### MTT + OPT Hybrid
- Shared MTT tables for high-volume transactional data (with Row Access Policies)
- Per-tenant schemas for tenant-specific configuration and custom objects
- Common in SaaS platforms with a standard core + tenant extensions

### OPT + APT Hybrid
- OPT for standard tenants within a shared account
- APT for premium/enterprise tenants requiring full isolation
- Managed via Snowflake Organizations with Data Sharing between accounts

### Snowflake Native Apps Pattern
- Package the entire application (data + logic + UI) as a Snowflake Native App
- Each tenant installs the app in their own account (consumer account)
- Provider account shares data via Listings
- Best for: data product companies, analytics SaaS
