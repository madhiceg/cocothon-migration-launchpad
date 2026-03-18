# Data Quality

**Weight:** 20% of overall AI Readiness Score
**Max Score:** 100

Data Quality is the single most important dimension for AI readiness. Models trained on incomplete, inaccurate, or inconsistent data will produce unreliable results regardless of algorithm sophistication.

---

## Criteria

### 1. Completeness (Weight: 25%)

Percentage of non-null values across critical columns.

| Score | Condition |
|-------|-----------|
| 0-20 | >30% null rate across critical tables |
| 21-40 | 15-30% null rate |
| 41-60 | 5-15% null rate |
| 61-80 | 1-5% null rate |
| 81-100 | <1% null rate with DMF monitoring active |

**Snowflake Signals:**
- `SNOWFLAKE.CORE.NULL_COUNT` DMF results
- `SNOWFLAKE.CORE.NULL_IF_NOT_EXPECTED` DMF
- `information_schema.columns` — nullable metadata

---

### 2. Accuracy (Weight: 20%)

Data conforms to expected formats, ranges, and referential integrity.

| Score | Condition |
|-------|-----------|
| 0-20 | No validation rules or constraints defined |
| 21-40 | Basic NOT NULL constraints only |
| 41-60 | Foreign keys and check constraints on key tables |
| 61-80 | Custom DMFs for business rule validation |
| 81-100 | Full DMF coverage with anomaly detection enabled |

**Snowflake Signals:**
- `TABLE_CONSTRAINTS` view
- Custom DMF deployment count
- `DATA_QUALITY_MONITORING_USAGE_HISTORY`

---

### 3. Consistency (Weight: 20%)

No conflicting records across tables; deduplication is enforced.

| Score | Condition |
|-------|-----------|
| 0-20 | Known duplicates exist, no dedup process |
| 21-40 | Manual dedup runs periodically |
| 41-60 | `SNOWFLAKE.CORE.DUPLICATE_COUNT` DMF set on key tables |
| 61-80 | Automated dedup pipelines with DMF alerting |
| 81-100 | Zero-dup guarantee with continuous monitoring |

**Snowflake Signals:**
- `SNOWFLAKE.CORE.DUPLICATE_COUNT` DMF
- `SNOWFLAKE.CORE.UNIQUE_COUNT` DMF

---

### 4. Validity (Weight: 15%)

Data types are correct, enums are within accepted values, and schema drift is tracked.

| Score | Condition |
|-------|-----------|
| 0-20 | Widespread VARIANT abuse, no schema enforcement |
| 21-40 | Basic type enforcement, no enum validation |
| 41-60 | Schema evolution tracked, accepted-value checks on key columns |
| 61-80 | Dynamic tables enforce schema, custom DMFs for value validation |
| 81-100 | Full schema contracts with automated drift detection |

**Snowflake Signals:**
- `information_schema.columns` — data_type audit
- Custom DMFs for value-range checks

---

### 5. Quality Monitoring Coverage (Weight: 20%)

Percentage of critical tables with active DMF schedules.

| Score | Condition |
|-------|-----------|
| 0-20 | No DMFs deployed |
| 21-40 | <25% of critical tables have DMFs |
| 41-60 | 25-50% coverage |
| 61-80 | 50-80% coverage with scheduled runs |
| 81-100 | >80% coverage with anomaly detection enabled |

**Snowflake Signals:**
- `DATA_QUALITY_MONITORING_USAGE_HISTORY`
- DMF schedule metadata
