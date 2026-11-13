---
title: "Login Server"
canonical_url: https://www.superlogical.com/rex/docs/linux/login-server
---

# Login Server

The login server lets several people use Rex on one machine, each as their
own operating system account, with their own files and permissions. It's
the [server mode](https://www.superlogical.com/rex/docs/linux/server-modes.md) to use when people shouldn't share
an account.

**Login servers are only on Linux and FreeBSD.** On Windows, see
[Running on Windows](https://www.superlogical.com/rex/docs/windows/running.md).

**If you're the only one using Rex on the machine, you don't need the
login server.** Start with the quickstart for
[Linux](https://www.superlogical.com/rex/docs/linux/installation.md#quickstart) or
[FreeBSD](https://www.superlogical.com/rex/docs/freebsd/installation.md#quickstart) instead, which sets up a
personal server that you reach over SSH.

**The login server has no passwords or keys.** It identifies people only by
how they connect, such as their Tailscale login. Anyone who can reach it
that way can use every account the accounts file lists for them. This
is only a short-term limitation, we have a full authentication and
authorization system planned (including supporting legacy SSH keys),
but until then we recommend using something like Tailscale.

## How It Works

The login server runs as root, as `rex-login-server.service`. It can also
start when the first client connects, through `rex-login-server.socket`.
See [Starting on Demand](#starting-on-demand). When a client connects:

1. The login server identifies the caller, such as by their Tailscale login
   or their local user ID.
2. It checks `/etc/rex/accounts.jsonc` for the accounts that caller may use,
   and picks one.
3. It opens a login session for that account through PAM, the same as a
   console or SSH login, and starts a Rex server as that account. If one is
   already running, it uses that one instead.
4. It hands the connection to that server.

Each account's server keeps running when the login server stops, restarts,
or is upgraded, so sessions survive all three. After an upgrade, each one
keeps the old version until its sessions end. See
[What Restarts](https://www.superlogical.com/rex/docs/linux/upgrading.md#what-restarts).

On machines with systemd-logind, an account's server is the same as that
person's [personal server](https://www.superlogical.com/rex/docs/linux/server-modes.md#personal-server). Sessions
they start with `rex` on the machine and sessions they start from another
computer are on the same server.

## Accounts File

`/etc/rex/accounts.jsonc` lists the accounts people may use and who may use
each one. It's JSON, with comments and trailing commas allowed. The file ships
empty, which lets nobody in by default.

This example lets Alice use her own account and root. She connects as
`alice` unless she asks for root:

```jsonc
{
  "version": 1,
  "accounts": {
    "alice": { "principals": ["tailscale:alice@example.com"] },
    "root": { "principals": ["tailscale:alice@example.com"] },
  },
  "defaults": { "tailscale:alice@example.com": "alice" },
}
```

Under `accounts`, each key is an account name, and `principals` lists the
callers allowed to use it. A caller may use an account if any of its
principals match:

| Principal                     | Matches                                                       |
| ----------------------------- | ------------------------------------------------------------- |
| `tailscale:alice@example.com` | A person, by their Tailscale login                            |
| `tailscale:tag:ci`            | A device with the Tailscale tag `tag:ci`                      |
| `tailscale:*`                 | Any person on the tailnet                                     |
| `tailscale:tag:*`             | Any tagged device                                             |
| `peer:1000`                   | A local user, by user ID                                      |
| `identified`                  | Any caller Rex can identify                                   |
| `anonymous`                   | Callers Rex can't identify, such as on a plain TCP listener   |

A tagged device never matches a person's login or `tailscale:*`.

### Any Account

The special account `"*"` lets its callers use any regular account, meaning
any account with a user ID of 1000 or higher, whether or not the file names
it. Root and system accounts must always be listed by name.

```jsonc
{
  "version": 1,
  "accounts": {
    "*": { "principals": ["tailscale:*"] },
  },
}
```

For safety, `anonymous` can't appear under `"*"`, and anonymous callers can
never use root.

### Defaults

When a client doesn't ask for a specific account, `defaults` picks one. A
default only chooses an account. The caller must still be allowed to use
it.

If several defaults match a caller, the most specific one wins: a login or
user ID first, then a tag, then a Tailscale wildcard, then `identified`,
then `anonymous`. Between equally specific matches, the first in the file
wins.

With no matching default, a caller allowed exactly one account connects as
that account. Otherwise, the client must name the account it wants.

## Starting and Reloading

Add at least one account so a user can access, then start the service:

```sh
sudo $EDITOR /etc/rex/accounts.jsonc
sudo systemctl enable --now rex-login-server.service
```

This will enable it to start now and for every reboot. On Alpine, use the
[OpenRC commands](https://www.superlogical.com/rex/docs/linux/installation.md#alpine) instead, and on FreeBSD, the
[FreeBSD commands](https://www.superlogical.com/rex/docs/freebsd/installation.md#commands-and-paths).

Reload the server anytime you change the accounts file:

```sh
sudo systemctl reload rex-login-server.service
```

On Alpine, run `rc-service rex-login-server reload`. On FreeBSD, run
`service rex-login-server reload`.

Reloading doesn't drop connections that are still allowed. It closes
connections whose access you removed, but leaves every account's server and
its sessions running. The journal shows `account policy reloaded`, or
`account policy reload failed; previous policy retained` if the new file
has an error.

Package upgrades keep your changes to the accounts file. The login
server's logs are in the journal:

```sh
journalctl -u rex-login-server.service
```

Alpine has no journal, so there the logs are in
`/var/log/rex-login-server.log`. On FreeBSD, they're in
`/var/log/messages`. See [FreeBSD](#freebsd).

The login server listens only on `/run/rex/login-server.sock`, which only
root can use. To let people connect from other computers, see
[Remote Access](https://www.superlogical.com/rex/docs/linux/remote-access.md).

## Starting on Demand

Rex can be paired with systemd to automatically start the login server
when a client connections, instead of at boot using `rex-login-server.socket`.

When this is enabled, systemd creates `/run/rex/login-server.sock` and waits.
When a client connects, systemd starts `rex-login-server.service` and hands
it the socket. The client waits a moment while the login server starts,
then works as usual. Only root can use the socket, the same as when the
login server creates it.

Add at least one account, then enable the socket instead of the service:

```sh
sudo $EDITOR /etc/rex/accounts.jsonc
sudo systemctl enable --now rex-login-server.socket
```

Enable one or the other, not both. The socket starts the service when it
needs to. `systemctl status rex-login-server.socket` shows "active
(listening)" until the first client connects.

While the socket is active, any connection starts the login server,
including `rex server status`. To check on it without starting it, run
`systemctl status rex-login-server.service rex-login-server.socket`.

Reload the accounts file the same way as above. Before any client has
connected, the login server isn't running, so the reload fails. There's
nothing to do then: the login server reads the new file when it starts.

If the accounts file is missing or invalid, the login server exits with
`loading accounts file:` and the reason, and starts again 5 seconds later.
Clients aren't refused meanwhile. Each one waits until its `--timeout`
runs out, 10 seconds by default. The journal shows why.

Stopping `rex-login-server.service` alone lasts only until the next
connection. To stop the login server and keep it stopped, stop both units
in one command:

```sh
sudo systemctl stop rex-login-server.socket rex-login-server.service
```

Stopping only the socket leaves the login server running without its
socket file, so nobody new can connect to it. Either way, each account's
server and its sessions keep running. Clients reach them again once the
login server is back.

To switch to a login server that always runs, disable both units, then
enable the service:

```sh
sudo systemctl disable --now rex-login-server.socket rex-login-server.service
sudo systemctl enable --now rex-login-server.service
```

To switch back, stop the service first. systemd won't listen on the socket
while the login server is running:

```sh
sudo systemctl disable --now rex-login-server.service
sudo systemctl enable --now rex-login-server.socket
```

To change the socket, run `sudo systemctl edit rex-login-server.socket`.
Every `ListenStream=` in it needs a matching option on the login server's
command line. It works the same way as for the shared server. See
[Customizing the Socket](https://www.superlogical.com/rex/docs/linux/shared-server.md#customizing-the-socket). To
have a request through Tailscale Serve start the login server too, see
[Tailscale Serve](https://www.superlogical.com/rex/docs/linux/remote-access.md#tailscale-serve).

Alpine and FreeBSD have no socket activation. On NixOS, set
`services.rex.loginServer.socketActivation`. See [NixOS](#nixos).

## Choosing an Account

To ask for a specific account, put it before the host in the server's
address:

```sh
rex -S root@build.example.ts.net ls
```

The same address works in the Mac app's **Add Remote Host…**. Without an
account in the address, the caller's default applies.

Accounts can only be chosen in an `https://` or `http://` address, so the
login server needs a network listener first. [Remote Access](https://www.superlogical.com/rex/docs/linux/remote-access.md)
covers setting one up and connecting to it as each account.

## PAM

The login server uses PAM each time it starts a server for an account. PAM
decides whether the account may log in at all, such as whether it's locked
or expired, and sets up the login session: resource limits, environment
variables, and a systemd-logind session on machines that have one.

Rex has already identified the caller before PAM runs, so its policy never
asks for a password, the same as SSH with keys. While `/etc/nologin`
exists, only root may log in. Accounts whose shell is `nologin` or `false`
are always refused.

The package installs a policy at `/etc/pam.d/rex-login-server` that fits
your distribution: Debian and Ubuntu, Red Hat and its relatives, SUSE, or
Alpine. Upgrades keep your changes to it. FreeBSD is different. See
[FreeBSD](#freebsd).

To skip PAM, run `sudo systemctl edit rex-login-server.service` and
replace the service's command line with one that adds `--pam=false`. Rex
then checks
`/etc/shadow` and `/etc/nologin` itself and opens no login session.

On Alpine, set `command_args` in `/etc/conf.d/rex-login-server` instead,
to the service's command line with `--pam=false` added:

```sh
command_args="login-server --listen unix:///run/rex/login-server.sock \
  --accounts /etc/rex/accounts.jsonc --runtime-root /run/rex --log-format text \
  --pam-service rex-login-server --pam=false"
```

## NixOS

The NixOS module writes the accounts file from
`services.rex.loginServer.accounts` and `services.rex.loginServer.defaults`.
It doesn't create the accounts, so declare them with `users.users`:

```nix
{
  users.users.alice.isNormalUser = true;

  services.rex.loginServer = {
    enable = true;
    accounts.alice.principals = [ "tailscale:alice@example.com" ];
  };
}
```

To keep the order of `defaults`, which decides ties, use
`services.rex.loginServer.accountsFile` to load your own file instead.

To start the login server only when the first client connects, set
`services.rex.loginServer.socketActivation = true;`. To stop it and keep it
stopped, stop `rex-login-server.socket` and `rex-login-server.service`
together. See [The NixOS Module](https://www.superlogical.com/rex/docs/linux/installation.md#the-nixos-module).

## FreeBSD

On FreeBSD, the accounts file is `/usr/local/etc/rex/accounts.jsonc`, and
the [FreeBSD commands](https://www.superlogical.com/rex/docs/freebsd/installation.md#commands-and-paths) start and
reload the service. The login server logs to syslog, in
`/var/log/messages`. Each account's server
logs to `/var/run/rex/accounts/<account>/server.log` instead, and can be read
by the person using that account, too.

The package installs its PAM policy at
`/usr/local/etc/pam.d/rex-login-server`, and **every upgrade replaces it**.
To change the rules, copy it to `/etc/pam.d` and edit the copy. OpenPAM
reads `/etc/pam.d` first, and upgrades never touch it:

```sh
install -o root -g wheel -m 0644 /usr/local/etc/pam.d/rex-login-server \
  /etc/pam.d/rex-login-server
$EDITOR /etc/pam.d/rex-login-server
```

OpenPAM ignores a policy that root doesn't own, so keep the copy owned by
root.

The policy checks accounts the same way sshd does. An account locked with
`pw lock` is refused, `/etc/login.access` applies, and while
`/var/run/nologin` exists, only root may log in. Rex applies each account's
login class from `/etc/login.conf` to its server, such as its resource
limits.

To skip PAM, add `--pam=false` to `rex_login_server_flags`, then restart
the service:

```sh
sysrc rex_login_server_flags="--pam=false"
service rex-login-server restart
```

Rex then checks `/etc/master.passwd` and `/var/run/nologin` itself.
