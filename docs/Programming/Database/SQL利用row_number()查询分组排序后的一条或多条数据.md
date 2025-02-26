# SQL 利用 row_number() 查询分组排序后的一条或多条数据

```sql
-- 每个线索的最新一条事件
SELECT * FROM (
    SELECT evnt.id AS event_id
        , row_number() over(partition by evnt.lead_id
                            order by evnt.start_time DESC, evnt.update_time DESC)
    FROM crm_event evnt
) t1
WHERE row_number = 1
```
