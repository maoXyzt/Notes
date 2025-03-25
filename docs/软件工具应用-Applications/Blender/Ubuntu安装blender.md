# Ubuntu 安装blender

## snap安装

```bash
sudo snap install blender --channel=2.83lts/stable --classic
```

## 添加 apt 源安装

```bash
# 添加源
sudo add-apt-repository ppa:thomas-schiex/blender

# 安装
sudo apt-get update
sudo apt-get install blender

# 卸载
sudo apt install ppa-purge
sudo ppa-purge ppa:thomas-schiex/blender
```

## 编译安装

> [Building Blender/Linux/Ubuntu - Blender Developer Wiki](https://wiki.blender.org/wiki/Building_Blender/Linux/Ubuntu)

### Install Packages

```bash
sudo apt-get update
sudo apt-get install build-essential git subversion cmake libx11-dev libxxf86vm-dev libxcursor-dev libxi-dev libxrandr-dev libxinerama-dev libglew-dev
```

### Download Sources

```bash
mkdir ~/blender-git
cd ~/blender-git
git clone https://git.blender.org/blender.git
# 选择一个版本
# cd blender
# git checkout blender-v2.83-release
```

### Download Libraries

下载预编译的依赖库：

These libraries are built on CentOS 7 for [VFX reference platform](https://vfxplatform.com/) compatibility, but they work fine on other Linux distributions.

```
mkdir ~/blender-git/lib
cd ~/blender-git/lib
svn checkout https://svn.blender.org/svnroot/bf-blender/trunk/lib/linux_centos7_x86_64
```

（[Advanced Setup](https://wiki.blender.org/wiki/Building_Blender/Linux/Ubuntu#Automatic_Dependency_Installation)）自行编译依赖：

适用于 Debian (and derivatives), Ubuntu, Fedora, Suse and Arch distributions：

```bash
cd ~/blender-git
./blender/build_files/build_environment/install_deps.sh
```

**Important** It might be required to re-run install-depsh.sh once in a while, as Blender updates its dependencies.

### Update and Build

Get latest source code and add-ons, and build. These commands can be used for the first build, and repeated whenever you want to update to the latest version.

```
cd ~/blender-git/blender
make update
make
```

After the build finished, you will find blender ready to run in `~/blender-git/build_linux/bin`.

If building fails after an update, it sometimes helps to remove the `~/blender-git/build_linux` folder to get a completely clean build.

**启用CUDA**

需要安装`nvidia-cuda-dev`

```bash
sudo apt install nvidia-cuda-dev
```

修改`CMakeLists.txt`，设置`WITH_CYCLES_CUDA_BINARIES=ON`

**指定编译过程中的gcc**

```bash
CC=gcc-9 CPP=g++-9 CXX=g++-9 LD=g++-9
```
