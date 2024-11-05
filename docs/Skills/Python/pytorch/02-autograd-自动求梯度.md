# 自动求梯度

> [autograd官方文档](https://pytorch.org/docs/stable/autograd.html)

在深度学习中，我们经常需要对函数求梯度（gradient）。PyTorch 提供的 autograd 包能够根据输入和前向传播过程自动构建计算图，并执行反向传播。

## 1. 概念

如果将`Tensor`类的属性`.requires_grad`设置为`True`，它将开始追踪（track）在其上的所有操作（这样就可以利用链式法则进行梯度传播了）。完成计算后，可以调用`.backward()`来完成所有梯度计算。此`Tensor`的梯度将累积到`.grad`属性中。

如果不想要被继续追踪，可以调用`.detach()`将其从追踪记录中分离出来，这样就可以防止将来的计算被追踪，这样梯度就传不过去了。

此外，还可以用`with torch.no_grad()`将不想被追踪的操作代码块包裹起来，这种方法在评估模型的时候很常用，因为在评估模型时，我们并不需要计算可训练参数（`requires_grad=True`）的梯度。

`Function`是另外一个很重要的类。`Tensor`和`Function`互相结合就可以构建一个记录有整个计算过程的有向无环图（DAG）。每个`Tensor`都有一个`.grad_fn`属性，该属性即创建该`Tensor`的`Function`, 就是说该`Tensor`是不是通过某些运算得到的，若是，则`grad_fn`返回一个与这些运算相关的对象，否则是None。

## 2. `Tensor`

创建一个`Tensor`并设置`requires_grad=True`:

```python
x = torch.ones(2, 2, requires_grad=True)
print(x)
print(x.grad_fn)
# 输出：
# tensor([[1., 1.],
#         [1., 1.]], requires_grad=True)
# None
```

再做一下运算操作：

```python
y = x + 2
print(y)
print(y.grad_fn)
# 输出：
# tensor([[3., 3.],
#         [3., 3.]], grad_fn=<AddBackward>)
# <AddBackward object at 0x1100477b8>
```

注意x是直接创建的，所以它没有`grad_fn`, 而y是通过一个加法操作创建的，所以它有一个为`<AddBackward>`的`grad_fn`。

像x这种直接创建的称为叶子节点，叶子节点对应的`grad_fn`是`None`。

```python
print(x.is_leaf, y.is_leaf)
# 输出：
# True False
```

通过`.requires_grad_()`来用 in-place 的方式改变`requires_grad`属性：

```python
a = torch.randn(2, 2)  # 默认 requires_grad = False
a = ((a * 3) / (a - 1))
print(a.requires_grad)
a.requires_grad_(True)
print(a.requires_grad)
b = (a * a).sum()
print(b.grad_fn)
# 输出：
# False
# True
# <SumBackward0 object at 0x118f50cc0>
```

## 3. 梯度

```python
x = torch.ones(2, 2, requires_grad=True)
y = x + 2
z = y * y * 3
out = z.mean()
```

因为`out`是一个标量，所以调用`backward()`时不需要指定求导变量：

```python
out.backward() # 等价于 out.backward(torch.tensor(1.))
```

`out`关于`x`的梯度
$$
\frac{d(out)}{dx}
$$

```python
print(x.grad)
# 输出：
# tensor([[4.5000, 4.5000],
#         [4.5000, 4.5000]])
```

验证：因为
$$
out = \frac{1}{4}\sum^4_{i=1} z_i = \frac{1}{4}\sum^4_{i=1} 3(x_i+2)^2
$$
所以
$$
\frac{\partial out}{\partial x_i} | _{x_i=1} = \frac{9}{2} = 4.5
$$
上面的输出正确。

数学上，如果有一个函数值和自变量都为向量的函数那么 y 关于 x 的梯度就是一个雅可比矩阵（Jacobian matrix），而`torch.autograd`这个包就是用来计算一些雅克比矩阵的乘积的。

注意：grad在反向传播过程中是累加的(accumulated)，这意味着每一次运行反向传播，梯度都会累加之前的梯度，所以一般在反向传播之前需把梯度清零。

```python
# 再来反向传播一次，注意grad是累加的
out2 = x.sum()
out2.backward()
print(x.grad)

out3 = x.sum()
x.grad.data.zero_()
out3.backward()
print(x.grad)
# 输出
# tensor([[5.5000, 5.5000],
#         [5.5000, 5.5000]])
# tensor([[1., 1.],
#         [1., 1.]])
```

为什么在`y.backward()`时，如果`y`是标量，则不需要为`backward()`传入任何参数；否则，需要传入一个与`y`同形的`Tensor`？简单来说就是为了避免向量（甚至更高维张量）对张量求导，而转换成标量对张量求导。**不允许张量对张量求导，只允许标量对张量求导，求导结果是和自变量同形的张量**。所以必要时我们要把张量通过将所有张量的元素加权求和的方式转换为标量。

> [PyTorch 的 backward 为什么有一个 grad_variables 参数？ - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/29923090)

---

来看一些实际例子。

```python
x = torch.tensor([1.0, 2.0, 3.0, 4.0], requires_grad=True)
y = 2 * x
z = y.view(2, 2)
```

现在 `z` 不是一个标量，所以在调用`backward`时需要传入一个和`z`同形的权重向量进行加权求和得到一个标量。

```python
v = torch.tensor([[1.0, 0.1], [0.01, 0.001]], dtype=torch.float)
z.backward(v)
print(x.grad)
# 输出：
# tensor([2.0000, 0.2000, 0.0200, 0.0020])
```

注意，`x.grad`是和`x`同形的张量。

---

再来看看中断梯度追踪的例子：

```python
x = torch.tensor(1.0, requires_grad=True)
y1 = x ** 2
with torch.no_grad():
    y2 = x ** 3
y3 = y1 + y2

print(x.requires_grad)
print(y1, y1.requires_grad) # True
print(y2, y2.requires_grad) # False
print(y3, y3.requires_grad) # True
# 输出：
# True
# tensor(1., grad_fn=<PowBackward0>) True
# tensor(1.) False
# tensor(2., grad_fn=<ThAddBackward>) True
```

可以看到，上面的`y2`是没有`grad_fn`而且`y2.requires_grad=False`的，而`y3`是有`grad_fn`的。如果我们将`y3`对`x`求梯度的话会是多少呢？

```python
y3.backward()
print(x.grad)
# 输出：
tensor(2.)
```

由于 y^2 的定义是被`torch.no_grad():`包裹的，所以与 y^2 有关的梯度是不会回传的，只有与 y^1 有关的梯度才会回传，即 x^2 对 x 的梯度。

---

此外，如果我们想要修改`tensor`的数值，但是又不希望被`autograd`记录（即不会影响反向传播），那么我么可以对`tensor.data`进行操作。

```python
x = torch.ones(1,requires_grad=True)

print(x.data) # 还是一个tensor
print(x.data.requires_grad) # 但是已经是独立于计算图之外

y = 2 * x
x.data *= 100 # 只改变了值，不会记录在计算图，所以不会影响梯度传播

y.backward()
print(x) # 更改data的值也会影响tensor的值
print(x.grad)

# 输出：
# tensor([1.])
# False
# tensor([100.], requires_grad=True)
# tensor([2.])
```
