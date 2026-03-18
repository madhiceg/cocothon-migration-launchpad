# Template: Security Policies

Network policy and authentication policy templates for securing Snowflake access.

## Network Policy

Restrict account access to known corporate IP ranges.

```sql
CREATE OR REPLACE NETWORK POLICY {{policy_name}}
    ALLOWED_IP_LIST = ('{{allowed_ip_1}}', '{{allowed_ip_2}}')
    BLOCKED_IP_LIST = ()
    COMMENT = 'Restrict access to known corporate IP ranges';

ALTER ACCOUNT SET NETWORK_POLICY = {{policy_name}};
```

## Authentication Policy — Enforce MFA

Require multi-factor authentication for all Snowsight users.

```sql
CREATE OR REPLACE AUTHENTICATION POLICY {{database}}.{{schema}}.enforce_mfa
    MFA_AUTHENTICATION_METHODS = ('TOTP')
    CLIENT_TYPES = ('SNOWFLAKE_UI', 'SNOWSIGHT')
    SECURITY_INTEGRATIONS = ()
    COMMENT = 'Enforce MFA for all Snowsight users';

ALTER ACCOUNT SET AUTHENTICATION POLICY {{database}}.{{schema}}.enforce_mfa;
```

## Customization

- Add your corporate CIDR ranges to `ALLOWED_IP_LIST`.
- For private connectivity, configure AWS PrivateLink or Azure Private Link instead.
- Adjust `CLIENT_TYPES` to include programmatic access if needed.
