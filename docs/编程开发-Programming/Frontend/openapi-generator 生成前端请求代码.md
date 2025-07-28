# openapi-generator 生成前端请求代码

openapi-generator 是一个开源工具，可以根据 OpenAPI 规范生成客户端代码。

> [OpenAPITools/openapi-generator-cli](https://github.com/OpenAPITools/openapi-generator-cli)

由于运行 `openapi-generator-cli` 需要依赖 Java 环境，因此可通过以下方式使用 `openapi-generator-cli`:

1. (推荐) 基于 Python 和 jdk4py
2. 基于 Docker 镜像运行
3. 基于本地安装的 JDK 运行

## 0. 推荐用法

1. 按照 [1.1](#11-非-docker-方式) 添加 `openapitools.yaml` 配置
2. 按照 [2.1.1](#211-使用-uvx-命令) 配置 `package.json` 的 scripts 命令
3. 执行 `npm run generate:client` 生成客户端代码

## 1. 任务配置

### 1.1 非 Docker 方式

准备如下项目目录结构：

```text
.
├── codegen/
│   └── openapi.json
├── src/
│   └── lib/
│       └── _client/
├── openapitools.yaml
└── package.json
```

编写配置文件 `openapitools.yaml` 内容如下：

```yaml
# openapitools.yaml
# References:
# - https://openapi-generator.tech/docs/generators/typescript-axios
inputSpec: codegen/openapi.json
outputDir: src/lib/_client
generatorName: typescript-axios
apiPackage: api
modelPackage: model
additionalProperties:
  withSeparateModelsAndApi: on
  npmVersion: 20.17.0
  supportsES6: on
# typeMappings: Date=string
validateSpec: off
```

注意其中配置项:

- `inputSpec`: 指定 OpenAPI 规范文件路径; 也可使用 `-i` 参数指定。
  - 一些后端框架可以自动生成，例如 [FastAPI](https://fastapi.tiangolo.com/features/#automatic-docs) 后端服务可通过 `/openapi.json` 路径获得。
- `outputDir`: 指定生成的客户端代码输出目录; 也可使用 `-o` 参数指定。
  - 这里指定输出目录为 `src/lib/_client`, 建议把该目录排除在 `prettier` & `eslint` 的检查范围之外。
- `generatorName`: 指定生成器名称
  - 这里选用 [typescript-axios](https://openapi-generator.tech/docs/generators/typescript-axios) 生成器，生成 TypeScript 客户端代码，使用 axios 进行请求
- `additionalProperties`:
  - `npmVersion`: 指定 npm 版本；这里使用 `nodejs 20.17.0` 版本
  - `supportsES6`: 指定是否支持 ES6

当执行 `openapi-generator-cli` 命令时，会加载工作目录的 `openapitools.yaml`, 或手动指定 `-c <path/to/config>`。

### 1.2 Docker 方式

利用镜像 `openapitools/openapi-generator-cli:v7.14.0` 来执行生成器命令。

镜像主页: [openapitools/openapi-generator-cli](https://hub.docker.com/r/openapitools/openapi-generator-cli)

准备如下项目目录结构：

```text
.
├── codegen/
│   ├── docker-compose.yml
│   ├── generate.sh
│   ├── openapi.json
│   └── openapitools.yaml
├── src/
│   └── lib/
│       └── _client/
└── package.json
```

`docker-compose.yml` 配置文件内容如下：

```yaml
# docker-compose.yml
services:
  openapi-generator-cli:
    image: openapitools/openapi-generator-cli:v7.14.0
    working_dir: /tmp/src
    entrypoint: ['bash']
    command: ['./generate.sh']
    volumes:
      - .:/tmp/src # For reading OpenAPI spec
      - ../src/lib/_client:/tmp/dist # For saving generated client
      # - ./mocks:/tmp/mocks # For saving generated mock server
```

`generate.sh` 是 docker 容器中执行的脚本，内容如下：

```bash
#!/bin/bash
# Description: Generate the API code from the OpenAPI specification
# Used inside docker container
_GRAY_BOLD='\033[1;30m'
_BLUE='\033[34m'
_GREEN='\033[32m'
_NC='\033[0m' # No Color

printf "${_GRAY_BOLD}"
echo "======================================================"
echo "    Generating API code from OpenAPI specification    "
echo "======================================================"
printf "${_NC}"
# echo " ⚙️ Working directory: $(pwd)"

export INPUT_FILE="./openapi.json"
export CONFIG_FILE="./client.config.yaml"
export OUTPUT_DIR="../dist"

set -e

# generate
echo ""
cwd=$(pwd)
printf "🔥 ${_BLUE}(a) Generating client code from OpenAPI specification ...${_NC}\n"
cd "$CLIENT_OUTPUT_DIR" && rm -rf * && cd $cwd
docker-entrypoint.sh generate -i "$INPUT_FILE" -o "$CLIENT_OUTPUT_DIR" -c "$CONFIG_FILE"
printf "✅ ${_GREEN}Client code generated!${_NC}\n"

echo ""
printf "👍️ ${_GREEN}===Generation successful!${_NC}\n"
echo ""
```

配置文件 `openapitools.yaml` 内容如下:

(其中省略了 `inputSpec` 和 `outputDir`, 在 `generate.sh` 中通过 `-i` 和 `-o` 参数直接指定)：

```yaml
# openapitools.yaml
# References:
# - https://openapi-generator.tech/docs/generators/typescript-axios
# inputSpec: /tmp/src/openapi.json
# outputDir: /tmp/dist
generatorName: typescript-axios
apiPackage: api
modelPackage: model
additionalProperties:
  withSeparateModelsAndApi: on
  npmVersion: 20.17.0
  supportsES6: on
# typeMappings: Date=string
validateSpec: off
```

## 2. 运行

### 2.1 基于 Python 和 jdk4py 来执行

#### 2.1.1 使用 `uvx` 命令

推荐使用 `uvx` 命令 (依赖 [uv](https://docs.astral.sh/uv/)) 直接执行，不用操心当前的 Python 环境。更适合写到 `package.json` 的 scripts 中。

```bash
uvx "openapi-generator-cli[jdk4py]==7.14.0" generate -c openapitools.yaml
```

可以配置到 `package.json` 的 scripts 中：

```json
{
  "scripts": {
    "generate:client": "uvx 'openapi-generator-cli[jdk4py]==7.14.0' generate -c openapitools.yaml"
  }
}
```

然后可以执行 `npm run generate:client` 来生成客户端代码：

```bash
# with npm
npm run generate:client
# with pnpm
pnpm generate:client
# with yarn
yarn generate:client
```

#### 2.1.2 不使用 `uvx` 命令

如果不希望安装和使用 `uvx` 命令，则需要先安装依赖到当前的 Python 环境，然后在命令行中运行：

```bash
pip install "openapi-generator-cli[jdk4py]==7.14.0"
openapi-generator-cli generate -c openapitools.yaml
```

配置到 `package.json` 的 scripts 中：

```json
{
  "scripts": {
    "generate:client": "openapi-generator-cli generate -c openapitools.yaml"
  }
}
```

同样可以执行 `npm run generate:client` 来生成客户端代码，但需要确保执行前处于正确的 Python 环境：

```bash
# with npm
npm run generate:client
# with pnpm
pnpm generate:client
# with yarn
yarn generate:client
```

## 2.2 基于 Docker 镜像来执行

需要安装 Docker。

### 2.2.1 通过 `docker-compose` 命令执行

```bash
docker-compose -f codegen/docker-compose.yml run --rm openapi-generator-cli
```

配置到 `package.json` 的 scripts 中：

```json
{
  "scripts": {
    "generate:client": "docker-compose -f codegen/docker-compose.yml run --rm openapi-generator-cli"
  }
}
```

执行 `npm run generate:client` 即可生成客户端代码（略）

### 2.2.2 直接通过 `docker run` 命令执行

直接通过 `docker run` 命令执行：

```bash
docker run --rm \
  -w /tmp/src \
  -v ./codegen:/tmp/src \
  -v ./src/lib/_client:/tmp/dist \
  --entrypoint bash \
  openapitools/openapi-generator-cli:v7.12.0 \
  generate.sh
```

配置到 `package.json` 的 scripts 中：

```json
{
  "scripts": {
    "generate:client": "docker run --rm -w /tmp/src -v ./codegen:/tmp/src -v ./src/lib/_client:/tmp/dist --entrypoint=bash openapitools/openapi-generator-cli:v7.12.0 generate.sh"
  }
}
```

执行 `npm run generate:client` 即可生成客户端代码（略）

## 2.3 基于本地 Java 环境来执行

需要本地已经安装了 JDK 环境。

安装 `@openapitools/openapi-generator-cli` 依赖：

```bash
# with npm
npm install -D @openapitools/openapi-generator-cli
# with pnpm
pnpm add -D @openapitools/openapi-generator-cli
# with yarn
yarn add -D @openapitools/openapi-generator-cli
```

在 `package.json` 中添加脚本命令：

```json
{
  "scripts": {
    "generate:client": "openapi-generator-cli generate"
  }
}
```

## 3. 获取 `openapi.json` 文件的辅助脚本

可以把如下脚本放到 `codegen/` 目录下：

- `run-update.js`: 根据平台调用 `update.ps1` 或 `update.sh` 脚本
- `update.ps1`: 更新 `openapi.json` 文件的 PowerShell 脚本
- `update.sh`: 更新 `openapi.json` 文件的 Bash 脚本

### 3.1 `run-update.js`

`run-update.js` 脚本内容如下：

```javascript
// run-update.js
import { execSync } from 'child_process';
import os from 'os';

if (os.platform() === 'win32') {
  execSync('powershell -File codegen/update.ps1');
} else {
  execSync('bash codegen/update.sh');
}
```

### 3.2 `update.ps1`

`update.ps1` 脚本内容如下：

```powershell
# Get the directory of the current script
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$PRJ_ROOT_DIR = Split-Path -Parent $SCRIPT_DIR

# Try to load .env file if it exists
$DOT_ENV_FILE = Join-Path $PRJ_ROOT_DIR ".env"
if (Test-Path $DOT_ENV_FILE) {
    Get-Content $DOT_ENV_FILE | ForEach-Object {
        if ($_ -match '^([^=]+)=(.*)$') {
            $name = $matches[1]
            $value = $matches[2]
            Set-Item -Path "env:$name" -Value $value
        }
    }
}

# Set default values if environment variables are not set
if (-not $env:OPENAPI_SPEC_URL) {
    $env:OPENAPI_SPEC_URL = "http://api.cubicraft.zoe.sensetime.com/api/v1/openapi.json"
}
if (-not $env:OUTPUT_FILE) {
    $env:OUTPUT_FILE = Join-Path $SCRIPT_DIR "openapi.json"
}

Write-Host "OPENAPI_SPEC_URL: $env:OPENAPI_SPEC_URL"
Write-Host "OUTPUT_FILE: $env:OUTPUT_FILE"

try {
    Invoke-WebRequest -Uri $env:OPENAPI_SPEC_URL -OutFile $env:OUTPUT_FILE
} catch {
    Write-Error "Error: Failed to download OpenAPI spec"
    exit 1
}
```

### 3.3 `update.sh`

`update.sh` 脚本内容如下：

```bash
#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PRJ_ROOT_DIR="$(dirname "${SCRIPT_DIR}")"

DOT_ENV_FILE="${PRJ_ROOT_DIR}/.env"
if [[ -f "$DOT_ENV_FILE" ]]; then
  source "$DOT_ENV_FILE"
fi

if [[ -z "$OPENAPI_SPEC_URL" ]]; then
  OPENAPI_SPEC_URL="http://api.cubicraft.zoe.sensetime.com/api/v1/openapi.json"
fi
if [[ -z "$OUTPUT_FILE" ]]; then
  OUTPUT_FILE="$SCRIPT_DIR/openapi.json"
fi

echo -e "OPENAPI_SPEC_URL: $OPENAPI_SPEC_URL"
echo -e "OUTPUT_FILE: $OUTPUT_FILE"

curl -o "$OUTPUT_FILE" $OPENAPI_SPEC_URL

if [[ $? -ne 0 ]]; then
  echo "Error: Failed to download OpenAPI spec"
  exit 1
fi
```

## 3. Example: 项目中使用生成的 API 客户端

首先创建 `src/services/common.ts` 文件，添加 API 客户端的配置信息，如下：

```typescript
/**
 * src/services/common.ts
 * Common utilities for services
 */
import { Configuration } from '@/lib/_client'

// Api configuration for all services
export const apiConfig = new Configuration({
  basePath: '',
  // accessToken: () => '', // Optional: set access token
})
```

然后在 `src/services/api` 目录下创建各组 API 的服务模块，例如 `src/services/api/user.ts` 文件：

```typescript
/**
 * src/services/api/user.ts
 * Example service module for user API
 */
import { UserApi } from '@/lib/_client'
import { apiConfig } from '../common'
import type * as __types__ from '@/lib/_client/model'

const userApi = new UserApi(apiConfig)

export const getUser = async (userId: string): Promise<__types__.User> => {
  const response = await userApi.getUser(userId)
  // codes for handle response
  // ...
  return response.data
}
```
