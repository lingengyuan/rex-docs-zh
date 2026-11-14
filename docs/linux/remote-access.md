> 原文：https://www.superlogical.com/rex/docs/linux/remote-access
> 原文版本：3513256f910b（抓取于 2026-11-13）

# 远程访问

本文档介绍在安装并运行 Rex 服务端之后，如何从远程访问你的服务端。
在 Linux 或 FreeBSD 上，Rex 服务端默认仅在本机的 Unix 套接字上监听。在 Windows 上，它默认仅在只有账户所有者才能打开的命名管道上监听。

若要从另一台机器上的客户端连接你的服务端，必须配置网络监听器或通过 SSH 进行访问。本文档将逐一介绍各个选项及其详细配置。

**目前 Rex 仅根据连接方式建立信任关系**，因此除非网络层能够提供身份信息，否则服务端无法校验访问方的具体身份。这也是为什么服务端默认仅在本地监听，且下文介绍的每个监听器在准入控制方面都十分谨慎的原因。这只是一个短期过渡方案。我们正在规划完整的身份认证与授权系统，包括对现有 SSH 密钥的支持。

在此之前，我们推荐使用 [SSH](#ssh)。大多数机器已在运行 SSH 服务，它可以直接复用你现有的密钥，且服务端能够获取你的 SSH 登录身份，这也是 Rex 决定准入权限的依据。除 sshd 之外无需在网络上暴露其他监听端口。

| 监听器 | 前提条件 | 适用模式 | 能否识别调用方 |
| --- | --- | --- | --- |
| SSH | 对该机器的 SSH 访问权限 | 个人服务端与共享服务端 | 是 |
| 内置 Tailscale | Tailscale 账户 | 个人服务端与共享服务端 | 是 |
| Tailscale Serve | 机器上已安装 Tailscale | 共享服务端与登录服务端 | 是 |
| Tailnet 地址 | 机器上已安装 Tailscale | 共享服务端与登录服务端 | 是 |
| 明文 HTTP | `--allow-anonymous` | 所有模式 | 否 |
| 其他 VPN | `--allow-anonymous` | 所有模式 | 否 |

## SSH

几乎每台联网机器上都已安装了 SSH，你可以直接使用现有的 SSH 凭据连接到 Rex。这是远程访问 Rex 的推荐首选方案。

你可以使用 `ssh://` 地址通过 SSH 连接到服务端。Rex 会优先调用系统自带的 `ssh` 命令，因此它可以直接使用你自有的密钥、代理（agent）和配置文件等：

```sh
rex -S ssh://alice@build.example.com ls
rex hosts add build ssh://alice@build.example.com
```

地址格式为 `ssh://[USER@]HOST[:PORT][/SOCKET]`。若未指定套接字路径，Rex 会查找该 SSH 用户的个人服务端，若未在运行则会自动启动它。若目标机器上设置了 `REX_AUTOSTART=0`，Rex 将不会通过 SSH 自动启动服务端。

在 Linux 上，个人服务端的套接字会在你注销登录时被清理，**这会终止你所有正在运行的会话。** 请使用 `loginctl enable-linger` 启用驻留以防止此情况发生。

为了确保 SSH 能够正常工作，`rex` 必须位于 SSH 连接的 PATH 中，或位于 `~/.local/bin` 中（非特权用户的安装路径正是此处，因此我们会显式进行检查）。

## 内置 Tailscale

携带 `--tailscale` 启动时，服务端会作为独立设备加入你的 tailnet，整个过程使用内置于 Rex 中的 Tailscale。目标机器本身无需安装 Tailscale。

```sh
rex server start --tailscale
```

首次运行时，服务端需要登录 Tailscale。其登录链接会显示在 `rex server status` 以及服务端的日志中。若要在无浏览器环境下完成登录，可通过 `--tailscale-auth-key-file FILE` 传入一次性认证密钥，或传入 `-` 以从标准输入读取。服务端会持久保存其登录凭据，因此仅需使用一次该密钥。

除非通过 `--tailscale-hostname` 指定其他名称，否则该设备默认命名为 `rex`。其访问地址为 `https://rex.<tailnet>.ts.net`。你的 tailnet 必须开启 MagicDNS 和 HTTPS 证书功能。

若要将其作为带有标签的设备登录，请添加 `--tailscale-advertise-tag tag:NAME`。带有标签的设备没有归属所有者，因此还需要搭配 `--tailscale-allow-tailnet-members`，详见[访问权限控制](#访问权限控制)。

在 Windows 上，必须在 `--` 之后将这些选项传递给 `rex server install`。Windows 服务没有标准输入，因此请以文件形式提供认证密钥：

```powershell
rex server install -- --tailscale --tailscale-auth-key-file C:\Users\alice\ts-key.txt
```

## Tailscale Serve 服务

如果机器上已在运行 Tailscale，Tailscale Serve 可以将 HTTPS 连接转发至 Rex 监听的套接字。这是访问共享服务端或登录服务端的常用方式。

运行 `sudo systemctl edit rex.service`（或 `rex-login-server.service`），在其命令行中添加该套接字。软件包升级会保留该文件。针对共享服务端：

```ini
[Unit]
After=tailscaled.service
Requires=tailscaled.service

[Service]
ExecStart=
ExecStart=/usr/bin/rex server run --listen /run/rex/server.sock \
  --state-dir /var/lib/rex --socket-mode 0660 --log-format text \
  --extra-listen tailnet-serve:///run/rex/serve.sock
```

针对登录服务端，其命令行如下：

```ini
ExecStart=
ExecStart=/usr/bin/rex login-server --listen unix:///run/rex/login-server.sock \
  --accounts /etc/rex/accounts.jsonc --runtime-root /run/rex --log-format text \
  --pam-service rex-login-server --extra-listen tailnet-serve:///run/rex/serve.sock
```

在 Alpine 上，请在 `/etc/conf.d/rex`（或 `/etc/conf.d/rex-login-server`）中将 `command_args` 设置为相同的命令行（无需包含 `/usr/bin/rex`）。使用 `rc_need` 代替 `After=` 与 `Requires=`。针对共享服务端：

```sh
command_args="server run --listen /run/rex/server.sock \
  --state-dir /var/lib/rex --socket-mode 0660 --log-format text \
  --extra-listen tailnet-serve:///run/rex/serve.sock"
rc_need="tailscale"
```

在 FreeBSD 上，将该套接字追加至 `rex_flags`（或 `rex_login_server_flags`），随后重启服务。其套接字位于 `/var/run/rex` 中：

```sh
sysrc rex_flags="--extra-listen tailnet-serve:///var/run/rex/serve.sock"
service rex restart
```

然后将 Tailscale Serve 指向该套接字：

```sh
sudo tailscale serve --bg --https=443 unix:/run/rex/serve.sock
```

在 FreeBSD 上，路径对应为 `unix:/var/run/rex/serve.sock`。

访问地址为该机器自身的 tailnet 主机名，例如 `https://build.<tailnet>.ts.net`。

Tailscale Serve 不会向 Rex 传递带有标签的设备的身份信息，因此 CI runner 等标签设备无法通过此种方式连接。对于此类设备，请改用 tailnet 地址。

**Serve 套接字必须使用 `tailnet-serve://`，绝不能使用 `unix://`。** 若使用 `unix://`，服务端虽然可以正常启动且不报错，但会将所有来自 tailnet 的调用方均视为运行 tailscaled 的账户（通常为 root）。

### 套接字激活服务端

搭配 `rex.socket` 或 `rex-login-server.socket` 时，上述 drop-in 配置无需修改即可使用，但服务端仅在其运行之后才会创建 Serve 套接字，因此通过 Tailscale Serve 发起的请求无法直接触发其启动。若要允许按需启动，请将 Serve 套接字同时添加至套接字单元中。运行 `sudo systemctl edit rex.socket`（或 `rex-login-server.socket`）并添加：

```ini
[Socket]
ListenStream=/run/rex/serve.sock
```

在服务单元的 drop-in 中保留 `--extra-listen` 选项。然后停止这两个单元并重新启动套接字，以便 systemd 创建新套接字：

```sh
sudo systemctl stop rex.socket rex.service
sudo systemctl start rex.socket
```

对于登录服务端，对应的单元为 `rex-login-server.socket` 与 `rex-login-server.service`。Serve 套接字会继承套接字单元的权限模式，Tailscale Serve 仍能正常访问它，因为 tailscaled 通常以 root 身份运行。详见[自定义套接字](shared-server.md#自定义套接字)。

## Tailnet 地址

服务端也可以直接在机器的 tailnet 地址上监听，利用机器自身的 Tailscale 来识别调用方身份。按照上文配置 Serve 套接字相同的方式，将以下选项添加至服务端的命令行：

```sh
--extra-listen tailnet://:7297
```

端口号不可省略。该连接为由 Tailscale 加密的明文 HTTP 连接，访问地址为 `http://build.<tailnet>.ts.net:7297`。

## 访问权限控制

**与服务端的连接能够执行该服务端所能执行的任何操作，** 包括以其账户身份启动程序。请务必谨慎管理访问权限。

对于个人服务端或共享服务端，默认仅允许拥有该机器（或在使用内置 Tailscale 时拥有该 Rex 设备）的 Tailscale 用户接入。若要允许其他人员接入：

| 监听器 | 选项 | 允许接入的对象 |
| --- | --- | --- |
| 内置 Tailscale | `--tailscale-allow-tailnet-members` | 你的 ACL 所允许的 tailnet 上的任何人 |
| Serve 或 tailnet 地址 | `--tailnet-allow-identified` | Tailscale 能够识别其身份的任何人 |

带有标签的机器或设备没有归属所有者，因此需要上述选项之一才能允许任何连接接入。

登录服务端则有所不同。由于其[账户文件](login-server.md#账户文件)决定了每个人获准使用的具体账户，因此它默认接纳 Tailscale 能够识别身份的所有人员。

若要查看当前连接至服务端的用户，可在服务端上运行 `rex client ls`。其 `principal` 列显示了各个客户端的身份标识。

## 明文 HTTP

明文 HTTP 监听器无法区分调用方的身份，因此除非同时传递 `--allow-anonymous`，否则 Rex 会拒绝启动该监听器：

```sh
rex server start --extra-listen :7297 --allow-anonymous
```

**此时所有连接均拥有完整访问权限。** 请仅在完全受控的网络环境中执行此操作。登录服务端仅允许此类调用方使用主体中包含 `anonymous` 的账户，且绝不允许使用 root。

需要再次强调，在开放网络中这样做**极度危险**，通常不应采用此方案。提供该选项的目的是便于与能够限制访问来源的网络配合使用，例如[自建 VPN](#自建-vpn)。

## 自建 VPN

你可以使用任何网络设备或自定义 VPN，例如 WireGuard、ZeroTier、NetBird 等。为此，请直接在正确的网络设备上进行监听：

```sh
rex server start \
  --extra-listen http://10.0.0.5:7297 --allow-anonymous
```

请指定 VPN 自身的 IP 地址。如果不包含主机地址（例如 `:7297`），则会在该机器拥有的每个网络地址上监听，包括其连接的其他网络。

**所有能够访问该地址的人都拥有完整权限。** Rex 无法区分不同的调用方，因此任何人都可以执行服务端所能执行的一切操作，包括以其账户身份启动程序。在私有 VPN 上，这意味着 VPN 上的所有人以及本机上的所有账户均拥有该权限。如果你的 VPN 支持访问控制规则，请使用这些规则限制哪些设备能够访问该端口。登录服务端对此类调用方的限制如[明文 HTTP](#明文-http) 中所述。

该监听器依赖于 VPN 处于就绪状态。若服务端无法在指定地址上监听，它将完全无法启动，甚至连其 Unix 套接字也不会开启。因此，请将这些选项写入服务的命令行中（如 [Tailscale Serve 服务](#tailscale-serve-服务)中所述），而不要依赖 `rex server start`，因为后者不会持久保存其选项，也不会修改已在运行的服务端。systemd 与 FreeBSD 每 5 秒会重试一次，因此在 VPN 连接建立后不久，服务端便会恢复运行。

若要连接，请在已连接该 VPN 的设备上将 `http://10.0.0.5:7297` 添加为主机。某些设备一次只能运行一个 VPN，因此开启另一个 VPN（包括 Tailscale）会导致 Rex 断开连接。

## 将服务端添加至客户端

在 Mac 版 Rex 中，选择 **Add Remote Host…**（添加远程主机）并输入服务端的地址。

在命令行中，可以通过 `-S` 传递该地址，或者将其保存为主机并使用其标签：

```sh
rex -S https://build.example.ts.net ls
rex hosts add build https://build.example.ts.net
rex -S build ls
```

纯主机名（例如 `build.example.ts.net`）会依次尝试 443 端口上的 HTTPS、7297 端口上的 HTTPS 以及 7297 端口上的 HTTP。

若要以特定账户连接到登录服务端，请将账户名放在主机名之前，例如 `https://root@build.example.ts.net`，详见[选择账户](login-server.md#选择账户)。

**注意：目前的 `rex hosts` 仅供 CLI 使用。** 它不会同步到图形界面客户端，也不会在机器之间同步。这一机制在未来会有所改进。

## NixOS 系统

NixOS 模块为各个监听器提供了对应的配置选项：

| 选项 | 配置内容 |
| --- | --- |
| `services.rex.tailscale.enable` | 内置 Tailscale，包含 `hostname`、`authKeyFile` 和 `advertiseTags` |
| `services.rex.tailscaleServe.enable` | 针对共享服务端的 Tailscale Serve |
| `services.rex.loginServer.tailscaleServe.enable` | 针对登录服务端的 Tailscale Serve |
| `services.rex.allowAnonymous` | 针对共享服务端的明文 HTTP。`openFirewall` 会开放其 `port`。 |
| `services.rex.loginServer.allowAnonymous` | 针对登录服务端的明文 HTTP 监听器 |

在开启 `socketActivation` 时，该模块的套接字单元还会同时容纳 Serve 套接字，因此通过 Tailscale Serve 发起的请求可以直接启动服务端。

## Windows

在 Windows 上，各个监听器的支持情况如下：

| 监听器 | 在 Windows 上的支持情况 |
| --- | --- |
| SSH | 支持，需搭配 Microsoft 的 OpenSSH Server。详见[在 Windows 上使用 SSH](#在-windows-上使用-ssh) |
| 内置 Tailscale | 支持，需搭配 `--tailscale` |
| Tailscale Serve | 不支持，同理也不支持 `login-server://` |
| Tailnet 地址 | 支持，需通过带有正常网络适配器的 `tailscaled`。若使用用户态 `tailscaled` 则不支持 |
| 明文 HTTP | 支持，需搭配 `--extra-listen` 与 `--allow-anonymous` |
| 其他 VPN | 支持，需搭配 `--extra-listen` 与 `--allow-anonymous` |

若要在每次服务端启动时保留这些监听器，请在 `--` 之后将它们传递给 `rex server install`（可选择携带或不携带 `--user`）：

```powershell
rex server install -- --tailscale
rex server install -- --extra-listen http://10.0.0.5:7297 --allow-anonymous
```

`rex server start` 支持相同的选项，但这些选项仅持续有效至服务端停止运行为止。详见[服务端启动标志](../windows/running.md#服务端启动标志)。

### 在 Windows 上使用 SSH

[SSH](#ssh) 需要安装并配置 Microsoft 的 OpenSSH Server。在通过**以管理员身份运行**启动的终端中执行：

```powershell
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Set-Service sshd -StartupType Automatic
Start-Service sshd
```

其防火墙规则仅允许在网络类型设置为“专用”（Private）时接入 SSH。对于管理员账户，sshd 从 `C:\ProgramData\ssh\administrators_authorized_keys` 读取密钥，而非从 `~\.ssh\authorized_keys` 读取。

### 防火墙

当由你启动的服务端首次在 TCP 端口上监听时，Windows 安全中心会针对 Rex Server 提示“是否允许公用网络和专用网络访问此应用？”。请选择**允许**。

**点击“取消”会导致该端口保持阻止状态。** 一旦该提示出现，Windows 便会添加名为 “Rex Server” 的阻止规则，点击“取消”会保留这些规则。后续再次启动时将不再弹出提示，且连接会超时。若要撤销该设置，请前往 **Windows 安全中心 > 防火墙和网络保护 > 允许应用通过防火墙** 并允许 Rex Server，或者在通过**以管理员身份运行**启动的终端中删除这些规则：

```powershell
Remove-NetFirewallRule -DisplayName "Rex Server"
```

**Windows 服务需要手动配置。** 由于后台运行时可能没有用户登录以查看提示，因此 Windows 会在没有提示的情况下直接阻止其端口，且不会添加任何规则。请在通过**以管理员身份运行**启动的终端中预先放行 `rex.exe`：

```powershell
New-NetFirewallRule -DisplayName "Rex Server" -Direction Inbound `
  -Program "C:\Program Files\Rex Server\rex.exe" -Action Allow
```

若使用 WinGet zip 安装，请使用 `(Get-Command rex).Source` 输出的实际路径。针对相同路径的阻止规则优先级高于此放行规则，因此若存在阻止规则，请先将其删除。

每条规则仅针对 `rex.exe` 的特定路径生效。切换至其他 WinGet 通道，或者在 WinGet zip 与 MSI 之间切换，都会改变 `rex.exe` 的路径，因此需要重新放行。通过 MSI 进行升级则会保留其安装目录以及对应的防火墙规则。
