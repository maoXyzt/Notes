# CUDA cuInit Unknown error

解决方法: 用 root 权限运行一次之后即可。

> 参考：
>
> [python - How to remove cuInit failed: unknown error in CUDA (PyCuda) - Stack Overflow](https://stackoverflow.com/questions/53369652/how-to-remove-cuinit-failed-unknown-error-in-cuda-pycuda#:~:text=cuInit)
>
> cuInit failed: unknown error is often the result of nvidia-uvm kernel module not being loaded. I've been periodically running into this issue on Ubuntu.
>
> sudo nvidia-modprobe -u should fix the problem. That is, until you reboot. Then you will need to do it again.
>
> Another workaround is to run your failing application as root once. AFAICT it in this case CUDA runtime will attempt to load the missing module (and will most likely succeed at that, because we're running as root).
