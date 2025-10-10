# 自动生成 CHANGELOG.md

借助 [generate-changelog](https://www.npmjs.com/package/generate-changelog) 可以自动生成 `CHANGELOG.md` 文件。

## 1 - 安装

```bash
npm install -D generate-changelog
```

## 2 - 使用方法

changelog 命令通过 `-p`, `-m`, `-M` 参数来生成不同类型的 changelog。

```bash
    -p, --patch            create a patch changelog
    -m, --minor            create a minor changelog
    -M, --major            create a major changelog
```

可以配置 `package.json` 中的 `scripts` 命令来使用:

```json
{
  "scripts": {
    "release:major": "changelog -M && git add CHANGELOG.md && git commit -m \"updated CHANGELOG.md\" && npm version major && git push origin && git push origin --tags",
    "release:minor": "changelog -m && git add CHANGELOG.md && git commit -m \"updated CHANGELOG.md\" && npm version minor && git push origin && git push origin --tags",
    "release:patch": "changelog -p && git add CHANGELOG.md && git commit -m \"updated CHANGELOG.md\" && npm version patch && git push origin && git push origin --tags"
  }
}
```

执行上述命令将自动更新 `CHANGELOG.md` 文件, 更新 `package.json` 中的 `version` 字段, 并打上对应的 tag 和推送到远端仓库。

```bash
npm run release:major
npm run release:minor
npm run release:patch
```
