# Flask app 的实例化和初始化

典型的 flask 工厂函数 create_app 的定义

```python
# apps/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    # 注册蓝本
    from . import projects
    app.register_blueprint(projects.projects_blueprint)

    return app
```

## 1 - Flask 实例(app)初始化

```python
# flask/apps.py
# import_name 字段必须提供，其余可以在 config 中设置
class Flask(_PackageBoundObject):
    # ...

    def __init__(
            self,
            import_name,    # app 的名称
            static_url_path = None,
            static_folder ='static',
            static_host = None,
            host_matching = False,
            subdomain_matching = False,
            template_folder ='templates',
            instance_path = None,
            instance_relative_config = False,
            root_path = None
        ):
        # ...
        # 用默认值初始化配置
        self.config = self.make_config(instance_relative_config)
        # ...

    # 返回默认的 flask.config.Config 类实例
    def make_config(self, instance_relative = False):
        # app 根目录位置
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path
        # 默认配置字典
        defaults = dict(self.default_config)
        # helpers.py:: get_env()
        ## 获取环境变量'FLASK_ENV'的值，未设置环境变量时，默认为'production'
        defaults ['ENV'] = get_env()
        # helpers.py:: get_debug_flag()
        ## 获取环境变量'FLASK_DEBUG'的值
        ## 如果未设置，当 get_env() == 'development'时为 True，否则为 False
        ## 如果已设置，当值属于('0', 'false', 'no')时为 True，否则为 False
        defaults ['DEBUG'] = get_debug_flag()
        # self.config_class 为 flask.config.Config 类
        ## 返回用默认值初始化的 Config 类实例
        return self.config_class(root_path, defaults)

    # 默认配置
    default_config = ImmutableDict({
        'ENV':                                  None,
        'DEBUG':                                None,
        'TESTING':                              False,
        'PROPAGATE_EXCEPTIONS':                 None,
        'PRESERVE_CONTEXT_ON_EXCEPTION':        None,
        'SECRET_KEY':                           None,
        'PERMANENT_SESSION_LIFETIME':           timedelta(days = 31),
        'USE_X_SENDFILE':                       False,
        'SERVER_NAME':                          None,
        'APPLICATION_ROOT':                     '/',
        'SESSION_COOKIE_NAME':                  'session',
        'SESSION_COOKIE_DOMAIN':                None,
        'SESSION_COOKIE_PATH':                  None,
        'SESSION_COOKIE_HTTPONLY':              True,
        'SESSION_COOKIE_SECURE':                False,
        'SESSION_COOKIE_SAMESITE':              None,
        'SESSION_REFRESH_EACH_REQUEST':         True,
        'MAX_CONTENT_LENGTH':                   None,
        'SEND_FILE_MAX_AGE_DEFAULT':            timedelta(hours = 12),
        'TRAP_BAD_REQUEST_ERRORS':              None,
        'TRAP_HTTP_EXCEPTIONS':                 False,
        'EXPLAIN_TEMPLATE_LOADING':             False,
        'PREFERRED_URL_SCHEME':                 'http',
        'JSON_AS_ASCII':                        True,
        'JSON_SORT_KEYS':                       True,
        'JSONIFY_PRETTYPRINT_REGULAR':          False,
        'JSONIFY_MIMETYPE':                     'application/json',
        'TEMPLATES_AUTO_RELOAD':                None,
        'MAX_COOKIE_SIZE': 4093,
    })

    # ...
```

## 2 - 项目的配置初始化

`app.config` 为 `flask.Config` 类的一个实例，`Config` 类继承自 `dict` 类，额外提供了一些用于从文件、对象等方式填充键值的方法。

项目常用的是用 `app.config.from_object()` 从自定义的对象中加载配置：

```python
# flask/config.py
class Config(dict):
    # 对象中所有名称大写的属性都被视为配置的关键字
    def from_object(self, obj):
        if isinstance(obj, string_types):
            obj = import_string(obj)
        for key in dir(obj):
            if key.isupper():
                self [key] = getattr(obj, key)
```

还有其他的方法

```python
from_envvar
from_pyfile
from_json
from_mapping
```

## 3 - Flask app 的响应流程

一个最简单的 flask 工作流程：

```bash
HTTP Request
|> WSGI Server
|> hook (before_first_request, before_request)
|> Router
|> View Function
|> hook (after_first_request, after_request)
|> WSGI Server
-> HTTP Response
```

WSGI
