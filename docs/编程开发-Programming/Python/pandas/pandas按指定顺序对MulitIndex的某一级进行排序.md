当需要对某一级索引进行自定义顺序的排序时，可以用`pandas.DataFrame.reindex`方法

例如：

```python
# columns有两级，排序前如下
# lv0:  A     B        C      
# lv1:  F  M  F  M  L  F  M  L
# 对lv1的索引进行排序
df = df.reindex(columns=['L', 'F', 'M'], level=1)
# 结果
# lv0:  A     B        C      
# lv1:  F  M  L  F  M  L  F  M
# 注意，A下只有F和M，不会使A增加L列。
```

注：如果不需要自定义顺序的排序，可以用`pandas.DataFrame.sort_index`方法。