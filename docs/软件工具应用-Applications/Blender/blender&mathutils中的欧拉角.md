# Blender 和 mathutils 中的欧拉角

Blender 中默认的欧拉角顺序是 "XYZ" 外旋，等价于 "ZYX" 内旋。

Maya 中默认的欧拉角顺序也是 "XYZ" 外旋，等价于 "ZYX" 内旋。

`mathutils.Euler` 中默认的欧拉角顺序是 "XYZ" 外旋，等价于 "ZYX" 内旋 (只能传入外旋顺序)。

```python
import mathutils
eul = mathutils.Euler()
print(eul.order)
# "XYZ"
```

`scipy.spatial.transform.Rotation` 无默认欧拉角顺序，外旋使用小写字母 `{'x', 'y', 'z'}`，内旋使用大写字母 `{'X', 'Y', 'Z'}`。

```bash
r = R.from_euler('x', 90, degrees=True)
print("Outer R:", r.as_euler('xyz', degrees=True))
print("Inner R:", r.as_euler('XYZ', degrees=True))
```
