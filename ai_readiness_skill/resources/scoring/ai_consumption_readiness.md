# AI Consumption Readiness

**Weight:** 15% of overall AI Readiness Score
**Max Score:** 100

This dimension measures how prepared the data estate is for direct AI/ML consumption — from feature engineering to model deployment to Cortex integration.

---

## Criteria

### 1. Feature Engineering Readiness (Weight: 20%)

Data is structured for ML feature consumption with proper types and encodings.

| Score | Condition |
|-------|-----------|
| 0-20 | Raw data only, no feature tables |
| 21-40 | Some aggregated views for analytics |
| 41-60 | Dedicated feature tables with scheduled refresh |
| 61-80 | Feature store patterns with versioned feature sets |
| 81-100 | Snowflake Feature Store with point-in-time correctness and serving |

**Snowflake Signals:**
- Feature Store objects
- Dynamic Tables as feature pipelines

---

### 2. Vector & Embedding Readiness (Weight: 20%)

Text and unstructured data is embeddable and vector-searchable.

| Score | Condition |
|-------|-----------|
| 0-20 | No embedding infrastructure |
| 21-40 | Awareness of Cortex Embed; no implementation |
| 41-60 | `CORTEX.EMBED` used on select text columns |
| 61-80 | Embeddings stored with VECTOR type, Cortex Search configured |
| 81-100 | Production Cortex Search services with hybrid search and RAG pipelines |

**Snowflake Signals:**
- Columns with `VECTOR` data type
- Cortex Search services
- `CORTEX.EMBED` usage in `QUERY_HISTORY`

---

### 3. Cortex LLM & AI Function Readiness (Weight: 20%)

Data estate leverages Cortex AI functions for enrichment and analysis.

| Score | Condition |
|-------|-----------|
| 0-20 | No Cortex functions used |
| 21-40 | Experimental use of `CORTEX.COMPLETE` or `CORTEX.SENTIMENT` |
| 41-60 | Multiple Cortex functions in production queries |
| 61-80 | Cortex Agent or Analyst deployed for business use cases |
| 81-100 | Full Cortex stack: Analyst + Agent + Search + custom fine-tuned models |

**Snowflake Signals:**
- `QUERY_HISTORY` — CORTEX function calls
- Cortex Analyst semantic models
- Cortex Agent deployments

---

### 4. ML Model Registry & Deployment (Weight: 20%)

Models are versioned, registered, and deployable via Snowflake ML.

| Score | Condition |
|-------|-----------|
| 0-20 | No model registry usage |
| 21-40 | Models trained externally, manual deployment |
| 41-60 | Snowflake Model Registry with logged models |
| 61-80 | Model versioning + inference in warehouse or SPCS |
| 81-100 | Full MLOps: registry + monitoring + A/B testing + automated retraining |

**Snowflake Signals:**
- `SNOWFLAKE.ML.*` functions
- Model Registry objects
- Compute Pool usage for ML

---

### 5. ML-Friendly Schema Design (Weight: 20%)

Schemas optimized for ML consumption with proper types, no excessive nesting.

| Score | Condition |
|-------|-----------|
| 0-20 | Deeply nested VARIANT, no flattening |
| 21-40 | Some flattened views, inconsistent types |
| 41-60 | Star schema or feature-friendly wide tables |
| 61-80 | Typed columns, proper NULLs, numeric encoding for categoricals |
| 81-100 | ML-optimized schemas with training/serving splits and sample weight columns |

**Snowflake Signals:**
- Column type distribution analysis
- VARIANT vs structured column ratio
