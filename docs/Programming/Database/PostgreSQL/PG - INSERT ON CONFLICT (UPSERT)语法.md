# PostgreSQL 的 INSERT ON CONFLICT (UPSERT) 语法

版本要求：PG >= 9.5

## Examples

示例表如下：

```sql
CREATE TABLE customers (
  customer_id serial PRIMARY KEY,
  name VARCHAR UNIQUE,
  email VARCHAR NOT NULL,
  active bool NOT NULL DEFAULT TRUE
);

INSERT INTO customers (NAME, email)
VALUES
  ('IBM', 'contact@ibm.com'),
  ('Microsoft', 'contact@microsoft.com'),
  ('Intel', 'contact@intel.com');
```

示例表将包含如下索引:

+ `"customers_pkey" PRIMARY KEY, bree <customer_id>`
+ `"customers_name_key" UNIQUE CONSTRAINT, btree <name>`

### (1) 与索引冲突

```sql
INSERT INTO customers (NAME, email)
VALUES
  ('Microsoft', 'hotline@microsoft.com')
ON CONFLICT ON CONSTRAINT customers_name_key
DO NOTHING;
```

### (2) 与字段冲突

```sql
INSERT INTO customers (name, email)
VALUES
  ('Microsoft', 'hotline@microsoft.com')
ON CONFLICT (name)
DO NOTHING;
```

### (3) 冲突时 update

```sql
INSERT INTO customers (name, email, active)
VALUES
  ('Microsoft', 'hotline@microsoft.com', false)
ON CONFLICT (name)
DO
 UPDATE
   SET email = EXCLUDED.email,
       active = EXCLUDED.active;
```
