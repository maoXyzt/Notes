# Docker 镜像 alpine, slim, bullseye, bookeworm, noble 等的区别

> Ref: <https://medium.com/@faruk13/alpine-slim-bullseye-bookworm-noble-differences-in-docker-images-explained-d9aa6efa23ec>

## 1. Alpine

- Created with simplicity in mind, has a smaller footprint, uses less disk space.
- Different from Linux based images on its C library and coreutils implementation
- Linux based images use glibc(GNU C libraby) and coreutils(GNU coreutils) whereas Alpine Linux replaces it with musl libc and Busybox respectively as they are comparatively lighweight, and less bloat. Smaller, the better right? Is it though?
- Package Manager: `apk`
- Shell: `/bin/sh`

Use case:

Choose it when you need small sized image without bloat and you are sure the alpine based alternatives of core functionality is enough for your application.

## 2. Slim

- Both **Debian** and **Ubuntu** versions(below) have slim tagged images.
- Image size is significantly reduced from the standard image by a process called slimification.
- As per the docker Debian documentation, man pages, documentation files and some other extra files that are normally not necessary within containers are removed.
- For more details about what gets removed during the “slimification” process check [here](https://github.com/debuerreotype/debuerreotype/blob/master/scripts/.slimify-excludes) and [here](https://github.com/debuerreotype/debuerreotype/blob/master/scripts/.slimify-includes).
- Package Managers are similar to their corresponding standard images for Debian OS.

Use case:

Choose it when you want a reduced sized image from the standard image. In “slimification” process, it mentioned it removed docs, man pages and extra unnecessary files; which seems harmless, but would suggest to proceed with caution and thoroughly test it.

## 3. Debian 系列

### Jessie

- OS: Debian 8
- Kernel: Linux 3.16

### Stretch

- OS: Debian 9
- Kernel: Linux 4.9

### Buster

- OS: Debian 10
- Kernel: Linux 4.19 (FYI 4.19 is a more latest version than 4.9, in versioning language 4.x, 19>9)

### Bullseye

- OS: Debian 11
- Kernel: Linux 5.10

### Bookworm

- OS: Debian 12
- Kernel: Linux 6.1

## 4. Ubuntu 系列

### Xenial

Fullname: Xenial Xerus

- OS: Ubuntu 16.04
- Kernel: Linux 4.4

### Bionic

Fullname: Bionic Beaver

- OS: Ubuntu 18.04
- Kernel: Linux 4.15

### Focal

Fullname: Focal Fossa

- OS: Ubuntu 20.04
- Kernel: Linux 5.4

### Jammy

Fullname: Jammy Jellyfish

- OS: Ubuntu 22.04
- Kernel: Linux 5.15

### Mantic

Fullname: Mantic Minotaur

- OS: Ubuntu 23.10
- Kernel: Linux 6.5

### Noble

Fullname: Noble Numbat

- OS: Ubuntu 24.04
- Kernel: Linux 6.6
