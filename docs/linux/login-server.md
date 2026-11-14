> 原文：https://www.superlogical.com/rex/docs/linux/login-server
> 原文版本：200e6a2ef404（抓取于 2026-11-13）

# 登录服务端

登录服务端允许多人在一台机器上使用 Rex，每个人均以其自有的操作系统账户运行，拥有各自独立的文件与权限。当用户之间不宜共用同一个账户时，应使用该[服务端模式](server-modes.md)。

**登录服务端仅适用于 Linux 和 FreeBSD。** 在 Windows 上，请参阅[在 Windows 上运行](../windows/running.md)。

**如果机器上只有你一个人使用 Rex，则不需要登录服务端。** 请改为阅读 [Linux](installation.md#快速入门) 或 [FreeBSD](../freebsd/installation.md#快速入门) 的快速入门，配置一个通过 SSH 访问的个人服务端。

**登录服务端不使用密码或密钥。** 它仅通过连接来源识别访问方身份，例如其 Tailscale 登录身份。任何能够以此种方式连接的人，均可使用账户文件中为其列出的所有账户。这只是一个短期过渡方案，我们已规划了完整的身份认证与授权系统（包括支持传统的 SSH 密钥），但在该系统就绪之前，我们建议配合 Tailscale 等工具使用。

## 工作原理

登录服务端以 root 权限运行，作为 `rex-login-server.service`。它也可以通过 `rex-login-server.socket` 在首个客户端连接时启动，详见[按需启动](#按需启动)。当客户端发起连接时：

1. 登录服务端识别调用方身份，例如通过其 Tailscale 登录名或本地用户 ID。
2. 检查 `/etc/rex/accounts.jsonc` 确认该调用方获准使用的账户，并选取其中一个。
3. 通过 PAM 为该账户开启一个登录会话（与控制台或 SSH 登录相同），并以该账户身份启动一个 Rex 服务端。如果已有服务端在运行，则直接复用该服务端。
4. 将连接转交至该服务端。

当登录服务端停止、重启或升级时，各账户的服务端会持续运行，因此会话能够在这三种情况下存活下来。升级后，各个账户的服务端会继续保持旧版本，直到其上的会话全部结束。详见[服务重启机制](upgrading.md#服务重启机制)。

在带有 systemd-logind 的机器上，某个账户的服务端与该用户的[个人服务端](server-modes.md#个人服务端)是同一个。用户在该机器上使用 `rex` 启动的会话，与从其他计算机启动的会话，均位于同一服务端上。

## 账户文件

`/etc/rex/accounts.jsonc` 列出了用户获准使用的账户以及允许使用每个账户的人员。该文件采用 JSON 格式，支持注释和行尾逗号。文件初始为空，默认不接纳任何访问。

以下示例允许 Alice 使用其自有账户以及 root。除非显式请求 root，否则她默认以 `alice` 连接：

```jsonc
{
  "version": 1,
  "accounts": {
    "alice": { "principals": ["tailscale:alice@example.com"] },
    "root": { "principals": ["tailscale:alice@example.com"] },
  },
  "defaults": { "tailscale:alice@example.com": "alice" },
}
```

在 `accounts` 下，每个键代表一个账户名，`principals` 列出了获准使用该账户的调用方。如果调用方匹配其中任何一个主体，即可使用该账户：

| 主体 | 匹配规则 |
| --- | --- |
| `tailscale:alice@example.com` | 通过 Tailscale 登录名匹配个人身份 |
| `tailscale:tag:ci` | 带有 Tailscale 标签 `tag:ci` 的设备 |
| `tailscale:*` | tailnet 上的任何人员 |
| `tailscale:tag:*` | 任何带有标签的设备 |
| `peer:1000` | 通过用户 ID 匹配本地用户 |
| `identified` | Rex 能够识别其身份的任何调用方 |
| `anonymous` | Rex 无法识别身份的调用方，例如在明文 TCP 监听器上 |

带有标签的设备绝不会匹配个人登录名或 `tailscale:*`。

### 任意账户

特殊账户 `"*"` 允许其调用方使用任何常规账户（即用户 ID 为 1000 或更高的任意账户），无论该账户是否在文件中显式命名。Root 账户和系统账户则必须始终在文件中按名称列出。

```jsonc
{
  "version": 1,
  "accounts": {
    "*": { "principals": ["tailscale:*"] },
  },
}
```

出于安全考量，`anonymous` 不能出现在 `"*"` 下，且匿名调用方绝不能使用 root。

### 默认值

当客户端未请求特定账户时，`defaults` 会为其选取一个账户。默认值仅用于选择账户，调用方仍必须获准使用该账户。

如果有多个默认值与调用方匹配，最具体的规则优先胜出：登录名或用户 ID 优先级最高，其次是标签，然后是 Tailscale 通配符，接着是 `identified`，最后是 `anonymous`。在具体程度相同的匹配项之间，文件中靠前的项胜出。

在没有匹配的默认值时，如果调用方仅获准使用一个账户，则以该账户连接。否则，客户端必须显式指定其希望使用的账户。

## 启动与重新加载

添加至少一个账户以供用户访问，然后启动服务：

```sh
sudo $EDITOR /etc/rex/accounts.jsonc
sudo systemctl enable --now rex-login-server.service
```

这会立即启动服务并设置为开机自启。在 Alpine 上，请改用 [OpenRC 命令](installation.md#alpine-发行版)；在 FreeBSD 上，请使用 [FreeBSD 命令](../freebsd/installation.md#命令与路径)。

每当修改账户文件后，重新加载服务端：

```sh
sudo systemctl reload rex-login-server.service
```

在 Alpine 上，运行 `rc-service rex-login-server reload`。在 FreeBSD 上，运行 `service rex-login-server reload`。

重新加载不会中断仍然获准的连接。它会关闭访问权限已被移除的连接，但会保留各账户的服务端及其会话持续运行。journal 会显示 `account policy reloaded`，如果新文件存在错误，则会显示 `account policy reload failed; previous policy retained`。

软件包升级会保留你对账户文件的修改。登录服务端的日志记录在 journal 中：

```sh
journalctl -u rex-login-server.service
```

Alpine 没有 journal，因此日志保存在 `/var/log/rex-login-server.log` 中。在 FreeBSD 上，日志保存在 `/var/log/messages` 中，详见 [FreeBSD](#freebsd)。

登录服务端仅在 `/run/rex/login-server.sock` 上监听，该套接字仅供 root 使用。若要允许他人从其他计算机连接，请参阅[远程访问](remote-access.md)。

## 按需启动

Rex 可以配合 systemd 使用，在客户端首次连接时自动启动登录服务端，而非在开机时通过 `rex-login-server.socket` 启动。

启用此项后，systemd 会创建 `/run/rex/login-server.sock` 并等待。当客户端发起连接时，systemd 会启动 `rex-login-server.service` 并将套接字移交给它。客户端在登录服务端启动时会稍作等待，随后照常工作。该套接字仅供 root 使用，与登录服务端自行创建时一致。

添加至少一个账户，然后启用套接字单元而非服务单元：

```sh
sudo $EDITOR /etc/rex/accounts.jsonc
sudo systemctl enable --now rex-login-server.socket
```

请二选一启用，切勿同时启用两者。套接字单元会在需要时自行启动服务。在首个客户端发起连接之前，`systemctl status rex-login-server.socket` 会显示为 “active (listening)”。

套接字处于激活状态时，任何连接都会触发启动登录服务端，包括 `rex server status`。若要在不触发启动的情况下检查其状态，请运行 `systemctl status rex-login-server.service rex-login-server.socket`。

按照上述相同方式重新加载账户文件。在尚无客户端连接之前，登录服务端并未在运行，因此重新加载会执行失败。此时无需进行额外操作：登录服务端会在启动时读取新文件。

如果账户文件缺失或无效，登录服务端会退出并输出 `loading accounts file:` 及具体原因，并在 5 秒后再次尝试启动。与此同时，客户端不会立刻被拒绝连接，而是各自等待直到其 `--timeout` 耗尽（默认 10 秒）。journal 会显示具体原因。

单独停止 `rex-login-server.service` 只能生效至下一次连接到来。若要停止登录服务端并保持停止状态，请在单条命令中同时停止这两个单元：

```sh
sudo systemctl stop rex-login-server.socket rex-login-server.service
```

若仅停止套接字，会导致登录服务端在缺少套接字文件的情况下继续运行，从而使新的连接无法建立。无论何种情况，各账户的服务端及其会话均会持续运行。一旦登录服务端恢复运行，客户端即可重新连接它们。

若要切换为始终运行的登录服务端，请先禁用这两个单元，然后启用服务单元：

```sh
sudo systemctl disable --now rex-login-server.socket rex-login-server.service
sudo systemctl enable --now rex-login-server.service
```

若要切换回来，请先停止服务。在登录服务端运行期间，systemd 无法接管套接字的监听：

```sh
sudo systemctl disable --now rex-login-server.service
sudo systemctl enable --now rex-login-server.socket
```

若要修改套接字，请运行 `sudo systemctl edit rex-login-server.socket`。其中的每个 `ListenStream=` 都需要在登录服务端的命令行中有与之匹配的选项。其运作机制与共享服务端相同，详见[自定义套接字](shared-server.md#自定义套接字)。若要通过 Tailscale Serve 发起的请求也能启动登录服务端，请参阅 [Tailscale Serve](remote-access.md#tailscale-serve-服务)。

Alpine 和 FreeBSD 不支持套接字激活。在 NixOS 上，请设置 `services.rex.loginServer.socketActivation`，详见 [NixOS 系统](#nixos-系统)。

## 选择账户

若要请求特定账户，请在服务端地址的主机名之前加上账户名：

```sh
rex -S root@build.example.ts.net ls
```

相同的地址格式也适用于 Mac 版应用中的 **Add Remote Host…**（添加远程主机）。若地址中未包含账户名，则应用调用方的默认配置。

账户只能在 `https://` 或 `http://` 地址中选择，因此登录服务端首先需要一个网络监听器。[远程访问](remote-access.md)涵盖了如何配置网络监听器以及如何以各个账户身份连接。

## PAM

登录服务端每次为账户启动服务端时都会使用 PAM。PAM 决定该账户是否获准登录（例如是否已锁定或已过期），并建立登录会话：资源限制、环境变量，以及在支持的机器上建立 systemd-logind 会话。

在 PAM 运行之前，Rex 已识别了调用方身份，因此其策略绝不会要求输入密码，这与使用密钥的 SSH 相同。当 `/etc/nologin` 存在时，仅允许 root 登录。shell 为 `nologin` 或 `false` 的账户始终会被拒绝。

软件包会安装适合你所用发行版的策略文件 `/etc/pam.d/rex-login-server`：适用于 Debian 与 Ubuntu、Red Hat 及其衍生版本、SUSE 或 Alpine。升级会保留对该文件的修改。FreeBSD 则有所不同，详见 [FreeBSD](#freebsd)。

若要跳过 PAM，运行 `sudo systemctl edit rex-login-server.service` 并将服务的命令行替换为追加了 `--pam=false` 的命令。此时 Rex 会自行检查 `/etc/shadow` 与 `/etc/nologin`，且不会建立登录会话。

在 Alpine 上，请在 `/etc/conf.d/rex-login-server` 中设置 `command_args`，填入追加了 `--pam=false` 的服务命令行：

```sh
command_args="login-server --listen unix:///run/rex/login-server.sock \
  --accounts /etc/rex/accounts.jsonc --runtime-root /run/rex --log-format text \
  --pam-service rex-login-server --pam=false"
```

## NixOS 系统

NixOS 模块通过 `services.rex.loginServer.accounts` 与 `services.rex.loginServer.defaults` 写入账户文件。该模块不会创建系统账户，因此请通过 `users.users` 声明它们：

```nix
{
  users.users.alice.isNormalUser = true;

  services.rex.loginServer = {
    enable = true;
    accounts.alice.principals = [ "tailscale:alice@example.com" ];
  };
}
```

若要保留 `defaults` 的顺序（用于在规则冲突时决胜），请改用 `services.rex.loginServer.accountsFile` 加载自有的账户文件。

若要仅在首个客户端连接时启动登录服务端，请设置 `services.rex.loginServer.socketActivation = true;`。若要停止并保持停止状态，请同时停止 `rex-login-server.socket` 与 `rex-login-server.service`。详见 [NixOS 模块](installation.md#nixos-模块)。

## FreeBSD

在 FreeBSD 上，账户文件路径为 `/usr/local/etc/rex/accounts.jsonc`，并通过 [FreeBSD 命令](../freebsd/installation.md#命令与路径)启动和重新加载服务。登录服务端将日志输出至 syslog 中的 `/var/log/messages`。各个账户的服务端则将日志写入 `/var/run/rex/accounts/<account>/server.log`，使用该账户的人员也可以读取这些日志。

软件包将其 PAM 策略安装至 `/usr/local/etc/pam.d/rex-login-server`，且**每次升级都会将其替换**。若要修改规则，请将其复制到 `/etc/pam.d` 并在该副本中编辑。OpenPAM 会优先读取 `/etc/pam.d`，且升级绝不会改动该目录：

```sh
install -o root -g wheel -m 0644 /usr/local/etc/pam.d/rex-login-server \
  /etc/pam.d/rex-login-server
$EDITOR /etc/pam.d/rex-login-server
```

OpenPAM 会忽略属主不是 root 的策略文件，因此请保持该副本的属主为 root。

该策略以与 sshd 相同的方式检查账户。通过 `pw lock` 锁定的账户会被拒绝登录，`/etc/login.access` 规则生效，且当 `/var/run/nologin` 存在时仅允许 root 登录。Rex 会将 `/etc/login.conf` 中各个账户的登录类别（例如资源限制）应用到其服务端上。

若要跳过 PAM，请在 `rex_login_server_flags` 中追加 `--pam=false`，然后重启服务：

```sh
sysrc rex_login_server_flags="--pam=false"
service rex-login-server restart
```

随后 Rex 会自行检查 `/etc/master.passwd` 与 `/var/run/nologin`。
