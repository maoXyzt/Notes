# pandas如何将NaN替换为None

场景：

数据处理后，最终需要写入数据库。用`pandas.DataFrame.to_dict`方法将DataFrame转为List[Dict]前，如果不处理DataFrame中的NaN数值，则写入数据库时也将包含有NaN。

我们希望所有值为NaN写入数据库时为Null值，这就需要将NaN转化为python中的None。

为实现这一点，可以使用`pandas.DataFrame.where`方法，代码如下：

```python
df.where(df.notna(), None).to_dict('records')
```

### where 方法介绍

> DataFrame.**where(*self*, *cond*, *other=nan*, *inplace=False*, *axis=None*, *level=None*, *errors='raise'*, *try_cast=False*) **

> Series.**where(*self*, *cond*, *other=nan*, *inplace=False*, *axis=None*, *level=None*, *errors='raise'*, *try_cast=False*)**

功能：返回一个同样shape的df，当满足条件为TRUE时，从self返回结果，否则从other返回结果

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

> numpy.**where(*condition*[, *x*, *y*])** 

当满足条件为TRUE时，从x返回结果，否则从y返回结果。

```python
df.where(m, -df) == np.where(m, df, -df)
```

### mask方法

mask方法与where方法相反，当满足条件为TRUE时，从self返回结果，否则从other返回结果。

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

