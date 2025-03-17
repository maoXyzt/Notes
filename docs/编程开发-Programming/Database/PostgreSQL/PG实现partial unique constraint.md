# PostgreSQL 实现 Partial Unique Constraint

PostgreSQL 使用 unique index 实现 unique constraint。

因此，如果想要“当满足某条件时，col_a 是唯一的”这样的约束，虽然无法直接定义一个 partial unique constraint，但是可以创建一个 partial unique index 来达成所需效果。

```sql
CREATE UNIQUE INDEX dogs_owner_id_alive_ix ON dogs (owner_id, status)
WHERE status = 'alive';
```
