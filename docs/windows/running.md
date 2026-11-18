> 原文：https://www.superlogical.com/rex/docs/windows/running
> 原文版本：698be7b3fa8d（抓取于 2026-11-18）

# 在 Windows 上运行

在 Windows 上，每个 Rex 服务端只能登录为单一账户：
即安装该 Windows 服务的账户。
[服务端模式](../linux/server-modes.md)、
[共享服务端](../linux/shared-server.md) 与
[登录服务端](../linux/login-server.md) 仅适用于 Linux 和 FreeBSD，并不适用于 Windows。

## 快速入门

本节介绍快速搭建并运行的推荐配置。为了便于快速上手，本节刻意省略了许多关于系统运作细节的说明。建议深入阅读后续章节以全面了解相关机制。

1. 使用 WinGet 安装 Rex，详见[在 Windows 上安装](installation.md#winget)。

2. 在通过**以管理员身份运行**打开的终端中，安装并启动 Microsoft 的 OpenSSH Server：

   ```powershell
   Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
   Set-Service sshd -StartupType Automatic
   Start-Service sshd
   ```

3. 在同一个终端中，添加你的公钥（例如 `~/.ssh/id_ed25519.pub` 的内容）。对于管理员账户，sshd 从该文件读取公钥，且要求仅管理员拥有修改权限：

   ```powershell
   Add-Content C:\ProgramData\ssh\administrators_authorized_keys "ssh-ed25519 AAAA... alice@mac"
   icacls.exe C:\ProgramData\ssh\administrators_authorized_keys /inheritance:r /grant Administrators:F /grant SYSTEM:F
   ```

   对于标准用户账户，请改将公钥添加至 `~\.ssh\authorized_keys` 中。

4. 在 Mac 上连接该 PC（其中 `pc` 为其名称或 IP 地址）：

   ```sh
   rex -S ssh://alice@pc ls
   ```

   在 Mac 版 Rex 中，选择 **Add Remote Host…**（添加远程主机）并输入 `ssh://alice@pc`。

首次连接会启动你的服务端，在你将其停止前它会持续运行。Windows 仅允许在设置为“专用”（Private）的网络上接入 SSH。关于 Tailscale 以及其他连接方式，请参阅[远程访问](../linux/remote-access.md#windows)。

## 服务端生命周期

以何种方式运行或安装服务端，决定了它能够保持运行的时长：

| 启动方式 | 何时启动 | 运行持续时长 | 是否需要管理员权限 |
| --- | --- | --- | --- |
| 任意 `rex` 命令 | 执行命令时 | 持续至最后一个客户端断开后约 10 秒 | 否 |
| `ssh://` 连接 | 客户端建立连接时 | 持续运行直到主动停止 | 否 |
| `rex server start` | 立即启动 | 持续运行直到主动停止或注销登录 | 否 |
| `rex server install --user` | 每次用户登录时 | 持续运行直到注销登录 | 否 |
| `rex server install` | 开机时作为 Windows 服务启动 | 持续运行直到系统关机（无论用户是否登录） | 是 |

如果你仅在 PC 本机前局部使用 Rex，直接让 `rex` 命令自动启动服务端即可。

若要从远程连接到 Rex，请通过 `rex server install` 设置为开机启动。如果无法获取管理员权限，请通过 `rex server install --user` 设置为随用户登录启动。

## CLI 触发的服务端

当没有服务端在运行时，任何 `rex` 命令都会自动启动一个服务端：

```powershell
rex ls
```

自动启动的服务端会在其最后一个会话和最后一个连接关闭约 10 秒后自行停止。若要启动一个持续运行直到主动停止或注销登录的服务端，请显式启动它：

```powershell
rex server start
```

`rex server status`、`rex server logs` 和 `rex server stop` 的工作方式与在 Linux 上相同，详见[个人服务端](../linux/server-modes.md#个人服务端)。

服务端在命名管道 `\\.\pipe\rex-<SID>` 上监听，其中 `<SID>` 为你账户的安全标识符。如果设置了 `REX_RUNTIME_DIR`，管道名称会追加后缀，因此使用不同运行目录的服务端不会发生冲突。

若要彻底禁止 `rex` 命令自动启动服务端，请设置 `REX_AUTOSTART=0`。

## 随系统开机启动

`rex server install` 会创建一个 Windows 服务，在系统开机时启动你的服务端，并在没有任何用户登录的情况下保持持续运行。请在通过**以管理员身份运行**打开的终端中执行：

```powershell
rex server install
```

该服务以你自有的账户身份运行，而非以 LocalSystem 运行。该命令在执行每项修改前都会打印说明：

- 创建服务 `RexServer-<SID>`，在服务控制台中显示为 “Rex Server (PC\alice)”。该服务被配置为**自动（延迟启动）**，并使用你配置的[服务端启动标志](#服务端启动标志)运行 `"<path to rex.exe>" server run`。
- 授予你的账户“作为服务登录”的权限。
- 将 “Rex Server” 注册为事件日志的事件来源。
- 如果此前添加了[随用户登录启动](#随用户登录启动)项，将其删除。

如果有服务端已在运行且当前无人使用，该命令会将其停止并在原位置启动服务。如果该服务端当前拥有会话或连接，它会继续运行，而服务会在下次开机时启动。命令会输出具体处理结果。

再次运行该命令是安全的，并且会保留已配置的服务端启动标志。在移动 `rex.exe` 的位置后（例如在 WinGet zip 与 MSI 之间切换），请重新运行该命令，以便服务使用新的路径运行。

## 随用户登录启动

`rex server install --user` 会在每次登录 Windows 时启动你的服务端，无需管理员权限：

```powershell
rex server install --user
```

它会在 `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` 中添加名为 “Rex Server” 的数值，使用你的[服务端启动标志](#服务端启动标志)运行 `rex server start`。如果当前没有服务端在运行，它还会立即启动一个服务端。服务端会在你注销登录时停止。

再次运行该命令是安全的，并且会保留已配置的服务端启动标志。

该启动项会显示在任务管理器的**启动应用**标签页中，以及系统“设置”的**应用 > 启动**中。如果在此处被禁用，Windows 会跳过该项，命令会提示此情况而不会强行将其重新启用。

登录启动项与 Windows 服务不能同时用于启动你的服务端。只要该服务存在，`rex server install --user` 就会执行失败。请先按照[移除服务](#移除服务)中的说明删除该服务。

## 服务端启动标志

`rex server tailscale on` 以及对正在运行的服务端所做的其他修改，仅能持续生效至服务端停止运行为止。若要在每次服务端启动时传递标志，请将它们置于 `--` 之后：

```powershell
rex server install -- --tailscale
rex server install --user -- --extra-listen tailnet://:7297
```

Windows 服务会携带这些标志运行 `server run`，而登录启动项会携带它们运行 `server start`。搭配 `--user` 时，命令立即启动的服务端同样会获取这些标志。`rex server run --help` 与 `rex server start --help` 列出了各自支持的标志。

再次运行该命令时 `--` 的具体行为如下：

| 命令 | 服务端启动标志 |
| --- | --- |
| `rex server install` | 保留已设置的标志 |
| `rex server install -- --tailscale` | 使用新标志替换旧标志 |
| `rex server install --` | 清除所有标志 |

搭配 `--user` 时也是如此。从 `--user` 迁移至 Windows 服务时，会将登录启动项的标志迁移至该服务。

该命令在进行任何修改前均会校验这些标志，并拒绝服务端不支持的标志。此外还会拒绝以下标志，因为它们不适用于由 Windows 启动的服务端：

| 标志 | 原因 |
| --- | --- |
| `--listen` | `rex` 命令通过命名管道寻找服务端。添加网络端点请使用 `--extra-listen`。 |
| `--exit-empty` | 服务在空闲后会自动停止，且 Windows 直到下次开机才会再次启动它。 |
| `--tailscale-auth-key-file -` | Windows 不为服务端提供标准输入。请提供文件路径。 |

已在运行的服务端会继续保持其旧标志直到重启，详见[停止与重启](#停止与重启)。`rex server start` 不会读取登录启动项中的配置，因此若要携带这些标志重启该服务端，请将其停止并重新运行 `rex server install --user`，或重新登录系统。

## 管理员权限

**由 Windows 服务启动的服务端在运行时不具备管理员权限，即便你的账户是管理员也是如此。** 服务在启动它时会使用其令牌的受限副本，因此每个终端、块插件和 `rex.exec` 程序的运行方式与正常登录时完全一致。

由 `rex server start` 或任何 `rex` 命令启动的服务端同样获取相同的受限权限，即便从通过**以管理员身份运行**打开的终端或管理员的 `ssh` 会话中启动也是如此。如果 Windows 无法生成受限令牌，服务端启动会失败。

**在通过“以管理员身份运行”打开的终端中执行 `rex server run` 会保留完整的管理员权限。** 在这种情况下，我们假定你明确需要该权限。

## 日志

无论服务端最初是以何种方式启动的（包括 Windows 服务），`rex server logs` 均可查看其日志：

```powershell
rex server logs --follow
```

日志文件位于 `%LocalAppData%\rex\servers` 中。Rex 会在日志大小超过 50MiB 之前将其清理。

Windows 服务还会以事件来源 “Rex Server” 向事件查看器中的“应用程序”日志写入记录：

| 事件 ID | 级别 | 含义 |
| --- | --- | --- |
| 1 | 信息 | 服务正在启动 |
| 2 | 信息 | 服务正在运行 |
| 3 | 信息 | Windows 请求服务停止 |
| 4 | 信息 | 服务已停止 |
| 5 | 错误 | 服务异常停止，事件内容中包含错误名称 |

## 停止与重启

无论服务端最初以何种方式启动，`rex server stop` 均可将其停止。这会终止其会话中运行的所有程序。服务端会保存其会话布局，一旦重新启动，`rex ls` 会再次列出它们：

```powershell
rex server stop
```

由服务启动的服务端在被停止后，会保持停止状态直到下次开机，或直到你主动将其启动。若要启动或停止该服务，请在通过**以管理员身份运行**打开的终端中执行：

```powershell
sc.exe start RexServer-<SID>
sc.exe stop RexServer-<SID>
```

也可以通过服务控制台进行操作，查找 “Rex Server (PC\alice)” 即可。服务停止时，会留给服务端 15 秒的时间保存会话并退出，随后将其终止。

在服务处于停止状态时，`rex` 命令可能会自行启动一个服务端，而 `sc.exe start` 在该服务端停止前会执行失败。若希望避免发生此情况，请设置 `REX_AUTOSTART=0`。

## 移除服务

`rex server uninstall` 会停止 Windows 服务（这会终止其会话中运行的所有程序），随后将其删除。请在通过**以管理员身份运行**打开的终端中执行：

```powershell
rex server uninstall
```

它还会注销作为事件日志来源的 “Rex Server”（除非其他账户的服务仍在继续使用它），并删除[随用户登录启动](#随用户登录启动)项。

一旦该服务存在，该命令即需要管理员权限，哪怕仅删除登录启动项也是如此。若服务不存在，则无需管理员权限，而由登录启动项启动的服务端会继续保持运行。你可以使用 `rex server stop` 将其停止。

你的账户会保留“作为服务登录”的权限，因为其他服务可能需要该权限。若要移除该权限，打开本地安全策略（`secpol.msc`），进入**本地策略 > 用户权限分配 > 作为服务登录**。

## 终端与 Shell

每个终端会优先运行服务端 PATH 上的 `pwsh.exe` 或 `powershell.exe`，若两者均不存在则运行 `%ComSpec%`。目前没有用于更改该默认设置的配置项。若要运行其他 shell，请将其作为命令传入：

```powershell
rex new -- cmd.exe
```

由 `rex` 命令、`rex server start` 或登录启动项启动的服务端仅向终端传递环境变量白名单：常见的 Windows 变量（例如 `USERPROFILE`、`APPDATA` 和 `ProgramFiles`）、通用工具链变量（例如 `JAVA_HOME` 和 `GOPATH`），以及 `PATH`、`REX_*`、`XDG_*`、`LC_*` 和代理变量。若要传递其他变量，请携带 `--env` 启动服务端：

```powershell
rex server start --env NAME --env OTHER=value
```

`--env` 仅在启动新服务端时生效。若要修改变量，请先停止服务端然后再重新启动。若要在每次登录时保持该变量设置，可将其作为[服务端启动标志](#服务端启动标志)传递给登录启动项：

```powershell
rex server install --user -- --env NAME
```

由 Windows 服务启动的服务端会获取该服务启动时 Windows 所拥有的系统和用户环境变量。在系统“设置”中新增的变量，会在该服务重启后传递至其终端。该服务会拒绝 `--env`，因为只有 `rex server start` 才支持该选项。

终端的 `TERM` 会被设置为 `xterm-256color`，且 `rex terminfo setup` 在 Windows 上会被拒绝执行。关闭终端会立即终止其中的所有进程。

## Windows 上不可用的功能

Rex 的以下功能需要 Unix 系统支持：

| 功能 | 在 Windows 上的对应情况 |
| --- | --- |
| 共享服务端与登录服务端 | 每个账户运行自有的独立服务端 |
| 通过套接字激活按需启动 | 任意 `rex` 命令均可启动服务端 |
| `--socket-mode` | 仅你自有的账户能够打开该管道 |
| `tailnet-serve://` 与 `login-server://` 监听器 | 通过 `rex server install -- --tailscale` 使用 Rex 自带的 Tailscale 节点 |
| 配合用户态 `tailscaled` 的 `tailnet://` | 需搭配使用正常网络适配器的 `tailscaled` |
| `rex terminfo setup` | 终端保持 `TERM=xterm-256color` |
| 面向 Windows PC 的 `rex server install ssh://` | 在 PC 上安装 Rex，随后通过 [`ssh://` 端点](../linux/remote-access.md#在-windows-上使用-ssh)访问 |
| 通过 `SIGHUP` 重新打开日志文件 | 使用 `rex server logs` 以及 50MiB 大小限制 |
