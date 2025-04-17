# torch.jit.script 与 torch.jit.trace

torch.jit.script 和 torch.jit.trace 是 PyTorch 中用于将模型转换为脚本或跟踪模型执行的工具。

## 1 - TorchScript

TorchScript 是 PyTorch 的一个重要特性，它允许您将 PyTorch 模型 (`torch.nn.Module` 的子类) 转换为一种中间表示形式，可以在高性能环境 (例如 C++) 中运行。

> [TorchScript -- PyTorch 2.6 documentation](https://pytorch.org/docs/stable/jit.html)
> [TorchScript 简介](https://pytorch.panchuang.net/EigthSection/torchScript/)

使用 TorchScript 的好处包括：

1. TorchScript 代码可以在其自己的解释器中调用，该解释器基本上是一个受限制的 Python 解释器。该解释器不被全局解释器锁定，因此可以在同 一实例上同时处理许多请求。
2. 这种格式使我们可以将整个模型保存到磁盘上，并将其加载到另一个环境中，例如在以 Python 以外的语言编写的服务器中
3. TorchScript 为我们提供了一种表示形式，其中我们可以对代码进行编译器优化以提供更有效的执行
4. TorchScript 允许我们与许多后端/设备运行时进行接口，这些运行时比单个操作员需要更广泛的程序视图。

## 2 - torch.jit.trace

`torch.jit.trace` 通过跟踪 (Tracing) 模型/函数的执行来创建 TorchScript。

它适用于那些 **具有固定输入形状** 的模型/函数。

### 2.1 Tracing 函数

传入一个函数和示例输入，返回一个 `torch.jit.ScriptFunction` 对象:

```python
def foo(x, y):
    return 2 * x + y

traced_foo = torch.jit.trace(foo, (torch.rand(3), torch.rand(3)))
print(traced_foo)
traced_foo(torch.Tensor([1, 2, 3]), torch.Tensor([4, 5, 6]))
### Output:
# <torch.jit.ScriptFunction object at 0x7febd01a9070>
```

### 2.2 Tracing 模型

传入一个 PyTorch 模型和示例输入，返回一个 `torch.jit.ScriptModule` 对象:

```python
class MyCell(torch.nn.Module):
    def __init__(self):
        super(MyCell, self).__init__()
        self.linear = torch.nn.Linear(4, 4)

    def forward(self, x, h):
        new_h = torch.tanh(self.linear(x) + h)
        return new_h, new_h

my_cell = MyCell()
x, h = torch.rand(3, 4), torch.rand(3, 4)
traced_cell = torch.jit.trace(my_cell, (x, h))
print(traced_cell)
traced_cell(x, h)
### Output:
# MyCell(
#   original_name=MyCell
#   (linear): Linear(original_name=Linear)
# )
###
```

### 2.3 运行原理

`torch.jit.trace` 函数做的事情是：调用模块，记录了模块运行时发生的操作，并创建了`torch.jit.ScriptFunction` 的实例或 `torch.jit.ScriptModule` 的实例 (`TracedModule` 是其实例)。

TorchScript 将其定义记录在中间表示（或 IR）中，在深度学习中通常称为图形。

我们可以检查图的 `.graph` 属性 (低级的表示) 或 `.code` 属性：

```python
print(traced_cell.graph)
### Output:
# graph(%self : ClassType <MyCell>,
#       %input : Float(3, 4),
#       %h : Float(3, 4)):
#   %1 : ClassType <Linear> = prim:: GetAttr [name = "linear"](%self)
#   %weight : Tensor = prim:: GetAttr [name = "weight"](%1)
#   %bias : Tensor = prim:: GetAttr [name = "bias"](%1)
#   %6 : Float(4, 4) = aten:: t(%weight), scope: MyCell/Linear [linear] # /opt/conda/lib/python3.6/site-packages/torch/nn/functional.py: 1370:0
#   %7 : int = prim:: Constant [value = 1](), scope: MyCell/Linear [linear] # /opt/conda/lib/python3.6/site-packages/torch/nn/functional.py: 1370:0
#   %8 : int = prim:: Constant [value = 1](), scope: MyCell/Linear [linear] # /opt/conda/lib/python3.6/site-packages/torch/nn/functional.py: 1370:0
#   %9 : Float(3, 4) = aten:: addmm(%bias, %input, %6, %7, %8), scope: MyCell/Linear [linear] # /opt/conda/lib/python3.6/site-packages/torch/nn/functional.py: 1370:0
#   %10 : int = prim:: Constant [value = 1](), scope: MyCell # /var/lib/jenkins/workspace/beginner_source/Intro_to_TorchScript_tutorial.py: 188:0
#   %11 : Float(3, 4) = aten:: add(%9, %h, %10), scope: MyCell # /var/lib/jenkins/workspace/beginner_source/Intro_to_TorchScript_tutorial.py: 188:0
#   %12 : Float(3, 4) = aten:: tanh(%11), scope: MyCell # /var/lib/jenkins/workspace/beginner_source/Intro_to_TorchScript_tutorial.py: 188:0
#   %13 : (Float(3, 4), Float(3, 4)) = prim:: TupleConstruct(%12, %12)
#   return (%13)
###
print(traced_cell.code)
### Output:
# import __torch__
# import __torch__.torch.nn.modules.linear
# def forward(self,
#     input: Tensor,
#     h: Tensor) -> Tuple [Tensor, Tensor]:
#   _0 = self.linear
#   weight = _0.weight
#   bias = _0.bias
#   _1 = torch.addmm(bias, input, torch.t(weight), beta = 1, alpha = 1)
#   _2 = torch.tanh(torch.add(_1, h, alpha = 1))
#   return (_2, _2)
###
```

## 3 - torch.jit.script

`torch.jit.trace` 运行代码，记录发生的操作，并构造一个可以做到这一点的 `ScriptModule`。但诸如控制流之类的东西被抹去了。

如果模型/函数具有动态输入形状或使用了 Python 控制流（例如 if 语句、循环等），则应使用 `torch.jit.script`。

`torch.jit.script` 通过分析模型/函数的 Python 代码来创建 TorchScript。

> [使用脚本转换模块](https://pytorch.panchuang.net/EigthSection/torchScript/#3)

### 3.1 Scripting 函数

传入一个函数，返回一个 `torch.jit.ScriptFunction` 对象:

```python
@torch.jit.script
def foo(len):
    # type: (int) -> torch.Tensor
    rv = torch.zeros(3, 4)
    for i in range(len):
        if i < 10:
            rv = rv - 1.0
        else:
            rv = rv + 1.0
    return rv
```

### 3.2 Scripting 模型

传入一个模型，返回一个 `torch.jit.ScriptModule` 对象:

```python
import torch

# 定义模型
class MyModel(torch.nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.conv = torch.nn.Conv2d(3, 64, kernel_size=3, padding=1)
        self.fc = torch.nn.Linear(64 * 8 * 8, 10)

    def forward(self, x):
        x = self.conv(x)
        x = torch.nn.functional.relu(x)
        x = x.view(-1, 64 * 8 * 8)
        x = self.fc(x)
        return x


model = MyModel()

# 将模型转换为 Torch 脚本模块
scripted_model = torch.jit.script(model)

# 调用
output = scripted_model(torch.randn(1, 3, 32, 32))
print(output)


# 保存模型
torch.jit.save(scripted_model, './model/Test/scripted_model.pth')
```

## 4 - 混合使用

在某些情况下，需要使用 tracing 而不是 scripting (例如，模块具有许多架构决策，这些决策是基于我们希望不会出现在TorchScript中的恒定Python 值做出的)。

在这种情况下，可以基于 trace 来编写 script: `torch.jit.script` 将内联被跟踪模块的代码，而 `torch.jit.trace` 将内联脚本模块的代码。

> [Mixing tracing and scripting](https://pytorch.org/docs/stable/jit.html#mixing-tracing-and-scripting)

Example (calling a traced function in script):

```python
def foo(x, y):
    return 2 * x + y

traced_foo = torch.jit.trace(foo, (torch.rand(3), torch.rand(3)))

@torch.jit.script
def bar(x):
    return traced_foo(x, x)
```

Example (calling a script function in a traced function):

```python
@torch.jit.script
def foo(x, y):
    if x.max() > y.max():
        r = x
    else:
        r = y
    return r


def bar(x, y, z):
    return foo(x, y) + z

traced_bar = torch.jit.trace(bar, (torch.rand(3), torch.rand(3), torch.rand(3)))
```

Example (using a traced module):

```python
class MyScriptModule(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.means = torch.nn.Parameter(torch.tensor([103.939, 116.779, 123.68])
                                        .resize_(1, 3, 1, 1))
        self.resnet = torch.jit.trace(torchvision.models.resnet18(),
                                      torch.rand(1, 3, 224, 224))

    def forward(self, input):
        return self.resnet(input - self.means)

my_script_module = torch.jit.script(MyScriptModule())
```

## 5 - 保存和加载

TorchScript 模块可以使用 `torch.jit.save` 和 `torch.jit.load` 函数保存和加载。

```python
# 保存
torch.jit.save(scripted_model, 'scripted_model.pt')
# 加载
loaded_model = torch.jit.load('scripted_model.pt')
loaded_model(torch.randn(1, 3, 32, 32))
```
