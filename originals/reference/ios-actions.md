---
title: "iOS Actions"
canonical_url: https://www.superlogical.com/rex/docs/reference/ios-actions
---

# iOS Actions

This page lists every action in the Rex for iOS command palette. Use the name to run it with `rex do`.

<div class="reference-page actions" hidden></div>

## Window

| Action | Name |
| --- | --- |
| <span id="action-client-window-new" data-entry="New Window"></span>New Window | `client.window.new` <span hidden>create workspace window</span> |
| <span id="action-client-window-close" data-entry="Close Window"></span>Close Window | `client.window.close` <span hidden>close workspace window</span> |
| <span id="action-client-close" data-entry="Close"></span>Close Closes the focused pane, else the selected tab, else the window. | `client.close` <span hidden>close pane tab window focused</span> |

## App

| Action | Name |
| --- | --- |
| <span id="action-client-settings" data-entry="Settings…"></span>Settings… | `client.settings` <span hidden>preferences settings options configure</span> |
| <span id="action-client-palette-toggle" data-entry="Command Palette…"></span>Command Palette… | `client.palette.toggle` <span hidden>command palette search commands actions</span> |
| <span id="action-client-version-copy" data-entry="Copy Version Info"></span>Copy Version Info Copies the app and server versions to the clipboard. | `client.version.copy` <span hidden>version build number copy clipboard about app server release</span> |
| <span id="action-client-debug-copy" data-entry="Copy Debug Info"></span>Copy Debug Info Copies a report of the app, system, server, and host state to the clipboard. | `client.debug.copy` <span hidden>debug debugging info report copy clipboard diagnostics troubleshoot support bug commit build environment</span> |
| <span id="action-client-diagnostics" data-entry="Rex Diagnostics"></span>Rex Diagnostics | `client.diagnostics` <span hidden>diagnostics logs debug troubleshoot server report</span> |
| <span id="action-client-agents-setup" data-entry="Install Rex for Agents"></span>Install Rex for Agents Installs the Rex skill and hooks for Claude Code, Codex, and other agents. | `client.agents.setup` <span hidden>`rex skill` install agent agents coding ai claude code codex cursor copilot gemini hook hooks setup</span> |

## View

| Action | Name |
| --- | --- |
| <span id="action-client-sidebar-toggle" data-entry="Toggle Sidebar"></span>Toggle Sidebar | `client.sidebar.toggle` <span hidden>sidebar collapse expand fold hide show tabs</span> |
| <span id="action-client-sidebar-activity-toggle" data-entry="Toggle Activity"></span>Toggle Activity | `client.sidebar.activity.toggle` <span hidden>activity mode view filter working waiting attention programs status sidebar tabs</span> |
| <span id="action-client-config-copy-path" data-entry="Copy Config File Path"></span>Copy Config File Path | `client.config.copy_path` <span hidden>config configuration file path copy clipboard init.lua lua keybindings shortcuts settings location where</span> |
| <span id="action-client-font-increase" data-entry="Increase Font Size"></span>Increase Font Size | `client.font.increase` <span hidden>terminal font size larger bigger increase zoom text typography</span> |
| <span id="action-client-font-decrease" data-entry="Decrease Font Size"></span>Decrease Font Size | `client.font.decrease` <span hidden>terminal font size smaller decrease zoom text typography</span> |
| <span id="action-client-font-reset" data-entry="Reset Font Size"></span>Reset Font Size | `client.font.reset` <span hidden>terminal font size reset default original text typography</span> |
| <span id="action-client-theme-change" data-entry="Change Theme…"></span>Change Theme… | `client.theme.change` <span hidden>theme colour color scheme palette appearance</span> |
| <span id="action-client-appearance-switch-mode" data-entry="Switch Appearance Mode"></span>Switch Appearance Mode | `client.appearance.switch_mode` <span hidden>appearance mode light dark toggle color scheme</span> |
| <span id="action-client-sidebar-filter-focus" data-entry="Focus Tab Filter"></span>Focus Tab Filter | `client.sidebar.filter.focus` <span hidden>filter search find type query focus keyboard sidebar activity tabs sessions hosts</span> |
| <span id="action-client-keyboard-show" data-entry="Show Keyboard"></span>Show Keyboard | `client.keyboard.show` <span hidden>keyboard show open type input</span> |
| <span id="action-client-keyboard-hide" data-entry="Hide Keyboard"></span>Hide Keyboard | `client.keyboard.hide` <span hidden>keyboard hide close dismiss</span> |

## Session

| Action | Name |
| --- | --- |
| <span id="action-session-new" data-entry="New Session"></span>New Session | `session.new` <span hidden>create session add</span> |
| <span id="action-session-select" data-entry="Go to Session"></span>Go to Session | `session.select` <span hidden>session select show jump go identifier id</span> |
| <span id="action-session-next" data-entry="Next Session"></span>Next Session | `session.next` <span hidden>cycle session forward</span> |
| <span id="action-session-previous" data-entry="Previous Session"></span>Previous Session | `session.previous` <span hidden>cycle session back</span> |
| <span id="action-session-rename" data-entry="Rename Session"></span>Rename Session | `session.rename` <span hidden>rename session name title</span> |
| <span id="action-session-close" data-entry="Close Session"></span>Close Session | `session.close` <span hidden>close kill destroy delete session</span> |
| <span id="action-session-refresh" data-entry="Refresh Sessions"></span>Refresh Sessions | `session.refresh` <span hidden>reload sync sessions</span> |
| <span id="action-session-switch" data-entry="Change Session…"></span>Change Session… | `session.switch` <span hidden>session switch jump go</span> |

## Host

| Action | Name |
| --- | --- |
| <span id="action-client-host-add" data-entry="Add Remote Host…"></span>Add Remote Host… | `client.host.add` <span hidden>host remote add server machine url http https connect</span> |
| <span id="action-client-host-remove" data-entry="Remove Host…"></span>Remove Host… | `client.host.remove` <span hidden>remove forget delete disconnect host remote server machine</span> |
| <span id="action-client-host-forward-port" data-entry="Forward Port…"></span>Forward Port… | `client.host.forward_port` <span hidden>port forward forwarding tunnel localhost open browser ssh `-L` local remote host</span> |

## Tab

| Action | Name |
| --- | --- |
| <span id="action-client-tab-new" data-entry="New Tab"></span>New Tab | `client.tab.new` <span hidden>create tab window add</span> |
| <span id="action-client-tab-previous" data-entry="Show Previous Tab"></span>Show Previous Tab | `client.tab.previous` <span hidden>cycle tab window back</span> |
| <span id="action-client-tab-next" data-entry="Show Next Tab"></span>Show Next Tab | `client.tab.next` <span hidden>cycle tab window forward</span> |
| <span id="action-client-tab-goto" data-entry="Go to Tab"></span>Go to Tab | `client.tab.goto` <span hidden>tab window select number index jump go</span> |
| <span id="action-client-tab-move-backward" data-entry="Move Tab Backward"></span>Move Tab Backward | `client.tab.move.backward` <span hidden>move tab window reorder left up earlier</span> |
| <span id="action-client-tab-move-forward" data-entry="Move Tab Forward"></span>Move Tab Forward | `client.tab.move.forward` <span hidden>move tab window reorder right down later</span> |
| <span id="action-client-tab-rename" data-entry="Rename Tab"></span>Rename Tab | `client.tab.rename` <span hidden>rename tab window name title</span> |
| <span id="action-client-tab-close" data-entry="Close Tab"></span>Close Tab | `client.tab.close` <span hidden>close tab window</span> |
| <span id="action-client-tab-close-others" data-entry="Close Other Tabs"></span>Close Other Tabs | `client.tab.close_others` <span hidden>close other tabs windows kill only keep</span> |
| <span id="action-client-tab-move" data-entry="Move Tab"></span>Move Tab | `client.tab.move` <span hidden>move tab window reorder</span> |
| <span id="action-client-tab-move-to-new-window" data-entry="Move Tab to New Window"></span>Move Tab to New Window | `client.tab.move_to_new_window` <span hidden>move tab new window tear off detach separate pop out own</span> |

## Pane

| Action | Name |
| --- | --- |
| <span id="action-pane-split-left" data-entry="Split Pane Left"></span>Split Pane Left | `pane.split.left` <span hidden>pane split terminal divide new left</span> |
| <span id="action-pane-split-right" data-entry="Split Pane Right"></span>Split Pane Right | `pane.split.right` <span hidden>pane split terminal divide new right</span> |
| <span id="action-pane-split-up" data-entry="Split Pane Up"></span>Split Pane Up | `pane.split.up` <span hidden>pane split terminal divide new above up</span> |
| <span id="action-pane-split-down" data-entry="Split Pane Down"></span>Split Pane Down | `pane.split.down` <span hidden>pane split terminal divide new below down</span> |
| <span id="action-pane-focus-previous" data-entry="Focus Previous Pane"></span>Focus Previous Pane | `pane.focus_previous` <span hidden>pane focus previous back</span> |
| <span id="action-pane-focus-next" data-entry="Focus Next Pane"></span>Focus Next Pane | `pane.focus_next` <span hidden>pane focus next forward</span> |
| <span id="action-pane-focus-left" data-entry="Focus Pane Left"></span>Focus Pane Left | `pane.focus.left` <span hidden>pane focus navigate left</span> |
| <span id="action-pane-focus-right" data-entry="Focus Pane Right"></span>Focus Pane Right | `pane.focus.right` <span hidden>pane focus navigate right</span> |
| <span id="action-pane-focus-up" data-entry="Focus Pane Up"></span>Focus Pane Up | `pane.focus.up` <span hidden>pane focus navigate up above</span> |
| <span id="action-pane-focus-down" data-entry="Focus Pane Down"></span>Focus Pane Down | `pane.focus.down` <span hidden>pane focus navigate down below</span> |
| <span id="action-pane-move-left" data-entry="Move Pane Left"></span>Move Pane Left | `pane.move.left` <span hidden>pane move swap rearrange left</span> |
| <span id="action-pane-move-right" data-entry="Move Pane Right"></span>Move Pane Right | `pane.move.right` <span hidden>pane move swap rearrange right</span> |
| <span id="action-pane-move-up" data-entry="Move Pane Up"></span>Move Pane Up | `pane.move.up` <span hidden>pane move swap rearrange up above</span> |
| <span id="action-pane-move-down" data-entry="Move Pane Down"></span>Move Pane Down | `pane.move.down` <span hidden>pane move swap rearrange down below</span> |
| <span id="action-pane-zoom" data-entry="Zoom Pane"></span>Zoom Pane | `pane.zoom` <span hidden>pane zoom maximize restore terminal</span> |
| <span id="action-pane-move-to-new-tab" data-entry="Move Pane to New Tab"></span>Move Pane to New Tab | `pane.move_to_new_tab` <span hidden>pane block move new window tab detach split</span> |
| <span id="action-pane-close" data-entry="Close Pane"></span>Close Pane | `pane.close` <span hidden>pane close remove terminal</span> |
| <span id="action-pane-split" data-entry="Split Pane"></span>Split Pane | `pane.split` <span hidden>pane split terminal divide new</span> |
| <span id="action-pane-split-auto" data-entry="Split Pane Best Fit"></span>Split Pane Best Fit | `pane.split.auto` <span hidden>pane split terminal divide new automatic best fit</span> |
| <span id="action-pane-close-others" data-entry="Close Other Panes"></span>Close Other Panes | `pane.close_others` <span hidden>close other panes kill only keep focused</span> |
| <span id="action-pane-move-to-tab" data-entry="Move Pane to Tab…"></span>Move Pane to Tab… | `pane.move_to_tab` <span hidden>pane block move tab window send other existing join</span> |
| <span id="action-pane-go-to-directory" data-entry="Go to Directory…"></span>Go to Directory… | `pane.go_to_directory` <span hidden>go to directory folder path cd new tab open navigate</span> |
| <span id="action-pane-insert-path" data-entry="Insert Path…"></span>Insert Path… | `pane.insert_path` <span hidden>insert path file folder directory cursor type paste complete browse</span> |
| <span id="action-pane-copy-id" data-entry="Copy Block ID"></span>Copy Block ID Copies the focused block's ID to the clipboard. | `pane.copy_id` <span hidden>pane block id identifier copy clipboard target agent capture</span> |
| <span id="action-pane-rename" data-entry="Rename Pane"></span>Rename Pane | `pane.rename` <span hidden>rename pane block name title label</span> |
| <span id="action-pane-balance" data-entry="Balance Splits"></span>Balance Splits | `pane.balance` <span hidden>pane split balance equalize equalise evenly distribute resize layout</span> |
| <span id="action-pane-resize" data-entry="Resize Pane"></span>Resize Pane | `pane.resize` <span hidden>pane resize grow shrink divider wider narrower taller shorter</span> |
| <span id="action-pane-float" data-entry="Float Pane"></span>Float Pane | `pane.float` <span hidden>pane float floating window dock undock detach overlay pop out tile</span> |
| <span id="action-pane-new-floating" data-entry="New Floating Pane"></span>New Floating Pane | `pane.new_floating` <span hidden>pane new create open float floating window terminal overlay popup scratchpad</span> |
| <span id="action-pane-minimize-floating" data-entry="Minimize Floating Window"></span>Minimize Floating Window | `pane.minimize_floating` <span hidden>pane floating window hide show toggle minimize minimise restore taskbar capsule stash scratchpad</span> |
| <span id="action-pane-minimize-all-floating" data-entry="Minimize Floating Windows"></span>Minimize Floating Windows | `pane.minimize_all_floating` <span hidden>pane floating windows all hide show toggle minimize minimise restore taskbar capsule stash scratchpad</span> |
| <span id="action-pane-paste" data-entry="Paste into Pane"></span>Paste into Pane Pastes the clipboard into the focused terminal. | `pane.paste` <span hidden>paste clipboard insert text terminal</span> |
| <span id="action-pane-copy" data-entry="Copy from Pane"></span>Copy from Pane Copies the focused terminal's selection to the clipboard. | `pane.copy` <span hidden>copy selection clipboard text terminal</span> |
| <span id="action-pane-select-all" data-entry="Select All in Pane"></span>Select All in Pane Selects everything in the focused terminal, including its scrollback. | `pane.select_all` <span hidden>select all selection text terminal scrollback</span> |
| <span id="action-pane-send-key" data-entry="Send Key"></span>Send Key Sends one key to the focused terminal, as if it had been pressed there. | `pane.send_key` <span hidden>send key terminal press chord binding</span> |
| <span id="action-client-prompt-previous" data-entry="Jump to Previous Prompt"></span>Jump to Previous Prompt | `client.prompt.previous` <span hidden>jump scroll previous prompt command mark shell integration up back history</span> |
| <span id="action-client-prompt-next" data-entry="Jump to Next Prompt"></span>Jump to Next Prompt | `client.prompt.next` <span hidden>jump scroll next prompt command mark shell integration down forward</span> |
| <span id="action-client-scroll-page-up" data-entry="Scroll Page Up"></span>Scroll Page Up | `client.scroll.page_up` <span hidden>scroll page up back scrollback history</span> |
| <span id="action-client-scroll-page-down" data-entry="Scroll Page Down"></span>Scroll Page Down | `client.scroll.page_down` <span hidden>scroll page down forward scrollback history</span> |
| <span id="action-client-composer-open" data-entry="Compose Input…"></span>Compose Input… | `client.composer.open` <span hidden>compose composer message input prompt attach image photo file upload claude codex</span> |
| <span id="action-pane-go-to" data-entry="Go to Anything…"></span>Go to Anything… | `pane.go_to` <span hidden>go to anything pane block tab session agent jump switch navigate find search tree overview</span> |
| <span id="action-pane-view-activity" data-entry="View Activity…"></span>View Activity… | `pane.view_activity` <span hidden>view activity active working blocked failed done agents programs status priority</span> |

## Settings

| Action | Name |
| --- | --- |
| <span id="action-client-setting-interface-appearance-scheme" data-entry="Color Scheme"></span>Color Scheme Follows the system appearance or always uses light or dark colors. | `client.setting.interface.appearance.scheme` <span hidden>appearance light dark auto automatic system night mode colour setting preference</span> |
| <span id="action-client-setting-interface-appearance-tint" data-entry="Tint with Theme"></span>Tint with Theme Applies the selected theme's colors to interface surfaces. | `client.setting.interface.appearance.tint` <span hidden>tint theme colors colours palette themed blend use theme interface surfaces setting preference</span> |
| <span id="action-client-setting-interface-active-panes-active-border" data-entry="Highlight Active Pane Edges"></span>Highlight Active Pane Edges Highlights the edges of the focused pane. | `client.setting.interface.active_panes.active_border` <span hidden>border outline focus ring active focused pane highlight edge indicator setting preference</span> |
| <span id="action-client-setting-interface-active-panes-active-border-color" data-entry="Active Pane Highlight Color"></span>Active Pane Highlight Color Chooses the color of the active pane highlight. | `client.setting.interface.active_panes.active_border_color` <span hidden>accent theme terminal text foreground border color focus ring swatch palette red blue green yellow cyan magenta setting preference</span> |
| <span id="action-client-setting-interface-active-panes-active-border-opacity" data-entry="Active Pane Highlight Opacity"></span>Active Pane Highlight Opacity Sets how strongly the active pane highlight draws. | `client.setting.interface.active_panes.active_border_opacity` <span hidden>opacity transparency alpha faint subtle strength border focus ring highlight setting preference</span> |
| <span id="action-client-setting-interface-active-panes-active-border-animation" data-entry="Animate Active Pane Highlight"></span>Animate Active Pane Highlight Fades or moves the highlight to the newly focused pane, or switches it at once. | `client.setting.interface.active_panes.active_border_animation` <span hidden>fade move crossfade glide slide animation transition border focus instant off setting preference</span> |
| <span id="action-client-setting-interface-splits-focus-autobalance" data-entry="Autobalance Splits"></span>Autobalance Splits Evenly resizes a tab's panes when one opens or closes. | `client.setting.interface.splits_focus.autobalance` <span hidden>balance panes equalize even equal size new close split resize divider setting preference</span> |
| <span id="action-client-setting-interface-animation-style" data-entry="Animation Style"></span>Animation Style Chooses how panes move, open, and close. | `client.setting.interface.animation.style` <span hidden>snappy natural off spring bounce motion disable animations instant speed pane split sidebar setting preference</span> |
| <span id="action-client-setting-themes-light-palette" data-entry="Light Theme"></span>Light Theme Selects the theme used in light appearance. | `client.setting.themes.light.palette` <span hidden>light mode theme day bright colors colour scheme palette setting preference</span> |
| <span id="action-client-setting-themes-dark-palette" data-entry="Dark Theme"></span>Dark Theme Selects the theme used in dark appearance. | `client.setting.themes.dark.palette` <span hidden>dark mode theme night dim colors colour scheme palette setting preference</span> |
| <span id="action-client-setting-terminal-typography-font" data-entry="Terminal Font"></span>Terminal Font Chooses the terminal typeface. | `client.setting.terminal.typography.font` <span hidden>font family typeface monospace menlo typography setting preference</span> |
| <span id="action-client-setting-terminal-typography-size" data-entry="Terminal Font Size"></span>Terminal Font Size Sets the size terminal text starts at. | `client.setting.terminal.typography.size` <span hidden>font size text size larger smaller points pt typography default setting preference</span> |
| <span id="action-client-setting-terminal-colors-contrast" data-entry="Improve Text Contrast"></span>Improve Text Contrast Adjusts low-contrast text against its background. | `client.setting.terminal.colors.contrast` <span hidden>minimum contrast legibility accessibility unreadable faint pale ansi truecolor setting preference</span> |
| <span id="action-client-setting-terminal-colors-palette" data-entry="Force Theme Palette for Text"></span>Force Theme Palette for Text Maps RGB and extended text colors to the nearest theme color. | `client.setting.terminal.colors.palette` <span hidden>force theme colors colours remap match palette ansi rgb truecolor 256 extended setting preference</span> |
| <span id="action-client-setting-terminal-cursor-blink" data-entry="Cursor Blink Speed"></span>Cursor Blink Speed Chooses how fast the cursor blinks. | `client.setting.terminal.cursor.blink` <span hidden>blink flashing steady slow fast normal off custom cursor caret setting preference</span> |
| <span id="action-client-setting-terminal-cursor-style" data-entry="Cursor Style"></span>Cursor Style Chooses a block, bar, or underline cursor. | `client.setting.terminal.cursor.style` <span hidden>cursor shape beam caret block bar underline setting preference</span> |
| <span id="action-client-setting-terminal-cursor-force" data-entry="Force Cursor Style"></span>Force Cursor Style Ignores programs' requests to change the cursor's shape. | `client.setting.terminal.cursor.force` <span hidden>override application ignore cursor shape requests setting preference</span> |
| <span id="action-client-setting-terminal-cursor-shaders" data-entry="Cursor Shaders"></span>Cursor Shaders Draws a trail shader behind terminal cursors. | `client.setting.terminal.cursor.shaders` <span hidden>cursor trail effect animation smear glow ghostty shader custom-shader shadertoy setting preference</span> |
| <span id="action-client-setting-terminal-cursor-shader" data-entry="Cursor Shader"></span>Cursor Shader Chooses the effect cursor shaders draw. | `client.setting.terminal.cursor.shader` <span hidden>cursor shader trail style effect warp sweep comet blaze tapered rainbow gradient frozen setting preference</span> |
| <span id="action-client-setting-terminal-scrolling-smooth" data-entry="Smooth Scrolling"></span>Smooth Scrolling Scrolls terminal history by pixels instead of whole lines. | `client.setting.terminal.scrolling.smooth` <span hidden>smooth pixel precise fluid momentum inertia trackpad line by line scroll history setting preference</span> |
| <span id="action-client-setting-terminal-resizing-smooth" data-entry="Smooth Terminal Resizing"></span>Smooth Terminal Resizing Reflows terminal text on the frame a pane changes size. | `client.setting.terminal.resizing.smooth` <span hidden>smooth resize reflow jitter glitch jump flicker live resize rewrap setting preference</span> |
| <span id="action-client-setting-terminal-titles-prefer-generated" data-entry="Prefer Generated Titles"></span>Prefer Generated Titles Names tabs after the running program instead of the title a shell sets. | `client.setting.terminal.titles.prefer_generated` <span hidden>shell title generated program process name directory ignore shell titles tab pane setting preference</span> |
| <span id="action-client-setting-developer-mode-enabled" data-entry="Developer Mode"></span>Developer Mode Reveals settings for development and debugging. | `client.setting.developer.mode.enabled` <span hidden>developer advanced development debugging enable tools setting preference</span> |

