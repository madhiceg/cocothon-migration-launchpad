# Template: Data Quality Constraints

Standard constraint patterns to enforce data integrity on production tables.

## Primary Key

```sql
ALTER TABLE {{database}}.{{schema}}.{{table_name}}
    ADD CONSTRAINT pk_{{table_name}} PRIMARY KEY ({{pk_column}});
```

## Unique Constraint

```sql
ALTER TABLE {{database}}.{{schema}}.{{table_name}}
    ADD CONSTRAINT uq_{{table_name}}_{{column}} UNIQUE ({{column}});
```

## NOT NULL Enforcement

```sql
ALTER TABLE {{database}}.{{schema}}.{{table_name}}
    ALTER COLUMN {{column}} SET NOT NULL;
```

## Foreign Key Reference

```sql
ALTER TABLE {{database}}.{{schema}}.{{child_table}}
    ADD CONSTRAINT fk_{{child_table}}_{{parent_table}}
    FOREIGN KEY ({{fk_column}})
    REFERENCES {{database}}.{{schema}}.{{parent_table}}({{pk_column}});
```

## Best Practices

- Start by auditing columns that are never NULL in practice and formalizing them with NOT NULL.
- Add PRIMARY KEYs to all fact and dimension tables.
- Use FOREIGN KEYs to document relationships even though Snowflake does not enforce them (they serve as metadata for query optimization and documentation).
- Combine with DMF monitoring for runtime validation of constraint assumptions.
