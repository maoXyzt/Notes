# python 字符串编码

## 1. python2 中的情况

python2 中，字符串 s 在 linux 系统下为 utf8 编码，在 windows 系统下为 gb2312 编码。

su 为 unicode 字符串。

```python
>>> s = "python字符串"
>>> su = u"python字符串"
>>> s   # windows 系统下，s 为 gb2312 编码
'python\xd7\xd6\xb7\xfb\xb4\xae'
>>> s   # linux 系统下，s 为 utf8 编码
'python\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2'
>>> su
u'python\u5b57\u7b26\u4e32'
```

使用 `s.encode("uft8")` 方法将字符串 s 编码为 utf8 时，会先调用 decode()方法对 s 进行解码，此时解码使用的编码方法为默认的编码方法（即 ascii）。

```python
>>> # 系统默认的编码方法为 ascii
>>> import sys
>>> sys.getdefaultencoding()
'ascii'
```

可以使用 decode()方法对字符串 s 进行解码（解码成 unicode），之后再用所需的编码方法进行编码。

```python
>>> # windows 系统下
>>> s.decode("gb2312")
u'python\u5b57\u7b26\u4e32'
>>> s.decode("gb2312").encode('utf8')
'python\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2'
>>> # linux 系统下
>>> s.decode("utf8")
u'python\u5b57\u7b26\u4e32'
>>> s.decode("utf8").encode('gb2312')
'python\xd7\xd6\xb7\xfb\xb4\xae'
```

对于.py 文件，在 python2 中，为了使解释器能够正确读取文件中的中文，需要在文件开头加上编码方式的声明

```python
# -*- coding: utf-8 -*-
```

## 2. python3 中的情况

python3 中，所有的字符串在内部都用 unicode 表示。因此，可以直接使用 encode()方法将字符串按要求的编码方式进行编码。

```python
>>> s = "python字符串"
>>> s
'python字符串'
>>> s.encode("utf8")
b'python\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2'
```
