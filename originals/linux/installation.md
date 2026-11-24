---
title: "Installing on Linux"
canonical_url: https://www.superlogical.com/rex/docs/linux/installation
---

# Installing on Linux

Rex can run as a server on Linux so that clients can access it as a remote
host.

**IMPORTANT:** Rex on Linux is in testing. The install commands show below
once you've logged in with Discord.

## Quickstart

This section documents the recommended setup to get up and running quickly.
It reaches your own personal server from your clients over SSH, with nothing
else to set up. We recommend you read the later sections, and
[Remote Access](https://www.superlogical.com/rex/docs/linux/remote-access.md#ssh), to understand the details and
other access options.

1. On the Linux machine, install Rex as [Install](#install) shows.

2. Start your personal server at boot, and keep it running while you're
   logged out. This needs no sudo, run it as the user you want to connect
   with:

   ```sh
   rex server install
   ```

   Without systemd, such as on Alpine, skip this step. A server that the
   first connection starts then runs until the machine restarts.

3. Check that you can log in with your SSH key from your client, and that
   SSH finds `rex` there:

   ```sh
   ssh alice@build.example.com rex version
   ```

4. Connect from your client:

   ```sh
   rex -S ssh://alice@build.example.com ls
   ```

   In Rex for Mac, choose **Add Remote Host…** and enter
   `ssh://alice@build.example.com`.

If several people need Rex on one machine, see
[Server Modes](https://www.superlogical.com/rex/docs/linux/server-modes.md).

## System Requirements

| Requirement  | Supported                                                                 |
| ------------ | ------------------------------------------------------------------------- |
| Architecture | x86-64 with SSE4.2, ARM64                                                 |
| C library    | glibc 2.26 or later (Amazon Linux 2, Ubuntu 18.04, Debian 10, RHEL 8, or newer), or musl on Alpine 3.21 or later |
| Init system  | systemd, or OpenRC on Alpine, for the shared server and the login server. The `rex` command runs without either. |
| Packages     | `.deb` (Debian, Ubuntu), `.rpm` (Fedora, RHEL and its rebuilds, openSUSE), `.pkg.tar.zst` (Arch Linux and derivatives), `.apk` (Alpine), Nix |

The Alpine package holds the musl build of Rex. It's dynamically linked,
not static, because Rex loads PAM at run time. On other distributions,
including other musl ones, install the binary alone with `--tarball`, which
picks the musl build on a musl system.

## Install


The **install script (`install.sh`)** is a convenience that adds the Rex
repository to apt, dnf, zypper, pacman, or apk and installs the `rex`
package, so updates arrive with your normal system updates. Running it
again upgrades Rex, as [Upgrading](https://www.superlogical.com/rex/docs/linux/upgrading.md) covers. To see what it
would do first, add `-s -- --dry-run` after `sh`. On NixOS and other
distributions without a Rex repository, it explains the options and exits.

``

| Option           | Effect                                                                   |
| ---------------- | ------------------------------------------------------------------------ |
| `--channel NAME` | Install from `stable`, `preview`, or `snapshot`.                         |
| `--tarball`      | Install only the `rex` binary, into `/usr/local/bin`, with no services. Needs glibc 2.26 or later, or musl, where it installs the musl build. Run the script again to update. |
| `--dry-run`      | Print every command without running it.                                  |

Pass options after `sh -s --`. For example, to install only the binary,
with no services:

```sh
curl -fsSL https://pkgs.superlogical.com/rex/install.sh | sh -s -- --tarball
```

## Channels

Rex publishes to three channels:

| Channel    | What it gets                         |
| ---------- | ------------------------------------ |
| `stable`   | Tagged releases (none right now)                      |
| `preview`  | Tagged previews of the next release  |
| `snapshot` | A frequent, likely unstable build              |

The install script defaults to `stable` but until the first stable
release exists, will fall back to `preview` and say so in the output.

To switch channels later, change the channel name in the repository file:
`Suites:` in `/etc/apt/sources.list.d/rex.sources`, or the `name` and
`baseurl` lines in `/etc/yum.repos.d/rex.repo` or zypper's repository, or
the `Server` line in `/etc/pacman.d/rex.conf`. On Alpine, change it in
`/etc/apk/repositories.d/rex.list` if the install script set up the
repository, or in the Rex line in `/etc/apk/repositories` if you added it
yourself, then run `apk update`.

Moving from snapshot to preview or stable upgrades Rex. Moving back to
snapshot is a downgrade, which you have to ask for. See
[Switching Channels and Downgrading](https://www.superlogical.com/rex/docs/linux/upgrading.md#switching-channels-and-downgrading).

## Package Contents

The `rex` package installs:

| Path                                | What it is                                                         |
| ----------------------------------- | ------------------------------------------------------------------ |
| `/usr/bin/rex`                      | The server and the CLI, in one binary                              |
| `rex.service`                       | One shared server, run as the `rex` account. Not enabled.          |
| `rex.socket`                        | Starts `rex.service` when a client first connects. Not enabled.    |
| `rex-login-server.service`          | One server per account, after a login. Not enabled.                |
| `rex-login-server.socket`           | Starts `rex-login-server.service` when a client first connects. Not enabled. |
| `rex` account and group             | A locked system account, with its home at `/var/lib/rex`           |
| `/etc/rex/accounts.jsonc`           | The login server's accounts. It ships empty, which admits nobody.  |
| `/etc/pam.d/rex-login-server`       | The login server's PAM policy, for your distribution               |
| `xterm-rex` terminfo                | Rex's terminal type                                                |
| `/etc/ssh/ssh_config.d/50-rex.conf` | Falls back to `xterm-256color` when you SSH from Rex to a host that doesn't know `xterm-rex` |

To run a server, enable one of the four units. Each socket starts its
service the first time a client connects, instead of at boot.
[Server Modes](https://www.superlogical.com/rex/docs/linux/server-modes.md) helps you choose.

On Alpine, OpenRC scripts at `/etc/init.d/rex` and
`/etc/init.d/rex-login-server` take the place of the two services. The
package never ships `/etc/conf.d/rex` or `/etc/conf.d/rex-login-server`,
so your changes to the services go there.

On Arch, the package creates the `rex` account through
`/usr/lib/sysusers.d/rex.conf`, and its home through
`/usr/lib/tmpfiles.d/rex.conf`.

Upgrades keep your changes to the accounts file and the PAM policy. See
[Keeping Your Changes](https://www.superlogical.com/rex/docs/linux/upgrading.md#keeping-your-changes).

### The SSH Fallback

`50-rex.conf` sets `TERM` with ssh's `SetEnv` keyword, so what it does
depends on your OpenSSH version:

| OpenSSH        | What happens                                                             |
| -------------- | ------------------------------------------------------------------------ |
| 8.7 or later   | ssh sends `xterm-256color` to hosts that don't know `xterm-rex`.         |
| 7.8 to 8.6     | ssh reads the fallback but still sends `xterm-rex`. RHEL 8 has 8.0.      |
| Older than 7.8 | ssh rejects any configuration that contains the fallback, so every ssh command fails. Amazon Linux 2 has 7.4, Ubuntu 18.04 has 7.6. |

`rex terminfo setup`, with or without `--system`, checks the version
first. On an ssh older than 7.8, it installs the terminfo entry, skips the
fallback, says why, and exits with status 1. The package can't check, so
it installs `50-rex.conf` everywhere. That's safe on Ubuntu 18.04 only
because its ssh never reads the file, as
[Debian and Ubuntu](#debian-and-ubuntu) explains.

To check that ssh still parses its configuration, run:

```sh
ssh -G example.com >/dev/null && echo ok
```

## Debian and Ubuntu

Debian and Ubuntu ship an unrelated package also named `rex`: (R)?ex, a
Perl automation framework. The install script and the **Debian** tab pin
the Rex repository above it, so apt installs Rex, and replaces (R)?ex if
it's already installed.

If `rex -v` prints `(R)?ex`, your machine's own apt preferences outranked
the pin. Run `apt-cache policy rex` to see which rule won, fix it, then run
the install script again.

On Ubuntu 18.04, `/etc/ssh/ssh_config` has no `Include` line, so ssh never
reads `/etc/ssh/ssh_config.d/50-rex.conf`. Its OpenSSH 7.6 is too old for
[the SSH fallback](#the-ssh-fallback). **Don't add an `Include` line for
`/etc/ssh/ssh_config.d` on Ubuntu 18.04.** It breaks ssh for every account
on the machine.

## Fedora

Fedora ships (R)?ex, the same unrelated tool, as `Rex`. Both packages own
`/usr/bin/rex`, so remove it with `sudo dnf remove Rex` before you install
Rex.

## Amazon Linux 2

Amazon Linux 2 reached the end of its support on 2026-06-30, and its rpm
and systemd are too old for the Rex package. So the install script installs
only the `rex` binary there, into `/usr/local/bin`, as `--tarball` does,
and prints a notice saying so. The **Fedora** tab doesn't work on Amazon
Linux 2, so use the install script. Amazon Linux 2023 uses the Rex
repository, like Fedora.

There are no services and no login server. To start a
[personal server](https://www.superlogical.com/rex/docs/linux/server-modes.md#personal-server) for your account,
run:

```sh
rex server start
```

To update Rex, run the install script again. A server that's already
running keeps the old version until it stops.

If an earlier run of the script left `/etc/yum.repos.d/rex.repo` behind,
the script removes it. Its OpenSSH 7.4 is too old for
[the SSH fallback](#the-ssh-fallback), so `rex terminfo setup` installs
only the terminfo entry.

## Arch Linux

On Arch, installing a package also upgrades the system, because pacman
doesn't support partial upgrades. So the **Arch Linux** tab and the install
script both run `pacman -Syu`. The script also passes `--needed`, so running
it again with Rex up to date doesn't reinstall Rex or restart its services.

Derivatives that set `ID_LIKE=arch` in `/etc/os-release`, such as Manjaro,
EndeavourOS, CachyOS, and Garuda, install the same way. SteamOS doesn't,
because its root file system is read-only. Omarchy needs one change, which
[Omarchy](#omarchy) covers.

The repository lists one version of Rex at a time, the newest on its
channel. Older packages stay in the channel's directory, so to go back to
one, pass its URL to `pacman -U`:

```sh
sudo pacman -U https://pkgs.superlogical.com/rex/arch/snapshot/x86_64/rex-VERSION-1-x86_64.pkg.tar.zst
```

If you installed `rex-bin` from the AUR, remove it first with
`sudo pacman -R rex-bin`. It conflicts with `rex`, so the install script
stops until it's gone. Unlike `rex`, removing `rex-bin` doesn't stop or
disable the Rex units, so stop and disable any you enabled first:

```sh
sudo systemctl disable --now rex.service rex.socket \
  rex-login-server.service rex-login-server.socket
```

### Omarchy

Omarchy upgrades the system only through `omarchy update`, and it cancels
`pacman -Syu` with a "Woah partner" message. The install script handles
this. On Omarchy, it installs Rex without upgrading anything else, and
`omarchy update` keeps Rex up to date from then on.

To install by hand, run the **Arch Linux** tab without its last line,
`sudo pacman -Syu rex`, then run:

```sh
omarchy update
sudo pacman -S --needed rex
```

`omarchy refresh pacman` and `omarchy channel set` replace
`/etc/pacman.conf`, which removes the Rex repository. Rex stays installed
but stops getting updates until you run the install script again.

## Alpine

Alpine has no `sudo` by default, so run the commands on these pages as
root. Alpine uses OpenRC instead of systemd. Where a page gives a
`systemctl` command, use the OpenRC form:

| On systemd                                             | On Alpine                                                          |
| ------------------------------------------------------ | ------------------------------------------------------------------ |
| `sudo systemctl enable --now rex.service`              | `rc-update add rex`, then `rc-service rex start`                   |
| `sudo systemctl enable --now rex-login-server.service` | `rc-update add rex-login-server`, then `rc-service rex-login-server start` |
| `sudo systemctl reload rex-login-server.service`       | `rc-service rex-login-server reload`                               |
| `sudo systemctl disable --now rex.service`             | `rc-service rex stop`, then `rc-update del rex`                    |
| `sudo systemctl edit rex.service`                      | Set `command_args` in `/etc/conf.d/rex`                            |
| `journalctl -u rex.service -f`                         | `tail -f /var/log/rex/server.log`                                  |
| `journalctl -u rex-login-server.service`               | `cat /var/log/rex-login-server.log`                                |
| `sudo usermod --append --groups rex alice`             | `addgroup alice rex`                                               |

OpenRC has no socket activation, so `rex.socket` and
`rex-login-server.socket` have no Alpine form. Use the services instead.

`/etc/conf.d/rex` is a shell script that OpenRC reads before the service's
own script, so a `command_args` set there replaces the server's command
line. [Shared Server](https://www.superlogical.com/rex/docs/linux/shared-server.md) and
[Remote Access](https://www.superlogical.com/rex/docs/linux/remote-access.md) show what to put in it.

The services need OpenRC, which a full Alpine install has. Containers
often don't. To install it, run `apk add openrc`.

On musl, `who` and `last` don't list Rex sessions, because musl keeps no
utmp or wtmp. `lastlog` records logins as usual.

## Nix and NixOS

Rex has a flake for each channel, at
`https://pkgs.superlogical.com/rex/nix/<channel>.tar.gz`. It packages the
release binary rather than building Rex from source, for x86-64 and ARM64
Linux. The **Nix** tab installs it into your profile. Older versions of
Nix call `nix profile add` by its old name, `nix profile install`.

To try Rex without installing it:

```sh
nix run https://pkgs.superlogical.com/rex/nix/snapshot.tar.gz -- --help
```

The channel URL always serves the newest release on its channel, but
`flake.lock` records the exact release, so a lock keeps working after newer
releases come out. To move to the newest one, run `nix flake update rex`.

### The NixOS Module

On NixOS, add the flake as an input and import `rex.nixosModules.default`.
The module runs Rex as a systemd service in one of two modes, the same two
the packages ship:

- `services.rex.enable` runs one shared server as the `rex` account, on
  `/run/rex/server.sock`. Members of the `rex` group can connect.
- `services.rex.loginServer.enable` runs one root process that identifies
  each caller, maps them to an account, and runs a server per account as
  that account. It listens on `/run/rex/login-server.sock`.

They can't both be on. Either mode also installs `rex` for every user, puts
Rex's terminal type where the service can find it, and adds the SSH
fallback to `/etc/ssh/ssh_config`.

`services.rex.socketActivation` and
`services.rex.loginServer.socketActivation` start the server the first time
a client connects, through `rex.socket` or `rex-login-server.socket`,
instead of at boot. Each needs its mode's `enable`, and
`services.rex.socketActivation` also needs a Unix `socketPath`. The module
keeps the socket unit and the server's command line in agreement. With
`tailscaleServe.enable`, the socket unit holds the Serve socket too, so a
request through Tailscale Serve also starts the server.

Unlike the packages' services, the module's services require their
sockets, so stopping `rex.socket` alone stops the server too. Turning
either option on or off restarts a running server at the next
`nixos-rebuild switch`, which ends every session on a shared server.

A shared server that one person can use:

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

A login server that lets Alice use her own account over Tailscale Serve.
The module writes the accounts to `/etc/rex/accounts.jsonc`, but doesn't
create them:

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

The host must be logged in to Tailscale, with HTTPS enabled for the
tailnet. Changes to the accounts reload the login server without ending
sessions. Connections whose account is no longer allowed are closed.

### The home-manager Module

The home-manager module sets up Rex for your own account. It works on any
Linux with Nix and systemd, such as Fedora or Amazon Linux 2023, not only
on NixOS. Add the flake as an input and import
`rex.homeManagerModules.default`. It's also exported as
`rex.homeModules.default`, the name some setups expect.

A personal server that keeps running between sessions:

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

          # home-manager writes ~/.ssh/config only when this is on, and
          # programs.rex adds the SSH fallback to it.
          programs.ssh.enable = true;
        }
      ];
    };
  };
}
```

The module has two parts:

| Option                | Effect                                                                   |
| --------------------- | ------------------------------------------------------------------------ |
| `programs.rex.enable` | Installs `rex`, writes the `xterm-rex` terminfo entry to `~/.terminfo`, and adds the SSH fallback to `~/.ssh/config`. `programs.rex.config` writes `~/.config/rex/init.lua`. |
| `services.rex.enable` | Runs a [personal server](https://www.superlogical.com/rex/docs/linux/server-modes.md#personal-server) as your account, in a systemd user service named `rex`. Also turns on `programs.rex`. |

The SSH fallback needs `programs.ssh.enable = true`. Without it, the module
prints a warning, and you can run `rex terminfo setup` once instead.
Running `rex terminfo setup` with the module in place is harmless.
It sees the guard home-manager already includes and
writes nothing to your ssh configuration, and `rex terminfo status` reports
that guard as in effect.

Unlike `rex terminfo setup`, the module doesn't check your OpenSSH
version. On an ssh older than 7.8, set `programs.rex.sshGuard = false`,
because [the SSH fallback](#the-ssh-fallback) breaks every ssh command
there.

The service uses the same socket as every `rex` command, so `rex ls`,
`rex server status`, and `rex server stop` all reach it. systemd restarts
it if it fails, but not after `rex server stop`. To start it again, run
`systemctl --user start rex`. It returns once the server is accepting
connections, so a `rex` command you run right after it works. Its log is in
`journalctl --user -u rex`.

The service starts when you log in and stops when you log out, which ends
every session. `home-manager switch` warns about this each time. To start it
at boot and keep it running while you're logged out, run this once:

```sh
loginctl enable-linger
```

For remote access, `services.rex.tailscale.enable` turns on
[built-in Tailscale](https://www.superlogical.com/rex/docs/linux/remote-access.md#built-in-tailscale).
`authKeyFile` needs systemd 250 or later (Fedora 36, Amazon Linux 2023).
The other options, such as `extraListen`, `blockDirs`, and `maxSessions`,
are described in `home-manager-module.nix`, which comes with the flake.

On macOS, turn on only `programs.rex`. The Rex app runs the server, so
`services.rex` stops the build with an error there.

The [shared server](https://www.superlogical.com/rex/docs/linux/shared-server.md) and the
[login server](https://www.superlogical.com/rex/docs/linux/login-server.md) need root, so home-manager can't run
them. Use the NixOS module, or the packages.
