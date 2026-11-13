---
title: "Mac Actions"
canonical_url: https://www.superlogical.com/rex/docs/reference/mac-actions
---

# Mac Actions

This page lists every action in the Rex for Mac command palette. Use the name to [bind a key](https://www.superlogical.com/rex/docs/customize/keyboard-shortcuts.md) or to run it with `rex do`. Anything tagged [Bleeding Edge](https://www.superlogical.com/rex/docs/reference/mac-settings.md#setting-app-version-update-channel) is on that update channel and not yet in Preview.

<div class="reference-page actions" hidden></div>

## Window

| Action | Name | Default Shortcut |
| --- | --- | --- |
| <span id="action-client-window-new" data-entry="New Window"></span>New Window | `client.window.new` <span hidden>create workspace window</span> |  <span hidden>Default shortcut:</span>`cmd+n` |
| <span id="action-client-window-close" data-entry="Close Window"></span>Close Window | `client.window.close` <span hidden>close workspace window</span> |  <span hidden>Default shortcut:</span>`shift+cmd+w` |
| <span id="action-client-window-fullscreen-toggle" data-entry="Toggle Full Screen"></span>Toggle Full Screen | `client.window.fullscreen.toggle` <span hidden>full screen fullscreen enter exit window</span> |  <span hidden>Default shortcut:</span>`ctrl+cmd+f` |
| <span id="action-client-close" data-entry="Close"></span>Close Closes the focused pane, else the selected tab, else the window. | `client.close` <span hidden>close pane tab window focused</span> |  <span hidden>Default shortcut:</span>`cmd+w` |

## App

| Action | Name | Default Shortcut |
| --- | --- | --- |
| <span id="action-client-palette-toggle" data-entry="Command Palette…"></span>Command Palette… | `client.palette.toggle` <span hidden>command palette search commands actions</span> |  <span hidden>Default shortcut:</span>`shift+cmd+p` |
| <span id="action-client-settings" data-entry="Settings…"></span>Settings… | `client.settings` <span hidden>preferences settings options configure</span> |  <span hidden>Default shortcut:</span>`cmd+,` |
| <span id="action-client-diagnostics" data-entry="Rex Diagnostics"></span>Rex Diagnostics | `client.diagnostics` <span hidden>diagnostics logs debug troubleshoot server report</span> |  <span hidden>Default shortcut:</span>`shift+cmd+,` |
| <span id="action-client-onboarding" data-entry="Open Onboarding Session…"></span>Open Onboarding Session… | `client.onboarding` <span hidden>onboarding welcome setup get started tour walkthrough migrate import keybindings theme appearance ghostty tmux zellij agent</span> |  |
| <span id="action-client-permissions" data-entry="Grant System Permissions…"></span>Grant System Permissions… | `client.permissions` <span hidden>permissions privacy security full disk access screen recording system audio grant allow system settings tcc</span> |  |
| <span id="action-client-visibility-toggle" data-entry="Toggle Visibility"></span>Toggle Visibility Shows Rex from any app, or hides it when it's in front. | `client.visibility.toggle` <span hidden>show hide rex global hotkey summon bring to front focus toggle_visibility</span> |  |
| <span id="action-client-version-copy" data-entry="Copy Version Info"></span>Copy Version Info Copies the app and server versions to the clipboard. | `client.version.copy` <span hidden>version build number copy clipboard about app server release</span> |  |
| <span id="action-client-debug-copy" data-entry="Copy Debug Info"></span>Copy Debug Info Copies a report of the app, system, server, and host state to the clipboard. | `client.debug.copy` <span hidden>debug debugging info report copy clipboard diagnostics troubleshoot support bug commit build environment</span> |  |
| <span id="action-client-pair-device" data-entry="Pair Device with QR Code…"></span>Pair Device with QR Code… | `client.pair_device` <span hidden>pair device qr code scan iphone ipad ios mobile tailscale connect link</span> |  |
| <span id="action-client-update-accept" data-entry="Install Update"></span>Install Update The menu shows the current update's own title; this is the static fallback. | `client.update.accept` <span hidden>update install retry app application version upgrade sparkle</span> |  <span hidden>Default shortcut:</span>`shift+cmd+u` |
| <span id="action-client-update-accept-when-idle" data-entry="Relaunch when Idle"></span>Relaunch when Idle Relaunches into a downloaded update once Rex's windows are out of sight. | `client.update.accept_when_idle` <span hidden>update install relaunch restart idle later automatic</span> |  <span hidden>Default shortcut:</span>`alt+shift+cmd+u` |
| <span id="action-client-update-check" data-entry="Check for Updates in Background"></span>Check for Updates in Background Checks for a Rex update without showing anything, and returns what it found. | `client.update.check` <span hidden>update check background quiet silent app application version sparkle</span> |  |
| <span id="action-client-update-status" data-entry="Report Update Status"></span>Report Update Status Returns the running version, the update settings, and the updater's state. | `client.update.status` <span hidden>update status version build channel feed state report sparkle</span> |  |
| <span id="action-client-update-install" data-entry="Install Update and Relaunch"></span>Install Update and Relaunch Downloads the available Rex update if needed, installs it, and relaunches without asking. | `client.update.install` <span hidden>update install download relaunch restart upgrade app application sparkle unattended</span> |  |
| <span id="action-client-update-set-automation" data-entry="Set Update Automation"></span>Set Update Automation Chooses whether Rex only offers updates, downloads them, or installs them. | `client.update.set_automation` <span hidden>update automatic automation download install notify setting preference</span> |  |
| <span id="action-client-update-set-channel" data-entry="Set Update Channel"></span>Set Update Channel Chooses the release channel Rex updates from. | `client.update.set_channel` <span hidden>update channel feed preview snapshot bleeding edge release setting preference</span> |  |
| <span id="action-client-notice-dismiss" data-entry="Dismiss Notice"></span>Dismiss Notice | `client.notice.dismiss` <span hidden>dismiss notice banner alert hide</span> |  <span hidden>Default shortcut:</span>`shift+cmd+.` |
| <span id="action-client-shortcuts-edit" data-entry="Change Shortcut…"></span>Change Shortcut… | `client.shortcuts.edit` <span hidden>keyboard key binding bindings keybinding keybindings rebind record hotkey shortcut</span> |  |
| <span id="action-client-agents-setup" data-entry="Install Rex for Agents"></span>Install Rex for Agents Installs the Rex skill and hooks for Claude Code, Codex, and other agents. | `client.agents.setup` <span hidden>`rex skill` install agent agents coding ai claude code codex cursor copilot gemini hook hooks setup</span> |  |
| <span id="action-client-server-restart" data-entry="Restart Server…"></span>Restart Server… Stops the local Rex server and starts it again. | `client.server.restart` <span hidden>restart reload relaunch reboot stop start server rex daemon process local</span> |  |

## Session

| Action | Name | Default Shortcut |
| --- | --- | --- |
| <span id="action-session-new" data-entry="New Session"></span>New Session | `session.new` <span hidden>create session add</span> |  <span hidden>Default shortcut:</span>`shift+cmd+n` |
| <span id="action-session-switch" data-entry="Change Session…"></span>Change Session… | `session.switch` <span hidden>session switch jump go</span> |  <span hidden>Default shortcut:</span>`cmd+k` |
| <span id="action-session-select" data-entry="Go to Session"></span>Go to Session | `session.select` <span hidden>session select show jump go identifier id</span> |  |
| <span id="action-session-next" data-entry="Next Session"></span>Next Session | `session.next` <span hidden>cycle session forward</span> |  |
| <span id="action-session-previous" data-entry="Previous Session"></span>Previous Session | `session.previous` <span hidden>cycle session back</span> |  |
| <span id="action-session-rename" data-entry="Rename Session"></span>Rename Session | `session.rename` <span hidden>rename session name title</span> |  |
| <span id="action-session-close" data-entry="Close Session"></span>Close Session | `session.close` <span hidden>close kill destroy delete session</span> |  |
| <span id="action-session-refresh" data-entry="Refresh Sessions"></span>Refresh Sessions | `session.refresh` <span hidden>reload sync sessions</span> |  <span hidden>Default shortcut:</span>`cmd+r` |
| <span id="action-session-collapse" data-entry="Collapse Session"></span>Collapse Session | `session.collapse` <span hidden>collapse fold hide session sidebar tabs</span> |  |
| <span id="action-session-expand" data-entry="Expand Session"></span>Expand Session | `session.expand` <span hidden>expand unfold show open session sidebar tabs</span> |  |
| <span id="action-session-collapse-others" data-entry="Collapse Other Sessions"></span>Collapse Other Sessions | `session.collapse_others` <span hidden>collapse fold hide other all sessions sidebar focus</span> |  |

## Host

| Action | Name | Default Shortcut |
| --- | --- | --- |
| <span id="action-client-host-switch" data-entry="Switch Host"></span>Switch Host | `client.host.switch` <span hidden>host remote machine server switch go</span> |  |
| <span id="action-client-host-add" data-entry="Add Remote Host…"></span>Add Remote Host… | `client.host.add` <span hidden>host remote add server machine url http https connect</span> |  |
| <span id="action-client-host-remove" data-entry="Remove Host…"></span>Remove Host… | `client.host.remove` <span hidden>remove forget delete disconnect host remote server machine</span> |  |

## Tab

| Action | Name | Default Shortcut |
| --- | --- | --- |
| <span id="action-client-tab-new" data-entry="New Tab"></span>New Tab | `client.tab.new` <span hidden>create tab window add</span> |  <span hidden>Default shortcut:</span>`cmd+t` |
| <span id="action-client-tab-close" data-entry="Close Tab"></span>Close Tab | `client.tab.close` <span hidden>close tab window</span> |  <span hidden>Default shortcut:</span>`alt+cmd+w` |
| <span id="action-client-tab-close-others" data-entry="Close Other Tabs"></span>Close Other Tabs | `client.tab.close_others` <span hidden>close other tabs windows kill only keep</span> |  |
| <span id="action-client-tab-rename" data-entry="Rename Tab"></span>Rename Tab | `client.tab.rename` <span hidden>rename tab window name title</span> |  |
| <span id="action-client-tab-next" data-entry="Show Next Tab"></span>Show Next Tab | `client.tab.next` <span hidden>cycle tab window forward</span> |  <span hidden>Default shortcut:</span>`ctrl+tab`, `shift+cmd+]` |
| <span id="action-client-tab-previous" data-entry="Show Previous Tab"></span>Show Previous Tab | `client.tab.previous` <span hidden>cycle tab window back</span> |  <span hidden>Default shortcut:</span>`ctrl+shift+tab`, `shift+cmd+[` |
| <span id="action-client-tab-goto" data-entry="Go to Tab"></span>Go to Tab | `client.tab.goto` <span hidden>tab window select number index jump go</span> |  <span hidden>Default shortcut:</span>`cmd+[Digit1]`, `cmd+[Digit2]`, `cmd+[Digit3]`, `cmd+[Digit4]`, `cmd+[Digit5]`, `cmd+[Digit6]`, `cmd+[Digit7]`, `cmd+[Digit8]`, `cmd+[Digit9]` |
| <span id="action-client-tab-move" data-entry="Move Tab"></span>Move Tab | `client.tab.move` <span hidden>move tab window reorder</span> |  |
| <span id="action-client-tab-move-backward" data-entry="Move Tab Backward"></span>Move Tab Backward | `client.tab.move.backward` <span hidden>move tab window reorder left up earlier</span> |  <span hidden>Default shortcut:</span>`ctrl+shift+pageup` |
| <span id="action-client-tab-move-forward" data-entry="Move Tab Forward"></span>Move Tab Forward | `client.tab.move.forward` <span hidden>move tab window reorder right down later</span> |  <span hidden>Default shortcut:</span>`ctrl+shift+pagedown` |
| <span id="action-client-tab-move-to-new-window" data-entry="Move Tab to New Window"></span>Move Tab to New Window | `client.tab.move_to_new_window` <span hidden>move tab new window tear off detach separate pop out own</span> |  |

## Pane

| Action | Name | Default Shortcut |
| --- | --- | --- |
| <span id="action-pane-split" data-entry="Split Pane"></span>Split Pane | `pane.split` <span hidden>pane split terminal divide new</span> |  |
| <span id="action-pane-split-left" data-entry="Split Pane Left"></span>Split Pane Left | `pane.split.left` <span hidden>pane split terminal divide new left</span> |  <span hidden>Default shortcut:</span>`shift+cmd+left` |
| <span id="action-pane-split-right" data-entry="Split Pane Right"></span>Split Pane Right | `pane.split.right` <span hidden>pane split terminal divide new right</span> |  <span hidden>Default shortcut:</span>`cmd+d`, `shift+cmd+right` |
| <span id="action-pane-split-up" data-entry="Split Pane Up"></span>Split Pane Up | `pane.split.up` <span hidden>pane split terminal divide new above up</span> |  <span hidden>Default shortcut:</span>`shift+cmd+up` |
| <span id="action-pane-split-down" data-entry="Split Pane Down"></span>Split Pane Down | `pane.split.down` <span hidden>pane split terminal divide new below down</span> |  <span hidden>Default shortcut:</span>`shift+cmd+d`, `shift+cmd+down` |
| <span id="action-pane-split-auto" data-entry="Split Pane Best Fit"></span>Split Pane Best Fit | `pane.split.auto` <span hidden>pane split terminal divide new automatic best fit</span> |  <span hidden>Default shortcut:</span>`cmd+enter` |
| <span id="action-pane-focus" data-entry="Focus Pane"></span>Focus Pane | `pane.focus` <span hidden>pane focus navigate</span> |  |
| <span id="action-pane-focus-left" data-entry="Focus Pane Left"></span>Focus Pane Left | `pane.focus.left` <span hidden>pane focus navigate left</span> |  <span hidden>Default shortcut:</span>`alt+cmd+left` |
| <span id="action-pane-focus-right" data-entry="Focus Pane Right"></span>Focus Pane Right | `pane.focus.right` <span hidden>pane focus navigate right</span> |  <span hidden>Default shortcut:</span>`alt+cmd+right` |
| <span id="action-pane-focus-up" data-entry="Focus Pane Up"></span>Focus Pane Up | `pane.focus.up` <span hidden>pane focus navigate up above</span> |  <span hidden>Default shortcut:</span>`alt+cmd+up` |
| <span id="action-pane-focus-down" data-entry="Focus Pane Down"></span>Focus Pane Down | `pane.focus.down` <span hidden>pane focus navigate down below</span> |  <span hidden>Default shortcut:</span>`alt+cmd+down` |
| <span id="action-pane-focus-next" data-entry="Focus Next Pane"></span>Focus Next Pane | `pane.focus_next` <span hidden>pane focus next forward</span> |  <span hidden>Default shortcut:</span>`cmd+]` |
| <span id="action-pane-focus-previous" data-entry="Focus Previous Pane"></span>Focus Previous Pane | `pane.focus_previous` <span hidden>pane focus previous back</span> |  <span hidden>Default shortcut:</span>`cmd+[` |
| <span id="action-pane-move" data-entry="Move Pane"></span>Move Pane | `pane.move` <span hidden>pane move swap rearrange</span> |  |
| <span id="action-pane-move-left" data-entry="Move Pane Left"></span>Move Pane Left | `pane.move.left` <span hidden>pane move swap rearrange left</span> |  <span hidden>Default shortcut:</span>`alt+shift+cmd+left` |
| <span id="action-pane-move-right" data-entry="Move Pane Right"></span>Move Pane Right | `pane.move.right` <span hidden>pane move swap rearrange right</span> |  <span hidden>Default shortcut:</span>`alt+shift+cmd+right` |
| <span id="action-pane-move-up" data-entry="Move Pane Up"></span>Move Pane Up | `pane.move.up` <span hidden>pane move swap rearrange up above</span> |  <span hidden>Default shortcut:</span>`alt+shift+cmd+up` |
| <span id="action-pane-move-down" data-entry="Move Pane Down"></span>Move Pane Down | `pane.move.down` <span hidden>pane move swap rearrange down below</span> |  <span hidden>Default shortcut:</span>`alt+shift+cmd+down` |
| <span id="action-pane-float" data-entry="Float Pane"></span>Float Pane | `pane.float` <span hidden>pane float floating window dock undock detach overlay pop out tile</span> |  <span hidden>Default shortcut:</span>`alt+cmd+enter` |
| <span id="action-pane-new-floating" data-entry="New Floating Pane"></span>New Floating Pane | `pane.new_floating` <span hidden>pane new create open float floating window terminal overlay popup scratchpad</span> |  |
| <span id="action-pane-minimize-floating" data-entry="Minimize Floating Window"></span>Minimize Floating Window | `pane.minimize_floating` <span hidden>pane floating window hide show toggle minimize minimise restore taskbar capsule stash scratchpad</span> |  <span hidden>Default shortcut:</span>`alt+cmd+m` |
| <span id="action-pane-minimize-all-floating" data-entry="Minimize Floating Windows"></span>Minimize Floating Windows | `pane.minimize_all_floating` <span hidden>pane floating windows all hide show toggle minimize minimise restore taskbar capsule stash scratchpad</span> |  <span hidden>Default shortcut:</span>`alt+shift+cmd+enter` |
| <span id="action-pane-zoom" data-entry="Zoom Pane"></span>Zoom Pane | `pane.zoom` <span hidden>pane zoom maximize restore terminal</span> |  <span hidden>Default shortcut:</span>`shift+cmd+enter` |
| <span id="action-pane-close" data-entry="Close Pane"></span>Close Pane | `pane.close` <span hidden>pane close remove terminal</span> |  <span hidden>Default shortcut:</span>`cmd+w` |
| <span id="action-pane-close-others" data-entry="Close Other Panes"></span>Close Other Panes | `pane.close_others` <span hidden>close other panes kill only keep focused</span> |  |
| <span id="action-pane-balance" data-entry="Balance Splits"></span>Balance Splits | `pane.balance` <span hidden>pane split balance equalize equalise evenly distribute resize layout</span> |  |
| <span id="action-pane-resize" data-entry="Resize Pane"></span>Resize Pane | `pane.resize` <span hidden>pane resize grow shrink divider wider narrower taller shorter</span> |  |
| <span id="action-pane-move-to-new-tab" data-entry="Move Pane to New Tab"></span>Move Pane to New Tab | `pane.move_to_new_tab` <span hidden>pane block move new window tab detach split</span> |  |
| <span id="action-pane-move-to-tab" data-entry="Move Pane to Tab…"></span>Move Pane to Tab… | `pane.move_to_tab` <span hidden>pane block move tab window send other existing join</span> |  |
| <span id="action-pane-go-to-directory" data-entry="Go to Directory…"></span>Go to Directory… | `pane.go_to_directory` <span hidden>go to directory folder path cd new tab open navigate</span> |  <span hidden>Default shortcut:</span>`shift+cmd+g` |
| <span id="action-pane-go-to" data-entry="Go to Anything…"></span>Go to Anything… | `pane.go_to` <span hidden>go to anything pane block tab session agent jump switch navigate find search tree overview</span> |  <span hidden>Default shortcut:</span>`cmd+p` |
| <span id="action-pane-view-activity" data-entry="View Activity…"></span>View Activity… | `pane.view_activity` <span hidden>view activity active working blocked failed done agents programs status priority</span> |  |
| <span id="action-pane-insert-path" data-entry="Insert Path…"></span>Insert Path… | `pane.insert_path` <span hidden>insert path file folder directory cursor type paste complete browse</span> |  <span hidden>Default shortcut:</span>`ctrl+cmd+i` |
| <span id="action-pane-copy-id" data-entry="Copy Pane ID"></span>Copy Pane ID Copies the focused pane's block ID to the clipboard. | `pane.copy_id` <span hidden>pane block id identifier copy clipboard target agent capture</span> |  |
| <span id="action-pane-rename" data-entry="Rename Pane"></span>Rename Pane | `pane.rename` <span hidden>rename pane block name title label</span> |  |
| <span id="action-pane-paste" data-entry="Paste into Pane"></span>Paste into Pane Pastes the clipboard into the focused terminal. | `pane.paste` <span hidden>paste clipboard insert text terminal</span> |  |
| <span id="action-pane-copy" data-entry="Copy from Pane"></span>Copy from Pane Copies the focused terminal's selection to the clipboard. | `pane.copy` <span hidden>copy selection clipboard text terminal</span> |  |
| <span id="action-pane-select-all" data-entry="Select All in Pane"></span>Select All in Pane Selects everything in the focused terminal, including its scrollback. | `pane.select_all` <span hidden>select all selection text terminal scrollback</span> |  |
| <span id="action-pane-send-key" data-entry="Send Key"></span>Send Key Sends one key to the focused terminal, as if it had been pressed there. | `pane.send_key` <span hidden>send key terminal press chord binding</span> |  <span hidden>Default shortcut:</span>`cmd+backspace`, `cmd+left`, `cmd+right`, `alt+left`, `alt+right` |
| <span id="action-client-key-forward" data-entry="Send Key to Server"></span>Send Key to Server Sends the key that performed it to the focused terminal, for a script to answer. | `client.key.forward` <span hidden>send key forward server script lua binding</span> |  |
| <span id="action-client-prompt-previous" data-entry="Jump to Previous Prompt"></span>Jump to Previous Prompt | `client.prompt.previous` <span hidden>jump scroll previous prompt command mark shell integration up back history</span> |  <span hidden>Default shortcut:</span>`cmd+up` |
| <span id="action-client-prompt-next" data-entry="Jump to Next Prompt"></span>Jump to Next Prompt | `client.prompt.next` <span hidden>jump scroll next prompt command mark shell integration down forward</span> |  <span hidden>Default shortcut:</span>`cmd+down` |
| <span id="action-client-scroll-page-up" data-entry="Scroll Page Up"></span>Scroll Page Up | `client.scroll.page_up` <span hidden>scroll page up back scrollback history</span> |  |
| <span id="action-client-scroll-page-down" data-entry="Scroll Page Down"></span>Scroll Page Down | `client.scroll.page_down` <span hidden>scroll page down forward scrollback history</span> |  |
| <span id="action-client-quick-look" data-entry="Quick Look"></span>Quick Look Previews the files and web links on screen in Quick Look. | `client.quick_look` <span hidden>quick look preview file image link path url web pointer hover</span> |  <span hidden>Default shortcut:</span>`cmd+y` |

## Keys

| Action | Name | Default Shortcut |
| --- | --- | --- |
| <span id="action-client-mode-enter" data-entry="Enter Mode"></span>Enter Mode Makes the keys a mode binds perform, until the mode is left. | `client.mode.enter` <span hidden>mode enter key table prefix resize modal</span> |  |
| <span id="action-client-mode-exit" data-entry="Exit Mode"></span>Exit Mode | `client.mode.exit` <span hidden>mode exit leave quit key table escape</span> |  |
| <span id="action-client-mode-exit-all" data-entry="Exit All Modes"></span>Exit All Modes | `client.mode.exit_all` <span hidden>mode exit leave quit all key table escape</span> |  |

## Find

| Action | Name | Default Shortcut |
| --- | --- | --- |
| <span id="action-client-find-open" data-entry="Find…"></span>Find… | `client.find.open` <span hidden>find search text scrollback highlight</span> |  <span hidden>Default shortcut:</span>`cmd+f` |
| <span id="action-client-find-next" data-entry="Find Next"></span>Find Next | `client.find.next` <span hidden>find search next forward match</span> |  <span hidden>Default shortcut:</span>`cmd+g` |
| <span id="action-client-find-previous" data-entry="Find Previous"></span>Find Previous | `client.find.previous` <span hidden>find search previous back match</span> |  <span hidden>Default shortcut:</span>`shift+cmd+g` |

## View

| Action | Name | Default Shortcut |
| --- | --- | --- |
| <span id="action-client-font-increase" data-entry="Increase Font Size"></span>Increase Font Size | `client.font.increase` <span hidden>terminal font size larger bigger increase zoom text typography</span> |  <span hidden>Default shortcut:</span>`shift+cmd+=`, `cmd+=` |
| <span id="action-client-font-decrease" data-entry="Decrease Font Size"></span>Decrease Font Size | `client.font.decrease` <span hidden>terminal font size smaller decrease zoom text typography</span> |  <span hidden>Default shortcut:</span>`cmd+-` |
| <span id="action-client-font-reset" data-entry="Reset Font Size"></span>Reset Font Size | `client.font.reset` <span hidden>terminal font size reset default original text typography</span> |  <span hidden>Default shortcut:</span>`cmd+[Digit0]` |
| <span id="action-client-sidebar-toggle" data-entry="Toggle Sidebar"></span>Toggle Sidebar | `client.sidebar.toggle` <span hidden>sidebar collapse expand fold hide show tabs</span> |  <span hidden>Default shortcut:</span>`cmd+/` |
| <span id="action-client-sidebar-activity-toggle" data-entry="Toggle Activity"></span>Toggle Activity | `client.sidebar.activity.toggle` <span hidden>activity mode view filter working waiting attention programs status sidebar tabs</span> |  <span hidden>Default shortcut:</span>`cmd+.` |
| <span id="action-client-sidebar-activity-by-session" data-entry="Show Activity by Session"></span>Show Activity by Session | `client.sidebar.activity.by_session` <span hidden>activity mode view filter group grouping by session sessions sidebar tabs</span> |  |
| <span id="action-client-sidebar-activity-by-priority" data-entry="Show Activity by Priority"></span>Show Activity by Priority | `client.sidebar.activity.by_priority` <span hidden>activity mode view filter group grouping by priority blocked failed done working idle sidebar tabs</span> |  |
| <span id="action-client-sidebar-filter-focus" data-entry="Focus Tab Filter"></span>Focus Tab Filter | `client.sidebar.filter.focus` <span hidden>filter search find type query focus keyboard sidebar activity tabs sessions hosts</span> |  |
| <span id="action-client-tab-style-toggle" data-entry="Toggle Toolbar Layout"></span>Toggle Toolbar Layout | `client.tab_style.toggle` <span hidden>toolbar layout tab style orientation sidebar horizontal vertical view</span> |  <span hidden>Default shortcut:</span>`shift+cmd+s` |
| <span id="action-client-toolbar-reveal" data-entry="Reveal Toolbar"></span>Reveal Toolbar | `client.toolbar.reveal` <span hidden>show reveal peek toolbar tab bar title row hover auto-hide hidden view</span> |  <span hidden>Default shortcut:</span>`alt+cmd+t` |
| <span id="action-client-pane-header-reveal" data-entry="Reveal Pane Header"></span>Reveal Pane Header | `client.pane_header.reveal` <span hidden>show reveal peek pane header title hover hidden focused pane view</span> |  <span hidden>Default shortcut:</span>`alt+shift+cmd+t` |
| <span id="action-client-theme-change" data-entry="Change Theme…"></span>Change Theme… | `client.theme.change` <span hidden>theme colour color scheme palette appearance</span> |  |
| <span id="action-client-theme-import" data-entry="Import Theme File"></span>Import Theme File Imports a Ghostty theme or iTerm color file and selects it. | `client.theme.import` <span hidden>theme import ghostty iterm file colour color scheme palette</span> |  |
| <span id="action-client-appearance-switch-mode" data-entry="Switch Appearance Mode"></span>Switch Appearance Mode | `client.appearance.switch_mode` <span hidden>appearance mode light dark toggle color scheme</span> |  |
| <span id="action-client-config-copy-path" data-entry="Copy Config File Path"></span>Copy Config File Path | `client.config.copy_path` <span hidden>config configuration file path copy clipboard init.lua lua keybindings shortcuts settings location where</span> |  |
| <span id="action-client-config-reload" data-entry="Reload Config"></span>Reload Config | `client.config.reload` <span hidden>config configuration reload reread apply init.lua lua keybindings shortcuts settings</span> |  |

