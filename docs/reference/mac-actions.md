> 原文：https://www.superlogical.com/rex/docs/reference/mac-actions
> 原文版本：bf71f75832d9（抓取于 2026-11-13）

# Mac 操作

本页列出 Rex for Mac 命令面板中的所有操作。可以使用操作名称来[绑定快捷键](../customize/keyboard-shortcuts.md)或通过 `rex do` 运行。任何标记为 [Bleeding Edge](mac-settings.md#setting-app-version-update-channel) 的内容均处于该更新通道中，尚未进入 Preview。

<div class="reference-page actions" hidden></div>

## 窗口

| 操作 | 名称 | 默认快捷键 |
| --- | --- | --- |
| <span id="action-client-window-new" data-entry="New Window"></span>New Window（新建窗口） | `client.window.new` <span hidden>create workspace window</span> |  <span hidden>默认快捷键：</span>`cmd+n` |
| <span id="action-client-window-close" data-entry="Close Window"></span>Close Window（关闭窗口） | `client.window.close` <span hidden>close workspace window</span> |  <span hidden>默认快捷键：</span>`shift+cmd+w` |
| <span id="action-client-window-fullscreen-toggle" data-entry="Toggle Full Screen"></span>Toggle Full Screen（切换全屏） | `client.window.fullscreen.toggle` <span hidden>full screen fullscreen enter exit window</span> |  <span hidden>默认快捷键：</span>`ctrl+cmd+f` |
| <span id="action-client-close" data-entry="Close"></span>Close（关闭） 关闭获得焦点的窗格；若无窗格则关闭选中的标签页；若无标签页则关闭窗口。 | `client.close` <span hidden>close pane tab window focused</span> |  <span hidden>默认快捷键：</span>`cmd+w` |

## 应用

| 操作 | 名称 | 默认快捷键 |
| --- | --- | --- |
| <span id="action-client-palette-toggle" data-entry="Command Palette…"></span>Command Palette…（命令面板…） | `client.palette.toggle` <span hidden>command palette search commands actions</span> |  <span hidden>默认快捷键：</span>`shift+cmd+p` |
| <span id="action-client-settings" data-entry="Settings…"></span>Settings…（设置…） | `client.settings` <span hidden>preferences settings options configure</span> |  <span hidden>默认快捷键：</span>`cmd+,` |
| <span id="action-client-diagnostics" data-entry="Rex Diagnostics"></span>Rex Diagnostics（Rex 诊断） | `client.diagnostics` <span hidden>diagnostics logs debug troubleshoot server report</span> |  <span hidden>默认快捷键：</span>`shift+cmd+,` |
| <span id="action-client-onboarding" data-entry="Open Onboarding Session…"></span>Open Onboarding Session…（打开入门引导会话…） | `client.onboarding` <span hidden>onboarding welcome setup get started tour walkthrough migrate import keybindings theme appearance ghostty tmux zellij agent</span> |  |
| <span id="action-client-permissions" data-entry="Grant System Permissions…"></span>Grant System Permissions…（授予系统权限…） | `client.permissions` <span hidden>permissions privacy security full disk access screen recording system audio grant allow system settings tcc</span> |  |
| <span id="action-client-visibility-toggle" data-entry="Toggle Visibility"></span>Toggle Visibility（切换可见性） 在任何应用中唤出 Rex，或者在处于前台时将其隐藏。 | `client.visibility.toggle` <span hidden>show hide rex global hotkey summon bring to front focus toggle_visibility</span> |  |
| <span id="action-client-version-copy" data-entry="Copy Version Info"></span>Copy Version Info（复制版本信息） 将应用和服务端版本复制到剪贴板。 | `client.version.copy` <span hidden>version build number copy clipboard about app server release</span> |  |
| <span id="action-client-debug-copy" data-entry="Copy Debug Info"></span>Copy Debug Info（复制调试信息） 将应用、系统、服务端和主机状态报告复制到剪贴板。 | `client.debug.copy` <span hidden>debug debugging info report copy clipboard diagnostics troubleshoot support bug commit build environment</span> |  |
| <span id="action-client-pair-device" data-entry="Pair Device with QR Code…"></span>Pair Device with QR Code…（通过二维码配对设备…） | `client.pair_device` <span hidden>pair device qr code scan iphone ipad ios mobile tailscale connect link</span> |  |
| <span id="action-client-update-accept" data-entry="Install Update"></span>Install Update（安装更新） 菜单中会显示当前更新自身的标题；此处为静态回退文案。 | `client.update.accept` <span hidden>update install retry app application version upgrade sparkle</span> |  <span hidden>默认快捷键：</span>`shift+cmd+u` |
| <span id="action-client-update-accept-when-idle" data-entry="Relaunch when Idle"></span>Relaunch when Idle（空闲时重启） 在 Rex 窗口移出视野后重启并进入已下载的更新。 | `client.update.accept_when_idle` <span hidden>update install relaunch restart idle later automatic</span> |  <span hidden>默认快捷键：</span>`alt+shift+cmd+u` |
| <span id="action-client-update-check" data-entry="Check for Updates in Background"></span>Check for Updates in Background（后台检查更新） 在后台静默检查 Rex 更新并返回检查结果。 | `client.update.check` <span hidden>update check background quiet silent app application version sparkle</span> |  |
| <span id="action-client-update-status" data-entry="Report Update Status"></span>Report Update Status（报告更新状态） 返回正在运行的版本、更新设置以及更新程序的状态。 | `client.update.status` <span hidden>update status version build channel feed state report sparkle</span> |  |
| <span id="action-client-update-install" data-entry="Install Update and Relaunch"></span>Install Update and Relaunch（安装更新并重启） 在需要时下载可用的 Rex 更新，安装并直接重启，无需再次确认。 | `client.update.install` <span hidden>update install download relaunch restart upgrade app application sparkle unattended</span> |  |
| <span id="action-client-update-set-automation" data-entry="Set Update Automation"></span>Set Update Automation（设置更新自动化） 选择 Rex 仅提示更新、下载更新还是自动安装更新。 | `client.update.set_automation` <span hidden>update automatic automation download install notify setting preference</span> |  |
| <span id="action-client-update-set-channel" data-entry="Set Update Channel"></span>Set Update Channel（设置更新通道） 选择 Rex 获取更新的发布通道。 | `client.update.set_channel` <span hidden>update channel feed preview snapshot bleeding edge release setting preference</span> |  |
| <span id="action-client-notice-dismiss" data-entry="Dismiss Notice"></span>Dismiss Notice（忽略通知） | `client.notice.dismiss` <span hidden>dismiss notice banner alert hide</span> |  <span hidden>默认快捷键：</span>`shift+cmd+.` |
| <span id="action-client-shortcuts-edit" data-entry="Change Shortcut…"></span>Change Shortcut…（更改快捷键…） | `client.shortcuts.edit` <span hidden>keyboard key binding bindings keybinding keybindings rebind record hotkey shortcut</span> |  |
| <span id="action-client-agents-setup" data-entry="Install Rex for Agents"></span>Install Rex for Agents（为智能体安装 Rex） 为 Claude Code、Codex 及其他智能体安装 Rex skill 与 hook。 | `client.agents.setup` <span hidden>`rex skill` install agent agents coding ai claude code codex cursor copilot gemini hook hooks setup</span> |  |
| <span id="action-client-server-restart" data-entry="Restart Server…"></span>Restart Server…（重启服务端…） 停止本地 Rex 服务端并重新启动。 | `client.server.restart` <span hidden>restart reload relaunch reboot stop start server rex daemon process local</span> |  |

## 会话

| 操作 | 名称 | 默认快捷键 |
| --- | --- | --- |
| <span id="action-session-new" data-entry="New Session"></span>New Session（新建会话） | `session.new` <span hidden>create session add</span> |  <span hidden>默认快捷键：</span>`shift+cmd+n` |
| <span id="action-session-switch" data-entry="Change Session…"></span>Change Session…（切换会话…） | `session.switch` <span hidden>session switch jump go</span> |  <span hidden>默认快捷键：</span>`cmd+k` |
| <span id="action-session-select" data-entry="Go to Session"></span>Go to Session（前往会话） | `session.select` <span hidden>session select show jump go identifier id</span> |  |
| <span id="action-session-next" data-entry="Next Session"></span>Next Session（下一个会话） | `session.next` <span hidden>cycle session forward</span> |  |
| <span id="action-session-previous" data-entry="Previous Session"></span>Previous Session（上一个会话） | `session.previous` <span hidden>cycle session back</span> |  |
| <span id="action-session-rename" data-entry="Rename Session"></span>Rename Session（重命名会话） | `session.rename` <span hidden>rename session name title</span> |  |
| <span id="action-session-close" data-entry="Close Session"></span>Close Session（关闭会话） | `session.close` <span hidden>close kill destroy delete session</span> |  |
| <span id="action-session-refresh" data-entry="Refresh Sessions"></span>Refresh Sessions（刷新会话） | `session.refresh` <span hidden>reload sync sessions</span> |  <span hidden>默认快捷键：</span>`cmd+r` |
| <span id="action-session-collapse" data-entry="Collapse Session"></span>Collapse Session（折叠会话） | `session.collapse` <span hidden>collapse fold hide session sidebar tabs</span> |  |
| <span id="action-session-expand" data-entry="Expand Session"></span>Expand Session（展开会话） | `session.expand` <span hidden>expand unfold show open session sidebar tabs</span> |  |
| <span id="action-session-collapse-others" data-entry="Collapse Other Sessions"></span>Collapse Other Sessions（折叠其他会话） | `session.collapse_others` <span hidden>collapse fold hide other all sessions sidebar focus</span> |  |

## 主机

| 操作 | 名称 | 默认快捷键 |
| --- | --- | --- |
| <span id="action-client-host-switch" data-entry="Switch Host"></span>Switch Host（切换主机） | `client.host.switch` <span hidden>host remote machine server switch go</span> |  |
| <span id="action-client-host-add" data-entry="Add Remote Host…"></span>Add Remote Host…（添加远程主机…） | `client.host.add` <span hidden>host remote add server machine url http https connect</span> |  |
| <span id="action-client-host-remove" data-entry="Remove Host…"></span>Remove Host…（移除主机…） | `client.host.remove` <span hidden>remove forget delete disconnect host remote server machine</span> |  |

## 标签页

| 操作 | 名称 | 默认快捷键 |
| --- | --- | --- |
| <span id="action-client-tab-new" data-entry="New Tab"></span>New Tab（新建标签页） | `client.tab.new` <span hidden>create tab window add</span> |  <span hidden>默认快捷键：</span>`cmd+t` |
| <span id="action-client-tab-close" data-entry="Close Tab"></span>Close Tab（关闭标签页） | `client.tab.close` <span hidden>close tab window</span> |  <span hidden>默认快捷键：</span>`alt+cmd+w` |
| <span id="action-client-tab-close-others" data-entry="Close Other Tabs"></span>Close Other Tabs（关闭其他标签页） | `client.tab.close_others` <span hidden>close other tabs windows kill only keep</span> |  |
| <span id="action-client-tab-rename" data-entry="Rename Tab"></span>Rename Tab（重命名标签页） | `client.tab.rename` <span hidden>rename tab window name title</span> |  |
| <span id="action-client-tab-next" data-entry="Show Next Tab"></span>Show Next Tab（显示下一个标签页） | `client.tab.next` <span hidden>cycle tab window forward</span> |  <span hidden>默认快捷键：</span>`ctrl+tab`, `shift+cmd+]` |
| <span id="action-client-tab-previous" data-entry="Show Previous Tab"></span>Show Previous Tab（显示上一个标签页） | `client.tab.previous` <span hidden>cycle tab window back</span> |  <span hidden>默认快捷键：</span>`ctrl+shift+tab`, `shift+cmd+[` |
| <span id="action-client-tab-goto" data-entry="Go to Tab"></span>Go to Tab（前往标签页） | `client.tab.goto` <span hidden>tab window select number index jump go</span> |  <span hidden>默认快捷键：</span>`cmd+[Digit1]`, `cmd+[Digit2]`, `cmd+[Digit3]`, `cmd+[Digit4]`, `cmd+[Digit5]`, `cmd+[Digit6]`, `cmd+[Digit7]`, `cmd+[Digit8]`, `cmd+[Digit9]` |
| <span id="action-client-tab-move" data-entry="Move Tab"></span>Move Tab（移动标签页） | `client.tab.move` <span hidden>move tab window reorder</span> |  |
| <span id="action-client-tab-move-backward" data-entry="Move Tab Backward"></span>Move Tab Backward（向后移动标签页） | `client.tab.move.backward` <span hidden>move tab window reorder left up earlier</span> |  <span hidden>默认快捷键：</span>`ctrl+shift+pageup` |
| <span id="action-client-tab-move-forward" data-entry="Move Tab Forward"></span>Move Tab Forward（向前移动标签页） | `client.tab.move.forward` <span hidden>move tab window reorder right down later</span> |  <span hidden>默认快捷键：</span>`ctrl+shift+pagedown` |
| <span id="action-client-tab-move-to-new-window" data-entry="Move Tab to New Window"></span>Move Tab to New Window（移动标签页至新窗口） | `client.tab.move_to_new_window` <span hidden>move tab new window tear off detach separate pop out own</span> |  |

## 窗格

| 操作 | 名称 | 默认快捷键 |
| --- | --- | --- |
| <span id="action-pane-split" data-entry="Split Pane"></span>Split Pane（拆分窗格） | `pane.split` <span hidden>pane split terminal divide new</span> |  |
| <span id="action-pane-split-left" data-entry="Split Pane Left"></span>Split Pane Left（向左拆分窗格） | `pane.split.left` <span hidden>pane split terminal divide new left</span> |  <span hidden>默认快捷键：</span>`shift+cmd+left` |
| <span id="action-pane-split-right" data-entry="Split Pane Right"></span>Split Pane Right（向右拆分窗格） | `pane.split.right` <span hidden>pane split terminal divide new right</span> |  <span hidden>默认快捷键：</span>`cmd+d`, `shift+cmd+right` |
| <span id="action-pane-split-up" data-entry="Split Pane Up"></span>Split Pane Up（向上拆分窗格） | `pane.split.up` <span hidden>pane split terminal divide new above up</span> |  <span hidden>默认快捷键：</span>`shift+cmd+up` |
| <span id="action-pane-split-down" data-entry="Split Pane Down"></span>Split Pane Down（向下拆分窗格） | `pane.split.down` <span hidden>pane split terminal divide new below down</span> |  <span hidden>默认快捷键：</span>`shift+cmd+d`, `shift+cmd+down` |
| <span id="action-pane-split-auto" data-entry="Split Pane Best Fit"></span>Split Pane Best Fit（自适应拆分窗格） | `pane.split.auto` <span hidden>pane split terminal divide new automatic best fit</span> |  <span hidden>默认快捷键：</span>`cmd+enter` |
| <span id="action-pane-focus" data-entry="Focus Pane"></span>Focus Pane（聚焦窗格） | `pane.focus` <span hidden>pane focus navigate</span> |  |
| <span id="action-pane-focus-left" data-entry="Focus Pane Left"></span>Focus Pane Left（聚焦左侧窗格） | `pane.focus.left` <span hidden>pane focus navigate left</span> |  <span hidden>默认快捷键：</span>`alt+cmd+left` |
| <span id="action-pane-focus-right" data-entry="Focus Pane Right"></span>Focus Pane Right（聚焦右侧窗格） | `pane.focus.right` <span hidden>pane focus navigate right</span> |  <span hidden>默认快捷键：</span>`alt+cmd+right` |
| <span id="action-pane-focus-up" data-entry="Focus Pane Up"></span>Focus Pane Up（聚焦上方窗格） | `pane.focus.up` <span hidden>pane focus navigate up above</span> |  <span hidden>默认快捷键：</span>`alt+cmd+up` |
| <span id="action-pane-focus-down" data-entry="Focus Pane Down"></span>Focus Pane Down（聚焦下方窗格） | `pane.focus.down` <span hidden>pane focus navigate down below</span> |  <span hidden>默认快捷键：</span>`alt+cmd+down` |
| <span id="action-pane-focus-next" data-entry="Focus Next Pane"></span>Focus Next Pane（聚焦下一个窗格） | `pane.focus_next` <span hidden>pane focus next forward</span> |  <span hidden>默认快捷键：</span>`cmd+]` |
| <span id="action-pane-focus-previous" data-entry="Focus Previous Pane"></span>Focus Previous Pane（聚焦上一个窗格） | `pane.focus_previous` <span hidden>pane focus previous back</span> |  <span hidden>默认快捷键：</span>`cmd+[` |
| <span id="action-pane-move" data-entry="Move Pane"></span>Move Pane（移动窗格） | `pane.move` <span hidden>pane move swap rearrange</span> |  |
| <span id="action-pane-move-left" data-entry="Move Pane Left"></span>Move Pane Left（向左移动窗格） | `pane.move.left` <span hidden>pane move swap rearrange left</span> |  <span hidden>默认快捷键：</span>`alt+shift+cmd+left` |
| <span id="action-pane-move-right" data-entry="Move Pane Right"></span>Move Pane Right（向右移动窗格） | `pane.move.right` <span hidden>pane move swap rearrange right</span> |  <span hidden>默认快捷键：</span>`alt+shift+cmd+right` |
| <span id="action-pane-move-up" data-entry="Move Pane Up"></span>Move Pane Up（向上移动窗格） | `pane.move.up` <span hidden>pane move swap rearrange up above</span> |  <span hidden>默认快捷键：</span>`alt+shift+cmd+up` |
| <span id="action-pane-move-down" data-entry="Move Pane Down"></span>Move Pane Down（向下移动窗格） | `pane.move.down` <span hidden>pane move swap rearrange down below</span> |  <span hidden>默认快捷键：</span>`alt+shift+cmd+down` |
| <span id="action-pane-float" data-entry="Float Pane"></span>Float Pane（悬浮窗格） | `pane.float` <span hidden>pane float floating window dock undock detach overlay pop out tile</span> |  <span hidden>默认快捷键：</span>`alt+cmd+enter` |
| <span id="action-pane-new-floating" data-entry="New Floating Pane"></span>New Floating Pane（新建悬浮窗格） | `pane.new_floating` <span hidden>pane new create open float floating window terminal overlay popup scratchpad</span> |  |
| <span id="action-pane-minimize-floating" data-entry="Minimize Floating Window"></span>Minimize Floating Window（最小化悬浮窗口） | `pane.minimize_floating` <span hidden>pane floating window hide show toggle minimize minimise restore taskbar capsule stash scratchpad</span> |  <span hidden>默认快捷键：</span>`alt+cmd+m` |
| <span id="action-pane-minimize-all-floating" data-entry="Minimize Floating Windows"></span>Minimize Floating Windows（最小化所有悬浮窗口） | `pane.minimize_all_floating` <span hidden>pane floating windows all hide show toggle minimize minimise restore taskbar capsule stash scratchpad</span> |  <span hidden>默认快捷键：</span>`alt+shift+cmd+enter` |
| <span id="action-pane-zoom" data-entry="Zoom Pane"></span>Zoom Pane（缩放/最大化窗格） | `pane.zoom` <span hidden>pane zoom maximize restore terminal</span> |  <span hidden>默认快捷键：</span>`shift+cmd+enter` |
| <span id="action-pane-close" data-entry="Close Pane"></span>Close Pane（关闭窗格） | `pane.close` <span hidden>pane close remove terminal</span> |  <span hidden>默认快捷键：</span>`cmd+w` |
| <span id="action-pane-close-others" data-entry="Close Other Panes"></span>Close Other Panes（关闭其他窗格） | `pane.close_others` <span hidden>close other panes kill only keep focused</span> |  |
| <span id="action-pane-balance" data-entry="Balance Splits"></span>Balance Splits（均分分栏） | `pane.balance` <span hidden>pane split balance equalize equalise evenly distribute resize layout</span> |  |
| <span id="action-pane-resize" data-entry="Resize Pane"></span>Resize Pane（调整窗格大小） | `pane.resize` <span hidden>pane resize grow shrink divider wider narrower taller shorter</span> |  |
| <span id="action-pane-move-to-new-tab" data-entry="Move Pane to New Tab"></span>Move Pane to New Tab（移动窗格至新标签页） | `pane.move_to_new_tab` <span hidden>pane block move new window tab detach split</span> |  |
| <span id="action-pane-move-to-tab" data-entry="Move Pane to Tab…"></span>Move Pane to Tab…（移动窗格至标签页…） | `pane.move_to_tab` <span hidden>pane block move tab window send other existing join</span> |  |
| <span id="action-pane-go-to-directory" data-entry="Go to Directory…"></span>Go to Directory…（前往目录…） | `pane.go_to_directory` <span hidden>go to directory folder path cd new tab open navigate</span> |  <span hidden>默认快捷键：</span>`shift+cmd+g` |
| <span id="action-pane-go-to" data-entry="Go to Anything…"></span>Go to Anything…（前往任意位置…） | `pane.go_to` <span hidden>go to anything pane block tab session agent jump switch navigate find search tree overview</span> |  <span hidden>默认快捷键：</span>`cmd+p` |
| <span id="action-pane-view-activity" data-entry="View Activity…"></span>View Activity…（查看活动…） | `pane.view_activity` <span hidden>view activity active working blocked failed done agents programs status priority</span> |  |
| <span id="action-pane-insert-path" data-entry="Insert Path…"></span>Insert Path…（插入路径…） | `pane.insert_path` <span hidden>insert path file folder directory cursor type paste complete browse</span> |  <span hidden>默认快捷键：</span>`ctrl+cmd+i` |
| <span id="action-pane-copy-id" data-entry="Copy Pane ID"></span>Copy Pane ID（复制窗格 ID） 将获得焦点的窗格块 ID 复制到剪贴板。 | `pane.copy_id` <span hidden>pane block id identifier copy clipboard target agent capture</span> |  |
| <span id="action-pane-rename" data-entry="Rename Pane"></span>Rename Pane（重命名窗格） | `pane.rename` <span hidden>rename pane block name title label</span> |  |
| <span id="action-pane-paste" data-entry="Paste into Pane"></span>Paste into Pane（粘贴至窗格） 将剪贴板内容粘贴到获得焦点的终端中。 | `pane.paste` <span hidden>paste clipboard insert text terminal</span> |  |
| <span id="action-pane-copy" data-entry="Copy from Pane"></span>Copy from Pane（从窗格复制） 将获得焦点的终端选中内容复制到剪贴板。 | `pane.copy` <span hidden>copy selection clipboard text terminal</span> |  |
| <span id="action-pane-select-all" data-entry="Select All in Pane"></span>Select All in Pane（全选窗格内容） 选中获得焦点的终端中的所有内容，包含其回滚缓冲区。 | `pane.select_all` <span hidden>select all selection text terminal scrollback</span> |  |
| <span id="action-pane-send-key" data-entry="Send Key"></span>Send Key（发送按键） 向获得焦点的终端发送一个按键，如同在该终端中按下一样。 | `pane.send_key` <span hidden>send key terminal press chord binding</span> |  <span hidden>默认快捷键：</span>`cmd+backspace`, `cmd+left`, `cmd+right`, `alt+left`, `alt+right` |
| <span id="action-client-key-forward" data-entry="Send Key to Server"></span>Send Key to Server（发送按键至服务端） 将触发该操作的按键发送到获得焦点的终端，供脚本响应。 | `client.key.forward` <span hidden>send key forward server script lua binding</span> |  |
| <span id="action-client-prompt-previous" data-entry="Jump to Previous Prompt"></span>Jump to Previous Prompt（跳至上一个提示符） | `client.prompt.previous` <span hidden>jump scroll previous prompt command mark shell integration up back history</span> |  <span hidden>默认快捷键：</span>`cmd+up` |
| <span id="action-client-prompt-next" data-entry="Jump to Next Prompt"></span>Jump to Next Prompt（跳至下一个提示符） | `client.prompt.next` <span hidden>jump scroll next prompt command mark shell integration down forward</span> |  <span hidden>默认快捷键：</span>`cmd+down` |
| <span id="action-client-scroll-page-up" data-entry="Scroll Page Up"></span>Scroll Page Up（向上翻页） | `client.scroll.page_up` <span hidden>scroll page up back scrollback history</span> |  |
| <span id="action-client-scroll-page-down" data-entry="Scroll Page Down"></span>Scroll Page Down（向下翻页） | `client.scroll.page_down` <span hidden>scroll page down forward scrollback history</span> |  |
| <span id="action-client-quick-look" data-entry="Quick Look"></span>Quick Look（快速查看） 在“快速查看”中预览屏幕上的文件和网页链接。 | `client.quick_look` <span hidden>quick look preview file image link path url web pointer hover</span> |  <span hidden>默认快捷键：</span>`cmd+y` |

## 按键

| 操作 | 名称 | 默认快捷键 |
| --- | --- | --- |
| <span id="action-client-mode-enter" data-entry="Enter Mode"></span>Enter Mode（进入模式） 启用某个模式所绑定的按键，直到退出该模式为止。 | `client.mode.enter` <span hidden>mode enter key table prefix resize modal</span> |  |
| <span id="action-client-mode-exit" data-entry="Exit Mode"></span>Exit Mode（退出模式） | `client.mode.exit` <span hidden>mode exit leave quit key table escape</span> |  |
| <span id="action-client-mode-exit-all" data-entry="Exit All Modes"></span>Exit All Modes（退出所有模式） | `client.mode.exit_all` <span hidden>mode exit leave quit all key table escape</span> |  |

## 查找

| 操作 | 名称 | 默认快捷键 |
| --- | --- | --- |
| <span id="action-client-find-open" data-entry="Find…"></span>Find…（查找…） | `client.find.open` <span hidden>find search text scrollback highlight</span> |  <span hidden>默认快捷键：</span>`cmd+f` |
| <span id="action-client-find-next" data-entry="Find Next"></span>Find Next（查找下一个） | `client.find.next` <span hidden>find search next forward match</span> |  <span hidden>默认快捷键：</span>`cmd+g` |
| <span id="action-client-find-previous" data-entry="Find Previous"></span>Find Previous（查找上一个） | `client.find.previous` <span hidden>find search previous back match</span> |  <span hidden>默认快捷键：</span>`shift+cmd+g` |

## 视图

| 操作 | 名称 | 默认快捷键 |
| --- | --- | --- |
| <span id="action-client-font-increase" data-entry="Increase Font Size"></span>Increase Font Size（增大字号） | `client.font.increase` <span hidden>terminal font size larger bigger increase zoom text typography</span> |  <span hidden>默认快捷键：</span>`shift+cmd+=`, `cmd+=` |
| <span id="action-client-font-decrease" data-entry="Decrease Font Size"></span>Decrease Font Size（减小字号） | `client.font.decrease` <span hidden>terminal font size smaller decrease zoom text typography</span> |  <span hidden>默认快捷键：</span>`cmd+-` |
| <span id="action-client-font-reset" data-entry="Reset Font Size"></span>Reset Font Size（重置字号） | `client.font.reset` <span hidden>terminal font size reset default original text typography</span> |  <span hidden>默认快捷键：</span>`cmd+[Digit0]` |
| <span id="action-client-sidebar-toggle" data-entry="Toggle Sidebar"></span>Toggle Sidebar（切换边栏） | `client.sidebar.toggle` <span hidden>sidebar collapse expand fold hide show tabs</span> |  <span hidden>默认快捷键：</span>`cmd+/` |
| <span id="action-client-sidebar-activity-toggle" data-entry="Toggle Activity"></span>Toggle Activity（切换活动） | `client.sidebar.activity.toggle` <span hidden>activity mode view filter working waiting attention programs status sidebar tabs</span> |  <span hidden>默认快捷键：</span>`cmd+.` |
| <span id="action-client-sidebar-activity-by-session" data-entry="Show Activity by Session"></span>Show Activity by Session（按会话显示活动） | `client.sidebar.activity.by_session` <span hidden>activity mode view filter group grouping by session sessions sidebar tabs</span> |  |
| <span id="action-client-sidebar-activity-by-priority" data-entry="Show Activity by Priority"></span>Show Activity by Priority（按优先级显示活动） | `client.sidebar.activity.by_priority` <span hidden>activity mode view filter group grouping by priority blocked failed done working idle sidebar tabs</span> |  |
| <span id="action-client-sidebar-filter-focus" data-entry="Focus Tab Filter"></span>Focus Tab Filter（聚焦标签页过滤器） | `client.sidebar.filter.focus` <span hidden>filter search find type query focus keyboard sidebar activity tabs sessions hosts</span> |  |
| <span id="action-client-tab-style-toggle" data-entry="Toggle Toolbar Layout"></span>Toggle Toolbar Layout（切换工具栏布局） | `client.tab_style.toggle` <span hidden>toolbar layout tab style orientation sidebar horizontal vertical view</span> |  <span hidden>默认快捷键：</span>`shift+cmd+s` |
| <span id="action-client-toolbar-reveal" data-entry="Reveal Toolbar"></span>Reveal Toolbar（显示工具栏） | `client.toolbar.reveal` <span hidden>show reveal peek toolbar tab bar title row hover auto-hide hidden view</span> |  <span hidden>默认快捷键：</span>`alt+cmd+t` |
| <span id="action-client-pane-header-reveal" data-entry="Reveal Pane Header"></span>Reveal Pane Header（显示窗格标题栏） | `client.pane_header.reveal` <span hidden>show reveal peek pane header title hover hidden focused pane view</span> |  <span hidden>默认快捷键：</span>`alt+shift+cmd+t` |
| <span id="action-client-theme-change" data-entry="Change Theme…"></span>Change Theme…（更改主题…） | `client.theme.change` <span hidden>theme colour color scheme palette appearance</span> |  |
| <span id="action-client-theme-import" data-entry="Import Theme File"></span>Import Theme File（导入主题文件） 导入 Ghostty 主题或 iTerm 配色文件并选中它。 | `client.theme.import` <span hidden>theme import ghostty iterm file colour color scheme palette</span> |  |
| <span id="action-client-appearance-switch-mode" data-entry="Switch Appearance Mode"></span>Switch Appearance Mode（切换外观模式） | `client.appearance.switch_mode` <span hidden>appearance mode light dark toggle color scheme</span> |  |
| <span id="action-client-config-copy-path" data-entry="Copy Config File Path"></span>Copy Config File Path（复制配置文件路径） | `client.config.copy_path` <span hidden>config configuration file path copy clipboard init.lua lua keybindings shortcuts settings location where</span> |  |
| <span id="action-client-config-reload" data-entry="Reload Config"></span>Reload Config（重新加载配置） | `client.config.reload` <span hidden>config configuration reload reread apply init.lua lua keybindings shortcuts settings</span> |  |
