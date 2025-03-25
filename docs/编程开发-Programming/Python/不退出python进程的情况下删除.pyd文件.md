# 不退出 python 进程的情况下删除 .pyd 文件

## 1 - 问题背景

在开发 Blender 插件时，有一个模块需要编译后使用。在 windows 平台上，编译产物为 `.pyd` 文件 (Windows Native Python Extension)。

插件启用过的状态下，卸载插件时，会因无法删除 `.pyd` 文件报错，导致卸载失败。

## 2 - 问题原因

插件启用时，`.pyd` 文件会被 Blender 的 python 进程 import。

Blender uninstall 插件时，会删除插件目录下的所有文件，包括 `.pyd` 文件。但因为 Blender 进程的 python 进程仍在运行，占用了 `.pyd` 文件，所以无法删除。

## 3 -  解决方案

Python 并未提供 unload 模块的方法，所以无法直接 unload 已经 import 的模块。

但我们可以 hack 一下，先将 ".pyd" 文件移动到临时文件夹，这样原先的插件目录就可以被删除了，临时文件夹会在 Blender 退出后自动被清理。
