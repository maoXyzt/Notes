## DataFrame.resample()方法

可自动根据索引的时间，按指定的时间频率来聚合数据。

```python
# df的index必须是datetime类型
df.resample('M').sum()

# 可以与groupby结合使用
df.groupby(["reim_user_name",
            "cost_trackings_project_name",
            "expense_category",
           ]).resample('MS').sum()
```

