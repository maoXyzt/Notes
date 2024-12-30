# python字符串编码

## 1. python2中的情况

python2中，字符串s在linux系统下为utf8编码，在windows系统下为gb2312编码。

su为unicode字符串。

```python
>>> s = "python字符串"
>>> su = u"python字符串"
>>> s   # windows系统下，s为gb2312编码
'python\xd7\xd6\xb7\xfb\xb4\xae'
>>> s   # linux系统下，s为utf8编码
'python\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2'
>>> su
u'python\u5b57\u7b26\u4e32'
```

使用`s.encode("uft8")`方法将字符串s编码为utf8时，会先调用decode()方法对s进行解码，此时解码使用的编码方法为默认的编码方法（即ascii）。

```python
>>> # 系统默认的编码方法为ascii
>>> import sys
>>> sys.getdefaultencoding()
'ascii'
```

可以使用decode()方法对字符串s进行解码（解码成unicode），之后再用所需的编码方法进行编码。

```python
>>> # windows系统下
>>> s.decode("gb2312")
u'python\u5b57\u7b26\u4e32'
>>> s.decode("gb2312").encode('utf8')
'python\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2'
>>> # linux系统下
>>> s.decode("utf8")
u'python\u5b57\u7b26\u4e32'
>>> s.decode("utf8").encode('gb2312')
'python\xd7\xd6\xb7\xfb\xb4\xae'
```

对于.py文件，在python2中，为了使解释器能够正确读取文件中的中文，需要在文件开头加上编码方式的声明

```python
# -*- coding: utf-8 -*-
```

## 2. python3中的情况

python3中，所有的字符串在内部都用unicode表示。因此，可以直接使用encode()方法将字符串按要求的编码方式进行编码。

```python
>>> s = "python字符串"
>>> s
'python字符串'
>>> s.encode("utf8")
b'python\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2'
```
