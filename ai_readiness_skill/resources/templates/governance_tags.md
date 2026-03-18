# Template: Governance Tags

Standard tagging taxonomy for data governance, ownership, and AI readiness tracking.

## Tags

| Tag | Purpose | Allowed Values |
|-----|---------|---------------|
| `data_owner` | Team or individual responsible for this data asset | Free-form |
| `data_steward` | Operational steward responsible for data quality | Free-form |
| `domain` | Business domain | FINANCE, MARKETING, SALES, OPERATIONS, HR, ENGINEERING, PRODUCT, CUSTOMER_SUCCESS |
| `data_tier` | Pipeline tier / maturity level | RAW, STAGING, CURATED, SERVING, SANDBOX |
| `cost_center` | Cost center for chargeback attribution | Free-form |
| `pii_level` | Level of PII sensitivity | NONE, LOW, MEDIUM, HIGH, CRITICAL |
| `retention_policy` | Data retention requirement for compliance | 30_DAYS, 90_DAYS, 1_YEAR, 3_YEARS, 7_YEARS, INDEFINITE |
| `ai_ready` | Whether this asset is validated for AI/ML consumption | TRUE, FALSE, IN_PROGRESS |

## SQL

```sql
CREATE TAG IF NOT EXISTS {{database}}.{{schema}}.data_owner
    COMMENT = 'The team or individual responsible for this data asset';

CREATE TAG IF NOT EXISTS {{database}}.{{schema}}.data_steward
    COMMENT = 'The operational steward responsible for data quality';

CREATE TAG IF NOT EXISTS {{database}}.{{schema}}.domain
    ALLOWED_VALUES 'FINANCE', 'MARKETING', 'SALES', 'OPERATIONS', 'HR', 'ENGINEERING', 'PRODUCT', 'CUSTOMER_SUCCESS'
    COMMENT = 'Business domain this data belongs to';

CREATE TAG IF NOT EXISTS {{database}}.{{schema}}.data_tier
    ALLOWED_VALUES 'RAW', 'STAGING', 'CURATED', 'SERVING', 'SANDBOX'
    COMMENT = 'Data pipeline tier / maturity level';

CREATE TAG IF NOT EXISTS {{database}}.{{schema}}.cost_center
    COMMENT = 'Cost center for chargeback attribution';

CREATE TAG IF NOT EXISTS {{database}}.{{schema}}.pii_level
    ALLOWED_VALUES 'NONE', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    COMMENT = 'Level of PII sensitivity in this object';

CREATE TAG IF NOT EXISTS {{database}}.{{schema}}.retention_policy
    ALLOWED_VALUES '30_DAYS', '90_DAYS', '1_YEAR', '3_YEARS', '7_YEARS', 'INDEFINITE'
    COMMENT = 'Data retention requirement for compliance';

CREATE TAG IF NOT EXISTS {{database}}.{{schema}}.ai_ready
    ALLOWED_VALUES 'TRUE', 'FALSE', 'IN_PROGRESS'
    COMMENT = 'Whether this data asset has been validated for AI/ML consumption';
```

## Customization

Adjust `ALLOWED_VALUES` to match your organization's domains, tiers, and compliance requirements.
