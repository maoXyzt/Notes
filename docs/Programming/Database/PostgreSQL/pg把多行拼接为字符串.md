```sql
-- array_to_string(array_agg(要拼接的字段名), 分隔符)
array_to_string(array_agg("name"), ',')
```

