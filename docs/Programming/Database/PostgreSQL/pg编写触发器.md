# PostgreSQL 编写触发器

> 参考
>
> [【PostgreSQL-9.6.3】触发器实例](https://www.cnblogs.com/NextAction/p/7385002.html)

为 `crm_lead` 表的 `opportunity_phase_id` 字段添加触发器:

```sql
-- 创建函数，两个 `$$` 之间为函数体，可以取名，如 `$some_name$`
-- `BEGIN` 和 `END;` 之间编写操作
-- `OLD` 代表操作前的旧行数据, `NEW` 代表操作后的新行数据
CREATE OR REPLACE FUNCTION opportunity_phase_snapshot_trigger_fun()
RETURNS trigger AS $$
BEGIN
  INSERT INTO crm_opportunity_phase_snapshot(snapshot_time, opportunity_id, opportunity_phase_id)
    SELECT now(), NEW.id, NEW.opportunity_phase_id;
  RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

-- 将触发器函数与 `crm_opportunity` 的 `opportunity_phase_id` 字段的 insert 和 update 操作关联
-- 仅针对操作有修改的每行触发
CREATE TRIGGER snapshot_crm_opportunity_phase_trigger
AFTER INSERT OR UPDATE OF opportunity_phase_id
ON crm_opportunity
FOR EACH ROW EXECUTE PROCEDURE opportunity_phase_snapshot_trigger_fun();
```
