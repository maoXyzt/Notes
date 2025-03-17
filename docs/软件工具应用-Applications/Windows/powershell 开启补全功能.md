# powershell 开启补全功能

## tab 补全

> [Autocomplete in PowerShell](https://techcommunity.microsoft.com/t5/itops-talk-blog/autocomplete-in-powershell/ba-p/2604524)

编辑配置文件：

```powershell
Notepad $profile
```

添加如下内容:

```powershell
# Shows navigable menu of all options when hitting Tab

Set-PSReadlineKeyHandler -Key Tab -Function MenuComplete
```

## 智能提示

> [PowerShell IntelliSense completion](https://www.poppastring.com/blog/powershell-intellisense-completion)

安装 powershell 7.3 或以上版本，默认启用 Predictive IntelliSense 特性。

安装方法：通过 winget 安装

> [winget 国内源](./winget 国内源.md)

```powershell
winget search powershell
winget install --id Microsoft.PowerShell --source winget
```
