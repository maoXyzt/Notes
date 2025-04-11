# Bash 脚本中获得脚本文件当前路径

## 0 - TL;DR

```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
```

`SCRIPT_DIR` 即为脚本文件的当前目录。
