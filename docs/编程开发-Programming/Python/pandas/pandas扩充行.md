# pandas 扩充行

## 简单 Index

对于简单的时间序列索引，用 `reindex` 可以实现行的扩充。

## MultiIndex

对于 MultiIndex，只在某个 level 上应用 `reindex` 不会使行扩充，只会对存在的行进行排序。因此需要生成完整的 MultiIndex 索引。

为此，可以使用 `pd.MultiIndex.levels` 方法取出已有的各级索引，然后用 `pd.MultiIndex.from_product` 生成新索引，新索引是旧索引的笛卡尔积

例如:

```python
# 原有索引列
df.index.names
# Out[1]:
# FrozenList(['employee_id', 'lead_code', 'start_time'])
#

df.index.names.unique()
# Out[2]:
# DatetimeIndex(['2019-01-31', '2019-02-28', '2019-03-31', '2019-04-30',
#                '2019-05-31'],
#               dtype='datetime64[ns]', name='start_time', freq=None)

# 需要扩充 start_time 这一列的索引，使对于所有的'employee_id'和'lead_code'，都有如下时间的行：
time_range = ['2019-01-31', '2019-02-28', '2019-03-31', '2019-04-30',
               '2019-05-31', '2019-06-30']
new_index = pd.MultiIndex.from_product([df.index.levels[0], df.index.levels[1], time_range], names=['employee_id', 'lead_code', 'start_time'])
```
