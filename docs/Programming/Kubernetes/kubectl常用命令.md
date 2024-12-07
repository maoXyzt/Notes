# kubectl 常用命令

> [Getting Started | Kubernetes](https://kubernetes.io/docs/setup/)

## 1. 查询

不提供`-n`参数时，默认查询`default`命名空间下的资源

```bash
kubectl get pod -n jenkins
kubectl get pod --all-namespaces
```

```bash
kubectl get deployment -n jenkins
kubectl get deployment --all-namespaces
```
