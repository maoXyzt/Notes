# SQLAlchemy与数据库交互的方式

## 一、ORM方式(通过session)

### 1. 查

利用Query对象

> [Tutorial](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html)

> [API](http://docs.sqlalchemy.org/en/latest/orm/query.html)

```python
# query from a class
session.query(User).filter_by(name='ed').all()

# query with multiple classes, returns tuples
session.query(User, Address).join('addresses').filter_by(name='ed').all()

# query using orm-enabled descriptors
session.query(User.name, User.fullname).all()

# query from a mapper
user_mapper = class_mapper(User)
session.query(user_mapper)
```

或者

```python
User.query.filter_by(...).order_by(...).all()
```

+ `session.query(...)`返回Query对象实例
+ `Query.all()`返回Query对象的查询结果(result对象实例)列表
+ `Query.first()`返回一个查询结果(result对象实例)或None
+ `Query.one()`返回一个查询结果(result对象实例)或引发NoResultFound异常
+ `Query.one_or_none()`返回None，一个查询结果(result对象实例)，或引发MultipleResultsFound异常

result实例的方法

```python
user1.keys()    # 返回查询结果的字段名list（有序）
user1.id        # 根据字段名获取字段值
user1[2]        # 按字段下标取值
for val in user1:
    print val   # 可迭代，依次获取每个字段值
dict(zip(user1.keys(), user1))  # 转为键值字典
```

### 2. 增

```python
user1 = User(name='tom')
db.session.add(user1)
db.session.add_all([user1, user2, user3, ...])

db.session.commit()
```

在seesion.add()之后，新增的记录不会立即插入数据库，其状态为pending。
>关于object的状态，见[Quickie Intro to Object States](http://docs.sqlalchemy.org/en/latest/orm/session_state_management.html#session-object-states)

```python
# 可查询当前新增（未提交）的记录
db.session.new
```

但在被查询时会触发session的flush过程，将pending状态的记录写入数据库(状态变为persistent)。

### 3. 改

直接给字段赋值或通过update({k: v, ...})

```python
# 直接修改实例的属性
user1.name = 'tommy'
# 利用Query的update函数
session.query(...).filter(...).update({k: v, ...})

db.session.commit()
```

```python
# 可查询当前已修改（未提交）的记录
db.session.new
```

### 4. 删

```python
# 将实例放入sesssion并标记为删除的
db.session.delete(user1)
# 删除符合筛选条件的记录。返回符合筛选条件的记录数量
db.session.query(User).filter(User.id==1).delete(synchronize_session='evaluate')

db.session.commit()
```

### 5. 回滚

回滚上一次commit的内容

```python
session.rollback()
```

## 二、执行原生sql语句的方式

### 1. 基本操作

通过`Engine`生成的[Connection](http://docs.sqlalchemy.org/en/latest/core/connections.html)对象的`execute()`方法，执行原生的sql语句：

```python
with db.engine.connect() as conn:
    conn.execute(sql)
    conn.execute(sqlalchemy.sql.text(sql), **param_dict)
```

（另一种方式：直接用`db.engine.execute()`方法）

返回ResultProxy对象实例，为对DB-API cursor的封装

> [ResultProxy](http://docs.sqlalchemy.org/en/latest/core/connections.html#sqlalchemy.engine.ResultProxy)

 从ResultProxy对象实例获得RowProxy对象实例

```python
.fetchall()     # 取完全部行之后，将自动释放cursor
.fetchone()
.fetchmany(size=None)
.first()    # 返回第一行或None，然后立即关闭结果集（调用.close())
```

从RowProxy对象实例获取column值的方法

```python
row = fetchone()

col1 = row[0]    # access via integer position

col2 = row['col2']   # access via name

col3 = row[mytable.c.mycol] # access via Column object.
```

补充：

将查询结果转为字典

```python
for row in results_proxy:
    record_dict = {tup[0]:tup[1] for tup in row.items()}
```

### 2. 事务

`Connetion.begin()`返回一个`Transaction`对象

```python
connection = engine.connect()
trans = connection.begin()
try:
    r1 = connection.execute(table1.select())
    connection.execute(table1.insert(), col1=7, col2='this is some data')
    trans.commit()
except:
    trans.rollback()
    raise
```

可以使用with语法来管理事务：

```python
with engine.begin() as connection:
    r1 = connection.execute(table1.select())
    connection.execute(table1.insert(), col1=7, col2='this is some data')
### 或 ###
with connection.begin() as trans:
    r1 = connection.execute(table1.select())
    connection.execute(table1.insert(), col1=7, col2='this is some data')
```
