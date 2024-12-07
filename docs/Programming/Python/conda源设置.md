## 命令

添加清华源

```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge 
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/
```

搜索时显示通道地址

```bash
conda config --set show_channel_urls yes
```

注意如果需要pytorch, 还需要添加pytorch的镜像：

```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
```

如果需要换回conda的默认源，直接删除channels即可，命令如下：

```bash
conda config --remove-key channels
```

## .condarc文件

可将以上配置写在`~/.condarc`中

```yaml
channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
ssl_verify: true
show_channel_urls: yes
```

Windows 用户无法直接创建名为 `.condarc` 的文件，可先执行 `conda config --set show_channel_urls yes` 生成该文件之后再修改。

