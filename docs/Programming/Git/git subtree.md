# 使用 Git Subtree 同步子项目

> [用 Git Subtree 在多个 Git 项目间双向同步子项目，附简明使用手册 (youzan.com)](https://tech.youzan.com/git-subtree/)
>
> [git subtree教程 - SegmentFault 思否](https://segmentfault.com/a/1190000012002151)

从 [Git 1.5.2](http://lwn.net/Articles/235109/) 开始，Git 新增并推荐使用这个功能来管理子项目

## 优点

> 经由 Git Subtree 来维护的子项目代码，对于父项目来说是透明的，所有的开发人员**看到的就是一个普通的目录，原来怎么做现在依旧那么做**，只需要维护这个 Subtree 的人在合适的时候去做同步代码的操作。

## 操作

### 在父仓库中新增子仓库

`git subtree add --prefix=<prefix> <commit>`

`git subtree add --prefix=<prefix> <repository> <ref>`

```bash
# 直接添加 subtree
git subtree add --prefix=components/zenjs http://github.com/youzan/zenjs.git master --squash

# 先添加 remote 方便记忆；再添加 subtree
git remote add zenjs http://github.com/youzan/zenjs.git  
git subtree add --prefix=components/zenjs zenjs master 
```

(`--squash`参数表示不拉取历史信息，而只生成一条commit信息。)

现在对于其他项目人员来说，这个仓库可以像普通仓库一样使用，正常地pull/push，不需要知道 zenjs 是一个子仓库，更不会影响子仓库。

### 从源仓库拉取更新

`git subtree pull --prefix=<prefix> <repository> <ref>`

```bash
git subtree pull --prefix=components/zenjs zenjs master  
```

### 推送修改到源仓库

`git subtree push --prefix=<prefix> <repository> <ref>`

```bash
git subtree push --prefix=components/zenjs zenjs hotfix/zenjs_xxxx
```

这会在远程的zenjs的仓库里生成一个叫 hotfix/zenjs_xxxx 的的分支，包含了你过去对components/zenjs 所有的更改记录。

> 有人可能会问，只用master分支，不管版本，太有风险了。
>
> 对的，正如我们前面说到的那样，subtree的方案适用的场景是：各个项目共用一个库，而这个库正在快速迭代更新的过程中。如果追求稳定，只需要给库拉出一个如v0.1.0这样的版本号命名的稳定分支，subtree只用这个分支即可。

### split

重新split出一个新起点（这样，每次提交subtree的时候就不会从头遍历一遍了）

```bash
git subtree split --rejoin --prefix=components/zenjs --branch new_zenjs
git push zenjs new_zenjs:master  
```

## Q&A

Q1. 如果在父项目中删除整个子项目的目录并提交，会导致子项目被删除吗？

A1. 不会。这时相当于父项目与子项目的之间的联系被删除，无法再`git subtree push`到向子项目上。

Q2. 要切换子项目分支，该怎么做？

A1. 删除原先的子项目目录，然后重新`git subtree add`另一分支（麻烦）

