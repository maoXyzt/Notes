# Tensor 数据操作

> [PyTorch官方文档](https://pytorch.org/tutorials/beginner/blitz/tensor_tutorial.html#sphx-glr-beginner-blitz-tensor-tutorial-py)

## 1. 创建`Tensor`

```python
# 5x3 未初始化的 Tensor
x = torch.empty(5, 3)
# x = torch.empty((5, 3))  # 也可以用这种 size 参数提供方式，下同
# 5x3 随机初始化的 Tensor
x = torch.rand(5, 3)
# 5x3 long型全0的 Tensor
x = torch.zeros(5, 3, dtype=torch.long)
# 根据数据创建
x = torch.tensor([5.5, 3])
# 通过现有 Tensor 创建，会默认重用输入 Tensor 的一些属性
y = x.new_ones(5, 3, dtype=torch.float64)  # 返回一个与size大小相同的用1填充的张量。返回的tensor默认具有相同的torch.dtype和torch.device
y = torch.randn_like(x, dtype=torch.float) # 指定新的数据类型
```

我们可以通过`shape`或者`size()`来获取`Tensor`的形状:

```python
print(x.size())
print(x.shape)
# 输出：
# torch.Size([5, 3])
# 该对象支持所有 tuple 操作
```

常用的创建`Tensor`的方法：

| 函数                              | 功能                           |
| --------------------------------- | ------------------------------ |
| Tensor(*sizes)                    | 基础构造函数                   |
| tensor(data,)                     | 类似 np.array 的构造函数       |
| ones(*sizes)                      | 全 1 Tensor                    |
| zeros(*sizes)                     | 全 0 Tensor                    |
| eye(*sizes)                       | 对角线为 1，其他为 0           |
| arange(s,e,step)                  | 从 s 到 e，步长为 step         |
| linspace(s,e,steps)               | 从 s 到 e，均匀切分成 steps 份 |
| rand/randn(*sizes)                | 均匀/标准分布                  |
| normal(mean,std)/uniform(from,to) | 正态分布/均匀分布              |
| randperm(m)                       | 随机排列                       |

这些创建方法都可以在创建的时候指定数据类型dtype和存放device(cpu/gpu)。

## 2. 操作

### 算术操作

同一种操作可能有很多形式，以加法为例：

```python
# 形式一
x + y

# 形式二
torch.add(x, y)
# 指定输出
result = torch.empty(5, 3)
torch.add(x, y, out=result)

# 形式三, inplace
y.add_(x)
```

**Pytorch 操作的 inplace 版本都有`_`后缀**

### 索引

可以使用类似NumPy的索引操作。**索引出来的结果与原数据共享内存**，也即修改一个，另一个会跟着修改。

```python
y = x[0, :]
```

PyTorch还提供了一些高级的选择函数:

| 函数                            | 功能                                                         |
| ------------------------------- | ------------------------------------------------------------ |
| index_select(input, dim, index) | 在指定维度dim上选取，比如选取某些行、某些列                  |
| masked_select(input, mask)      | 例子如上，a[a>0]，使用 ByteTensor 进行选取                   |
| nonzero(input)                  | 非 0 元素的下标                                              |
| gather(input, dim, index)       | 根据 index，在 dim 维度上选取数据，输出的 size 与 index 一样 |

### 改变形状

- `view()`

```python
y = x.view(15)
z = x.view(-1, 5)  # -1所指的维度可以根据其他维度的值推出来
```

注意：**`view()`返回的新`Tensor`与源`Tensor`虽然可能有不同的`size`，但是是共享`data`的**，也即更改其中的一个，另外一个也会跟着改变。(顾名思义，view仅仅是改变了对这个张量的观察角度，内部数据并未改变)

- `clone().view()`

Pytorch还提供了一个`reshape()`可以改变形状，但是此函数并不能保证返回的是其拷贝，所以不推荐使用。

推荐先用`clone`创造一个副本然后再使用`view`。（参考：[What's the difference between reshape and view in pytorch? - Stack Overflow](https://stackoverflow.com/questions/49643225/whats-the-difference-between-reshape-and-view-in-pytorch)）

```python
x_cp = x.clone().view(15)
```

使用`clone`还有一个好处是会被记录在计算图中，即梯度回传到副本时也会传到源`Tensor`。

- `item()`

它可以将一个标量`Tensor`转换成一个Python number

```python
x = torch.randn(1)
print(x.item())
```

### 线性代数

PyTorch还支持一些线性函数

| 函数                              | 功能                              |
| --------------------------------- | --------------------------------- |
| trace                             | 对角线元素之和(矩阵的迹)          |
| diag                              | 对角线元素                        |
| triu/tril                         | 矩阵的上三角/下三角，可指定偏移量 |
| mm/bmm                            | 矩阵乘法，batch 的矩阵乘法        |
| addmm/addbmm/addmv/addr/baddbmm.. | 矩阵运算                          |
| t                                 | 转置                              |
| dot/cross                         | 内积/外积                         |
| inverse                           | 求逆矩阵                          |
| svd                               | 奇异值分解                        |

PyTorch中的`Tensor`支持超过一百种操作，包括转置、索引、切片、数学运算、线性代数、随机数等等，可参考[官方文档](https://pytorch.org/docs/stable/tensors.html)。

## 3. 广播机制

当对两个形状不同的`Tensor`按元素运算时，可能会触发广播（broadcasting）机制：先适当复制元素使这两个`Tensor`形状相同后再按元素运算。

```python
x = torch.arange(1, 3).view(1, 2)
print(x)
y = torch.arange(1, 4).view(3, 1)
print(y)
print(x + y)
# 输出
# tensor([[1, 2]])
# tensor([[1],
#         [2],
#         [3]])
# tensor([[2, 3],
#         [3, 4],
#         [4, 5]])
```

## 4. 运算的内存开销

索引操作是不会开辟新内存的，而像`y = x + y`这样的运算是会新开内存的，然后将`y`指向新内存。

如果想指定结果到原来的`y`的内存，我们可以使用前面介绍的索引来进行替换操作。

```python
y[:] = y + x
```

我们还可以使用运算符全名函数中的`out`参数或者自加运算符`+=`(也即`add_()`)达到上述效果：

```python
torch.add(x, y, out=y)
y += x
y.add_(x)
```

## 5. `Tensor`和 Numpy 数组相互转换

`numpy()`和`from_numpy()`产生的`Tensor`与NumPy中的数组共享相同的内存（所以他们之间的转换很快），改变其中一个时另一个也会改变。

而用`torch.tensor()`将 Numpy 中的 array 转成`Tensor`时，总是会进行数据拷贝。

### `Tensor`转 NumPy 数组

```python
a = torch.ones(5)
b = a.numpy()
```

### NumPy 数组转`Tensor`

```python
a = np.ones(5)
# 不进行数据拷贝
b = torch.from_numpy(a)
# 总是进行数据拷贝
c = torch.tensor(a)
```

所有在CPU上的`Tensor`（除了`CharTensor`）都支持与 NumPy 数组相互转换。

## 6. `Tensor` on GPU

用方法`to()`可以将`Tensor`在CPU和GPU（需要硬件支持）之间相互移动。

```python
# 以下代码只有在PyTorch GPU版本上才会执行
if torch.cuda.is_available():
    device = torch.device("cuda")          # GPU
    y = torch.ones_like(x, device=device)  # 直接创建一个在GPU上的Tensor
    x = x.to(device)                       # 等价于 .to("cuda")
    z = x + y
    print(z)
    print(z.to("cpu", torch.double))       # to()还可以同时更改数据类型
```
