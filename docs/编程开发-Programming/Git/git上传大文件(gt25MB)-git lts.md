# Git 上传大文件 (> 25MB): Git LFS

GitHub 对单个文件大小限制为 100MB，超过 100MB 的文件无法上传。对于大于 25MB 的文件，GitHub 会提示你使用 Git LFS（Large File Storage）来管理。

Git Large File Storage (LFS) 是一个 Git 扩展，用于管理大文件和二进制文件。它将大文件存储在 GitHub 的服务器上，而不是在 Git 仓库中，从而减小了仓库的大小。

> Git LFS 官方网站：<https://git-lfs.com>

## 1 - 安装 Git LFS

> GitHub 的 Git LFS 安装指南: <https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage>

在安装 Git 之后，可以在 [官方网站](https://git-lfs.com) 上下载 Git LFS 的安装程序。

> 在 MacOS 平台上，也可以使用 Homebrew 安装 Git LFS：
>
> ```bash
> brew install git-lfs
> ```

> 在 Linux 平台上，也可以参考该链接，用包管理器安装 (支持 apt/deb 和 rpm/yum)：
>
> <https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage>

## 2 - 使用方法

### 2.1 初始化 Git LFS

首先用你的账号初始化 Git LFS (每个账号在一台机器上只需要执行一次)：

```bash
git lfs install
```

### 2.2 添加文件到 Git LFS

在你的 Git 仓库中，使用以下命令将指定类型的文件添加到 Git LFS：

```bash
git lfs track "*.psd"   # 将所有 .psd 文件添加到 Git LFS
```

或者，可以在 `.gitattributes` 文件中手动添加：

```bash
*.psd filter=lfs diff=lfs merge=lfs -text
```

### 2.3 仓库已有文件转移到 Git LFS

如果你已经有一些大文件在 Git 仓库中，并且想要将它们转移到 Git LFS，可以使用 [git lif migrate](https://github.com/git-lfs/git-lfs/blob/main/docs/man/git-lfs-migrate.adoc?utm_source=gitlfs_site&utm_medium=doc_man_migrate_link&utm_campaign=gitlfs#examples) 命令：

```bash
git lfs migrate import --include="*.psd"
```

这将会将所有 `.psd` 文件从 Git 仓库中移除，并将它们添加到 Git LFS 中。

另外，可以用这个命令查看各类文件占用的空间情况:

```bash
git lfs migrate info
# Fetching remote refs: ..., done
# Sorting commits: ..., done
# Examining commits: 100% (1/1), done
# *.mp3   284 MB    1/1 files(s)  100%
# *.pdf   42 MB     8/8 files(s)  100%
# *.psd   9.8 MB  15/15 files(s)  100%
# *.ipynb 6.9 MB    6/6 files(s)  100%
# *.csv   5.8 MB    2/2 files(s)  100%
```

### 2.4 提交和推送

在添加了大文件到 Git LFS 后，像平常一样提交和推送：

（确保 `.gitattributes` 文件已经添加到 Git 仓库中）

```bash
git add .gitattributes
git add <your_large_file>
git commit -m "Add large file"
git push
```
