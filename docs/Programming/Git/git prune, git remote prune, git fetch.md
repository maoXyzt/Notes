# git prune, git remote prune, git fetch --prune 三者异同

> <https://blog.csdn.net/sgs595595/article/details/72480346>

## 远程分支的3种状态

- 远程仓库确实存在分支dev
- 本地版本库（.git）中的远程快照
- 和远程分支建立联系的本地分支

## git prune

<https://git-scm.com/docs/git-prune>

Prune all unreachable objects from the object database
unreachable objects 指的是.git\objects中没有被使用的hash文件

```bash
song@test MINGW64 /d/Git/Temp (master)
$ git prune -n
0baff3f3df27aacdd2edb6f83a5c47dd3b7ca05b tree

song@test MINGW64 /d/Git/Temp (master)
$ git prune

song@test MINGW64 /d/Git/Temp (master)
$ git prune -n
```

## git remote prune origin

<https://git-scm.com/docs/git-remote>

Deletes all stale remote-tracking branches under .
会清理掉状态2中的远程库已被删除的远程分支，本地库仍存在的 stale remote-tracking branches

```bash
song@test MINGW64 /d/Git/Temp (master)
$ git branch
* master

song@test MINGW64 /d/Git/Temp (master)
$ git checkout -b dev
Switched to a new branch 'dev'

song@test MINGW64 /d/Git/Temp (dev)
$ git push origin dev
Total 0 (delta 0), reused 0 (delta 0)
To github.com:Song2017/Temp.git
 * [new branch]      dev -> dev

song@test MINGW64 /d/Git/Temp (dev)
$ git branch -a -v
* dev                   3902953  add readme.md
  master                3902953  add readme.md
  remotes/origin/HEAD   -> origin/master
  remotes/origin/dev    3902953  add readme.md
  remotes/origin/master 3902953  add readme.md
```

接下来，在github中删掉dev分支，此时本地版本库中的数据快照仍然有dev分支
git remote prune 会与远程库进行一次同步，最终清理掉版本库中的dev分支，但本地工作区中的dev分支并不会删除。

```bash
song@test MINGW64 /d/Git/Temp (master)
$ git remote prune origin
Pruning origin
URL: git@github.com:Song2017/Temp.git
 * [pruned] origin/dev

song@test MINGW64 /d/Git/Temp (master)
$ git branch -a -v
  dev                   3902953  add readme.md
* master                3902953  add readme.md
  remotes/origin/HEAD   -> origin/master
  remotes/origin/master 3902953  add readme.md
```

## git fetch –(2 -)prune

<https://git-scm.com/docs/git-fetch>

Before fetching, remove any remote-tracking references that no longer exist on the remote
同git remote prune
删除本地分支

```bash
git branch -d/D dev  # -D 强制删除
```
