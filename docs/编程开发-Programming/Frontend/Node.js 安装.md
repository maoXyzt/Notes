# 安装 Node.js

## 1. (推荐) 使用 `fnm` 管理 Node.js 版本

```bash
curl -fsSL https://fnm.vercel.app/install | bash
```

> [fnm](https://github.com/Schniz/fnm?tab=readme-ov-file#installation)

## 2. 使用 `nvm` 管理 Node.js 版本

```bash
https://github.com/Schniz/fnm?tab=readme-ov-file#installation
```

## 3. 通过平台的包管理器安装 Node.js

> [Node.js](https://nodejs.org/en/download/package-manager/)

## 4. 安装 `tar.gz` 包

```bash
wget https://nodejs.org/download/release/v16.19.1/node-v16.19.1-linux-x64.tar.gz
sudo tar -C /usr/local --strip-components 1 -xzf node-v16.19.1-linux-x64.tar.gz
```

> 查询所有release versions
> [Node.js](https://nodejs.org/en/download/releases/)
