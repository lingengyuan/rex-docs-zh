---
title: "Mac Settings"
canonical_url: https://www.superlogical.com/rex/docs/reference/mac-settings
---

# Mac Settings

This page lists every setting in Rex for Mac and where to find it. Anything tagged [Bleeding Edge](https://www.superlogical.com/rex/docs/reference/mac-settings.md#setting-app-version-update-channel) is on that update channel and not yet in Preview.

<div class="reference-page settings" hidden></div>

## Integrations

### Coding Agents

Teach Claude Code, Codex, OpenCode and Pi how to use Rex. In Settings > Integrations > Coding Agents. <span hidden>agents, ai, claude, claude code, codex, opencode, pi, skill, hooks, `rex skill setup`, llm, assistant, integrations</span>

| Setting | Description |
| --- | --- |
| <span id="setting-coding-agents-integrate-with-available-agents" data-entry="Integrate with available agents"></span>Integrate with available agents | Installs a Rex skill and session hooks for supported agents. <span hidden>In Settings &gt; Integrations &gt; Coding Agents.</span> <span hidden>install skill, remove skill, set up agents, uninstall, enable agents, disable agents, update skill</span> |

### Agent Behavior

Choose what Rex tells coding agents running in its terminals. In Settings > Integrations > Agent Behavior. <span hidden>agent instructions, agent rules, session hook</span>

| Setting | Description |
| --- | --- |
| <span id="setting-agent-behavior-let-agents-name-sessions" data-entry="Let agents name sessions"></span>Let agents name sessions | Let agents label the session after the task they're working on. Shown while Integrate with available agents is on. <span hidden>In Settings &gt; Integrations &gt; Agent Behavior.</span> <span hidden>rename session, session label, session name, auto name, title, label sessions</span> |

## Notifications

### In-App Notifications

Choose where floating notifications appear in the window. In Settings > Notifications > In-App Notifications. <span hidden>notifications, notification settings, alerts, banners, notification center, in app notifications, customize notifications</span>

| Setting | Description |
| --- | --- |
| <span id="setting-in-app-notifications-notification-position" data-entry="Notification position"></span>Notification position | Click a position in the window diagram to place notifications at the top or bottom, aligned left, center, or right. <span hidden>In Settings &gt; Notifications &gt; In-App Notifications.</span> <span hidden>notification position, notification placement, banner location, anchor, top left, top center, top right, bottom left, bottom center, bottom right</span> |

### Program Activity

Independently configure tab indicators, system notifications, Dock badges, and sounds for program activity. In Settings > Notifications > Program Activity. <span hidden>program activity, tab activity, activity indicators</span>

| Setting | Description |
| --- | --- |
| <span id="setting-program-activity-show-activity-in-tabs" data-entry="Show activity in tabs"></span>Show activity in tabs | Show working dots, progress pies, and needs-attention dots and messages on tabs when a program in them reports its status. <span hidden>In Settings &gt; Notifications &gt; Program Activity.</span> <span hidden>program status, process status, osc 7501, agent, claude, progress, progress pie, blocked, waiting, question, permission, error, failed, status dot, status badges, notification dot, badge, working, tab status, indicator, needs attention</span> |
| <span id="setting-program-activity-include-idle-processes-in-activity" data-entry="Include idle processes in activity"></span>Include idle processes in activity | Keep tabs whose programs report that they're idle in the Activity filter and popup, even after you've seen them. <span hidden>In Settings &gt; Notifications &gt; Program Activity.</span> <span hidden>idle, idle processes, idle agents, ready, activity filter, activity popup, keep idle, show idle, include idle, always show idle processes in activity, eye</span> |
| <span id="setting-program-activity-show-system-notifications" data-entry="Show system notifications"></span>Show system notifications | Send a macOS notification when a program reports a status while Rex is in the background, independently of tab indicators. Clicking it opens the program's tab. <span hidden>In Settings &gt; Notifications &gt; Program Activity.</span> <span hidden>program notifications, agent notifications, background notifications, claude notification, notify when done, notify when blocked, notifications without tab indicators</span> |
| <span id="setting-program-activity-badge-dock-icon" data-entry="Badge Dock icon"></span>Badge Dock icon | Show on Rex's Dock icon how many tabs have a program that's blocked, failed, or finished that you haven't seen. <span hidden>In Settings &gt; Notifications &gt; Program Activity.</span> <span hidden>dock badge, badge count, app icon badge, unread count, red badge, badge application icon, dock icon</span> |
| <span id="setting-program-activity-play-sounds" data-entry="Play sounds"></span>Play sounds | Play a sound when a program in a tab is blocked, reports an error, or finishes. <span hidden>In Settings &gt; Notifications &gt; Program Activity.</span> <span hidden>sound, audio, chime, alert sound, beep, bell, audible, monoh, sound effects, program finished, done sound, mute, silence</span> |
| <span id="setting-program-activity-sound-volume" data-entry="Sound volume"></span>Sound volume | Set how loud the blocked, error, and done sounds play, from quieter to louder than the default. <span hidden>In Settings &gt; Notifications &gt; Program Activity.</span> <span hidden>volume, loudness, louder, quieter, too quiet, too loud, sound level, alert volume, notification volume, boost, gain</span> |
| <span id="setting-program-activity-working" data-entry="Working"></span>Working | Enable or disable all activity for working programs, or configure their tab indicators, notifications, Dock badges, and sounds individually. <span hidden>In Settings &gt; Notifications &gt; Program Activity.</span> <span hidden>working status, busy, progress, spinner, running, disable all working, enable working status</span> |
| <span id="setting-program-activity-blocked" data-entry="Blocked"></span>Blocked | Enable or disable all activity for programs waiting for you, or configure their tab indicators, notifications, Dock badges, and sounds individually. <span hidden>In Settings &gt; Notifications &gt; Program Activity.</span> <span hidden>blocked status, waiting, question, permission, approval, sign in, attention sound, blocked notifications, disable all blocked, enable blocked status</span> |
| <span id="setting-program-activity-error" data-entry="Error"></span>Error | Enable or disable all activity for programs reporting errors, or configure their tab indicators, notifications, Dock badges, and sounds individually. <span hidden>In Settings &gt; Notifications &gt; Program Activity.</span> <span hidden>error status, failed, failure, error sound, disable all errors, enable error status</span> |
| <span id="setting-program-activity-done" data-entry="Done"></span>Done | Enable or disable all activity for finished programs, or configure their tab indicators, notifications, Dock badges, and sounds individually. <span hidden>In Settings &gt; Notifications &gt; Program Activity.</span> <span hidden>done status, finished, complete, completed, success sound, finish sound, disable all done, enable done status</span> |

### System Notifications

Choose whether terminal programs can send native macOS notifications, and see the ones Rex sends for Tailscale. In Settings > Notifications > System Notifications. <span hidden>native notifications, macOS notifications, mac notifications, tailscale alerts, terminal notifications</span>

| Setting | Description |
| --- | --- |
| <span id="setting-system-notifications-terminal-notifications" data-entry="Terminal notifications"></span>Terminal notifications | Let programs send native notifications with OSC 9 or OSC 777. <span hidden>In Settings &gt; Notifications &gt; System Notifications.</span> <span hidden>osc 9, osc 777, osc9, osc777, desktop notification, notify-send, escape sequence, program notifications, printf notify</span> |
| <span id="setting-system-notifications-tailscale-sign-in" data-entry="Tailscale sign-in"></span>Tailscale sign-in | A native notification when Rex needs you to sign in to Tailscale. <span hidden>In Settings &gt; Notifications &gt; System Notifications.</span> <span hidden>tailscale login notification, sign in, authentication, account</span> |
| <span id="setting-system-notifications-tailscale-device-approval" data-entry="Tailscale device approval"></span>Tailscale device approval | A native notification when a tailnet administrator must approve this Mac. <span hidden>In Settings &gt; Notifications &gt; System Notifications.</span> <span hidden>device approval notification, approve mac, tailnet administrator, authorization</span> |
| <span id="setting-system-notifications-tailscale-failures" data-entry="Tailscale failures"></span>Tailscale failures | A native notification when Tailscale stops or reports an error. <span hidden>In Settings &gt; Notifications &gt; System Notifications.</span> <span hidden>tailscale failure notification, tailscale stopped, connection error, offline</span> |

## Server

### Rex Server

Manage the local server, compatibility, and diagnostics. In Settings > Server > Rex Server. <span hidden>start, stop, restart, status, version, api, diagnostics</span>

| Setting | Description |
| --- | --- |
| <span id="setting-rex-server-server-status" data-entry="Server status"></span>Server status | See whether the local server is running and for how long, with version and API details in its info popover. <span hidden>In Settings &gt; Server &gt; Rex Server.</span> <span hidden>health, running, stopped, preparing server, failed, error, source checkout, server details, server version, api revision, uptime, running time, how long, started, duration</span> |
| <span id="setting-rex-server-compatibility" data-entry="Compatibility"></span>Compatibility | When an update, compatibility issue, or pending settings change is detected, see the discrepancy and update or restart the server when appropriate. <span hidden>In Settings &gt; Server &gt; Rex Server.</span> <span hidden>incompatible server, restart recommended, update rex app, restart server, upgrade server, newer server, available version, restart required, new features, apply settings, use bundled server, older app, backward compatible, a newer server is available, updating is optional, optional update, new API features are available, newer API features, unavailable features, server settings have changed, cannot connect to this server, this server requires a newer rex app, server and app are incompatible, reconnect, server compatibility, pending changes, update server, restart using included server, restart from source</span> |

### Remote Address

Check serving progress, copy the address, or pair another device. In Settings > Server > Remote Address. <span hidden>tailnet, https, endpoint, connectivity</span>

| Setting | Description |
| --- | --- |
| <span id="setting-remote-address-remote-address" data-entry="Remote Address"></span>Remote Address | Check serving progress and certificate readiness, retry, copy the address, or pair a device using its QR code. <span hidden>In Settings &gt; Server &gt; Remote Address.</span> <span hidden>copy remote address, tailscale connection progress, https, dns, hostname, endpoint, copy, qr, scan, pair, device, iphone, ipad, certificate, waiting for certificate, tls, ssl, secure, starting, stopping, connection progress, retry, connected, disconnected, approval, error, dns recovery</span> |

### Server Version

See the server's version and whether it works with this app, and install another. In Settings > Server > Server Version. <span hidden>version, release, what's new, download</span>

| Setting | Description |
| --- | --- |
| <span id="setting-server-version-installed" data-entry="Installed"></span>Installed | See which Rex Server is running and whether this app can use all of it. Its info button chooses the server channel. <span hidden>In Settings &gt; Server &gt; Server Version.</span> <span hidden>server version, running version, bundled, downloaded, works with this app, works with limits, unavailable features, release notes, changelog, server channel, bundled server, install server, download server, server release, update server, snapshot server, preview server, source checkout, source directory, checkout, repository, repo, build from source, local build, development server, installation</span> |

### Tailscale

Connect Rex to your tailnet and control who can access it. In Settings > Server > Tailscale. <span hidden>network, vpn, remote, secure, sharing</span>

| Setting | Description |
| --- | --- |
| <span id="setting-tailscale-serve-over-tailscale" data-entry="Serve over Tailscale"></span>Serve over Tailscale | Enable or disable access to Rex over your tailnet. <span hidden>In Settings &gt; Server &gt; Tailscale.</span> <span hidden>connect, network, vpn, share, enable, disable</span> |
| <span id="setting-tailscale-preferred-hostname" data-entry="Preferred Hostname"></span>Preferred Hostname | Choose this Mac’s Tailscale hostname while serving. The assigned address may differ. <span hidden>In Settings &gt; Server &gt; Tailscale.</span> <span hidden>hostname, device name, dns, rename, machine, address, assigned address, host id, durable host id, identity</span> |
| <span id="setting-tailscale-limit-access-to-your-tailscale-account" data-entry="Limit access to your Tailscale account"></span>Limit access to your Tailscale account | Restrict callers to your account or allow tailnet members. <span hidden>In Settings &gt; Server &gt; Tailscale.</span> <span hidden>security, authentication, identity, permissions, owner, members, acl</span> |
| <span id="setting-tailscale-tags" data-entry="Tags"></span>Tags | See this device’s Tailscale tags. Sign out and back in to change them. <span hidden>In Settings &gt; Server &gt; Tailscale.</span> <span hidden>tag, tagged, acl tags, advertise tags, tailnet policy, machine identity, owner, access</span> |
| <span id="setting-tailscale-control-server" data-entry="Control Server"></span>Control Server | See which control server this device signs in with. Sign out and back in to change it. <span hidden>In Settings &gt; Server &gt; Tailscale.</span> <span hidden>control url, control plane, coordination server, login server, self-hosted, custom server</span> |
| <span id="setting-tailscale-sign-in-to-tailscale" data-entry="Sign in to Tailscale"></span>Sign in to Tailscale | Check your account and sign-out progress, configure a hostname and sign in, reopen or cancel enrollment, turn off serving while signed out, or sign out. <span hidden>In Settings &gt; Server &gt; Tailscale.</span> <span hidden>login, tailscale login, sign in, sign in to tailscale, log in, sign out, turn off, turn off tailscale, disable tailscale, needs login, stop asking to sign in, account, status, signed in to tailscale, enrolled account, signing in to tailscale, browser sign in, open browser, reopen browser, preparing to sign in, this may take a moment, ready to connect, awaiting connection, finish the process in your browser, taking longer than usual, slow sign in, cancel sign in, cancel login, signing out of tailscale, remove saved login, sign out progress</span> |

## Interface

### Appearance

Choose the color scheme, interface materials, and theme tint. In Settings > Interface > Appearance. <span hidden>look, visual, display, theme</span>

| Setting | Description |
| --- | --- |
| <span id="setting-appearance-color-scheme" data-entry="Color scheme"></span>Color scheme | Select a live Auto, Light, or Dark material preview. Auto follows the system appearance. <span hidden>In Settings &gt; Interface &gt; Appearance.</span> <span hidden>colour, light, dark, auto, automatic, system, night mode, cards</span> |
| <span id="setting-appearance-interface-style" data-entry="Interface style"></span>Interface style | Preview Glass or Classic materials with the current theme tint and select a surface style. <span hidden>In Settings &gt; Interface &gt; Appearance.</span> <span hidden>glass, classic, liquid glass, material, native, system, modern, opaque, translucent, cards</span> |
| <span id="setting-appearance-tint-with-theme" data-entry="Tint with theme"></span>Tint with theme | Apply the selected theme's colors to interface surfaces. <span hidden>In Settings &gt; Interface &gt; Appearance.</span> <span hidden>tint, theme colors, theme colours, palette, themed, blended, blend theme, use theme</span> |
| <span id="setting-appearance-use-glass-for-panes" data-entry="Use glass for panes"></span>Use glass for panes | Available with the Glass interface style: add glass to panes alongside window and tab materials. <span hidden>In Settings &gt; Interface &gt; Appearance.</span> <span hidden>pane glass, no glass, remove glass, liquid glass, pane material, transparency</span> |

### Toolbar

Choose the toolbar layout and whether the toolbar always shows or shows on hover. In Settings > Interface > Toolbar. <span hidden>workspace, chrome, layout, navigation, tab bar, title bar</span>

| Setting | Description |
| --- | --- |
| <span id="setting-toolbar-toolbar-layout" data-entry="Toolbar layout"></span>Toolbar layout | Place the toolbar and its tabs Above or Below the panes, or on the Left or Right of the window. <span hidden>In Settings &gt; Interface &gt; Toolbar.</span> <span hidden>toolbar layout, tab style, tab placement, tab layout, horizontal tabs, vertical tabs, vertical, horizontal, sidebar, navigation, orientation, sidebar position, above, left side, right side, bottom, below, bottom tabs, tab bar at bottom, left sidebar, right sidebar, edge, location</span> |
| <span id="setting-toolbar-toolbar-behavior" data-entry="Toolbar behavior"></span>Toolbar behavior | Always show the toolbar, Show on hover: hide the tab bar, or the sidebar's title row, until the pointer reaches the top of the window, or keep it Hidden until Reveal Toolbar. <span hidden>In Settings &gt; Interface &gt; Toolbar.</span> <span hidden>always show, on hover, show toolbar on hover, hidden, never, never show toolbar, reveal toolbar, toolbar visibility, auto-hide toolbar, autohide, hide toolbar, hide tab bar, floating toolbar, reveal, tab bar, title bar, title row, traffic lights, distraction free, minimal, full height, chrome, hot corner, hot corners</span> |

### Tab behavior

Choose whether tabs above the panes fill the tab bar. Opens from Customize tabs under Toolbar. In Settings > Interface > Tab behavior. <span hidden>tabs, tab bar, tab sizing, customize tabs</span>

| Setting | Description |
| --- | --- |
| <span id="setting-tab-behavior-tabs-fill-available-space" data-entry="Tabs fill available space"></span>Tabs fill available space | Available with horizontal tabs: expand tabs equally to fill the bar, showing backgrounds only for two or more tabs. <span hidden>In Settings &gt; Interface &gt; Tab behavior.</span> <span hidden>fill available space, tab width, stretch, expand, full width, equal width, maximum, capped</span> |

### Tab icons

Choose how many pane icons tabs show, and how tab and shell icons are colored. Opens from Customize tabs under Toolbar. In Settings > Interface > Tab icons. <span hidden>workspace, icons, symbols, pane cards, icon stack, tab icons, tabs, customize tabs</span>

| Setting | Description |
| --- | --- |
| <span id="setting-tab-icons-use-color-for-tab-icons" data-entry="Use color for tab icons"></span>Use color for tab icons | Show colored icons Always, For active panes, For active tabs, or Never. <span hidden>In Settings &gt; Interface &gt; Tab icons.</span> <span hidden>colour, monochrome, grayscale, greyscale, saturation, always, never, active panes, active tabs, focused pane, selected tab</span> |
| <span id="setting-tab-icons-shell-icon-theme" data-entry="Shell icon theme"></span>Shell icon theme | Choose Default artwork, Use theme for background and foreground colors, or Use theme accent for accents. <span hidden>In Settings &gt; Interface &gt; Tab icons.</span> <span hidden>shell colors, shell colours, terminal icon, shell palette, default, use theme, use theme accent, accent, background, foreground, glyph</span> |
| <span id="setting-tab-icons-show-tab-icons" data-entry="Show tab icons"></span>Show tab icons | Show zero to three pane icons in vertical tabs, or up to five in horizontal tabs. <span hidden>In Settings &gt; Interface &gt; Tab icons.</span> <span hidden>icon count, icons per tab, number of icons, stack size, stack limit, icon count slider, slider, maximum, none, hide icons, no icons, zero icons, one icon, two icons, three icons, four icons, five icons, 0, 1, 2, 3, 4, 5, pane icons</span> |

### Panes

Adjust pane spacing and headers. In Settings > Interface > Panes. <span hidden>workspace, chrome, layout, density, spacing, split</span>

| Setting | Description |
| --- | --- |
| <span id="setting-panes-pane-style" data-entry="Pane style"></span>Pane style | Choose Comfortable or Compact pane surfaces and spacing. <span hidden>In Settings &gt; Interface &gt; Panes.</span> <span hidden>compact, comfortable, pane density, padding, gaps, spacing</span> |
| <span id="setting-panes-pane-header-behavior" data-entry="Pane header behavior"></span>Pane header behavior | Show the title and controls above each pane: Always show, Show on hover, or Hidden. <span hidden>In Settings &gt; Interface &gt; Panes.</span> <span hidden>pane headers, show pane headers, titles, toolbar, chrome, hide headers, always, always show, on hover, show on hover, hidden, never, hover, floating header, auto-hide header, pane header visibility</span> |

### Window

Available with sidebar toolbar layouts: choose whether the sidebar resizes the window, which swipe shows or hides it, and the size of its text. In Settings > Interface > Window. <span hidden>window sizing, window width, sidebar, layout, swipe, trackpad, text size</span>

| Setting | Description |
| --- | --- |
| <span id="setting-window-sidebar-text-size" data-entry="Sidebar text size"></span>Sidebar text size | Available with vertical tabs: set the size of session and tab titles in the sidebar, or follow the Sidebar icon size in System Settings. <span hidden>In Settings &gt; Interface &gt; Window.</span> <span hidden>sidebar text, text size, tab title size, session title size, larger text, bigger text, sidebar icon size, sidebar row size, row height, follow system size</span> |
| <span id="setting-window-preserve-width-when-resizing-sidebar" data-entry="Preserve width when resizing sidebar"></span>Preserve width when resizing sidebar | Available with vertical tabs: resize panes when showing or hiding the sidebar, keeping the window width unchanged. <span hidden>In Settings &gt; Interface &gt; Window.</span> <span hidden>keep window width, preserve window width, fixed window width, resizing sidebar, window size, resize window, shrink window, grow window, keep window size, show sidebar, hide sidebar, toggle sidebar, collapse sidebar, fold sidebar, pane width, maximized, full screen</span> |
| <span id="setting-window-show-back-and-forward-buttons" data-entry="Show Back and Forward buttons"></span>Show Back and Forward buttons | Add Back and Forward arrows to step through the panes you've focused: before the session picker in the tab bar, or beside Activity in the sidebar's title row. <span hidden>In Settings &gt; Interface &gt; Window.</span> <span hidden>navigate, navigation, history, browser, arrows, back, forward, previous, next, chevron, focus history, title row, sidebar buttons, tab bar buttons, navigate back, navigate forward, go back, pane history</span> |
| <span id="setting-window-use-a-gesture-to-toggle-the-sidebar" data-entry="Use a gesture to toggle the sidebar"></span>Use a gesture to toggle the sidebar | Available with vertical tabs: choose whether a swipe or an Option-swipe shows or hides the sidebar, or turn the gesture off. Hold the ⌥ key to scroll content sideways instead. <span hidden>In Settings &gt; Interface &gt; Window.</span> <span hidden>show or hide sidebar, option-swipe, option swipe, ⌥, off, disable swipe, turn off swipe, no gesture, disable gesture, magic mouse, mouse, one finger, option scroll, alt scroll, option key, alt key, hold option, modifier, swipe, two finger swipe, two fingers, trackpad, gesture, trackpad gesture, sidebar swipe, swipe sidebar, fold sidebar, horizontal scroll, scroll sideways, sideways, side scroll, scroll left, scroll right, tui, diff, long lines</span> |

### Padding

Set the space between a pane's edges and its terminal text, and whether a program's colors fill it. Opens from Customize panes under Interface › Panes. In Settings > Interface > Padding. <span hidden>pane padding, terminal padding, inset, margin, margins, gutter, spacing around text, edges, window padding, pane background, background</span>

| Setting | Description |
| --- | --- |
| <span id="setting-padding-padding-x" data-entry="Padding X"></span>Padding X | Set the space to the left and right of the terminal text. <span hidden>In Settings &gt; Interface &gt; Padding.</span> <span hidden>horizontal padding, x padding, left padding, right padding, side padding, horizontal inset, horizontal margin</span> |
| <span id="setting-padding-padding-y" data-entry="Padding Y"></span>Padding Y | Set the space below the terminal text, and above it when pane headers are hidden. <span hidden>In Settings &gt; Interface &gt; Padding.</span> <span hidden>vertical padding, y padding, bottom padding, top padding, vertical inset, vertical margin</span> |
| <span id="setting-padding-fill-with-program-colors" data-entry="Fill with program colors"></span>Fill with program colors | Let a full-screen program color the padding Off, Automatic, or Always. <span hidden>In Settings &gt; Interface &gt; Padding.</span> <span hidden>padding color, colour, off, automatic, always, extend, extend always, background, edge cells, window-padding-color, program background, editor, full screen, tui</span> |
| <span id="setting-padding-include-pane-header" data-entry="Include pane header"></span>Include pane header | Color the pane header to match the program too, while the padding fills. <span hidden>In Settings &gt; Interface &gt; Padding.</span> <span hidden>match program backgrounds, tint, pane color, header color, pane background, terminal background, program background, editor, full screen, tui, neovim, vim, blend, match terminal</span> |

### Active Pane

Highlight the edges of the active pane and fade inactive ones. Opens from Customize panes under Interface › Panes. In Settings > Interface > Active Pane. <span hidden>customize panes, customize pane behavior, pane behavior, active pane, active panes, inactive panes, focused pane, unfocused panes, pane focus, focus appearance, dim inactive</span>

| Setting | Description |
| --- | --- |
| <span id="setting-active-pane-highlight-active-pane-edges" data-entry="Highlight active pane edges"></span>Highlight active pane edges | Highlight the edges of the focused pane, following focus. <span hidden>In Settings &gt; Interface &gt; Active Pane.</span> <span hidden>border, outline, focus ring, active border, focused pane, highlight, highlight active pane, edge highlight, indicator, focus indicator, show border on active pane</span> |
| <span id="setting-active-pane-highlight-color" data-entry="Highlight color"></span>Highlight color | Draw the highlight in the accent, a terminal palette color, or the terminal text color. <span hidden>In Settings &gt; Interface &gt; Active Pane.</span> <span hidden>accent, accent color, theme color, terminal text, terminal foreground, foreground color, text color, highlight color, border color, focus ring color, active pane border color, swatch, color swatches, palette, red, blue, green, yellow, cyan, magenta</span> |
| <span id="setting-active-pane-highlight-opacity" data-entry="Highlight opacity"></span>Highlight opacity | Set how strongly the highlight draws. <span hidden>In Settings &gt; Interface &gt; Active Pane.</span> <span hidden>opacity, transparency, alpha, translucent, faint, subtle, strength, border opacity, border strength, focus ring opacity, highlight strength, active pane border opacity</span> |
| <span id="setting-active-pane-animate-active-pane-highlight" data-entry="Animate active pane highlight"></span>Animate active pane highlight | Fade the highlight to the newly focused pane, move it there, or switch it at once. <span hidden>In Settings &gt; Interface &gt; Active Pane.</span> <span hidden>fade, move, crossfade, glide, slide, animate, animation, transition, border motion, focus animation, highlight animation, border fade, border move, off, instant, no animation, active pane border animation</span> |
| <span id="setting-active-pane-fade-inactive-panes" data-entry="Fade inactive panes"></span>Fade inactive panes | Fade unfocused pane surfaces, content, both, or neither. <span hidden>In Settings &gt; Interface &gt; Active Pane.</span> <span hidden>dim, opacity, unfocused, focus, inactive, off, none, surface, surface only, content, content only, surface &amp; content, surface and content, both, neither, decorations, styling, text, background, borders, shadows, glass, fade inactive pane content</span> |
| <span id="setting-active-pane-fade-panes-for-inactive-windows" data-entry="Fade panes for inactive windows"></span>Fade panes for inactive windows | Fade inactive windows while respecting the pane fade choice. Glass content fades equally in every pane. <span hidden>In Settings &gt; Interface &gt; Active Pane.</span> <span hidden>window inactive, window focus, background window, switch apps, window deactivation, standard window styles, theme defaults, all panes, fade panes in inactive windows, use pane fade choice, fade content for inactive windows, liquid glass content</span> |

### Splits &amp; Focus

Balance a tab's splits and let focus follow the pointer. Opens from Customize panes under Interface › Panes. In Settings > Interface > Splits &amp; Focus. <span hidden>splits, split panes, split balancing, pointer focus, pane layout</span>

| Setting | Description |
| --- | --- |
| <span id="setting-splits-focus-autobalance-splits" data-entry="Autobalance splits"></span>Autobalance splits | Evenly resize a tab's panes when one opens or closes, keeping dividers you drag. <span hidden>In Settings &gt; Interface &gt; Splits &amp;amp; Focus.</span> <span hidden>balance panes, equalize, even, equal size, new pane, close pane, split, resize, divider, keep divider, dragged divider, manual split size</span> |
| <span id="setting-splits-focus-focus-follows-mouse" data-entry="Focus follows mouse"></span>Focus follows mouse | Focus a pane by moving the pointer over it, without clicking. <span hidden>In Settings &gt; Interface &gt; Splits &amp;amp; Focus.</span> <span hidden>hover, pointer, cursor, sloppy focus, mouse focus, active pane, select pane, without clicking</span> |

### Floating Windows

Choose where a tab keeps its minimized floating windows. Opens from Customize panes under Interface › Panes. In Settings > Interface > Floating Windows. <span hidden>floating windows, floating panes, minimized, minimised, hidden windows, taskbar, dock</span>

| Setting | Description |
| --- | --- |
| <span id="setting-floating-windows-minimized-floating-windows" data-entry="Minimized floating windows"></span>Minimized floating windows | Pick the corner of a tab where minimized floating windows line up, or drag them there. <span hidden>In Settings &gt; Interface &gt; Floating Windows.</span> <span hidden>corner, anchor, minimized corner, capsules, chat heads, minimize, minimise, drag, taskbar corner, move minimized windows</span> |

### Gestures

Turn trackpad gestures for panes and the sidebar on or off. In Settings > Interface > Gestures. <span hidden>gestures, trackpad, multi-touch, fingers</span>

| Setting | Description |
| --- | --- |
| <span id="setting-gestures-use-trackpad-gestures" data-entry="Use trackpad gestures"></span>Use trackpad gestures | Spread two fingers over a pane to zoom it and pinch them to restore it, and swipe to show or hide the sidebar. <span hidden>In Settings &gt; Interface &gt; Gestures.</span> <span hidden>use gestures, pinch, pinch to zoom, pinch zoom, magnify, magnification, spread, pinch zoom pane, unzoom, trackpad zoom, trackpad pinch, two finger pinch, swipe, sidebar swipe, disable gestures, turn off gestures, no gestures, trackpad gestures</span> |

### Animation

Choose how panes move, open, and close. In Settings > Interface > Animation. <span hidden>motion, animations, transitions, movement</span>

| Setting | Description |
| --- | --- |
| <span id="setting-animation-animation-style" data-entry="Animation style"></span>Animation style | Choose Snappy, Natural, or Off for pane motion, the active border, and showing or hiding the sidebar. Off while Reduce Motion is on. <span hidden>In Settings &gt; Interface &gt; Animation.</span> <span hidden>snappy, natural, off, spring, bounce, no bounce, overshoot, disable animations, turn off animations, reduce motion, instant, fast, speed, pane animation, split animation, hyprland, sidebar animation</span> |

## General

### App Version

Check for, download, and install Rex.app updates, and choose how they arrive. In Settings > General > App Version. <span hidden>application, release, update, channel, upgrade, software update</span>

| Setting | Description |
| --- | --- |
| <span id="setting-app-version-software-update" data-entry="Software Update"></span>Software Update | See whether Rex is up to date, check for updates, and download or install one. <span hidden>In Settings &gt; General &gt; App Version.</span> <span hidden>check for updates, check now, update now, up to date, latest version, current version, last checked, relaunch to update, restart to update, install update, download update, new version, sparkle</span> |
| <span id="setting-app-version-update-channel" data-entry="Update Channel"></span>Update Channel | Choose Preview or Snapshot updates. Its info button sets whether updates download and install on their own. <span hidden>In Settings &gt; General &gt; App Version.</span> <span hidden>bleeding edge, testing, snapshot, preview, version, upgrade, automatic updates, auto update, auto download, background download, download new updates, install on quit, auto install, auto relaunch, auto restart, install updates automatically, silent update, unattended update, relaunch when idle, low data mode, hotspot, tethering, cellular, metered, expensive network, save data, download paused</span> |

### Client Info

Choose how this Mac appears to Rex Servers and the command line. In Settings > General > Client Info. <span hidden>client, device, identity, `rex client ls`, command line, cli</span>

| Setting | Description |
| --- | --- |
| <span id="setting-client-info-label" data-entry="Label"></span>Label | Name this Mac in client lists and for targeting it from rex commands. <span hidden>In Settings &gt; General &gt; Client Info.</span> <span hidden>device label, client label, name, computer, identify, rename, rename this mac, this device, `-C`, target, targeting, client ls</span> |
| <span id="setting-client-info-remote-control" data-entry="Remote Control"></span>Remote Control | Let Rex and other clients perform actions in this app. <span hidden>In Settings &gt; General &gt; Client Info.</span> <span hidden>remote, control, allow, allow actions, actions, command line, `rex do`, perform, security</span> |

### App Icon

Customize Rex's app icon and Dock and menu bar icon visibility. In Settings > General > App Icon. <span hidden>app icon, application icon, dock icon, artwork</span>

| Setting | Description |
| --- | --- |
| <span id="setting-app-icon-app-icon" data-entry="App Icon"></span>App Icon | Choose Rexie, the Dynamic default icon, or one of the Alternates: Bright, Twilight, Vibe, Shell, or Spookie. <span hidden>In Settings &gt; General &gt; App Icon.</span> <span hidden>app icon, application icon, dock icon, custom icon, alternate icon, bright, bright icon, twilight, twilight icon, light icon, dark icon, artwork, dynamic, dynamic icon, rexie, vibe, vibe icon, glowing prompt, prompt icon, terminal prompt icon, spook, spook icon, spookie, ghost icon, blue icon</span> |
| <span id="setting-app-icon-show-app-icon" data-entry="Show app icon"></span>Show app icon | Show Rex's icon in the Dock and menu bar, the Dock only, or the menu bar only while no window is open. <span hidden>In Settings &gt; General &gt; App Icon.</span> <span hidden>dock and menu bar, dock only, menubar only, menu bar only, dock icon, hide dock icon, show dock icon, dock visibility, application switcher, app switcher, command tab, cmd tab, menubar, menu bar icon, status item, status bar, tray icon, hide menu bar icon, show menu bar icon, hide, show, visibility</span> |

### Launch

Choose whether Rex opens workspace windows at startup. In Settings > General > Launch. <span hidden>launch, startup, start up, opening, background</span>

| Setting | Description |
| --- | --- |
| <span id="setting-launch-show-window-on-launch" data-entry="Show window on launch"></span>Show window on launch | Automatically open workspace windows when Rex launches. <span hidden>In Settings &gt; General &gt; Launch.</span> <span hidden>show window on launch, open window on startup, launch in background, hide window on launch, restore windows, start minimized</span> |

## Themes

### Light Mode

Select the theme palette used in light appearance. In Settings > Themes > Light Mode. <span hidden>colors, colours, appearance, theme, palette, day, bright</span>

| Setting | Description |
| --- | --- |
| <span id="setting-light-mode-light-theme" data-entry="Light theme"></span>Light theme | Choose a custom, default, or built-in palette used in light mode. <span hidden>In Settings &gt; Themes &gt; Light Mode.</span> <span hidden>day, bright, light colors, colour scheme, new light theme, edit light theme, customize light theme, duplicate light theme, fork light theme, delete light theme, theme customizer, ansi palette, ansi standard, ansi bright, terminal colors, preview, live preview, live update, pause preview, freeze, theme editor</span> |
| <span id="setting-light-mode-use-extended-theme-palette" data-entry="Use extended theme palette"></span>Use extended theme palette | Use the theme’s colors 16–255 in light mode, or xterm’s standard palette when off. <span hidden>In Settings &gt; Themes &gt; Light Mode.</span> <span hidden>extended palette, extended colors, extended colours, xterm, xterm palette, standard palette, color cube, colour cube, grayscale ramp, greyscale ramp, generated palette, palette-generate, compatibility, on, off</span> |

### Dark Mode

Select the theme palette used in dark appearance. In Settings > Themes > Dark Mode. <span hidden>colors, colours, appearance, theme, palette, night, dim</span>

| Setting | Description |
| --- | --- |
| <span id="setting-dark-mode-dark-theme" data-entry="Dark theme"></span>Dark theme | Choose a custom, default, or built-in palette used in dark mode. <span hidden>In Settings &gt; Themes &gt; Dark Mode.</span> <span hidden>night, dim, dark colors, colour scheme, new dark theme, edit dark theme, customize dark theme, duplicate dark theme, fork dark theme, delete dark theme, theme customizer, ansi palette, ansi standard, ansi bright, terminal colors, preview, live preview, live update, pause preview, freeze, theme editor</span> |
| <span id="setting-dark-mode-use-extended-theme-palette" data-entry="Use extended theme palette"></span>Use extended theme palette | Use the theme’s colors 16–255 in dark mode, or xterm’s standard palette when off. <span hidden>In Settings &gt; Themes &gt; Dark Mode.</span> <span hidden>extended palette, extended colors, extended colours, xterm, xterm palette, standard palette, color cube, colour cube, grayscale ramp, greyscale ramp, generated palette, palette-generate, compatibility, on, off</span> |

### Import Theme

Add a Ghostty or iTerm palette to your custom themes. In Settings > Themes > Import Theme. <span hidden>import, file, ghostty, iterm, itermcolors, palette, load, colors, colours, appearance, background, light, dark</span>

## Terminal

### Typography

Preview and choose the terminal font, style, size, weight, and line height. In Settings > Terminal > Typography. <span hidden>text, typeface, readability, typography preview, font preview</span>

| Setting | Description |
| --- | --- |
| <span id="setting-typography-terminal-font" data-entry="Terminal font"></span>Terminal font | Browse monospaced or all installed fonts to choose the terminal typeface. <span hidden>In Settings &gt; Terminal &gt; Typography.</span> <span hidden>font, family, typeface, monospace, menlo, font picker, monospaced fonts, all fonts</span> |
| <span id="setting-typography-font-size" data-entry="Font size"></span>Font size | Adjust terminal text size in points. <span hidden>In Settings &gt; Terminal &gt; Typography.</span> <span hidden>text size, larger, smaller, zoom, pt</span> |
| <span id="setting-typography-font-style" data-entry="Font style"></span>Font style | Choose an installed face of the terminal font, such as Light or Book. <span hidden>In Settings &gt; Terminal &gt; Typography.</span> <span hidden>face, variant, italic, oblique, regular, light, medium, semibold, book</span> |
| <span id="setting-typography-font-weight" data-entry="Font weight"></span>Font weight | Adjust the stroke weight of a variable terminal font. <span hidden>In Settings &gt; Terminal &gt; Typography.</span> <span hidden>thickness, thin, light, medium, bold, heavy, variable font, wght</span> |
| <span id="setting-typography-line-height" data-entry="Line height"></span>Line height | Add or remove space between terminal lines. <span hidden>In Settings &gt; Terminal &gt; Typography.</span> <span hidden>cell height, line spacing, leading, adjust-cell-height, ghostty, spacing, taller, compact</span> |

### Advanced Font Settings

Adjust character spacing, ligatures, bold and italic, synthesized styles, smoothing, and fallback fonts. Opens from Advanced font settings under Typography. In Settings > Terminal > Advanced Font Settings. <span hidden>advanced font settings, advanced typography, advanced font options, advanced fonts, font rendering, text rendering, font options</span>

| Setting | Description |
| --- | --- |
| <span id="setting-advanced-font-settings-character-spacing" data-entry="Character spacing"></span>Character spacing | Tighten or widen terminal character spacing in pixels or percent. <span hidden>In Settings &gt; Terminal &gt; Advanced Font Settings.</span> <span hidden>letter spacing, kerning, tracking, cell width, adjust-cell-width, ghostty, maple mono, tighter, wider, pixels, percentage</span> |
| <span id="setting-advanced-font-settings-ligatures" data-entry="Ligatures"></span>Ligatures | Join characters like -&gt; and != into single symbols. <span hidden>In Settings &gt; Terminal &gt; Advanced Font Settings.</span> <span hidden>font features, font-feature, calt, liga, arrows, operators, fira code, jetbrains mono</span> |
| <span id="setting-advanced-font-settings-render-bold-and-italic" data-entry="Render bold and italic"></span>Render bold and italic | Draw bold and italic text, only one of them, or neither. <span hidden>In Settings &gt; Terminal &gt; Advanced Font Settings.</span> <span hidden>font-style-bold, font-style-italic, disable bold, no bold, never bold, disable italic, no italic, never italic, upright, bold face, italic face, font weight, regular, both, bold only, italic only, neither, bold, italic, ghostty</span> |
| <span id="setting-advanced-font-settings-force-bold-and-italic-styles" data-entry="Force bold and italic styles"></span>Force bold and italic styles | Use faux bold and italic rendering for fonts without native styles. Shown only for such fonts. <span hidden>In Settings &gt; Terminal &gt; Advanced Font Settings.</span> <span hidden>font-synthetic-style, synthetic style, synthesize, synthesized, pseudo bold, pseudo italic, fake bold, faux bold, fake italic, faux italic, oblique, slant, slanted, outline, emboldened, missing bold, missing italic, pixel font, bitmap font, monaco, ghostty</span> |
| <span id="setting-advanced-font-settings-font-smoothing" data-entry="Font smoothing"></span>Font smoothing | Smooth the edges of terminal text. <span hidden>In Settings &gt; Terminal &gt; Advanced Font Settings.</span> <span hidden>antialiasing, anti aliasing, text rendering, sharp, font-thicken, thicken</span> |
| <span id="setting-advanced-font-settings-fallback-fonts" data-entry="Fallback fonts"></span>Fallback fonts | Choose fonts, in order, for characters the terminal font doesn't have. <span hidden>In Settings &gt; Terminal &gt; Advanced Font Settings.</span> <span hidden>fallback, font fallback, font-family, missing glyphs, missing characters, symbols, icons, nerd font, cjk, chinese, japanese, korean, emoji, font order, ghostty</span> |

### Colors

Control terminal text colors and readability. In Settings > Terminal > Colors. <span hidden>colour, color, text, readability</span>

| Setting | Description |
| --- | --- |
| <span id="setting-colors-improve-text-contrast" data-entry="Improve text contrast"></span>Improve text contrast | Adjust low-contrast text against its background; included when using the theme palette. <span hidden>In Settings &gt; Terminal &gt; Colors.</span> <span hidden>minimum contrast, automatic, legibility, accessibility, unreadable, faint, pale, yellow, ansi, truecolor, theme, on, off</span> |
| <span id="setting-colors-force-theme-palette-for-text" data-entry="Force theme palette for text"></span>Force theme palette for text | Map RGB and extended text colors to the nearest theme color, then correct contrast. <span hidden>In Settings &gt; Terminal &gt; Colors.</span> <span hidden>force theme colors, force theme colours, remap, match colors, palette, ansi, rgb, truecolor, 256 colors, extended colors, replace, consistent, on, off</span> |
| <span id="setting-colors-use-display-p3-color-space" data-entry="Use Display P3 color space"></span>Use Display P3 color space | Read theme and program colors as Display P3, like Ghostty's window-colorspace. <span hidden>In Settings &gt; Terminal &gt; Colors.</span> <span hidden>p3, display p3, wide gamut, wide colour, color space, colour space, colorspace, window-colorspace, ghostty, srgb, saturated, vivid, on, off</span> |

### Cursor

Preview and adjust the terminal cursor shape, blinking, and shader effect. In Settings > Terminal > Cursor. <span hidden>caret, insertion, indicator, cursor preview</span>

| Setting | Description |
| --- | --- |
| <span id="setting-cursor-blink-speed" data-entry="Blink speed"></span>Blink speed | Choose Off, Slow, Normal, Fast, or Custom to edit the blink interval. <span hidden>In Settings &gt; Terminal &gt; Cursor.</span> <span hidden>flashing, steady, slow, fast, normal, off, custom</span> |
| <span id="setting-cursor-blink-interval" data-entry="Blink interval"></span>Blink interval | Set the time between cursor blinks in milliseconds when Blink speed is Custom. <span hidden>In Settings &gt; Terminal &gt; Cursor.</span> <span hidden>speed, duration, frequency, ms, custom</span> |
| <span id="setting-cursor-cursor-style" data-entry="Cursor style"></span>Cursor style | Choose a block, bar, or underline cursor. <span hidden>In Settings &gt; Terminal &gt; Cursor.</span> <span hidden>shape, beam, caret, block, bar, underline</span> |
| <span id="setting-cursor-force-style" data-entry="Force style"></span>Force style | Ignore application requests to change cursor shape. <span hidden>In Settings &gt; Terminal &gt; Cursor.</span> <span hidden>override, application, ignore, shape</span> |
| <span id="setting-cursor-cursor-shaders" data-entry="Cursor shaders"></span>Cursor shaders | Draw a trail shader, such as Warp, Comet, or Blaze, behind terminal cursors. <span hidden>In Settings &gt; Terminal &gt; Cursor.</span> <span hidden>cursor trail, cursor effect, cursor animation, smear, glow, ghostty shader, custom-shader, shadertoy, on, off</span> |
| <span id="setting-cursor-shader" data-entry="Shader"></span>Shader | With Cursor shaders on, choose the effect they draw, such as Warp, Comet, or Blaze. <span hidden>In Settings &gt; Terminal &gt; Cursor.</span> <span hidden>cursor shader, trail style, effect, warp, sweep, comet, blaze, tapered, rainbow, gradient, frozen</span> |

### Keyboard

Show key sequence hints and choose how modifier keys behave in terminal input. In Settings > Terminal > Keyboard. <span hidden>input, keys, shortcuts, modifier</span>

| Setting | Description |
| --- | --- |
| <span id="setting-keyboard-show-key-sequence-hints" data-entry="Show key sequence hints"></span>Show key sequence hints | Show the keys that can come next after the first key of a sequence, such as a tmux-style prefix. <span hidden>In Settings &gt; Terminal &gt; Keyboard.</span> <span hidden>which-key, which key, prefix, leader, chord, key sequence, popup, overlay, pill</span> |
| <span id="setting-keyboard-option-key" data-entry="Option key"></span>Option key | Choose whether the Option key sends Alt or types special characters. <span hidden>In Settings &gt; Terminal &gt; Keyboard.</span> <span hidden>option, alt, meta, esc, escape, emacs, readline, tmux, compose, accents, special characters, left, right, ∫</span> |

### Scrolling

Choose how trackpad and Magic Mouse scrolling move through terminal history. In Settings > Terminal > Scrolling. <span hidden>scroll, scrollback, history, trackpad, touchpad</span>

| Setting | Description |
| --- | --- |
| <span id="setting-scrolling-smooth-scrolling" data-entry="Smooth scrolling"></span>Smooth scrolling | Move through terminal history by pixels instead of whole lines. <span hidden>In Settings &gt; Terminal &gt; Scrolling.</span> <span hidden>smooth, pixel, precise, sub-line, fluid, momentum, inertia, trackpad, line by line, on, off</span> |

### Resizing

Choose how terminal text follows a pane as it changes size. In Settings > Terminal > Resizing. <span hidden>resize, window size, pane size</span>

| Setting | Description |
| --- | --- |
| <span id="setting-resizing-smooth-terminal-resizing" data-entry="Smooth terminal resizing"></span>Smooth terminal resizing | Reflow terminal text on the frame a pane changes size, without waiting for the server. <span hidden>In Settings &gt; Terminal &gt; Resizing.</span> <span hidden>smooth resize, resize, reflow, jitter, glitch, jump, flicker, live resize, resize preview, zoom, split, sidebar, window drag, drag, re-wrap, rewrap, on, off</span> |

### Selection

Preview selection colors and corners, and customize copying with its animation. In Settings > Terminal > Selection. <span hidden>highlight, selected text, copy, colour, animation, selection preview</span>

| Setting | Description |
| --- | --- |
| <span id="setting-selection-copy-on-selection" data-entry="Copy on selection"></span>Copy on selection | Automatically copy selected terminal text to the clipboard. <span hidden>In Settings &gt; Terminal &gt; Selection.</span> <span hidden>automatic copy, clipboard, selection, mouse, on, off</span> |
| <span id="setting-selection-play-animation-on-copy" data-entry="Play animation on copy"></span>Play animation on copy | Shine across the selection to confirm each copy. <span hidden>In Settings &gt; Terminal &gt; Selection.</span> <span hidden>shine, highlight, sheen, glint, pulse, effect, feedback, motion, animate, on, off</span> |
| <span id="setting-selection-selection-foreground" data-entry="Selection foreground"></span>Selection foreground | Choose the text color inside a selection. <span hidden>In Settings &gt; Terminal &gt; Selection.</span> <span hidden>foreground, text color, colour, contrast</span> |
| <span id="setting-selection-selection-background" data-entry="Selection background"></span>Selection background | Choose the fill color behind selected text. <span hidden>In Settings &gt; Terminal &gt; Selection.</span> <span hidden>background, highlight color, colour, fill</span> |
| <span id="setting-selection-rounded-corners" data-entry="Rounded corners"></span>Rounded corners | Round the corners of terminal text selections. <span hidden>In Settings &gt; Terminal &gt; Selection.</span> <span hidden>radius, rounding, square</span> |

### Links

Choose whether terminal links that launch other apps ask first. In Settings > Terminal > Links. <span hidden>hyperlink, url, osc 8, command click, cmd click, open link, security, safety, custom scheme, url scheme</span>

| Setting | Description |
| --- | --- |
| <span id="setting-links-links-that-open-apps" data-entry="Links that open apps"></span>Links that open apps | Ask before, always, or never open links such as ssh:// that launch another app. <span hidden>In Settings &gt; Terminal &gt; Links.</span> <span hidden>ask first, ask before opening, always open, never open, confirm, confirmation, prompt, allow, block, vscode, ssh, custom scheme, launch app, open app</span> |
| <span id="setting-links-trusted-links" data-entry="Trusted links"></span>Trusted links | Review and remove the links you chose to always open, once Always Open adds one. <span hidden>In Settings &gt; Terminal &gt; Links.</span> <span hidden>always open, allowed links, allowlist, trusted apps, remembered, forget, remove, revoke, permissions</span> |

### Integrated Path Browser

Choose what Insert Path lists when it types a path at the cursor. In Settings > Terminal > Integrated Path Browser. <span hidden>insert path, path browser, file picker, path picker, paths, files, folders, autocomplete, completion</span>

| Setting | Description |
| --- | --- |
| <span id="setting-integrated-path-browser-show-recently-used-paths" data-entry="Show recently used paths"></span>Show recently used paths | List the paths you chose most recently first, shared by every session on a host. <span hidden>In Settings &gt; Terminal &gt; Integrated Path Browser.</span> <span hidden>recents, recent files, history, recently used, mru, frequent, remember, on, off</span> |

### Titles

Choose how terminal tabs and pane headers are named. In Settings > Terminal > Titles. <span hidden>tab, window, pane, name, label</span>

| Setting | Description |
| --- | --- |
| <span id="setting-titles-prefer-generated-titles" data-entry="Prefer generated titles"></span>Prefer generated titles | Show the running program and its directory instead of titles that shells set. <span hidden>In Settings &gt; Terminal &gt; Titles.</span> <span hidden>shell title, generated title, program name, process name, directory, working directory, path, ignore shell titles, always use generated titles, automatic, on, off</span> |

### Shell

Choose the command run when a new local terminal opens. In Settings > Terminal > Shell. <span hidden>startup, session, command line, login</span>

| Setting | Description |
| --- | --- |
| <span id="setting-shell-startup-command" data-entry="Startup command"></span>Startup command | Set the executable and arguments, or leave empty for the default login shell. <span hidden>In Settings &gt; Terminal &gt; Shell.</span> <span hidden>shell, zsh, bash, fish, executable, arguments, launch, startup, working directory</span> |

## Remote Hosts

### Remote hosts

Add, reorder, and manage remote Rex hosts, view connection status, disconnect hosts you aren’t using, answer SSH questions, retry connection failures, and forward ports. In Settings > Remote Hosts > Remote hosts. <span hidden>remote, connections, machines, servers, add host, remove host, retry, disconnect host, connect host, pause host, stop connecting, turn off host, offline host, disable host, keep host, disconnected, host details, remote host status, remote host reconnect, connection warning, connection failure, host address, reorder hosts, host order, sort hosts, arrange hosts, move host up, move host down, drag hosts, ssh, ssh host, ssh passphrase, ssh password, host key, answer ssh question, waiting for an answer, needs your answer, finish setup, trust host, port forwarding, forward port, forwards, tunnel, ssh `-L`, localhost link</span>

### SSH

Choose how ssh reaches ssh:// hosts, including the SSH agent it asks for keys, such as Secretive or 1Password. In Settings > Remote Hosts > SSH. <span hidden>ssh agent, agent, SSH_AUTH_SOCK, auth sock, agent socket, IdentityAgent, identity agent, ssh keys, keys, publickey, permission denied, authentication failed, Secretive, 1Password, Bitwarden, yubikey-agent, YubiKey, gpg-agent, GnuPG, system agent, custom agent</span>

| Setting | Description |
| --- | --- |
| <span id="setting-ssh-ssh-agent" data-entry="SSH agent"></span>SSH agent | Where ssh finds keys for ssh:// hosts: the macOS agent, an agent on this Mac, or a custom socket. <span hidden>In Settings &gt; Remote Hosts &gt; SSH.</span> <span hidden>system, macOS agent, Secretive, 1Password, Bitwarden, yubikey-agent, gpg-agent, custom</span> |
| <span id="setting-ssh-ssh-agent-socket" data-entry="SSH agent socket"></span>SSH agent socket | The path of a custom agent's socket. <span hidden>In Settings &gt; Remote Hosts &gt; SSH.</span> <span hidden>socket path, SSH_AUTH_SOCK, custom agent, agent.sock</span> |
| <span id="setting-ssh-ssh-agent-status" data-entry="SSH agent status"></span>SSH agent status | Whether the chosen agent answers, and how many keys it holds. <span hidden>In Settings &gt; Remote Hosts &gt; SSH.</span> <span hidden>check again, keys, ssh-add, not running, no keys</span> |

## Developer

<div class="api-tags"><span class="api-tag developer"><a href="#setting-developer-developer-mode">Developer Mode</a></span></div>

Reveal settings for development and debugging. In Settings > Developer. <span hidden>advanced, debug, tools</span>

| Setting | Description |
| --- | --- |
| <span id="setting-developer-developer-mode" data-entry="Developer Mode"></span>Developer Mode | Show experiment, local API, and web-client origin settings. <span hidden>In Settings &gt; Developer.</span> <span hidden>enable, advanced, development, debugging</span> |

### Experimental Features

Try features that aren't finished when Developer Mode is enabled. In Settings > Developer > Experimental Features. <span hidden>experiment, beta, unfinished, labs</span>

| Setting | Description |
| --- | --- |
| <span id="setting-experimental-features-terminal-anchoring" data-entry="Terminal anchoring"></span>Terminal anchoring | Pin terminal text to the top or the bottom of each pane. <span hidden>In Settings &gt; Developer &gt; Experimental Features. Needs Developer Mode.</span> <span hidden>anchor, terminal alignment, grid gravity, leftover row</span> |
| <span id="setting-experimental-features-new-quick-switcher" data-entry="New quick switcher"></span>New quick switcher | Open one list of every session, block, and reporting process from Go to Anything. <span hidden>In Settings &gt; Developer &gt; Experimental Features. Needs Developer Mode.</span> <span hidden>go to anything, go to session, view activity, switcher, command palette, cmd p, jump, navigate, panes, blocks, sessions, experiment</span> |

### Local API

Inspect the local server's API endpoint when Developer Mode is enabled. In Settings > Developer > Local API. <span hidden>local server, control api, development, connection</span>

| Setting | Description |
| --- | --- |
| <span id="setting-local-api-local-api-url" data-entry="Local API URL"></span>Local API URL | View and copy the local server endpoint when Developer Mode is enabled. <span hidden>In Settings &gt; Developer &gt; Local API. Needs Developer Mode.</span> <span hidden>address, localhost, port, http, copy local endpoint, unix socket, socket path</span> |

### Web Client Origins

Manage browser origins allowed to open Rex WebSocket streams. In Settings > Developer > Web Client Origins. <span hidden>browser, web, websocket, security, cors</span>

| Setting | Description |
| --- | --- |
| <span id="setting-web-client-origins-allowed-origins" data-entry="Allowed origins"></span>Allowed origins | Review the permitted origins and remove custom entries. <span hidden>In Settings &gt; Developer &gt; Web Client Origins. Needs Developer Mode.</span> <span hidden>allowlist, delete, remove, hosted client, default, permissions</span> |
| <span id="setting-web-client-origins-origin-pattern" data-entry="Origin pattern"></span>Origin pattern | Enter a browser origin or wildcard subdomain to allow after restarting Rex. <span hidden>In Settings &gt; Developer &gt; Web Client Origins. Needs Developer Mode.</span> <span hidden>add origin, allowed origin, wildcard, subdomain, domain, https, web client</span> |

