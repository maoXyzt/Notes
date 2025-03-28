# 在 Cython 中使用 C++

> 作者: tushushu
>
> 项目地址: <https://github.com/tushushu/flying-python>

## 0. 如何安装 Cython

跟大多数的 Python 库不同，Cython 需要一个 C 编译器，在不同的平台上配置方法也不一样。

### 0.1 配置 gcc

- **windows**
  安装 MingW-w64 编译器：`conda install libpython m2w64-toolchain -c msys2`
  在 Python 安装路径下找到\Lib\distutils 文件夹，创建 distutils.cfg 写入如下内容：
  `[build] compiler=mingw32`
- **macOS**
  安装 XCode 即可
- **linux:**
  gcc 一般都是配置好的，如果没有就执行这条命令： `sudo apt-get install build-essential`

### 0.2 安装 cython 库

- pip: `pip install cython`
- conda： `conda install cython`

## 1. 在 Jupyter Notebook 上使用 C++

- 首先加载 Cython 扩展，使用魔术命令 `%load_ext Cython`
- 接下来运行 Cython 代码，使用魔术命令 `%%cython --cplus`
- 如果使用 MacOS，使用魔术命令  `%%cython --cplus --compile-args=-stdlib=libc++ --link-args=-stdlib=libc++`，详情请参考 <https://stackoverflow.com/questions/57367764/cant-import-cpplist-into-cython>

```python
%load_ext Cython
```

```python
%%cython --cplus --compile-args=-stdlib=libc++ --link-args=-stdlib=libc++
# 注意: 使用 'cimport' 而不是 'import'
from libcpp.string cimport string
cdef string s
s = b"Hello world!"
print(s.decode("utf-8"))
```

```text
Hello world!
```

## 2. C++和 Python 类型的相互转换

| Python type| C++ type | Python type |
| ------ | ------ | ------ |
| bytes | std:: string | bytes |
|iterable|std:: vector|list|
|iterable|std:: list|list|
|iterable|std:: set|set|
|iterable (len 2)|std:: pair|tuple (len 2)|

## 3. 使用 C++ STL

### 3.1 使用 C++ Vector

可以替代 Python 的 List。

1. 初始化 - 通过 Python 的可迭代对象进行初始化，需要声明变量的嵌套类型
2. 遍历 - 让 index 自增，通过 while 循环进行遍历
3. 访问 - 和 Python 一样使用'[]'操作符对元素进行访问
4. 追加 - 与 Python list 的 append 方法相似，使用 C++ Vector 的 push_back 方法追加元素

最后，我们通过分别实现 Python 和 C++版本的元素计数函数来对比性能，C++大约快 240 倍左右。
注意: 为了公平起见，函数没有传入参数，而是直接访问函数体外部的变量。避免计入 C++版本把 Python 列表转换为 C++ Vector 的耗时。如果计入这部分耗时，C++的版本大约快 4 倍左右。

```python
%%cython --cplus --compile-args=-stdlib=libc++ --link-args=-stdlib=libc++
from libcpp.vector cimport vector
# 通过Python对象初始化
cdef vector[int] vec = range(5)
# 遍历
cdef:
    int i = 0
    int n = vec.size()
print("开始遍历...")
while i < n:
    # 访问
    print("\t第%d个位置的元素是%d" % (i, vec[i]))
    i += 1
print()
# 追加
vec.push_back(5)
print("追加元素之后vec变为", vec)
```

```text
开始遍历...
    第 0 个位置的元素是 0
    第 1 个位置的元素是 1
    第 2 个位置的元素是 2
    第 3 个位置的元素是 3
    第 4 个位置的元素是 4

追加元素之后 vec 变为 [0, 1, 2, 3, 4, 5]
```

```python
arr = [x // 100 for x in range(1000)]
target = 6

def count_py():
    return sum(1 for x in arr if x == target)

print("用Python来实现，计算结果为%d!"% count_py())
```

```text
用Python来实现，计算结果为100!
```

```python
%%cython --cplus --compile-args=-stdlib=libc++ --link-args=-stdlib=libc++
from libcpp.vector cimport vector

cdef:
    int target = 6
    vector[int] v = [x // 100 for x in range(1000)]

cdef int _count_cpp():
    cdef:
        int i = 0
        int n = v.size()
        int ret = 0
    while i < n:
        if v[i] == target:
            ret += 1
        i += 1
    return ret

def count_cpp():
    return _count_cpp()

print("用Cython(C++)来实现，计算结果为%d!"% count_cpp())
```

```text
用Cython(C++)来实现，计算结果为100!
```

```python
print("对比Python版本与C++版本的性能...")
%timeit count_py()
%timeit count_cpp()
```

```text
对比Python版本与C++版本的性能...
29.9 µs ± 995 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
130 ns ± 2.91 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
```

### 3.2 使用 C++ Unordered Map

可以替代 Python 的 Dict。

1. 初始化 - 通过 Python 的可迭代对象进行初始化，需要声明变量的嵌套类型
2. 遍历 - 让泛型指针自增，通过 while 循环进行遍历
3. 访问 - 使用 deref(C++中的'*'操作符)来解引用，返回 pair 对象，通过.first 来访问 key, .second 来访问 Value
4. 查找 - 使用 unordered_map.count，返回 1 或 0；或者用 unordered_map.find，返回一个泛型指针，如果指针指向 unordered_map.end，则表示未找到。
5. 追加/修改 - unordered_map [key] = value。如果 Key 不存在，'[]'操作符会添加一个 Key，并赋值为默认的 Value，比如 0.0。所以，除非确定不会产生错误，否则在修改 Key 对应的 Value 之前，要先判断 Key 是否存在。这与 Python 的 DecaultDict 有点相似。

最后，我们通过分别实现 Python 和 C++版本的 map 条件求和函数来对比性能，C++大约快 40 倍左右。

```python
%%cython --cplus --compile-args=-stdlib=libc++ --link-args=-stdlib=libc++
from cython.operator cimport dereference as deref, preincrement as inc
from libcpp.unordered_map cimport unordered_map
# 通过 Python 对象初始化
cdef unordered_map[int, float] mymap = {i: i/10 for i in range(10)}
# 遍历
cdef:
    unordered_map[int, float].iterator it = mymap.begin()
    unordered_map[int, float].iterator end = mymap.end()
print("开始遍历...")
while it != end:
    # 访问
    print("\tKey is %d, Value is %.1f" % (deref(it).first, deref(it).second))
    inc(it)
print()

# 查找
print("开始查找...")
if mymap.count(-2):
    print("\t元素-2存在!")
else:
    print("\t元素-2不存在!")

it = mymap.find(3)
if it != end:
    print("\t元素3存在, 它的值是%.1f!" % deref(it).second)
else:
    print("\t元素3不存在!")
print()

# 修改
print("修改元素...")
if mymap.count(3):
    mymap[3] += 1.0
mymap[-2]  # Key -2 不存在，会被添加一个默认值 0.0
print("\tKey is 3, Value is %.1f" % mymap[3])
print("\tKey is -2, Value is %.1f" % mymap[-2])
```

```text
开始遍历...
    Key is 0, Value is 0.0
    Key is 1, Value is 0.1
    Key is 2, Value is 0.2
    Key is 3, Value is 0.3
    Key is 4, Value is 0.4
    Key is 5, Value is 0.5
    Key is 6, Value is 0.6
    Key is 7, Value is 0.7
    Key is 8, Value is 0.8
    Key is 9, Value is 0.9

开始查找...
    元素-2不存在!
    元素3存在, 它的值是0.3!

修改元素...
    Key is 3, Value is 1.3
    Key is -2, Value is 0.0
```

```python
my_map = {x: x for x in range(100)}
target = 50

def sum_lt_py():
    return sum(my_map[x] for x in my_map if x < target)

print("用Python来实现，计算结果为%d!"% sum_lt_py())
```

```text
用Python来实现，计算结果为1225!
```

```python
%%cython --cplus --compile-args=-stdlib=libc++ --link-args=-stdlib=libc++
from libcpp.unordered_map cimport unordered_map
from cython.operator cimport dereference as deref, preincrement as inc

cdef:
    unordered_map[int, int] my_map = {x: x for x in range(100)}
    int target = 50

cdef _sum_lt_cpp():
    cdef:
        unordered_map[int, int].iterator it = my_map.begin()
        int ret
    while it != my_map.end():
        if deref(it).first < target:
            ret += deref(it).second
        inc(it)
    return ret

def sum_lt_cpp():
    return _sum_lt_cpp()

print("用Cython(C++)来实现，计算结果为%d!"% sum_lt_cpp())
```

```text
用Cython(C++)来实现，计算结果为1225!
```

```python
print("对比Python版本与C++版本的性能...")
%timeit sum_lt_py()
%timeit sum_lt_cpp()
```

```text
对比Python版本与C++版本的性能...
6.56 µs ± 117 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
162 ns ± 6.29 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
```

### 3.3 使用 C++ Unordered Set

可以替代 Python 的 Set。

1. 初始化 - 通过 Python 的可迭代对象进行初始化，需要声明变量的嵌套类型
2. 遍历 - 让泛型指针自增，通过 while 循环进行遍历
3. 访问 - 使用 deref(C++中的'*'操作符)来解引用
4. 查找 - 使用 unordered_set.count，返回 1 或 0
5. 追加 - 使用 unordered_set.insert，如果元素已经存在，则元素不会被追加
6. 交集、并集、差集 - 据我所知，unordered_set 的这些操作需要开发者自己去实现，不如 Python 的 Set 用起来方便。

最后，我们通过分别实现 Python 和 C++版本的 set 求交集对比性能，C++大约 **慢** 20 倍左右。详情可参考 <https://stackoverflow.com/questions/54763112/how-to-improve-stdset-intersection-performance-in-c>
如果只是求两个集合相同元素的数量，C++的性能大约是 Python 的 6 倍。不难推测，C++的 unordered set 查询很快，但是创建很慢。

```python
%%cython --cplus --compile-args=-stdlib=libc++ --link-args=-stdlib=libc++
from cython.operator cimport dereference as deref, preincrement as inc
from libcpp.unordered_set cimport unordered_set
# 通过 Python 对象初始化
cdef unordered_set[int] myset = {i for i in range(5)}
# 遍历
cdef:
    unordered_set[int].iterator it = myset.begin()
    unordered_set[int].iterator end = myset.end()
print("开始遍历...")
while it != end:
    # 访问
    print("\tValue is %d" % deref(it))
    inc(it)
print()

# 查找
print("开始查找...")
if myset.count(-2):
    print("\t元素-2存在!")
else:
    print("\t元素-2不存在!")

print()

# 追加
print("追加元素...")
myset.insert(0)
myset.insert(-1)

print("\tMyset is: ", myset)
```

```text
开始遍历...
    Value is 0
    Value is 1
    Value is 2
    Value is 3
    Value is 4

开始查找...
    元素-2不存在!

追加元素...
    Myset is:  {0, 1, 2, 3, 4, -1}
```

```python
myset1 = {x for x in range(100)}
myset2 = {x for x in range(50, 60)}

def intersection_py():
    return myset1 & myset2

print("用Python来实现，计算结果为%s!"% intersection_py())
```

```text
用Python来实现，计算结果为{50, 51, 52, 53, 54, 55, 56, 57, 58, 59}!
```

```python
%%cython --cplus --compile-args=-stdlib=libc++ --link-args=-stdlib=libc++
from cython.operator cimport dereference as deref, preincrement as inc
from libcpp.unordered_set cimport unordered_set

cdef:
    unordered_set[int] myset1 = {x for x in range(100)}
    unordered_set[int] myset2 = {x for x in range(50, 60)}

cdef unordered_set[int] _intersection_cpp():
    cdef:
        unordered_set[int].iterator it = myset1.begin()
        unordered_set[int] ret
    while it != myset1.end():
        if myset2.count(deref(it)):
            ret.insert(deref(it))
        inc(it)
    return ret

def intersection_cpp():
    return _intersection_cpp()

print("用Cython(C++)来实现，计算结果为%s!"% intersection_cpp())
```

```text
用Cython(C++)来实现，计算结果为{50, 51, 52, 53, 54, 55, 56, 57, 58, 59}!
```

```python
print("对比Python版本与C++版本的性能...")
%timeit intersection_py()
%timeit intersection_cpp()
```

```text
对比Python版本与C++版本的性能...
274 ns ± 13.7 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
5.28 µs ± 220 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
```

```python
myset1 = {x for x in range(100)}
myset2 = {x for x in range(50, 60)}

def count_common_py():
    return len(myset1 & myset2)

print("用Python(C++)来实现，计算结果为%s!"% count_common_py())
```

```text
用Python(C++)来实现，计算结果为10!
```

```python
%%cython --cplus --compile-args=-stdlib=libc++ --link-args=-stdlib=libc++
from cython.operator cimport dereference as deref, preincrement as inc
from libcpp.unordered_set cimport unordered_set

cdef:
    unordered_set[int] myset2 = {x for x in range(100)}
    unordered_set[int] myset1 = {x for x in range(50, 60)}

cdef int _count_common_cpp():
    if myset1.size() > myset2.size():
        myset1.swap(myset2)
    cdef:
        unordered_set[int].iterator it = myset1.begin()
        int ret = 0
    while it != myset1.end():
        if myset2.count(deref(it)):
            ret += 1
        inc(it)
    return ret

def count_common_cpp():
    return _count_common_cpp()

print("用Cython(C++)来实现，计算结果为%s!"% count_common_cpp())
```

```text
用Cython(C++)来实现，计算结果为10!
```

```python
print("对比Python版本与C++版本的性能...")
%timeit count_common_py()
%timeit count_common_cpp()
```

```text
对比Python版本与C++版本的性能...
295 ns ± 5.91 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
46.1 ns ± 0.785 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
```

## 4. 传值与传引用

Python 的函数，如果是容器类对象(如 List, Set)，传递的是引用，否则传递的是值(如 int, float)，如果不希望让函数修改容器类对象，可以用 deepcopy 函数先拷贝一份容器的副本。
但在 C++里默认都是传值，如果需要传引用需要声明。
以 int 型 Vector 为例，可以看到 v1 的值没有被 pass_value 修改，但被 pass_reference 修改了。

- 传值使用  ``vector[int]``，pass_value 函数只是传入了 v1 的一份拷贝，所以函数无法修改 v1
- 传引用使用  ``vector[int]&``，pass_reference 传入了 v1 的引用，函数可以修改 v1。

下面的两块代码可以展示 Python 与 C++的不同之处。

```python
from copy import deepcopy

def pass_value(v):
    v = deepcopy(v)
    v[0] = -1

def pass_reference(v):
    v[0] = -1

v1 = [0, 0, 0]
print("v1的初始值是%s" % v1)
pass_value(v1)
print("执行pass_value函数后，v1的值是%s" % v1)
pass_reference(v1)
print("执行pass_reference函数后，v1的值是%s" % v1)
```

```text
v1的初始值是[0, 0, 0]
执行pass_value函数后，v1的值是[0, 0, 0]
执行pass_reference函数后，v1的值是[-1, 0, 0]
```

```python
%%cython --cplus --compile-args=-stdlib=libc++ --link-args=-stdlib=libc++

from libcpp.vector cimport vector

cdef void pass_value(vector[int] v):
    v[0] = -1

cdef void pass_reference(vector[int]& v):
    v[0] = -1

cdef vector[int] v1 = [0, 0, 0]
print("v1的初始值是%s" % v1)
pass_value(v1)
print("执行pass_value函数后，v1的值是%s" % v1)
pass_reference(v1)
print("执行pass_reference函数后，v1的值是%s" % v1)
```

```text
v1的初始值是[0, 0, 0]
执行pass_value函数后，v1的值是[0, 0, 0]
执行pass_reference函数后，v1的值是[-1, 0, 0]
```

## 5. 数字的范围

Python 只有 int 型，而且 int 的范围可以认为是无限大的，只要没有超出内存限制，所以 Python 使用者一般不太关心数值溢出等问题。但使用 C++的时候就需要谨慎，C++各个数字类型对应的范围如下：

|Type |Typical Bit Width |Typical Range|
| ------ | ------ | ------ |
|char |1byte |-127 to 127 or 0 to 255|
|unsigned char |1byte |0 to 255|
|signed char |1byte -127 to 127|
|int |4bytes |-2147483648 to 2147483647|
|unsigned int |4bytes |0 to 4294967295|
|signed int |4bytes |-2147483648 to 2147483647|
|short int |2bytes |-32768 to 32767|
|unsigned short int |2bytes |0 to 65,535|
|signed short int |2bytes |-32768 to 32767|
|long int |4bytes |-2,147,483,648 to 2,147,483,647|
|signed long int |8bytes |same as long int|
|unsigned long int |4bytes |0 to 4,294,967,295|
|long long int |8bytes |-(2^63) to (2^63)-1|
|unsigned long long int |8bytes |0 to 18,446,744,073,709,551,615|
|float |4bytes ||
|double |8bytes ||
|long double |12bytes||
|wchar_t |2 or 4 bytes |1 wide character|

比如下面的函数就会造成错误。

```python
%%cython --cplus --compile-args=-stdlib=libc++ --link-args=-stdlib=libc++
def sum_py(num1, num2):
    print("The result by python is:", num1 + num2)

cdef int _sum_cpp(int num1, int num2):  # int -> long int
    return num1 + num2

def sum_cpp(num1, num2):
    print("The result by cpp is:", _sum_cpp(num1, num2))
```

```python
sum_py(2**31-1, 1)
sum_cpp(2**31-1, 1)
```

```text
The result by python is: 2147483648
The result by cpp is: -2147483648
```

```python
%%cython --cplus --compile-args=-stdlib=libc++ --link-args=-stdlib=libc++
from libcpp cimport bool

def lt_py(num1, num2):
    print("The result by python is:", num1 < num2)

cdef bool _lt_cpp(float num1, float num2):  # float -> double
    return num1 > num2

def lt_cpp(num1, num2):
    print("The result by cpp is:", _lt_cpp(num1, num2))
```

```python
lt_py(1234567890.0, 1234567891.0)
lt_cpp(1234567890.0, 1234567891.0)
```

```text
The result by python is: True
The result by cpp is: False
```
