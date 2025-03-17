# powershell 加速启动

> [PowerShell steps to fix slow startup](https://stackoverflow.com/questions/59341482/powershell-steps-to-fix-slow-startup)

用 **管理员权限** 运行以下命令：

```powershell
$env:PATH = [Runtime.InteropServices.RuntimeEnvironment]::GetRuntimeDirectory()
[AppDomain]::CurrentDomain.GetAssemblies() | ForEach-Object {
    $path = $_.Location
    if ($path) {
        $name = Split-Path $path -Leaf
        Write-Host -ForegroundColor Yellow "`r`nRunning ngen.exe on '$name'"
        ngen.exe install $path /nologo
    }
}
```
