# openapi-generator 生成前端请求代码

openapi-generator 是一个开源工具，可以根据 OpenAPI 规范生成客户端代码。

## 环境

* 基于 docker 镜像执行工具命令:
  * 镜像: `openapitools/openapi-generator-cli:v7.12.0`
  * DockerHub 主页: [openapitools/openapi-generator-cli](https://hub.docker.com/r/openapitools/openapi-generator-cli)
* 客户端代码代码要求：
  * 生成 TypeScript 客户端代码，使用 axios 进行请求
    * 选用生成器: [typescript-axios](https://openapi-generator.tech/docs/generators/typescript-axios)

## 使用

### 文件目录结构

准备如下项目目录结构：

```text
.
├── codegen
│   ├── openapi.json
│   ├── client.config.yaml
│   └── generate.sh
├── build
│   └── _client
└── docker-compose.yml
```

* `openapi.json`: API 服务的 OpenAPI 规范文件 (FastAPI 后端会自动生成，访问服务的 `/openapi.json` 路径获得)
* `client.config.yaml`: 生成器配置文件
* `generate.sh`: 生成脚本，对生成器进行配置和调用
* `build/_client`: 生成的客户端代码输出目录
* (可选) `docker-compose.yml`: 用于配置 docker 容器的环境和启动命令，执行生成脚本

### 配置文件

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

(可选) `docker-compose.yml` 配置如下：

```yaml
# docker-compose.yml
services:
  openapi-generator-cli:
    image: openapitools/openapi-generator-cli:v7.12.0
    working_dir: /tmp/src
    entrypoint: ['bash']
    command: ['./generate.sh']
    volumes:
      - ./codegen:/tmp/src # For reading OpenAPI spec
      - ./lib/_client:/tmp/dist # For saving generated client
      # - ./mocks:/tmp/mocks # For saving generated mock server
```

### 生成代码

利用 `docker-compose.yml` 配置文件，执行如下命令，生成客户端代码：

```bash
docker-compose run --rm openapi-generator-cli
```

生成的代码会输出到 `build/_client` 目录下。

---

也可以直接用 `docker run` 命令执行：

```bash
docker run --rm \
    -w /tmp/src \
    -v ./codegen:/tmp/src \
    -v ./build/_client:/tmp/dist \
    --entrypoint bash \
    openapitools/openapi-generator-cli:v7.12.0 \
    generate.sh
```

生成的代码会输出到 `build/_client` 目录下。
