# openapi-generator 生成前端请求代码

openapi-generator 是一个开源工具，可以根据 OpenAPI 规范生成客户端代码。

## 1. 环境

需要安装 Docker，用于执行生成器命令。

* 基于 docker 镜像执行工具命令:
  * 镜像: `openapitools/openapi-generator-cli:v7.12.0`
  * DockerHub 主页: [openapitools/openapi-generator-cli](https://hub.docker.com/r/openapitools/openapi-generator-cli)
* 客户端代码代码要求：
  * 生成 TypeScript 客户端代码，使用 axios 进行请求
    * 选用生成器: [typescript-axios](https://openapi-generator.tech/docs/generators/typescript-axios)

## 2. 使用

### 2.1 文件目录结构

准备如下项目目录结构：

```text
.
├── codegen
│   ├── client.config.yaml
│   ├── docker-compose.yml
│   ├── generate.sh
│   └── openapi.json
└── src
    └── lib
        └── _client/
```

* `openapi.json`: API 服务的 OpenAPI 规范文件 (FastAPI 后端会自动生成，访问服务的 `/openapi.json` 路径获得)
* `client.config.yaml`: 生成器配置文件
* (可选) `docker-compose.yml`: 用于配置 docker 容器的环境和启动命令，执行生成脚本; 也可直接使用 `docker run` 命令
* `generate.sh`: 生成脚本，对生成器进行配置和调用
* `src/lib/_client`: 生成的客户端代码输出目录, 在 `src` 目录下，方便后续使用

### 2.2 配置文件

`generate.sh` 脚本内容如下：

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
# echo "⚙️ Working directory: $(pwd)"

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

`client.config.yaml` 配置文件内容如下:

```yaml
# client.config.yaml
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

### 3. 生成代码

#### 3.1 使用 docker compose 方式执行

配置 `docker-compose.yml` 文件内容如下：

```yaml
# docker-compose.yml
services:
  openapi-generator-cli:
    image: openapitools/openapi-generator-cli:v7.12.0
    working_dir: /tmp/src
    entrypoint: ['bash']
    command: ['./generate.sh']
    volumes:
      - .:/tmp/src # For reading OpenAPI spec
      - ../src/lib/_client:/tmp/dist # For saving generated client
      # - ./mocks:/tmp/mocks # For saving generated mock server
```

利用 `docker-compose.yml` 配置文件，执行如下命令，生成客户端代码：

```bash
docker-compose -f codegen/docker-compose.yml run --rm openapi-generator-cli
```

生成的代码会输出到 `src/lib/_client` 目录下。

#### 3.2 使用 docker run 方式执行

也可以直接用 `docker run` 命令执行：

```bash
docker run --rm \
    -w /tmp/src \
    -v ./codegen:/tmp/src \
    -v ./src/lib/_client:/tmp/dist \
    --entrypoint bash \
    openapitools/openapi-generator-cli:v7.12.0 \
    generate.sh
```

生成的代码会输出到 `build/_client` 目录下。

#### 3.3 使用 npm scripts 方式执行

可以配置 [3.1](#31-使用-docker-compose-方式执行) 或 [3.2](#32-使用-docker-run-方式执行) 的执行命令到 `package.json` 的 scripts 中，方便执行：

```json
{
  "scripts": {
    "generate:client": "docker-compose -f codegen/docker-compose.yml run --rm openapi-generator-cli"
  }
}
```

或:

```json
{
  "scripts": {
    "generate:client": "docker run --rm -w /tmp/src -v ./codegen:/tmp/src -v ./src/lib/_client:/tmp/dist --entrypoint=bash openapitools/openapi-generator-cli:v7.12.0 generate.sh"
  }
}
```

执行 `npm run generate:client` 即可生成客户端代码:

```bash
# with npm
npm run generate:client
# with pnpm
pnpm generate:client
# with yarn
yarn generate:client
```
