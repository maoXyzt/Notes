# PostgreSQL 把多行拼接为字符串

使用 `array_agg` 函数将多行数据拼接为数组，再使用 `array_to_string` 函数将数组拼接为字符串。

`array_to_string(array_agg([要拼接的字段名]), [分隔符])`

示例：

```sql
array_to_string(array_agg("name"), ',')
```
