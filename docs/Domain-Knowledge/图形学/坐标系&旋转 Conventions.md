# 常用软件的坐标系和旋转 Conventions

## 1. Maya

### 1.1 世界坐标系

$$
\begin{aligned}
 &y \\
 &\uparrow \\
 &\odot \longrightarrow x \\
z \swarrow\ & \\
\end{aligned}
$$

### 1.2 旋转

欧拉角顺序：外旋XYZ

$$
R = R_z \cdot R_y \cdot R_x
$$

|       |     |
| ----- | --- |
| Yaw   | Y   |
| Pitch | X   |
| Roll  | Z   |

## 2. Blender

### 2.1 世界坐标系

$$
\begin{aligned}
&z \\
&\uparrow \nearrow\ y \\
&\otimes \longrightarrow x \\
\end{aligned}
$$

### 2.2 相机坐标系

跟maya世界坐标系相同：

$$
\begin{aligned}
 &y \\
 &\uparrow \\
 &\odot \longrightarrow x \\
z \swarrow\ & \\
\end{aligned}
$$

### 2.3 旋转

欧拉角顺序：默认为外旋XYZ

$$
R = R_z \cdot R_y \cdot R_x
$$

动画pose中的旋转默认为四元数

## 3. UE

**左手系**

### 3.1 世界坐标系

$$
\begin{aligned}
 &z \\
 &\uparrow \\
 &\odot \longrightarrow x \\
y \swarrow\ & \\
\end{aligned}
$$

### 3.2 相机坐标系

$$
\begin{aligned}
&z \\
&\uparrow \nearrow\ x \\
&\otimes \longrightarrow y \\
\end{aligned}
$$

### 3.3 旋转

欧拉角顺序：外旋XYZ

$$
R = R_z \cdot R_y \cdot R_x
$$

|       |     |
| ----- | --- |
| Yaw   | Z   |
| Pitch | Y   |
| Roll  | X   |

***!!! 注意***

- **z轴**用**左手**螺旋确定欧拉角正方向（**与右手系的方向相反**）
- **x、y轴**用**右手**螺旋确定欧拉角正方向

也可等价为欧拉角时使用如下坐标系：

*（左手系）*
$$
\begin{aligned}
 &z\\
 &\uparrow \nearrow y\\
x \longleftarrow &\otimes \\
\end{aligned}
$$

*（右手系）*
$$
\begin{aligned}
 &\odot \longrightarrow x \\
y \swarrow\ &\downarrow \\
   &z \\

\end{aligned}
$$

## 4. MeshLab

### 4.1 世界坐标系

$$
\begin{aligned}
 &y \\
 &\uparrow \\
 &\odot \longrightarrow x \\
z \swarrow\ & \\
\end{aligned}
$$

同Maya

## 5. SMPL(X)

### 5.1 世界坐标系

坐标系原点在胸腔内部，使得模型各顶点 `(x-mean, y-mean, z-mean) = (0,0,0)`

$$
\begin{aligned}
 &y \\
 &\uparrow \\
 &\odot \longrightarrow x \\
z \swarrow\ & \\
\end{aligned}
$$
同Maya

### 5.2 旋转

同Maya

## 6. Pytorch3D

### 6.1 世界坐标系

$$
\begin{aligned}
&y \\
&\uparrow \nearrow\ z\\
x \longleftarrow &\otimes \\
\end{aligned}
$$

### 6.2 旋转

矩阵或四元数表示

## 7. OpenCV (pyrenderer)

### 7.1 相机坐标系

以相机位置为原点，+z为远离相机方向

$$
\begin{aligned}
 &\ \ \nearrow z \\
 &\otimes \longrightarrow x \\
 &\downarrow \\
 &y
\end{aligned}
$$

### 7.2 旋转

矩阵形式

## 8. OpenGL

### 8.1 世界坐标系

$$
\begin{aligned}
 &y \\
 &\uparrow \\
 &\odot \longrightarrow x \\
z \swarrow\ & \\
\end{aligned}
$$

同Maya

### 8.2 旋转

欧拉角顺序：内旋YZX

$$
R = R_y \cdot R_z \cdot R_x
$$

|       |     |
| ----- | --- |
| Yaw   | Y   |
| Pitch | X   |
| Roll  | Z   |
