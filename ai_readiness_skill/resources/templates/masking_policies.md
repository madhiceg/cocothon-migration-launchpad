# Template: Masking Policies

Standard masking policy suite for common PII data types. Each policy uses role-based unmasking — privileged roles see full data, all others see masked values.

## Policies

| Policy | Data Type | Masking Strategy |
|--------|-----------|-----------------|
| `mask_email` | STRING | Preserves domain: `****@example.com` |
| `mask_phone` | STRING | Last 4 digits: `***-***-1234` |
| `mask_ssn` | STRING | Fully masked: `***-**-****` |
| `mask_name` | STRING | First initial: `J****` |
| `mask_number` | STRING | Last 4 digits: `****-****-****-5678` |
| `mask_date` | DATE | Truncated to year: `2024-01-01` |

## SQL

### Email Masking

```sql
CREATE OR REPLACE MASKING POLICY {{database}}.{{schema}}.mask_email AS
    (val STRING) RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() IN ('DATA_ENGINEER', 'ADMIN', 'SYSADMIN') THEN val
        WHEN val IS NOT NULL THEN REGEXP_REPLACE(val, '.+@', '****@')
        ELSE val
    END
    COMMENT = 'Masks email address, preserving domain';
```

### Phone Masking

```sql
CREATE OR REPLACE MASKING POLICY {{database}}.{{schema}}.mask_phone AS
    (val STRING) RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() IN ('DATA_ENGINEER', 'ADMIN', 'SYSADMIN') THEN val
        WHEN val IS NOT NULL THEN CONCAT('***-***-', RIGHT(val, 4))
        ELSE val
    END
    COMMENT = 'Masks phone number, preserving last 4 digits';
```

### SSN Masking

```sql
CREATE OR REPLACE MASKING POLICY {{database}}.{{schema}}.mask_ssn AS
    (val STRING) RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() IN ('DATA_ENGINEER', 'ADMIN', 'SYSADMIN') THEN val
        WHEN val IS NOT NULL THEN '***-**-****'
        ELSE val
    END
    COMMENT = 'Fully masks SSN';
```

### Name Masking

```sql
CREATE OR REPLACE MASKING POLICY {{database}}.{{schema}}.mask_name AS
    (val STRING) RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() IN ('DATA_ENGINEER', 'ADMIN', 'SYSADMIN') THEN val
        WHEN val IS NOT NULL THEN CONCAT(LEFT(val, 1), '****')
        ELSE val
    END
    COMMENT = 'Masks name, preserving first initial';
```

### Number Masking (Credit Card, Account Numbers)

```sql
CREATE OR REPLACE MASKING POLICY {{database}}.{{schema}}.mask_number AS
    (val STRING) RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() IN ('DATA_ENGINEER', 'ADMIN', 'SYSADMIN') THEN val
        WHEN val IS NOT NULL THEN CONCAT('****-****-****-', RIGHT(val, 4))
        ELSE val
    END
    COMMENT = 'Masks numeric identifiers, preserving last 4 digits';
```

### Date Masking (DOB)

```sql
CREATE OR REPLACE MASKING POLICY {{database}}.{{schema}}.mask_date AS
    (val DATE) RETURNS DATE ->
    CASE
        WHEN CURRENT_ROLE() IN ('DATA_ENGINEER', 'ADMIN', 'SYSADMIN') THEN val
        WHEN val IS NOT NULL THEN DATE_TRUNC('YEAR', val)
        ELSE val
    END
    COMMENT = 'Masks date to year-level precision';
```

## Customization

- Replace the role list in `CURRENT_ROLE() IN (...)` with your organization's privileged roles.
- For tag-based masking, attach these policies to tags instead of individual columns.
