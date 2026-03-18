# Action Plan: Data Governance

## Foundational (Score 0-25)

### ACTION: Run SYSTEM$CLASSIFY on All Production Databases
- **Effort:** Low | **Impact:** High | **Timeline:** Week 1
- Automatically detect PII, PHI, and PCI data across all tables. Review and approve tag assignments.
- **SQL Template:** `tools/action_plan/sql/run_classification.sql`

### ACTION: Create Ownership and Domain Tags
- **Effort:** Low | **Impact:** High | **Timeline:** Week 1
- Define tags: `data_owner`, `data_steward`, `domain`, `cost_center`. Assign to all databases and schemas.
- **SQL Template:** `resources/templates/governance_tags_template.sql`

### ACTION: Add COMMENT ON to All Tables and Critical Columns
- **Effort:** Medium | **Impact:** Medium | **Timeline:** Week 1-2
- Use `CORTEX.COMPLETE` to auto-generate table descriptions from column names and sample data.

---

## Developing (Score 26-50)

### ACTION: Deploy Tag-Based Masking Policies
- **Effort:** Medium | **Impact:** High | **Timeline:** Week 2-3
- Create masking policies that automatically mask columns tagged as EMAIL, PHONE, SSN, etc.
- **SQL Template:** `tools/action_plan/sql/deploy_tag_masking.sql`

### ACTION: Set Up Classification Profiles on Databases
- **Effort:** Low | **Impact:** High | **Timeline:** Week 2
- Enable auto-classification profiles so new tables are classified automatically on creation.

---

## Advancing (Score 51-75)

### ACTION: Implement Row Access Policies for Multi-Tenant Data
- **Effort:** High | **Impact:** High | **Timeline:** Week 3-5
- Create row access policies that restrict data visibility based on user role/region/department.
