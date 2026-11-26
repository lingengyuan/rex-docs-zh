---
title: "Server Modes"
canonical_url: https://www.superlogical.com/rex/docs/linux/server-modes
---

# Server Modes

How you run a Rex server decides which account it runs as and who can
connect to it. **On Windows, there's only the personal server, as
[Running on Windows](https://www.superlogical.com/rex/docs/windows/running.md) explains.**

**If you only want to reach Rex on one machine from your Mac, start with a
quickstart.** Each sets up a personal server that you reach over SSH:
[Linux](https://www.superlogical.com/rex/docs/linux/installation.md#quickstart),
[FreeBSD](https://www.superlogical.com/rex/docs/freebsd/installation.md#quickstart), or
[Windows](https://www.superlogical.com/rex/docs/windows/running.md#quickstart).

There are three ways to run the Rex server on Linux and FreeBSD:

| Mode            | Who it's for                            | Runs as                           | Started by                                                  |
| --------------- | --------------------------------------- | --------------------------------- | ----------------------------------------------------------- |
| Personal        | Just you                                | Your account                      | Any `rex` command, or `rex server start`                    |
| Shared          | A few people you trust with one account | `rex`                             | `rex.service`, or `rex.socket` on demand                    |
| Login           | Several people, each as themselves      | root, then each person's account  | `rex-login-server.service`, or `rex-login-server.socket` on demand |

If you're the only person using Rex on the machine, run a personal server.
If a few people need it and can share one account, use the shared server.
If you or others need to access and login as separate accounts, use the
login server.

The shared server and the login server can't run together. Their services
and sockets all use `/run/rex`, so starting the service or socket of one
stops both units of the other. On Alpine and FreeBSD, each refuses to start
while the other is running. Personal servers can run alongside either one.
With the login server, your personal server is the same server the login
server connects you to, so local `rex` commands and remote connections see
the same sessions.

Every mode listens only on Unix sockets on this machine by default. To
connect from another computer, see [Remote Access](https://www.superlogical.com/rex/docs/linux/remote-access.md).

## Personal Server

A personal server runs as your own user account and doesn't require any
special setup or root access. Any `rex` command automatically starts a
personal server if none is running:

```sh
rex ls
```

An automatically started personal server stops on its own around 10 seconds
after its last session and its last connection close. To start one that remains
running you must explicitly start it:

```sh
rex server start
```

`rex server start` does nothing if a server is already running, including
one that a `rex` command started, so its safe to call multiple times. Its
options, such as `--max-sessions`, apply only when it starts a new server.
To change them, stop the server and start it again.

| Command                    | Effect                                                         |
| -------------------------- | -------------------------------------------------------------- |
| `rex server status`        | Show the running server's status.                              |
| `rex server logs --follow` | Show and follow the log of a server started by `rex server start`. |
| `rex server stop`          | Stop the server. This ends every session on it.                |

The socket is in `$XDG_RUNTIME_DIR/rex`, which is usually
`/run/user/<uid>/rex`. Logs and other state are in `~/.local/state/rex`, or
`$XDG_STATE_HOME/rex` if you've set it. FreeBSD has no `/run/user`, so
there the socket is in `~/.local/state/rex/run`. The same goes for Linux
machines without it, such as many containers.

A `rex` command starts a server on its own only for a socket in that
directory, or in `REX_RUNTIME_DIR` instead if you've set it. Given any
other socket with `-S`, such as the shared server's, it starts nothing and
says how to start a server there. To run one of your own at another path,
start it yourself. Your account must be able to create files in the
socket's directory:

```sh
rex -S PATH server start
```

To keep `rex` commands from starting a server at all, set
`REX_AUTOSTART=0`.

### Shared Home Directories

Rex can run as a personal server even if the home directory of a user is
shared across multiple machines (e.g. via NFS). Rex keys its local state by
machine ID, so this should all work automatically, but this section clearly
documents how it all works.

The first machine to use `~/.local/state/rex` claims it and keeps its state
there as usual. This makes it so that the local state looks "clean" to normal
non-shared-filesystem users.

Future machines that access the same state directory keep their state in
a subdirectory keyed by machine ID: `~/.local/state/rex/machines/<key>`.
Each machine has its own server, sessions, host ID, and list of hosts.
Your config in `~/.config/rex` stays shared.

Rex determines machine ID by `/etc/machine-id`, or `kern.hostuuid` on
FreeBSD.

A machine whose ID changes, such as after you reinstall its system, looks
like a new machine and starts with no sessions. If it was the first machine,
it can take its old state back. Remove the claim, then stop its server so
that the next `rex` command starts one with the old state:

```sh
rm ~/.local/state/rex/machine-owner
rex server stop
rex ls
```

## Shared Server

A shared server is one server that runs as the `rex` system account.
Members of the `rex` group can connect to it, and every program they start
runs as `rex`. It's the simplest way to let more than one person use Rex.

**Access to the shared server is access to the `rex` account.** Anyone in
the group can see and type into every session on it. Only add people you
would trust with that account.

Add each person to the group, then start the service now and at every boot:

```sh
sudo usermod --append --groups rex alice
sudo systemctl enable --now rex.service
```

A group change applies the next time that person logs in. The server keeps
its data in `/var/lib/rex`, or `/var/db/rex` on FreeBSD. On Alpine, the
[OpenRC commands](https://www.superlogical.com/rex/docs/linux/installation.md#alpine) do both steps, and on
FreeBSD, the [FreeBSD commands](https://www.superlogical.com/rex/docs/freebsd/installation.md#commands-and-paths).

To start the server only when someone first connects, enable `rex.socket`
instead of `rex.service`. See
[Starting on Demand](https://www.superlogical.com/rex/docs/linux/shared-server.md#starting-on-demand).

A package upgrade restarts the service, which automatically ends every
program running on it. Its sessions are
[restored](https://www.superlogical.com/rex/docs/features/session-restore.md). See [Upgrading](https://www.superlogical.com/rex/docs/linux/upgrading.md).

Read [Shared Server](https://www.superlogical.com/rex/docs/linux/shared-server.md) before you set it up for other
people. It covers giving them access, configuring the server, and changing
the service without losing your changes on upgrade.

## Login Server

The login server gives each person a server that runs as their own account,
with their own files and permissions. It runs as root. When someone
connects, it identifies them, checks `/etc/rex/accounts.jsonc` for the
accounts they may use, and hands the connection to a server running as that
account. It starts that server if needed.

The login server is the most similar to SSH: one root service that lets each
person in as their own account. Unlike SSH, it has no passwords or keys.
**It identifies people only by how they connect**, such as the local account
on the other end of its socket or their Tailscale login. Anyone who can
reach it that way can use the accounts listed for them.

Each account's server keeps running when the login server stops, restarts,
or is upgraded, so sessions survive all three. After an upgrade, each one
keeps the old version until its sessions end.

The accounts file ships empty, which lets nobody in. Add at least one
account, then start the service now and at every boot:

```sh
sudo $EDITOR /etc/rex/accounts.jsonc
sudo systemctl enable --now rex-login-server.service
```

On Alpine, use the [OpenRC commands](https://www.superlogical.com/rex/docs/linux/installation.md#alpine) instead.
On FreeBSD, use the
[FreeBSD commands](https://www.superlogical.com/rex/docs/freebsd/installation.md#commands-and-paths), and edit
`/usr/local/etc/rex/accounts.jsonc`.

To start the login server only when someone first connects, enable
`rex-login-server.socket` instead of `rex-login-server.service`. See
[Starting on Demand](https://www.superlogical.com/rex/docs/linux/login-server.md#starting-on-demand).

After you change the accounts file, reload it. This doesn't drop any
connections:

```sh
sudo systemctl reload rex-login-server.service
```

On Alpine, run `rc-service rex-login-server reload`. On FreeBSD, run
`service rex-login-server reload`.

Read [Login Server](https://www.superlogical.com/rex/docs/linux/login-server.md) before you add accounts. It covers
the accounts file, how people choose an account when they connect, and the
PAM policy the login server checks accounts against.

## Switching Between the Services

Starting either server stops the other, but disable the old server's
service and socket too, so that neither comes back at the next boot:

```sh
sudo systemctl disable --now rex.service rex.socket
sudo systemctl enable --now rex-login-server.service
```

To start the new server on demand, enable its socket instead, such as
`rex-login-server.socket`. To switch back, swap the names: disable
`rex-login-server.service` and `rex-login-server.socket`, then enable
`rex.service` or `rex.socket`.

On Alpine, starting either service fails while the other is running, so
stop the old one first:

```sh
rc-service rex stop
rc-update del rex
rc-update add rex-login-server
rc-service rex-login-server start
```

On FreeBSD, the same applies. Stop and disable the old one first:

```sh
service rex stop
sysrc rex_enable=NO
sysrc rex_login_server_enable=YES
service rex-login-server start
```

Switching from the shared server ends every session on it.

Switching from the login server leaves each account's server running. On
machines without systemd-logind, or with a login server run with
`--pam=false`, those servers keep their sockets in `/run/rex/accounts`, and
`rex.service` and `rex.socket` refuse to start while that directory exists.
Once nobody needs those sessions, clear the directory and start the shared
server:

```sh
sudo rm -rf /run/rex
sudo systemctl start rex.service
```

To start the shared server on demand, start `rex.socket` instead. A
refused start can still stop the login server's units, so if you back out,
start the login server's service or socket again.

Alpine has no systemd-logind, so the account servers always keep their
sockets in `/run/rex/accounts` there. Clear the directory the same way,
then run `rc-service rex start`.

FreeBSD has no systemd-logind either, and keeps `/var/run` across reboots,
so there the `rex` service refuses to start only while
`/var/run/rex/accounts` holds a socket. Clear it the same way with
`rm -rf /var/run/rex`, then run `service rex start`.
