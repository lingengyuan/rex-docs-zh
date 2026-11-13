---
title: "Remote Access"
canonical_url: https://www.superlogical.com/rex/docs/linux/remote-access
---

# Remote Access

This page documents how you access your servers remotely once you have Rex
Server installed and running.
On Linux or FreeBSD, Rex Server listens only on Unix sockets on that
machine by default. On Windows, it listens only on a named pipe that only
the account owner can open.

To connect to your server from a client on another machine, you must
specify a network listener or access it over SSH. This page covers each
option and the details of it.

**Rex trusts a caller based only on how they connect today**, so it can't
check who someone is unless the network tells it. That's why servers listen
only locally by default and why every listener below is cautious about who
it lets in. This is a short-term limitation. A full authentication and
authorization system is planned, including support for existing SSH keys.

Until then, we recommend [SSH](#ssh). Most machines already run it, it
uses the keys you already have, and the server sees your SSH login, which
is how Rex decides who gets in. Nothing listens on the network but sshd.

| Listener            | Needs                          | Works with                 | Identifies callers |
| ------------------- | ------------------------------ | -------------------------- | ------------------ |
| SSH                 | SSH access to the machine      | Personal and shared server | Yes                |
| Built-in Tailscale  | A Tailscale account            | Personal and shared server | Yes                |
| Tailscale Serve     | Tailscale on the machine       | Shared and login server    | Yes                |
| Tailnet address     | Tailscale on the machine       | Shared and login server    | Yes                |
| Plain HTTP          | `--allow-anonymous`            | Every mode                 | No                 |
| Another VPN         | `--allow-anonymous`            | Every mode                 | No                 |

## SSH

SSH is installed on almost every network-connected machine already, and
you can connect to Rex using your existing SSH credentials. This is the
recommended starting path for accessing Rex remotely.

You can use an `ssh://` address to connect to a server via SSH. Rex
runs your own system `ssh` if available, so it uses your own keys, agents,
config, etc.

```sh
rex -S ssh://alice@build.example.com ls
rex hosts add build ssh://alice@build.example.com
```

The address form is `ssh://[USER@]HOST[:PORT][/SOCKET]`. Without a socket,
Rex finds the SSH user's personal server or starts it if none is running.
If `REX_AUTOSTART=0` is set on the machine, Rex will not autostart your
server over SSH.

On Linux, your personal server's socket goes away when you log out
which will *kill all your running sessions.** Enable linger with
`loginctl enable-linger` to prevent this.

For SSH to work, `rex` must be on the PATH for SSH connections, or in
`~/.local/bin` which we check explicitly since that's where our unprivileged
user install goes.

## Built-in Tailscale

With `--tailscale`, the server joins your tailnet as its own device, using
Tailscale built into Rex. The machine doesn't need Tailscale installed.

```sh
rex server start --tailscale
```

The first time, the server needs to sign in to Tailscale. Its sign-in link
appears in `rex server status` and the server's log. To sign in without a
browser, pass a one-time auth key with `--tailscale-auth-key-file FILE`, or
`-` to read it from standard input. The server keeps its login, so it needs
the key only once.

The device is named `rex` unless you choose another name with
`--tailscale-hostname`. Its address is `https://rex.<tailnet>.ts.net`. Your
tailnet must have MagicDNS and HTTPS certificates turned on.

To sign it in as a tagged device, add `--tailscale-advertise-tag tag:NAME`.
A tagged device has no owner, so this also needs
`--tailscale-allow-tailnet-members`. See [Who Can Connect](#who-can-connect).

On Windows, you must specify these options to `rex server install` after
`--`. A Windows Service has no standard input, so give the auth key as a
file:

```powershell
rex server install -- --tailscale --tailscale-auth-key-file C:\Users\alice\ts-key.txt
```

## Tailscale Serve

If the machine already runs Tailscale, Tailscale Serve can forward HTTPS
connections to a socket that Rex listens on. This is the usual way to reach
the shared server or the login server.

Run `sudo systemctl edit rex.service` (or
`rex-login-server.service`) and add the socket to its command line. Package
upgrades keep this file. For the shared server:

```ini
[Unit]
After=tailscaled.service
Requires=tailscaled.service

[Service]
ExecStart=
ExecStart=/usr/bin/rex server run --listen /run/rex/server.sock \
  --state-dir /var/lib/rex --socket-mode 0660 --log-format text \
  --extra-listen tailnet-serve:///run/rex/serve.sock
```

For the login server, the command line is:

```ini
ExecStart=
ExecStart=/usr/bin/rex login-server --listen unix:///run/rex/login-server.sock \
  --accounts /etc/rex/accounts.jsonc --runtime-root /run/rex --log-format text \
  --pam-service rex-login-server --extra-listen tailnet-serve:///run/rex/serve.sock
```

On Alpine, set `command_args` in `/etc/conf.d/rex` (or
`/etc/conf.d/rex-login-server`) to the same command line, without
`/usr/bin/rex`. `rc_need` takes the place of `After=` and `Requires=`. For
the shared server:

```sh
command_args="server run --listen /run/rex/server.sock \
  --state-dir /var/lib/rex --socket-mode 0660 --log-format text \
  --extra-listen tailnet-serve:///run/rex/serve.sock"
rc_need="tailscale"
```

On FreeBSD, add the socket to `rex_flags` (or `rex_login_server_flags`),
then restart the service. Its socket is in `/var/run/rex`:

```sh
sysrc rex_flags="--extra-listen tailnet-serve:///var/run/rex/serve.sock"
service rex restart
```

Then point Tailscale Serve at the socket:

```sh
sudo tailscale serve --bg --https=443 unix:/run/rex/serve.sock
```

On FreeBSD, that's `unix:/var/run/rex/serve.sock`.

The address is the machine's own tailnet name, such as
`https://build.<tailnet>.ts.net`.

Tailscale Serve doesn't tell Rex who a tagged device is, so tagged devices
such as CI runners can't connect this way. Use a tailnet address for them
instead.

**Use `tailnet-serve://` for the Serve socket, never `unix://`.** With
`unix://`, the server starts without an error, but treats every tailnet
caller as the account that runs tailscaled, usually root.

### Socket-Activated Servers

With `rex.socket` or `rex-login-server.socket`, the drop-in above works
unchanged, but the server creates the Serve socket only once it's running,
so a request through Tailscale Serve can't start it. To let it, add the
Serve socket to the socket unit too. Run `sudo systemctl edit rex.socket`
(or `rex-login-server.socket`) and add:

```ini
[Socket]
ListenStream=/run/rex/serve.sock
```

Keep the `--extra-listen` option in the service's drop-in. Then stop both
units and start the socket again, so that systemd creates the new socket:

```sh
sudo systemctl stop rex.socket rex.service
sudo systemctl start rex.socket
```

For the login server, that's `rex-login-server.socket` and
`rex-login-server.service`. The Serve socket gets the socket unit's mode,
and Tailscale Serve still reaches it, because tailscaled normally runs as
root. See
[Customizing the Socket](https://www.superlogical.com/rex/docs/linux/shared-server.md#customizing-the-socket).

## Tailnet Address

A server can also listen directly on the machine's tailnet addresses, using
the machine's own Tailscale to identify callers. Add this to the server's
command line, the same way as the Serve socket above:

```sh
--extra-listen tailnet://:7297
```

The port is required. The connection is plain HTTP, encrypted by Tailscale,
at `http://build.<tailnet>.ts.net:7297`.

## Who Can Connect

**A connection to a server can do anything that server can,** including
starting programs as its account. Control access with care.

For a personal server or the shared server, only the Tailscale user who
owns the machine (or the Rex device, with built-in Tailscale) is let in by
default. To let in other people:

| Listener           | Option                              | Lets in                                    |
| ------------------ | ----------------------------------- | ------------------------------------------ |
| Built-in Tailscale | `--tailscale-allow-tailnet-members` | Anyone on the tailnet your ACLs allow      |
| Serve or address   | `--tailnet-allow-identified`        | Anyone Tailscale can identify              |

A tagged machine or device has no owner, so it needs one of these options
to let anyone in.

The login server is different. It lets in everyone Tailscale can identify,
because its [accounts file](https://www.superlogical.com/rex/docs/linux/login-server.md#accounts-file) decides
which accounts each person may use.

To see who's connected to a server, run `rex client ls` on it. Its
`principal` column shows the identity of each client.

## Plain HTTP

A plain HTTP listener can't tell callers apart, so Rex refuses one unless
you also pass `--allow-anonymous`:

```sh
rex server start --extra-listen :7297 --allow-anonymous
```

**Every connection then has full access.** Only do this on a network you
completely control. The login server lets such callers use only accounts
whose principals include `anonymous`, and never root.

Again, on an open network this is **super dangerous** and you probably
shouldn't do it. This option exists so that you can pair it with a network
that limits who can reach the server, such as
[your own VPN](#vpns).

## VPNs

You can use any network device or custom VPN you want, such as WireGuard,
ZeroTier, NetBird, etc. To do this, listen directly on the proper network
device:

```sh
rex server start \
  --extra-listen http://10.0.0.5:7297 --allow-anonymous
```

Use the VPN address itself. An address without a host, such as `:7297`, listens
on every address the machine has, including those on its other networks.

**Everyone who can reach that address has full access.** Rex can't tell callers
apart, so each one can do anything the server can, including starting programs
as its account. On a private VPN, that means everyone on the VPN and every
account on this machine. If your VPN has access rules, use them to limit which
devices can reach this port. The login server limits these callers as described
in [Plain HTTP](#plain-http).

The listener depends on the VPN being up. A server that can't listen on an
address doesn't start at all, not even on its Unix socket. So put these options
on the service's command line, as in [Tailscale Serve](#tailscale-serve), rather
than relying on `rex server start`, which doesn't save its options or change a
server that's already running. systemd and FreeBSD try again every 5 seconds, so
the server comes up soon after the VPN connects.

To connect, add `http://10.0.0.5:7297` as a host on a device that's on the VPN.
Some devices run only one VPN at a time, so turning on another one, including
Tailscale, disconnects Rex.

## Adding the Server to a Client

In Rex for Mac, choose **Add Remote Host…** and enter the server's address.

On the command line, pass the address with `-S`, or save it as a host and
use its label:

```sh
rex -S https://build.example.ts.net ls
rex hosts add build https://build.example.ts.net
rex -S build ls
```

A bare host name, such as `build.example.ts.net`, tries HTTPS on port 443,
then HTTPS on port 7297, then HTTP on port 7297.

To connect to the login server as a specific account, put it before the
host, such as `https://root@build.example.ts.net`. See
[Choosing an Account](https://www.superlogical.com/rex/docs/linux/login-server.md#choosing-an-account).

**Note: `rex hosts` today is CLI-only.** It doesn't sync to your GUI client
or across machines. This will change in the future.

## NixOS

The NixOS module has options for each listener:

| Option                                           | Sets up                                                     |
| ------------------------------------------------ | ----------------------------------------------------------- |
| `services.rex.tailscale.enable`                  | Built-in Tailscale, with `hostname`, `authKeyFile`, and `advertiseTags` |
| `services.rex.tailscaleServe.enable`             | Tailscale Serve for the shared server                       |
| `services.rex.loginServer.tailscaleServe.enable` | Tailscale Serve for the login server                        |
| `services.rex.allowAnonymous`                    | Plain HTTP for the shared server. `openFirewall` opens its `port`. |
| `services.rex.loginServer.allowAnonymous`        | Plain HTTP listeners for the login server                   |

With `socketActivation` on, the module's socket unit also holds the Serve
socket, so a request through Tailscale Serve starts the server.

## Windows

On Windows, each listener works as follows:

| Listener           | On Windows                                                        |
| ------------------ | ----------------------------------------------------------------- |
| SSH                | Works, with Microsoft's OpenSSH Server. See [SSH with Windows](#ssh-with-windows) |
| Built-in Tailscale | Works, with `--tailscale`                                         |
| Tailscale Serve    | Refused, and so is `login-server://`                              |
| Tailnet address    | Works through `tailscaled` with its normal network adapter. Refused with a userspace `tailscaled` |
| Plain HTTP         | Works, with `--extra-listen` and `--allow-anonymous`              |
| Another VPN        | Works, with `--extra-listen` and `--allow-anonymous`              |

To keep listeners each time the server starts, give them to
`rex server install` after `--`, with or without `--user`:

```powershell
rex server install -- --tailscale
rex server install -- --extra-listen http://10.0.0.5:7297 --allow-anonymous
```

`rex server start` takes the same options, but they last only until the
server stops. See [Server Flags](https://www.superlogical.com/rex/docs/windows/running.md#server-flags).

### SSH with Windows

[SSH](#ssh) needs Microsoft's OpenSSH Server installed
and configured. From a terminal with **Run as administrator**:

```powershell
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Set-Service sshd -StartupType Automatic
Start-Service sshd
```

Its firewall rule lets SSH in only on networks set to Private. For an
administrator account, sshd reads keys from
`C:\ProgramData\ssh\administrators_authorized_keys`, not from
`~\.ssh\authorized_keys`.

### The Firewall

The first time a server that you started listens on a TCP port, Windows
Security asks "Do you want to allow public and private networks to access
this app?" for Rex Server. Choose **Allow**.

**Cancel leaves the port blocked.** Windows adds Block rules named
"Rex Server" as soon as the prompt appears, and Cancel keeps them. Later
starts don't ask again, and connections time out. To undo it, go to
**Windows Security > Firewall & network protection > Allow an app through
firewall** and allow Rex Server, or delete the rules from a terminal
started with **Run as administrator**:

```powershell
Remove-NetFirewallRule -DisplayName "Rex Server"
```

**The Windows Service requires manual setup.** Nobody may be signed in to see a
prompt, so Windows blocks its port without one, and adds no rules. Allow
`rex.exe` ahead of time from a terminal started with
**Run as administrator**:

```powershell
New-NetFirewallRule -DisplayName "Rex Server" -Direction Inbound `
  -Program "C:\Program Files\Rex Server\rex.exe" -Action Allow
```

For the WinGet zip, use the path that `(Get-Command rex).Source` prints. A
Block rule for the same path wins over this one, so delete those first.

Each rule names one path of `rex.exe`. Switching to another WinGet channel,
or between the WinGet zip and the MSI, moves `rex.exe`, so you need to
allow it again. An MSI upgrade keeps its folder, and its rules.
