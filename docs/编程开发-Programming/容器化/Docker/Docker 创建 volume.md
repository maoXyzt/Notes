# Docker 创建 volume

> Ref:
> [Volumes top-level element](https://docs.docker.com/reference/compose-file/volumes/)
> [Volumes](https://docs.docker.com/engine/storage/volumes/)

## 最小化的例子

```yaml
volumes:
  data-volume:

services:
  my-service:
    # ...
    volumes:
      - data-volume:/path/in/container
    # ...
```

## volume 选项

### driver

driver 选项可以指定 volume 的驱动，默认为 local。
local 驱动是 Docker 默认的驱动，它会在本地文件系统中创建 volume。

```yaml
volumes:
  data-volume:
    driver: local
```

如果 driver 选项指定的驱动不存在则会报错。

### driver_opts

driver_opts 选项可以指定 volume 驱动的参数。

local 驱动的参数为 `mount` 命令的参数, 有 type、device、o。

> [mount(8) — Linux manual page](https://man7.org/linux/man-pages/man8/mount.8.html)

```yaml
volumes:
  data-volume:
    driver: local
    driver_opts:
      type: none
      device: /path/to/dir
      o: bind
```

`type` 参数指定 volume 的类型。

`device` 参数指定 volume 的挂载点。

`o` 参数指定挂载选项。
