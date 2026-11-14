> 原文：https://www.superlogical.com/rex/docs/reference/privacy
> 原文版本：9a913bbcf2ab（抓取于 2026-11-13）

# 隐私与遥测

**Rex 不收集遥测数据。** 它不包含使用分析数据，没有自带的崩溃报告功能，也没有账户或许可证检查。

本页详细列出 Rex 各组件发起的所有网络连接、连接时机以及发送的内容。在 Rex 内部运行的程序不属于此范围。它们会建立各自独立的网络连接，不受我们的控制。

**Rex 仍处于测试阶段。** Rex 迭代迅速，本页内容可能会有所滞后。若此处有任何错误，请遵循[汉隆剃刀（Hanlon's razor）](https://en.wikipedia.org/wiki/Hanlon%27s_razor)原则：假设这是疏忽而非恶意，并在公测 Discord 频道中报告，以便我们及时修正。

## 出站连接

以下是 Rex 可能发起的出站连接列表。

| 连接类型 | 触发时机 | 目标位置 |
| --- | --- | --- |
| 检查更新 | Rex Mac 客户端，在启动时以及每天一次 | Superlogical 的更新服务器 |
| 远程服务端 | 仅限你主动添加的服务器 | 你所添加的服务器 |
| 崩溃报告 | Rex iOS 客户端，如果你选择共享或使用 TestFlight | Apple，随后至 Superlogical |
| 软件包更新 | Linux 与 WinGet，在你的包管理器执行更新时 | Superlogical 的软件包仓库 |
| Tailscale | 仅在主动启用时 | Tailscale 的服务器 |

## Rex Mac 客户端

### 检查更新

Rex Mac 客户端在启动时以及每天检查一次新版本，方法是从 Superlogical 的更新服务器下载带签名的版本发布订阅源。更新检查无法关闭。

每次检查仅发送常规 Web 请求所包含的内容：

- 你的 IP 地址。
- 包含应用名称与版本的 User-Agent，例如 `Rex Beta/0.1.0 Sparkle/2.9.6`。

它不会发送账户信息、设备标识符、系统配置概要，也不会发送关于你如何使用 Rex 的任何信息。只有当你选择安装更新时，才会下载更新文件。

### 本地服务端

Rex Mac 客户端会在你的 Mac 上运行一个 Rex 服务端，并通过 Unix 套接字与其通信，因此该流量永远不会离开你的机器。应用在启动服务端时不会开启任何网络监听器或 Tailscale。

### 远程服务端

Rex Mac 客户端仅连接至你主动添加的服务器。它会保持与这些服务器的连接并在启动时自动重新连接，直到你将其移除为止。它不会在你的局域网中搜寻服务器。

## Rex iOS 客户端

Rex iOS 客户端自身不收集遥测数据。Apple 会为每个应用收集部分数据，且仅在你允许的情况下才会与 Superlogical 共享。

### 崩溃报告与分析数据

如果在**“设置”>“隐私与安全性”>“分析与改进”**中开启了**“与 App 开发者共享”**，Apple 会向我们发送：

- 崩溃报告，包含设备型号、iOS 版本、应用版本以及崩溃发生在 Rex 代码中的具体位置。
- 诊断数据，例如无响应卡死、启动缓慢，以及电池或磁盘高负荷使用情况。
- App Store 分析数据，例如使用会话数与活跃设备数。此数据会与其他用户的数据汇聚统计，无法识别到任何具体个人。

这些数据均不包含任何额外的应用特定元数据，例如你的服务器列表、名称、会话布局、终端内容等。它仅为所有 App Store 应用通用的常规应用数据。关闭**“与 App 开发者共享”**后，Apple 不会向我们发送其中的任何数据。

无论该设置如何，Apple 总是会报告 Rex 的下载次数，所有应用均是如此。

如果你使用 TestFlight 构建版本（预览发布版本），无论**“与 App 开发者共享”**设置如何，TestFlight 都会向我们发送崩溃报告以及你提交的任何反馈。这是 TestFlight 的固有要求。

### 更新

Rex iOS 客户端本身从不检查更新。App Store 或 TestFlight 会负责对其进行更新。

### 远程服务端

Rex iOS 客户端仅连接至你主动添加的服务器，与 Rex Mac 客户端的方式一致。它不会在你的局域网中搜寻服务器。

## Rex 服务端（全平台）

在默认设置下，Rex 服务端与 `rex` CLI 不会建立任何出站连接。

### 更新

服务端本身从不检查更新。在 Linux 上，系统的包管理器会从 Superlogical 的软件包仓库中将其与其他软件包一同更新。在 Nix 上，当你更新 flake 时会从 Superlogical 的服务器更新。在 Windows 上，WinGet 会检查 Superlogical 的 WinGet 源并从 Superlogical 的服务器下载，但仅在 `winget` 命令中指定 `--source rex` 时才会发生。

这些请求仅发送包管理器或 Nix 通常发送的内容，例如你的 IP 地址及其 User-Agent。

`winget list` 和 `winget upgrade` 通常会向各个源发送 PC 上已安装程序的产品代码、名称和发布者。Rex 的 WinGet 源声明不支持这些字段，因此 WinGet 会在搜索中排除这些信息，该源永远不会获悉你还安装了哪些软件。它仅根据 Rex 的发布版本列表返回响应，且不会记录接收到的搜索请求。

### 远程服务端

CLI 仅在你通过 `--server`、`REX_SERVER`、`rex home` 或 `rex hosts` 明确指定另一台服务器时，才会连接至该服务器。

### 内置 Tailscale

[内置 Tailscale](../linux/remote-access.md#内置-tailscale)在主动开启前处于关闭状态。开启后，服务端会运行其自身的 Tailscale 设备，该设备会像其他任何设备一样连接至 Tailscale：

- Tailscale 的协调服务器，用于登录并加入你的 tailnet。
- Tailscale 的中继服务器，以及你 tailnet 上的其他设备。
- 你的路由器，通过 UPnP、NAT-PMP 或 PCP 打开端口。
- Let's Encrypt，用于获取服务端的 HTTPS 证书。

该 Tailscale 设备还会向 Tailscale 上传其日志与客户端指标，如同 Tailscale 官方应用默认所做的那样。这些是关于连接本身的 Tailscale 日志，而非你的终端内容。如果你的 tailnet 管理员开启了网络流日志，这些日志也会发送至 Tailscale。[Tailscale 隐私政策](https://tailscale.com/privacy-policy)涵盖了此数据。这些数据均不会发送至 Superlogical。

### 机器自带的 Tailscale

在使用 Tailscale Serve 或 tailnet 地址时，Rex 仅通过本地套接字向机器上已安装的 Tailscale 询问当前连接者的身份，自身不会建立任何网络连接。
