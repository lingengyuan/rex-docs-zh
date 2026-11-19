> 原文：https://www.superlogical.com/rex/docs/reference/ios-settings
> 原文版本：b2cbf3ed8da7（抓取于 2026-11-19）

# iOS 设置

本页列出 Rex for iOS 中的所有设置项及其所在位置。

<div class="reference-page settings" hidden></div>

## 界面

选择配色方案、主题色调、窗格以及窗格移动方式。位于“设置”>“界面”。 <span hidden>display, automatic, system, light, dark, animation, motion</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-interface-color-scheme" data-entry="Color Scheme"></span>Color Scheme（配色方案） | 外观 · 使用自动、浅色或深色外观。<span hidden>In Settings &gt; Interface.</span> <span hidden>appearance, display, system, device, mode, automatic, light mode, dark mode</span> |
| <span id="setting-interface-tint-with-theme" data-entry="Tint with Theme"></span>Tint with Theme（随主题着色） | 外观 · 匹配终端颜色或使用标准 iOS 颜色。<span hidden>In Settings &gt; Interface.</span> <span hidden>theme tint, use theme tint, tinting, matching, neutral, system colors, on, off</span> |
| <span id="setting-interface-match-program-backgrounds" data-entry="Match Program Backgrounds"></span>Match Program Backgrounds（匹配程序背景） | 窗格 · 使用全屏程序的背景为屏幕着色。<span hidden>In Settings &gt; Interface.</span> <span hidden>tint, screen color, header color, terminal background, program background, editor, full screen, tui, neovim, vim, extend, blend, match terminal</span> |

## 主题

为每种外观选择终端颜色。位于“设置”>“主题”。 <span hidden>palette, color scheme, light, dark</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-themes-light-theme" data-entry="Light Theme"></span>Light Theme（浅色主题） | 浅色模式 · 选择浅色外观下的终端调色板。<span hidden>In Settings &gt; Themes.</span> <span hidden>colors, day, scheme, light mode</span> |
| <span id="setting-themes-dark-theme" data-entry="Dark Theme"></span>Dark Theme（深色主题） | 深色模式 · 选择深色外观下的终端调色板。<span hidden>In Settings &gt; Themes.</span> <span hidden>colors, night, scheme, dark mode</span> |

## 终端

配置字体、文本颜色、光标、滚动、调整大小与标题。位于“设置”>“终端”。 <span hidden>shell, console, text, display</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-terminal-terminal-font" data-entry="Terminal Font"></span>Terminal Font（终端字体） | 版式 · 选择终端的字体系列。<span hidden>In Settings &gt; Terminal.</span> <span hidden>font, typeface, monospace, family, menlo, sf mono, system font, jetbrains mono, geist mono, ioskeley mono, roboto mono</span> |
| <span id="setting-terminal-font-size" data-entry="Font Size"></span>Font Size（字号） | 版式 · 设置此设备上的终端文本大小。<span hidden>In Settings &gt; Terminal.</span> <span hidden>text size, bigger, larger, smaller, zoom, points, pt</span> |
| <span id="setting-terminal-improve-text-contrast" data-entry="Improve Text Contrast"></span>Improve Text Contrast（提升文本对比度） | 颜色 · 调整低对比度文本与其背景的对比度；在强制使用主题调色板时生效。<span hidden>In Settings &gt; Terminal.</span> <span hidden>minimum contrast, automatic, legibility, readability, accessibility, unreadable, faint, pale, colors, on, off</span> |
| <span id="setting-terminal-force-theme-palette-for-text" data-entry="Force Theme Palette for Text"></span>Force Theme Palette for Text（对文本强制使用主题调色板） | 颜色 · 将 RGB 与扩展文本颜色映射到最接近的主题颜色，随后修正对比度。<span hidden>In Settings &gt; Terminal.</span> <span hidden>force theme colors, 256 colors, truecolor, rgb, ansi, extended colors, nearest, palette</span> |
| <span id="setting-terminal-cursor-style" data-entry="Cursor Style"></span>Cursor Style（光标样式） | 光标 · 选择方块、竖线或下划线光标。<span hidden>In Settings &gt; Terminal.</span> <span hidden>cursor, caret, shape, block, bar, beam, underline</span> |
| <span id="setting-terminal-blink-speed" data-entry="Blink Speed"></span>Blink Speed（闪烁速度） | 光标 · 让光标慢速、正常、快速闪烁或完全不闪烁。<span hidden>In Settings &gt; Terminal.</span> <span hidden>cursor, blink, blinking, flash, solid, steady, off, slow, fast</span> |
| <span id="setting-terminal-force-style" data-entry="Force Style"></span>Force Style（强制光标样式） | 光标 · 当程序请求更改光标样式时，保持你设定的样式。<span hidden>In Settings &gt; Terminal.</span> <span hidden>cursor, override, ignore, lock, shape, decscusr</span> |
| <span id="setting-terminal-smooth-scrolling" data-entry="Smooth Scrolling"></span>Smooth Scrolling（平滑滚动） | 滚动 · 平滑滚动历史记录，而非按单行滚动。<span hidden>In Settings &gt; Terminal.</span> <span hidden>scroll, scrollback, history, pixel, fling, momentum, drag</span> |
| <span id="setting-terminal-smooth-terminal-resizing" data-entry="Smooth Terminal Resizing"></span>Smooth Terminal Resizing（平滑调整终端大小） | 调整大小 · 在终端改变大小后立即重排文本。<span hidden>In Settings &gt; Terminal.</span> <span hidden>smooth resize, resizing, reflow, re-wrap, rewrap, rotation, rotate, orientation, jitter, jump, flicker, stage manager, split view, preview, on, off</span> |
| <span id="setting-terminal-prefer-generated-titles" data-entry="Prefer Generated Titles"></span>Prefer Generated Titles（优先使用生成的标题） | 标题 · 显示正在运行的程序及其目录，而非 shell 标题。<span hidden>In Settings &gt; Terminal.</span> <span hidden>titles, tab title, window title, program name, directory, shell title, osc, rename</span> |

## 键盘

配置屏幕键盘、硬件键盘的按键重复以及按键栏。位于“设置”>“键盘”。 <span hidden>input, typing, accessory, shortcuts, on-screen keyboard, software keyboard</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-keyboard-autocorrect" data-entry="Autocorrect"></span>Autocorrect（自动更正） | 屏幕键盘 · 允许键盘自动更正和预测词语。<span hidden>In Settings &gt; Keyboard.</span> <span hidden>typing, auto correction, autocorrection, predictive text, spelling</span> |
| <span id="setting-keyboard-keep-keyboard-open" data-entry="Keep Keyboard Open"></span>Keep Keyboard Open（保持键盘展开） | 屏幕键盘 · 返回终端时重新展开键盘。<span hidden>In Settings &gt; Keyboard.</span> <span hidden>keyboard, background, reopen, restore, focus</span> |
| <span id="setting-keyboard-open-keyboard-manually" data-entry="Open Keyboard Manually"></span>Open Keyboard Manually（手动打开键盘） | 屏幕键盘 · 点击终端时保持键盘收起，通过键盘按钮手动打开。<span hidden>In Settings &gt; Keyboard.</span> <span hidden>tap, tap to type, keyboard button, closed, hidden, show keyboard, key bar, keybar, manual</span> |
| <span id="setting-keyboard-key-repeat" data-entry="Key Repeat"></span>Key Repeat（按键重复） | 硬件键盘 · 在外接键盘上按住按键时重复输入。<span hidden>In Settings &gt; Keyboard.</span> <span hidden>hardware keyboard, magic keyboard, external keyboard, hold, held, repeating, backspace, delete, arrows, accessibility</span> |
| <span id="setting-keyboard-delay-until-repeat" data-entry="Delay Until Repeat"></span>Delay Until Repeat（重复前延迟） | 硬件键盘 · 按住按键多长时间后开始重复输入。<span hidden>In Settings &gt; Keyboard.</span> <span hidden>hardware keyboard, key repeat, delay, wait, hold, seconds, speed</span> |
| <span id="setting-keyboard-key-repeat-interval" data-entry="Key Repeat Interval"></span>Key Repeat Interval（按键重复间隔） | 硬件键盘 · 按住按键时重复输入的速率。<span hidden>In Settings &gt; Keyboard.</span> <span hidden>hardware keyboard, key repeat, rate, speed, fast, slow, seconds, interval</span> |
| <span id="setting-keyboard-repeat-held-letters" data-entry="Repeat Held Letters"></span>Repeat Held Letters（重复按住的字母） | 硬件键盘 · 重复输入按住的字母，而非显示变音符号菜单。<span hidden>In Settings &gt; Keyboard.</span> <span hidden>hardware keyboard, accents, accented, accent menu, alternate characters, diacritics, long press, press and hold, letters, symbols</span> |
| <span id="setting-keyboard-key-bar-layout" data-entry="Key Bar Layout"></span>Key Bar Layout（按键栏布局） | 按键栏 · 排列、隐藏和重新排序按键栏的内置按键。<span hidden>In Settings &gt; Keyboard.</span> <span hidden>arrows, escape, tab, control, option, shift, paste, home, end, page up, page down, delete, return, rearrange, reorder, hide keys</span> |
| <span id="setting-keyboard-shortcut-groups" data-entry="Shortcut Groups"></span>Shortcut Groups（快捷键分组） | 按键栏 · 添加 Control 快捷键、功能键以及自定按键。<span hidden>In Settings &gt; Keyboard.</span> <span hidden>function keys, f1, ctrl, control, custom keys, slash commands, hotkeys, accessory</span> |
| <span id="setting-keyboard-characters" data-entry="Characters"></span>Characters（字符按键） | 选择标点符号按键。<span hidden>In Settings &gt; Keyboard.</span> <span hidden>punctuation, shell characters, symbols, tilde, pipe, slash</span> |
| <span id="setting-keyboard-use-symbols" data-entry="Use Symbols"></span>Use Symbols（使用符号） | 按键栏 · 显示符号而非缩写的按键名称。<span hidden>In Settings &gt; Keyboard.</span> <span hidden>keyboard, key bar, icons, control, option, shift</span> |
| <span id="setting-keyboard-haptic-feedback" data-entry="Haptic Feedback"></span>Haptic Feedback（触觉反馈） | 按键栏 · 按下按键栏按钮时感受轻微触感反馈。<span hidden>In Settings &gt; Keyboard.</span> <span hidden>keyboard, vibration, vibrate, touch</span> |
| <span id="setting-keyboard-command-palette" data-entry="Command Palette"></span>Command Palette（命令面板说明） | 按键栏 · 了解如何打开命令以及使用修饰键。<span hidden>In Settings &gt; Keyboard.</span> <span hidden>keyboard, shortcuts, command shift p, control, option, shift, paste</span> |

## 远程主机

管理已保存的主机、连接、端口转发以及每台主机启动的 shell。位于“设置”>“远程主机”。 <span hidden>server, add, pair, connect, reconnect, edit, delete, remove, startup command, shell, default shell, login shell, nushell, zsh, fish, port forwarding, forward, forwards, tunnel, localhost, ssh `-L`</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-remote-hosts-ssh-key" data-entry="SSH Key"></span>SSH Key（SSH 密钥） | 创建或导入 Rex 登录 `ssh://` 主机所用的密钥，以及其受信任的主机密钥。<span hidden>In Settings &gt; Remote Hosts.</span> <span hidden>ssh, key, private key, public key, authorized_keys, secure enclave, import, passphrase, ed25519, ecdsa, host key, fingerprint, known hosts, trust</span> |

## 开发者模式

开发者 · 显示用于网络与终端的高级设置。位于“设置”>“开发者模式”。 <span hidden>developer, debug, diagnostics</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-developer-mode-network-diagnostics" data-entry="Network Diagnostics"></span>Network Diagnostics（网络诊断） | 在开启“开发者模式”时，在屏幕上悬浮显示网络路径与主机连接状态。<span hidden>In Settings &gt; Developer Mode. Needs Developer Mode.</span> <span hidden>debug, network, path, wi-fi, cellular, reconnect, overlay</span> |
| <span id="setting-developer-mode-cursor-shaders" data-entry="Cursor Shaders"></span>Cursor Shaders（光标着色器） | 光标 · 在开启“开发者模式”时，在光标后方绘制拖尾着色器效果，例如 Warp、Comet 或 Blaze。<span hidden>In Settings &gt; Developer Mode. Needs Developer Mode.</span> <span hidden>cursor, cursor trail, cursor effect, cursor animation, smear, glow, warp, sweep, comet, blaze, tapered, rainbow, gradient, frozen, ghostty shader, custom-shader, shadertoy, shader, experimental</span> |

## 关于

关于 · 查看 App 的版本和设备信息，并可将其复制以用于提交错误报告。位于“设置”>“关于”。 <span hidden>version, build, commit, device, model, ios, system, bug report, feedback, copy version info, copy debug info, diagnostics, support, license, open source, acknowledgements, fonts</span>
