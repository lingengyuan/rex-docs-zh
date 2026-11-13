---
title: "Running on Windows"
canonical_url: https://www.superlogical.com/rex/docs/windows/running
---

# Running on Windows

On Windows, every Rex server can only login as a single account:
the account that installs the Windows service.
[Server Modes](https://www.superlogical.com/rex/docs/linux/server-modes.md),
[Shared Server](https://www.superlogical.com/rex/docs/linux/shared-server.md) and
[Login Server](https://www.superlogical.com/rex/docs/linux/login-server.md) are for Linux and FreeBSD, and don't
apply here.

## Quickstart

This section documents the recommended setup to get up and running quickly.
It purposely omits many details about how everything works. We recommend
you read the later sections in detail to understand.

1. Install Rex with WinGet, as
   [Installing on Windows](https://www.superlogical.com/rex/docs/windows/installation.md#winget-recommended)
   shows.

2. Open a terminal with **Run as administrator**, and install and start
   Microsoft's OpenSSH Server:

   ```powershell
   Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
   Set-Service sshd -StartupType Automatic
   Start-Service sshd
   ```

3. In the same terminal, add your public key, such as the contents
   of `~/.ssh/id_ed25519.pub`. For an administrator account, sshd reads
   it from this file, and only if only administrators can change it:

   ```powershell
   Add-Content C:\ProgramData\ssh\administrators_authorized_keys "ssh-ed25519 AAAA... alice@mac"
   icacls.exe C:\ProgramData\ssh\administrators_authorized_keys /inheritance:r /grant Administrators:F /grant SYSTEM:F
   ```

   For a standard account, add the key to `~\.ssh\authorized_keys`
   instead.

4. On your Mac, connect to the PC, where `pc` is its name or address:

   ```sh
   rex -S ssh://alice@pc ls
   ```

   In Rex for Mac, choose **Add Remote Host…** and enter
   `ssh://alice@pc`.

The first connection starts your server, and it keeps running until you
stop it. Windows lets SSH in only on networks set to Private. For
Tailscale and other ways to connect, see
[Remote Access](https://www.superlogical.com/rex/docs/linux/remote-access.md#windows).

## Server Lifetimes

How you run or install the server determines how long it stays running:

| Started by                  | Starts                        | Keeps running                          | Needs administrator |
| --------------------------- | ----------------------------- | -------------------------------------- | ------------------- |
| Any `rex` command           | When you run it               | Until about 10 s after its last client | No                  |
| An `ssh://` connection      | When it connects              | Until you stop it                      | No                  |
| `rex server start`          | Now                           | Until you stop it or sign out          | No                  |
| `rex server install --user` | Each time you sign in         | Until you sign out                     | No                  |
| `rex server install`        | At boot, as a Windows Service | Until shutdown, signed in or not       | Yes                 |

If you only use Rex locally while you're at your PC, let `rex` commands
autostart the server.

If you want to connect to Rex remotely, start it at boot with
`rex server install`. If you can't get administrator rights, then
start it at sign in with `rex server install --user`.

## CLI-Triggered Servers

Any `rex` command automatically starts a server if none is running:

```powershell
rex ls
```

An automatically started server stops on its own about 10 seconds after
its last session and its last connection close. To start one that keeps
running until you stop it or sign out, start it explicitly:

```powershell
rex server start
```

`rex server status`, `rex server logs` and `rex server stop` work as they
do on Linux. See [Personal Server](https://www.superlogical.com/rex/docs/linux/server-modes.md#personal-server).

The server listens on the named pipe `\\.\pipe\rex-<SID>`, where `<SID>`
is your account's security identifier. If you set `REX_RUNTIME_DIR`, the
name gets a suffix, so servers with different runtime directories don't
collide.

To keep `rex` commands from starting a server at all, set
`REX_AUTOSTART=0`.

## Starting at Boot

`rex server install` creates a Windows Service that starts your server at
boot and keeps it running while nobody is signed in. Run it from a
terminal started with **Run as administrator**:

```powershell
rex server install
```

The service runs as your own account, not as LocalSystem. The command
prints each change before it makes it:

- It creates the service `RexServer-<SID>`, shown as
  "Rex Server (PC\alice)" in the Services console. It's set to
  **Automatic (Delayed Start)** and runs `"<path to rex.exe>" server run`
  with your [server flags](#server-flags).
- It grants your account the right to log on as a service.
- It registers "Rex Server" as a source of the Event Log.
- It deletes the [sign-in entry](#starting-at-sign-in), if you added one.

If a server is already running and nothing is using it, the command stops
it and starts the service in its place. If the server has sessions or
clients, it keeps running, and the service starts at the next boot. The
command says which happened.

Running the command again is safe, and keeps your server flags. Run it
again after you move `rex.exe`, such as when you switch between the WinGet
zip and the MSI, so that the service runs the new path.

## Starting at Sign-In

`rex server install --user` starts your server each time you sign in to
Windows, and needs no administrator rights:

```powershell
rex server install --user
```

It adds a value named "Rex Server" to
`HKCU\Software\Microsoft\Windows\CurrentVersion\Run`, which runs
`rex server start` with your [server flags](#server-flags). It also starts
a server now if none is running. The server stops when you sign out.

Running the command again is safe, and keeps your server flags.

The value shows in the **Startup** tab of Task Manager, and in Settings
under **Apps > Startup**. If it's turned off there, Windows skips it, and
the command says so rather than turning it back on.

The sign-in entry and the Windows Service can't both start your server.
While the service exists, `rex server install --user` fails. Remove the
service first, as [Removing the Service](#removing-the-service) shows.

## Server Flags

`rex server tailscale on` and other changes to a running server last only
until it stops. To give your server flags each time it starts, put them
after `--`:

```powershell
rex server install -- --tailscale
rex server install --user -- --extra-listen tailnet://:7297
```

The Windows Service runs `server run` with the flags, and the sign-in
entry runs `server start` with them. With `--user`, the server that the
command starts right away gets them too. `rex server run --help` and
`rex server start --help` list the flags that each one takes.

What `--` does when you run the command again:

| Command                             | Server flags                   |
| ----------------------------------- | ------------------------------ |
| `rex server install`                | Keeps the flags already set    |
| `rex server install -- --tailscale` | Replaces them with the new ones |
| `rex server install --`             | Removes them                   |

The same goes for `--user`. Moving from `--user` to the Windows Service
carries the sign-in entry's flags over to the service.

The command checks the flags before it changes anything, and refuses
those that the server would refuse. It also refuses these, which don't
work for a server that Windows starts:

| Flag                          | Why                                                         |
| ----------------------------- | ----------------------------------------------------------- |
| `--listen`                    | `rex` commands look for the server on its named pipe. Use `--extra-listen` to add an endpoint. |
| `--exit-empty`                | The service would stop once it's idle, and Windows wouldn't start it again until the next boot. |
| `--tailscale-auth-key-file -` | Windows gives the server no standard input. Give the path of a file instead. |

A server that's already running keeps its old flags until it restarts.
See [Stopping and Restarting](#stopping-and-restarting). `rex server start`
doesn't read the sign-in entry, so to restart that server with its flags,
stop it and run `rex server install --user` again, or sign in again.

## Administrator Rights

**A server that the Windows Service starts runs without administrator
rights, even if your account is an administrator.** The service starts it
with a reduced copy of its token, so every terminal, block plugin and
`rex.exec` program runs as it would after a normal sign-in.

A server that `rex server start` or any `rex` command starts gets the
same reduced rights, even from a terminal opened with **Run as
administrator**, or from an administrator's `ssh` session. If Windows
can't make the reduced token, server startup fails.

**`rex server run` in a terminal opened with Run as administrator keeps
full administrator rights.** We assume in this scenario you explicitly want
this.

## Logs

`rex server logs` shows the log of your server however it was started,
the service included:

```powershell
rex server logs --follow
```

The log is in `%LocalAppData%\rex\servers`. Rex clears it before it grows
past 50MiB.

The Windows Service also writes to the Application log in Event Viewer,
under the source "Rex Server":

| Event ID | Level       | Meaning                       |
| -------- | ----------- | ----------------------------- |
| 1        | Information | The service is starting       |
| 2        | Information | The service is running        |
| 3        | Information | Windows asked it to stop      |
| 4        | Information | The service stopped           |
| 5        | Error       | The service stopped with an error, which the event names |

## Stopping and Restarting

`rex server stop` stops your server, however it was started. This ends
every program running in its sessions. The server saves its session
layouts, and `rex ls` lists them again once it restarts:

```powershell
rex server stop
```

When the service started it, the service stays stopped until the next
boot, or until you start it again. To start or stop the service, run
these from a terminal started with **Run as administrator**:

```powershell
sc.exe start RexServer-<SID>
sc.exe stop RexServer-<SID>
```

The Services console works too. Look for "Rex Server (PC\alice)". When the
service stops, it gives the server 15 seconds to save its sessions and
exit before it ends it.

While the service is stopped, a `rex` command can start a server on its
own, and `sc.exe start` then fails until that server stops. Set
`REX_AUTOSTART=0` if you want to keep it from happening.

## Removing the Service

`rex server uninstall` stops the Windows Service, which ends every program
running in its sessions, and then deletes it. Run it from a terminal
started with **Run as administrator**:

```powershell
rex server uninstall
```

It also unregisters "Rex Server" as a source of the Event Log, unless
another account's service still uses it, and deletes the
[sign-in entry](#starting-at-sign-in).

Once a service exists, the command needs administrator rights, even to
delete only the sign-in entry. Without a service, it needs none, and a
server that the sign-in entry started keeps running. Stop it with
`rex server stop`.

Your account keeps the right to log on as a service, because other
services may need it. To remove it, open Local Security Policy
(`secpol.msc`) and go to **Local Policies > User Rights Assignment >
Log on as a service**.

## Terminals and Shells

Each terminal runs the first of `pwsh.exe` and `powershell.exe` on the
server's PATH, or `%ComSpec%` if neither is there. There's no setting to
change the default. To run another shell, give it as the command:

```powershell
rex new -- cmd.exe
```

A server started by a `rex` command, by `rex server start` or by the
sign-in entry passes terminals only an allowlist of variables: the usual
Windows ones, such as `USERPROFILE`, `APPDATA` and `ProgramFiles`, common
toolchain variables, such as `JAVA_HOME` and `GOPATH`, and `PATH`, `REX_*`,
`XDG_*`, `LC_*` and the proxy variables. To pass others, start the server
with `--env`:

```powershell
rex server start --env NAME --env OTHER=value
```

`--env` applies only when it starts a new server. To change it, stop the
server and start it again. To keep it each time you sign in, give it to
the sign-in entry as a [server flag](#server-flags):

```powershell
rex server install --user -- --env NAME
```

A server that the Windows Service starts gets the system and user
variables Windows had when the service started. A variable you add in
Settings reaches its terminals after the service restarts. The service
refuses `--env`, because only `rex server start` takes it.

Terminals have `TERM` set to `xterm-256color`, and `rex terminfo setup` is
refused on Windows. Closing a terminal ends every process in it at once.

## Not Available on Windows

These parts of Rex need a Unix system:

| Feature                                        | On Windows                                               |
| ---------------------------------------------- | -------------------------------------------------------- |
| The shared server and the login server         | Each account runs its own server                         |
| Starting on demand through socket activation   | Any `rex` command starts the server                      |
| `--socket-mode`                                | Only your account can open the pipe                      |
| `tailnet-serve://` and `login-server://` listeners | Rex's own Tailscale node, with `rex server install -- --tailscale` |
| `tailnet://` with a userspace `tailscaled`     | `tailscaled` with its normal network adapter             |
| `rex terminfo setup`                           | Terminals keep `TERM=xterm-256color`                     |
| `rex server install ssh://` to a Windows PC    | Install Rex on the PC, then reach it with an [`ssh://` endpoint](https://www.superlogical.com/rex/docs/linux/remote-access.md#ssh-with-windows) |
| Reopening the log with `SIGHUP`                | `rex server logs` and the 50MiB limit                    |
