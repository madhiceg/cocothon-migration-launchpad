# Action Plan: AI Consumption Readiness

## Foundational (Score 0-25)

### ACTION: Start Using Cortex AI Functions on Existing Data
- **Effort:** Low | **Impact:** High | **Timeline:** Week 1
- Run `CORTEX.SENTIMENT`, `CORTEX.SUMMARIZE`, and `CORTEX.EXTRACT_ANSWER` on text columns to demonstrate value.
- **SQL Template:** `tools/action_plan/sql/cortex_quickstart.sql`

### ACTION: Generate Embeddings for Text-Heavy Tables
- **Effort:** Medium | **Impact:** High | **Timeline:** Week 1-2
- Use `CORTEX.EMBED` to create VECTOR columns. Build a Cortex Search service for semantic retrieval.

---

## Developing (Score 26-50)

### ACTION: Build Feature Tables for ML Consumption
- **Effort:** High | **Impact:** High | **Timeline:** Week 2-4
- Create curated wide tables with proper numeric types, encoded categoricals, and NULL handling for ML.

### ACTION: Register First Model in Snowflake Model Registry
- **Effort:** Medium | **Impact:** High | **Timeline:** Week 3-4
- Train a simple model in Snowpark ML and log it to the Model Registry with metrics and sample input.

---

## Advancing (Score 51-75)

### ACTION: Deploy Cortex Agent or Analyst for Business Users
- **Effort:** High | **Impact:** High | **Timeline:** Week 4-8
- Build semantic model YAML for Cortex Analyst or configure Cortex Agent with tool definitions.

### ACTION: Set Up Compute Pools for GPU-Accelerated ML
- **Effort:** High | **Impact:** High | **Timeline:** Week 6-10
- Create SPCS compute pools with GPU instances for model training and real-time inference.
