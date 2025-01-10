# k8s 集群搭建

通过 kubeadm 搭建集群

> [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)

要求：

- 支持 deb/rpm 的 Linux 系统（如，Ubuntu 和 CentOS），本文以 Ubuntu 为例
- 2GiB 内存
- 2个CPU核
- 机器之间网络相互连通

目标：

- 搭建一个单control-plane的k8s集群
- 在集群上搭建一个Pod network，使Pods之间可以相互通信

## 1 前置要求

### 1.1 节点的 hostname，MAC 地址，product_uuid 互不相同

```bash
# MAC
ip link
ifconfig -a
# product_uuid
sudo cat /sys/class/dmi/id/product_uuid
```

### 1.2 端口可用

> 可能用到的所有端口：[Ports and Protocols](https://kubernetes.io/docs/reference/networking/ports-and-protocols/)

```bash
nc 127.0.0.1 6443
nc 127.0.0.1 10250
```

### 1.3 关闭 selinux

```bash
sudo touch /etc/selinux/config
sudo sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
# 重启
reboot
```

### 1.4 关闭 swap

```bash
sudo swapoff -a
# 永久关闭
sudo sed -i '/swap/s/^/#/' /etc/fstab
```

### 1.5 关闭防火墙

```bash
sudo systemctl stop firewalld
sudo systemctl disable firewalld
```

### 1.6 设置主机名

`hostnamectl set-hostname <hostname>`

```bash
# 在机器0上
sudo hostnamectl set-hostname k8s-master
# 在机器1上
sudo hostnamectl set-hostname k8s-node1
# 在机器2上
sudo hostnamectl set-hostname k8s-node2
```

在master节点上添加hosts

```bash
sudo cat >> /etc/hosts << EOF
192.168.217.100 k8s-master
192.168.217.101 k8s-node1
192.168.217.102 k8s-node2
EOF
```

### 1.7 IPv4 转发

```bash
sudo cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter
sudo cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF
sudo sysctl --system
```

### 1.8 配置时间同步

```cron
# Puppet Name: ntpdate
*/30 * * * * /usr/sbin/ntpdate ntp1.xxxx.com ntp2.xxxx.com
# Puppet Name: hwclock
*/30 * * * * /sbin/hwclock -w
```

## 2 安装 container runtime

> [Installing a container runtime](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#installing-runtime)

### 2.1 Docker Engine

本文使用 Docker Engine。安装方法：

> [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/#installation-methods)
>
> Optional:
>
> - [给非root用户运行docker命令的权限](https://github.com/maoXyzt/Notes/blob/master/docs/Programming/Docker/%E7%BB%99%E9%9D%9Eroot%E7%94%A8%E6%88%B7%E8%BF%90%E8%A1%8Cdocker%E7%9A%84%E6%9D%83%E9%99%90.md)

### 2.2 Container Runtime Interface (CRI)

由于 Docker Engine 未实现 CRI，因此需要安装 containerd

> [containerd](https://github.com/containerd/containerd/blob/main/docs/getting-started.md)

生成默认配置文件：

```bash
sudo containerd config default > /etc/containerd/config.toml
```

#### 2.2.1 配置 cgroup driver

`/etc/containerd/config.toml`:

```toml
[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
  ...
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
    SystemdCgroup = true
```

重启 containerd：

```bash
sudo systemctl restart containerd
```

#### 2.2.2 配置使用 GPU

> [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin#quick-start)

**(1) 配置 docker**

`/etc/docker/daemon.json`:

```json
{
  "default-runtime": "nvidia",
  "runtimes": {
    "nvidia": {
      "path": "/usr/bin/nvidia-container-runtime",
      "runtimeArgs": []
    }
  }
}
```

```bash
sudo systemctl restart docker
```

**(2) 配置 containerd**

`/etc/containerd/config.toml`:

```toml
version = 2
[plugins]
  [plugins."io.containerd.grpc.v1.cri"]
    [plugins."io.containerd.grpc.v1.cri".containerd]
      default_runtime_name = "nvidia"

      [plugins."io.containerd.grpc.v1.cri".containerd.runtimes]
        [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.nvidia]
          privileged_without_host_devices = false
          runtime_engine = ""
          runtime_root = ""
          runtime_type = "io.containerd.runc.v2"
          [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.nvidia.options]
            BinaryName = "/usr/bin/nvidia-container-runtime"
```

```bash
sudo systemctl restart containerd
sudo systemctl status containerd
```

**(3) Enabling GPU Support in Kubernetes**

```bash
kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.14.0/nvidia-device-plugin.yml
```

## 3 安装 `kubeadm`, `kubelet` 和 `kubectl`

> [Installing kubeadm, kubelet and kubectl](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#installing-kubeadm-kubelet-and-kubectl)

- `kubeadm`: the command to bootstrap the cluster.
- `kubelet`: the component that runs on all of the machines in your cluster and does things like starting pods and containers.
- `kubectl`: the command line util to talk to your cluster.

```bash
# Update the apt package index and install packages needed to use the Kubernetes apt repository:
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl

# Download the Google Cloud public signing key:
sudo mkdir -p /etc/apt/keyrings     # Ubuntu 22.04之前版本无 keyrings 目录，需要创建
sudo curl -fsSLo /etc/apt/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg

# Add the Kubernetes apt repository:
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list

# Update apt package index, install kubelet, kubeadm and kubectl, and pin their version:
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```

记录 kubelet, kubeadm, kubectl 的版本，它们应该是一致的(本文安装时版本为 1.27.1-00)。

## 4 配置

### 4.1 cgroup driver

#### 4.1.1 配置 container runtime 的 cgroup driver

配置使用systemd

```bash
sudo cat > /etc/docker/daemon.json << EOF
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com",
    "https://reg-mirror.qiniu.com",
    "https://registry.docker-cn.com"
  ],
  "exec-opts": ["native.cgroupdriver=systemd"]
}
EOF

sudo systemctl daemon-reload
sudo systemctl restart docker
sudo systemctl status docker
```

#### 4.1.2 配置 kubelet 的 cgroup driver

> [Configuring a cgroup driver | Kubernetes](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/configure-cgroup-driver/#configuring-the-kubelet-cgroup-driver)

编辑`KubeletConfiguration`的`cgroupDriver`选项，将其值设置为`systemd`。

```yaml
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
...
cgroupDriver: systemd
```

在下一节会进行更完整的配置。

### 4.2 (Optional) 准备所需的镜像

这一步是可选的，只有在你希望 `kubeadm init` 和 `kubeadm join` 不从 `registry.k8s.io` 下载默认容器镜像的情况下才适用。

Kubeadm 有一些命令可以帮助你在没有互联网连接的情况下创建一个集群节点时，预先拉取所需的镜像。请参阅 [Running kubeadm without an internet connection](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init#without-internet-connection) 以了解更多细节。

Kubeadm 允许你使用自定义镜像仓库来获取所需的镜像。请参阅 [Using custom images](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init#custom-images) 以了解更多细节。

```bash
sudo kubeadm config images list
sudo kubeadm config images pull --config kubeadm-config.yaml
```

### 4.3 初始化 control-plane 节点

control-plane 节点是 Kubernetes 集群中的主节点，负责管理集群。在它上面会运行 control plane 组件，如 [etcd](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/) (集群数据库) 和 [API Server](https://kubernetes.io/docs/concepts/overview/components/#kube-apiserver) (`kube-apiserver`, `kubectl`命令行工具的后端)。

可以通过执行 `kubeadm init <args>` 命令初始化 control-plane 节点。

- 有关 `kubeadm init` 参数的更多信息，请参见 [kubeadm reference guide](https://kubernetes.io/docs/reference/setup-tools/kubeadm/)。
  1. (Recommended) 如果希望将 control-plane 升级为高可用，应指定 `--control-plane-endpoint` 为所有 control-plane 节点设置共享 endpoint（可以是负载均衡器的DNS名称或IP地址）。
  2. 选择一个 Pod 网络插件，并验证是否需要为 kubeadm init 传递参数。(`--pod-network-cidr`)
  3. (Optional) kubeadm会自动检查使用的 container runtime。通过 `--cri-socket` 参数可配置 （如，cri-dockerd 的 socket 为 `unix:///var/run/cri-dockerd.sock`）。
  4. (Optional) kubeadm 使用与默认网关关联的网络接口来设置此 control-plane 节点 API server 的广播地址。 要使用其他网络接口，请设置 `--apiserver-advertise-address=<ip-address>` 参数。
- 要使用配置文件配置 `kubeadm init` 命令， 请参见 [Using kubeadm init with a configuration file](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init/#config-file)。支持以下配置类型

```yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: InitConfiguration

apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration

apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration

apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration

apiVersion: kubeadm.k8s.io/v1beta3
kind: JoinConfiguration
```

- 要自定义 control-plane 组件，请参阅 [custom arguments](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/control-plane-flags/)。
- 要重新配置一个已经创建的集群， 请参见 [Reconfiguring a kubeadm cluster](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-reconfigure)。
  - `kubectl edit`
- 要再次运行 `kubeadm init`，你必须首先卸载集群 [tear down the cluster](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/#tear-down)。
  - 移除节点
  - 清理control plane

执行：

```bash
sudo kubeadm init \
  --pod-network-cidr=192.168.0.0/16 \
  --cri-socket=unix:///var/run/cri-dockerd.sock \
  --image-repository registry.aliyuncs.com/google_containers
```

或使用如下 `kubeadm-config.yaml` 文件：

```yaml
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
cgroupDriver: systemd
---
apiVersion: kubeadm.k8s.io/v1beta3
kind: InitConfiguration
---
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
networking:
  podSubnet: "192.168.0.0/16" # --pod-network-cidr
imageRepository: "registry.aliyuncs.com/google_containers"
```

执行:

```bash
sudo kubeadm init --config=kubeadm-config.yaml
```

`kubeadm init` 首先运行一系列预检查以确保机器为运行 Kubernetes 准备就绪。 这些预检查会显示警告并在错误时退出。然后 `kubeadm init` 下载并安装集群 control-plane 组件。这可能会需要几分钟。

**记录 `kubeadm init` 输出的 `kubeadm join` 命令**，如下。你需要此命令将节点加入集群。

```bash
kubeadm join <control-plane-host>:<control-plane-port> --token <token> --discovery-token-ca-cert-hash sha256:<hash>
```

> Kubeadm 对集群中的所有节点使用相同的 `KubeletConfiguration`。`KubeletConfiguration` 存储在 `kube-system` 命名空间下的一个 `ConfigMap` 对象中。
>
> 执行子命令 `init`、`join` 和 `upgrade` 将导致 kubeadm 将 `KubeletConfiguration` 作为一个文件写入 `/var/lib/kubelet/config.yaml` 并将其传递给本地节点 kubelet。

根据`kubeadm init`输出的提示信息，在master节点上执行如下命令（可使非root用户可以运行 kubectl）：

```bash
mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

## 5. 安装网络插件 - Container Network Interface (CNI)

你必须部署一个基于 Pod 网络插件的 容器网络接口 (CNI)，以便你的 Pod 可以相互通信。 在安装网络之前，集群 DNS (CoreDNS) 将不会启动。

每个集群只能安装一个 Pod 网络(在master节点安装)。

这里使用 calico 作为网络插件，安装方法如下：

> [Quickstart for Calico on Kubernetes | Calico Documentation](https://docs.tigera.io/calico/latest/getting-started/kubernetes/quickstart#how-to)

```bash
# 在k8s中安装calico
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.25.1/manifests/tigera-operator.yaml
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.25.1/manifests/custom-resources.yaml

# 确认 calico 是否安装成功（直到所有容器状态都变为Running）
watch kubectl get pods -n calico-system
# 或(-w可以实时变化):
# kubectl get pods --all-namespaces -w
```

消除 master 隔离。默认 master 上不调度 pods，要允许另外的 pods 在 master 上运行请执行该命令

```bash
kubectl taint nodes --all node-role.kubernetes.io/control-plane-
kubectl taint nodes --all node-role.kubernetes.io/master-

# 输出如下类似内容：
# node/<your-hostname> untainted
```

确认在集群中有一个或多个节点已经就绪：

```bash
kubectl get nodes -o wide

# 输出如下类似的内容
# NAME              STATUS   ROLES    AGE   VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION    CONTAINER-RUNTIME
# <your-hostname>   Ready    master   52m   v1.12.2   10.128.0.28   <none>        Ubuntu 18.04.1 LTS   4.15.0-1023-gcp   docker://18.6.1
```

> Optional：
>
> [Install calicoctl | Calico Documentation](https://docs.tigera.io/calico/latest/operations/calicoctl/install)

## 6. 加入节点

1. 切换到root用户 `sudo su -`
2. 安装container runtime 和 CRI
3. 安装 kubeadm、kubelet 和 kubectl
4. 执行 `kubeadm join` 命令（已由`kubeadm init`给出）

```bash
kubeadm join <control-plane-host>:<control-plane-port> --token <token> --discovery-token-ca-cert-hash sha256:<hash>
```

由于节点安装了 cri-dockerd，所以`kubeadm join`还需要额外指定 --cri-socket=unix:///var/run/cri-dockerd.sock

> - \<token\>: 用于节点之间的相互身份验证，24h后自动失效。可以使用 `kubeadm token` 命令列出，创建和删除。请参阅 [kubeadm reference guide](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-token/)
> - \<hash\>: 通过以下命令可得到`--discovery-token-ca-cert-hash`的值：
>
> ```bash
> openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | \
>   openssl dgst -sha256 -hex | sed 's/^.* //'
> ```

## 7. 最终检查

在master节点上执行如下命令：

- 查看节点状态

```bash
kubectl get pods -n kube-system

# 输出如下类似内容：
# NAME       STATUS   ROLES           AGE   VERSION   INTERNAL-IP       EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION       CONTAINER-RUNTIME
# ubuntu16   Ready    control-plane   94m   v1.27.1   192.168.225.129   <none>        Ubuntu 16.04.7 LTS   4.4.0-186-generic    docker://20.10.7
# ubuntu18   Ready    <none>          25m   v1.27.1   192.168.225.130   <none>        Ubuntu 18.04.6 LTS   4.15.0-208-generic   docker://23.0.3
# ubuntu20   Ready    <none>          23m   v1.27.1   192.168.225.131   <none>        Ubuntu 20.04.6 LTS   5.4.0-146-generic    docker://23.0.3
```

- 查看集群健康状态

```bash
kubectl get cs

# 输出如下类似内容：
# NAME                 STATUS    MESSAGE                         ERROR
# controller-manager   Healthy   ok
# scheduler            Healthy   ok
# etcd-0               Healthy   {"health":"true","reason":""}
```

```bash
kubectl cluster-info

# 输出如下类似内容：
# Kubernetes control plane is running at https://192.168.225.129:6443
# CoreDNS is running at https://192.168.225.129:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
#
# To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

## 8. 安装 Dashboard

选择 kuboard

> [安装 Kubernetes 多集群管理工具](https://kuboard.cn/install/v3/install.html)
