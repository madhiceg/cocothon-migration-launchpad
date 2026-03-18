# Action Plan: Metadata & Lineage

## Foundational (Score 0-25)

### ACTION: Auto-Generate Table and Column Descriptions
- **Effort:** Medium | **Impact:** High | **Timeline:** Week 1-2
- Use `CORTEX.COMPLETE` to generate `COMMENT ON` statements from column names and sample data for all tables.

### ACTION: Create a Tagging Taxonomy
- **Effort:** Low | **Impact:** High | **Timeline:** Week 1
- Define standard tags: `domain`, `data_tier` (raw/curated/serving), `pii_level`, `cost_center`.
- **SQL Template:** `resources/templates/governance_tags_template.sql`

---

## Developing (Score 26-50)

### ACTION: Enable Git Integration for Schema-as-Code
- **Effort:** Medium | **Impact:** High | **Timeline:** Week 2-3
- Connect Snowflake Git integration to track DDL changes. Use dbt or Snowflake CLI for deployment.

### ACTION: Build Impact Analysis Queries
- **Effort:** Medium | **Impact:** Medium | **Timeline:** Week 3-4
- Query `OBJECT_DEPENDENCIES` and `ACCESS_HISTORY` to build downstream impact reports before schema changes.

---

## Advancing (Score 51-75)

### ACTION: Implement Automated Drift Detection
- **Effort:** High | **Impact:** High | **Timeline:** Week 4-6
- Create tasks that compare current schema to Git-tracked definitions and alert on unauthorized changes.
