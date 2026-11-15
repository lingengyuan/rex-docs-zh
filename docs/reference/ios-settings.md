> 原文：https://www.superlogical.com/rex/docs/reference/ios-settings
> 原文版本：1af343b09484（抓取于 2026-11-15）

# iOS 设置

本页列出 Rex for iOS 中的所有设置项及其所在位置。

<div class="reference-page settings" hidden></div>

## 界面

选择配色方案、主题色调、窗格以及窗格移动方式。位于“设置”>“界面”。 <span hidden>display, automatic, system, light, dark, animation, motion</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-interface-color-scheme" data-entry="Color scheme"></span>Color scheme（配色方案） | 外观 · 使用自动、浅色或深色外观。<span hidden>In Settings &gt; Interface.</span> <span hidden>appearance, display, system, device, mode, automatic, light mode, dark mode</span> |
| <span id="setting-interface-tint-with-theme" data-entry="Tint with theme"></span>Tint with theme（随主题着色） | 外观 · 匹配终端颜色或使用标准 iOS 颜色。<span hidden>In Settings &gt; Interface.</span> <span hidden>theme tint, use theme tint, tinting, matching, neutral, system colors, on, off</span> |
| <span id="setting-interface-match-program-backgrounds" data-entry="Match program backgrounds"></span>Match program backgrounds（匹配程序背景） | 窗格 · 使用全屏程序的背景为屏幕着色。<span hidden>In Settings &gt; Interface.</span> <span hidden>tint, screen color, header color, terminal background, program background, editor, full screen, tui, neovim, vim, extend, blend, match terminal</span> |

## 主题

为每种外观选择终端颜色。位于“设置”>“主题”。 <span hidden>palette, color scheme, light, dark</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-themes-light-theme" data-entry="Light theme"></span>Light theme（浅色主题） | 浅色模式 · 选择浅色外观下的终端调色板。<span hidden>In Settings &gt; Themes.</span> <span hidden>colors, day, scheme, light mode</span> |
| <span id="setting-themes-dark-theme" data-entry="Dark theme"></span>Dark theme（深色主题） | 深色模式 · 选择深色外观下的终端调色板。<span hidden>In Settings &gt; Themes.</span> <span hidden>colors, night, scheme, dark mode</span> |

## 终端

配置字体、文本颜色、光标、键盘、按键栏、滚动与标题。位于“设置”>“终端”。 <span hidden>keyboard, input, accessory, shortcuts</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-terminal-terminal-font" data-entry="Terminal font"></span>Terminal font（终端字体） | 版式 · 选择终端的字体系列。<span hidden>In Settings &gt; Terminal.</span> <span hidden>font, typeface, monospace, family, menlo, sf mono, system font, jetbrains mono, geist mono, ioskeley mono, roboto mono</span> |
| <span id="setting-terminal-font-size" data-entry="Font size"></span>Font size（字号） | 版式 · 设置此设备上的终端文本大小。<span hidden>In Settings &gt; Terminal.</span> <span hidden>text size, bigger, larger, smaller, zoom, points, pt</span> |
| <span id="setting-terminal-improve-text-contrast" data-entry="Improve text contrast"></span>Improve text contrast（提升文本对比度） | 颜色 · 调整低对比度文本与其背景的对比度；在强制使用主题调色板时生效。<span hidden>In Settings &gt; Terminal.</span> <span hidden>minimum contrast, automatic, legibility, readability, accessibility, unreadable, faint, pale, colors, on, off</span> |
| <span id="setting-terminal-force-theme-palette-for-text" data-entry="Force theme palette for text"></span>Force theme palette for text（对文本强制使用主题调色板） | 颜色 · 将 RGB 与扩展文本颜色映射到最接近的主题颜色，随后修正对比度。<span hidden>In Settings &gt; Terminal.</span> <span hidden>force theme colors, 256 colors, truecolor, rgb, ansi, extended colors, nearest, palette</span> |
| <span id="setting-terminal-cursor-style" data-entry="Cursor style"></span>Cursor style（光标样式） | 光标 · 选择方块、竖线或下划线光标。<span hidden>In Settings &gt; Terminal.</span> <span hidden>cursor, caret, shape, block, bar, beam, underline</span> |
| <span id="setting-terminal-blink-speed" data-entry="Blink speed"></span>Blink speed（闪烁速度） | 光标 · 让光标慢速、正常、快速闪烁或完全不闪烁。<span hidden>In Settings &gt; Terminal.</span> <span hidden>cursor, blink, blinking, flash, solid, steady, off, slow, fast</span> |
| <span id="setting-terminal-force-style" data-entry="Force style"></span>Force style（强制光标样式） | 光标 · 当程序请求更改光标样式时，保持你设定的样式。<span hidden>In Settings &gt; Terminal.</span> <span hidden>cursor, override, ignore, lock, shape, decscusr</span> |
| <span id="setting-terminal-autocorrect" data-entry="Autocorrect"></span>Autocorrect（自动更正） | 键盘 · 允许键盘自动更正和预测词语。<span hidden>In Settings &gt; Terminal.</span> <span hidden>typing, auto correction, autocorrection, predictive text, spelling</span> |
| <span id="setting-terminal-keep-keyboard-open" data-entry="Keep keyboard open"></span>Keep keyboard open（保持键盘展开） | 键盘 · 返回终端时重新展开键盘。<span hidden>In Settings &gt; Terminal.</span> <span hidden>keyboard, background, reopen, restore, focus</span> |
| <span id="setting-terminal-key-repeat" data-entry="Key repeat"></span>Key repeat（按键重复） | 外接硬件键盘 · 在外接键盘上按住按键时重复输入。<span hidden>In Settings &gt; Terminal.</span> <span hidden>hardware keyboard, magic keyboard, external keyboard, hold, held, repeating, backspace, delete, arrows, accessibility</span> |
| <span id="setting-terminal-delay-until-repeat" data-entry="Delay until repeat"></span>Delay until repeat（重复前延迟） | 外接硬件键盘 · 按住按键多长时间后开始重复输入。<span hidden>In Settings &gt; Terminal.</span> <span hidden>hardware keyboard, key repeat, delay, wait, hold, seconds, speed</span> |
| <span id="setting-terminal-key-repeat-interval" data-entry="Key repeat interval"></span>Key repeat interval（按键重复间隔） | 外接硬件键盘 · 按住按键时重复输入的速率。<span hidden>In Settings &gt; Terminal.</span> <span hidden>hardware keyboard, key repeat, rate, speed, fast, slow, seconds, interval</span> |
| <span id="setting-terminal-repeat-held-letters" data-entry="Repeat held letters"></span>Repeat held letters（重复按住的字母） | 外接硬件键盘 · 重复输入按住的字母，而非显示变音符号菜单。<span hidden>In Settings &gt; Terminal.</span> <span hidden>hardware keyboard, accents, accented, accent menu, alternate characters, diacritics, long press, press and hold, letters, symbols</span> |
| <span id="setting-terminal-key-bar-layout" data-entry="Key Bar Layout"></span>Key Bar Layout（按键栏布局） | 按键栏 · 排列、隐藏和重新排序按键栏的内置按键。<span hidden>In Settings &gt; Terminal.</span> <span hidden>arrows, escape, tab, control, option, shift, paste, home, end, page up, page down, delete, return, rearrange, reorder, hide keys</span> |
| <span id="setting-terminal-shortcut-groups" data-entry="Shortcut Groups"></span>Shortcut Groups（快捷键分组） | 按键栏 · 添加 Control 快捷键、功能键以及自定按键。<span hidden>In Settings &gt; Terminal.</span> <span hidden>function keys, f1, ctrl, control, custom keys, slash commands, hotkeys, accessory</span> |
| <span id="setting-terminal-characters" data-entry="Characters"></span>Characters（字符按键） | 选择标点符号按键。<span hidden>In Settings &gt; Terminal.</span> <span hidden>punctuation, shell characters, symbols, tilde, pipe, slash</span> |
| <span id="setting-terminal-use-symbols" data-entry="Use symbols"></span>Use symbols（使用符号） | 按键栏 · 显示符号而非缩写的按键名称。<span hidden>In Settings &gt; Terminal.</span> <span hidden>keyboard, key bar, icons, control, option, shift</span> |
| <span id="setting-terminal-haptic-feedback" data-entry="Haptic feedback"></span>Haptic feedback（触觉反馈） | 按键栏 · 按下按键栏按钮时感受轻微触感反馈。<span hidden>In Settings &gt; Terminal.</span> <span hidden>keyboard, vibration, vibrate, touch</span> |
| <span id="setting-terminal-command-palette" data-entry="Command palette"></span>Command palette（命令面板说明） | 按键栏 · 了解如何打开命令以及使用修饰键。<span hidden>In Settings &gt; Terminal.</span> <span hidden>keyboard, shortcuts, command shift p, control, option, shift, paste</span> |
| <span id="setting-terminal-smooth-scrolling" data-entry="Smooth scrolling"></span>Smooth scrolling（平滑滚动） | 滚动 · 平滑滚动历史记录，而非按单行滚动。<span hidden>In Settings &gt; Terminal.</span> <span hidden>scroll, scrollback, history, pixel, fling, momentum, drag</span> |
| <span id="setting-terminal-smooth-terminal-resizing" data-entry="Smooth terminal resizing"></span>Smooth terminal resizing（平滑调整终端大小） | 调整大小 · 在终端改变大小后立即重排文本。<span hidden>In Settings &gt; Terminal.</span> <span hidden>smooth resize, resizing, reflow, re-wrap, rewrap, rotation, rotate, orientation, jitter, jump, flicker, stage manager, split view, preview, on, off</span> |
| <span id="setting-terminal-prefer-generated-titles" data-entry="Prefer generated titles"></span>Prefer generated titles（优先使用生成的标题） | 标题 · 显示正在运行的程序及其目录，而非 shell 标题。<span hidden>In Settings &gt; Terminal.</span> <span hidden>titles, tab title, window title, program name, directory, shell title, osc, rename</span> |

## 远程主机

管理已保存的主机、连接、端口转发以及每台主机启动的 shell。位于“设置”>“远程主机”。 <span hidden>server, add, pair, connect, reconnect, edit, delete, remove, startup command, shell, default shell, login shell, nushell, zsh, fish, port forwarding, forward, forwards, tunnel, localhost, ssh `-L`</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-remote-hosts-ssh-key" data-entry="SSH Key"></span>SSH Key（SSH 密钥） | 创建或导入 Rex 登录 `ssh://` 主机所用的密钥，以及其受信任的主机密钥。<span hidden>In Settings &gt; Remote Hosts.</span> <span hidden>ssh, key, private key, public key, authorized_keys, secure enclave, import, passphrase, ed25519, ecdsa, host key, fingerprint, known hosts, trust</span> |

## 开发者模式

开发者 · 显示用于开发与调试的设置项。位于“设置”>“开发者模式”。 <span hidden>developer, debug, diagnostics</span>

| 设置项 | 说明 |
| --- | --- |
| <span id="setting-developer-mode-network-diagnostics" data-entry="Network Diagnostics"></span>Network Diagnostics（网络诊断） | 在开启“开发者模式”时，在屏幕上悬浮显示网络路径与主机连接状态。<span hidden>In Settings &gt; Developer Mode. Needs Developer Mode.</span> <span hidden>debug, network, path, wi-fi, cellular, reconnect, overlay</span> |
| <span id="setting-developer-mode-cursor-shaders" data-entry="Cursor shaders"></span>Cursor shaders（光标着色器） | 实验性功能 · 在开启“开发者模式”时，在光标后方绘制拖尾着色器效果，例如 Warp、Comet 或 Blaze。<span hidden>In Settings &gt; Developer Mode. Needs Developer Mode.</span> <span hidden>cursor, cursor trail, cursor effect, cursor animation, smear, glow, warp, sweep, comet, blaze, tapered, rainbow, gradient, frozen, ghostty shader, custom-shader, shadertoy, shader, experimental</span> |

## 关于

关于 · 查看 App 的版本和设备信息，并可将其复制以用于提交错误报告。位于“设置”>“关于”。 <span hidden>version, build, commit, device, model, ios, system, bug report, feedback, copy version info, copy debug info, diagnostics, support, license, open source, acknowledgements, fonts</span>
