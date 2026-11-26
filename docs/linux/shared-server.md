> 原文：https://www.superlogical.com/rex/docs/linux/shared-server
> 原文版本：6fc9cc074496（抓取于 2026-11-26）

# 共享服务端

共享服务端是作为 `rex.service` 以 `rex` 系统账户运行的单个 Rex 服务端。`rex` 用户组的成员可以连接到该服务端，并且他们启动的每个程序均以 `rex` 身份运行。对于信任并愿意共用同一账户的少数几个人而言，这是最简单的[服务端模式](server-modes.md)。

**共享服务端仅适用于 Linux 和 FreeBSD。** 在 Windows 上，请参阅[在 Windows 上运行](../windows/running.md)。

**如果机器上只有你一个人使用 Rex，则不需要共享服务端。** 请改为阅读 [Linux](installation.md#快速入门) 或 [FreeBSD](../freebsd/installation.md#快速入门) 的快速入门，配置一个通过 SSH 访问的个人服务端。

**访问共享服务端等同于访问 `rex` 账户。** 该组中的任何人都可以查看并向其上的所有会话输入内容，并以 `rex` 身份启动程序。因此，只应添加你信任并愿意与之共享该账户的人员。如果各成员需要拥有独立的文件与权限，请改用[登录服务端](login-server.md)。

## 启动服务端

软件包在创建 `rex` 账户时将其 shell 设置为 `nologin`，而 Rex 启动每个终端时均使用对应账户的 shell。因此请先为该账户设置一个真实的 shell，否则共享服务端上的每个终端都会在启动后立即退出：

```sh
sudo usermod --shell /bin/bash rex
```

Alpine 默认既没有 `usermod` 也没有 bash。请通过 `shadow` 软件包安装 `usermod` 并使用 `/bin/sh`：

```sh
apk add shadow
usermod --shell /bin/sh rex
```

FreeBSD 默认同样没有 bash。在该系统上请使用 `pw` 和 `/bin/sh`：

```sh
pw usermod rex -s /bin/sh
```

该账户保持锁定状态且没有密码，因此任何人都无法以此种方式直接登录 `rex`。

然后立即启动该服务并设置为开机自启：

```sh
sudo systemctl enable --now rex.service
```

在 Alpine 上，运行 `rc-update add rex`，然后运行 `rc-service rex start`。在 FreeBSD 上，运行 `sysrc rex_enable=YES`，然后运行 `service rex start`。

若要仅在有人首次发起连接时才启动服务端，请改为启用 `rex.socket`。详见[按需启动](#按需启动)。

服务端在 `/run/rex/server.sock` 上监听，并将其数据保存在 `rex` 账户的主目录 `/var/lib/rex` 中。在 FreeBSD 上，对应路径分别为 `/var/run/rex/server.sock` 和 `/var/db/rex`。

## 按需启动

Rex 可以配合 systemd 使用，在客户端首次发起连接时自动启动共享服务端，而非在开机时通过 `rex.socket` 启动。

启用此项后，systemd 会创建 `/run/rex/server.sock` 并等待。当客户端发起连接时，systemd 会以相同的命令行启动 `rex.service` 并将套接字移交给它。客户端在服务端启动时会稍作等待，随后照常工作。访问权限规则保持不变：`rex` 用户组的成员可以使用该套接字。

启用套接字单元而非服务单元：

```sh
sudo systemctl enable --now rex.socket
```

请二选一启用，切勿同时启用两者。套接字单元会在需要时自行启动服务。在首个客户端发起连接之前，`systemctl status rex.socket` 会显示为 “active (listening)”。

服务端一旦启动便会持续运行，即便当前无人使用也是如此。套接字单元改变的是服务端的启动时机，而非其运行持续时长。

套接字处于激活状态时，任何连接都会触发启动服务端，包括 `rex server status`。若要在不触发启动的情况下检查其状态，请查询 systemd：

```sh
systemctl status rex.service rex.socket
```

单独停止 `rex.service` 只能生效至下一次连接到来。若要停止服务端并保持其处于停止状态，请在单条命令中同时停止这两个单元。这会终止其上的所有会话：

```sh
sudo systemctl stop rex.socket rex.service
```

若仅停止 `rex.socket`，会导致服务端在缺少套接字文件的情况下继续运行，从而使新的连接无法建立。同样，请勿使用 `rex server stop`。该命令会连接到套接字以确认服务端是否已停止，这反而可能导致其被重新启动。

若要切换为始终运行的服务端，请先禁用这两个单元，然后启用服务单元：

```sh
sudo systemctl disable --now rex.socket rex.service
sudo systemctl enable --now rex.service
```

若要切换回来，请先停止服务。在服务端运行期间，systemd 无法接管套接字的监听：

```sh
sudo systemctl disable --now rex.service
sudo systemctl enable --now rex.socket
```

任一切换操作都会终止正在运行的共享服务端上的所有会话。

Alpine 和 FreeBSD 不支持套接字激活，因此在这些系统上以服务形式运行是运行共享服务端的唯一方式。在 NixOS 上，请设置 `services.rex.socketActivation`，详见 [NixOS 模块](installation.md#nixos-模块)。

## 分配访问权限

将每个人添加至 `rex` 用户组。该修改会在他们下次登录时生效：

```sh
sudo usermod --append --groups rex alice
```

在 Alpine 上，运行 `addgroup alice rex`。在 FreeBSD 上，运行 `pw groupmod rex -m alice`。

他们的 `rex` 命令默认会查找其自有的[个人服务端](server-modes.md#个人服务端)，如果未在运行则会自动启动一个。若要改用共享服务端，请使用 `-S` 传递其套接字路径，或在其 shell profile 中设置 `REX_SERVER`，以便所有 `rex` 命令默认使用该路径：

```sh
rex -S /run/rex/server.sock ls
export REX_SERVER=/run/rex/server.sock
```

在 FreeBSD 上，套接字路径为 `/var/run/rex/server.sock`。在共享服务端自身的终端内部，`rex` 命令已默认指向该共享服务端。

`rex` 命令绝不会在共享服务端的套接字路径处自动启动个人服务端。如果共享服务端未在运行，命令会执行失败，并在 Linux 上提示需要启动的服务名称。在启用了 `rex.socket` 的情况下，该连接则会启动共享服务端。`rex` 用户组之外的人员会收到权限错误，因为只有该组能够打开 `/run/rex`。

该服务有意未作沙箱隔离。沙箱隔离同样会限制用户在其中运行的程序，因此 `rex` 账户本身即为安全边界。

若要从其他计算机访问共享服务端，请参阅[远程访问](remote-access.md)。

## 配置

共享服务端从 `rex` 账户的主目录读取其[配置文件](../customize/config.md)：

```
/var/lib/rex/.config/rex/init.lua
```

在 FreeBSD 上，对应路径为 `/var/db/rex/.config/rex/init.lua`。由于主目录仅限 `rex` 账户私有，因此只有 root 用户才能编辑该文件。修改之后，该用户组的任何成员均可重新加载配置：

```sh
sudo $EDITOR /var/lib/rex/.config/rex/init.lua
rex -S /run/rex/server.sock config reload
```

若要将配置文件存放在其他位置，可通过 drop-in 配置传递 `--config PATH`，如下所述。

## 自定义服务

软件包升级会替换 `rex.service`，因此请将自定义更改写入 drop-in 配置中。以下命令可创建并使用编辑器打开该配置：

```sh
sudo systemctl edit rex.service
```

若要修改服务端的启动选项，请先清空 `ExecStart` 然后重新设置。以下示例调高了会话上限：

```ini
[Service]
ExecStart=
ExecStart=/usr/bin/rex server run --listen /run/rex/server.sock \
  --state-dir /var/lib/rex --socket-mode 0660 --log-format text \
  --max-sessions 128
```

在 Alpine 上，升级会替换 `/etc/init.d/rex`，因此请在 `/etc/conf.d/rex` 中设置 `command_args`。软件包绝不会创建或修改该文件。在 Alpine 上相同的配置只需省去 `/usr/bin/rex`：

```sh
command_args="server run --listen /run/rex/server.sock \
  --state-dir /var/lib/rex --socket-mode 0660 --log-format text \
  --max-sessions 128"
```

请保留原命令行中的四个基础选项。采用相同模式还可以为[远程访问](remote-access.md)添加网络监听器，或通过 `--block-dir` 添加块插件目录。运行 `rex server run --help` 可查看全部可选选项。

使用 `rex.socket` 时同样适用该 drop-in 配置，因为套接字单元最终会启动 `rex.service`。套接字的路径和权限模式由套接字单元决定，因此若要修改它们，需要同时编辑这两个单元。详见[自定义套接字](#自定义套接字)。

在 FreeBSD 上，升级会替换 `/usr/local/etc/rc.d/rex` 但绝不会修改 `/etc/rc.conf`，因此请在 `/etc/rc.conf` 中设置 `rex_flags`。该设置是向服务的命令行追加选项而非替换它，因此请省略原有的四个基础选项：

```sh
sysrc rex_flags="--max-sessions 128"
service rex restart
```

[配置项](../freebsd/installation.md#配置项)列出了该服务的其他设置，例如 `rex_umask`。

## 自定义套接字

使用 `rex.socket` 时，systemd 会创建服务端的套接字并移交给服务端，由服务端直接监听该套接字，而不是自行创建新的套接字。软件包升级同样会替换 `rex.socket`，因此请通过 drop-in 为其添加自定义修改：

```sh
sudo systemctl edit rex.socket
```

服务端仅监听其命令行中显式声明的套接字。套接字单元中的每个 `ListenStream=` 路径，都需要在 `rex.service` 中有与之匹配的 `--listen` 或 `--extra-listen`。否则服务端会拒绝启动，而客户端会持续等待直到超时。

若要将套接字移至 `/run/rex/rex.sock`，请先停止这两个单元。systemd 在单元停止时会清理其已知的套接字文件，若在编辑之后再停止，则会导致旧文件残留：

```sh
sudo systemctl stop rex.socket rex.service
```

然后运行 `sudo systemctl edit rex.socket` 并设置新路径。空值的 `ListenStream=` 用于清空单元中原有的设置：

```ini
[Socket]
ListenStream=
ListenStream=/run/rex/rex.sock
```

运行 `sudo systemctl edit rex.service` 并配置相同的路径：

```ini
[Service]
ExecStart=
ExecStart=/usr/bin/rex server run --listen /run/rex/rex.sock \
  --state-dir /var/lib/rex --socket-mode 0660 --log-format text
```

随后重新启动套接字：

```sh
sudo systemctl start rex.socket
```

之后客户端便可使用 `rex -S /run/rex/rex.sock` 进行连接。若要监听第二个套接字，请在套接字单元中追加一行 `ListenStream=`，并在服务单元中追加匹配的 `--extra-listen unix://PATH`。用于 Tailscale Serve 的套接字则需要使用 `tailnet-serve://`，详见 [Tailscale Serve](remote-access.md#tailscale-serve-服务)。

服务端会保持 `SocketMode=` 赋予套接字的权限模式，并忽略针对该套接字的 `--socket-mode`。它会拒绝允许机器上所有用户连接的权限模式（例如 `0666`），因此请将其保持为 `0660` 或更严格的权限。`0600` 可以生效，但会阻止 `rex` 组的访问。

服务端仅接收来自 `ListenStream=` 的流式监听套接字，并拒绝 `Accept=yes`。对于 TCP `ListenStream=`，需要搭配端口相同且带有 `--allow-anonymous` 的 `--extra-listen`，具体如[明文 HTTP](remote-access.md#明文-http) 所述。此处应填写 IP 地址，而非主机名。

若要在日后应用对 `rex.socket` 的任何修改，请先停止这两个单元然后重新启动套接字，如上所述。在服务端正在运行时执行 `sudo systemctl restart rex.socket` 会失败，并会导致服务端失去其套接字文件。

## 日志

共享服务端将日志输出至 systemd journal：

```sh
journalctl -u rex.service -f
```

Alpine 没有 journal，因此在该系统上服务端将日志写入文件：

```sh
tail -f /var/log/rex/server.log
```

在 FreeBSD 上，服务端将日志输出至 syslog，syslog 会写入 `/var/log/messages`：

```sh
grep ' rex\[' /var/log/messages
```

日志格式为纯文本。若需要 JSON 格式，可在 drop-in 配置中将 `--log-format text` 修改为 `--log-format json`。

搭配 `rex.socket` 时，服务端仍作为 `rex.service` 输出日志。如果服务端拒绝启动（例如因尝试监听未配置的套接字），journal 会指明该套接字以及需要追加的选项。与此同时，客户端不会立刻被拒绝连接，而是各自等待直到其 `--timeout` 耗尽（默认 10 秒）。

`rex server logs` 仅显示由 `rex server start` 启动的服务端日志，而不显示系统服务日志。查看系统服务日志请使用 journal。

## 升级

升级软件包会重启正在运行的共享服务端，使其立即运行新版本。在 FreeBSD 上，pkg 不会重启任何服务，因此服务端会保持旧版本，直到运行 `service rex restart`。

搭配 `rex.socket` 时，正在运行的服务端会以相同方式重启，而尚未启动的服务端会在首个客户端连接时运行新版本。升级绝不会重启 `rex.socket` 本身。如果新版本修改了套接字单元，修改会在停止这两个单元并重新启动套接字后生效，或在下次重启系统后生效。

**重启会终止所有会话中运行的所有程序。** 这些会话会被[恢复](https://www.superlogical.com/rex/docs/features/session-restore.md)，每个窗格都会启动一个新的 Shell，只有支持恢复的程序才会重新启动。请在无人进行工作时执行升级，或在升级前[锁定升级版本](upgrading.md#锁定升级版本)。

登录服务端则没有这个问题，其会话能够在升级过程中存活下来。其余升级细节详见[升级](upgrading.md)。
