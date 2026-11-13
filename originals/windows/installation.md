---
title: "Installing on Windows"
canonical_url: https://www.superlogical.com/rex/docs/windows/installation
---

# Installing on Windows

Rex can run as a server on Windows so that clients can access it as a
remote host.

**IMPORTANT:** Rex on Windows is in testing and is currently open to
a subset of testers in Discord. We will extend testing to more people
soon.

On Windows, every server is a personal server, which runs as your own
account. You can configure the Rex server to start at boot or at sign-in,
as [Running on Windows](https://www.superlogical.com/rex/docs/windows/running.md) explains.
[Server Modes](https://www.superlogical.com/rex/docs/linux/server-modes.md),
[Shared Server](https://www.superlogical.com/rex/docs/linux/shared-server.md) and
[Login Server](https://www.superlogical.com/rex/docs/linux/login-server.md) _do not apply to Windows_.

## System Requirements

| Requirement  | Supported                                                                 |
| ------------ | ------------------------------------------------------------------------- |
| Release      | Windows 10 1809 or later                                                  |
| Architecture | x86-64, ARM64                                                             |
| Packages     | WinGet, MSI, or Zip

## Install

Rex isn't signed yet, so while it's in testing, Windows may warn that the
publisher is unknown.

Every installation scenario installs `rex.exe` and puts it on your PATH,
but **does not automatically start a server or install a Windows Service.**
You must do this manually with `rex server install` after Rex is installed.

### WinGet (Recommended)

WinGet is the recommended way to install Rex Server. You can install
via WinGet from either a Zip source (default) or MSI:


Administrator rights are required to add a new WinGet source, so run
the first line in a terminal with "Run as Administrator" rights.

The **WinGet** tab installs Rex for your own account, with no administrator
rights. The **WinGet (MSI)** tab installs it for the whole machine instead,
as explained in [MSI](#msi).

After installation, `rex` is added to your `PATH`. PATH changes require
opening a new terminal, so open a new terminal to verify this.

### MSI


The MSI installs Rex for every account, into `%ProgramFiles%\Rex Server`,
and adds that folder to the system PATH. It needs administrator rights.

The download above is the x86-64 MSI. On ARM64, use the **WinGet (MSI)**
tab or the [zip](#zip). Open the MSI to run its setup wizard, or install
it without a window from a terminal opened with **Run as administrator**:

```powershell
msiexec /i rex-windows-amd64.msi /qn
```

To install somewhere other than `%ProgramFiles%\Rex Server`, add
`INSTALLDIR="D:\Tools\Rex Server"`.

### Zip

The zip holds Rex's files with no installer.

{#if download}

Download the newest preview for your machine:

<ul>
{#each download.zips as zip}
<li><a href={zip.href}>{zip.filename}</a> ({zip.arch})</li>
{/each}
</ul>

{:else}

The downloads show here for testers with the Windows role.

{/if}

If you are using the Zip, it is expected that you know how to move it into
a proper location and add `rex.exe` to your `PATH`.

## Channels

Rex publishes to three channels, each with its own WinGet package:

| Channel    | Package                           | What it gets                         |
| ---------- | --------------------------------- | ------------------------------------ |
| `stable`   | `Superlogical.RexServer`          | Tagged stable releases      |
| `preview`  | `Superlogical.RexServer.Preview`  | Tagged previews of the next release  |
| `snapshot` | `Superlogical.RexServer.Snapshot` | Development builds   |

The install commands use `preview`. Until the first stable release,
`winget install Superlogical.RexServer` fails, because WinGet treats a
channel with no release as a package that doesn't exist.

To switch channels, remove the package you have, as
[Removing Rex](#removing-rex) shows, then install the other one with
`--source rex`.

## Package Contents

All packages have the same set of files:

| File                      | What it is                                                     |
| ------------------------- | -------------------------------------------------------------- |
| `rex.exe`                 | The server and the CLI, in one binary                          |
| `OpenConsole.exe`         | The console host from Windows Terminal |
| `LICENSE-OpenConsole.txt` | The license of `OpenConsole.exe`                               |

Each way of installing puts them in its own folder:

| Package | Folder                                                                  | Added to    |
| ------- | ----------------------------------------------------------------------- | ----------- |
| WinGet  | `%LocalAppData%\Microsoft\WinGet\Packages\Superlogical.RexServer.Preview_…` | User PATH   |
| MSI     | `%ProgramFiles%\Rex Server`                                             | System PATH |
| Zip     | The folder you extract it into                                          | User PATH, once you add it |

## Removing Rex

**Run `rex server uninstall` before you remove the package.** Otherwise the
Windows Service or sign-in entry that `rex server install` made is left
pointing at a `rex.exe` that's gone. Removing the service needs a terminal
opened with **Run as administrator**.

Removing the package doesn't stop a server that's running, so stop it with
`rex server stop`. Then remove the package. For the zip, use a normal
terminal, because WinGet won't remove it from one opened with **Run as
administrator**:

```powershell
winget uninstall --id Superlogical.RexServer.Preview --source rex
```

For an MSI you installed yourself, remove "Rex Server" in
**Add or Remove Programs** instead.

For a zip, delete its folder and take it out of your user PATH.

WinGet leaves the zip's folder on your user PATH, though the folder is
gone. You can take it out of your PATH by hand.

Your configuration, `%AppData%\rex\init.lua`, and Rex's state and logs, in
`%LocalAppData%\rex`, stay. Delete them to remove every trace of Rex.
