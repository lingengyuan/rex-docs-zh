---
title: "Privacy & Telemetry"
canonical_url: https://www.superlogical.com/rex/docs/reference/privacy
---

# Privacy & Telemetry

**Rex doesn't collect telemetry.** It has no usage analytics, no crash
reporting of its own, and no account or license checks.

This page lists every network connection Rex makes, when it makes it,
and what it sends, for each part of Rex. Programs you run inside Rex
aren't covered. They make their own connections, and we don't control
them.

**Rex is still in testing.** Rex changes quickly and this page could fall
behind. If anything here is wrong, please apply
[Hanlon's razor](https://en.wikipedia.org/wiki/Hanlon%27s_razor): assume
it's a mistake, not malice, and report it in the beta Discord so we can
fix it.

## Outbound Connections

This is the list of outbound connections that Rex may make.

| Connection      | When                                                | Where                             |
| --------------- | --------------------------------------------------- | --------------------------------- |
| Update check    | Rex for Mac, at launch and once a day               | Superlogical's update server      |
| Remote servers  | Only servers you add                                | The servers you add               |
| Crash reports   | Rex for iOS, if you share them or use TestFlight    | Apple, then Superlogical          |
| Package updates | Linux and WinGet, when your package manager updates | Superlogical's package repository |
| Tailscale       | Only if you turn it on                              | Tailscale's servers               |

## Rex for Mac

### Update Checks

Rex for Mac checks for new versions at launch and then once a day by
downloading a signed feed of releases from Superlogical's update server.
Update checks can't be turned off.

Each check sends only what any web request does:

- Your IP address.
- A user agent with the app's name and version, such as
  `Rex Beta/0.1.0 Sparkle/2.9.6`.

It doesn't send an account, a device identifier, a system profile, or
anything about how you use Rex. An update is downloaded only when you
choose to install it.

### The Local Server

Rex for Mac runs a Rex server on your Mac and talks to it over a Unix
socket, so that traffic never leaves your machine. The app starts it
without any network listeners or Tailscale.

### Remote Servers

Rex for Mac connects only to the servers you add. It stays connected to
them, and reconnects at launch, until you remove them. It doesn't look
for servers on your network.

## Rex for iOS

Rex for iOS doesn't collect telemetry of its own. Apple collects some
data for every app, and shares it with Superlogical only if you allow it.

### Crash Reports and Analytics

If **Share With App Developers** is on, in **Settings > Privacy &
Security > Analytics & Improvements**, Apple sends us:

- Crash reports, with the device model, iOS version, app version, and
  where in Rex's code the crash happened.
- Diagnostics such as hangs, slow launches, and heavy battery or disk use.
- App Store analytics, such as sessions and active devices. This data
  is combined with other users' so no one person can be identified.

None of this data includes any extra app-specific metadata such as
your server list, names, session layouts, terminal contents, etc. It is
only the generic app data that all App Store apps report. With
**Share With App Developers** off, Apple doesn't send us any of it.

Apple always reports how many times Rex was downloaded, as it does for
every app, whatever this setting is.

If you use a TestFlight build (a preview release), TestFlight sends us
crash reports and any feedback you submit, regardless of the **Share With
App Developers** setting. This is a requirement of TestFlight.

### Updates

Rex for iOS never checks for updates itself. The App Store or TestFlight
updates it.

### Remote Servers

Rex for iOS connects only to the servers you add, the same way Rex for
Mac does. It doesn't look for servers on your network.

## Rex Server (All Platforms)

With default settings, the Rex server and the `rex` CLI make no outbound
connections.

### Updates

The server never checks for updates itself. On Linux, your system's
package manager updates it along with your other packages, from
Superlogical's package repository. With Nix, it's updated from
Superlogical's servers when you update your flake. On Windows, WinGet
checks Superlogical's WinGet source and downloads from Superlogical's
servers, but only when a `winget` command names it with `--source rex`.

These requests send only what the package manager or Nix always sends,
such as your IP address and its user agent.

`winget list` and `winget upgrade` normally send each source the product
codes, names and publishers of the programs installed on your PC. Rex's
WinGet source declares those fields unsupported, so WinGet leaves them out
of its searches, and the source never learns what else you have
installed. It answers from the list of Rex releases, and doesn't record
the searches it receives.

### Remote Servers

The CLI connects to another server only when you name one, with
`--server`, `REX_SERVER`, `rex home`, or `rex hosts`.

### Built-in Tailscale

[Built-in Tailscale](https://www.superlogical.com/rex/docs/linux/remote-access.md#built-in-tailscale) is off
until you turn it on. When it's on, the server runs its own Tailscale
device, which connects to Tailscale like any other device does:

- Tailscale's coordination server, to sign in and join your tailnet.
- Tailscale's relay servers, and other devices on your tailnet.
- Your router, to open a port with UPnP, NAT-PMP, or PCP.
- Let's Encrypt, for the server's HTTPS certificate.

The Tailscale device also uploads its logs and client metrics to
Tailscale, as Tailscale's own apps do by default. These are Tailscale's
logs about the connection, not your terminal contents. If your tailnet's
admin turns on network flow logs, those go to Tailscale too.
[Tailscale's privacy policy](https://tailscale.com/privacy-policy) covers
this data. None of it goes to Superlogical.

### Your Machine's Tailscale

With Tailscale Serve or a tailnet address, Rex only asks the Tailscale
already installed on your machine who is connecting, over its local
socket, and makes no connections of its own.
