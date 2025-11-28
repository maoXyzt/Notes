# Husky: 配置前端项目的 git hooks

> [Husky](https://typicode.github.io/husky/)

## 1. 安装 Husky

```bash
pnpm i -D husky
```

## 2. 初始化

```bash
pnpm exec husky init
```

## 3. 配置

编辑 `.husky/pre-commit` 文件，添加如下内容：

```bash
npx lint-staged
```

在 `package.json` 中添加 `lint-staged` 配置：

```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx,vue}": [
      "prettier --write",
      "eslint --ignore-path .gitignore --fix"
    ],
    "*.{json,md}": [
      "prettier --write"
    ]
  }
}
```

## 4. 全局初始化配置

有时候在 `pre-commit` 钩子中执行命令时，会报错 `command not found`，这是因为环境变量没有正确设置。

(比如在 VSCode UI 中使用 COMMIT 按钮提交代码，此时并未使用 `.bashrc` 或 `.zshrc` 加载环境变量)

可以在 `~/.husky/init.sh` 文件中添加如下内容，来初始化 Node.js 环境:

(按需选择一种方式)

```bash
# fnm
FNM_PATH="$HOME/.local/share/fnm"
if [ -d "$FNM_PATH" ]; then
  export PATH="$FNM_PATH:$PATH"
fi
# nvm
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
```
