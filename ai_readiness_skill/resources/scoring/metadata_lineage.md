# Metadata & Lineage

**Weight:** 10% of overall AI Readiness Score
**Max Score:** 100

Discoverability, documentation, and lineage are essential for trust in AI outputs. If data scientists cannot find, understand, and trace data, AI projects stall in the "data wrangling" phase.

---

## Criteria

### 1. Column-Level Lineage (Weight: 25%)

Ability to trace data flow from source to consumption at column granularity.

| Score | Condition |
|-------|-----------|
| 0-20 | No lineage visibility |
| 21-40 | Object-level dependencies only via OBJECT_DEPENDENCIES |
| 41-60 | ACCESS_HISTORY column lineage for recent queries |
| 61-80 | Systematic lineage via Horizon + external tools |
| 81-100 | Full column-level lineage with impact analysis automation |

**Snowflake Signals:**
- `ACCESS_HISTORY` — direct/base column refs
- `OBJECT_DEPENDENCIES` view

---

### 2. Object Documentation (Weight: 20%)

Tables, columns, and views are documented with comments and descriptions.

| Score | Condition |
|-------|-----------|
| 0-20 | No comments on any objects |
| 21-40 | Comments on <25% of tables |
| 41-60 | Comments on >50% of tables, <25% of columns |
| 61-80 | Comments on >75% of tables and >50% of columns |
| 81-100 | >90% documentation coverage for tables and columns |

**Snowflake Signals:**
- `TABLES` view — comment IS NOT NULL
- `COLUMNS` view — comment IS NOT NULL

---

### 3. Object Tagging Coverage (Weight: 20%)

Objects tagged for domain, sensitivity, cost center, and lifecycle.

| Score | Condition |
|-------|-----------|
| 0-20 | No tags defined |
| 21-40 | System tags from classification only |
| 41-60 | Custom tags for domain/cost-center on key objects |
| 61-80 | Comprehensive tagging taxonomy with >60% coverage |
| 81-100 | Full tagging with tag-based policies and automated propagation |

**Snowflake Signals:**
- `TAG_REFERENCES` view
- `TAGS` view — custom tags count

---

### 4. Impact Analysis Capability (Weight: 20%)

Ability to assess downstream impact before schema changes.

| Score | Condition |
|-------|-----------|
| 0-20 | No impact analysis process |
| 21-40 | Manual dependency checks before changes |
| 41-60 | OBJECT_DEPENDENCIES queried for impact checks |
| 61-80 | Automated impact analysis in CI/CD pipeline |
| 81-100 | Full DAG-aware impact analysis with automated notifications |

**Snowflake Signals:**
- `OBJECT_DEPENDENCIES` view
- Dynamic Table DAG relationships

---

### 5. Schema Evolution Tracking (Weight: 15%)

Schema changes are tracked, versioned, and communicated.

| Score | Condition |
|-------|-----------|
| 0-20 | No schema change tracking |
| 21-40 | QUERY_HISTORY DDL audit |
| 41-60 | Schema change alerts via tasks |
| 61-80 | Schema versioning via Git integration or dbt |
| 81-100 | Full schema-as-code with CI/CD, drift detection, and rollback |

**Snowflake Signals:**
- `QUERY_HISTORY` — DDL statements
- Git integration repositories
