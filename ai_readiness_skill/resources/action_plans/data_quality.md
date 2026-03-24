# Action Plan: Data Quality

## Foundational (Score 0-25)

### ACTION: Deploy System DMFs on All Production Tables
- **Effort:** Medium | **Impact:** High | **Timeline:** Week 1-2
- Attach `SNOWFLAKE.CORE.NULL_COUNT`, `DUPLICATE_COUNT`, and `FRESHNESS` to every production table. Start with the top-20 most queried tables from `QUERY_HISTORY`.
- **SQL Template:** `tools/action_plan/sql/deploy_system_dmfs.sql`

### ACTION: Add NOT NULL and PRIMARY KEY Constraints
- **Effort:** Low | **Impact:** Medium | **Timeline:** Week 1
- Audit columns that are never NULL in practice and formalize constraints. Use `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`.
- **SQL Template:** `resources/templates/constraints_template.sql`

### ACTION: Build a Data Quality Dashboard
- **Effort:** Medium | **Impact:** High | **Timeline:** Week 2-3
- Query `DATA_QUALITY_MONITORING_USAGE_HISTORY` to build a Streamlit dashboard showing DMF trends per table.

---

## Developing (Score 26-50)

### ACTION: Create Custom DMFs for Business-Rule Validation
- **Effort:** Medium | **Impact:** High | **Timeline:** Week 2-4
- Write custom Data Metric Functions for domain-specific rules (e.g., order_total > 0, email format validation).

### ACTION: Enable Anomaly Detection on DMF Results
- **Effort:** Low | **Impact:** Medium | **Timeline:** Week 3
- Configure DMF alert rules to trigger notifications when metric values deviate beyond expected thresholds.

---

## Advancing (Score 51-75)

### ACTION: Implement Zero-Duplicate Guarantee Pipelines
- **Effort:** High | **Impact:** High | **Timeline:** Week 4-6
- Use `MERGE INTO` with deduplication logic. Monitor with `DUPLICATE_COUNT` DMF.
