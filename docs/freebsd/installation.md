> 原文：https://www.superlogical.com/rex/docs/freebsd/installation
> 原文版本：283ca2fca487（抓取于 2026-11-13）

# 在 FreeBSD 上安装

Rex 可以在 FreeBSD 上作为服务端运行，以便客户端将其作为远程主机访问。

**重要提示：** FreeBSD 版 Rex 目前处于测试阶段。使用 Discord 登录后，下方会显示安装命令。

其他服务端文档（以[服务端模式](../linux/server-modes.md)为起始）同样适用于 FreeBSD。若其中提及 Linux 命令或路径，请使用[命令与路径](#命令与路径)中给出的 FreeBSD 对应项。

## 快速入门

本节介绍快速搭建并运行的推荐配置。该配置可通过 SSH 从客户端直接访问你自有的个人服务端，无需其他额外设置。建议阅读后续章节以及[远程访问](../linux/remote-access.md#ssh)，以了解详细机制与其他访问方式。

1. 在 FreeBSD 机器上，按照[安装](#安装)中的说明安装 Rex。

2. 检查能否使用 SSH 密钥从客户端登录，且 SSH 能够在目标机器上找到 `rex`：

   ```sh
   ssh alice@build.example.com rex version
   ```

3. 从客户端发起连接：

   ```sh
   rex -S ssh://alice@build.example.com ls
   ```

   在 Mac 版 Rex 中，选择 **Add Remote Host…**（添加远程主机）并输入 `ssh://alice@build.example.com`。

首次连接会启动你的个人服务端，在你注销登录后它会持续运行，直到你将其停止或机器重启。如果一台机器上需要供多人使用 Rex，请参阅[服务端模式](../linux/server-modes.md)。

## 系统要求

| 要求 | 支持情况 |
| --- | --- |
| 发行版本 | FreeBSD 14.0 或更高版本 |
| 架构 | x86-64、ARM64 |
| 依赖项 | 无。Rex 仅使用基础系统组件。 |
| 系统服务 | rc.d（适用于共享服务端和登录服务端）。`rex` 命令无需这两者即可直接运行。 |
| 软件包格式 | `.pkg`，来自 Rex 软件源 |

单个软件包可适用于 FreeBSD 14 及后续所有发行版本。

## 安装

**安装脚本（`install.sh`）**会将 Rex 软件源添加至 pkg 并安装 `rex` 软件包，从而使 `pkg upgrade` 能够随系统其他软件包一同更新 Rex。该脚本支持与 [Linux](../linux/installation.md#安装) 相同的选项，例如 `--channel`、`--tarball` 和 `--dry-run`。请在 `sh -s --` 之后传递这些选项。

FreeBSD 默认没有 `sudo`，因此请以 root 身份运行 **pkg** 标签页中的命令。首先执行的 `umask 022` 能够确保创建的文件对所有用户可读，而无论 root 的 umask 为何。安装脚本同样需要 root 权限，或者使用已安装的 `sudo`。

FreeBSD 默认同样没有 curl，因此命令使用 FreeBSD 自带的 `fetch` 进行下载。

如果某个通道暂无 FreeBSD 软件包，脚本仅会将 `rex` 二进制文件安装至 `/usr/local/bin`（行为同 `--tarball`），且不包含系统服务。一旦该通道发布了软件包，再次运行该脚本即可自动切换至软件包安装。

pkg 通过 `/usr/local/etc/pkg/fingerprints/rex` 中的签名密钥指纹信任 Rex 软件源。如果密钥发生变更，请重新运行安装脚本以信任新密钥。

## 通道

FreeBSD 拥有与 Linux 相同的三个[通道](../linux/installation.md#发布通道)。若要切换通道，请修改 `/usr/local/etc/pkg/repos/rex.conf` 中 `url` 行对应的通道名称，随后更新软件目录：

```sh
pkg update -r rex
```

从 snapshot 切换至 preview 或 stable 会升级 Rex。切换回 snapshot 属于降级操作，需要显式指定，详见[在 FreeBSD 上升级](../linux/upgrading.md#freebsd)。

## 软件包内容

`rex` 软件包会安装以下内容：

| 路径 | 说明 |
| --- | --- |
| `/usr/local/bin/rex` | 服务端与 CLI 二进制文件，两者合二为一 |
| `/usr/local/etc/rc.d/rex` | 单个共享服务端，以 `rex` 账户运行。默认未启用。 |
| `/usr/local/etc/rc.d/rex-login-server` | 登录后为每个账户运行一个服务端。默认未启用。 |
| `rex` 账户与用户组 | 锁定的系统账户，UID 为 729（或下一个可用空闲 ID），主目录位于 `/var/db/rex` |
| `/usr/local/etc/rex/accounts.jsonc` | 登录服务端的账户配置文件。初始为空，不接纳任何访问。 |
| `/usr/local/etc/pam.d/rex-login-server` | 登录服务端的 PAM 策略 |
| `xterm-rex` terminfo | Rex 的终端类型定义，位于 `/usr/local/share/terminfo` |

与 Linux 软件包不同，FreeBSD 软件包不包含 SSH 回退配置，因为 FreeBSD 的 `/etc/ssh/ssh_config` 不会读取其他附属文件。详见 [Terminfo 与 SSH](#terminfo-与-ssh)。

升级会保留你对账户文件的修改，但会替换 PAM 策略，详见[在 FreeBSD 上升级](../linux/upgrading.md#freebsd)。若要再次查看软件包的安装说明，请运行 `pkg info -D rex`。

## 命令与路径

其他服务端页面通常提供 systemd 命令。在 FreeBSD 上，请改用以下对应命令：

| 在 systemd 上 | 在 FreeBSD 上 |
| --- | --- |
| `sudo systemctl enable --now rex.service` | `sysrc rex_enable=YES`，然后 `service rex start` |
| `sudo systemctl enable --now rex-login-server.service` | `sysrc rex_login_server_enable=YES`，然后 `service rex-login-server start` |
| `sudo systemctl reload rex-login-server.service` | `service rex-login-server reload` |
| `sudo systemctl restart rex.service` | `service rex restart` |
| `sudo systemctl disable --now rex.service` | `service rex stop`，然后 `sysrc rex_enable=NO` |
| `sudo systemctl edit rex.service` | 使用 `sysrc` 设置 `rex_flags`。详见[配置项](#配置项)。 |
| `journalctl -u rex.service` | `grep ' rex\[' /var/log/messages` |
| `journalctl -u rex-login-server.service` | `grep ' rex-login-server\[' /var/log/messages` |
| `sudo usermod --append --groups rex alice` | `pw groupmod rex -m alice` |
| `sudo usermod --shell /bin/bash rex` | `pw usermod rex -s /bin/sh` |

FreeBSD 不支持套接字激活，因此 `rex.socket` 与 `rex-login-server.socket` 在 FreeBSD 上没有对应形式。请直接使用系统服务。

文件的存放位置也有所不同：

| 在 Linux 上 | 在 FreeBSD 上 |
| --- | --- |
| `/usr/bin/rex` | `/usr/local/bin/rex` |
| `/run/rex` | `/var/run/rex` |
| `/var/lib/rex` | `/var/db/rex` |
| `/etc/rex/accounts.jsonc` | `/usr/local/etc/rex/accounts.jsonc` |
| `/etc/pam.d/rex-login-server` | `/usr/local/etc/pam.d/rex-login-server` |
| `/etc/nologin` | `/var/run/nologin` |
| `/run/user/<uid>/rex` | `~/.local/state/rex/run` |

这两个服务均将日志输出至 syslog，syslog 默认写入 `/var/log/messages`。登录服务端为各个账户启动的服务端则将日志写入 `/var/run/rex/accounts/<account>/server.log`。

如果服务端因任何原因退出，其服务会在 5 秒后再次尝试启动。只有 `service rex stop` 才会彻底停止它。`service rex start` 在服务端进程建立后便会立即返回，此时距离其正式开始接收连接可能还需要短暂的等待。

## 配置项

这些服务从 `/etc/rc.conf` 中读取其配置。使用 `sysrc` 进行配置，随后重启服务即可使配置生效。系统升级会替换 rc.d 脚本，但绝不会修改 `/etc/rc.conf`。以下示例调高了共享服务端的会话上限：

```sh
sysrc rex_flags="--max-sessions 128"
service rex restart
```

| 配置项 | 默认值 | 效果 |
| --- | --- | --- |
| `rex_flags` | 无 | 传递给 `rex server run` 的额外选项 |
| `rex_umask` | `0007` | 服务端及其启动的每个程序的文件权限掩码 |
| `rex_user` | `rex` | 服务端运行所使用的账户 |
| `rex_group` | `rex` | 获准使用该套接字的用户组 |
| `rex_runtime_dir` | `/var/run/rex` | 存放套接字的目录 |
| `rex_state_dir` | `/var/db/rex` | 服务端的数据目录 |
| `rex_login_server_flags` | 无 | 传递给 `rex login-server` 的额外选项 |
| `rex_login_server_accounts` | `/usr/local/etc/rex/accounts.jsonc` | 账户配置文件路径 |
| `rex_login_server_runtime_dir` | `/var/run/rex` | 登录服务端的套接字及各个账户服务端的目录 |

`rex_flags` 与 `rex_login_server_flags` 用于向服务的命令行追加选项。systemd 的 drop-in 配置则是替换整条命令行，因此当其他页面展示完整的 `ExecStart` 行时，只需将其新增的选项填入 flags 中即可。每个 rc.d 脚本开头的注释中均详细说明了各项配置。

共享服务端也可以使用其他账户运行，而非必须使用 `rex`。以下示例将其配置为以 `alice` 运行：

```sh
sysrc rex_user=alice rex_group=alice
service rex restart
```

服务端在修改前写入的文件仍属于旧账户。在下次启动时，服务会将这些文件移交给新账户，并在每修改一个目录时输出一行提示：

```
Giving the files in /var/run/rex to alice:alice.
Giving the files in /var/db/rex to alice:alice.
```

服务端会保留其保存的会话，其中的程序现在以 `alice` 身份运行。切换回 `rex` 的方式与此完全相同。

## Terminfo 与 SSH

Rex 终端中的程序能够获取到 `TERM=xterm-rex`，且软件包会为每个账户安装该终端类型。ssh 会将 `TERM` 传递给其他主机，而其他主机通常无法识别该类型。若要让 ssh 在连接到那些主机时向其发送 `xterm-256color`，请以 root 身份运行：

```sh
rex terminfo setup --system
```

FreeBSD 的 `/etc/ssh/ssh_config` 不会读取其他文件，因此该命令还会向其中添加一行带有标记的 `Include` 配置。运行 `rex terminfo remove --system` 可再次移除该行。若仅为自己的账户进行配置，请直接运行 `rex terminfo setup`。
