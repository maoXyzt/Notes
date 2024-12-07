# 下载 Google Drive 共享的文件

使用 `wget` 命令：

```bash
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=FILEID' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=FILEID" -O FILENAME && rm -rf /tmp/cookies.txt
```

修改 FILEID （从共享链接获取）和 FILENAME （保存时使用的名称，任意）

如果无法连接 google ，需要代理，加上：

```bash
export http_proxy=aaa.bbb.ccc.ddd:pppp
```

