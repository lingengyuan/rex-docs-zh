---
title: "Shared Server"
canonical_url: https://www.superlogical.com/rex/docs/linux/shared-server
---

# Shared Server

The shared server is one Rex server that runs as the `rex` system account,
as `rex.service`. Members of the `rex` group can connect to it, and every
program they start runs as `rex`. It's the simplest
[server mode](https://www.superlogical.com/rex/docs/linux/server-modes.md) for a few people who are comfortable
sharing one account.

**Shared servers are only on Linux and FreeBSD.** On Windows, see
[Running on Windows](https://www.superlogical.com/rex/docs/windows/running.md).

**If you're the only one using Rex on the machine, you don't need the
shared server.** Start with the quickstart for
[Linux](https://www.superlogical.com/rex/docs/linux/installation.md#quickstart) or
[FreeBSD](https://www.superlogical.com/rex/docs/freebsd/installation.md#quickstart) instead, which sets up a
personal server that you reach over SSH.

**Access to the shared server is access to the `rex` account.** Anyone in
the group can see and type into every session on it and start programs as
`rex`. Only add people you would trust with that account. If people need
their own files and permissions, use the [login server](https://www.superlogical.com/rex/docs/linux/login-server.md)
instead.

## Starting the Server

The package creates the `rex` account with `nologin` as its shell, and Rex
starts each terminal with its account's shell. Give the account a real
shell first, or every terminal on the shared server exits as soon as it
starts:

```sh
sudo usermod --shell /bin/bash rex
```

Alpine has neither `usermod` nor bash by default. Install `usermod` with
the `shadow` package and use `/bin/sh`:

```sh
apk add shadow
usermod --shell /bin/sh rex
```

FreeBSD has no bash by default either. Use `pw` and `/bin/sh` there:

```sh
pw usermod rex -s /bin/sh
```

The account stays locked, with no password, so nobody can log in as `rex`
this way.

Then start the service now and at every boot:

```sh
sudo systemctl enable --now rex.service
```

On Alpine, run `rc-update add rex`, then `rc-service rex start`. On
FreeBSD, run `sysrc rex_enable=YES`, then `service rex start`.

To start the server only when someone first connects, enable `rex.socket`
instead. See [Starting on Demand](#starting-on-demand).

The server listens on `/run/rex/server.sock` and keeps its data in
`/var/lib/rex`, the `rex` account's home directory. On FreeBSD, those are
`/var/run/rex/server.sock` and `/var/db/rex`.

## Starting on Demand

Rex can be paired with systemd to automatically start the shared server
when a client connections, instead of at boot using `rex.socket`.

When this is enabled, systemd creates `/run/rex/server.sock` and waits. When
a client connects, systemd starts `rex.service` with the same command line
and hands it the socket. The client waits a moment while the server starts,
then works as usual. Access is the same: members of the `rex` group can use
the socket.

Enable the socket instead of the service:

```sh
sudo systemctl enable --now rex.socket
```

Enable one or the other, not both. The socket starts the service when it
needs to. `systemctl status rex.socket` shows "active (listening)" until
the first client connects.

Once it starts, the server keeps running, even when nobody is using it.
The socket changes when the server starts, not how long it runs.

While the socket is active, any connection starts the server, including
`rex server status`. To check on it without starting it, ask systemd:

```sh
systemctl status rex.service rex.socket
```

Stopping `rex.service` alone lasts only until the next connection. To stop
the server and keep it stopped, stop both units in one command. This ends
every session on it:

```sh
sudo systemctl stop rex.socket rex.service
```

Stopping only `rex.socket` leaves the server running without its socket
file, so nobody new can connect to it. Don't use `rex server stop` either.
It connects to the socket to check that the server stopped, which can start
it again.

To switch to a server that always runs, disable both units, then enable
the service:

```sh
sudo systemctl disable --now rex.socket rex.service
sudo systemctl enable --now rex.service
```

To switch back, stop the service first. systemd won't listen on the socket
while the server is running:

```sh
sudo systemctl disable --now rex.service
sudo systemctl enable --now rex.socket
```

Either switch ends every session on a running shared server.

Alpine and FreeBSD have no socket activation, so there the service is the
only way to run the shared server. On NixOS, set
`services.rex.socketActivation`. See
[The NixOS Module](https://www.superlogical.com/rex/docs/linux/installation.md#the-nixos-module).

## Giving People Access

Add each person to the `rex` group. The change applies the next time they
log in:

```sh
sudo usermod --append --groups rex alice
```

On Alpine, run `addgroup alice rex`. On FreeBSD, run
`pw groupmod rex -m alice`.

Their `rex` commands look for their own [personal
server](https://www.superlogical.com/rex/docs/linux/server-modes.md#personal-server) by default, and start one if
it isn't running. To use the shared server instead, pass its socket with
`-S`, or set `REX_SERVER` in their shell profile so every `rex` command
uses it:

```sh
rex -S /run/rex/server.sock ls
export REX_SERVER=/run/rex/server.sock
```

On FreeBSD, the socket is `/var/run/rex/server.sock`. Inside the shared
server's own terminals, `rex` commands already use the shared server.

A `rex` command never starts a personal server at the shared server's
socket. If the shared server isn't running, the command fails, and on Linux
the error names the service to start. With `rex.socket` enabled, the
connection starts the shared server instead. People outside the `rex` group
get a permission error, because only the group can open `/run/rex`.

The service isn't sandboxed on purpose. Sandboxing would also restrict the
programs people run in it, so the `rex` account is the security boundary.

To reach the shared server from another computer, see
[Remote Access](https://www.superlogical.com/rex/docs/linux/remote-access.md).

## Configuration

The shared server reads its [configuration file](https://www.superlogical.com/rex/docs/customize/config.md) from
the `rex` account's home:

```
/var/lib/rex/.config/rex/init.lua
```

On FreeBSD, it's `/var/db/rex/.config/rex/init.lua`. Only root can edit
it, because the home directory is private to the `rex` account. After you
change it, any member of the group can reload it:

```sh
sudo $EDITOR /var/lib/rex/.config/rex/init.lua
rex -S /run/rex/server.sock config reload
```

To keep the file somewhere else, pass `--config PATH` in a drop-in, as
below.

## Customizing the Service

Package upgrades replace `rex.service`, so put changes in a drop-in file
instead. This command creates one and opens it in your editor:

```sh
sudo systemctl edit rex.service
```

To change the server's options, clear `ExecStart` and set it again. This
example raises the session limit:

```ini
[Service]
ExecStart=
ExecStart=/usr/bin/rex server run --listen /run/rex/server.sock \
  --state-dir /var/lib/rex --socket-mode 0660 --log-format text \
  --max-sessions 128
```

On Alpine, upgrades replace `/etc/init.d/rex`, so set `command_args` in
`/etc/conf.d/rex` instead. The package never creates or changes that file.
The same example there leaves out `/usr/bin/rex`:

```sh
command_args="server run --listen /run/rex/server.sock \
  --state-dir /var/lib/rex --socket-mode 0660 --log-format text \
  --max-sessions 128"
```

Keep the four options from the original command line. The same pattern adds
a network listener for [Remote Access](https://www.superlogical.com/rex/docs/linux/remote-access.md) or a block
plugin directory with `--block-dir`. Run `rex server run --help` for every
option.

With `rex.socket`, the same drop-in applies, because the socket starts
`rex.service`. The socket's path and mode come from the socket unit, so to
change them, edit both units. See
[Customizing the Socket](#customizing-the-socket).

On FreeBSD, upgrades replace `/usr/local/etc/rc.d/rex` but never change
`/etc/rc.conf`, so set `rex_flags` there instead. It adds options to the
service's command line rather than replacing it, so leave out the four it
already has:

```sh
sysrc rex_flags="--max-sessions 128"
service rex restart
```

[Settings](https://www.superlogical.com/rex/docs/freebsd/installation.md#settings) lists the service's other
settings, such as `rex_umask`.

## Customizing the Socket

With `rex.socket`, systemd creates the server's socket and hands it to the
server, which serves it instead of creating its own. Package upgrades
replace `rex.socket` too, so put changes in a drop-in for it:

```sh
sudo systemctl edit rex.socket
```

The server serves only the sockets its command line names. Every
`ListenStream=` path in the socket unit needs a matching `--listen` or
`--extra-listen` in `rex.service`. Otherwise the server refuses to start,
and clients wait until they time out.

To move the socket to `/run/rex/rex.sock`, stop both units first. systemd
removes the socket file it knows about when the unit stops, so stopping
after the edit would leave the old file behind:

```sh
sudo systemctl stop rex.socket rex.service
```

Then run `sudo systemctl edit rex.socket` and set the new path. The empty
`ListenStream=` clears the one in the unit:

```ini
[Socket]
ListenStream=
ListenStream=/run/rex/rex.sock
```

Run `sudo systemctl edit rex.service` and set the same path:

```ini
[Service]
ExecStart=
ExecStart=/usr/bin/rex server run --listen /run/rex/rex.sock \
  --state-dir /var/lib/rex --socket-mode 0660 --log-format text
```

Then start the socket again:

```sh
sudo systemctl start rex.socket
```

Clients then connect with `rex -S /run/rex/rex.sock`. To serve a second
socket, add another `ListenStream=` line to the socket unit and a matching
`--extra-listen unix://PATH` to the service. A socket for Tailscale Serve
needs `tailnet-serve://` instead, as
[Tailscale Serve](https://www.superlogical.com/rex/docs/linux/remote-access.md#tailscale-serve) shows.

The server keeps the mode that `SocketMode=` gives the socket, and ignores
`--socket-mode` for it. It refuses a mode that lets every user on the
machine connect, such as `0666`, so keep it at `0660` or narrower. `0600`
works, but locks out the `rex` group.

The server takes only listening stream sockets, from `ListenStream=`, and
refuses `Accept=yes`. A TCP `ListenStream=` needs `--extra-listen` with the
same port and `--allow-anonymous`, as
[Plain HTTP](https://www.superlogical.com/rex/docs/linux/remote-access.md#plain-http) describes. Give it an IP
address, not a host name.

To apply any later change to `rex.socket`, stop both units and start the
socket again, as above. `sudo systemctl restart rex.socket` fails while
the server is running, and leaves the server without its socket file.

## Logs

The shared server logs to the journal:

```sh
journalctl -u rex.service -f
```

Alpine has no journal, so there the server logs to a file:

```sh
tail -f /var/log/rex/server.log
```

On FreeBSD, the server logs to syslog, which writes to `/var/log/messages`:

```sh
grep ' rex\[' /var/log/messages
```

The logs are plain text. For JSON, change `--log-format text` to
`--log-format json` in a drop-in.

With `rex.socket`, the server still logs as `rex.service`. If it refuses
to start, such as for a socket it isn't configured to serve, the journal
names the socket and the option to add. Clients aren't refused meanwhile.
Each one waits until its `--timeout` runs out, 10 seconds by default.

`rex server logs` shows only servers started with `rex server start`, not
the service. Use the journal instead.

## Upgrading

Upgrading the package restarts a running shared server, so it runs the new
version right away. On FreeBSD, pkg restarts nothing, so the server keeps
the old version until you run `service rex restart`.

With `rex.socket`, a running server restarts the same way, and one that
hasn't started yet runs the new version when the first client connects.
Upgrades never restart `rex.socket` itself. If a new version changes the
socket unit, the change applies once you stop both units and start the
socket again, or at the next reboot.

**Restarting ends every program in every session.** The sessions are
[restored](https://www.superlogical.com/rex/docs/features/session-restore.md), each pane with a new shell, and only
programs that can resume come back. Upgrade when nobody has work running, or
[hold the package](https://www.superlogical.com/rex/docs/linux/upgrading.md#holding-an-upgrade) until then.

The login server doesn't have this problem. Its sessions survive upgrades.
[Upgrading](https://www.superlogical.com/rex/docs/linux/upgrading.md) covers the rest.
