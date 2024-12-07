# pandas时间处理：将时间转为月末日期

> 参考了stackoverflow的如下问题：
>
> [pandas: convert datetime to end-of-month](https://stackoverflow.com/questions/18233107/pandas-convert-datetime-to-end-of-month)

## 方法一（较快）：

转换为period再转换成timestamp

```python
# 以下三种方法等价
df.index = df.index.to_period('M').to_timestamp('M')
df.index = df.index.to_period('M').to_timestamp(how='e')
df.index = df.index.to_period('M').to_timestamp(how='end')
```

## 方法二：

利用`pd.tseries.offsets`中的`MonthEnd`对象

```python
df.index = df.index + pd.offsets.MonthEnd(0) 
```

## 补充：转为月初日期

```python
# 方法1
df.index = df.index.to_period('M').to_timestamp()
# 方法2
df.index = df.index + pd.offsets.MonthEnd(0) - pd.offsets.MonthEnd(1)
```

