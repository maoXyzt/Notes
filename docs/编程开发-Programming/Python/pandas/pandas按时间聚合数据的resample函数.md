# pandas 按时间聚合数据: resample 方法

## `DataFrame.resample` 方法

可自动根据索引的时间，按指定的时间频率来聚合数据。

```python
# df 的 index 必须是 datetime 类型
df.resample('M').sum()

# 可以与 groupby 结合使用
df.groupby(["reim_user_name",
            "cost_trackings_project_name",
            "expense_category",
           ]).resample('MS').sum()
```
