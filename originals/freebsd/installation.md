---
title: "Installing on FreeBSD"
canonical_url: https://www.superlogical.com/rex/docs/freebsd/installation
---

# Installing on FreeBSD

Rex can run as a server on FreeBSD so that clients can access it as a
remote host.

**IMPORTANT:** Rex on FreeBSD is in testing. The install commands show
below once you've logged in with Discord.

The other server pages, starting with [Server Modes](https://www.superlogical.com/rex/docs/linux/server-modes.md),
apply to FreeBSD too. Where they give a Linux command or path, use the one
in [Commands and Paths](#commands-and-paths).

## Quickstart

This section documents the recommended setup to get up and running quickly.
It reaches your own personal server from your clients over SSH, with nothing
else to set up. We recommend you read the later sections, and
[Remote Access](https://www.superlogical.com/rex/docs/linux/remote-access.md#ssh), to understand the details and
other access options.

1. On the FreeBSD machine, install Rex as [Install](#install) documents.

2. Check that you can log in with your SSH key from your client, and that
   SSH can access `rex` there:

   ```sh
   ssh alice@build.example.com rex version
   ```

3. Connect from your client:

   ```sh
   rex -S ssh://alice@build.example.com ls
   ```

   In Rex for Mac, choose **Add Remote Host…** and enter
   `ssh://alice@build.example.com`.

The first connection starts your personal server, and it keeps running
after you log out, until you stop it or the machine restarts. If several
people need Rex on one machine, see [Server Modes](https://www.superlogical.com/rex/docs/linux/server-modes.md).

## System Requirements

| Requirement  | Supported                                                                     |
| ------------ | ----------------------------------------------------------------------------- |
| Release      | FreeBSD 14.0 or later                                                         |
| Architecture | x86-64 with SSE4.2, ARM64                                                     |
| Dependencies | None. Rex uses only the base system.                                          |
| Services     | rc.d, for the shared server and the login server. The `rex` command runs without them. |
| Packages     | `.pkg`, from the Rex repository                                               |

One package serves FreeBSD 14 and every later release.

## Install


The **install script (`install.sh`)** adds the Rex repository to pkg and
installs the `rex` package, so `pkg upgrade` updates Rex along with your
other packages. It takes the same options as on
[Linux](https://www.superlogical.com/rex/docs/linux/installation.md#install), such as `--channel`, `--tarball`, and
`--dry-run`. Pass them after `sh -s --`.

FreeBSD has no `sudo` by default, so run the **pkg** tab's commands as
root. The first, `umask 022`, makes the files they create readable by every
user, whatever root's umask is. The install script needs root too, or `sudo`
if you've installed it.

FreeBSD has no curl either, so the commands download with FreeBSD's own
`fetch`.

If a channel has no FreeBSD package yet, the script installs only the
`rex` binary into `/usr/local/bin`, as `--tarball` does, with no services.
Run the script again once the channel has a package, and it switches to the
package.

pkg trusts the Rex repository by the fingerprint of its signing key, in
`/usr/local/etc/pkg/fingerprints/rex`. If the key changes, run the install
script again to trust the new one.

FreeBSD's own repository has an unrelated package also named `rex`, with a
higher version, so `pkg version` shows Rex as out of date. Ignore it, and
upgrade with `pkg upgrade -r rex rex`, as
[Upgrading](https://www.superlogical.com/rex/docs/linux/upgrading.md#upgrading-the-package) shows.

## Channels

FreeBSD has the same three [channels](https://www.superlogical.com/rex/docs/linux/installation.md#channels) as
Linux. To switch, change the channel name in the `url` line of
`/usr/local/etc/pkg/repos/rex.conf`, then update the catalogue:

```sh
pkg update -r rex
```

Moving from snapshot to preview or stable upgrades Rex. Moving back to
snapshot is a downgrade, which you have to ask for. See
[Upgrading on FreeBSD](https://www.superlogical.com/rex/docs/linux/upgrading.md#freebsd).

## Package Contents

The `rex` package installs:

| Path                                    | What it is                                                         |
| --------------------------------------- | ------------------------------------------------------------------ |
| `/usr/local/bin/rex`                    | The server and the CLI, in one binary                              |
| `/usr/local/etc/rc.d/rex`               | One shared server, run as the `rex` account. Not enabled.          |
| `/usr/local/etc/rc.d/rex-login-server`  | One server per account, after a login. Not enabled.                |
| `rex` account and group                 | A locked system account with the ID 729, or the next free one, and its home at `/var/db/rex` |
| `/usr/local/etc/rex/accounts.jsonc`     | The login server's accounts. It ships empty, which admits nobody.  |
| `/usr/local/etc/pam.d/rex-login-server` | The login server's PAM policy                                      |
| `xterm-rex` terminfo                    | Rex's terminal type, in `/usr/local/share/terminfo`                |

Unlike the Linux packages, it has no SSH fallback, because FreeBSD's
`/etc/ssh/ssh_config` reads no other files. See
[Terminfo and SSH](#terminfo-and-ssh).

Upgrades keep your changes to the accounts file, but replace the PAM
policy. See [Upgrading on FreeBSD](https://www.superlogical.com/rex/docs/linux/upgrading.md#freebsd). To see the
package's setup notes again, run `pkg info -D rex`.

## Commands and Paths

The other server pages give systemd commands. On FreeBSD, use these
instead:

| On systemd                                             | On FreeBSD                                                         |
| ------------------------------------------------------ | ------------------------------------------------------------------ |
| `sudo systemctl enable --now rex.service`              | `sysrc rex_enable=YES`, then `service rex start`                   |
| `sudo systemctl enable --now rex-login-server.service` | `sysrc rex_login_server_enable=YES`, then `service rex-login-server start` |
| `sudo systemctl reload rex-login-server.service`       | `service rex-login-server reload`                                  |
| `sudo systemctl restart rex.service`                   | `service rex restart`                                              |
| `sudo systemctl disable --now rex.service`             | `service rex stop`, then `sysrc rex_enable=NO`                     |
| `sudo systemctl edit rex.service`                      | Set `rex_flags` with `sysrc`. See [Settings](#settings).           |
| `journalctl -u rex.service`                            | `grep ' rex\[' /var/log/messages`                                  |
| `journalctl -u rex-login-server.service`               | `grep ' rex-login-server\[' /var/log/messages`                     |
| `sudo usermod --append --groups rex alice`             | `pw groupmod rex -m alice`                                         |
| `sudo usermod --shell /bin/bash rex`                   | `pw usermod rex -s /bin/sh`                                        |

FreeBSD has no socket activation, so `rex.socket` and
`rex-login-server.socket` have no FreeBSD form. Use the services instead.

Files are in different places too:

| On Linux                      | On FreeBSD                              |
| ----------------------------- | --------------------------------------- |
| `/usr/bin/rex`                | `/usr/local/bin/rex`                    |
| `/run/rex`                    | `/var/run/rex`                          |
| `/var/lib/rex`                | `/var/db/rex`                           |
| `/etc/rex/accounts.jsonc`     | `/usr/local/etc/rex/accounts.jsonc`     |
| `/etc/pam.d/rex-login-server` | `/usr/local/etc/pam.d/rex-login-server` |
| `/etc/nologin`                | `/var/run/nologin`                      |
| `/run/user/<uid>/rex`         | `~/.local/state/rex/run`                |

Both services log to syslog, which writes to `/var/log/messages` by
default. The servers that the login server starts for each account log to
`/var/run/rex/accounts/<account>/server.log` instead.

If a server exits for any reason, its service starts it again 5 seconds
later. Only `service rex stop` stops it for good. `service rex start`
returns as soon as the server's process exists, which can be a moment
before it accepts connections.

## Settings

The services read their settings from `/etc/rc.conf`. Set them with
`sysrc`, then restart the service to apply them. Upgrades replace the rc.d
scripts but never change `/etc/rc.conf`. This example raises the shared
server's session limit:

```sh
sysrc rex_flags="--max-sessions 128"
service rex restart
```

| Setting                        | Default                             | Effect                                         |
| ------------------------------ | ----------------------------------- | ---------------------------------------------- |
| `rex_flags`                    | None                                | More options for `rex server run`              |
| `rex_umask`                    | `0007`                              | The file mode mask for the server and every program it starts |
| `rex_user`                     | `rex`                               | The account the server runs as                 |
| `rex_group`                    | `rex`                               | The group that may use the socket              |
| `rex_runtime_dir`              | `/var/run/rex`                      | The directory that holds the socket            |
| `rex_state_dir`                | `/var/db/rex`                       | The server's data                              |
| `rex_login_server_flags`       | None                                | More options for `rex login-server`            |
| `rex_login_server_accounts`    | `/usr/local/etc/rex/accounts.jsonc` | The accounts file                              |
| `rex_login_server_runtime_dir` | `/var/run/rex`                      | The login server's socket and each account server's directory |

`rex_flags` and `rex_login_server_flags` add options to the service's
command line. A systemd drop-in replaces the command line instead, so where
another page shows a whole `ExecStart` line, put only the options it adds
in the flags. The comment at the top of each rc.d script explains every
setting.

The shared server can run as another account instead of `rex`.
This example runs it as `alice`:

```sh
sysrc rex_user=alice rex_group=alice
service rex restart
```

The files the server wrote before the change still belong to the old
account. On the next start, the service gives them to the new one and prints
a line for each directory it changes:

```
Giving the files in /var/run/rex to alice:alice.
Giving the files in /var/db/rex to alice:alice.
```

The server keeps its saved sessions, and the programs in them now run as
`alice`. Changing back to `rex` works the same way.

## Terminfo and SSH

Programs in Rex terminals see `TERM=xterm-rex`, and the package installs
that terminal type for every account. ssh passes `TERM` on to other hosts,
which usually don't know it. To make ssh send `xterm-256color` to those
hosts instead, for every account, run as root:

```sh
rex terminfo setup --system
```

FreeBSD's `/etc/ssh/ssh_config` reads no other files, so this also adds a
marked `Include` line to it. `rex terminfo remove --system` takes the line
out again. To set it up for your own account only, run
`rex terminfo setup`.
