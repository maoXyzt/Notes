# Flask 扩展的初始化

```python
db.init_db(app)
# 注册到 app.extensions 中
app.extension['sqlalchemy'] = _SQLAlchemyState(self)
```
