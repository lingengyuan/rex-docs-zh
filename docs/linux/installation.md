> 原文：https://www.superlogical.com/rex/docs/linux/installation
> 原文版本：650bbc3546d5（抓取于 2026-11-13）

# 在 Linux 上安装

Rex 可以在 Linux 上作为服务端运行，以便客户端将其作为远程主机访问。

**重要提示：** Linux 版 Rex 目前处于测试阶段。使用 Discord 登录后，下方会显示安装命令。

## 快速入门

本节介绍快速搭建并运行的推荐配置。该配置可通过 SSH 从客户端直接访问你自己的个人服务端，无需其他额外设置。建议阅读后续章节以及[远程访问](remote-access.md#ssh)，以了解详细机制与其他访问方式。

1. 在 Linux 机器上，按照[安装](#安装)中的说明安装 Rex。

2. 设置开机时启动个人服务端，并在注销登录后保持运行。此操作无需 sudo，以希望用于连接的用户身份运行即可：

   ```sh
   rex server install
   ```

   在没有 systemd 的系统上（例如 Alpine），跳过此步骤。由首次连接触发启动的服务端将持续运行，直到机器重启。

3. 检查能否使用 SSH 密钥从客户端登录，且 SSH 能够在该机器上找到 `rex`：

   ```sh
   ssh alice@build.example.com rex version
   ```

4. 从客户端发起连接：

   ```sh
   rex -S ssh://alice@build.example.com ls
   ```

   在 Mac 版 Rex 中，选择 **Add Remote Host…**（添加远程主机）并输入 `ssh://alice@build.example.com`。

如果一台机器上需要供多人使用 Rex，请参阅[服务端运行模式](server-modes.md)。

## 系统要求

| 要求 | 支持情况 |
| --- | --- |
| 架构 | x86-64、ARM64 |
| C 语言运行库 | glibc 2.26 或更高版本（Amazon Linux 2、Ubuntu 18.04、Debian 10、RHEL 8 或更新版本），或 Alpine 3.21 及更高版本上的 musl |
| Init 系统 | systemd，或 Alpine 上的 OpenRC（适用于共享服务端和登录服务端）。`rex` 命令无需这两者即可直接运行。 |
| 软件包格式 | `.deb`（Debian、Ubuntu）、`.rpm`（Fedora、RHEL 及其衍生版本、openSUSE）、`.pkg.tar.zst`（Arch Linux 及其衍生版）、`.apk`（Alpine）、Nix |

Alpine 软件包包含 Rex 的 musl 构建版本。由于 Rex 在运行时需要加载 PAM，因此该版本采用动态链接而非静态链接。在其他发行版（包括其他基于 musl 的发行版）上，可以使用 `--tarball` 单独安装二进制文件，该选项在 musl 系统上会自动选择 musl 构建版本。

## 安装

**安装脚本（`install.sh`）**提供了一种便捷方式，可将 Rex 软件源添加至 apt、dnf、zypper、pacman 或 apk，并安装 `rex` 软件包，从而使更新能够随日常系统更新一同获取。再次运行该脚本可以升级 Rex，详见[升级](upgrading.md)。若要先行查看脚本将执行的操作，可在 `sh` 后添加 `-s -- --dry-run`。在 NixOS 以及其他未提供 Rex 软件源的发行版上，脚本会说明可选方案并退出。

| 选项 | 效果 |
| --- | --- |
| `--channel NAME` | 从 `stable`、`preview` 或 `snapshot` 通道安装。 |
| `--tarball` | 仅将 `rex` 二进制文件安装至 `/usr/local/bin`，不包含服务。需要 glibc 2.26 或更高版本，或者 musl（此时会安装 musl 构建版）。再次运行脚本即可更新。 |
| `--dry-run` | 打印将要执行的每条命令而不实际运行。 |

在 `sh -s --` 之后传递选项。例如，若要仅安装二进制文件而不安装服务：

```sh
curl -fsSL https://pkgs.superlogical.com/rex/install.sh | sh -s -- --tarball
```

## 发布通道

Rex 面向三个通道发布：

| 通道 | 包含内容 |
| --- | --- |
| `stable` | 正式发布的版本（目前暂无） |
| `preview` | 下一个发布版本的带标签预览版 |
| `snapshot` | 频繁构建的最新版本，可能不够稳定 |

安装脚本默认使用 `stable`，但在首个稳定版发布之前，会自动回退至 `preview` 并在输出中予以提示。

若要在日后切换通道，请修改软件源文件中的通道名称：在 `/etc/apt/sources.list.d/rex.sources` 中修改 `Suites:`，在 `/etc/yum.repos.d/rex.repo` 或 zypper 软件源中修改 `name` 与 `baseurl` 行，或在 `/etc/pacman.d/rex.conf` 中修改 `Server` 行。在 Alpine 上，如果软件源由安装脚本配置，请在 `/etc/apk/repositories.d/rex.list` 中修改；如果是自行添加的，请在 `/etc/apk/repositories` 的 Rex 行中修改，随后运行 `apk update`。

从 snapshot 切换至 preview 或 stable 会升级 Rex。切换回 snapshot 属于降级操作，需要显式指定。详见[切换通道与降级](upgrading.md#切换通道与降级)。

## 软件包内容

`rex` 软件包会安装以下内容：

| 路径 | 说明 |
| --- | --- |
| `/usr/bin/rex` | 服务端与 CLI 二进制文件，两者合二为一 |
| `rex.service` | 单个共享服务端，以 `rex` 账户运行。默认未启用。 |
| `rex.socket` | 当客户端首次连接时启动 `rex.service`。默认未启用。 |
| `rex-login-server.service` | 登录后为每个账户运行一个服务端。默认未启用。 |
| `rex-login-server.socket` | 当客户端首次连接时启动 `rex-login-server.service`。默认未启用。 |
| `rex` 账户与用户组 | 锁定的系统账户，主目录为 `/var/lib/rex` |
| `/etc/rex/accounts.jsonc` | 登录服务端的账户配置文件。初始为空，不接纳任何访问。 |
| `/etc/pam.d/rex-login-server` | 针对当前发行版的登录服务端 PAM 策略 |
| `xterm-rex` terminfo | Rex 的终端类型定义 |
| `/etc/ssh/ssh_config.d/50-rex.conf` | 当从 Rex 通过 SSH 连接至无法识别 `xterm-rex` 的主机时，回退至 `xterm-256color` |

若要运行服务端，请启用上述四个单元之一。每个套接字单元都会在客户端首次连接时启动其对应服务，而非在开机时启动。[服务端运行模式](server-modes.md)可协助进行选择。

在 Alpine 上，`/etc/init.d/rex` 与 `/etc/init.d/rex-login-server` 处的 OpenRC 脚本取代了这两个 systemd 服务。软件包不会提供 `/etc/conf.d/rex` 或 `/etc/conf.d/rex-login-server`，因此对服务的自定义配置写入这些文件中。

在 Arch 上，软件包通过 `/usr/lib/sysusers.d/rex.conf` 创建 `rex` 账户，并通过 `/usr/lib/tmpfiles.d/rex.conf` 创建其主目录。

升级会保留对账户文件和 PAM 策略所做的修改。详见[保留自定义修改](upgrading.md#保留自定义修改)。

### SSH 回退配置

`50-rex.conf` 使用 ssh 的 `SetEnv` 关键字设置 `TERM`，因此其行为取决于 OpenSSH 版本：

| OpenSSH | 行为表现 |
| --- | --- |
| 8.7 或更高版本 | ssh 向无法识别 `xterm-rex` 的主机发送 `xterm-256color`。 |
| 7.8 至 8.6 | ssh 会读取回退配置，但仍发送 `xterm-rex`。RHEL 8 包含 8.0。 |
| 低于 7.8 | ssh 会拒绝任何包含该回退配置的设定，导致所有 ssh 命令执行失败。Amazon Linux 2 包含 7.4，Ubuntu 18.04 包含 7.6。 |

`rex terminfo setup` 命令（无论是否携带 `--system`）都会首先检查版本。当 ssh 版本低于 7.8 时，该命令会安装 terminfo 条目，跳过回退配置，说明原因并以状态码 1 退出。由于软件包无法在安装时检查版本，因此会在所有环境中安装 `50-rex.conf`。在 Ubuntu 18.04 上这样做是安全的，仅因为其 ssh 从不读取该文件，具体说明见 [Debian 与 Ubuntu](#debian-与-ubuntu)。

若要检查 ssh 是否仍能正常解析其配置，请运行：

```sh
ssh -G example.com >/dev/null && echo ok
```

## Debian 与 Ubuntu

Debian 和 Ubuntu 提供了一个同样名为 `rex` 的不相关软件包：(R)?ex（一个 Perl 自动化框架）。安装脚本和 **Debian** 标签页将 Rex 软件源的优先级固定高于该软件包，因此 apt 会安装 Rex，并在已安装 (R)?ex 的情况下将其替换。

如果 `rex -v` 输出 `(R)?ex`，说明机器本身的 apt preferences 优先级覆盖了固定设置。运行 `apt-cache policy rex` 查看生效的规则，修复后重新运行安装脚本。

在 Ubuntu 18.04 上，`/etc/ssh/ssh_config` 没有 `Include` 行，因此 ssh 从不读取 `/etc/ssh/ssh_config.d/50-rex.conf`。其内置的 OpenSSH 7.6 版本过低，无法支持 [SSH 回退配置](#ssh-回退配置)。**切勿在 Ubuntu 18.04 上为 `/etc/ssh/ssh_config.d` 添加 `Include` 行。** 这会导致机器上所有账户的 ssh 均无法使用。

## Fedora 发行版

Fedora 将同名工具 (R)?ex 打包为 `Rex`。这两个软件包均占用 `/usr/bin/rex`，因此在安装 Rex 之前，请先使用 `sudo dnf remove Rex` 将其卸载。

## Amazon Linux 2 发行版

Amazon Linux 2 已于 2026-06-30 结束支持，其 rpm 和 systemd 版本过低，无法支持 Rex 软件包。因此安装脚本在该系统上仅安装 `rex` 二进制文件至 `/usr/local/bin`（行为同 `--tarball`），并输出相关提示。**Fedora** 标签页在 Amazon Linux 2 上无法使用，请直接使用安装脚本。Amazon Linux 2023 则与 Fedora 一样使用 Rex 软件源。

该系统上不提供系统服务和登录服务端。若要为你的账户启动[个人服务端](server-modes.md#个人服务端)，请运行：

```sh
rex server start
```

若要更新 Rex，再次运行安装脚本即可。已在运行的服务端会保持旧版本，直到停止运行。

如果脚本先前的运行遗留了 `/etc/yum.repos.d/rex.repo`，脚本会将其清理。由于其 OpenSSH 7.4 版本过低，无法支持 [SSH 回退配置](#ssh-回退配置)，因此 `rex terminfo setup` 仅会安装 terminfo 条目。

## Arch Linux 发行版

在 Arch 上，安装软件包的同时也会升级系统，因为 pacman 不支持部分升级。因此 **Arch Linux** 标签页和安装脚本都会运行 `pacman -Syu`。脚本同时还会传递 `--needed`，因此在 Rex 已是最新版本时再次运行，不会重新安装 Rex 或重启其服务。

在 `/etc/os-release` 中设置了 `ID_LIKE=arch` 的衍生版（例如 Manjaro、EndeavourOS、CachyOS 和 Garuda）安装方式完全相同。SteamOS 不支持此方式，因为其根文件系统为只读。Omarchy 需要一项调整，详见 [Omarchy 发行版](#omarchy-发行版)。

软件源中一次仅列出一个 Rex 版本，即该通道上的最新版本。较早的软件包保留在通道目录中，若要回退至某个版本，可将其 URL 传递给 `pacman -U`：

```sh
sudo pacman -U https://pkgs.superlogical.com/rex/arch/snapshot/x86_64/rex-VERSION-1-x86_64.pkg.tar.zst
```

如果先前从 AUR 安装了 `rex-bin`，请先使用 `sudo pacman -R rex-bin` 将其卸载。该包与 `rex` 冲突，安装脚本在将其移除前会中止执行。与 `rex` 不同，卸载 `rex-bin` 不会停止或禁用 Rex 单元，因此请先停止并禁用已启用的单元：

```sh
sudo systemctl disable --now rex.service rex.socket \
  rex-login-server.service rex-login-server.socket
```

### Omarchy 发行版

Omarchy 仅通过 `omarchy update` 升级系统，并会以 “Woah partner” 提示拦截 `pacman -Syu`。安装脚本能够妥善处理该情况。在 Omarchy 上，脚本会安装 Rex 而不升级其他内容，后续由 `omarchy update` 保持 Rex 更新。

若要手动安装，请运行 **Arch Linux** 标签页中的命令但跳过最后一行 `sudo pacman -Syu rex`，然后运行：

```sh
omarchy update
sudo pacman -S --needed rex
```

`omarchy refresh pacman` 和 `omarchy channel set` 会替换 `/etc/pacman.conf`，这会移除 Rex 软件源。Rex 会保持安装状态，但会暂停获取更新，直到再次运行安装脚本。

## Alpine 发行版

Alpine 默认未安装 `sudo`，因此请以 root 身份运行这些页面上的命令。Alpine 使用 OpenRC 代替 systemd。在页面提供 `systemctl` 命令之处，请使用对应的 OpenRC 形式：

| 在 systemd 上 | 在 Alpine 上 |
| --- | --- |
| `sudo systemctl enable --now rex.service` | `rc-update add rex`，然后 `rc-service rex start` |
| `sudo systemctl enable --now rex-login-server.service` | `rc-update add rex-login-server`，然后 `rc-service rex-login-server start` |
| `sudo systemctl reload rex-login-server.service` | `rc-service rex-login-server reload` |
| `sudo systemctl disable --now rex.service` | `rc-service rex stop`，然后 `rc-update del rex` |
| `sudo systemctl edit rex.service` | 在 `/etc/conf.d/rex` 中设置 `command_args` |
| `journalctl -u rex.service -f` | `tail -f /var/log/rex/server.log` |
| `journalctl -u rex-login-server.service` | `cat /var/log/rex-login-server.log` |
| `sudo usermod --append --groups rex alice` | `addgroup alice rex` |

OpenRC 不支持套接字激活，因此 `rex.socket` 与 `rex-login-server.socket` 在 Alpine 上没有对应形式。请直接使用服务本身。

`/etc/conf.d/rex` 是 OpenRC 在运行服务自身脚本之前读取的 shell 脚本，因此在该文件中设置的 `command_args` 会替换服务端的命令行参数。[共享服务端](shared-server.md)与[远程访问](remote-access.md)说明了应在其中填入的内容。

这些服务需要 OpenRC，完整的 Alpine 安装均包含该组件。容器镜像通常不包含。若要安装，请运行 `apk add openrc`。

在 musl 上，`who` 和 `last` 不会列出 Rex 会话，因为 musl 不维护 utmp 或 wtmp。`lastlog` 会照常记录登录信息。

## Nix 与 NixOS

Rex 为每个通道都提供了一个 flake，位于 `https://pkgs.superlogical.com/rex/nix/<channel>.tar.gz`。该 flake 针对 x86-64 和 ARM64 Linux 打包发布二进制文件，而非从源码构建 Rex。**Nix** 标签页可将其安装至你的 profile 中。较旧版本的 Nix 将 `nix profile add` 称为 `nix profile install`。

若要在不安装的情况下试用 Rex：

```sh
nix run https://pkgs.superlogical.com/rex/nix/snapshot.tar.gz -- --help
```

通道 URL 始终提供该通道上的最新版本，但 `flake.lock` 会记录确切版本，因此在发布更新版本后 lock 仍能正常工作。若要更新至最新版本，请运行 `nix flake update rex`。

### NixOS 模块

在 NixOS 上，将该 flake 作为 input 添加并导入 `rex.nixosModules.default`。该模块以 systemd 服务形式运行 Rex，提供软件包所附带的两种运行模式：

- `services.rex.enable` 以 `rex` 账户在 `/run/rex/server.sock` 上运行一个共享服务端。`rex` 用户组成员均可连接。
- `services.rex.loginServer.enable` 运行一个 root 进程，用于识别每个调用方，将其映射至对应账户，并以该账户身份为每个账户运行一个服务端。它在 `/run/rex/login-server.sock` 上监听。

这两种模式不能同时启用。任意一种模式都会为所有用户安装 `rex`，将 Rex 的终端类型放置在服务可找到的位置，并将 SSH 回退配置添加至 `/etc/ssh/ssh_config`。

`services.rex.socketActivation` 与 `services.rex.loginServer.socketActivation` 会通过 `rex.socket` 或 `rex-login-server.socket` 在客户端首次连接时启动服务端，而非在开机时启动。每项设置都需要对应模式的 `enable`，且 `services.rex.socketActivation` 还需要配置 Unix `socketPath`。该模块保持套接字单元与服务端的命令行一致。当启用 `tailscaleServe.enable` 时，套接字单元还会容纳 Serve 套接字，因此通过 Tailscale Serve 发起的请求也会启动服务端。

与软件包附带的服务不同，该模块的服务需要对应的套接字单元，因此单独停止 `rex.socket` 也会停止服务端。开启或关闭任一选项都会在下一次 `nixos-rebuild switch` 时重启正在运行的服务端，这会终止共享服务端上的所有会话。

供单个用户使用的共享服务端配置：

```nix
{
  inputs.rex.url = "https://pkgs.superlogical.com/rex/nix/snapshot.tar.gz";

  outputs = { nixpkgs, rex, ... }: {
    nixosConfigurations.myhost = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [
        rex.nixosModules.default
        {
          services.rex.enable = true;
          users.users.alice = {
            isNormalUser = true;
            extraGroups = [ "rex" ];
          };
        }
      ];
    };
  };
}
```

允许 Alice 通过 Tailscale Serve 使用其自有账户的登录服务端。该模块会将账户写入 `/etc/rex/accounts.jsonc`，但不会创建这些系统账户：

```nix
{
  services.tailscale.enable = true;
  users.users.alice.isNormalUser = true;

  services.rex.loginServer = {
    enable = true;
    accounts.alice.principals = [ "tailscale:alice@example.com" ];
    tailscaleServe.enable = true;
  };
}
```

主机必须已登录 Tailscale，且 tailnet 已启用 HTTPS。修改账户配置会重新加载登录服务端而不会终止会话。对应账户不再受允许的连接会被关闭。

### home-manager 模块

home-manager 模块可为你的自有账户配置 Rex。它适用于任何带有 Nix 和 systemd 的 Linux 系统（例如 Fedora 或 Amazon Linux 2023），而不仅限于 NixOS。添加该 flake 作为 input 并导入 `rex.homeManagerModules.default`。该模块也以 `rex.homeModules.default` 导出，以满足某些配置所期望的名称。

在多次会话之间持续运行的个人服务端：

```nix
{
  inputs.rex.url = "https://pkgs.superlogical.com/rex/nix/snapshot.tar.gz";

  outputs = { home-manager, nixpkgs, rex, ... }: {
    homeConfigurations.alice = home-manager.lib.homeManagerConfiguration {
      pkgs = nixpkgs.legacyPackages.x86_64-linux;
      modules = [
        rex.homeManagerModules.default
        {
          home.username = "alice";
          home.homeDirectory = "/home/alice";
          home.stateVersion = "26.05";

          programs.rex.enable = true;
          services.rex.enable = true;

          # 仅当启用此项时，home-manager 才会写入 ~/.ssh/config，
          # 且 programs.rex 会将 SSH 回退配置追加至其中。
          programs.ssh.enable = true;
        }
      ];
    };
  };
}
```

该模块包含两部分：

| 选项 | 效果 |
| --- | --- |
| `programs.rex.enable` | 安装 `rex`，将 `xterm-rex` terminfo 条目写入 `~/.terminfo`，并将 SSH 回退配置添加至 `~/.ssh/config`。`programs.rex.config` 会写入 `~/.config/rex/init.lua`。 |
| `services.rex.enable` | 以你的账户身份在名为 `rex` 的 systemd 用户服务中运行[个人服务端](server-modes.md#个人服务端)。同时也会开启 `programs.rex`。 |

SSH 回退配置需要 `programs.ssh.enable = true`。若未启用，模块会输出警告，此时可改为运行一次 `rex terminfo setup`。在模块已配置的情况下运行 `rex terminfo setup` 是无害的。它会检测到 home-manager 已经包含的保护配置，且不会向 ssh 配置中写入任何内容，`rex terminfo status` 会报告该保护配置已生效。

与 `rex terminfo setup` 不同，该模块不会检查 OpenSSH 版本。在低于 7.8 的 ssh 上，请设置 `programs.rex.sshGuard = false`，因为 [SSH 回退配置](#ssh-回退配置)会导致所有 ssh 命令执行失败。

该服务使用与所有 `rex` 命令相同的套接字，因此 `rex ls`、`rex server status` 和 `rex server stop` 均会连接至该服务。如果服务异常退出，systemd 会将其重启，但在执行 `rex server stop` 后不会重启。若要重新启动，请运行 `systemctl --user start rex`。该命令会在服务端开始接受连接后返回，因此紧随其后运行的 `rex` 命令能够正常执行。其日志可通过 `journalctl --user -u rex` 查看。

该服务在你登录时启动，在注销时停止，注销会终止所有会话。`home-manager switch` 每次都会就此输出警告。若要在开机时启动并在注销后保持运行，请运行一次以下命令：

```sh
loginctl enable-linger
```

关于远程访问，`services.rex.tailscale.enable` 可开启[内置 Tailscale](remote-access.md#内置-tailscale)。`authKeyFile` 需要 systemd 250 或更高版本（Fedora 36、Amazon Linux 2023）。其他选项（例如 `extraListen`、`blockDirs` 和 `maxSessions`）在 flake 自带的 `home-manager-module.nix` 中有所说明。

在 macOS 上，仅需启用 `programs.rex`。Rex 应用会自行运行服务端，因此在该平台上启用 `services.rex` 会因报错而中止构建。

[共享服务端](shared-server.md)与[登录服务端](login-server.md)需要 root 权限，因此 home-manager 无法运行它们。请使用 NixOS 模块或软件包。
