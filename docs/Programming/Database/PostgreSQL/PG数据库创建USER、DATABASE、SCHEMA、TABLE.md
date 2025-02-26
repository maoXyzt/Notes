# PG 数据库创建 USER、DATABASE、SCHEMA、TABLE

## 1. User

```sql
CREATE USER username WITH PASSWORD 'password';
```

## 2. Database

```sql
CREATE DATABASE dbname OWNER user_name;

-- change owner
ALTER DATABASE dbname OWNER TO new_owner;

-- privileges：
-- GRANT { { CREATE | TEMPORARY | TEMP } [,...] | ALL [ PRIVILEGES ] }
--     ON DATABASE dbname [, ...]
--     TO { username | GROUP groupname | PUBLIC } [, ...] [ WITH GRANT OPTION ]
GRANT all ON DATABASE dbname TO username;
```

## 3. Schema

```sql
CREATE SCHEMA schemaname;

-- privileges
-- GRANT { { CREATE | USAGE } [,...] | ALL [ PRIVILEGES ] }
--     ON SCHEMA schemaname [, ...]
--     TO { username | GROUP groupname | PUBLIC } [, ...] [ WITH GRANT OPTION ]
GRANT all ON SCHEMA schemaname TO username;
```

## 4. Table

```sql
-- privileges
-- GRANT { { SELECT | INSERT | UPDATE | DELETE | RULE | REFERENCES | TRIGGER }
--     [,...] | ALL [ PRIVILEGES ] }
--     ON [ TABLE ] tablename [, ...]
--     TO { username | GROUP groupname | PUBLIC } [, ...] [ WITH GRANT OPTION ]
GRANT all ON tablename TO username;
```
