# k8s runtime endpoints

| Runtime | Endpoint |
| --- | --- |
| containerd | unix:///var/run/containerd/containerd.sock |
| CRI-O | unix:///var/run/crio/crio.sock |
| Docker Engine（使用 cri-dockerd） | unix:///var/run/cri-dockerd.sock |
