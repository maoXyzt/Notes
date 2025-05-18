---
NoteStatus: editing
---

# 配置 Pyright

Pyright 是一个强大的 Python 静态类型检查工具，可以帮助开发者提前发现潜在的类型错误和代码问题。

## 1 - 配置文件 `pyrightconfig.json`

在项目根目录创建 `pyrightconfig.json` 文件。

### 1.1 常用配置项

#### 1.1.1 基础配置

- `exclude`: 排除的文件或目录。可缩小检查范围，加快检查速度。
- `include`: 包含的文件或目录。可缩小检查范围，加快检查速度。
- `ignore`: 忽略特定错误类型。例如 `["reportMissingImports"]` 可以忽略未导入模块的警告。

#### 1.1.2 类型检查配置

- `typeCheckingMode`: 类型检查模式
  - `"basic"`: 基本类型检查
  - `"strict"`: 严格类型检查
  - `"off"`: 关闭类型检查

#### 1.1.3 环境配置

- `venvPath`: 虚拟环境路径
- `venv`: 虚拟环境名称
- `pythonVersion`: Python 版本
- `pythonPlatform`: Python 平台（如 "Windows"、"Linux"、"Darwin"）

#### 1.1.4 性能配置

- `maxCacheSize`: 最大缓存大小（MB）
- `maxWorkerCount`: 最大工作进程数

## 2 - 配置示例

基础配置示例:

```json
{
  "exclude": [
    ".history",
    "build",
    "dist",
    "logs",
    "**/node_modules",
    "**/__pycache__"
  ],
  "include": [
    "src",
    "tests"
  ],
  "ignore": [
    "reportMissingImports"
  ]
}
```

严格类型检查配置示例:

```json
{
  "typeCheckingMode": "strict",
  "reportMissingImports": true,
  "reportMissingTypeStubs": true,
  "reportGeneralTypeIssues": true,
  "reportOptionalMemberAccess": true,
  "useLibraryCodeForTypes": true
}
```

## 3 - 最佳实践

1. **渐进式采用**
   - 开始时使用 `"typeCheckingMode": "basic"`
   - 随着项目成熟，逐步过渡到 `"strict"` 模式

2. **性能优化**
   - 使用 `exclude` 排除不需要检查的目录
   - 适当设置 `maxCacheSize` 和 `maxWorkerCount`

3. **类型存根文件**
   - 为第三方库创建类型存根文件（.pyi）
   - 使用 `reportMissingTypeStubs` 确保类型存根完整性

4. **虚拟环境**
   - 正确配置 `venvPath` 和 `venv` 确保类型检查使用正确的环境

5. **错误处理**
   - 使用 `ignore` 配置临时忽略特定错误
   - 定期审查忽略的错误，确保它们仍然合理

### VS Code 集成

在 VS Code 中使用 Pyright：

1. 安装 Pylance 扩展
2. 在设置中启用 Pyright：

```json
{
  "python.analysis.typeCheckingMode": "basic"
}
```

3. 可选：在项目级别覆盖设置：

```json
{
  "python.analysis.typeCheckingMode": "strict",
  "python.analysis.diagnosticMode": "workspace"
}
```
