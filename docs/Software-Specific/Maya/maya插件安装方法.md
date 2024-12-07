---

通过环境变量`MAYA_PLUG_IN_PATH`指定插件路径，或通过`MAYA_SHELF_PATH`指定Maya工具架Shelf的路径

[Setting environment variables using Maya.env](https://knowledge.autodesk.com/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2016/ENU/Maya/files/GUID-8EFB1AC1-ED7D-4099-9EEE-624097872C04-htm.html)



---

在Maya的main Maya preferences directory目录下创建一个`modules`文件夹，

例如：

`/Users/[********]/Library/Preferences/Autodesk/maya/modules`

以插件名为文件名，如`tradigiTOOLS.module`，创建如下内容的文件：

```
//Module file for Maya.  Helps Maya find resources for tradigiTOOLS.
+ tradigiTOOLS 1.30 /Applications/FUNhouse/tradigiTOOLS
```



插件安装的位置的目录结构应该类似 preferences 目录，例如，插件安装在：

```
/special/mayaModule/
```

则应该包含如下目录：

```
/special/mayaModule/bin
/special/mayaModule/icons
/special/mayaModule/plug-ins
/special/mayaModule/scripts
```



---

[Maya 常用环境变量详解 - ibingshan - 博客园 (cnblogs.com)](https://www.cnblogs.com/ibingshan/p/9786721.html)
