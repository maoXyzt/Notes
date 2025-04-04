# Global gitignore

我们不希望一些操作系统、IDE、编辑器等的特有文件被 git 托管，但项目的 `.gitignore` 文件应该记录那些不希望保存版本信息的文件/目录，或编译过程中生成的文件。

作为 best practice，可以使这类通用的条目被全局忽略。

## 方法

> [Global gitignore (github.com)](https://gist.github.com/subfuzion/db7f57fff2fb6998a16c)

- 在自己的 home 目录中创建 `.gitignore` 文件，加入需要忽略的条目
- 告诉 git 自己的全局 `.gitignore` 文件的位置

### 1) Mac

```bash
git config --global core.excludesfile ~/.gitignore
```

### 2) Windows

```bash
git config --global core.excludesfile "%USERPROFILE%\.gitignore"
```

PowerShell 用户：

```bash
git config --global core.excludesfile "$Env:USERPROFILE\.gitignore"
```

对于 windows 用户，应确认路径被正确解析：

```bash
git config --global core.excludesfile
```

以上操作会在 `.gitconfig` 中创建如下条目：

```ini
[core]
    excludesfile = {path-to-home-dir}/.gitignore
```

### 3) Visual Studio Code

对于 vscode 用户，开启如下选项使搜索时忽略相应的文件/目录。

```yml
"search.useIgnoreFiles": true,
"search.useGlobalIgnoreFiles": true
```

## Example of `.gitignore`

```bash
# Node
npm-debug.log

# Mac
.DS_Store

# Windows
Thumbs.db

# WebStorm
.idea/

# vi
*~

# General
log/
*.log

# etc...
```

更多 gitignore 模板，可参考

[gitignore/Global at main · github/gitignore](https://github.com/github/gitignore/tree/main/Global)
