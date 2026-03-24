# Action Plan: Security & Compliance

## Foundational (Score 0-25)

### ACTION: Enforce MFA for All Human Users
- **Effort:** Low | **Impact:** Critical | **Timeline:** Week 1
- Create authentication policy requiring MFA. Assign to account or individual users. Prioritize ACCOUNTADMIN holders.
- **SQL Template:** `resources/templates/security_policies_template.sql`

### ACTION: Reduce ACCOUNTADMIN Usage
- **Effort:** Medium | **Impact:** Critical | **Timeline:** Week 1-2
- Audit ACCOUNTADMIN query history. Create functional roles (DATA_ENGINEER, ANALYST, etc.) with least-privilege grants.
- **SQL Template:** `tools/action_plan/sql/rbac_restructure.sql`

### ACTION: Create Network Policies
- **Effort:** Low | **Impact:** High | **Timeline:** Week 1
- Restrict access to known IP ranges. Apply network policy at account level.
- **SQL Template:** `resources/templates/security_policies_template.sql`

---

## Developing (Score 26-50)

### ACTION: Deploy Key-Pair Auth for Service Accounts
- **Effort:** Medium | **Impact:** High | **Timeline:** Week 2-3
- Migrate service accounts from password auth to RSA key-pair authentication.

### ACTION: Set Up Access Review Automation
- **Effort:** Medium | **Impact:** Medium | **Timeline:** Week 3-4
- Build scheduled task querying `ACCESS_HISTORY` to detect unused grants and orphaned roles.

---

## Advancing (Score 51-75)

### ACTION: Evaluate Tri-Secret Secure and Private Connectivity
- **Effort:** High | **Impact:** High | **Timeline:** Week 4-8
- For regulated industries, implement customer-managed encryption keys and private link.
