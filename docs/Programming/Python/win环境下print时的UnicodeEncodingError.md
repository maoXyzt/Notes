# win 环境下 print 时的 UnicodeEncodingError

在一些特殊环境下，比如在 windows 环境下，使用 python print时，可能会遇到 `UnicodeEncodingError` 的错误。

这是因为，python3 的字符串是 unicode 字符串，未经过编码。
而该环境下，stdin/stdout/stderr 的默认编码不是 utf-8，打印前调用 `str.encode()` 对字符串进行编码时，编码失败。
所以会抛出 `UnicodeEncodingError`。

为此，我们可以改变 stdin/stdout/stderr 的默认编码，或改变编码失败时的行为，让它不抛出异常。

## `PYTHONIOENCODING` 环境变量

Python3 支持环境变量 `PYTHONIOENCODING`。

```
export PYTHONIOENCODING=${encodingname}:${errorhandler}
```

它由两部分组成，以 `:` 分隔，前半部分代表 `encodingname`，后半部分代表 `errorhandler`。

它们的含义与 `str.encode()` 的参数相同，即 `encodingname` 代表编码名称，`errorhandler` 代表编码失败时的行为。

两部分都是可选的，如果不指定 `errorhandler`，则默认为 `strict`。
