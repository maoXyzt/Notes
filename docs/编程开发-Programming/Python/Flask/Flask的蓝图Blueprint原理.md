# Flask 的蓝图(Blueprint)原理

## 1 - 实例化一个蓝图

`flask/blueprints.py::Blueprint()`

```python
# main = Blueprint('main', __name__)
class Blueprint(_PackageBoundObject):
    warn_on_modifications = False
    _got_registered_once = False
    # 初始化
    def __init__(self, name, import_name, static_folder=None,
                 static_url_path=None, template_folder=None,
                 url_prefix=None, subdomain=None, url_defaults=None,
                 root_path=None):
        _PackageBoundObject.__init__(self, import_name, template_folder,
                                     root_path=root_path)
        self.name = name  # 蓝图的名称
        self.url_prefix = url_prefix  # url 前缀
        self.subdomain = subdomain  # 子域名。subdomain.SERVER_NAME
        self.static_folder = static_folder
        self.static_url_path = static_url_path
        self.deferred_functions = []  # 用于注册 url 规则的一组函数
                        # 在添加 url 规则时会调用用 self.record()或 self.record_once()添加
        if url_defaults is None:
            url_defaults = {}  # 调用视图函数的默认参数
        self.url_values_defaults = url_defaults

# 蓝图的基类
class _PackageBoundObject(object):
    def __init__(self, import_name, template_folder=None, root_path=None):
        # 包或模块的名称，实例化时通常传入的参数为 __name__，
        self.import_name = import_name
        #
        self.template_folder = template_folder
        # root_path: app 的根路径
        # 如果没有指定 root_path，就会根据包或模块的名称来获取根路径
        if root_path is None:
            root_path = get_root_path(self.import_name)
        self.root_path = root_path

        self._static_folder = None
        self._static_url_path = None
```

## 2 - 在蓝图中添加 url 路由规则

`flask/blueprints.py::Blueprint().add_url_rule()`

```python
class Blueprint(_PackageBoundObject):
    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        if endpoint:
            assert '.' not in endpoint, "Blueprint endpoints should not contain dots"
        # 生成了一个闭包，参数都是添加路由规则的时候传进来的参数。
        # # 这个闭包被添加到 self.deferred_functions 列表中。
        # # 在 Blueprint().register()中可以看到如何调用。
        self.record(lambda s:
            s.add_url_rule(rule, endpoint, view_func, **options))
```

## 3 - 将蓝图注册到 app 上

### 3.1 Flask.register_blueprint

`app.py::Flask().register_blueprint()`

```python
class Flask(_PackageBoundObject):
    def register_blueprint(self, blueprint, **options):  # 注意 options 将一直向下传递
        first_registration = False
        # 检查蓝图的命名冲突
        if blueprint.name in self.blueprints:
            assert self.blueprints[blueprint.name] is blueprint, \
                'A blueprint\'s name collision occurred between %r and ' \
                '%r.  Both share the same name "%s".  Blueprints that ' \
                'are created on the fly need unique names.' % \
                (blueprint, self.blueprints[blueprint.name], blueprint.name)
        else:
            self.blueprints[blueprint.name] = blueprint
            self._blueprint_order.append(blueprint)  # 将蓝图添加到列表中(按蓝图注册顺序)
            first_registration = True
        blueprint.register(self, options, first_registration)  # 注册蓝图
```

### 3.2 Blueprint.register

`blueprints.py::Blueprint().register()`

```python
class Blueprint(_PackageBoundObject):
    def register(self, app, options, first_registration=False):
        self._got_registered_once = True  # 标记该蓝图为已注册
        # 初始化蓝图的状态，一个 BlueprintSetupState()类的实例
        state = self.make_setup_state(app, options, first_registration)
        if self.has_static_folder:
            # 注册静态目录的 url 到 endpoint 'static'上
            state.add_url_rule(self.static_url_path + '/<path:filename>',
                               view_func=self.send_static_file,
                               endpoint='static')

        for deferred in self.deferred_functions:
            deferred(state)  # 真正将 url 规则注册到 app 上的地方
                             # 调用 state.add_url_rule()，参数是注册路由时的参数
```

### 3.3 BlueprintSetupState 类

`BlueprintSetupState` 类: 临时储存蓝图状态

`blueprints.py::BlueprintSetupState().__init__()`

```python
class BlueprintSetupState(object):
    def __init__(self, blueprint, app, options, first_registration):
        self.app = app
        self.blueprint = blueprint
        # 在这里处理注册蓝图时提供的选项 options
        # # 以下三个选项会覆盖 Blueprint 初始化时的选项。
        # # 其余参数会储存，但从 self.add_url_rule()可以看出，其余参数实际上没被用到。
        # # 因此，用 app.register_blueprint()注册蓝图时,
        # # 除了命名了的参数以外，也就只有下面的三个参数是有效的。 <- 文档没写的东西
        self.options = options

        self.first_registration = first_registration  # `first_registion` 的用途
        # `subdomain` -> 默认为蓝图的 subdomain（蓝图的 subdomain 默认为 None）
        # # 即优先级顺序：注册蓝图时给定 > 蓝图实例化时给定的
        # # 但是在 self.add_url_rule(）中可以看到，注册 url 时给定的值有限级更高。
        subdomain = self.options.get('subdomain')
        if subdomain is None:
            subdomain = self.blueprint.subdomain
        self.subdomain = subdomain
        # `url_prefix` -> 默认为蓝图的 url_prefix（蓝图的 url_prefix 默认为 None）
        url_prefix = self.options.get('url_prefix')
        if url_prefix is None:
            url_prefix = self.blueprint.url_prefix
        self.url_prefix = url_prefix
        # `url_defaults` -> 默认为蓝图的 url_defaults（蓝图的 url_defaults 默认为 None）
        self.url_defaults = dict(self.blueprint.url_values_defaults)
        self.url_defaults.update(self.options.get('url_defaults', ()))

    # 真正将蓝图的 url 规则注册到 app 上的函数
    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        # 给 url 添加蓝图的前缀 `url_prefix`
        if self.url_prefix:
            rule = self.url_prefix + rule
        # 设置子域名 `subdomain` 选项，注册 url 规则时有指定，就用指定的值,
        # # 否则用 BlueprintSetupState 初始化的值（注册蓝图时的 > 蓝图实例化时的）
        options.setdefault('subdomain', self.subdomain)
        # 未指定 endpoint 时，从视图函数获取 endpoint（即使用视图函数的 __name__）
        # # 如果无视图函数，则必须指定 endpoint
        if endpoint is None:
            endpoint = _endpoint_from_view_func(view_func)
        defaults = self.url_defaults  # 调用视图函数的默认参数字典 `url_defaults`
        if 'defaults' in options:  # 添加 url 规则时的 defaults 参数 <-实际是 Rule()使用的参数
                                   # `defaults` 参数值为一个字典(可以用**解引用)
                                   # 作用跟实例化蓝图和注册蓝图时的 url_defaults 一样，
                                   # 优先级更高。
            defaults = dict(defaults, **options.pop('defaults')) # 更新 defaults 的值
        # 最终还是要调用 Flask()实例的 add_url_rule 方法来添加路由规则
        # # endpoint 名带上了蓝图名作为前缀
        # # 文档没写 defaults = defaults 这个参数
        self.app.add_url_rule(rule, '%s.%s' % (self.blueprint.name, endpoint),
                              view_func, defaults=defaults, **options)
```

### 3.4 - Flask.add_url_rule

`Flask()` 实例中是怎么添加路由规则的

`flask/app.py::Flask().add_url_rule()`

```python
class Flask(_PackageBoundObject):
    @setupmethod  # <- 在 debug 模式下，如果被装饰的函数在 app 初始化之后调用，将发出警告
    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        # 给定 endpoint，或为视图函数的 __name__
        if endpoint is None:
            endpoint = _endpoint_from_view_func(view_func)
        options['endpoint'] = endpoint
        # 添加路由规则时可以指定 methods 参数，即路由规则支持的 HTTP 方法
        # # 如果没有指定，则使用视图函数的 methods 属性的值（元组或列表）
        # # 如果视图函数也没有 methods 属性或 methods 值为空，则默认支持为'GET'方法
        # # 根据 flask 的文档，还将隐式添加支持'HEAD'方法。
        methods = options.pop('methods', None)
        if methods is None:
            methods = getattr(view_func, 'methods', None) or ('GET',)
        if isinstance(methods, string_types):
            raise TypeError('Allowed methods have to be iterables of strings, '
                            'for example: @app.route(..., methods=["POST"])')
        methods = set(item.upper() for item in methods)

        # 表示必须支持的 HTTP 方法，这些方法会被添加到 methods 中
        # # 取值来自视图函数，或为空集
        required_methods = set(getattr(view_func, 'required_methods', ()))

        # provide_automatic_options 表示是否需要使用内置的对 OPTION 方法的支持
        # # 未提供参数值时，根据视图函数是否支持 OPTIONS 方法来确定参数的取值
        provide_automatic_options = getattr(view_func,
            'provide_automatic_options', None)
        if provide_automatic_options is None:
            if 'OPTIONS' not in methods:
                provide_automatic_options = True
                required_methods.add('OPTIONS')
            else:
                provide_automatic_options = False

        # 将 required_methods 添加到 methods 中
        methods |= required_methods

        # 创建路由规则，是一个 url_rule_class 类的实例
        # # url_rule_class 类默认就是 werkzeug.routing.Rule 类（不能设为其他类，除非改源码）
        rule = self.url_rule_class(rule, methods=methods, **options)
        rule.provide_automatic_options = provide_automatic_options

        # app.url_map 是 werkzeug.routing.Map 类的一个实例
        self.url_map.add(rule)
        # 将视图函数添加到 app.view_funtions 字典中，键为 endpoint 参数值
        # # 禁止不相同的视图函数用相同的 endpoint
        if view_func is not None:
            old_func = self.view_functions.get(endpoint)
            if old_func is not None and old_func != view_func:
                raise AssertionError('View function mapping is overwriting an '
                                     'existing endpoint function: %s' % endpoint)
            self.view_functions[endpoint] = view_func
```

### 3.5 - 路由 Rule 类

```python
@implements_to_string
class Rule(RuleFactory):

    """A Rule represents one URL pattern.  There are some options for `Rule`
    that change the way it behaves and are passed to the `Rule` constructor.
    Note that besides the rule-string all arguments *must* be keyword arguments
    in order to not break the application on Werkzeug upgrades.

    `string`
        Rule strings basically are just normal URL paths with placeholders in
        the format ``<converter(arguments):name>`` where the converter and the
        arguments are optional.  If no converter is defined the `default`
        converter is used which means `string` in the normal configuration.

        URL rules that end with a slash are branch URLs, others are leaves.
        If you have `strict_slashes` enabled (which is the default), all
        branch URLs that are matched without a trailing slash will trigger a
        redirect to the same URL with the missing slash appended.

        The converters are defined on the `Map`.

    `endpoint`
        The endpoint for this rule. This can be anything. A reference to a
        function, a string, a number etc.  The preferred way is using a string
        because the endpoint is used for URL generation.

    `defaults`
        An optional dict with defaults for other rules with the same endpoint.
        This is a bit tricky but useful if you want to have unique URLs::

            url_map = Map([
                Rule('/all/', defaults={'page': 1}, endpoint='all_entries'),
                Rule('/all/page/<int:page>', endpoint='all_entries')
            ])

        If a user now visits ``http://example.com/all/page/1`` he will be
        redirected to ``http://example.com/all/``.  If `redirect_defaults` is
        disabled on the `Map` instance this will only affect the URL
        generation.

    `subdomain`
        The subdomain rule string for this rule. If not specified the rule
        only matches for the `default_subdomain` of the map.  If the map is
        not bound to a subdomain this feature is disabled.

        Can be useful if you want to have user profiles on different subdomains
        and all subdomains are forwarded to your application::

            url_map = Map([
                Rule('/', subdomain='<username>', endpoint='user/homepage'),
                Rule('/stats', subdomain='<username>', endpoint='user/stats')
            ])

    `methods`
        A sequence of http methods this rule applies to.  If not specified, all
        methods are allowed. For example this can be useful if you want different
        endpoints for `POST` and `GET`.  If methods are defined and the path
        matches but the method matched against is not in this list or in the
        list of another rule for that path the error raised is of the type
        `MethodNotAllowed` rather than `NotFound`.  If `GET` is present in the
        list of methods and `HEAD` is not, `HEAD` is added automatically.

        .. versionchanged:: 0.6.1
           `HEAD` is now automatically added to the methods if `GET` is
           present.  The reason for this is that existing code often did not
           work properly in servers not rewriting `HEAD` to `GET`
           automatically and it was not documented how `HEAD` should be
           treated.  This was considered a bug in Werkzeug because of that.

    `strict_slashes`
        Override the `Map` setting for `strict_slashes` only for this rule. If
        not specified the `Map` setting is used.

    `build_only`
        Set this to True and the rule will never match but will create a URL
        that can be build. This is useful if you have resources on a subdomain
        or folder that are not handled by the WSGI application (like static data)

    `redirect_to`
        If given this must be either a string or callable.  In case of a
        callable it's called with the url adapter that triggered the match and
        the values of the URL as keyword arguments and has to return the target
        for the redirect, otherwise it has to be a string with placeholders in
        rule syntax::

            def foo_with_slug(adapter, id):
                # ask the database for the slug for the old id.  this of
                # course has nothing to do with werkzeug.
                return 'foo/' + Foo.get_slug_for_id(id)

            url_map = Map([
                Rule('/foo/<slug>', endpoint='foo'),
                Rule('/some/old/url/<slug>', redirect_to='foo/<slug>'),
                Rule('/other/old/url/<int:id>', redirect_to=foo_with_slug)
            ])

        When the rule is matched the routing system will raise a
        `RequestRedirect` exception with the target for the redirect.

        Keep in mind that the URL will be joined against the URL root of the
        script so don't use a leading slash on the target URL unless you
        really mean root of that domain.

    `alias`
        If enabled this rule serves as an alias for another rule with the same
        endpoint and arguments.

    `host`
        If provided and the URL map has host matching enabled this can be
        used to provide a match rule for the whole host.  This also means
        that the subdomain feature is disabled.

    .. versionadded:: 0.7
       The `alias` and `host` parameters were added.
    """

    def __init__(self, string, defaults=None, subdomain=None, methods=None,
                 build_only=False, endpoint=None, strict_slashes=None,
                 redirect_to=None, alias=False, host=None):
        if not string.startswith('/'):
            raise ValueError('urls must start with a leading slash')
        self.rule = string
        self.is_leaf = not string.endswith('/')

        self.map = None
        self.strict_slashes = strict_slashes
        self.subdomain = subdomain
        self.host = host
        self.defaults = defaults
        self.build_only = build_only
        self.alias = alias
        if methods is None:
            self.methods = None
        else:
            if isinstance(methods, str):
                raise TypeError('param `methods` should be `Iterable[str]`, not `str`')
            self.methods = set([x.upper() for x in methods])
            if 'HEAD' not in self.methods and 'GET' in self.methods:
                self.methods.add('HEAD')
        self.endpoint = endpoint
        self.redirect_to = redirect_to

        if defaults:
            self.arguments = set(map(str, defaults))
        else:
            self.arguments = set()
        self._trace = self._converters = self._regex = self._weights = None
```
