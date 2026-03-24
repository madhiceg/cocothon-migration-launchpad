# Infrastructure & Scalability

**Weight:** 10% of overall AI Readiness Score
**Max Score:** 100

AI workloads demand elastic compute, cost control, and optimized storage. This dimension assesses whether the Snowflake infrastructure can support ML training, inference, and serving at scale.

---

## Criteria

### 1. Warehouse Optimization (Weight: 25%)

Right-sized warehouses with auto-suspend and multi-cluster scaling.

| Score | Condition |
|-------|-----------|
| 0-20 | Single oversized warehouse for all workloads |
| 21-40 | Separate warehouses but no auto-suspend tuning |
| 41-60 | Workload-specific warehouses with auto-suspend |
| 61-80 | Multi-cluster warehouses with query routing |
| 81-100 | Optimized sizing + multi-cluster + resource monitors + query acceleration |

**Snowflake Signals:**
- `WAREHOUSES` view — size, auto_suspend, min/max_cluster_count
- `WAREHOUSE_METERING_HISTORY`
- `RESOURCE_MONITORS` view

---

### 2. Cost Governance (Weight: 25%)

Budgets, resource monitors, and cost attribution in place.

| Score | Condition |
|-------|-----------|
| 0-20 | No cost tracking or budgets |
| 21-40 | Resource monitors on account level only |
| 41-60 | Per-warehouse resource monitors with alerts |
| 61-80 | Budgets + cost-center tagging + serverless cost tracking |
| 81-100 | Full FinOps: budgets + attribution + anomaly detection + chargeback |

**Snowflake Signals:**
- `RESOURCE_MONITORS` view
- `METERING_DAILY_HISTORY`
- `TAG_REFERENCES` — cost center tags

---

### 3. Compute Pool Readiness (Weight: 25%)

Snowpark Container Services and GPU compute for ML workloads.

| Score | Condition |
|-------|-----------|
| 0-20 | No awareness of SPCS or compute pools |
| 21-40 | Awareness but no compute pools created |
| 41-60 | Compute pool created for experimentation |
| 61-80 | Production SPCS services with GPU for ML inference |
| 81-100 | Multi-pool strategy: CPU for ETL, GPU for training/inference, auto-scaling |

**Snowflake Signals:**
- `COMPUTE_POOLS` view
- `SERVICES` view (SPCS)

---

### 4. Storage Optimization (Weight: 25%)

Clustering, search optimization, and storage cost management.

| Score | Condition |
|-------|-----------|
| 0-20 | No clustering or optimization |
| 21-40 | Basic clustering on large tables |
| 41-60 | Clustering + search optimization on key tables |
| 61-80 | Tiered storage strategy + Iceberg tables for open format |
| 81-100 | Full optimization: clustering + search opt + Iceberg + lifecycle management |

**Snowflake Signals:**
- `AUTOMATIC_CLUSTERING_HISTORY`
- `SEARCH_OPTIMIZATION_HISTORY`
- `TABLE_STORAGE_METRICS`
