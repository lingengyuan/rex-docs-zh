> 原文：https://www.superlogical.com/rex/docs/reference/mac-settings
> 原文版本：12e63d82cf69（抓取于 2026-11-18）

# Mac 设置

本页列出 Rex for Mac 中的所有设置项及其所在位置。任何标记为 [Bleeding Edge](mac-settings.md#setting-app-version-update-channel) 的内容均处于该更新通道中，尚未进入 Preview。

<div class="reference-page settings" hidden></div>

## 集成

### 编码智能体（Coding Agents）
向 Claude Code、Codex、OpenCode 和 Pi 讲授如何使用 Rex。位于“设置”>“集成”>“Coding Agents”。 <span hidden>agents, ai, claude, claude code, codex, opencode, pi, skill, hooks, `rex skill setup`, llm, assistant, integrations</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-coding-agents-integrate-with-available-agents" data-entry="Integrate with available agents"></span>Integrate with available agents（与可用智能体集成） | 为受支持的智能体安装 Rex skill 与会话 hook。<span hidden>In Settings &gt; Integrations &gt; Coding Agents.</span> <span hidden>install skill, remove skill, set up agents, uninstall, enable agents, disable agents, update skill</span> |

### 智能体行为（Agent Behavior）
选择 Rex 向在其终端中运行的编码智能体传递哪些信息。位于“设置”>“集成”>“Agent Behavior”。 <span hidden>agent instructions, agent rules, session hook</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-agent-behavior-let-agents-name-sessions" data-entry="Let agents name sessions"></span>Let agents name sessions（允许智能体命名会话） | 允许智能体根据其正在执行的任务标记会话名称。在开启“与可用智能体集成”时显示。<span hidden>In Settings &gt; Integrations &gt; Agent Behavior.</span> <span hidden>rename session, session label, session name, auto name, title, label sessions</span> |

## 通知

### 应用内通知（In-App Notifications）
选择浮动通知在窗口中的显示位置。位于“设置”>“通知”>“In-App Notifications”。 <span hidden>notifications, notification settings, alerts, banners, notification center, in app notifications, customize notifications</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-in-app-notifications-notification-position" data-entry="Notification position"></span>Notification position（通知位置） | 点击窗口图示中的对应位置，将通知放置在顶部或底部，并靠左、居中或靠右对齐。<span hidden>In Settings &gt; Notifications &gt; In-App Notifications.</span> <span hidden>notification position, notification placement, banner location, anchor, top left, top center, top right, bottom left, bottom center, bottom right</span> |

### 程序活动（Program Activity）
独立配置程序活动的标签页指示符、系统通知、Dock 标记和提示音。位于“设置”>“通知”>“Program Activity”。 <span hidden>program activity, tab activity, activity indicators</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-program-activity-show-activity-in-tabs" data-entry="Show activity in tabs"></span>Show activity in tabs（在标签页中显示活动） | 当标签页中的程序报告其状态时，在标签页上显示运行指示点、进度饼图以及需要关注的点和消息。<span hidden>In Settings &gt; Notifications &gt; Program Activity.</span> <span hidden>program status, process status, osc 7501, agent, claude, progress, progress pie, blocked, waiting, question, permission, error, failed, status dot, status badges, notification dot, badge, working, tab status, indicator, needs attention</span> |
| <span id="setting-program-activity-include-idle-processes-in-activity" data-entry="Include idle processes in activity"></span>Include idle processes in activity（在活动中包含空闲进程） | 即使查看后，仍在活动过滤器和弹出窗口中保留报告为空闲状态的标签页。<span hidden>In Settings &gt; Notifications &gt; Program Activity.</span> <span hidden>idle, idle processes, idle agents, ready, activity filter, activity popup, keep idle, show idle, include idle, always show idle processes in activity, eye</span> |
| <span id="setting-program-activity-show-system-notifications" data-entry="Show system notifications"></span>Show system notifications（显示系统通知） | 当 Rex 处于后台且程序报告状态时发送 macOS 系统通知，该设置独立于标签页指示符。点击通知可打开该程序的标签页。<span hidden>In Settings &gt; Notifications &gt; Program Activity.</span> <span hidden>program notifications, agent notifications, background notifications, claude notification, notify when done, notify when blocked, notifications without tab indicators</span> |
| <span id="setting-program-activity-badge-dock-icon" data-entry="Badge Dock icon"></span>Badge Dock icon（在 Dock 图标上显示标记） | 在 Rex 的 Dock 图标上显示有多少个尚未查看且包含阻塞、失败或完成程序的标签页。<span hidden>In Settings &gt; Notifications &gt; Program Activity.</span> <span hidden>dock badge, badge count, app icon badge, unread count, red badge, badge application icon, dock icon</span> |
| <span id="setting-program-activity-play-sounds" data-entry="Play sounds"></span>Play sounds（播放声音） | 当标签页中的程序被阻塞、报告错误或完成时播放提示音。<span hidden>In Settings &gt; Notifications &gt; Program Activity.</span> <span hidden>sound, audio, chime, alert sound, beep, bell, audible, monoh, sound effects, program finished, done sound, mute, silence</span> |
| <span id="setting-program-activity-sound-volume" data-entry="Sound volume"></span>Sound volume（声音音量） | 设置阻塞、错误和完成提示音的播放音量，范围可低于或高于默认音量。<span hidden>In Settings &gt; Notifications &gt; Program Activity.</span> <span hidden>volume, loudness, louder, quieter, too quiet, too loud, sound level, alert volume, notification volume, boost, gain</span> |
| <span id="setting-program-activity-working" data-entry="Working"></span>Working（正在运行） | 启用或禁用运行中程序的所有活动提醒，或单独配置其标签页指示符、通知、Dock 标记和提示音。<span hidden>In Settings &gt; Notifications &gt; Program Activity.</span> <span hidden>working status, busy, progress, spinner, running, disable all working, enable working status</span> |
| <span id="setting-program-activity-blocked" data-entry="Blocked"></span>Blocked（等待输入/已阻塞） | 启用或禁用等待用户响应程序的所有活动提醒，或单独配置其标签页指示符、通知、Dock 标记和提示音。<span hidden>In Settings &gt; Notifications &gt; Program Activity.</span> <span hidden>blocked status, waiting, question, permission, approval, sign in, attention sound, blocked notifications, disable all blocked, enable blocked status</span> |
| <span id="setting-program-activity-error" data-entry="Error"></span>Error（错误） | 启用或禁用报错程序的所有活动提醒，或单独配置其标签页指示符、通知、Dock 标记和提示音。<span hidden>In Settings &gt; Notifications &gt; Program Activity.</span> <span hidden>error status, failed, failure, error sound, disable all errors, enable error status</span> |
| <span id="setting-program-activity-done" data-entry="Done"></span>Done（已完成） | 启用或禁用已完成程序的所有活动提醒，或单独配置其标签页指示符、通知、Dock 标记和提示音。<span hidden>In Settings &gt; Notifications &gt; Program Activity.</span> <span hidden>done status, finished, complete, completed, success sound, finish sound, disable all done, enable done status</span> |

### 系统通知（System Notifications）
选择终端程序是否可以发送原生 macOS 通知，并查看 Rex 针对 Tailscale 发送的通知。位于“设置”>“通知”>“System Notifications”。 <span hidden>native notifications, macOS notifications, mac notifications, tailscale alerts, terminal notifications</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-system-notifications-terminal-notifications" data-entry="Terminal notifications"></span>Terminal notifications（终端通知） | 允许程序使用 OSC 9 或 OSC 777 发送原生系统通知。<span hidden>In Settings &gt; Notifications &gt; System Notifications.</span> <span hidden>osc 9, osc 777, osc9, osc777, desktop notification, notify-send, escape sequence, program notifications, printf notify</span> |
| <span id="setting-system-notifications-tailscale-sign-in" data-entry="Tailscale sign-in"></span>Tailscale sign-in（Tailscale 登录通知） | 当 Rex 需要你登录 Tailscale 时发送原生系统通知。<span hidden>In Settings &gt; Notifications &gt; System Notifications.</span> <span hidden>tailscale login notification, sign in, authentication, account</span> |
| <span id="setting-system-notifications-tailscale-device-approval" data-entry="Tailscale device approval"></span>Tailscale device approval（Tailscale 设备批准通知） | 当 tailnet 管理员必须批准这台 Mac 时发送原生系统通知。<span hidden>In Settings &gt; Notifications &gt; System Notifications.</span> <span hidden>device approval notification, approve mac, tailnet administrator, authorization</span> |
| <span id="setting-system-notifications-tailscale-failures" data-entry="Tailscale failures"></span>Tailscale failures（Tailscale 故障通知） | 当 Tailscale 停止运行或报告错误时发送原生系统通知。<span hidden>In Settings &gt; Notifications &gt; System Notifications.</span> <span hidden>tailscale failure notification, tailscale stopped, connection error, offline</span> |

## 服务端

### Rex 服务端（Rex Server）
管理本地服务端、兼容性与诊断。位于“设置”>“服务端”>“Rex Server”。 <span hidden>start, stop, restart, status, version, api, diagnostics</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-rex-server-server-status" data-entry="Server status"></span>Server status（服务端状态） | 查看本地服务端是否正在运行以及运行了多长时间，其信息浮层中提供了版本与 API 详情。<span hidden>In Settings &gt; Server &gt; Rex Server.</span> <span hidden>health, running, stopped, preparing server, failed, error, source checkout, server details, server version, api revision, uptime, running time, how long, started, duration</span> |
| <span id="setting-rex-server-compatibility" data-entry="Compatibility"></span>Compatibility（兼容性） | 当检测到更新、兼容性问题或待应用的设置变更时，查看差异并在适当时机更新或重启服务端。<span hidden>In Settings &gt; Server &gt; Rex Server.</span> <span hidden>incompatible server, restart recommended, update rex app, restart server, upgrade server, newer server, available version, restart required, new features, apply settings, use bundled server, older app, backward compatible, a newer server is available, updating is optional, optional update, new API features are available, newer API features, unavailable features, server settings have changed, cannot connect to this server, this server requires a newer rex app, server and app are incompatible, reconnect, server compatibility, pending changes, update server, restart using included server, restart from source</span> |

### 远程地址（Remote Address）
查看服务进度、复制地址或配对其他设备。位于“设置”>“服务端”>“Remote Address”。 <span hidden>tailnet, https, endpoint, connectivity</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-remote-address-remote-address" data-entry="Remote Address"></span>Remote Address（远程地址） | 查看服务进度与证书就绪状态，重试连接、复制地址，或使用其二维码配对设备。<span hidden>In Settings &gt; Server &gt; Remote Address.</span> <span hidden>copy remote address, tailscale connection progress, https, dns, hostname, endpoint, copy, qr, scan, pair, device, iphone, ipad, certificate, waiting for certificate, tls, ssl, secure, starting, stopping, connection progress, retry, connected, disconnected, approval, error, dns recovery</span> |

### Tailscale

将 Rex 连接至你的 tailnet 并控制访问权限。位于“设置”>“服务端”>“Tailscale”。 <span hidden>network, vpn, remote, secure, sharing</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-tailscale-serve-over-tailscale" data-entry="Serve over Tailscale"></span>Serve over Tailscale（通过 Tailscale 提供服务） | 启用或禁用通过 tailnet 访问 Rex。<span hidden>In Settings &gt; Server &gt; Tailscale.</span> <span hidden>connect, network, vpn, share, enable, disable</span> |
| <span id="setting-tailscale-preferred-hostname" data-entry="Preferred Hostname"></span>Preferred Hostname（偏好主机名） | 选择这台 Mac 在提供服务时的 Tailscale 主机名。分配到的实际地址可能会有所不同。<span hidden>In Settings &gt; Server &gt; Tailscale.</span> <span hidden>hostname, device name, dns, rename, machine, address, assigned address, host id, durable host id, identity</span> |
| <span id="setting-tailscale-limit-access-to-your-tailscale-account" data-entry="Limit access to your Tailscale account"></span>Limit access to your Tailscale account（限制仅你的 Tailscale 账户可访问） | 限制仅调用方为你自己的账户，或允许所有 tailnet 成员访问。<span hidden>In Settings &gt; Server &gt; Tailscale.</span> <span hidden>security, authentication, identity, permissions, owner, members, acl</span> |
| <span id="setting-tailscale-tags" data-entry="Tags"></span>Tags（标签） | 查看此设备的 Tailscale 标签。退出登录并重新登录以更改它们。<span hidden>In Settings &gt; Server &gt; Tailscale.</span> <span hidden>tag, tagged, acl tags, advertise tags, tailnet policy, machine identity, owner, access</span> |
| <span id="setting-tailscale-control-server" data-entry="Control Server"></span>Control Server（控制服务器） | 查看此设备登录所使用的控制服务器。退出登录并重新登录以更改它。<span hidden>In Settings &gt; Server &gt; Tailscale.</span> <span hidden>control url, control plane, coordination server, login server, self-hosted, custom server</span> |
| <span id="setting-tailscale-sign-in-to-tailscale" data-entry="Sign in to Tailscale"></span>Sign in to Tailscale（登录至 Tailscale） | 查看账户信息与退出登录进度，配置主机名并登录，重新打开或取消注册，或退出登录。<span hidden>In Settings &gt; Server &gt; Tailscale.</span> <span hidden>login, tailscale login, sign in, sign in to tailscale, log in, sign out, account, status, signed in to tailscale, enrolled account, signing in to tailscale, browser sign in, open browser, reopen browser, preparing to sign in, this may take a moment, ready to connect, awaiting connection, finish the process in your browser, taking longer than usual, slow sign in, cancel sign in, cancel login, signing out of tailscale, remove saved login, sign out progress</span> |

### 客户端信息（Client Info）
选择此 Mac 在 Rex 服务端和命令行中的显示方式。位于“设置”>“服务端”>“Client Info”。 <span hidden>client, device, identity, `rex client ls`, command line, cli</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-client-info-label" data-entry="Label"></span>Label（标签） | 在客户端列表中为此 Mac 命名，以便在 rex 命令中作为目标指定。<span hidden>In Settings &gt; Server &gt; Client Info.</span> <span hidden>device label, client label, name, computer, identify, rename, rename this mac, this device, `-C`, target, targeting, client ls</span> |
| <span id="setting-client-info-remote-control" data-entry="Remote Control"></span>Remote Control（远程控制） | 允许 Rex 和其他客户端在此应用中执行操作。<span hidden>In Settings &gt; Server &gt; Client Info.</span> <span hidden>remote, control, allow, allow actions, actions, command line, `rex do`, perform, security</span> |

## 界面

### 外观（Appearance）
选择配色方案、界面材质与主题色调。位于“设置”>“界面”>“Appearance”。 <span hidden>look, visual, display, theme</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-appearance-color-scheme" data-entry="Color scheme"></span>Color scheme（配色方案） | 选择自动、浅色或深色材质的实时预览。自动模式会跟随系统外观。<span hidden>In Settings &gt; Interface &gt; Appearance.</span> <span hidden>colour, light, dark, auto, automatic, system, night mode, cards</span> |
| <span id="setting-appearance-interface-style" data-entry="Interface style"></span>Interface style（界面样式） | 预览带有当前主题色调的玻璃或经典材质，并选择表面样式。<span hidden>In Settings &gt; Interface &gt; Appearance.</span> <span hidden>glass, classic, liquid glass, material, native, system, modern, opaque, translucent, cards</span> |
| <span id="setting-appearance-tint-with-theme" data-entry="Tint with theme"></span>Tint with theme（随主题着色） | 将所选主题的颜色应用到界面各表面。<span hidden>In Settings &gt; Interface &gt; Appearance.</span> <span hidden>tint, theme colors, theme colours, palette, themed, blended, blend theme, use theme</span> |
| <span id="setting-appearance-use-glass-for-panes" data-entry="Use glass for panes"></span>Use glass for panes（窗格使用玻璃材质） | 在玻璃界面样式下可用：在窗口和标签页材质的基础上，为窗格添加玻璃效果。<span hidden>In Settings &gt; Interface &gt; Appearance.</span> <span hidden>pane glass, no glass, remove glass, liquid glass, pane material, transparency</span> |

### 工具栏（Toolbar）
选择工具栏布局，以及工具栏是始终显示还是悬停时显示。位于“设置”>“界面”>“Toolbar”。 <span hidden>workspace, chrome, layout, navigation, tab bar, title bar</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-toolbar-toolbar-layout" data-entry="Toolbar layout"></span>Toolbar layout（工具栏布局） | 将工具栏及其标签页放置在窗口的上方、左侧或右侧。<span hidden>In Settings &gt; Interface &gt; Toolbar.</span> <span hidden>tab style, tab placement, tab layout, horizontal tabs, vertical tabs, vertical, horizontal, sidebar, navigation, orientation, sidebar position, above, left side, right side, left sidebar, right sidebar, edge, location</span> |
| <span id="setting-toolbar-toolbar-behavior" data-entry="Toolbar behavior"></span>Toolbar behavior（工具栏行为） | 始终显示工具栏、悬停时显示（隐藏标签栏或边栏标题行，直到光标移至窗口顶部），或保持隐藏直到执行“显示工具栏”。<span hidden>In Settings &gt; Interface &gt; Toolbar.</span> <span hidden>always show, on hover, show toolbar on hover, hidden, never, never show toolbar, reveal toolbar, toolbar visibility, auto-hide toolbar, autohide, hide toolbar, hide tab bar, floating toolbar, reveal, tab bar, title bar, title row, traffic lights, distraction free, minimal, full height, chrome, hot corner, hot corners</span> |

### 标签页行为（Tab behavior）
选择窗格上方的标签页是否填满标签栏。从“工具栏”下的“自定标签页”打开。位于“设置”>“界面”>“Tab behavior”。 <span hidden>tabs, tab bar, tab sizing, customize tabs</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-tab-behavior-tabs-fill-available-space" data-entry="Tabs fill available space"></span>Tabs fill available space（标签页填满可用空间） | 在水平标签页下可用：均等拉伸标签页以填满标签栏，仅在有两个或更多标签页时显示背景。<span hidden>In Settings &gt; Interface &gt; Tab behavior.</span> <span hidden>fill available space, tab width, stretch, expand, full width, equal width, maximum, capped</span> |

### 标签页图标（Tab icons）
选择标签页显示的窗格图标数量，以及标签页和 shell 图标的着色方式。从“工具栏”下的“自定标签页”打开。位于“设置”>“界面”>“Tab icons”。 <span hidden>workspace, icons, symbols, pane cards, icon stack, tab icons, tabs, customize tabs</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-tab-icons-use-color-for-tab-icons" data-entry="Use color for tab icons"></span>Use color for tab icons（为标签页图标使用颜色） | 选择始终、仅对活动窗格、仅对活动标签页显示彩色图标，或从不显示。<span hidden>In Settings &gt; Interface &gt; Tab icons.</span> <span hidden>colour, monochrome, grayscale, greyscale, saturation, always, never, active panes, active tabs, focused pane, selected tab</span> |
| <span id="setting-tab-icons-shell-icon-theme" data-entry="Shell icon theme"></span>Shell icon theme（Shell 图标主题） | 选择默认图形、使用主题的前景与背景色，或使用主题强调色。<span hidden>In Settings &gt; Interface &gt; Tab icons.</span> <span hidden>shell colors, shell colours, terminal icon, shell palette, default, use theme, use theme accent, accent, background, foreground, glyph</span> |
| <span id="setting-tab-icons-show-tab-icons" data-entry="Show tab icons"></span>Show tab icons（显示标签页图标） | 在垂直标签页中显示 0 到 3 个窗格图标，在水平标签页中最多显示 5 个。<span hidden>In Settings &gt; Interface &gt; Tab icons.</span> <span hidden>icon count, icons per tab, number of icons, stack size, stack limit, icon count slider, slider, maximum, none, hide icons, no icons, zero icons, one icon, two icons, three icons, four icons, five icons, 0, 1, 2, 3, 4, 5, pane icons</span> |

### 窗格（Panes）
调整窗格间距与标题栏。位于“设置”>“界面”>“Panes”。 <span hidden>workspace, chrome, layout, density, spacing, split</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-panes-pane-style" data-entry="Pane style"></span>Pane style（窗格样式） | 选择舒适（Comfortable）或紧凑（Compact）的窗格表面与间距。<span hidden>In Settings &gt; Interface &gt; Panes.</span> <span hidden>compact, comfortable, pane density, padding, gaps, spacing</span> |
| <span id="setting-panes-pane-header-behavior" data-entry="Pane header behavior"></span>Pane header behavior（窗格标题栏行为） | 控制每个窗格上方的标题与控件的显示：始终显示、悬停时显示或隐藏。<span hidden>In Settings &gt; Interface &gt; Panes.</span> <span hidden>pane headers, show pane headers, titles, toolbar, chrome, hide headers, always, always show, on hover, show on hover, hidden, never, hover, floating header, auto-hide header, pane header visibility</span> |

### 窗口（Window）
适用于边栏工具栏布局：选择边栏是否调整窗口大小、通过何种轻扫手势显示或隐藏边栏，以及边栏文字的大小。位于“设置”>“界面”>“Window”。 <span hidden>window sizing, window width, sidebar, layout, swipe, trackpad, text size</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-window-sidebar-text-size" data-entry="Sidebar text size"></span>Sidebar text size（边栏文字大小） | 在垂直标签页下可用：设置边栏中会话和标签页标题的大小，或跟随系统设置中的边栏图标大小。<span hidden>In Settings &gt; Interface &gt; Window.</span> <span hidden>sidebar text, text size, tab title size, session title size, larger text, bigger text, sidebar icon size, sidebar row size, row height, follow system size</span> |
| <span id="setting-window-preserve-width-when-resizing-sidebar" data-entry="Preserve width when resizing sidebar"></span>Preserve width when resizing sidebar（调整边栏大小时保持窗口宽度） | 在垂直标签页下可用：在显示或隐藏边栏时调整窗格大小，保持窗口总宽度不变。<span hidden>In Settings &gt; Interface &gt; Window.</span> <span hidden>keep window width, preserve window width, fixed window width, resizing sidebar, window size, resize window, shrink window, grow window, keep window size, show sidebar, hide sidebar, toggle sidebar, collapse sidebar, fold sidebar, pane width, maximized, full screen</span> |
| <span id="setting-window-use-a-gesture-to-toggle-the-sidebar" data-entry="Use a gesture to toggle the sidebar"></span>Use a gesture to toggle the sidebar（使用手势切换边栏） | 在垂直标签页下可用：选择使用单指/双指轻扫或 Option+轻扫显示/隐藏边栏，亦可关闭手势。按住 ⌥ 键可改为水平滚动内容。<span hidden>In Settings &gt; Interface &gt; Window.</span> <span hidden>show or hide sidebar, option-swipe, option swipe, ⌥, off, disable swipe, turn off swipe, no gesture, disable gesture, magic mouse, mouse, one finger, option scroll, alt scroll, option key, alt key, hold option, modifier, swipe, two finger swipe, two fingers, trackpad, gesture, trackpad gesture, sidebar swipe, swipe sidebar, fold sidebar, horizontal scroll, scroll sideways, sideways, side scroll, scroll left, scroll right, tui, diff, long lines</span> |

### 内边距（Padding）
设置窗格边缘与终端文本之间的间距，以及是否填充程序颜色。从“界面”›“窗格”下的“自定窗格”打开。位于“设置”>“界面”>“Padding”。 <span hidden>pane padding, terminal padding, inset, margin, margins, gutter, spacing around text, edges, window padding, pane background, background</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-padding-padding-x" data-entry="Padding X"></span>Padding X（水平内边距） | 设置终端文本左右两侧的留白间距。<span hidden>In Settings &gt; Interface &gt; Padding.</span> <span hidden>horizontal padding, x padding, left padding, right padding, side padding, horizontal inset, horizontal margin</span> |
| <span id="setting-padding-padding-y" data-entry="Padding Y"></span>Padding Y（垂直内边距） | 设置终端文本下方的留白间距，并在隐藏窗格标题栏时同时应用于上方。<span hidden>In Settings &gt; Interface &gt; Padding.</span> <span hidden>vertical padding, y padding, bottom padding, top padding, vertical inset, vertical margin</span> |
| <span id="setting-padding-fill-with-program-colors" data-entry="Fill with program colors"></span>Fill with program colors（填充程序颜色） | 允许全屏程序为内边距着色：关闭、自动或始终。<span hidden>In Settings &gt; Interface &gt; Padding.</span> <span hidden>padding color, colour, off, automatic, always, extend, extend always, background, edge cells, window-padding-color, program background, editor, full screen, tui</span> |
| <span id="setting-padding-include-pane-header" data-entry="Include pane header"></span>Include pane header（包含窗格标题栏） | 在填充内边距的同时，为窗格标题栏着色以匹配程序。<span hidden>In Settings &gt; Interface &gt; Padding.</span> <span hidden>match program backgrounds, tint, pane color, header color, pane background, terminal background, program background, editor, full screen, tui, neovim, vim, blend, match terminal</span> |

### 活动窗格（Active Pane）
高亮活动窗格的边缘并淡化非活动窗格。从“界面”›“窗格”下的“自定窗格”打开。位于“设置”>“界面”>“Active Pane”。 <span hidden>customize panes, customize pane behavior, pane behavior, active pane, active panes, inactive panes, focused pane, unfocused panes, pane focus, focus appearance, dim inactive</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-active-pane-highlight-active-pane-edges" data-entry="Highlight active pane edges"></span>Highlight active pane edges（高亮活动窗格边缘） | 高亮获得焦点的窗格边缘，跟随焦点移动。<span hidden>In Settings &gt; Interface &gt; Active Pane.</span> <span hidden>border, outline, focus ring, active border, focused pane, highlight, highlight active pane, edge highlight, indicator, focus indicator, show border on active pane</span> |
| <span id="setting-active-pane-highlight-color" data-entry="Highlight color"></span>Highlight color（高亮颜色） | 使用强调色、终端调色板颜色或终端文本颜色绘制高亮。<span hidden>In Settings &gt; Interface &gt; Active Pane.</span> <span hidden>accent, accent color, theme color, terminal text, terminal foreground, foreground color, text color, highlight color, border color, focus ring color, active pane border color, swatch, color swatches, palette, red, blue, green, yellow, cyan, magenta</span> |
| <span id="setting-active-pane-highlight-opacity" data-entry="Highlight opacity"></span>Highlight opacity（高亮不透明度） | 设置高亮绘制的强度与不透明度。<span hidden>In Settings &gt; Interface &gt; Active Pane.</span> <span hidden>opacity, transparency, alpha, translucent, faint, subtle, strength, border opacity, border strength, focus ring opacity, highlight strength, active pane border opacity</span> |
| <span id="setting-active-pane-animate-active-pane-highlight" data-entry="Animate active pane highlight"></span>Animate active pane highlight（活动窗格高亮动画） | 淡入至新聚焦的窗格、平移至新窗格，或立即切换。<span hidden>In Settings &gt; Interface &gt; Active Pane.</span> <span hidden>fade, move, crossfade, glide, slide, animate, animation, transition, border motion, focus animation, highlight animation, border fade, border move, off, instant, no animation, active pane border animation</span> |
| <span id="setting-active-pane-fade-inactive-panes" data-entry="Fade inactive panes"></span>Fade inactive panes（淡化非活动窗格） | 淡化未聚焦窗格的表面、内容、两者兼有或两者皆否。<span hidden>In Settings &gt; Interface &gt; Active Pane.</span> <span hidden>dim, opacity, unfocused, focus, inactive, off, none, surface, surface only, content, content only, surface &amp; content, surface and content, both, neither, decorations, styling, text, background, borders, shadows, glass, fade inactive pane content</span> |
| <span id="setting-active-pane-fade-panes-for-inactive-windows" data-entry="Fade panes for inactive windows"></span>Fade panes for inactive windows（淡化非活动窗口的窗格） | 在遵循窗格淡化设置的同时淡化非活动窗口。玻璃材质内容在每个窗格中均等淡化。<span hidden>In Settings &gt; Interface &gt; Active Pane.</span> <span hidden>window inactive, window focus, background window, switch apps, window deactivation, standard window styles, theme defaults, all panes, fade panes in inactive windows, use pane fade choice, fade content for inactive windows, liquid glass content</span> |

### 分栏与焦点（Splits &amp; Focus）
均分标签页的分栏，并支持焦点跟随光标。从“界面”›“窗格”下的“自定窗格”打开。位于“设置”>“界面”>“Splits &amp; Focus”。 <span hidden>splits, split panes, split balancing, pointer focus, pane layout</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-splits-focus-autobalance-splits" data-entry="Autobalance splits"></span>Autobalance splits（自动均分分栏） | 在窗格打开或关闭时均等调整标签页各窗格大小，同时保留手动拖拽的分隔线位置。<span hidden>In Settings &gt; Interface &gt; Splits &amp;amp; Focus.</span> <span hidden>balance panes, equalize, even, equal size, new pane, close pane, split, resize, divider, keep divider, dragged divider, manual split size</span> |
| <span id="setting-splits-focus-focus-follows-mouse" data-entry="Focus follows mouse"></span>Focus follows mouse（焦点跟随鼠标） | 光标移至窗格上方即可聚焦该窗格，无需点击。<span hidden>In Settings &gt; Interface &gt; Splits &amp;amp; Focus.</span> <span hidden>hover, pointer, cursor, sloppy focus, mouse focus, active pane, select pane, without clicking</span> |

### 悬浮窗口（Floating Windows）
选择标签页存放最小化悬浮窗口的位置。从“界面”›“窗格”下的“自定窗格”打开。位于“设置”>“界面”>“Floating Windows”。 <span hidden>floating windows, floating panes, minimized, minimised, hidden windows, taskbar, dock</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-floating-windows-minimized-floating-windows" data-entry="Minimized floating windows"></span>Minimized floating windows（最小化悬浮窗口） | 选择标签页中最小化悬浮窗口排列的角落位置，或直接将其拖拽至该处。<span hidden>In Settings &gt; Interface &gt; Floating Windows.</span> <span hidden>corner, anchor, minimized corner, capsules, chat heads, minimize, minimise, drag, taskbar corner, move minimized windows</span> |

### 手势（Gestures）
开启或关闭用于窗格和边栏的触控板手势。位于“设置”>“界面”>“Gestures”。 <span hidden>gestures, trackpad, multi-touch, fingers</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-gestures-use-trackpad-gestures" data-entry="Use trackpad gestures"></span>Use trackpad gestures（使用触控板手势） | 在窗格上双指张开可放大/最大化，捏合可复原；轻扫可显示或隐藏边栏。<span hidden>In Settings &gt; Interface &gt; Gestures.</span> <span hidden>use gestures, pinch, pinch to zoom, pinch zoom, magnify, magnification, spread, pinch zoom pane, unzoom, trackpad zoom, trackpad pinch, two finger pinch, swipe, sidebar swipe, disable gestures, turn off gestures, no gestures, trackpad gestures</span> |

### 动画（Animation）
选择窗格移动、打开和关闭的方式。位于“设置”>“界面”>“Animation”。 <span hidden>motion, animations, transitions, movement</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-animation-animation-style" data-entry="Animation style"></span>Animation style（动画样式） | 为窗格移动、活动边框以及显示/隐藏边栏选择干脆（Snappy）、自然（Natural）或关闭（Off）。开启“减弱动态效果”时为关闭。<span hidden>In Settings &gt; Interface &gt; Animation.</span> <span hidden>snappy, natural, off, spring, bounce, no bounce, overshoot, disable animations, turn off animations, reduce motion, instant, fast, speed, pane animation, split animation, hyprland, sidebar animation</span> |

### 应用图标（App Icon）
自定 Rex 的应用图标，以及在 Dock 和菜单栏中的图标可见性。位于“设置”>“界面”>“App Icon”。 <span hidden>app icon, application icon, dock icon, artwork</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-app-icon-app-icon" data-entry="App Icon"></span>App Icon（应用图标） | 为应用图标选择默认（动态）、明亮（Bright）或微光（Twilight）图形。<span hidden>In Settings &gt; Interface &gt; App Icon.</span> <span hidden>app icon, application icon, dock icon, custom icon, alternate icon, bright, bright icon, twilight, twilight icon, light icon, dark icon, artwork, dynamic, dynamic icon</span> |
| <span id="setting-app-icon-show-app-icon" data-entry="Show app icon"></span>Show app icon（显示应用图标） | 在 Dock 和菜单栏、仅 Dock，或未打开窗口时仅菜单栏中显示 Rex 图标。<span hidden>In Settings &gt; Interface &gt; App Icon.</span> <span hidden>dock and menu bar, dock only, menubar only, menu bar only, dock icon, hide dock icon, show dock icon, dock visibility, application switcher, app switcher, command tab, cmd tab, menubar, menu bar icon, status item, status bar, tray icon, hide menu bar icon, show menu bar icon, hide, show, visibility</span> |

### 启动（Launch）
选择 Rex 启动时是否打开工作区窗口。位于“设置”>“界面”>“Launch”。 <span hidden>launch, startup, start up, opening, background</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-launch-show-window-on-launch" data-entry="Show window on launch"></span>Show window on launch（启动时显示窗口） | 在 Rex 启动时自动打开工作区窗口。<span hidden>In Settings &gt; Interface &gt; Launch.</span> <span hidden>show window on launch, open window on startup, launch in background, hide window on launch, restore windows, start minimized</span> |

## 主题

### 浅色模式（Light Mode）
选择浅色外观下使用的主题调色板。位于“设置”>“主题”>“Light Mode”。 <span hidden>colors, colours, appearance, theme, palette, day, bright</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-light-mode-light-theme" data-entry="Light theme"></span>Light theme（浅色主题） | 选择在浅色模式下使用的自定、默认或内置调色板。<span hidden>In Settings &gt; Themes &gt; Light Mode.</span> <span hidden>day, bright, light colors, colour scheme, new light theme, edit light theme, customize light theme, duplicate light theme, fork light theme, delete light theme, theme customizer, ansi palette, ansi standard, ansi bright, terminal colors, preview, live preview, live update, pause preview, freeze, theme editor</span> |
| <span id="setting-light-mode-use-extended-theme-palette" data-entry="Use extended theme palette"></span>Use extended theme palette（使用扩展主题调色板） | 在浅色模式下使用主题的 16–255 号颜色；关闭时使用 xterm 标准调色板。<span hidden>In Settings &gt; Themes &gt; Light Mode.</span> <span hidden>extended palette, extended colors, extended colours, xterm, xterm palette, standard palette, color cube, colour cube, grayscale ramp, greyscale ramp, generated palette, palette-generate, compatibility, on, off</span> |

### 深色模式（Dark Mode）
选择深色外观下使用的主题调色板。位于“设置”>“主题”>“Dark Mode”。 <span hidden>colors, colours, appearance, theme, palette, night, dim</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-dark-mode-dark-theme" data-entry="Dark theme"></span>Dark theme（深色主题） | 选择在深色模式下使用的自定、默认或内置调色板。<span hidden>In Settings &gt; Themes &gt; Dark Mode.</span> <span hidden>night, dim, dark colors, colour scheme, new dark theme, edit dark theme, customize dark theme, duplicate dark theme, fork dark theme, delete dark theme, theme customizer, ansi palette, ansi standard, ansi bright, terminal colors, preview, live preview, live update, pause preview, freeze, theme editor</span> |
| <span id="setting-dark-mode-use-extended-theme-palette" data-entry="Use extended theme palette"></span>Use extended theme palette（使用扩展主题调色板） | 在深色模式下使用主题的 16–255 号颜色；关闭时使用 xterm 标准调色板。<span hidden>In Settings &gt; Themes &gt; Dark Mode.</span> <span hidden>extended palette, extended colors, extended colours, xterm, xterm palette, standard palette, color cube, colour cube, grayscale ramp, greyscale ramp, generated palette, palette-generate, compatibility, on, off</span> |

### 导入主题（Import Theme）
将 Ghostty 或 iTerm 调色板添加到自定主题中。位于“设置”>“主题”>“Import Theme”。 <span hidden>import, file, ghostty, iterm, itermcolors, palette, load, colors, colours, appearance, background, light, dark</span>

## 终端

### 版式（Typography）
预览并选择终端字体、字形、字号、字重与行高。位于“设置”>“终端”>“Typography”。 <span hidden>text, typeface, readability, typography preview, font preview</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-typography-terminal-font" data-entry="Terminal font"></span>Terminal font（终端字体） | 浏览等宽字体或所有已安装字体，以选择终端字体系列。<span hidden>In Settings &gt; Terminal &gt; Typography.</span> <span hidden>font, family, typeface, monospace, menlo, font picker, monospaced fonts, all fonts</span> |
| <span id="setting-typography-font-size" data-entry="Font size"></span>Font size（字号） | 以点（pt）为单位调整终端文本大小。<span hidden>In Settings &gt; Terminal &gt; Typography.</span> <span hidden>text size, larger, smaller, zoom, pt</span> |
| <span id="setting-typography-font-style" data-entry="Font style"></span>Font style（字形样式） | 选择终端字体的已安装字形，例如 Light 或 Book。<span hidden>In Settings &gt; Terminal &gt; Typography.</span> <span hidden>face, variant, italic, oblique, regular, light, medium, semibold, book</span> |
| <span id="setting-typography-font-weight" data-entry="Font weight"></span>Font weight（字重） | 调整可变终端字体的笔画粗细。<span hidden>In Settings &gt; Terminal &gt; Typography.</span> <span hidden>thickness, thin, light, medium, bold, heavy, variable font, wght</span> |
| <span id="setting-typography-line-height" data-entry="Line height"></span>Line height（行高） | 增加或减少终端各行之间的间距。<span hidden>In Settings &gt; Terminal &gt; Typography.</span> <span hidden>cell height, line spacing, leading, adjust-cell-height, ghostty, spacing, taller, compact</span> |

### 高级字体设置（Advanced Font Settings）
调整字符间距、连字、粗体与斜体、合成字形、平滑度以及回退字体。从“版式”下的“高级字体设置”打开。位于“设置”>“终端”>“Advanced Font Settings”。 <span hidden>advanced font settings, advanced typography, advanced font options, advanced fonts, font rendering, text rendering, font options</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-advanced-font-settings-character-spacing" data-entry="Character spacing"></span>Character spacing（字符间距） | 以像素或百分比紧缩或加宽终端字符间距。<span hidden>In Settings &gt; Terminal &gt; Advanced Font Settings.</span> <span hidden>letter spacing, kerning, tracking, cell width, adjust-cell-width, ghostty, maple mono, tighter, wider, pixels, percentage</span> |
| <span id="setting-advanced-font-settings-ligatures" data-entry="Ligatures"></span>Ligatures（连字） | 将如 `-&gt;` 和 `!=` 等字符组合连接为单个符号。<span hidden>In Settings &gt; Terminal &gt; Advanced Font Settings.</span> <span hidden>font features, font-feature, calt, liga, arrows, operators, fira code, jetbrains mono</span> |
| <span id="setting-advanced-font-settings-render-bold-and-italic" data-entry="Render bold and italic"></span>Render bold and italic（渲染粗体与斜体） | 绘制粗体和斜体文本、仅绘制其中之一，或两者均不绘制。<span hidden>In Settings &gt; Terminal &gt; Advanced Font Settings.</span> <span hidden>font-style-bold, font-style-italic, disable bold, no bold, never bold, disable italic, no italic, never italic, upright, bold face, italic face, font weight, regular, both, bold only, italic only, neither, bold, italic, ghostty</span> |
| <span id="setting-advanced-font-settings-force-bold-and-italic-styles" data-entry="Force bold and italic styles"></span>Force bold and italic styles（强制粗体与斜体样式） | 对不包含原生字形的字体使用合成粗体与斜体渲染。仅对缺少对应字形的字体显示。<span hidden>In Settings &gt; Terminal &gt; Advanced Font Settings.</span> <span hidden>font-synthetic-style, synthetic style, synthesize, synthesized, pseudo bold, pseudo italic, fake bold, faux bold, fake italic, faux italic, oblique, slant, slanted, outline, emboldened, missing bold, missing italic, pixel font, bitmap font, monaco, ghostty</span> |
| <span id="setting-advanced-font-settings-font-smoothing" data-entry="Font smoothing"></span>Font smoothing（字体平滑） | 平滑终端文本的边缘。<span hidden>In Settings &gt; Terminal &gt; Advanced Font Settings.</span> <span hidden>antialiasing, anti aliasing, text rendering, sharp, font-thicken, thicken</span> |
| <span id="setting-advanced-font-settings-fallback-fonts" data-entry="Fallback fonts"></span>Fallback fonts（回退字体） | 按优先顺序选择用于显示终端字体中缺失字符的回退字体。<span hidden>In Settings &gt; Terminal &gt; Advanced Font Settings.</span> <span hidden>fallback, font fallback, font-family, missing glyphs, missing characters, symbols, icons, nerd font, cjk, chinese, japanese, korean, emoji, font order, ghostty</span> |

### 颜色（Colors）
控制终端文本颜色与可读性。位于“设置”>“终端”>“Colors”。 <span hidden>colour, color, text, readability</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-colors-improve-text-contrast" data-entry="Improve text contrast"></span>Improve text contrast（提升文本对比度） | 调整低对比度文本与其背景的对比度；在使用主题调色板时生效。<span hidden>In Settings &gt; Terminal &gt; Colors.</span> <span hidden>minimum contrast, automatic, legibility, accessibility, unreadable, faint, pale, yellow, ansi, truecolor, theme, on, off</span> |
| <span id="setting-colors-force-theme-palette-for-text" data-entry="Force theme palette for text"></span>Force theme palette for text（对文本强制使用主题调色板） | 将 RGB 与扩展文本颜色映射到最接近的主题颜色，随后修正对比度。<span hidden>In Settings &gt; Terminal &gt; Colors.</span> <span hidden>force theme colors, force theme colours, remap, match colors, palette, ansi, rgb, truecolor, 256 colors, extended colors, replace, consistent, on, off</span> |
| <span id="setting-colors-use-display-p3-color-space" data-entry="Use Display P3 color space"></span>Use Display P3 color space（使用 Display P3 色彩空间） | 将主题与程序颜色解析为 Display P3 色彩空间，类似于 Ghostty 的 window-colorspace。<span hidden>In Settings &gt; Terminal &gt; Colors.</span> <span hidden>p3, display p3, wide gamut, wide colour, color space, colour space, colorspace, window-colorspace, ghostty, srgb, saturated, vivid, on, off</span> |

### 光标（Cursor）
预览并调整终端光标形状、闪烁和着色器效果。位于“设置”>“终端”>“Cursor”。 <span hidden>caret, insertion, indicator, cursor preview</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-cursor-blink-speed" data-entry="Blink speed"></span>Blink speed（闪烁速度） | 选择关闭、较慢、正常、较快或自定以编辑闪烁间隔。<span hidden>In Settings &gt; Terminal &gt; Cursor.</span> <span hidden>flashing, steady, slow, fast, normal, off, custom</span> |
| <span id="setting-cursor-blink-interval" data-entry="Blink interval"></span>Blink interval（闪烁间隔） | 当闪烁速度设为自定时，以毫秒为单位设置光标闪烁的时间间隔。<span hidden>In Settings &gt; Terminal &gt; Cursor.</span> <span hidden>speed, duration, frequency, ms, custom</span> |
| <span id="setting-cursor-cursor-style" data-entry="Cursor style"></span>Cursor style（光标样式） | 选择方块（Block）、竖线（Bar）或下划线（Underline）光标。<span hidden>In Settings &gt; Terminal &gt; Cursor.</span> <span hidden>shape, beam, caret, block, bar, underline</span> |
| <span id="setting-cursor-force-style" data-entry="Force style"></span>Force style（强制光标样式） | 忽略应用程序更改光标形状的请求。<span hidden>In Settings &gt; Terminal &gt; Cursor.</span> <span hidden>override, application, ignore, shape</span> |
| <span id="setting-cursor-cursor-shaders" data-entry="Cursor shaders"></span>Cursor shaders（光标着色器） | 在终端光标后方绘制拖尾着色器效果，例如 Warp、Comet 或 Blaze。<span hidden>In Settings &gt; Terminal &gt; Cursor.</span> <span hidden>cursor trail, cursor effect, cursor animation, smear, glow, ghostty shader, custom-shader, shadertoy, on, off</span> |
| <span id="setting-cursor-shader" data-entry="Shader"></span>Shader（着色器效果） | 在开启“光标着色器”时，选择所绘制的效果，例如 Warp、Comet 或 Blaze。<span hidden>In Settings &gt; Terminal &gt; Cursor.</span> <span hidden>cursor shader, trail style, effect, warp, sweep, comet, blaze, tapered, rainbow, gradient, frozen</span> |

### 键盘（Keyboard）
显示按键序列提示，并选择修饰键在终端输入中的行为。位于“设置”>“终端”>“Keyboard”。 <span hidden>input, keys, shortcuts, modifier</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-keyboard-show-key-sequence-hints" data-entry="Show key sequence hints"></span>Show key sequence hints（显示按键序列提示） | 在按下序列的首个按键（例如 tmux 风格的前缀键）后，显示可紧跟其后的后续按键。<span hidden>In Settings &gt; Terminal &gt; Keyboard.</span> <span hidden>which-key, which key, prefix, leader, chord, key sequence, popup, overlay, pill</span> |
| <span id="setting-keyboard-option-key" data-entry="Option key"></span>Option key（Option 键） | 选择 Option 键是发送 Alt 键信号还是输入特殊字符。<span hidden>In Settings &gt; Terminal &gt; Keyboard.</span> <span hidden>option, alt, meta, esc, escape, emacs, readline, tmux, compose, accents, special characters, left, right, ∫</span> |

### 滚动（Scrolling）
选择触控板和妙控鼠标滚动在终端历史中的移动方式。位于“设置”>“终端”>“Scrolling”。 <span hidden>scroll, scrollback, history, trackpad, touchpad</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-scrolling-smooth-scrolling" data-entry="Smooth scrolling"></span>Smooth scrolling（平滑滚动） | 在终端历史中按像素逐级滚动，而非整行跳跃。<span hidden>In Settings &gt; Terminal &gt; Scrolling.</span> <span hidden>smooth, pixel, precise, sub-line, fluid, momentum, inertia, trackpad, line by line, on, off</span> |

### 调整大小（Resizing）
选择窗格大小变动时终端文本的排版跟随方式。位于“设置”>“终端”>“Resizing”。 <span hidden>resize, window size, pane size</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-resizing-smooth-terminal-resizing" data-entry="Smooth terminal resizing"></span>Smooth terminal resizing（平滑调整终端大小） | 在窗格改变大小的当帧直接重排终端文本，无需等待服务端响应。<span hidden>In Settings &gt; Terminal &gt; Resizing.</span> <span hidden>smooth resize, resize, reflow, jitter, glitch, jump, flicker, live resize, resize preview, zoom, split, sidebar, window drag, drag, re-wrap, rewrap, on, off</span> |

### 选区（Selection）
预览选区颜色和圆角，并自定复制操作及其动画。位于“设置”>“终端”>“Selection”。 <span hidden>highlight, selected text, copy, colour, animation, selection preview</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-selection-copy-on-selection" data-entry="Copy on selection"></span>Copy on selection（选中文本时自动复制） | 选中终端文本后自动复制到剪贴板。<span hidden>In Settings &gt; Terminal &gt; Selection.</span> <span hidden>automatic copy, clipboard, selection, mouse, on, off</span> |
| <span id="setting-selection-play-animation-on-copy" data-entry="Play animation on copy"></span>Play animation on copy（复制时播放动画） | 在选区上闪烁划过以确认每次复制操作。<span hidden>In Settings &gt; Terminal &gt; Selection.</span> <span hidden>shine, highlight, sheen, glint, pulse, effect, feedback, motion, animate, on, off</span> |
| <span id="setting-selection-selection-foreground" data-entry="Selection foreground"></span>Selection foreground（选区前景色） | 选择选区内部的文本颜色。<span hidden>In Settings &gt; Terminal &gt; Selection.</span> <span hidden>foreground, text color, colour, contrast</span> |
| <span id="setting-selection-selection-background" data-entry="Selection background"></span>Selection background（选区背景色） | 选择选中文本背后的填充颜色。<span hidden>In Settings &gt; Terminal &gt; Selection.</span> <span hidden>background, highlight color, colour, fill</span> |
| <span id="setting-selection-rounded-corners" data-entry="Rounded corners"></span>Rounded corners（圆角） | 为终端文本选区应用圆角效果。<span hidden>In Settings &gt; Terminal &gt; Selection.</span> <span hidden>radius, rounding, square</span> |

### 链接（Links）
选择启动其他应用的终端链接在打开前是否需要确认。位于“设置”>“终端”>“Links”。 <span hidden>hyperlink, url, osc 8, command click, cmd click, open link, security, safety, custom scheme, url scheme</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-links-links-that-open-apps" data-entry="Links that open apps"></span>Links that open apps（打开应用的链接） | 打开如 `ssh://` 等会启动其他应用的链接时：打开前询问、始终打开或从不打开。<span hidden>In Settings &gt; Terminal &gt; Links.</span> <span hidden>ask first, ask before opening, always open, never open, confirm, confirmation, prompt, allow, block, vscode, ssh, custom scheme, launch app, open app</span> |
| <span id="setting-links-trusted-links" data-entry="Trusted links"></span>Trusted links（受信任的链接） | 当通过“始终打开”添加条目后，检查并移除你此前选择始终打开的链接。<span hidden>In Settings &gt; Terminal &gt; Links.</span> <span hidden>always open, allowed links, allowlist, trusted apps, remembered, forget, remove, revoke, permissions</span> |

### 集成路径浏览器（Integrated Path Browser）
选择“插入路径”在光标处输入路径时列出的内容。从“版式”下的“高级字体设置”打开。位于“设置”>“终端”>“Integrated Path Browser”。 <span hidden>insert path, path browser, file picker, path picker, paths, files, folders, autocomplete, completion</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-integrated-path-browser-show-recently-used-paths" data-entry="Show recently used paths"></span>Show recently used paths（显示最近使用的路径） | 优先列出你最近选择的路径，该列表由同一主机上的所有会话共享。<span hidden>In Settings &gt; Terminal &gt; Integrated Path Browser.</span> <span hidden>recents, recent files, history, recently used, mru, frequent, remember, on, off</span> |

### 标题（Titles）
选择终端标签页和窗格标题栏的命名方式。位于“设置”>“终端”>“Titles”。 <span hidden>tab, window, pane, name, label</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-titles-prefer-generated-titles" data-entry="Prefer generated titles"></span>Prefer generated titles（优先使用生成的标题） | 显示正在运行的程序及其目录，而非 shell 设置的标题。<span hidden>In Settings &gt; Terminal &gt; Titles.</span> <span hidden>shell title, generated title, program name, process name, directory, working directory, path, ignore shell titles, always use generated titles, automatic, on, off</span> |

### Shell 设置（Shell）
选择打开新的本地终端时运行的命令。位于“设置”>“终端”>“Shell”。 <span hidden>startup, session, command line, login</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-shell-startup-command" data-entry="Startup command"></span>Startup command（启动命令） | 设置可执行文件与参数，留空则使用默认登录 shell。<span hidden>In Settings &gt; Terminal &gt; Shell.</span> <span hidden>shell, zsh, bash, fish, executable, arguments, launch, startup, working directory</span> |

## 远程主机

### 远程主机（Remote hosts）
添加、重新排序和管理远程 Rex 主机，查看连接状态，回答 SSH 提示问题，在连接失败时重试，以及进行端口转发。位于“设置”>“远程主机”>“Remote hosts”。 <span hidden>remote, connections, machines, servers, add host, remove host, retry, host details, remote host status, remote host reconnect, connection warning, connection failure, host address, reorder hosts, host order, sort hosts, arrange hosts, move host up, move host down, drag hosts, ssh, ssh host, ssh passphrase, ssh password, host key, answer ssh question, waiting for an answer, needs your answer, finish setup, trust host, port forwarding, forward port, forwards, tunnel, ssh `-L`, localhost link</span>

### SSH

选择 ssh 连接 `ssh://` 主机的方式，包括向其请求密钥的 SSH agent（例如 Secretive 或 1Password）。位于“设置”>“远程主机”>“SSH”。 <span hidden>ssh agent, agent, SSH_AUTH_SOCK, auth sock, agent socket, IdentityAgent, identity agent, ssh keys, keys, publickey, permission denied, authentication failed, Secretive, 1Password, Bitwarden, yubikey-agent, YubiKey, gpg-agent, GnuPG, system agent, custom agent</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-ssh-ssh-agent" data-entry="SSH agent"></span>SSH agent | ssh 查找 `ssh://` 主机密钥的来源：macOS agent、此 Mac 上的特定 agent 或自定套接字。<span hidden>In Settings &gt; Remote Hosts &gt; SSH.</span> <span hidden>system, macOS agent, Secretive, 1Password, Bitwarden, yubikey-agent, gpg-agent, custom</span> |
| <span id="setting-ssh-ssh-agent-socket" data-entry="SSH agent socket"></span>SSH agent socket（SSH agent 套接字） | 自定 agent 套接字的路径。<span hidden>In Settings &gt; Remote Hosts &gt; SSH.</span> <span hidden>socket path, SSH_AUTH_SOCK, custom agent, agent.sock</span> |
| <span id="setting-ssh-ssh-agent-status" data-entry="SSH agent status"></span>SSH agent status（SSH agent 状态） | 所选 agent 是否响应，以及其持有的密钥数量。<span hidden>In Settings &gt; Remote Hosts &gt; SSH.</span> <span hidden>check again, keys, ssh-add, not running, no keys</span> |

## 开发者

<div class="api-tags"><span class="api-tag developer"><a href="#setting-developer-developer-mode">Developer Mode</a></span></div>

显示用于开发和调试的设置项。位于“设置”>“开发者”。 <span hidden>advanced, debug, tools</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-developer-developer-mode" data-entry="Developer Mode"></span>Developer Mode（开发者模式） | 显示更新通道、安装方式、本地 API、Web 客户端源以及实验性设置项。<span hidden>In Settings &gt; Developer.</span> <span hidden>enable, advanced, development, debugging</span> |

### 实验性功能（Experimental）
在启用“开发者模式”时体验未正式发布的特性。位于“设置”>“开发者”>“Experimental”。 <span hidden>experiment, beta, unfinished, labs</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-experimental-download-new-updates-when-available" data-entry="Download new updates when available"></span>Download new updates when available（有可用更新时自动下载） | 在后台下载更新并在重启前进行提示。<span hidden>In Settings &gt; Developer &gt; Experimental. Needs Developer Mode.</span> <span hidden>auto download, background download, install on quit, download new updates, auto update, sparkle</span> |
| <span id="setting-experimental-install-updates-automatically" data-entry="Install updates automatically"></span>Install updates automatically（自动安装更新） | 在 Rex 未处于前台显示状态时重启进入新版本。<span hidden>In Settings &gt; Developer &gt; Experimental. Needs Developer Mode.</span> <span hidden>auto install, auto relaunch, auto restart, silent update, unattended update, relaunch when idle</span> |
| <span id="setting-experimental-terminal-anchoring" data-entry="Terminal anchoring"></span>Terminal anchoring（终端锚定） | 将终端文本固定在每个窗格的顶部或底部。<span hidden>In Settings &gt; Developer &gt; Experimental. Needs Developer Mode.</span> <span hidden>anchor, terminal alignment, grid gravity, leftover row</span> |
| <span id="setting-experimental-new-quick-switcher" data-entry="New quick switcher"></span>New quick switcher（新版快速切换器） | 在“前往任意位置”中打开一个汇总所有会话、块和报告中进程的统一列表。<span hidden>In Settings &gt; Developer &gt; Experimental. Needs Developer Mode.</span> <span hidden>go to anything, go to session, view activity, switcher, command palette, cmd p, jump, navigate, panes, blocks, sessions, experiment</span> |

### 应用版本（App Version）
在启用“开发者模式”时选择 Rex.app 接收更新的方式。位于“设置”>“开发者”>“App Version”。 <span hidden>application, release, update, channel, upgrade</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-app-version-update-channel" data-entry="Update Channel"></span>Update Channel（更新通道） | 在启用“开发者模式”时选择 Preview 或 Bleeding Edge 更新。<span hidden>In Settings &gt; Developer &gt; App Version. Needs Developer Mode.</span> <span hidden>bleeding edge, testing, snapshot, preview, version, upgrade</span> |

### Rex 安装（Rex Installation）
选择使用内置服务端或从源码仓库运行 Rex。位于“设置”>“开发者”>“Rex Installation”。 <span hidden>binary, install, source, development</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-rex-installation-location" data-entry="Location"></span>Location（安装位置） | 使用 Rex.app 内置的服务端或本地源码仓库。<span hidden>In Settings &gt; Developer &gt; Rex Installation. Needs Developer Mode.</span> <span hidden>bundled, included, source checkout, installation</span> |
| <span id="setting-rex-installation-source-directory" data-entry="Source Directory"></span>Source Directory（源码目录） | 选择包含 Rex 源码仓库的文件夹。<span hidden>In Settings &gt; Developer &gt; Rex Installation. Needs Developer Mode.</span> <span hidden>folder, path, repository, repo, checkout, choose</span> |
| <span id="setting-rex-installation-installation-status" data-entry="Installation status"></span>Installation status（安装状态） | 检查所选的 Rex 安装是否已准备就绪可运行。<span hidden>In Settings &gt; Developer &gt; Rex Installation. Needs Developer Mode.</span> <span hidden>show details, hide details, version, binary, executable, copy, paths, status</span> |
| <span id="setting-rex-installation-version" data-entry="Version"></span>Version（版本） | 在“显示详细信息”下查看并复制内置服务端版本。<span hidden>In Settings &gt; Developer &gt; Rex Installation. Needs Developer Mode.</span> <span hidden>release, build, included, bundled, copy</span> |
| <span id="setting-rex-installation-commit" data-entry="Commit"></span>Commit（提交哈希） | 在“显示详细信息”下查看并复制内置服务端的源码提交。<span hidden>In Settings &gt; Developer &gt; Rex Installation. Needs Developer Mode.</span> <span hidden>revision, git, hash, build, copy</span> |
| <span id="setting-rex-installation-final-sha-256" data-entry="Final SHA-256"></span>Final SHA-256（最终校验和） | 在“显示详细信息”下查看并复制内置服务端的校验和。<span hidden>In Settings &gt; Developer &gt; Rex Installation. Needs Developer Mode.</span> <span hidden>checksum, digest, hash, sha256, integrity, copy</span> |

### 本地 API（Local API）
在启用“开发者模式”时检查本地服务端的 API 端点。位于“设置”>“开发者”>“Local API”。 <span hidden>local server, control api, development, connection</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-local-api-local-api-url" data-entry="Local API URL"></span>Local API URL（本地 API 地址） | 在启用“开发者模式”时查看并复制本地服务端端点。<span hidden>In Settings &gt; Developer &gt; Local API. Needs Developer Mode.</span> <span hidden>address, localhost, port, http, copy local endpoint, unix socket, socket path</span> |

### Web 客户端源（Web Client Origins）
管理获准建立 Rex WebSocket 流的浏览器来源（origins）。位于“设置”>“开发者”>“Web Client Origins”。 <span hidden>browser, web, websocket, security, cors</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-web-client-origins-allowed-origins" data-entry="Allowed origins"></span>Allowed origins（获准的来源） | 查看获准的来源并移除自定条目。<span hidden>In Settings &gt; Developer &gt; Web Client Origins. Needs Developer Mode.</span> <span hidden>allowlist, delete, remove, hosted client, default, permissions</span> |
| <span id="setting-web-client-origins-origin-pattern" data-entry="Origin pattern"></span>Origin pattern（来源模式） | 输入重启 Rex 后获准接入的浏览器源或通配符子域名。<span hidden>In Settings &gt; Developer &gt; Web Client Origins. Needs Developer Mode.</span> <span hidden>add origin, allowed origin, wildcard, subdomain, domain, https, web client</span> |
