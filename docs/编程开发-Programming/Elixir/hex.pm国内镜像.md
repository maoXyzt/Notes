# hex.pm国内镜像

> 原文：[UPYUN 支持 Elixir hex.pm 国内镜像 · Ruby China (ruby-china.org)](https://ruby-china.org/topics/31631)
>
> 官方说明：[Mirrors | Hex](https://hex.pm/docs/mirrors)

## 通过环境变量指定

配置如下环境变量

```bash
export HEX_MIRROR="https://hexpm.upyun.com"
export HEX_CDN="https://hexpm.upyun.com"
```

或临时指定

```bash
$ HEX_MIRROR=https://hexpm.upyun.com mix deps.get
$ HEX_CDN=https://hexpm.upyun.com rebar3 update
```

如果遇到下面问题：

> ** (Mix) Could not verify authenticity of fetched registry file. This may happen because a proxy or some entity is interfering with the download or because you don't have a public key to verify the registry.
>
> You may try again later or check if a new public key has been released in our public keys page: https://hex.pm/docs/public_keys

请先运行`mix local.hex`，参见 [#reply16](https://ruby-china.org/topics/31631#reply16)

## 通过配置文件指定

**Mix**:

```bash
mix hex.config mirror_url https://hexpm.upyun.com
```

**Rebar3**:

在全局或项目配置文件`rebar.config`中添加`{rebar_packages_cdn, "https://hexpm.upyun.com"}`

