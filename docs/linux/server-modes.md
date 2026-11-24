> 原文：https://www.superlogical.com/rex/docs/linux/server-modes
> 原文版本：42ecdaf1d5ba（抓取于 2026-11-24）

# 服务端运行模式

以何种方式运行 Rex 服务端，决定了它以哪个账户运行以及允许谁连接。**在 Windows 上仅支持个人服务端，详见[在 Windows 上运行](../windows/running.md)。**

**如果只需从 Mac 连接一台机器上的 Rex，建议先从快速入门开始。** 各平台的快速入门都会配置一个通过 SSH 访问的个人服务端：
[Linux](installation.md#快速入门)、
[FreeBSD](../freebsd/installation.md#快速入门) 或
[Windows](../windows/running.md#快速入门)。

在 Linux 和 FreeBSD 上运行 Rex 服务端有三种方式：

| 模式 | 适用对象 | 运行身份 | 启动方式 |
| --- | --- | --- | --- |
| 个人服务端 | 仅限本人 | 你的账户 | 任意 `rex` 命令，或 `rex server start` |
| 共享服务端 | 信任并共用同一账户的少数几人 | `rex` | `rex.service`，或通过 `rex.socket` 按需启动 |
| 登录服务端 | 多人各自以独立身份登录 | root，随后切换为各用户的账户 | `rex-login-server.service`，或通过 `rex-login-server.socket` 按需启动 |

如果这台机器上只有你一个人使用 Rex，请运行个人服务端。如果有几个人需要使用并且可以共享同一个账户，请使用共享服务端。如果你或其他人需要以各自独立的账户访问和登录，请使用登录服务端。

共享服务端与登录服务端不能同时运行。它们的服务和套接字均使用 `/run/rex`，因此启动其中一个的服务或套接字会停止另一个的两个单元。在 Alpine 和 FreeBSD 上，其中一个正在运行时，另一个会拒绝启动。个人服务端可以与这两者中的任意一个并行运行。在登录服务端模式下，你的个人服务端与登录服务端将你连接至的服务端是同一个，因此本地的 `rex` 命令与远程连接看到的是完全相同的会话。

默认情况下，每种模式均仅在本机的 Unix 套接字上监听。若要从其他计算机连接，请参阅[远程访问](remote-access.md)。

## 个人服务端

个人服务端以你自己的用户账户运行，无需任何特殊配置或 root 权限。当没有服务端正在运行时，任何 `rex` 命令都会自动启动一个个人服务端：

```sh
rex ls
```

自动启动的个人服务端在其最后一个会话及最后一个连接关闭约 10 秒后自行停止。若要启动一个持续运行的服务端，必须显式启动它：

```sh
rex server start
```

如果已有服务端在运行（包括由 `rex` 命令自动启动的服务端），`rex server start` 不会执行任何操作，因此可以安全地多次调用。其选项（例如 `--max-sessions`）仅在启动新的服务端时生效。若要修改这些选项，请先停止服务端然后再重新启动。

| 命令 | 效果 |
| --- | --- |
| `rex server status` | 显示正在运行的服务端的状态。 |
| `rex server logs --follow` | 显示并持续跟踪由 `rex server start` 启动的服务端的日志。 |
| `rex server stop` | 停止服务端。这会终止其上的所有会话。 |

套接字位于 `$XDG_RUNTIME_DIR/rex` 中，通常为 `/run/user/<uid>/rex`。日志和其他状态位于 `~/.local/state/rex` 中，若设置了 `$XDG_STATE_HOME` 则位于 `$XDG_STATE_HOME/rex`。FreeBSD 没有 `/run/user`，因此在该系统上套接字位于 `~/.local/state/rex/run`。对于没有该目录的 Linux 机器（例如许多容器环境），情况也是如此。

`rex` 命令仅会针对该目录下的套接字（或在设置了 `REX_RUNTIME_DIR` 时针对该环境变量指定的目录）自动启动服务端。当使用 `-S` 指定任何其他套接字时（例如共享服务端的套接字），它不会自动启动任何内容，并会提示如何在对应位置启动服务端。若要在其他路径运行你自己的服务端，请自行启动。你的账户必须有权在该套接字所在目录中创建文件：

```sh
rex -S PATH server start
```

若要彻底禁止 `rex` 命令自动启动服务端，请设置 `REX_AUTOSTART=0`。

### 共享主目录

即使用户的主目录跨多台机器共享（例如通过 NFS），Rex 也能作为个人服务端正常运行。Rex 使用机器 ID 来区分本地状态，因此通常会自动处理，本节将说明其具体机制。

第一台使用 `~/.local/state/rex` 的机器会声明归属权，并照常将状态保存在该目录中。这样一来，对于不使用共享文件系统的普通用户，本地状态目录仍能保持整洁。

后续访问同一状态目录的其他机器，会将其状态保存在按机器 ID 区分的子目录 `~/.local/state/rex/machines/<key>` 中。每台机器各自拥有独立的服务端、会话、主机 ID 和主机列表。`~/.config/rex` 中的配置则保持共享。

Rex 通过 `/etc/machine-id`（在 FreeBSD 上则为 `kern.hostuuid`）来确定机器 ID。

当某台机器的 ID 发生变化时（例如重装系统后），它会被视为一台新机器，并在启动时没有任何会话。如果它原本是第一台声明归属权的机器，可以收回其旧状态：移除归属标记，然后停止当前服务端，使下一条 `rex` 命令使用旧状态启动服务端：

```sh
rm ~/.local/state/rex/machine-owner
rex server stop
rex ls
```

## 共享服务端

共享服务端是作为一个整体以 `rex` 系统账户运行的单个服务端。`rex` 用户组的成员可以连接到该服务端，并且他们启动的每个程序均以 `rex` 身份运行。这是允许多人使用 Rex 的最简单方式。

**访问共享服务端等同于访问 `rex` 账户。** 该用户组中的任何人都可以查看并向其上的所有会话中输入内容。因此，只应添加你信任并愿意与之共享该账户的人员。

将每个人添加至该用户组，然后立即启动服务并设置为开机自启：

```sh
sudo usermod --append --groups rex alice
sudo systemctl enable --now rex.service
```

用户组更改会在对应人员下次登录时生效。服务端将其数据保存在 `/var/lib/rex` 中，在 FreeBSD 上则保存在 `/var/db/rex` 中。在 Alpine 上，通过 [OpenRC 命令](installation.md#alpine-发行版)完成上述两个步骤；在 FreeBSD 上，通过 [FreeBSD 命令](../freebsd/installation.md#命令与路径)完成。

若要仅在有人首次发起连接时才启动服务端，请启用 `rex.socket` 而非 `rex.service`。详见[按需启动](shared-server.md#按需启动)。

软件包升级会重启该服务，这会自动终止其上的所有会话。详见[升级](upgrading.md)。

在为其他人配置之前，请先阅读[共享服务端](shared-server.md)。该文档涵盖了如何向他人分配访问权限、配置服务端以及在修改服务的同时确保升级时不丢失自定义更改。

## 登录服务端

登录服务端为每个人提供一个以其自身账户运行的服务端，拥有各自独立的文件与权限。登录服务端以 root 权限运行。当有人连接时，它会识别其身份，检查 `/etc/rex/accounts.jsonc` 确认其获准使用的账户，并将连接转交给以该账户运行的服务端。如有需要，它会自动启动该服务端。

登录服务端与 SSH 最为相似：一个统一的 root 服务，允许每个人作为各自的账户登录。与 SSH 不同的是，它不使用密码或密钥。**它仅通过连接来源识别访问方身份**，例如其套接字对端的本地账户或其 Tailscale 登录身份。任何能够以此种方式访问它的人，均可使用为其列出的账户。

当登录服务端停止、重启或升级时，各账户的服务端会保持持续运行，因此会话能够在这三种情况下存活下来。升级之后，各个账户的服务端会继续保持旧版本，直到其上的会话全部结束。

账户配置文件初始为空，不接纳任何人访问。添加至少一个账户，然后立即启动服务并设置为开机自启：

```sh
sudo $EDITOR /etc/rex/accounts.jsonc
sudo systemctl enable --now rex-login-server.service
```

在 Alpine 上，请改用 [OpenRC 命令](installation.md#alpine-发行版)。在 FreeBSD 上，请使用 [FreeBSD 命令](../freebsd/installation.md#命令与路径)，并编辑 `/usr/local/etc/rex/accounts.jsonc`。

若要仅在有人首次连接时才启动登录服务端，请启用 `rex-login-server.socket` 而非 `rex-login-server.service`。详见[按需启动](login-server.md#按需启动)。

修改账户文件后，重新加载该配置。这不会中断任何已有连接：

```sh
sudo systemctl reload rex-login-server.service
```

在 Alpine 上，运行 `rc-service rex-login-server reload`。在 FreeBSD 上，运行 `service rex-login-server reload`。

在添加账户之前，请先阅读[登录服务端](login-server.md)。该文档涵盖了账户文件格式、访问者在连接时如何选择账户，以及登录服务端用于校验账户的 PAM 策略。

## 在服务之间切换

启动任意一个服务端都会停止另一个，但也应禁用旧服务端的服务与套接字，以免在下次开机时重新启动：

```sh
sudo systemctl disable --now rex.service rex.socket
sudo systemctl enable --now rex-login-server.service
```

若要按需启动新服务端，请改为启用其套接字单元，例如 `rex-login-server.socket`。若要切换回原服务端，互换服务名称即可：禁用 `rex-login-server.service` 与 `rex-login-server.socket`，然后启用 `rex.service` 或 `rex.socket`。

在 Alpine 上，另一个服务正在运行时启动任一服务均会失败，因此请先停止旧服务：

```sh
rc-service rex stop
rc-update del rex
rc-update add rex-login-server
rc-service rex-login-server start
```

在 FreeBSD 上的情况也是如此。请先停止并禁用旧服务：

```sh
service rex stop
sysrc rex_enable=NO
sysrc rex_login_server_enable=YES
service rex-login-server start
```

从共享服务端切换会终止其上的所有会话。

从登录服务端切换则会保留各个账户正在运行的服务端。在没有 systemd-logind 的机器上，或者登录服务端以 `--pam=false` 运行时，这些服务端会将其套接字保留在 `/run/rex/accounts` 中，而 `rex.service` 与 `rex.socket` 在该目录存在时会拒绝启动。一旦不再需要那些会话，清理该目录并启动共享服务端：

```sh
sudo rm -rf /run/rex
sudo systemctl start rex.service
```

若要按需启动共享服务端，请改为启动 `rex.socket`。被拒绝的启动仍可能导致登录服务端的单元停止运行，因此如果要放弃切换，请重新启动登录服务端的服务或套接字。

Alpine 没有 systemd-logind，因此在该系统上各账户服务端始终将其套接字保存在 `/run/rex/accounts` 中。以相同方式清理该目录，然后运行 `rc-service rex start`。

FreeBSD 同样没有 systemd-logind，并且会在重启后保留 `/var/run`，因此在该系统上仅当 `/var/run/rex/accounts` 中存在套接字时，`rex` 服务才会拒绝启动。使用 `rm -rf /var/run/rex` 以相同方式进行清理，然后运行 `service rex start`。
