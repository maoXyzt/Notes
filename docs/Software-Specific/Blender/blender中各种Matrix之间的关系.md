# Blender中各种Matrix之间的关系

## 0. bpy_types

- `bpy_types.Object`

```python
>>> type(bpy.data.objects['Armature'])
<class 'bpy_types.Object'>
```

- `bpy.types.Armature`

```python
>>> type(bpy.data.armatures['Armature'])
<class 'bpy.types.Armature'>
>>> type(bpy.data.objects['Armature'].data)
<class 'bpy.types.Armature'>
```

- `bpy.types.Pose` <- `bpy.types.Object`.pose

```python
>>> type(bpy.data.objects['Armature'].pose)
<class 'bpy.types.Pose'>
```

- `bpy_types.PoseBone` <- `bpy.types.Pose`.bones[0]

```python
>>> type(bpy.data.objects['Armature'].pose.bones[0])
<class 'bpy_types.PoseBone'>
```

- `bpy_types.Bone` <- `bpy.types.Armature`.bones[0]
- `bpy_types.Bone` <- `bpy.types.PoseBone`.bone

```python
>>> type(bpy.data.armatures['Armature'].bones[0])
<class 'bpy_types.Bone'>
>>> type(bpy.data.objects['Armature'].data.bones[0])
<class 'bpy_types.Bone'>
>>> type(bpy.data.objects['Armature'].pose.bones[0].bone)
<class 'bpy_types.Bone'>
```


## 1. Matrix

> [How can I manually calculate bpy.types.PoseBone.matrix using Blender's Python API? - Blender Stack Exchange](https://blender.stackexchange.com/questions/44637/how-can-i-manually-calculate-bpy-types-posebone-matrix-using-blenders-python-ap)

> [scripting - bpy.types.Bone.matrix vs matrix_local - Blender Stack Exchange](https://blender.stackexchange.com/questions/229927/bpy-types-bone-matrix-vs-matrix-local)

> [Blender Manual - Space types](https://docs.blender.org/manual/en/latest/animation/constraints/interface/common.html#space-types)

均为4×4矩阵。

- `Bone.matrix_local`：bone在**ARMATURE SPACE**中的无pose矩阵；等价于**在Rest Position状态下**的 `PoseBone.matrix`。

```python
>>> bpy.data.objects['Armature'].data.bones["Bone"].matrix_local \
... == bpy.data.objects['Armature'].pose.bones["Bone"].matrix
True
```

- `Bone.matrix`: 在Rest Position下，从bone的**BONE SPACE**变换到父骨骼的**BONE SPACE**的变换矩阵(3x3)，但不包含translation。

  矩阵的各个列分别等于 `Bone.x_axis`, `Bone.y_axis`, `Bone.z_axis`，表示骨骼的 x/y/z 轴在父骨骼的BONE SPACE中的位置。

```python
>>> bone = bpy.data.objects['Armature'].data.bones["Bone"]
>>> bone.matrix \
... == (bone.parent.matrix_local.inverted() @ bone.matrix_local).to_3x3()
True
```

- `PoseBone.matrix_basis`：bone在**BONE SPACE**中的局部变换矩阵，不受父骨骼影响。

```python
>>> bpy.data.objects['Armature'].pose.bones["Bone"].matrix_basis.translation \
... == bpy.data.objects['Armature'].pose.bones["Bone"].matrix_basis.to_translation() \
... == bpy.data.objects['Armature'].pose.bones["Bone"].location
True

>>> bpy.data.objects['Armature'].pose.bones["Bone"].matrix_basis.to_quaternion() \
... == bpy.data.objects['Armature'].pose.bones["Bone"].rotation_quaternion
True

>>> bpy.data.objects['Armature'].pose.bones["Bone"].matrix_basis.to_scale() \
... == bpy.data.objects['Armature'].pose.bones["Bone"].scale
True
```

- `PoseBone.matrix`：bone在**ARMATURE SPACE**中的pose矩阵。

  子骨骼的matrix_basis在与父骨骼的matrix复合可得到子骨骼在在**POSE SPACE** (ARMATURE SPACE带上pose参数) 中的变换矩阵。

```python
>>> posebone = bpy.data.objects['Armature'].pose.bones["Bone"]
>>> posebone.parent.matrix @ posebone.matrix_basis \
... == posebone.matrix
# bone无parent时
>>> posebone.bone.matrix_local @ posebone.matrix_basis \
... == posebone.matrix
```

- `PoseBone.matrix_channel`: （只读）在**ARMATURE SPACE**中，使bone从**REST POSE**状态直接变换到**POSE SPACE**的矩阵

```python
>>> posebone = bpy.data.objects['Armature'].pose.bones["Bone"]
>>> posebone.matrix_channel @ posebone.bone.matrix_local == posebone.matrix
```

- `Object.matrix_world`：object在**WORLD SPACE**中的变换矩阵。

### 矩阵间的变换关系

```python
def matrix_armature(armature_ob, bone_name):
    local = armature_ob.data.bones[bone_name].matrix_local
    basis = armature_ob.pose.bones[bone_name].matrix_basis

    parent = armature_ob.pose.bones[bone_name].parent
    if parent is None:
        return local @ basis
    else:
        parent_local = armature_ob.data.bones[parent.name].matrix_local
        return matrix_armature(armature_ob, parent.name) @ (parent_local.inverted() @ local) @ basis
```

思路：从 BONE SPACE 逐级变换到父骨骼的 BONE SPACE，最终到达根骨骼的 BONE SPACE 即为 ARMATURE SPACE。

- basis：当前骨骼在自己的bone space中的变换矩阵。
- local @ basis：当所有祖先骨骼都在rest position状态下时，当前骨骼在armature space中的变换矩阵。
- (parent_local.inverted() @ local) W basis：父骨骼在rest position状态下时，当前骨骼在父骨骼的bone space中的变换矩阵。
- parent_basis @ (parent_local.inverted() @ local) @ basis：当前骨骼在父骨骼的bone space中的变换矩阵。
- parent_local @ parent_basis @ (parent_local.inverted() @ local) @ basis：考虑了父骨骼的pose后，父骨骼以上骨骼都在rest position状态下时，在当前骨骼在armature space中的变换矩阵。

只考虑旋转的话，可以用另一种变换方式：利用`Bone.matrix`和`PoseBone.matrix_basis`

```python
def rotation_armature(armature_ob, bone_name):
    bone_mat = armature_ob.data.bones[bone_name].matrix
    rot_mat = armature_ob.pose.bones[bone_name].rotation_quaternion.to_matrix()

    parent = armature_ob.pose.bones[bone_name].parent
    if parent is None:
        return bone_mat @ rot_mat
    else:
        return rotation_armature(armature_ob, parent.name) @ bone_mat @ rot_mat
```
