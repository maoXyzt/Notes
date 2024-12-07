> [python处理数据的风骚操作[pandas 之 groupby&agg]](https://segmentfault.com/a/1190000012394176)

## 实践：

利用`pd.Grouper`实现取每个月的数据中的最新一条

```python
slicer = lead_snapshots_df.groupby(
    [pd.Grouper(key='snapshot_time', freq='M'), 'lead_code']
)['snapshot_time'].idxmax()     # 获取每月最新一条数据的索引
lead_monthly_snapshots_df = lead_snapshots_df.loc[slicer]
```

