> 原文：https://www.superlogical.com/rex/docs/windows/installation
> 原文版本：ec7708acea08（抓取于 2026-11-18）

# 在 Windows 上安装

Rex 可以在 Windows 上作为服务端运行，以便客户端将其作为远程主机访问。

**重要提示：** Windows 版 Rex 目前处于测试阶段，仅向 Discord 中拥有 Windows 角色的测试者开放。我们很快会将测试范围扩大至更多人员。

在 Windows 上，所有服务端均为以你自有账户运行的个人服务端。你可以配置 Rex 服务端随系统开机启动或随用户登录启动，详见[在 Windows 上运行](running.md)。[服务端模式](../linux/server-modes.md)、[共享服务端](../linux/shared-server.md)和[登录服务端](../linux/login-server.md) *不适用于 Windows*。

## 系统要求

| 要求 | 支持情况 |
| --- | --- |
| 发行版本 | Windows 10 1809 或更高版本 |
| 架构 | x86-64、ARM64 |
| 软件包格式 | WinGet、MSI 或 Zip |

## 安装

Rex 目前尚未进行代码签名，因此在测试阶段，Windows 可能会提示发布者未知。

每种安装方式都会安装 `rex.exe` 并将其添加至 PATH 中，但**不会自动启动服务端或安装 Windows 服务。** 在安装 Rex 之后，必须使用 `rex server install` 手动执行此操作。

请选择一种安装方式。推荐使用 WinGet。

<span id="winget"></span>**WinGet**

添加 Rex WinGet 源需要管理员权限，因此请在通过**以管理员身份运行**打开的终端中执行第一行命令。

<span id="msi"></span>**MSI**

MSI 会为机器上的所有账户安装 Rex 至 `%ProgramFiles%\Rex Server`，并将该文件夹添加至系统 PATH 中。该方式需要管理员权限。

上方提供的下载为 x86-64 MSI。在 ARM64 上，请使用 [WinGet (MSI)](#winget-msi) 或 [zip](#zip)。打开 MSI 即可运行其安装向导，或者在通过**以管理员身份运行**打开的终端中执行静默安装：

```powershell
msiexec /i rex-windows-amd64.msi /qn
```

若要安装至 `%ProgramFiles%\Rex Server` 之外的其他位置，请添加 `INSTALLDIR="D:\Tools\Rex Server"`。

<span id="zip"></span>**Zip**

Zip 包含 Rex 的所有文件，无需安装程序。

拥有 Windows 角色的测试者可在此处获取下载。

如果使用 Zip，需要自行将其移动至合适位置并将 `rex.exe` 添加到 `PATH` 中。

安装完成后，`rex` 会位于你的 `PATH` 中。PATH 的变动仅对新打开的终端生效，因此请打开新的终端进行检查。

## 通道

Rex 面向三个通道发布，每个通道均有独立的 WinGet 软件包：

| 通道 | 软件包 | 包含内容 |
| --- | --- | --- |
| `stable` | `Superlogical.RexServer` | 正式发布的稳定版 |
| `preview` | `Superlogical.RexServer.Preview` | 下一个发布版本的带标签预览版 |
| `snapshot` | `Superlogical.RexServer.Snapshot` | 开发构建版 |

安装命令默认使用 `preview`。在首个稳定版发布之前，`winget install Superlogical.RexServer` 会执行失败，因为 WinGet 会将尚无发布版本的通道视作不存在的软件包。

若要切换通道，请先按照[卸载 Rex](#卸载-rex) 中的说明卸载当前软件包，随后携带 `--source rex` 安装另一个通道的软件包。

## 软件包内容

所有软件包均包含相同的文件集：

| 文件 | 说明 |
| --- | --- |
| `rex.exe` | 服务端与 CLI 二进制文件，两者合二为一 |
| `OpenConsole.exe` | 来自 Windows Terminal 的控制台宿主程序 |
| `LICENSE-OpenConsole.txt` | `OpenConsole.exe` 的许可证文件 |

不同的安装方式会将它们放置在各自对应的文件夹中：

- **WinGet** 将其放在 `%LocalAppData%\Microsoft\WinGet\Packages` 下以 `Superlogical.RexServer.Preview_` 开头的文件夹中，并将该目录添加至用户 PATH。
- **MSI** 将其放在 `%ProgramFiles%\Rex Server` 中，并将该目录添加至系统 PATH。
- **Zip** 将其留在你解压的目标文件夹中。请自行将该文件夹添加至用户 PATH。

## 卸载 Rex

**在卸载软件包之前，请先运行 `rex server uninstall`。** 否则 `rex server install` 创建的 Windows 服务或登录启动项仍会指向已被删除的 `rex.exe`。移除该服务需要在通过**以管理员身份运行**打开的终端中执行。

卸载软件包不会停止正在运行的服务端，因此请先使用 `rex server stop` 将其停止。然后卸载软件包。对于 zip 安装方式，请使用普通终端执行卸载，因为 WinGet 无法在通过**以管理员身份运行**打开的终端中卸载它：

```powershell
winget uninstall --id Superlogical.RexServer.Preview --source rex
```

对于自行手动安装的 MSI，请在**添加或删除程序**中卸载 “Rex Server”。

对于 zip 安装方式，直接删除其文件夹并从你的用户 PATH 中移除对应路径即可。

WinGet 在卸载 zip 软件包后会将其文件夹路径遗留在你的用户 PATH 中，即便该文件夹已被删除。你可以手动将其从 PATH 中清除。

你的配置文件 `%AppData%\rex\init.lua`，以及位于 `%LocalAppData%\rex` 中的 Rex 状态和日志会被保留。删除它们即可彻底清除 Rex 的所有痕迹。
