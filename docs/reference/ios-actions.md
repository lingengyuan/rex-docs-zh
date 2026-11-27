> 原文：https://www.superlogical.com/rex/docs/reference/ios-actions
> 原文版本：55fff6134a8b（抓取于 2026-11-27）

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
| <span id="action-client-url-open" data-entry="Open URL"></span>Open URL（打开 URL） 使用这台电脑默认用于处理此类链接的应用（例如浏览器）打开 URL。 | `client.url.open` <span hidden>open url link web browser page address http https launch default app</span> |

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
| <span id="action-pane-copy-id" data-entry="Copy Block ID"></span>Copy Block ID（复制块 ID） 将获得焦点的块 ID 复制到剪贴板。 | `pane.copy_id` <span hidden>pane block id identifier copy clipboard target agent capture</span> |
| <span id="action-pane-rename" data-entry="Rename Pane"></span>Rename Pane（重命名窗格） | `pane.rename` <span hidden>rename pane block name title label</span> |
| <span id="action-pane-balance" data-entry="Balance Splits"></span>Balance Splits（均分分栏） | `pane.balance` <span hidden>pane split balance equalize equalise evenly distribute resize layout</span> |
| <span id="action-pane-resize" data-entry="Resize Pane"></span>Resize Pane（调整窗格大小） | `pane.resize` <span hidden>pane resize grow shrink divider wider narrower taller shorter</span> |
| <span id="action-pane-float" data-entry="Float Pane"></span>Float Pane（悬浮窗格） | `pane.float` <span hidden>pane float floating window dock undock detach overlay pop out tile</span> |
| <span id="action-pane-new-floating" data-entry="New Floating Pane"></span>New Floating Pane（新建悬浮窗格） | `pane.new_floating` <span hidden>pane new create open float floating window terminal overlay popup scratchpad</span> |
| <span id="action-pane-minimize-floating" data-entry="Minimize Floating Window"></span>Minimize Floating Window（最小化悬浮窗口） | `pane.minimize_floating` <span hidden>pane floating window hide show toggle minimize minimise restore taskbar capsule stash scratchpad</span> |
| <span id="action-pane-minimize-all-floating" data-entry="Minimize All Floating Windows"></span>Minimize All Floating Windows（最小化所有悬浮窗口） | `pane.minimize_all_floating` <span hidden>pane floating windows all hide show toggle minimize minimise restore taskbar capsule stash scratchpad</span> |
| <span id="action-pane-paste" data-entry="Paste into Pane"></span>Paste into Pane（粘贴至窗格） 将剪贴板内容粘贴到获得焦点的终端中。 | `pane.paste` <span hidden>paste clipboard insert text terminal</span> |
| <span id="action-pane-copy" data-entry="Copy from Pane"></span>Copy from Pane（从窗格复制） 将获得焦点的终端选中内容复制到剪贴板。 | `pane.copy` <span hidden>copy selection clipboard text terminal</span> |
| <span id="action-pane-select-all" data-entry="Select All in Pane"></span>Select All in Pane（全选窗格内容） 选中获得焦点的终端中的所有内容，包含其回滚缓冲区。 | `pane.select_all` <span hidden>select all selection text terminal scrollback</span> |
| <span id="action-pane-send-key" data-entry="Send Key"></span>Send Key（发送按键） 向获得焦点的终端发送一个按键，如同在该终端中按下一样。 | `pane.send_key` <span hidden>send key terminal press chord binding</span> |
| <span id="action-client-prompt-previous" data-entry="Jump to Previous Prompt"></span>Jump to Previous Prompt（跳至上一个提示符） | `client.prompt.previous` <span hidden>jump scroll previous prompt command mark shell integration up back history</span> |
| <span id="action-client-prompt-next" data-entry="Jump to Next Prompt"></span>Jump to Next Prompt（跳至下一个提示符） | `client.prompt.next` <span hidden>jump scroll next prompt command mark shell integration down forward</span> |
| <span id="action-client-scroll-page-up" data-entry="Scroll Page Up"></span>Scroll Page Up（向上翻页） | `client.scroll.page_up` <span hidden>scroll page up back scrollback history</span> |
| <span id="action-client-scroll-page-down" data-entry="Scroll Page Down"></span>Scroll Page Down（向下翻页） | `client.scroll.page_down` <span hidden>scroll page down forward scrollback history</span> |
| <span id="action-client-composer-open" data-entry="Compose Input…"></span>Compose Input…（撰写输入…） | `client.composer.open` <span hidden>compose composer message input prompt attach image photo file upload claude codex</span> |
| <span id="action-pane-insert-photo" data-entry="Insert Photo…"></span>Insert Photo…（插入照片…） 将图库中的照片发送到终端并输入其路径。 | `pane.insert_photo` <span hidden>insert photo image picture library screenshot upload attach send path</span> |
| <span id="action-pane-insert-file" data-entry="Insert File…"></span>Insert File…（插入文件…） 将本设备中的文件发送到终端并输入其路径。 | `pane.insert_file` <span hidden>insert file document files finder upload attach send path</span> |
| <span id="action-pane-go-to" data-entry="Go to Anything…"></span>Go to Anything…（前往任意位置…） | `pane.go_to` <span hidden>go to anything pane block tab session agent jump switch navigate find search tree overview</span> |
| <span id="action-pane-view-activity" data-entry="View Activity…"></span>View Activity…（查看活动…） | `pane.view_activity` <span hidden>view activity active working blocked failed done agents programs status priority</span> |

## 设置

| 操作 | 名称 |
| --- | --- |
| <span id="action-client-setting-interface-appearance-scheme" data-entry="Color Scheme"></span>Color Scheme（配色方案） 跟随系统外观，或始终使用浅色或深色。 | `client.setting.interface.appearance.scheme` <span hidden>appearance light dark auto automatic system night mode colour setting preference</span> |
| <span id="action-client-setting-interface-appearance-tint" data-entry="Tint with Theme"></span>Tint with Theme（使用主题着色） 将所选主题的颜色应用到界面表面。 | `client.setting.interface.appearance.tint` <span hidden>tint theme colors colours palette themed blend use theme interface surfaces setting preference</span> |
| <span id="action-client-setting-interface-active-panes-active-border" data-entry="Highlight Active Pane Edges"></span>Highlight Active Pane Edges（高亮活动窗格边框） 高亮显示获得焦点的窗格边缘。 | `client.setting.interface.active_panes.active_border` <span hidden>border outline focus ring active focused pane highlight edge indicator setting preference</span> |
| <span id="action-client-setting-interface-active-panes-active-border-color" data-entry="Active Pane Highlight Color"></span>Active Pane Highlight Color（活动窗格高亮颜色） 选择活动窗格高亮的颜色。 | `client.setting.interface.active_panes.active_border_color` <span hidden>accent theme terminal text foreground border color focus ring swatch palette red blue green yellow cyan magenta setting preference</span> |
| <span id="action-client-setting-interface-active-panes-active-border-opacity" data-entry="Active Pane Highlight Opacity"></span>Active Pane Highlight Opacity（活动窗格高亮不透明度） 设置活动窗格高亮的显示强度。 | `client.setting.interface.active_panes.active_border_opacity` <span hidden>opacity transparency alpha faint subtle strength border focus ring highlight setting preference</span> |
| <span id="action-client-setting-interface-active-panes-active-border-animation" data-entry="Animate Active Pane Highlight"></span>Animate Active Pane Highlight（活动窗格高亮动画） 以淡入淡出或移动的方式将高亮切换到新聚焦的窗格，或立即切换。 | `client.setting.interface.active_panes.active_border_animation` <span hidden>fade move crossfade glide slide animation transition border focus instant off setting preference</span> |
| <span id="action-client-setting-interface-splits-focus-autobalance" data-entry="Autobalance Splits"></span>Autobalance Splits（自动平衡分屏） 当窗格打开或关闭时，平均调整标签页中各窗格的大小。 | `client.setting.interface.splits_focus.autobalance` <span hidden>balance panes equalize even equal size new close split resize divider setting preference</span> |
| <span id="action-client-setting-interface-animation-style" data-entry="Animation Style"></span>Animation Style（动画样式） 选择窗格移动、打开和关闭时的动画效果。 | `client.setting.interface.animation.style` <span hidden>snappy natural off spring bounce motion disable animations instant speed pane split sidebar setting preference</span> |
| <span id="action-client-setting-themes-light-palette" data-entry="Light Theme"></span>Light Theme（浅色主题） 选择浅色外观下使用的主题。 | `client.setting.themes.light.palette` <span hidden>light mode theme day bright colors colour scheme palette setting preference</span> |
| <span id="action-client-setting-themes-dark-palette" data-entry="Dark Theme"></span>Dark Theme（深色主题） 选择深色外观下使用的主题。 | `client.setting.themes.dark.palette` <span hidden>dark mode theme night dim colors colour scheme palette setting preference</span> |
| <span id="action-client-setting-terminal-typography-font" data-entry="Terminal Font"></span>Terminal Font（终端字体） 选择终端使用的字体。 | `client.setting.terminal.typography.font` <span hidden>font family typeface monospace menlo typography setting preference</span> |
| <span id="action-client-setting-terminal-typography-size" data-entry="Terminal Font Size"></span>Terminal Font Size（终端字号） 设置终端文本的初始字号。 | `client.setting.terminal.typography.size` <span hidden>font size text size larger smaller points pt typography default setting preference</span> |
| <span id="action-client-setting-terminal-colors-contrast" data-entry="Improve Text Contrast"></span>Improve Text Contrast（增强文本对比度） 调整低对比度文本与背景之间的对比效果。 | `client.setting.terminal.colors.contrast` <span hidden>minimum contrast legibility accessibility unreadable faint pale ansi truecolor setting preference</span> |
| <span id="action-client-setting-terminal-colors-palette" data-entry="Force Theme Palette for Text"></span>Force Theme Palette for Text（强制文本使用主题调色板） 将 RGB 和扩展文本颜色映射到最接近的主题颜色。 | `client.setting.terminal.colors.palette` <span hidden>force theme colors colours remap match palette ansi rgb truecolor 256 extended setting preference</span> |
| <span id="action-client-setting-terminal-cursor-blink" data-entry="Cursor Blink Speed"></span>Cursor Blink Speed（光标闪烁速度） 选择光标闪烁的快慢。 | `client.setting.terminal.cursor.blink` <span hidden>blink flashing steady slow fast normal off custom cursor caret setting preference</span> |
| <span id="action-client-setting-terminal-cursor-style" data-entry="Cursor Style"></span>Cursor Style（光标样式） 选择块状、竖线或下划线光标。 | `client.setting.terminal.cursor.style` <span hidden>cursor shape beam caret block bar underline setting preference</span> |
| <span id="action-client-setting-terminal-cursor-force" data-entry="Force Cursor Style"></span>Force Cursor Style（强制光标样式） 忽略程序更改光标形状的请求。 | `client.setting.terminal.cursor.force` <span hidden>override application ignore cursor shape requests setting preference</span> |
| <span id="action-client-setting-terminal-cursor-shaders" data-entry="Cursor Shaders"></span>Cursor Shaders（光标着色器） 在终端光标移动后方绘制拖尾着色器效果。 | `client.setting.terminal.cursor.shaders` <span hidden>cursor trail effect animation smear glow ghostty shader custom-shader shadertoy setting preference</span> |
| <span id="action-client-setting-terminal-cursor-shader" data-entry="Cursor Shader"></span>Cursor Shader（光标着色器样式） 选择光标着色器绘制的效果。 | `client.setting.terminal.cursor.shader` <span hidden>cursor shader trail style effect warp sweep comet blaze tapered rainbow gradient frozen setting preference</span> |
| <span id="action-client-setting-terminal-scrolling-smooth" data-entry="Smooth Scrolling"></span>Smooth Scrolling（平滑滚动） 按像素而非整行滚动终端历史记录。 | `client.setting.terminal.scrolling.smooth` <span hidden>smooth pixel precise fluid momentum inertia trackpad line by line scroll history setting preference</span> |
| <span id="action-client-setting-terminal-resizing-smooth" data-entry="Smooth Terminal Resizing"></span>Smooth Terminal Resizing（平滑调整终端大小） 在窗格大小变化的那一帧立即重排终端文本。 | `client.setting.terminal.resizing.smooth` <span hidden>smooth resize reflow jitter glitch jump flicker live resize rewrap setting preference</span> |
| <span id="action-client-setting-terminal-titles-prefer-generated" data-entry="Prefer Generated Titles"></span>Prefer Generated Titles（优先使用生成的标题） 以正在运行的程序名称命名标签页，而非使用 Shell 设置的标题。 | `client.setting.terminal.titles.prefer_generated` <span hidden>shell title generated program process name directory ignore shell titles tab pane setting preference</span> |
| <span id="action-client-setting-developer-mode-enabled" data-entry="Developer Mode"></span>Developer Mode（开发者模式） 显示用于开发与调试的设置项。 | `client.setting.developer.mode.enabled` <span hidden>developer advanced development debugging enable tools setting preference</span> |
