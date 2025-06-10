# SQLAlchemy 2.0 基础增删改查

> 官方文档: [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html)

## 1 - 核心概念

### 1.1 SQLAlchemy 2.0 与 1.x 的区别

1. 废弃 Query 对象，改用基于 `select()` 的统一查询方式
2. 声明式模型的更新: `Mapped` 和 `mapped_column`
   1. 使用类型注解（Type Hints）和 `mapped_column` 明确定义字段属性。
   2. 类型注解（如 `Mapped[int]`）提供更好的 IDE 支持和代码可读性。
   3. `mapped_column` 可以更灵活地配置字段属性（如默认值、索引等）。
3. 推荐使用 context manager (`with` 语句) 管理连接

### 1.2 Core 与 ORM

SQLAlchemy 提供了两个不同的 API，一个建立在另一个之上。这些 API 分别被称为 Core 和 ORM。

* SQLAlchemy Core 是 SQLAlchemy 作为“database toolkit”的基础架构。该库提供了管理数据库连接、与数据库查询和结果交互以及程序化构造 SQL 语句的工具。
* SQLAlchemy ORM 基于 SQLAlchemy Core，提供了 “object relational mapping” 能力。包含:
  * 一个配置层，可将 Python 类和对象映射到数据库表。
  * Session: 一种对象持久化机制

## 2 - 连接数据库

> [Establishing Connectivity - the Engine](https://docs.sqlalchemy.org/en/20/tutorial/engine.html#establishing-connectivity-the-engine)

### 2.1 创建 Engine 实例

[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine): `sqlalchemy.engine.Engine`

```python
from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
```

> Lazy Connecting 特性:
>
> * 创建 Engine 实例的时候不会立即连接数据库，而是在需要的时候才连接。

## 3 - 事务

### 3.1 Connection 模式 vs Session 模式

当使用 Core API 时，通过 `Connection` 对象操作数据库，返回 `Result` 对象。

当使用 ORM 时，`Engine` 则由 `Session` 管理。

* 现代 SQLAlchemy 的 `Session` 强调事务，其 SQL 执行模式与 `Connection` 模式大致相同
* 实际上，`Session` 是 `Connection` 的封装，最终是调用 `Connection` 来执行 SQL
* 当传入非 ORM 的 SQL 语句时，`Session` 跟 `Connection` 没什么区别

### 3.2 Connection 模式

#### 3.2.1 获取 Connection 对象

> 文档: [class sqlalchemy.engine.Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)

用 `Engine.connect()` 方法获取 `Connection` 对象。

执行 SQL statement: 用 `text()` 构造 **textual SQL**, 用 `conn.execute()` 执行。

```python
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())
```

进入 `with` 语句块时，自动开启事务。

当退出 `with` 语句块时，事务结束，自动执行 ROLLBACK。

#### 3.2.2 Commit Changes

教程中会更多地使用 "commit as you go" 风格，而我们实际使用中可能更多地使用 "begin once" 风格。

##### "commit as you go" 风格

如果有修改，在退出前，应显式地使用 `Connection.commit()` 提交事务

```python
# "commit as you go"
with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
    )
    conn.commit()
```

> 特殊情况下，如果希望 autocommit，可参考如下文档进行配置:
>
> <https://docs.sqlalchemy.org/en/20/core/connections.html#setting-transaction-isolation-levels-including-dbapi-autocommit>

##### "begin once" 风格

用 `Connection.begin()` 显式地开启事务，如果正常退出，自动 COMMIT；如果抛出了异常，自动 ROLLBACK。

```python
# "begin once"
with engine.begin() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
    )
```

### 3.3 Session 模式

在现代 SQLAlchemy 中，当使用 ORM 时，通过 `Session` 对象进行事务和数据库交互。

> 文档: [class sqlalchemy.orm.Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)

#### 3.3.1 获取 Session 对象

同样的，推荐使用 context manager (`with` 语句) 管理 `Session` 对象。

```python
from sqlalchemy.orm import Session

stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")
with Session(engine) as session:
    result = session.execute(stmt, {"y": 6})
    for row in result:
        print(f"x: {row.x}  y: {row.y}")
```

这种情况下，也是 "commit as you go" 风格，需要在退出 `with` 语句块时，显式地使用 `Session.commit()` 提交事务。

> 更多 Session 用法，参考文档: [Basics of Using a Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#id1)

## 4 - Core API 增删改查

Core API 通过 `execute()` 方法接收 sql statement 作为参数，实现对数据库的增删改查。

### 4.1 查询结果

执行 SELECT 语句，查询结果返回 `Result` 对象实例。

#### 4.1.1 `Result` 对象

> 文档: [class sqlalchemy.engine.Result](https://docs.sqlalchemy.org/en/21/core/connections.html#sqlalchemy.engine.Result)

`Result` 对象支持迭代，每次迭代返回一个 `Row` 对象实例。

```python
with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))
    for row in result:
        print(f"x: {row.x}  y: {row.y}")
```

#### 4.1.2 `Row` 对象

> 文档: [class sqlalchemy.engine.Row](https://docs.sqlalchemy.org/en/21/core/connections.html#sqlalchemy.engine.Row)

`Row` 对象使用方法类似于 python 的 `namedtuple`，可以用以下四种方式访问值:

（假设: `result = conn.execute(text("select x, y from some_table"))`）

##### (1) Tuple Assignment

```python
for x, y in result:
    ...
```

##### (2) Integer Index

```python
for row in result:
    x = row[0]
    y = row[1]
```

##### (3) Attribute Name

大部分情况下，`Row` 对象的属性名与表的列名相同，也可以通过 SELECT 语句显式指定。但个别情况下，名字会受数据库特性影响。

```python
for row in result:
    x = row.x
    y = row.y
```

##### (4) Mapping Access

通过 `Result.mappings()` 方法，将 `Result` 对象转为 `MappingResult` 对象。迭代时返回 `RowMapping` 对象 (read-only)。

> 文档:
>
> * [class sqlalchemy.engine.MappingResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.MappingResult)
> * [class sqlalchemy.engine.RowMapping](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.RowMapping)

```python
for dict_row in result.mappings():
    x = dict_row["x"]
    y = dict_row["y"]
```

### 4.2 传参

`execute()` 接受 [bound parameters](https://docs.sqlalchemy.org/en/20/glossary.html#term-bound-parameters) 作为参数。

SQL 语句中使用 `:param_name` 表示参数，在 `execute()` 中传入 `{param_name: value}` 形式的字典。

```python
with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2})
    for row in result:
        print(f"x: {row.x}  y: {row.y}")
```

#### 4.2.1 executemany

当执行 [DML](https://docs.sqlalchemy.org/en/20/glossary.html#term-DML) 语句（如 `INSERT`, `UPDATE`, `DELETE`）时，可以传入包含多个参数的列表。

语句会被执行多次，依次从参数列表中取值。

这种执行风格叫做 [executemany](https://docs.sqlalchemy.org/en/20/glossary.html#term-executemany)。

```python
with engine.connect() as conn:
    result = conn.execute(
        text("SELECT x, y FROM some_table WHERE y > :y"),
        [{"y": 2}, {"y": 3}],
    )
```

**execute** *vs* **executemany**

* executemany 方式下，执行过程会得到优化，实现更高的性能
* executemany 方式不支持返回结果 (唯一例外: 使用 `insert()` 构建的语句)

## 5 - ORM 增删改查

> (Data Manipulation with the ORM)(<https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html>)

当使用 textual SQL 时，Session 与 Connection 的执行模式大致相同。

本节主要介绍对 ORM 的增删改查。

### 5.1 查询

> 文档: [Selecting ORM Entities and Columns](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-selecting-orm-entities)

SQLAlchemy 的 ORM 提供了一系列 SQL constructs 来构建查询语句。

#### 5.1.1 增

##### (1) `insert()` SQL Expression Construct

使用 `insert()` 构造 `Insert` 对象，它表示一条 `INSERT` 语句。

> * [function sqlalchemy.sql.expression.insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert)
> * [class sqlalchemy.sql.expression.Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert)

```python
from sqlalchemy import insert
stmt = insert(user_table).values(name="spongebob", fullname="Spongebob Squarepants")
```

通常情况下，不需要显式调用 `.values()` 方法。通过在执行时传入参数，也可实现相同效果。

> 高级用法:
>
> 在用到 scalar subquery (子查询) 时, 同时使用 `.values()` 和执行时传入参数。
>
> 参考 [文档的 "Deep Alchemy" 部分](https://docs.sqlalchemy.org/en/20/tutorial/data_insert.html)

##### (2) SQL Statement

大部分 SQL 语句都支持直接 print 出来。

用 `stmt.compile()` 可以获取编译后的 SQL 语句 (`Compiled` 对象)。

> 文档: [class sqlalchemy.engine.Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled)

```python
compiled = stmt.compile()
```

##### (3) 执行

```python
with engine.connect() as conn:
    result = conn.execute(stmt)
    conn.commit()
```

执行 INSERT 语句不会返回 rows。

当只插入一条记录时，通常支持返回在执行 INSERT 时自动生成的默认值（例如，primary key）。

```python
result.inserted_primary_key
# (1,)
```

支持 "executemany" 风格，实现批量插入:

```python
with engine.connect() as conn:
    result = conn.execute(
        insert(user_table),
        [
            {"name": "sandy", "fullname": "Sandy Cheeks"},
            {"name": "patrick", "fullname": "Patrick Star"},
        ],
    )
    conn.commit()
```

##### (4) INSERT...RETURNING

对于支持 `RETURNING` 的数据库，可以使用 `Insert.returning()` 方法，显式要求返回插入的值。

```python
insert_stmt = insert(address_table).returning(
    address_table.c.id, address_table.c.email_address
)
print(insert_stmt)
# INSERT INTO address (id, user_id, email_address)
# VALUES (:id, :user_id, :email_address)
# RETURNING address.id, address.email_address
```

也可以和 `Insert.from_select()` 一起使用:

```python
select_stmt = select(user_table.c.id, user_table.c.name + "@aol.com")
insert_stmt = insert(address_table).from_select(
    ["user_id", "email_address"], select_stmt
)
print(insert_stmt.returning(address_table.c.id, address_table.c.email_address))
# INSERT INTO address (user_id, email_address)
# SELECT user_account.id, user_account.name || :name_1 AS anon_1
# FROM user_account RETURNING address.id, address.email_address
```

#### 5.1.2 查询

> 文档: [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/tutorial/orm_data_select.html#tutorial-orm-data-select)

使用 `select()` construct 构造 `Select` 对象，表示 `SELECT` 语句。

> 文档: [function sqlalchemy.sql.expression.select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select)

```python
print(select(User))
# SELECT user_account.id, user_account.name, user_account.fullname
# FROM user_account
```

##### (1) 查询整个 ORM 对象

当使用 `Session.execute()` 查询 ORM 映射对象时，返回的数据中，每一项都是一个被查询的 ORM 映射对象。

(用 `Connection.execute()` 执行查询时，返回的数据是普通的 `Row` 对象)

```python
stmt = select(User).where(User.name == "spongebob")
with Session(engine) as session:
    for row in session.execute(stmt):
        print(row)
# BEGIN (implicit)
# SELECT user_account.id, user_account.name, user_account.fullname
# FROM user_account
# WHERE user_account.name = ?
# [...] ('spongebob',)
# (User(id=1, name='spongebob', fullname='Spongebob Squarepants'),)
# ROLLBACK
```

在结果上调用 `.first()` 方法，返回只有一个元素的 `Result` 对象。

```python
row = session.execute(select(User)).first()
row
# (User(id=1, name='spongebob', fullname='Spongebob Squarepants'),)
```

推荐用 `Session.scalars()` 方法，返回一个 `ScalarResult` 对象，再调用 `.first()` 方法可直接得到结果对象。

```python
user = session.scalars(select(User)).first()
user
# User(id=1, name='spongebob', fullname='Spongebob Squarepants')
```

##### (2) 查询特定列

用 `select()` 的参数指定要查询的列。

```python
row = session.execute(select(User.name, User.fullname)).first()
row
# ('spongebob', 'Spongebob Squarepants')
```

##### (3) 列与 ORM 对象混合查询

```python
session.execute(
    select(User.name, Address).where(User.id == Address.user_id).order_by(Address.id)
).all()
```

##### (4) Labeled SQL Expressions

用 `ColumnElement.label()` 方法为列指定别名。

```python
from sqlalchemy import func, cast
stmt = select(
    ("Username: " + user_table.c.name).label("username"),
).order_by(user_table.c.name)
with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(f"{row.username}")
# Username: spongebob
```

##### (5) Where 子句

`Select.where()` 方法支持将包含 `Column` 对象的 `==`, `!=`, `<`, `>=`, `>`, `<=` 等表达式转为 where 子句。

```python
stmt = select(User).where(User.name == "spongebob")
```

“AND” 和 “OR” 连接符分别使用 `and_()` 和 `or_()` 函数构造。

```python
from sqlalchemy import and_, or_
print(
    select(Address.email_address).where(
        and_(
            or_(User.name == "squidward", User.name == "sandy"),
            Address.user_id == User.id,
        )
    )
)
```

对于简单相等关系，也可以用 `Select.filter_by()` 方法构造。

```python
stmt = select(User).filter_by(name="spongebob")
```

##### (6) 显式的 FROM 和 JOIN

对于两表之间有外键关系的情况，SQLAlchemy 会自动生成 JOIN 语句。

`Select.join_from()` 方法支持显式指定 `FROM` 子句。需要传入 JOIN 关系中的左表和右表。

```python
print(
    select(user_table.c.name, address_table.c.email_address).join_from(
        user_table, address_table
    )
)
# SELECT user_account.name, address.email_address
# FROM user_account JOIN address ON user_account.id = address.user_id
```

`Select.join()` 方法只需要传入 JOIN 关系中的右表。

```python
print(select(user_table.c.name, address_table.c.email_address).join(address_table))
# SELECT user_account.name, address.email_address
# FROM user_account JOIN address ON user_account.id = address.user_id
```

`Select.select_from()` 方法支持指定子查询的 `FROM` 子句。

```python
from sqlalchemy import func
print(select(func.count("*")).select_from(user_table))
# SELECT count(:count_2) AS count_1
# FROM user_account
```

**ON 子句**

`Select.join()` 和 `Select.join_from()` 方法支持指定 `ON` 子句。

```python
print(
    select(address_table.c.email_address)
    .select_from(user_table)
    .join(address_table, user_table.c.id == address_table.c.user_id)
)
```

**OUTER和FULL**

```python
print(select(user_table).join(address_table, isouter=True))
# SELECT user_account.id, user_account.name, user_account.fullname
# FROM user_account LEFT OUTER JOIN address ON user_account.id = address.user_id
print(select(user_table).join(address_table, full=True))
# SELECT user_account.id, user_account.name, user_account.fullname
# FROM user_account FULL OUTER JOIN address ON user_account.id = address.user_id
```

##### (7) ORDER BY, GROUP BY, HAVING

> 文档: [ORDER BY, GROUP BY, HAVING](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#order-by-group-by-having)
