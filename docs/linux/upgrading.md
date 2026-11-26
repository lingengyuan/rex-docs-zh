> 原文：https://www.superlogical.com/rex/docs/linux/upgrading
> 原文版本：085d1d40c2a2（抓取于 2026-11-26）

# 升级

你可以使用初次安装时所用的标准包管理器来升级 Rex。如果使用了 `install.sh` 脚本，再次运行该脚本同样是安全的；它仅会自动检测并调用你系统上的包管理器。

在 Linux 上，`install.sh` 和标准包管理器会自动重启正在运行的服务端。在 FreeBSD 和 Windows 上，则不会自动重启任何服务；你必须手动将服务端重启至最新版本。详见 [FreeBSD](#freebsd) 与 [Windows](#windows)。

**升级会终止正在运行的共享服务端上运行的所有程序。** 其会话会被恢复。登录服务端和个人服务端则会保持其会话运行，详见[服务重启机制](#服务重启机制)。

## 升级软件包

| 安装方式 | 升级命令 |
| --- | --- |
| Debian、Ubuntu | `sudo apt-get update && sudo apt-get install --only-upgrade rex` |
| Fedora、RHEL | `sudo dnf upgrade --refresh rex` |
| openSUSE | `sudo zypper update rex` |
| Arch Linux | `sudo pacman -Syu` |
| Omarchy | `omarchy update` |
| Alpine | `apk update && apk add -u rex` |
| FreeBSD | `pkg upgrade -r rex rex` |
| Nix profile | `nix profile upgrade --regex '.*superlogical.*'` |
| 安装脚本 | 运行初次安装时所用的相同命令。 |
| `--tarball` | 携带 `--tarball` 再次运行安装脚本。 |
| Amazon Linux 2 | 再次运行安装脚本。 |
| Windows | 参阅 [Windows](#windows)。 |

再次运行安装脚本时，请传递与初次安装相同的 `--channel`。若未指定，脚本会将软件源重置为默认通道。

## 服务重启机制

软件包会重启正在运行的 Rex 服务，并保持处于停止状态的服务继续处于停止状态。在没有运行 init 系统的容器中，不会重启任何服务；FreeBSD 软件包同样不会自动重启服务，详见 [FreeBSD](#freebsd)。

软件包绝不会重启 `rex.socket` 或 `rex-login-server.socket`。由套接字启动的服务端会像其他服务一样重启，尚未启动的服务端则会在首个客户端连接时运行新版本。如果新版本修改了套接字单元，修改会在停止该套接字及其服务并重新启动套接字后生效，或在下次系统重启后生效。

| 服务端类型 | 升级时的表现 | 会话状态 | 何时运行新版本 |
| --- | --- | --- | --- |
| 共享服务端 | 重启 | 恢复 | 立即运行 |
| 登录服务端 | 重启 | 存活 | 立即运行 |
| 各账户服务端 | 保持运行 | 存活 | 当其所有会话结束时 |
| 个人服务端 | 保持运行 | 存活 | 当其停止运行时 |

**重启共享服务端会终止其会话中运行的所有程序。** 这些会话会被[恢复](https://www.superlogical.com/rex/docs/features/session-restore.md)，每个窗格都会启动一个新的 Shell，只有支持恢复的程序才会重新启动。请在无人进行工作时执行升级，或在升级前[锁定升级版本](#锁定升级版本)。

登录服务端为每个账户启动的服务端会继续保持其启动时的版本。每个服务端在其最后一个会话结束且最后一个客户端断开连接约 10 秒后停止，随后的下一次连接会使用新版本重新启动它。在带有 systemd-logind 的机器上，用户可以通过以自身身份在机器上运行 `rex server stop` 来提前切换，这会终止其自身的会话。

由 `rex` 命令启动的个人服务端在空闲后会自动停止，因此它会自动获取新版本。通过 `rex server start` 启动的个人服务端则会持续运行旧版本，直到你将其停止并重新启动：

```sh
rex server stop
rex server start
```

## 检查版本

`rex version` 显示已安装的版本，`rex server status` 显示当前正在运行的服务端版本：

```sh
rex version
rex server status
```

如果 `rex version` 的第一行与 `rex server status` 的 `version:` 行不一致，说明该服务端仍在运行旧版本。通过登录服务端连接时，`rex server status` 显示的是你所在账户的服务端版本。

## 锁定升级版本

若要将 Rex 保持在当前版本直到准备好升级：

| 包管理器 | 锁定版本 | 解除锁定 |
| --- | --- | --- |
| apt | `sudo apt-mark hold rex` | `sudo apt-mark unhold rex` |
| dnf | `sudo dnf versionlock add rex` | `sudo dnf versionlock delete rex` |
| zypper | `sudo zypper addlock rex` | `sudo zypper removelock rex` |
| pacman | 在 `/etc/pacman.conf` 的 `[options]` 下添加 `IgnorePkg = rex` | 删除该行配置 |
| apk | `apk add rex=VERSION` | `apk add -u rex` |
| pkg | `pkg lock rex` | `pkg unlock rex` |

在 RHEL 及其衍生版本上，`versionlock` 是一个插件，请通过 `sudo dnf install 'dnf-command(versionlock)'` 进行安装。Fedora 已内置该功能。

在 Alpine 上，`VERSION` 为完整版本号，例如 `0.1.0-r0`。`apk info -e -v rex` 可显示已安装的版本。

## 保留自定义修改

升级会保留你对以下内容的修改：

- 账户文件 `/etc/rex/accounts.jsonc`
- PAM 策略 `/etc/pam.d/rex-login-server`
- 针对 `rex.service`、`rex-login-server.service` 及其套接字的 drop-in 配置
- Alpine 上的 `/etc/conf.d/rex` 与 `/etc/conf.d/rex-login-server`
- FreeBSD 上的 `/etc/rc.conf`

升级会替换服务本身：`rex.service`、`rex-login-server.service`、`rex.socket`、`rex-login-server.socket`、`/etc/init.d` 中的脚本以及 FreeBSD 上 `/usr/local/etc/rc.d` 中的脚本。在 FreeBSD 上，升级还会替换 PAM 策略，详见 [FreeBSD](#freebsd)。请将自定义修改写入 drop-in 配置或 `/etc/conf.d` 中，如[自定义服务](shared-server.md#自定义服务)所述。

如果你修改了配置文件，而 Rex 新版本也对其进行了修改，系统会保留你的文件，并将新文件保存在其旁边：

| 包管理器 | 新文件保存格式 | 说明 |
| --- | --- | --- |
| apt | `.dpkg-dist` | apt 会先行询问。安装脚本不会询问。 |
| dnf、zypper | `.rpmnew` | |
| apk | `.apk-new` | |
| pkg | `.sample` | 仅限账户文件。pkg 每次升级都会更新 sample 文件。 |

对比这两个文件并将需要的修改合并过来即可。在 dnf 和 zypper 上，SSH 回退配置 `/etc/ssh/ssh_config.d/50-rex.conf` 是个例外：升级会直接替换它并将你的原配置另存为 `.rpmsave`。

## 客户端与服务端版本兼容

Mac 版 Rex 与服务端无需保持相同版本，两者中任意一方都可以更新。较新的客户端无法使用较旧服务端尚未提供的功能。当需要某项新功能时，客户端会予以提示：

```
this server is too old for rex client ls; it needs Rex 0.1.0 or later
```

如果两者的版本差异过大而无法协同工作，服务端会拒绝连接，且提示信息的结尾会包含 `update the server`（请更新服务端）或 `update the client`（请更新客户端）。

## 切换通道与降级

从 snapshot [切换通道](installation.md#发布通道)至 preview 或 stable 会像往常一样升级 Rex。切换回 snapshot 属于降级操作，因为快照版本的排序低于正式发布版本。降级不会自动进行，因此请显式指定你所需的版本：

| 包管理器 | 查询可选版本 | 降级命令 |
| --- | --- | --- |
| apt | `apt-cache madison rex` | `sudo apt-get install --allow-downgrades rex=VERSION` |
| dnf | `dnf list --showduplicates rex` | `sudo dnf downgrade rex-VERSION` |
| zypper | `zypper search -s -x rex` | `sudo zypper install --oldpackage rex-VERSION` |
| pacman | 仅保留一个版本。详见 [Arch Linux 发行版](installation.md#arch-linux-发行版)。 | `sudo pacman -U URL` |
| apk | `apk search -a -x rex` | `apk add rex=VERSION` |
| pkg | 仅保留一个版本。详见 [FreeBSD](#freebsd)。 | 参阅 [FreeBSD](#freebsd)。 |

降级重启服务的方式与升级相同。在降级过程中你的数据是安全的。当某个版本的 Rex 发现由更高版本格式写入的数据时，它会拒绝使用该数据，而非将其覆盖。

## 更改 Rex 安装方式

一台机器上请仅保留一份 Rex。位于 `/usr/local/bin` 的 `--tarball` 二进制文件在常用 `PATH` 中的优先级高于软件包的 `/usr/bin/rex`，因此若同时安装了这两者，无论你升级哪一个，`rex` 命令及其启动的个人服务端都会运行 tarball 版本。若要查看 `PATH` 中的所有 `rex`：

```sh
which -a rex
```

若要从 `--tarball` 迁移至软件包，请先安装软件包，然后删除该二进制文件：

```sh
sudo rm /usr/local/bin/rex
```

若要从软件包迁移至 `--tarball` 或 Nix，请先卸载软件包：

| 包管理器 | 卸载命令 |
| --- | --- |
| apt | `sudo apt-get remove rex` |
| dnf | `sudo dnf remove rex` |
| zypper | `sudo zypper remove rex` |
| pacman | `sudo pacman -R rex` |
| apk | `apk del rex` |
| pkg | `pkg delete rex` |

卸载软件包会停止并禁用其服务和套接字，这会终止共享服务端上的所有会话。来自 AUR 的 `rex-bin` 不会自动执行此操作，因此请自行先停止并禁用它们，详见 [Arch Linux 发行版](installation.md#arch-linux-发行版)。

卸载软件包会保留 `/var/lib/rex` 与 `rex` 账户，因此再次安装软件包时能够直接继承共享服务端的数据。在 FreeBSD 上，会保留 `/var/db/rex` 以及你在 `/etc/rc.conf` 中的配置。

安装脚本与其他安装标签页中的命令配置的是同一个软件源，因此你可以在它们之间相互切换。在 Alpine 上，脚本将软件源写入 `/etc/apk/repositories.d/rex.list`，而 **Alpine** 标签页将其添加至 `/etc/apk/repositories`。请仅保留其中一份配置。

## NixOS 系统

在 flake 中更新 Rex 的 input，然后执行切换：

```sh
nix flake update rex
sudo nixos-rebuild switch --flake .
```

当 Rex 发生变动时，`nixos-rebuild switch` 会重启 Rex 服务，其表现与软件包升级一致：共享服务端的程序会终止，各账户服务端则会保留旧版本直到其会话结束。

`flake.lock` 会将 Rex 保持在当前版本直到你更新它，因此无需采取其他措施即可锁定升级版本。

## FreeBSD

pkg 无法自动重启服务，因此在升级之后，原先正在运行的服务会继续保持旧版本。pkg 会在其输出末尾指明涉及的服务，安装脚本同样如此。请在准备好后重启对应服务：

```sh
service rex restart
service rex-login-server restart
```

**重启 `rex` 会终止共享服务端上运行的所有程序**，这与 Linux 上的表现相同。其会话会被恢复。重启 `rex-login-server` 会保留各个账户的服务端及其会话，它们会保持旧版本直到会话结束。

升级会保留你对账户文件的修改，但会替换 `/usr/local/etc/pam.d` 中的 PAM 策略。若要修改策略，请编辑在 `/etc/pam.d` 中的副本，如[登录服务端](login-server.md#freebsd)所述。

pkg 无法通过 `pkg install` 直接执行降级，因此请先删除较新版本。删除操作会停止这两个服务，从而终止共享服务端上的所有会话：

```sh
pkg delete rex
pkg install -r rex rex
```

软件源中同一时间只保留一个版本的 Rex，即该通道上的最新版本。较旧的软件包仍留在通道目录中，因此若要回退到旧版本，请将其 URL 传给 `pkg add`，然后[锁定版本](#锁定版本)：

```sh
pkg delete rex
pkg add https://pkgs.superlogical.com/rex/freebsd/snapshot/amd64/rex-VERSION.pkg
pkg lock rex
```

`VERSION` 为完整版本号，例如 `0.1.0.alpha2514`。在 ARM64 上请将 `amd64` 替换为 `aarch64`。`pkg info rex` 可显示已安装的版本。

## Windows

按照初次安装时的相同方式升级 Rex：

| 安装方式 | 升级方式 |
| --- | --- |
| WinGet | `winget upgrade --id Superlogical.RexServer.Preview --source rex` |
| 手动安装 MSI | 下载新版 [MSI](../windows/installation.md#msi) 并运行。 |
| 手动安装 Zip | 停止服务端，然后将新版 zip 解压覆盖旧文件夹。 |

**使用 WinGet 升级前必须先停止服务端。** WinGet 无法替换正在运行的服务端文件，因此升级会报错“拒绝访问”（Access is denied），且 Rex 会保持在旧版本。

在所有情况下，均不会自动重启服务。如何重启服务端取决于其最初的启动方式，如[服务端生命周期](../windows/running.md#服务端生命周期)所述：

| 启动方式 | 如何运行新版本 |
| --- | --- |
| 任意 `rex` 命令 | 无需操作。服务端空闲后会自动停止，随后的下一条命令即会启动新版本。 |
| `rex server start` | 先执行 `rex server stop`，再执行 `rex server start` |
| `rex server install --user` | 先执行 `rex server stop`，再执行 `rex server install --user`，或重新登录用户账户 |
| `rex server install` | 先执行 `rex server stop`，再执行 `sc.exe start RexServer-<SID>` |

`sc.exe start` 需要在通过**以管理员身份运行**打开的终端中执行，详见[停止与重启](../windows/running.md#停止与重启)。

**警告！重启服务端会终止其会话中运行的所有程序。** 服务端会保存会话布局，但目前无法恢复此前正在运行的程序。

### 锁定升级版本

若要防止 WinGet 在你准备好之前自动升级 Rex，可以固定该版本：

```powershell
winget pin add --id Superlogical.RexServer.Preview --source rex
```

若要查看固定的版本或解除固定：

```powershell
winget pin list --source rex
winget pin remove --id Superlogical.RexServer.Preview --source rex
```

由于指定了显式源，未携带 `--source rex` 时 `winget pin list` 不会显示任何内容。自行手动安装的 MSI 或 zip 绝不会自动升级，除非你主动安装新版本。
