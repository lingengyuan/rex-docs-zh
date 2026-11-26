---
title: "Upgrading"
canonical_url: https://www.superlogical.com/rex/docs/linux/upgrading
---

# Upgrading

You can upgrade Rex using your standard package manager that you installed
with. If you used the `install.sh` script, running that again is also safe;
it merely detects and invokes your package manager.

On Linux, `install.sh` and standard package managers auto-restart
the running server. On FreeBSD and Windows, nothing restarts automatically;
you must manually restart the server into the latest version. See
[FreeBSD](#freebsd) and [Windows](#windows).

**Upgrading ends every program running on a shared server.** Its sessions
are restored. The login server and personal servers keep their sessions
running. See [What Restarts](#what-restarts).

## Upgrading the Package

| Installed with   | Upgrade                                                            |
| ---------------- | ------------------------------------------------------------------ |
| Debian, Ubuntu   | `sudo apt-get update && sudo apt-get install --only-upgrade rex`   |
| Fedora, RHEL     | `sudo dnf upgrade --refresh rex`                                   |
| openSUSE         | `sudo zypper update rex`                                           |
| Arch Linux       | `sudo pacman -Syu`                                                 |
| Omarchy          | `omarchy update`                                                   |
| Alpine           | `apk update && apk add -u rex`                                     |
| FreeBSD          | `pkg upgrade -r rex rex`                                           |
| Nix profile      | `nix profile upgrade --regex '.*superlogical.*'`                   |
| Install script   | Run the same command you installed with.                           |
| `--tarball`      | Run the install script again with `--tarball`.                     |
| Amazon Linux 2   | Run the install script again.                                      |
| Windows          | See [Windows](#windows).                                           |

When you run the install script again, pass the same `--channel` you
installed with. Without it, the script switches the repository to the
default channel.

## What Restarts

The package restarts the Rex services that are running, and leaves stopped
ones stopped. In containers without a running init system, it restarts
nothing, and neither does the FreeBSD package. See [FreeBSD](#freebsd).

The package never restarts `rex.socket` or `rex-login-server.socket`. A
server that a socket started restarts like any other, and one that hasn't
started yet runs the new version when the first client connects. If a new
version changes a socket unit, the change applies once you stop the socket
and its service and start the socket again, or at the next reboot.

| Server          | On upgrade        | Sessions | Runs the new version    |
| --------------- | ----------------- | -------- | ----------------------- |
| Shared server   | Restarts          | Restored | Right away              |
| Login server    | Restarts          | Survive  | Right away              |
| Account servers | Keep running      | Survive  | When their sessions end |
| Personal server | Keeps running     | Survive  | When it stops           |

**Restarting the shared server ends every program in its sessions.** The
sessions are [restored](https://www.superlogical.com/rex/docs/features/session-restore.md), each pane with a new
shell, and only programs that can resume come back. Upgrade when nobody has
work running, or [hold the package](#holding-an-upgrade) until then.

The servers the login server starts for each account keep running the
version they started with. Each one stops around 10 seconds after its last
session ends and its last client disconnects, and the next connection
starts it again on the new version. On machines with systemd-logind, a
person can switch sooner by running `rex server stop` on the machine as
themselves, which ends their sessions.

A personal server that a `rex` command started stops on its own once it's
idle, so it picks up the new version by itself. One started with
`rex server start` keeps running the old version until you stop it and
start it again:

```sh
rex server stop
rex server start
```

## Checking the Version

`rex version` shows the version that's installed, and `rex server status`
shows the version of the server that's running:

```sh
rex version
rex server status
```

If the first line of `rex version` doesn't match the `version:` line of
`rex server status`, that server is still running the old version. Through
the login server, `rex server status` shows the version of your account's
server.

## Holding an Upgrade

To keep Rex at its current version until you're ready:

| Package manager | Hold                          | Release                         |
| --------------- | ----------------------------- | ------------------------------- |
| apt             | `sudo apt-mark hold rex`      | `sudo apt-mark unhold rex`      |
| dnf             | `sudo dnf versionlock add rex` | `sudo dnf versionlock delete rex` |
| zypper          | `sudo zypper addlock rex`     | `sudo zypper removelock rex`    |
| pacman          | Add `IgnorePkg = rex` under `[options]` in `/etc/pacman.conf` | Remove that line |
| apk             | `apk add rex=VERSION`         | `apk add -u rex`                |
| pkg             | `pkg lock rex`                | `pkg unlock rex`                |

On RHEL and its rebuilds, `versionlock` is a plugin. Install it with
`sudo dnf install 'dnf-command(versionlock)'`. Fedora has it built in.

On Alpine, `VERSION` is the full version, such as `0.1.0-r0`.
`apk info -e -v rex` shows the one that's installed.

## Keeping Your Changes

Upgrades keep your changes to:

- The accounts file, `/etc/rex/accounts.jsonc`
- The PAM policy, `/etc/pam.d/rex-login-server`
- Drop-ins for `rex.service`, `rex-login-server.service`, and their sockets
- `/etc/conf.d/rex` and `/etc/conf.d/rex-login-server` on Alpine
- `/etc/rc.conf` on FreeBSD

Upgrades replace the services themselves, `rex.service`,
`rex-login-server.service`, `rex.socket`, `rex-login-server.socket`, the
scripts in `/etc/init.d`, and the scripts in `/usr/local/etc/rc.d` on
FreeBSD. On FreeBSD, they replace the PAM policy too. See
[FreeBSD](#freebsd). Put your changes in a drop-in or `/etc/conf.d`
instead, as
[Customizing the Service](https://www.superlogical.com/rex/docs/linux/shared-server.md#customizing-the-service)
shows.

If you changed a config file and a new version of Rex changes it too, you
keep yours, and the new one is saved beside it:

| Package manager | New file saved as | Notes                                           |
| --------------- | ----------------- | ----------------------------------------------- |
| apt             | `.dpkg-dist`      | apt asks first. The install script doesn't ask. |
| dnf, zypper     | `.rpmnew`         |                                                 |
| apk             | `.apk-new`        |                                                 |
| pkg             | `.sample`         | Only the accounts file. pkg updates the sample on every upgrade. |

Compare the two and copy over any changes you want. The SSH fallback,
`/etc/ssh/ssh_config.d/50-rex.conf`, is the exception on dnf and zypper: an
upgrade replaces it and saves yours as `.rpmsave`.

## Client and Server Versions

Rex for Mac and the server don't need to be the same version, and either
one can be newer. A newer client can't use features an older server
doesn't have. When it needs one, it says so:

```
this server is too old for rex client ls; it needs Rex 0.1.0 or later
```

If the two are too far apart to work together at all, the server refuses
the connection, and the message ends with `update the server` or
`update the client`.

## Switching Channels and Downgrading

[Switching channels](https://www.superlogical.com/rex/docs/linux/installation.md#channels) from snapshot to preview
or stable upgrades Rex as usual. Switching back to snapshot is a downgrade,
because snapshot versions sort below every release. A downgrade doesn't
happen on its own, so ask for the version you want:

| Package manager | List versions                       | Downgrade                                         |
| --------------- | ----------------------------------- | ------------------------------------------------- |
| apt             | `apt-cache madison rex`             | `sudo apt-get install --allow-downgrades rex=VERSION` |
| dnf             | `dnf list --showduplicates rex`     | `sudo dnf downgrade rex-VERSION`                  |
| zypper          | `zypper search -s -x rex`           | `sudo zypper install --oldpackage rex-VERSION`    |
| pacman          | One version only. See [Arch Linux](https://www.superlogical.com/rex/docs/linux/installation.md#arch-linux). | `sudo pacman -U URL`        |
| apk             | `apk search -a -x rex`              | `apk add rex=VERSION`                             |
| pkg             | One version only. See [FreeBSD](#freebsd). | See [FreeBSD](#freebsd).                   |

A downgrade restarts services the same way an upgrade does. Your data is
safe across a downgrade. A version of Rex that finds data written in a
newer format refuses to use it instead of overwriting it.

## Changing How Rex Is Installed

Keep one copy of Rex on a machine. The `--tarball` binary in
`/usr/local/bin` comes before the package's `/usr/bin/rex` on the usual
`PATH`, so with both installed, `rex` commands and the personal servers
they start run the tarball's version, whichever one you upgrade. To see
every `rex` on your `PATH`:

```sh
which -a rex
```

To move from `--tarball` to a package, install the package, then remove
the binary:

```sh
sudo rm /usr/local/bin/rex
```

To move from a package to `--tarball` or Nix, remove the package first:

| Package manager | Remove                    |
| --------------- | ------------------------- |
| apt             | `sudo apt-get remove rex` |
| dnf             | `sudo dnf remove rex`     |
| zypper          | `sudo zypper remove rex`  |
| pacman          | `sudo pacman -R rex`      |
| apk             | `apk del rex`             |
| pkg             | `pkg delete rex`          |

Removing the package stops and disables its services and sockets, which
ends every session on the shared server. `rex-bin` from the AUR doesn't, so
stop and disable them yourself first. See
[Arch Linux](https://www.superlogical.com/rex/docs/linux/installation.md#arch-linux).

Removing the package keeps `/var/lib/rex` and the `rex` account, so
installing the package again picks up the shared server's data. On
FreeBSD, it keeps `/var/db/rex`, and your settings in `/etc/rc.conf`.

The install script and the commands on the other install tabs set up the
same repository, so you can switch between them. On Alpine, the script
puts the repository in `/etc/apk/repositories.d/rex.list`, and the
**Alpine** tab adds it to `/etc/apk/repositories`. Keep only one of them.

## NixOS

Update the Rex input in your flake, then switch:

```sh
nix flake update rex
sudo nixos-rebuild switch --flake .
```

`nixos-rebuild switch` restarts the Rex service when Rex changes, the same
as a package upgrade: the shared server's programs end, and account servers
keep the old version until their sessions end.

`flake.lock` holds Rex at its current version until you update it, so
there's nothing else to do to hold an upgrade.

## FreeBSD

pkg can't restart services, so after an upgrade, the services that were
running keep the old version. pkg says which ones at the end of its output,
and so does the install script. Restart each one when you're ready:

```sh
service rex restart
service rex-login-server restart
```

**Restarting `rex` ends every program on the shared server**, the same as
on Linux. Its sessions are restored. Restarting `rex-login-server` keeps
each account's server and its sessions, and they keep the old version until
their sessions end.

Upgrades keep your changes to the accounts file, but replace the PAM policy
in `/usr/local/etc/pam.d`. To change the policy, edit a copy in
`/etc/pam.d` instead, as [Login Server](https://www.superlogical.com/rex/docs/linux/login-server.md#freebsd) shows.

pkg doesn't downgrade with `pkg install`, so delete the newer version
first. Deleting stops both services, which ends every session on the
shared server:

```sh
pkg delete rex
pkg install -r rex rex
```

The repository lists one version of Rex at a time, the newest on its
channel. Older packages stay in the channel's directory, so to go back to
one, pass its URL to `pkg add`, then [hold it](#holding-an-upgrade):

```sh
pkg delete rex
pkg add https://pkgs.superlogical.com/rex/freebsd/snapshot/amd64/rex-VERSION.pkg
pkg lock rex
```

`VERSION` is the full version, such as `0.1.0.alpha2514`. On ARM64, use
`aarch64` in place of `amd64`. `pkg info rex` shows the one that's
installed.

## Windows

Upgrade Rex the same way you installed it:

| Installed with        | Upgrade                                                              |
| --------------------- | -------------------------------------------------------------------- |
| WinGet                | `winget upgrade --id Superlogical.RexServer.Preview --source rex`    |
| Manual MSI | Download the new [MSI](https://www.superlogical.com/rex/docs/windows/installation.md#msi) and run it.         |
| Manual Zip| Stop the server, then extract the new zip over the old folder.        |

**Stop the server before you upgrade with WinGet.** WinGet can't replace
the files of a running server, so the upgrade fails with "Access is
denied" and Rex stays at the old version.

In all cases, nothing automatically restarts. How you restart your server
depends on how it was started, as
[Server Lifetimes](https://www.superlogical.com/rex/docs/windows/running.md#server-lifetimes) explains:

| Started by                  | To run the new version                                         |
| --------------------------- | -------------------------------------------------------------- |
| Any `rex` command           | Nothing. It stops once it's idle, and the next command starts the new version. |
| `rex server start`          | `rex server stop`, then `rex server start`                     |
| `rex server install --user` | `rex server stop`, then `rex server install --user`, or sign in again |
| `rex server install`        | `rex server stop`, then `sc.exe start RexServer-<SID>`         |

`sc.exe start` needs a terminal opened with **Run as administrator**. See
[Stopping and Restarting](https://www.superlogical.com/rex/docs/windows/running.md#stopping-and-restarting).

**Warning! Restarting the server ends every program running in its sessions.**
The server saves its session layouts but the programs that were running
in them don't come back today.

### Holding an Upgrade

To keep WinGet from upgrading Rex until you're ready, pin it:

```powershell
winget pin add --id Superlogical.RexServer.Preview --source rex
```

To see your pins, and to remove this one:

```powershell
winget pin list --source rex
winget pin remove --id Superlogical.RexServer.Preview --source rex
```

`winget pin list` shows nothing without `--source rex`, because the source
is explicit. An MSI or zip you installed yourself is never upgraded until
you install a new one.
