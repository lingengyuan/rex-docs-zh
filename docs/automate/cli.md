> 原文：https://www.superlogical.com/rex/docs/automate/cli
> 原文版本：d8c8bfe9d855（抓取于 2026-11-13）

# CLI

`rex` 是 Rex 的命令行界面（CLI）。

`rex` 既是 Rex 的管理工具，也是自动化的基础。作为管理工具，它可以创建会话、拆分窗格、列出活跃客户端、强制断开客户端连接等。作为自动化工具，它提供了完整且强大的 Lua 脚本接口。

Rex 会将 `rex` 添加到其打开的每个终端的 `PATH` 中，并配置好上下文环境，因此 CLI 能够直接感知当前所在的会话、正在查看的块等信息。

如果找不到 `rex` 命令，详见 [PATH](#path)。

打开终端尝试以下命令：

```sh
rex ls                 # 列出所有会话
rex session inspect    # 显示当前所在会话的详细信息
rex block inspect      # 显示当前输入所在终端的详细信息
```

运行 `rex help` 可以查看所有命令，运行 `rex help <command>` 可以查看指定命令的详细信息。

## 概念分类

Rex 将工作划分为四类对象。每个命令都会作用于其中一个或多个对象。

- **会话**（session）是一组相关工作的集合，例如一个项目。无论是否有客户端在查看，服务端都会保持会话持续运行。
- **窗口**（window）是会话内的一个标签页，用于容纳块的布局。
- **块**（block）是窗口中的一个应用，目前是指终端。
- **客户端**（client）是连接到服务端的程序，例如应用本身。当需要让应用自身执行操作时（例如打开命令面板），就会涉及客户端。

每个对象都有一个永不改变且不会复用的 ID，例如 `block:01a10d99-0c06-7795-bf67-798ce4c36a33`。会话、窗口、块和客户端还可以拥有标签（label），标签是用户自行指定且可以修改的名称。

## 命令目标

在不指定任何选项时，CLI 命令会根据其上下文执行操作。在 Rex 终端中，上下文即为该终端自身的块和会话，因此 `rex split` 会直接拆分输入命令的当前终端。Rex 通过在每个终端中设置的三个环境变量感知当前位置：

| 环境变量 | 内容 |
| --- | --- |
| `REX_SESSION` | 终端所属会话的 ID |
| `REX_BLOCK` | 终端自身块的 ID |
| `REX_SERVER` | 运行该终端的服务端地址 |

要对其他位置执行操作，可以通过选项指定目标：

| 选项 | 指定对象 |
| --- | --- |
| `-s`, `--session` | 会话 |
| `-w`, `--window` | 会话内的窗口 |
| `-b`, `--block` | 块 |
| `-C`, `--client` | 客户端，可通过 `REX_CLIENT` 设置默认值 |
| `-S`, `--server` | 服务端，可通过 `rex hosts` 中的主机标签或地址指定，可通过 `REX_SERVER` 设置默认值 |

```sh
rex send -s build -w 2 'make test'   # 在 "build" 会话的第 2 个窗口中输入
rex capture -b logs                  # 输出标签为 "logs" 的块的屏幕内容
rex -S studio ls                     # 列出标签为 "studio" 的主机上的会话
```

### 目标匹配规则

Rex 会按以下顺序尝试匹配会话、窗口、块或客户端目标（例如 `-C`），并在找到第一类匹配时停止查找：

1. 完整 ID，例如 `session:01a10cf3-2655-7e48-9b9c-43dd6612bef5`。
2. 不区分大小写的标签，例如 `build`。
3. 位置序号，从 1 开始计数。窗口按标签页顺序编号，因此 `-w 2` 表示第二个标签页。
4. ID 的末尾部分，长度至少为 4 个字符，例如 `12bef5`。列表类命令会打印这些短 ID。

如果一个目标匹配到多个对象，命令会在不更改任何内容的情况下终止，列出匹配到的对象，并以状态码 3 退出：

```
Error: session target "work" is ambiguous
  first   …001234
  second  …00abcd
```

服务端是例外情况。`-S` 仅接收主机标签或地址；包含端口号的值始终被视作地址。

在命令行提示符下使用标签很方便，但标签可以修改，且不同对象可能重名。在需要稳定运行的脚本中，应当保存命令返回的 ID 并使用该 ID。

## 机器可读输出

大多数命令默认输出便于人类阅读的表格。传入 `--json` 可以改为获取 JSON 输出，其解析格式更稳定，且包含完整 ID：

```
$ rex ls --json
{
  "sessions": [
    {
      "session_id": "session:01a10cf3-2655-7e48-9b9c-43dd6612bef5",
      "label": "Research"
    },
    {
      "session_id": "session:01a10d97-414b-79ee-9988-4d96d804ef90",
      "label": "SL Website"
    }
  ]
}
```

退出状态码说明了命令的结束状态：

| 状态码 | 含义 |
| --- | --- |
| 0 | 命令执行成功 |
| 1 | 命令执行失败 |
| 2 | 命令行参数无效 |
| 3 | 未找到目标或目标不明确 |
| 4 | 无法连接到服务端 |
| 130 | 命令被中断 |

等待程序执行的命令（如 `rex wait` 和 `rex run --wait`）会改为以该程序的退出状态码退出。

## PATH

Rex 打开终端时，会将服务端 `rex` 可执行文件所在的目录放置在 `PATH` 的最前面。它还会将 `REX_BIN_DIR` 设置为同一目录。Shell 的启动文件在此之后运行。如果启动文件将 `PATH` 覆盖为固定列表，就会遗漏 `rex`；如果重排 `PATH`，可能会导致其他版本的 `rex` 优先于匹配服务端的版本。

可以对比两者进行检查：

```sh
echo "$REX_BIN_DIR"
echo "$PATH"
```

如果 `PATH` 不是以 `REX_BIN_DIR` 开头，请在 Shell 启动文件的末尾将其重新添加到最前面。如果将其添加到 `PATH` 的末尾，仍可能优先匹配到其他 `rex` 副本。

```sh
# ~/.zshrc 或 ~/.bashrc
if [ -n "$REX_BIN_DIR" ]; then
    export PATH="$REX_BIN_DIR:$PATH"
fi
```

```fish
# ~/.config/fish/config.fish
if set -q REX_BIN_DIR
    fish_add_path --path --prepend --move $REX_BIN_DIR
end
```

### Nix

NixOS 和 nix-darwin 每次启动 Shell 时都会将 `PATH` 设置为固定列表。只要 `PATH` 中包含 `/run/current-system/sw/bin`，就会受到影响，即使仅使用 Nix 安装了 Shell 也是如此。在系统配置中添加相同的检查，使其在每个交互式 `bash` 和 `zsh` 中运行：

```nix
environment.interactiveShellInit = ''
  if [ -n "$REX_BIN_DIR" ]; then
    export PATH="$REX_BIN_DIR:$PATH"
  fi
'';
```

对于 `fish`，将上述 `fish` 示例配置到 `programs.fish.interactiveShellInit` 中。使用 home-manager 时，使用 Shell 对应的初始化选项，例如 `programs.zsh.initContent`。不要将 `REX_BIN_DIR` 添加到 `home.sessionPath`，因为在 Rex 外部该变量为空，会导致在 `PATH` 中添加一个空条目。
