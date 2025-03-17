# 通过脚本安装和启用blender插件(add-on)

## >=2.8版本

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

## 2.7 版本

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

