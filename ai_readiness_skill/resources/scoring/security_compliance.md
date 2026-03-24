# Security & Compliance

**Weight:** 15% of overall AI Readiness Score
**Max Score:** 100

Security and compliance are non-negotiable for AI workloads. AI models that ingest unprotected PII or operate under loose RBAC create regulatory exposure and reputational risk.

---

## Criteria

### 1. RBAC Maturity (Weight: 25%)

Role hierarchy is well-structured with least-privilege enforcement.

| Score | Condition |
|-------|-----------|
| 0-20 | ACCOUNTADMIN used for daily operations |
| 21-40 | Basic role separation but broad grants |
| 41-60 | Functional roles with schema-level grants |
| 61-80 | Least-privilege enforced, database roles used |
| 81-100 | Full RBAC hierarchy with automated role reviews and no orphaned grants |

**Snowflake Signals:**
- `GRANTS_TO_ROLES` view
- `GRANTS_TO_USERS` view
- `ROLES` view — role hierarchy

---

### 2. Encryption & Key Management (Weight: 15%)

Data encrypted at rest and in transit with managed key rotation.

| Score | Condition |
|-------|-----------|
| 0-20 | Default encryption only, no Tri-Secret Secure |
| 21-40 | Default Snowflake encryption acknowledged |
| 41-60 | Periodic key rotation enabled |
| 61-80 | Customer-managed keys (Tri-Secret Secure) deployed |
| 81-100 | Tri-Secret Secure with external key vault and annual rotation policy |

**Snowflake Signals:**
- `ENCRYPTION_KEYS` view
- Account parameters — `PERIODIC_DATA_REKEYING`

---

### 3. Network Security (Weight: 15%)

Network policies, private connectivity, and IP allowlisting.

| Score | Condition |
|-------|-----------|
| 0-20 | No network policies; public access |
| 21-40 | Basic network policy with IP allowlist |
| 41-60 | Network policies per user/group |
| 61-80 | AWS PrivateLink / Azure Private Link configured |
| 81-100 | Private connectivity + network rules + SCIM integration |

**Snowflake Signals:**
- `NETWORK_POLICIES` view
- Account parameters — `NETWORK_POLICY`

---

### 4. Authentication & MFA (Weight: 15%)

Multi-factor authentication and SSO enforcement.

| Score | Condition |
|-------|-----------|
| 0-20 | Password-only auth, no MFA |
| 21-40 | MFA available but not enforced |
| 41-60 | MFA enforced for admin roles |
| 61-80 | SSO + MFA enforced for all human users |
| 81-100 | SSO + MFA + key-pair auth for service accounts, no password auth |

**Snowflake Signals:**
- `USERS` view — has_mfa, ext_authn_duo
- `AUTHENTICATION_POLICIES`

---

### 5. Regulatory Compliance Posture (Weight: 15%)

Readiness for GDPR, HIPAA, PCI-DSS, SOC2 requirements.

| Score | Condition |
|-------|-----------|
| 0-20 | No compliance framework mapped |
| 21-40 | Compliance requirements identified but not implemented |
| 41-60 | Classification profiles detect PII/PHI, partial masking |
| 61-80 | Full classification + masking + audit trails for target regulations |
| 81-100 | Continuous compliance monitoring with Trust Center clean dashboard |

**Snowflake Signals:**
- Trust Center — Objects by compliance category
- `DATA_CLASSIFICATION_LATEST` — compliance categories

---

### 6. Dynamic Data Masking (Weight: 15%)

Sensitive columns protected with masking and projection policies.

| Score | Condition |
|-------|-----------|
| 0-20 | No masking policies |
| 21-40 | Ad-hoc masking on select columns |
| 41-60 | Masking policies on all classified PII columns |
| 61-80 | Tag-based masking with role-aware unmasking |
| 81-100 | Full masking + projection + conditional policies with audit |

**Snowflake Signals:**
- `MASKING_POLICIES` view
- `POLICY_REFERENCES` view
