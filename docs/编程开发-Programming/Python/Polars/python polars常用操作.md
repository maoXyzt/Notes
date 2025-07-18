# Python Polars 常用操作

## 1 - lazy 模式

lazy 模式读取数据:

```python
lazy = pl.scan_parquet(parquet_file_path)
```

DataFrame 转为 LazyFrame:

```python
lazy = df.lazy()
```

把 LazyFrame 导出:

```python
lazy.sink_parquet(parquet_file_path)
```

## 2 - LazyFrame 的常用操作

### 2.1 数据过滤

```python
lazy.filter(pl.col("column_name") == "value")
```

### 2.2 数据列选择

```python
lazy.select(["column_name1", "column_name2"])
```

### 2.3 获取符合条件的数据总行数

```python
lazy.filter(pl.col("column_name") == "value").select(pl.count()).collect().item()
```

### 2.4 新增、替换列

根据已有列生成新列:

```python
lazy.with_columns(
  pl.col("column_name")
  .alias("new_column_name")
)
```

用默认值生成新列:

```python
lazy.with_columns(
  pl.lit("default_value", dtype=pl.Utf8)
  .alias("new_column_name")
)
```

### 2.5 条件赋值

```python
lazy.with_columns(
  pl.when(pl.col("column_name") == "value")
  .then(pl.lit("new_value"))
  .otherwise(pl.col("column_name"))
  .alias("new_column_name")
)
```

### 2.6 查询 Schema

```python
schema = lazy.collect_schema()
for col in schema.names():
  col_type = schema[col]
  print(col, col_type)
# 输出:
# column_name Utf8  # <== pl.Utf8
# another_column Int64  # <== pl.Int64
```
