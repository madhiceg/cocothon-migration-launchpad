# Data Governance

**Weight:** 15% of overall AI Readiness Score
**Max Score:** 100

Data Governance ensures data assets are owned, cataloged, classified, and protected by policy. Without governance, AI adoption carries regulatory risk and operational chaos.

---

## Criteria

### 1. Data Ownership & Stewardship (Weight: 20%)

Every critical data asset has a designated owner and steward.

| Score | Condition |
|-------|-----------|
| 0-20 | No ownership tags or documentation |
| 21-40 | Ownership defined for <25% of objects |
| 41-60 | Ownership tags on 25-60% of objects |
| 61-80 | Ownership tags on >60%, stewardship roles defined |
| 81-100 | 100% tagged with automated ownership propagation |

**Snowflake Signals:**
- `TAG_REFERENCES` view — ownership tags
- `OBJECT_DEPENDENCIES` view

---

### 2. Data Cataloging & Discovery (Weight: 20%)

Objects are described, tagged, and discoverable via Snowflake catalog.

| Score | Condition |
|-------|-----------|
| 0-20 | No comments or tags on objects |
| 21-40 | Sporadic COMMENT ON usage |
| 41-60 | >50% tables have comments, some tagging |
| 61-80 | Systematic tagging with Snowflake object tags |
| 81-100 | Full catalog with Horizon integration and search |

**Snowflake Signals:**
- `TABLES` view — comment column
- `COLUMNS` view — comment column
- `TAG_REFERENCES` view

---

### 3. Policy Coverage (Weight: 25%)

Masking, row access, and projection policies applied to sensitive data.

| Score | Condition |
|-------|-----------|
| 0-20 | No policies defined |
| 21-40 | Masking policies on <25% of sensitive columns |
| 41-60 | Masking and row-access policies on key tables |
| 61-80 | Tag-based masking deployed, >75% sensitive columns covered |
| 81-100 | Full policy coverage with Trust Center dashboard clean |

**Snowflake Signals:**
- `POLICY_REFERENCES` view
- Trust Center — Sensitive data masking status

---

### 4. Sensitive Data Classification (Weight: 20%)

PII/PHI/PCI data is classified using Snowflake classification profiles.

| Score | Condition |
|-------|-----------|
| 0-20 | No classification run |
| 21-40 | Manual classification on select tables |
| 41-60 | Auto-classification profiles on some databases |
| 61-80 | Auto-classification on all production databases |
| 81-100 | Full auto-classification with custom classifiers and tag propagation |

**Snowflake Signals:**
- `DATA_CLASSIFICATION_LATEST` view
- `SYSTEM$GET_CLASSIFICATION_RESULT`
- Classification profiles on databases

---

### 5. Access Auditing & History (Weight: 15%)

Access patterns are tracked and regularly reviewed.

| Score | Condition |
|-------|-----------|
| 0-20 | ACCESS_HISTORY never queried |
| 21-40 | Ad-hoc access reviews |
| 41-60 | Quarterly access reviews using ACCESS_HISTORY |
| 61-80 | Automated access anomaly alerts |
| 81-100 | Continuous access monitoring with RBAC governance reviews |

**Snowflake Signals:**
- `ACCESS_HISTORY` view
- `LOGIN_HISTORY` view
- `QUERY_HISTORY` view
