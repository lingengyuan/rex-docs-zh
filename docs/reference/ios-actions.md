> 原文：https://www.superlogical.com/rex/docs/reference/ios-actions
> 原文版本：40530b92ff13（抓取于 2026-11-15）

# iOS 操作

本页列出 Rex for iOS 命令面板中的所有操作。可以使用操作名称并通过 `rex do` 运行。

<div class="reference-page actions" hidden></div>

## 窗口

| 操作 | 名称 |
| --- | --- |
| <span id="action-client-window-new" data-entry="New Window"></span>New Window（新建窗口） | `client.window.new` <span hidden>create workspace window</span> |
| <span id="action-client-window-close" data-entry="Close Window"></span>Close Window（关闭窗口） | `client.window.close` <span hidden>close workspace window</span> |
| <span id="action-client-close" data-entry="Close"></span>Close（关闭） 关闭获得焦点的窗格；若无窗格则关闭选中的标签页；若无标签页则关闭窗口。 | `client.close` <span hidden>close pane tab window focused</span> |

## 应用

| 操作 | 名称 |
| --- | --- |
| <span id="action-client-settings" data-entry="Settings…"></span>Settings…（设置…） | `client.settings` <span hidden>preferences settings options configure</span> |
| <span id="action-client-palette-toggle" data-entry="Command Palette…"></span>Command Palette…（命令面板…） | `client.palette.toggle` <span hidden>command palette search commands actions</span> |
| <span id="action-client-version-copy" data-entry="Copy Version Info"></span>Copy Version Info（复制版本信息） 将应用和服务端版本复制到剪贴板。 | `client.version.copy` <span hidden>version build number copy clipboard about app server release</span> |
| <span id="action-client-debug-copy" data-entry="Copy Debug Info"></span>Copy Debug Info（复制调试信息） 将应用、系统、服务端和主机状态报告复制到剪贴板。 | `client.debug.copy` <span hidden>debug debugging info report copy clipboard diagnostics troubleshoot support bug commit build environment</span> |
| <span id="action-client-diagnostics" data-entry="Rex Diagnostics"></span>Rex Diagnostics（Rex 诊断） | `client.diagnostics` <span hidden>diagnostics logs debug troubleshoot server report</span> |
| <span id="action-client-agents-setup" data-entry="Install Rex for Agents"></span>Install Rex for Agents（为智能体安装 Rex） 为 Claude Code、Codex 及其他智能体安装 Rex skill 与 hook。 | `client.agents.setup` <span hidden>`rex skill` install agent agents coding ai claude code codex cursor copilot gemini hook hooks setup</span> |

## 视图

| 操作 | 名称 |
| --- | --- |
| <span id="action-client-sidebar-toggle" data-entry="Toggle Sidebar"></span>Toggle Sidebar（切换边栏） | `client.sidebar.toggle` <span hidden>sidebar collapse expand fold hide show tabs</span> |
| <span id="action-client-sidebar-activity-toggle" data-entry="Toggle Activity"></span>Toggle Activity（切换活动） | `client.sidebar.activity.toggle` <span hidden>activity mode view filter working waiting attention programs status sidebar tabs</span> |
| <span id="action-client-config-copy-path" data-entry="Copy Config File Path"></span>Copy Config File Path（复制配置文件路径） | `client.config.copy_path` <span hidden>config configuration file path copy clipboard init.lua lua keybindings shortcuts settings location where</span> |
| <span id="action-client-font-increase" data-entry="Increase Font Size"></span>Increase Font Size（增大字号） | `client.font.increase` <span hidden>terminal font size larger bigger increase zoom text typography</span> |
| <span id="action-client-font-decrease" data-entry="Decrease Font Size"></span>Decrease Font Size（减小字号） | `client.font.decrease` <span hidden>terminal font size smaller decrease zoom text typography</span> |
| <span id="action-client-font-reset" data-entry="Reset Font Size"></span>Reset Font Size（重置字号） | `client.font.reset` <span hidden>terminal font size reset default original text typography</span> |
| <span id="action-client-theme-change" data-entry="Change Theme…"></span>Change Theme…（更改主题…） | `client.theme.change` <span hidden>theme colour color scheme palette appearance</span> |
| <span id="action-client-appearance-switch-mode" data-entry="Switch Appearance Mode"></span>Switch Appearance Mode（切换外观模式） | `client.appearance.switch_mode` <span hidden>appearance mode light dark toggle color scheme</span> |
| <span id="action-client-sidebar-filter-focus" data-entry="Focus Tab Filter"></span>Focus Tab Filter（聚焦标签页过滤器） | `client.sidebar.filter.focus` <span hidden>filter search find type query focus keyboard sidebar activity tabs sessions hosts</span> |
| <span id="action-client-keyboard-show" data-entry="Show Keyboard"></span>Show Keyboard（显示键盘） | `client.keyboard.show` <span hidden>keyboard show open type input</span> |
| <span id="action-client-keyboard-hide" data-entry="Hide Keyboard"></span>Hide Keyboard（隐藏键盘） | `client.keyboard.hide` <span hidden>keyboard hide close dismiss</span> |

## 会话

| 操作 | 名称 |
| --- | --- |
| <span id="action-session-new" data-entry="New Session"></span>New Session（新建会话） | `session.new` <span hidden>create session add</span> |
| <span id="action-session-select" data-entry="Go to Session"></span>Go to Session（前往会话） | `session.select` <span hidden>session select show jump go identifier id</span> |
| <span id="action-session-next" data-entry="Next Session"></span>Next Session（下一个会话） | `session.next` <span hidden>cycle session forward</span> |
| <span id="action-session-previous" data-entry="Previous Session"></span>Previous Session（上一个会话） | `session.previous` <span hidden>cycle session back</span> |
| <span id="action-session-rename" data-entry="Rename Session"></span>Rename Session（重命名会话） | `session.rename` <span hidden>rename session name title</span> |
| <span id="action-session-close" data-entry="Close Session"></span>Close Session（关闭会话） | `session.close` <span hidden>close kill destroy delete session</span> |
| <span id="action-session-refresh" data-entry="Refresh Sessions"></span>Refresh Sessions（刷新会话） | `session.refresh` <span hidden>reload sync sessions</span> |
| <span id="action-session-switch" data-entry="Change Session…"></span>Change Session…（切换会话…） | `session.switch` <span hidden>session switch jump go</span> |

## 主机

| 操作 | 名称 |
| --- | --- |
| <span id="action-client-host-add" data-entry="Add Remote Host…"></span>Add Remote Host…（添加远程主机…） | `client.host.add` <span hidden>host remote add server machine url http https connect</span> |
| <span id="action-client-host-remove" data-entry="Remove Host…"></span>Remove Host…（移除主机…） | `client.host.remove` <span hidden>remove forget delete disconnect host remote server machine</span> |
| <span id="action-client-host-forward-port" data-entry="Forward Port…"></span>Forward Port…（端口转发…） | `client.host.forward_port` <span hidden>port forward forwarding tunnel localhost open browser ssh `-L` local remote host</span> |

## 标签页

| 操作 | 名称 |
| --- | --- |
| <span id="action-client-tab-new" data-entry="New Tab"></span>New Tab（新建标签页） | `client.tab.new` <span hidden>create tab window add</span> |
| <span id="action-client-tab-previous" data-entry="Show Previous Tab"></span>Show Previous Tab（显示上一个标签页） | `client.tab.previous` <span hidden>cycle tab window back</span> |
| <span id="action-client-tab-next" data-entry="Show Next Tab"></span>Show Next Tab（显示下一个标签页） | `client.tab.next` <span hidden>cycle tab window forward</span> |
| <span id="action-client-tab-goto" data-entry="Go to Tab"></span>Go to Tab（前往标签页） | `client.tab.goto` <span hidden>tab window select number index jump go</span> |
| <span id="action-client-tab-move-backward" data-entry="Move Tab Backward"></span>Move Tab Backward（向后移动标签页） | `client.tab.move.backward` <span hidden>move tab window reorder left up earlier</span> |
| <span id="action-client-tab-move-forward" data-entry="Move Tab Forward"></span>Move Tab Forward（向前移动标签页） | `client.tab.move.forward` <span hidden>move tab window reorder right down later</span> |
| <span id="action-client-tab-rename" data-entry="Rename Tab"></span>Rename Tab（重命名标签页） | `client.tab.rename` <span hidden>rename tab window name title</span> |
| <span id="action-client-tab-close" data-entry="Close Tab"></span>Close Tab（关闭标签页） | `client.tab.close` <span hidden>close tab window</span> |
| <span id="action-client-tab-close-others" data-entry="Close Other Tabs"></span>Close Other Tabs（关闭其他标签页） | `client.tab.close_others` <span hidden>close other tabs windows kill only keep</span> |
| <span id="action-client-tab-move" data-entry="Move Tab"></span>Move Tab（移动标签页） | `client.tab.move` <span hidden>move tab window reorder</span> |
| <span id="action-client-tab-move-to-new-window" data-entry="Move Tab to New Window"></span>Move Tab to New Window（移动标签页至新窗口） | `client.tab.move_to_new_window` <span hidden>move tab new window tear off detach separate pop out own</span> |

## 窗格

| 操作 | 名称 |
| --- | --- |
| <span id="action-pane-split-left" data-entry="Split Pane Left"></span>Split Pane Left（向左拆分窗格） | `pane.split.left` <span hidden>pane split terminal divide new left</span> |
| <span id="action-pane-split-right" data-entry="Split Pane Right"></span>Split Pane Right（向右拆分窗格） | `pane.split.right` <span hidden>pane split terminal divide new right</span> |
| <span id="action-pane-split-up" data-entry="Split Pane Up"></span>Split Pane Up（向上拆分窗格） | `pane.split.up` <span hidden>pane split terminal divide new above up</span> |
| <span id="action-pane-split-down" data-entry="Split Pane Down"></span>Split Pane Down（向下拆分窗格） | `pane.split.down` <span hidden>pane split terminal divide new below down</span> |
| <span id="action-pane-focus-previous" data-entry="Focus Previous Pane"></span>Focus Previous Pane（聚焦上一个窗格） | `pane.focus_previous` <span hidden>pane focus previous back</span> |
| <span id="action-pane-focus-next" data-entry="Focus Next Pane"></span>Focus Next Pane（聚焦下一个窗格） | `pane.focus_next` <span hidden>pane focus next forward</span> |
| <span id="action-pane-focus-left" data-entry="Focus Pane Left"></span>Focus Pane Left（聚焦左侧窗格） | `pane.focus.left` <span hidden>pane focus navigate left</span> |
| <span id="action-pane-focus-right" data-entry="Focus Pane Right"></span>Focus Pane Right（聚焦右侧窗格） | `pane.focus.right` <span hidden>pane focus navigate right</span> |
| <span id="action-pane-focus-up" data-entry="Focus Pane Up"></span>Focus Pane Up（聚焦上方窗格） | `pane.focus.up` <span hidden>pane focus navigate up above</span> |
| <span id="action-pane-focus-down" data-entry="Focus Pane Down"></span>Focus Pane Down（聚焦下方窗格） | `pane.focus.down` <span hidden>pane focus navigate down below</span> |
| <span id="action-pane-move-left" data-entry="Move Pane Left"></span>Move Pane Left（向左移动窗格） | `pane.move.left` <span hidden>pane move swap rearrange left</span> |
| <span id="action-pane-move-right" data-entry="Move Pane Right"></span>Move Pane Right（向右移动窗格） | `pane.move.right` <span hidden>pane move swap rearrange right</span> |
| <span id="action-pane-move-up" data-entry="Move Pane Up"></span>Move Pane Up（向上移动窗格） | `pane.move.up` <span hidden>pane move swap rearrange up above</span> |
| <span id="action-pane-move-down" data-entry="Move Pane Down"></span>Move Pane Down（向下移动窗格） | `pane.move.down` <span hidden>pane move swap rearrange down below</span> |
| <span id="action-pane-zoom" data-entry="Zoom Pane"></span>Zoom Pane（缩放/最大化窗格） | `pane.zoom` <span hidden>pane zoom maximize restore terminal</span> |
| <span id="action-pane-move-to-new-tab" data-entry="Move Pane to New Tab"></span>Move Pane to New Tab（移动窗格至新标签页） | `pane.move_to_new_tab` <span hidden>pane block move new window tab detach split</span> |
| <span id="action-pane-close" data-entry="Close Pane"></span>Close Pane（关闭窗格） | `pane.close` <span hidden>pane close remove terminal</span> |
| <span id="action-pane-split" data-entry="Split Pane"></span>Split Pane（拆分窗格） | `pane.split` <span hidden>pane split terminal divide new</span> |
| <span id="action-pane-split-auto" data-entry="Split Pane Best Fit"></span>Split Pane Best Fit（自适应拆分窗格） | `pane.split.auto` <span hidden>pane split terminal divide new automatic best fit</span> |
| <span id="action-pane-close-others" data-entry="Close Other Panes"></span>Close Other Panes（关闭其他窗格） | `pane.close_others` <span hidden>close other panes kill only keep focused</span> |
| <span id="action-pane-move-to-tab" data-entry="Move Pane to Tab…"></span>Move Pane to Tab…（移动窗格至标签页…） | `pane.move_to_tab` <span hidden>pane block move tab window send other existing join</span> |
| <span id="action-pane-go-to-directory" data-entry="Go to Directory…"></span>Go to Directory…（前往目录…） | `pane.go_to_directory` <span hidden>go to directory folder path cd new tab open navigate</span> |
| <span id="action-pane-insert-path" data-entry="Insert Path…"></span>Insert Path…（插入路径…） | `pane.insert_path` <span hidden>insert path file folder directory cursor type paste complete browse</span> |
| <span id="action-pane-copy-id" data-entry="Copy Pane ID"></span>Copy Pane ID（复制窗格 ID） 将获得焦点的窗格块 ID 复制到剪贴板。 | `pane.copy_id` <span hidden>pane block id identifier copy clipboard target agent capture</span> |
| <span id="action-pane-rename" data-entry="Rename Pane"></span>Rename Pane（重命名窗格） | `pane.rename` <span hidden>rename pane block name title label</span> |
| <span id="action-pane-balance" data-entry="Balance Splits"></span>Balance Splits（均分分栏） | `pane.balance` <span hidden>pane split balance equalize equalise evenly distribute resize layout</span> |
| <span id="action-pane-resize" data-entry="Resize Pane"></span>Resize Pane（调整窗格大小） | `pane.resize` <span hidden>pane resize grow shrink divider wider narrower taller shorter</span> |
| <span id="action-pane-float" data-entry="Float Pane"></span>Float Pane（悬浮窗格） | `pane.float` <span hidden>pane float floating window dock undock detach overlay pop out tile</span> |
| <span id="action-pane-new-floating" data-entry="New Floating Pane"></span>New Floating Pane（新建悬浮窗格） | `pane.new_floating` <span hidden>pane new create open float floating window terminal overlay popup scratchpad</span> |
| <span id="action-pane-minimize-floating" data-entry="Minimize Floating Window"></span>Minimize Floating Window（最小化悬浮窗口） | `pane.minimize_floating` <span hidden>pane floating window hide show toggle minimize minimise restore taskbar capsule stash scratchpad</span> |
| <span id="action-pane-minimize-all-floating" data-entry="Minimize Floating Windows"></span>Minimize Floating Windows（最小化所有悬浮窗口） | `pane.minimize_all_floating` <span hidden>pane floating windows all hide show toggle minimize minimise restore taskbar capsule stash scratchpad</span> |
| <span id="action-pane-paste" data-entry="Paste into Pane"></span>Paste into Pane（粘贴至窗格） 将剪贴板内容粘贴到获得焦点的终端中。 | `pane.paste` <span hidden>paste clipboard insert text terminal</span> |
| <span id="action-pane-copy" data-entry="Copy from Pane"></span>Copy from Pane（从窗格复制） 将获得焦点的终端选中内容复制到剪贴板。 | `pane.copy` <span hidden>copy selection clipboard text terminal</span> |
| <span id="action-pane-select-all" data-entry="Select All in Pane"></span>Select All in Pane（全选窗格内容） 选中获得焦点的终端中的所有内容，包含其回滚缓冲区。 | `pane.select_all` <span hidden>select all selection text terminal scrollback</span> |
| <span id="action-pane-send-key" data-entry="Send Key"></span>Send Key（发送按键） 向获得焦点的终端发送一个按键，如同在该终端中按下一样。 | `pane.send_key` <span hidden>send key terminal press chord binding</span> |
| <span id="action-client-prompt-previous" data-entry="Jump to Previous Prompt"></span>Jump to Previous Prompt（跳至上一个提示符） | `client.prompt.previous` <span hidden>jump scroll previous prompt command mark shell integration up back history</span> |
| <span id="action-client-prompt-next" data-entry="Jump to Next Prompt"></span>Jump to Next Prompt（跳至下一个提示符） | `client.prompt.next` <span hidden>jump scroll next prompt command mark shell integration down forward</span> |
| <span id="action-client-scroll-page-up" data-entry="Scroll Page Up"></span>Scroll Page Up（向上翻页） | `client.scroll.page_up` <span hidden>scroll page up back scrollback history</span> |
| <span id="action-client-scroll-page-down" data-entry="Scroll Page Down"></span>Scroll Page Down（向下翻页） | `client.scroll.page_down` <span hidden>scroll page down forward scrollback history</span> |
| <span id="action-pane-go-to" data-entry="Go to Anything…"></span>Go to Anything…（前往任意位置…） | `pane.go_to` <span hidden>go to anything pane block tab session agent jump switch navigate find search tree overview</span> |
| <span id="action-pane-view-activity" data-entry="View Activity…"></span>View Activity…（查看活动…） | `pane.view_activity` <span hidden>view activity active working blocked failed done agents programs status priority</span> |
