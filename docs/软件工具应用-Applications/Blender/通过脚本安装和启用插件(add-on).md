# 通过脚本安装和启用 blender 插件(add-on)

## 1 - `>=2.8` 版本

```python
import bpy

# 安装
bpy.ops.preferences.addon_install(filepath='path/to/add-on.zip')
bpy.ops.preferences.addon_enable(module='name-of-add-on')
bpy.ops.wm.save_userpref()

# 移除
bpy.ops.preferences.addon_disable(module='name-of-add-on')
bpy.ops.preferences.addon_remove(module='name-of-add-on')
bpy.ops.wm.save_userpref()
```

## 2 - `<2.8` 版本

```python
import bpy

# 安装
bpy.ops.wm.addon_install(filepath='path/to/add-on.zip')
bpy.ops.wm.addon_enable(module='name-of-add-on')
bpy.ops.wm.save_userpref()

# 移除
bpy.ops.wm.addon_disable(module='name-of-add-on')
bpy.ops.wm.addon_remove(module='name-of-add-on')
bpy.ops.wm.save_userpref()
```
