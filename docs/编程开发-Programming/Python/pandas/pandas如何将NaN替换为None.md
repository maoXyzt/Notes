# pandas 如何将 NaN 替换为 None: where 和 mask 方法

场景：

数据处理后，最终需要写入数据库。用 `pandas.DataFrame.to_dict` 方法将 DataFrame 转为 `List[Dict]` 前，如果不处理 DataFrame 中的 NaN 数值，则写入数据库时也将包含有 NaN。

我们希望所有值为 NaN 写入数据库时为 Null 值，这就需要将 NaN 转化为 python 中的 None。

为实现这一点，可以使用 `pandas.DataFrame.where` 方法，代码如下：

```python
df.where(df.notna(), None).to_dict('records')
```

## 1 - 用 `where` 方法

```python
DataFrame.where(self, cond, other=nan, inplace=False, axis=None, level=None, errors='raise', try_cast=False)
Series.where(self, cond, other=nan, inplace=False, axis=None, level=None, errors='raise', try_cast=False)
```

功能：返回一个同样 shape 的 df，当满足条件为 TRUE 时，从 self 返回结果，否则从 other 返回结果

```python
>>> s = pd.Series(range(5))
>>> s.where(s > 0)
0    NaN
1    1.0
2    2.0
3    3.0
4    4.0
dtype: float64
```

> 类似 `numpy.where(condition[, x, y])`

当满足条件为 TRUE 时，从 x 返回结果，否则从 y 返回结果。

```python
df.where(m, -df) == np.where(m, df, -df)
```

## 2 - 用 `mask` 方法

mask 方法与 where 方法相反，当满足条件为 TRUE 时，从 self 返回结果，否则从 other 返回结果。

```python
>>> s = pd.Series(range(5))
>>> s.mask(s > 0)
0    0.0
1    NaN
2    NaN
3    NaN
4    NaN
dtype: float64
```

```python
df.where(m, -df) == df.mask(~m, -df)
```
