# 术语表

译文中的术语以本表为准。新增术语先加到这里，再用于正文。

| 原文 | 译文 | 说明 |
| --- | --- | --- |
| session | 会话 | Rex 的工作单元，由服务端保持运行 |
| window | 窗口 | 会话内的一个标签页，容纳块的布局 |
| block | 块 | 窗口中的一个应用，目前是终端 |
| pane | 窗格 | 与块指同一终端区域；命令和操作名中的 `pane` 不译 |
| client | 客户端 | 连接到服务端的程序，例如 macOS 和 iOS 应用 |
| server | 服务端 | 运行会话的进程或机器 |
| host | 主机 | `rex hosts` 中的条目 |
| label | 标签 | 用户自定、可修改的名称 |
| target | 目标 | CLI 命令作用的对象 |
| binding | 绑定 | 键到操作的映射 |
| key sequence | 按键序列 | 依次按下的多个键 |
| key mode | 按键模式 | 只在激活期间生效的一组快捷键 |
| action | 操作 | 内置操作名保留英文，例如 `pane.split` |
| command palette | 命令面板 | |
| terminal | 终端 | |
| scrollback | 回滚缓冲区 | |
| personal server | 个人服务端 | |
| shared server | 共享服务端 | |
| login server | 登录服务端 | |

## 不译内容

- 命令、参数、环境变量、配置项、API 方法名：保留原文，放在行内代码中。
- 产品名称和通道名：Rex、Snapshot、Bleeding Edge、Preview、Tailscale 等保持英文。
- 界面中的按钮和菜单名：首次出现时写英文，必要时在括号中加中文说明。
