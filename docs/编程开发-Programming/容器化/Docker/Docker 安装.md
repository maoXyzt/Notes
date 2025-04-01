# Docker 安装

Components to install:

+ [Docker Engine](https://docs.docker.com/engine/)
+ [Docker Build](https://docs.docker.com/build/)
+ [Docker Compose](https://docs.docker.com/compose/)

## 1. Install on Ubuntu

> [Install using the `apt` repository](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

### Uninstall old versions

### Set up Docker's apt repository

```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get -y install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

### Install the Docker packages

```bash
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### Verify the installation

```bash
sudo docker run hello-world
```

## 2. Next

[Give non-root users permission to run Docker commands](https://docs.docker.com/engine/install/linux-postinstall/)
