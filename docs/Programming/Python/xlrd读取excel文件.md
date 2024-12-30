# Python用xlrd读取Excel文件

```python
file_path = r"ABC.xlsx"
# 打开文件
book = xlrd.open_workbook(file_path)
# 选择sheet
sheet = book.sheets()[0]

# 获取行列总数
n_rows = sheet.nrows
n_cols = sheet.ncols

# 获取某个单元格
the_cell = sheet.cell(1, 4)
val = the_cell.value
```
