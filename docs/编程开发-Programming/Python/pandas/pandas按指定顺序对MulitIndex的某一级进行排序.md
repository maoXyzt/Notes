# pandas 按指定顺序对 MultiIndex 的某一级进行排序: reindex 方法

当需要对某一级索引进行自定义顺序的排序时，可以用 `pandas.DataFrame.reindex` 方法

例如：

```python
# columns 有两级，排序前如下
# lv0:  A     B        C
# lv1:  F  M  F  M  L  F  M  L
# 对 lv1 的索引进行排序
df = df.reindex(columns=['L', 'F', 'M'], level=1)
# 结果
# lv0:  A     B        C
# lv1:  F  M  L  F  M  L  F  M
# 注意，A 下只有 F 和 M，不会使 A 增加 L 列。
```

注：如果不需要自定义顺序的排序，可以用 `pandas.DataFrame.sort_index` 方法。
