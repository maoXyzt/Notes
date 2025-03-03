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
