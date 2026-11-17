> 原文：https://www.superlogical.com/rex/docs/reference/cli
> 原文版本：685cd528cc2c（抓取于 2026-11-17）

# CLI 命令

本页列出所有公开的 `rex` 命令与标志。有关其使用方法，参见 [CLI](../automate/cli.md)。任何带有 [Snapshot](../linux/installation.md#发布通道) 标记的内容均处于 Snapshot 通道，尚未进入 Preview。

<div class="reference-page commands" hidden></div>

## 常用命令

### `rex new [LABEL] [-- COMMAND...]`

创建一个会话。

| 选项 | 说明 |
| --- | --- |
| `-c, --cwd string` | 终端的工作目录。 |
| `--keep-open` | 命令退出后保持终端打开。 |
| `--shell SHELL` | 通过 SHELL 的登录环境运行 COMMAND（none 则直接启动）。 |
| `--interactive` | 同时读取 Shell 的交互式启动文件（如 ~/.zshrc）。 |
| `--window string` | 第一个窗口的标签。 |
| `--json` | 将创建的会话以 JSON 格式输出。 |

### `rex ls`

列出会话。

| 选项 | 说明 |
| --- | --- |
| `--json` | 将会话列表以 JSON 格式输出。 |
| `-q, --quiet` | 仅打印 ID，每行一个。 |
| `--short` | 显示简短 ID（`--short=false` 显示完整 ID）。默认为 `true`。 |

### `rex run [flags] -- COMMAND...`

在新块中运行命令。

在新终端块中运行命令。

COMMAND 通过登录 Shell 的环境运行，但不加载其交互式配置，因此 profile 变量与 PATH 生效，而别名（alias）不生效。对于通过交互式配置添加 PATH 的程序，使用 `--interactive` 同时读取该配置（如 ~/.zshrc）。使用 `--shell` 选择其他 Shell，或使用 `--shell=none` 直接启动 COMMAND。

默认情况下，Rex 将该块置于新窗口中。使用 `--split` 将其置于现有块旁。使用 `--focus=false` 保持活动窗口不变。指定 `--wait` 时，Rex 会输出创建结果，然后等待并返回终端子进程的退出状态码。

| 选项 | 说明 |
| --- | --- |
| `--split DIRECTION` | 将新块置于锚点相对的 DIRECTION 方向（right、left、above 或 below）。 |
| `--ratio PCT` | 为新块分配拆分区域的 PCT 百分比。默认为 `50`。 |
| `-b, --block BLOCK` | 将 BLOCK 用作拆分锚点（默认为获得焦点的块）。 |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `-w, --window string` | 将作用域限定在窗口 WINDOW。 |
| `-c, --cwd string` | 终端的工作目录。 |
| `--keep-open` | 命令退出后保持终端打开。 |
| `--shell SHELL` | 通过 SHELL 的登录环境运行 COMMAND（none 则直接启动）。 |
| `--interactive` | 同时读取 Shell 的交互式启动文件（如 ~/.zshrc）。 |
| `--label TEXT` | 将新块的标签设置为 TEXT。 |
| `--focus` | 聚焦新块。默认为 `true`。 |
| `--json` | 将创建结果以 JSON 格式输出。 |
| `--wait` | 等待并返回终端子进程的退出状态码。 |

```sh
rex run -- htop
rex run --wait -- go test ./...
rex run --split=below --ratio 30 -- tail -f app.log
rex run -b editor --split=left -- lazygit
rex run -s build -- make
rex run --interactive -- opencode
rex run --shell=none -- /opt/tool/bin/x
```

### `rex split [flags] [-- COMMAND...]`

拆分获得焦点的块。

为 Shell 或命令创建终端块。

COMMAND 通过登录 Shell 的环境运行，但不加载其交互式配置。使用 `--interactive` 同时读取该配置，使用 `--shell` 选择其他 Shell，或使用 `--shell=none` 直接启动 COMMAND。

默认情况下，Rex 会拆分当前焦点的块并将新块置于其右侧。使用 `-b` BLOCK 选择其他锚点，或使用 `--split` 选择其他方向。使用 `--focus=false` 保持当前焦点不变。指定 `--wait` 时，Rex 会输出创建结果，然后等待并返回终端子进程的退出状态码。使用 `rex run` 则将块置于新窗口中。

| 选项 | 说明 |
| --- | --- |
| `--split DIRECTION` | 将新块置于锚点相对的 DIRECTION 方向（right、left、above 或 below）。默认为 `right`。 |
| `--ratio PCT` | 为新块分配拆分区域的 PCT 百分比。默认为 `50`。 |
| `-b, --block BLOCK` | 将 BLOCK 用作拆分锚点（默认为获得焦点的块）。 |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `-w, --window string` | 将作用域限定在窗口 WINDOW。 |
| `-c, --cwd string` | 终端的工作目录。 |
| `--keep-open` | 命令退出后保持终端打开。 |
| `--shell SHELL` | 通过 SHELL 的登录环境运行 COMMAND（none 则直接启动）。 |
| `--interactive` | 同时读取 Shell 的交互式启动文件（如 ~/.zshrc）。 |
| `--label TEXT` | 将新块的标签设置为 TEXT。 |
| `--focus` | 聚焦新块。默认为 `true`。 |
| `--json` | 将创建结果以 JSON 格式输出。 |
| `--wait` | 等待并返回终端子进程的退出状态码。 |

```sh
rex split
rex split --split=below
rex split -b editor --split=left -- lazygit
rex split --wait -- make
rex split -- htop
```

### `rex do (ACTION | SCRIPT | -e CODE) [KEY=VALUE...]`

执行操作或运行 Lua 脚本。

按名称执行操作，或运行 Lua 脚本。

不带点的名称是由 init.lua 通过 rex.action 定义的操作。以客户端前缀开头的名称（如 pane.split）由目标客户端执行。以块类型创建者名称开头的名称（如 com.superlogical.terminal.reset）是块操作或方法。运行 “rex actions” 可列出这些操作。

来自 init.lua 的操作可以使用 rex.ui.input 或 rex.ui.pick 提出问题。`rex do` 无法自行显示该问题，因此所有已连接的 Rex 应用都会显示它，`rex do` 则会等待有人在其中某个应用上作答。默认情况下，`rex do` 会一直等待直到操作完成，无论耗时多久。使用 `--timeout` 可限制等待时间。超过时限后，`rex do` 会停止该操作并以状态码 1 退出。

若要运行 Lua 脚本，请提供其路径。当第一个参数包含斜杠（Windows 上为反斜杠）或以 .lua 结尾时，该参数被视为脚本路径。使用 - 从标准输入读取脚本，或使用 `-e` 在命令行中直接传入代码。脚本可以调用与 init.lua 相同的 API。其返回值与操作结果的打印方式相同。在脚本中，rex.invoke 会运行脚本自身定义的操作，并请求服务端运行其他操作。

脚本还可以调用 “rex hosts” 列出的主机。rex.servers() 返回这些主机的标签，rex.server(LABEL) 返回与 rex 相同的 API 辅助对象，其调用将定向到该主机。`rex do` 在脚本首次调用主机时与其建立连接，并保持连接直至脚本结束。`--server` 仅选择 rex 自身调用的服务端。

指定 `--action` NAME 时，`rex do` 会先运行该脚本，然后运行脚本中定义为 NAME 的操作并打印该操作的结果。键值对会针对该操作的模式进行类型检查。在服务端重新加载前，可借此测试 init.lua 中的操作。

注册了 rex.on 处理程序的脚本在执行完最后一行后会继续保持运行，并在事件到达时逐一运行其处理程序。它会监听由 `-s`、`-b` 或环境变量指定的会话；如果均未指定，则监听所有会话。`--all` 使其监听所有会话，包括后续创建的会话。运行期间，rex.session.attach 与 rex.session.detach 可改变其监听范围。

此类脚本会一直运行，直到调用 rex.stop(CODE)，随后 `rex do` 以 CODE 退出；若省略则以 0 退出。当 `--for` DURATION 超时，或者当其监听的最后一个会话被销毁时（除非监听所有会话），脚本也会以状态码 0 停止。Ctrl-C 会以状态码 130 停止脚本。处理程序发生失败时会进行报告，且脚本继续运行。使用 `--fail-fast` 时，首次失败即以状态码 1 退出。

任何脚本均可暂停。rex.sleep(SECONDS) 等待指定时间，rex.wait(EVENT, FILTER, TIMEOUT) 等待特定事件（如脚本启动的命令退出）。在此期间，脚本中的其他内容不会执行。`--for` 不会中断脚本顶层的暂停。

参数为 KEY=VALUE 键值对，针对操作的模式进行类型检查。使用 `--args` 可改用 JSON 对象传入，或使用 @FILE 从文件读取，或使用 - 从标准输入读取。脚本通过 rex.args 读取其参数。脚本没有模式定义，因此每个值的类型由其书写方式决定：n=2 为数字，name=x 为字符串。

客户端操作需要目标客户端。使用 `-C` 指定客户端，或设置 REX_CLIENT。若均未指定，当恰好有一个应用客户端连接时，将使用该客户端。init.lua 操作排队的客户端操作会发送给该客户端，脚本中对 rex.client.queue 的调用亦是如此。

| 选项 | 说明 |
| --- | --- |
| `--args JSON` | 以 JSON 对象形式传递参数（@FILE，或 - 代表标准输入）。 |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `-b, --block BLOCK` | 将操作应用于 BLOCK（默认为获得焦点的块）。 |
| `--origin ORIGIN` | 将来源报告为 ORIGIN：key、palette、api 或 cli。默认为 `cli`。 |
| `-e, --eval CODE` | 将 CODE 作为 Lua 脚本运行。 |
| `-a, --action NAME` | 运行脚本中定义的操作 NAME。 |
| `--all` | 监听来自所有会话的事件。 |
| `--for DURATION` | 在 DURATION 后停止监听事件。 |
| `--fail-fast` | 在首个失败的 rex.on 处理程序处退出。 |
| `--json` | 以 JSON 格式打印结果。 |

```sh
rex do dev_layout branch=main
rex -C studio do pane.split direction=right
rex do com.superlogical.terminal.reset
rex -C studio do client.tab.goto index=2 --json
rex do ./layout.lua branch=main
rex do - < script.lua
rex do -e 'return rex.call("session.list")' --json
rex do notify.lua --args '{"title":"done"}'
rex do watch.lua --all --for 10m
rex do ~/.config/rex/init.lua --action dev_layout branch=main
```

### `rex send [TEXT]`

向终端发送输入

| 选项 | 说明 |
| --- | --- |
| `-b, --block string` | 发送至块 BLOCK。 |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `-w, --window string` | 将作用域限定在窗口 WINDOW。 |

```sh
rex send 'make test'
rex send -b logs $'\003'
printf 'y\n' | rex send
rex send -s build -w 2 'ls'
```

### `rex send-key KEY...`

向终端发送按键

每个 KEY 使用 Rex 的按键绑定语法。使用 + 连接修饰键，如 ctrl+c 或 shift+left。带方括号的名称（如 [Slash]）用于选择物理按键。默认情况下，Rex 对每个按键发送一次按下后紧接着一次释放。使用 `--action` 可改为发送单个操作。

Rex 使用美式键盘布局解析可打印字符，因为 send-key 不接收物理键盘输入。生成的文本和物理按键在其他布局上可能有所不同。当需要精确文本时，请使用 `rex send`。

| 选项 | 说明 |
| --- | --- |
| `-b, --block string` | 发送至块 BLOCK。 |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `-w, --window string` | 将作用域限定在窗口 WINDOW。 |
| `--action ACTION` | 为每个按键发送一个 ACTION：press、release 或 repeat。 |

```sh
rex send-key enter
rex send-key ctrl+c
rex send 'make test' && rex send-key enter
rex send-key -b logs ctrl+c
rex send-key shift+left shift+left
rex send-key --action release ctrl+[KeyQ]
```

### `rex capture`

打印终端的屏幕内容和回滚缓冲区。

打印终端块的屏幕内容和回滚缓冲区。

当省略 `--block` 时，如果 REX_BLOCK 指定了一个活跃块，Rex 将使用该块；否则使用默认窗口中获得焦点的块。text 是默认格式。html 保留渲染样式。vt 保留终端控制序列。输出始终以换行符结尾。

终端大约保留 64 MiB 的回滚缓冲区。在 80 列宽度下大约相当于 100,000 行纯文本，在更宽的终端或带样式输出中行数会更少。一旦达到上限，最旧的行将被丢弃。

| 选项 | 说明 |
| --- | --- |
| `-b, --block BLOCK` | 选择块 BLOCK。 |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `-w, --window string` | 将作用域限定在窗口 WINDOW。 |
| `--format FORMAT` | 输出 FORMAT：text、html 或 vt。默认为 `text`。 |
| `--trim` | 移除末尾空白行。 |
| `--unwrap` | 合并自动换行的行。 |

```sh
rex capture
rex capture -b logs --trim > screen.txt
rex capture --format=html > screen.html
rex capture -s build -w 2
```

### `rex kill SESSION...`

终止会话。

### `rex forward`

转发 TCP 端口。

### `rex forward new (-L|-R) [bind_address:]port:host:hostport...`

转发端口直至中断。

通过 Rex 服务端转发 TCP 连接，类似于 ssh `-L` 和 ssh `-R`。

`-L`（“客户端端口；服务端网络”）[bind_address:]port:host:hostport 在本机监听 &lt;port&gt;，并将每个本地连接从服务端连接到 &lt;host&gt;:&lt;hostport&gt;。

`-R`（“服务端端口；客户端网络”）[bind_address:]port:host:hostport 在服务端监听 &lt;port&gt;，并将每个远程连接从本机连接到 &lt;host&gt;:&lt;hostport&gt;。

绑定地址默认为 127.0.0.1；使用 * 代表所有网络接口。端口 0 将选择空闲端口。可按需多次指定 `-L` 和 `-R` 以创建多个转发。它们均由当前进程管理并具有相同的生命周期。

每个转发都是通过 `--session` 选择的会话（或默认会话）中的隧道块。`rex forward new` 在前台运行直至中断，然后关闭其块。运行期间除非指定 `-v`，否则不打印任何内容。

当与服务端的连接断开时，`rex forward new` 会重新连接并继续使用相同的块。断开时处于打开状态的 TCP 连接会被重置。

若转发对应的块被关闭（例如通过 `rex forward close`），该转发将停止。一旦没有剩余转发，`rex forward new` 便会退出。

被终止的 `rex forward new` 会留下其转发对应的块。从同一台机器再次建立相同的转发时，会接管该块而非新建一个，因此重新运行相同的命令即可继续使用。端口为 0 的 `-R` 转发始终会分配新端口。其他机器上的客户端仍可能回来使用的块会保持原样。

| 选项 | 说明 |
| --- | --- |
| `-L, --local stringArray` | 在本机监听 port 并从服务端连接到 host:hostport。 |
| `-R, --remote stringArray` | 在服务端监听 port 并从本机连接到 host:hostport。 |
| `-s, --session string` | 将转发对应的块保留在会话 SESSION 中。 |

### `rex forward open [flags] (URL | [host:]port | BLOCK)`

将本地端口转发至服务端目标并打开。

将本机上的端口转发至服务端可达的目标并打开该目标。这是 `rex forward new` `-L` 针对单端口转发常见场景的简化用法。

目标可以是一个 URL（如 http://localhost:8080/app 或 postgres://db/app）、host:port，或单个端口（代表服务端 localhost 上的该端口）。不带协议 scheme 的目标默认视为 http。不带端口的 URL 使用该协议的常用默认端口（如果已知）。

目标也可以是按 ID 或标签指定的终端块（即 rex block ls 中显示的标识）。此时转发会指向该终端中程序正在监听的端口（例如在其中启动的开发服务器），并以 http 方式打开。如果该终端中的程序监听了多个端口，`rex forward open` 会列出这些端口且不执行转发。凡是可被解析为 URL、host:port 或端口的参数都会始终按此类格式处理，因此若块的标签形如这类格式，请使用其 ID 来指定。服务端只查找仍附加到终端上的程序所监听的端口，因此会略过例如后台守护进程。

转发监听 `--bind` 与 `--port`，默认为 127.0.0.1 和一个空闲端口。一旦开始监听，`rex forward open` 会打印将主机和端口替换为转发监听地址的目标 URL，并打开该 URL。http 或 https URL 会发送给 $BROWSER（若已设置，为冒号分隔的命令列表，其中 %s 代表 URL）。其他 URL 或 $BROWSER 无法打开的 URL 会交给系统该协议的默认处理程序。`--no-open` 仅打印 URL 而不打开。

浏览器向 localhost 及转发端口发送请求，而非向目标自身的名称发送，因此检查 Host 头的网站，或使用自身名称证书提供 https 服务的网站，可能无法通过转发正常工作。

转发块会保留在通过 `--session` 指定的会话或默认会话中。对于终端块，转发块会保留在该终端所属的会话中，此时 `--session` 用于指定在哪个会话中查找该终端。

`rex forward open` 像 `rex forward new` 一样在前台运行，直到被中断或通过 `rex forward close` 关闭转发。

| 选项 | 说明 |
| --- | --- |
| `-b, --bind ADDRESS` | 监听 ADDRESS；* 代表所有网络接口。默认为 `127.0.0.1`。 |
| `-p, --port PORT` | 监听 PORT；0 会选择空闲端口。 |
| `-s, --session string` | 将转发对应的块保留在会话 SESSION 中。 |
| `--no-open` | 打印 URL 而不打开。 |

### `rex forward share [flags] (URL | [host:]port)`

将服务端端口转发至本机端的目标。

将服务端上的端口转发至本机可达的目标。这是 `rex forward new` `-R` 针对单端口转发常见场景的简化用法。

目标可以是一个 URL（如 http://localhost:3000）、host:port，或单个端口（代表本机 localhost 上的该端口）。不带端口的 URL 解析规则与 `rex forward open` 相同。

转发在服务端上监听 `--bind` 与 `--port`，默认为 127.0.0.1 和一个空闲端口。使用 `--bind` '*' 可允许其他机器连接。一旦开始监听，`rex forward share` 会打印监听位置：如果目标是 URL，则打印替换了主机和端口的目标 URL，否则打印 host:port。使用 `--bind` '*' 时，主机为 Rex 连接到的服务端地址。

客户端向服务端发送请求，而非向目标自身的名称发送，因此检查 Host 头的网站，或使用自身名称证书提供 https 服务的网站，可能无法通过转发正常工作。

`rex forward share` 像 `rex forward new` 一样在前台运行，直到被中断或通过 `rex forward close` 关闭转发。

| 选项 | 说明 |
| --- | --- |
| `-b, --bind ADDRESS` | 监听 ADDRESS；* 代表所有网络接口。默认为 `127.0.0.1`。 |
| `-p, --port PORT` | 监听 PORT；0 会选择空闲端口。 |
| `-s, --session string` | 将转发对应的块保留在会话 SESSION 中。 |

### `rex forward ls`

列出转发。

列出会话中的转发：由 `rex forward new` 及其他客户端创建的隧道块。

STATE（状态）在承载转发的客户端连接时为 active（活跃），断开连接但可能重新连回时为 away（离开），在没有任何客户端承载时（例如其 `rex forward new` 被杀死后）为 orphaned（孤立）。在服务端监听的孤立转发仍会接受连接，随后这些连接将超时，因此 `rex forward ls` 会对孤立转发发出警告；可使用 `rex forward close` 关闭它们。

DIRECTION（方向）显示转发监听的位置及其连接来源：client -> server 为 `-L` 转发，server -> client 为 `-R` 转发。客户端未报告的字段显示为 -。

| 选项 | 说明 |
| --- | --- |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `-A, --all` | 列出所有会话中的转发。 |
| `--json` | 将转发列表以 JSON 格式输出。 |
| `-q, --quiet` | 仅打印 ID，每行一个。 |
| `--short` | 显示简短 ID（`--short=false` 显示完整 ID）。默认为 `true`。 |

### `rex forward close [FORWARD...]`

通过关闭隧道块来关闭转发。提供如 rex forward ls 显示的转发 ID，或使用 `--orphaned` 关闭会话中的所有孤立转发，或使用 `--all` 关闭会话中的所有转发。

承载已关闭转发的 `rex forward new` 会停止该转发，并在没有剩余转发时退出。

| 选项 | 说明 |
| --- | --- |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `--orphaned` | 关闭会话中的所有孤立转发。 |
| `--all` | 关闭会话中的所有转发。 |


## 布局

### `rex focus TARGET|DIRECTION`

聚焦块或窗口。

方向 left、right、up 和 down 按位置在块之间移动。next 和 prev 按布局顺序在块之间移动。焦点在到达布局边缘或顺序末尾时停止。使用 `--wrap` 从另一侧继续环回移动。

目标可以是块或窗口的 ID、标签或 ID 后缀。正整数按基于 1 的位置选择窗口。如果目标同时匹配块和窗口，请使用完整 ID 来选择预期资源。

| 选项 | 说明 |
| --- | --- |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `-w, --window string` | 将作用域限定在窗口 WINDOW。 |
| `--wrap` | 到达边缘时从另一侧环回继续。 |

```sh
rex focus left
rex focus left --wrap
rex focus next --wrap
rex focus 2
rex focus logs
rex focus -s build editor
```

### `rex zoom [BLOCK]`

将块缩放至填满其窗口。

缩放仅改变块的显示方式，不改变底层的窗口布局。若不指定 `--on` 或 `--off`，该命令会切换当前的缩放状态。使用 `--on` 或 `--off` 可显式设置状态。

BLOCK 可以作为位置参数传入，也可以通过 `--block` 传入。若省略 BLOCK，当 REX_BLOCK 指定了一个活跃块时，Rex 将使用该块；否则使用默认窗口中获得焦点的块。

| 选项 | 说明 |
| --- | --- |
| `-b, --block BLOCK` | 选择块 BLOCK。 |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `-w, --window string` | 将作用域限定在窗口 WINDOW。 |
| `--on` | 启用缩放。 |
| `--off` | 禁用缩放。 |

```sh
rex zoom
rex zoom --off
rex zoom -b logs --on
```

### `rex move [BLOCK] DIRECTION ANCHOR`

将块移动至另一个块旁边。

将块移动到锚点块旁边。

DIRECTION 选择 BLOCK 相对于 ANCHOR 的新位置。必须为 right、left、above 或 below。两个块可以位于不同窗口中，但必须都可见且属于同一会话。

若省略 BLOCK，当 REX_BLOCK 指定了一个可见块时，Rex 将使用该块；否则使用默认窗口中获得焦点的块。`--ratio` 标志设置分配给 BLOCK 的拆分比例百分比。PCT 必须介于 1 和 99 之间。

如果块标签也是方向词，请通过其完整块 ID 或十六进制 ID 后缀来标识该块。

| 选项 | 说明 |
| --- | --- |
| `--ratio PCT` | 为移动的块分配拆分区域的 PCT 百分比。默认为 `50`。 |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `-w, --window string` | 将作用域限定在窗口 WINDOW。 |

```sh
rex move below editor
rex move logs right editor --ratio 30
rex move c2a9f3 above 1bc2a9 -s work
```

### `rex swap BLOCK OTHER`

交换两个块。

交换两个可见块的布局位置。

这两个块可以位于不同窗口中，但必须属于同一会话。Rex 会在更改布局前解析两个块参数。周围的布局保持不变。

| 选项 | 说明 |
| --- | --- |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `-w, --window string` | 将作用域限定在窗口 WINDOW。 |

```sh
rex swap editor logs
rex swap c2a9f3 1bc2a9
```

### `rex resize [BLOCK]`

调整块的大小。

## 资源

### `rex session`

管理会话。

### `rex session new [LABEL] [-- COMMAND...]`

创建一个会话。

| 选项 | 说明 |
| --- | --- |
| `-c, --cwd string` | 终端的工作目录。 |
| `--keep-open` | 命令退出后保持终端打开。 |
| `--shell SHELL` | 通过 SHELL 的登录环境运行 COMMAND（none 则直接启动）。 |
| `--interactive` | 同时读取 Shell 的交互式启动文件（如 ~/.zshrc）。 |
| `--window string` | 第一个窗口的标签。 |
| `--json` | 将创建的会话以 JSON 格式输出。 |

### `rex session ls`

列出会话。

| 选项 | 说明 |
| --- | --- |
| `--json` | 将会话列表以 JSON 格式输出。 |
| `-q, --quiet` | 仅打印 ID，每行一个。 |
| `--short` | 显示简短 ID（`--short=false` 显示完整 ID）。默认为 `true`。 |

### `rex session inspect [SESSION]`

检查会话。

| 选项 | 说明 |
| --- | --- |
| `--json` | 将会话信息以 JSON 格式输出。 |

### `rex session rename [SESSION] LABEL`

重命名会话。

### `rex session move [SESSION] (--before S | --after S | --index N)`

将会话移动至会话顺序中的新位置。

会话顺序即 session ls 打印的顺序。它还决定了数字所指代的会话，因此在移动之后，“rex session inspect 1” 会显示当前排在第一位的会话。

`--before`、`--after` 或 `--index` 必须且只能指定其中一个。位置从 1 开始计数。超出末尾的索引会将该会话移至最后。将会话移动到其当前所在位置不会产生任何影响并返回成功。

若省略 SESSION，当设置了 REX_SESSION 时 Rex 将使用该变量；否则使用默认会话。

| 选项 | 说明 |
| --- | --- |
| `--before S` | 紧邻移动至会话 S 之前。 |
| `--after S` | 紧邻移动至会话 S 之后。 |
| `--index N` | 移动至从 1 开始的位置 N。 |

```sh
rex session move logs --before work
rex session move 3 --after 1
rex session move --index 1
rex session move build --index 99
```

### `rex session kill SESSION...`

终止会话。

### `rex window`

管理窗口。

### `rex window new [-s SESSION] [LABEL] [-- COMMAND...]`

在选定会话中创建窗口。新窗口默认成为活动窗口。使用 `--focus=false` 可保持活动窗口和获得焦点的块不变。如果会话中没有活动窗口，即使指定 `--focus=false`，新窗口也会成为活动窗口。

| 选项 | 说明 |
| --- | --- |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `-c, --cwd string` | 终端的工作目录。 |
| `--keep-open` | 命令退出后保持终端打开。 |
| `--shell SHELL` | 通过 SHELL 的登录环境运行 COMMAND（none 则直接启动）。 |
| `--interactive` | 同时读取 Shell 的交互式启动文件（如 ~/.zshrc）。 |
| `--focus` | 将新窗口设为活动窗口（`--focus=false` 保持当前窗口为活动状态）。默认为 `true`。 |
| `--json` | 将创建的窗口以 JSON 格式输出。 |

```sh
rex window new
rex window new logs -- tail -f app.log
rex window new logs --focus=false -- tail -f app.log
rex window new -s build tests
```

### `rex window ls`

列出窗口。

| 选项 | 说明 |
| --- | --- |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `-A, --all` | 列出所有会话中的窗口。 |
| `--json` | 将窗口列表以 JSON 格式输出。 |
| `-q, --quiet` | 仅打印 ID，每行一个。 |
| `--short` | 显示简短 ID（`--short=false` 显示完整 ID）。默认为 `true`。 |

### `rex window inspect [WINDOW]`

检查窗口。

| 选项 | 说明 |
| --- | --- |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `--json` | 将窗口信息以 JSON 格式输出。 |

### `rex window focus [WINDOW|next|prev]`

按 ID、标签、位置或 ID 后缀聚焦窗口。

若省略 WINDOW，当包含 REX_BLOCK 的窗口可用时聚焦该窗口；否则聚焦默认会话中的活动窗口。使用 next 或 prev 按窗口顺序移动。

| 选项 | 说明 |
| --- | --- |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `--wrap` | 在首尾处环回 next 和 prev。 |

### `rex window move [WINDOW] (--before W | --after W | --index N) [-s SESSION]`

在其会话的标签页顺序内移动窗口。

`--before`、`--after` 或 `--index` 必须且只能指定其中一个。窗口位置按 window ls 显示的相同顺序从 1 开始编号。超出末尾的索引会将该窗口移至最后。

若省略 WINDOW，当包含 REX_BLOCK 的窗口可用时 Rex 将使用该窗口；否则使用默认会话中的活动窗口。

| 选项 | 说明 |
| --- | --- |
| `--before W` | 紧邻移动至窗口 W 之前。 |
| `--after W` | 紧邻移动至窗口 W 之后。 |
| `--index N` | 移动至从 1 开始的位置 N。 |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |

```sh
rex window move logs --before editor
rex window move 3 --after 1
rex window move --index 1
rex window move -s work build --index 99
```

### `rex window rename [WINDOW] LABEL`

重命名窗口。

| 选项 | 说明 |
| --- | --- |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |

### `rex window close WINDOW...`

关闭窗口。

| 选项 | 说明 |
| --- | --- |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |


### `rex block`

管理块。

### `rex block new FLAVOR`

创建一个块。

### `rex block ls`

列出块。

| 选项 | 说明 |
| --- | --- |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `-w, --window string` | 将作用域限定在窗口 WINDOW。 |
| `-A, --all` | 列出所有会话中的块。 |
| `--json` | 将块列表以 JSON 格式输出。 |
| `-q, --quiet` | 仅打印 ID，每行一个。 |
| `--short` | 显示简短 ID（`--short=false` 显示完整 ID）。默认为 `true`。 |

### `rex block inspect [BLOCK]`

检查块。

| 选项 | 说明 |
| --- | --- |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `-w, --window string` | 将作用域限定在窗口 WINDOW。 |
| `--json` | 将块信息以 JSON 格式输出。 |

### `rex block focus [BLOCK]`

按 ID、标签或 ID 后缀聚焦块。

若省略 BLOCK，当 REX_BLOCK 指定的块可用时聚焦该块；否则聚焦默认窗口中的当前块。

| 选项 | 说明 |
| --- | --- |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `-w, --window string` | 将作用域限定在窗口 WINDOW。 |

### `rex block types`

列出块类型。

| 选项 | 说明 |
| --- | --- |
| `--json` | 将块类型以 JSON 格式输出。 |

### `rex block send [TEXT]`

向终端发送输入

| 选项 | 说明 |
| --- | --- |
| `-b, --block string` | 发送至块 BLOCK。 |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `-w, --window string` | 将作用域限定在窗口 WINDOW。 |

```sh
rex send 'make test'
rex send -b logs $'\003'
printf 'y\n' | rex send
rex send -s build -w 2 'ls'
```

### `rex block send-key KEY...`

向终端发送按键

每个 KEY 使用 Rex 的按键绑定语法。使用 + 连接修饰键，如 ctrl+c 或 shift+left。带方括号的名称（如 [Slash]）用于选择物理按键。默认情况下，Rex 对每个按键发送一次按下后紧接着一次释放。使用 `--action` 可改为发送单个操作。

Rex 使用美式键盘布局解析可打印字符，因为 send-key 不接收物理键盘输入。生成的文本和物理按键在其他布局上可能有所不同。当需要精确文本时，请使用 `rex send`。

| 选项 | 说明 |
| --- | --- |
| `-b, --block string` | 发送至块 BLOCK。 |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `-w, --window string` | 将作用域限定在窗口 WINDOW。 |
| `--action ACTION` | 为每个按键发送一个 ACTION：press、release 或 repeat。 |

```sh
rex send-key enter
rex send-key ctrl+c
rex send 'make test' && rex send-key enter
rex send-key -b logs ctrl+c
rex send-key shift+left shift+left
rex send-key --action release ctrl+[KeyQ]
```

### `rex block capture`

打印终端的屏幕内容和回滚缓冲区。

打印终端块的屏幕内容和回滚缓冲区。

当省略 `--block` 时，如果 REX_BLOCK 指定了一个活跃块，Rex 将使用该块；否则使用默认窗口中获得焦点的块。text 是默认格式。html 保留渲染样式。vt 保留终端控制序列。输出始终以换行符结尾。

终端大约保留 64 MiB 的回滚缓冲区。在 80 列宽度下大约相当于 100,000 行纯文本，在更宽的终端或带样式输出中行数会更少。一旦达到上限，最旧的行将被丢弃。

| 选项 | 说明 |
| --- | --- |
| `-b, --block BLOCK` | 选择块 BLOCK。 |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `-w, --window string` | 将作用域限定在窗口 WINDOW。 |
| `--format FORMAT` | 输出 FORMAT：text、html 或 vt。默认为 `text`。 |
| `--trim` | 移除末尾空白行。 |
| `--unwrap` | 合并自动换行的行。 |

```sh
rex block capture
rex block capture -b logs --trim > screen.txt
rex block capture --format=html > screen.html
rex block capture -s build -w 2
```

### `rex block zoom [BLOCK]`

将块缩放至填满其窗口。

缩放仅改变块的显示方式，不改变底层的窗口布局。若不指定 `--on` 或 `--off`，该命令会切换当前的缩放状态。使用 `--on` 或 `--off` 可显式设置状态。

BLOCK 可以作为位置参数传入，也可以通过 `--block` 传入。若省略 BLOCK，当 REX_BLOCK 指定了一个活跃块时，Rex 将使用该块；否则使用默认窗口中获得焦点的块。

| 选项 | 说明 |
| --- | --- |
| `-b, --block BLOCK` | 选择块 BLOCK。 |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `-w, --window string` | 将作用域限定在窗口 WINDOW。 |
| `--on` | 启用缩放。 |
| `--off` | 禁用缩放。 |

```sh
rex block zoom
rex block zoom --off
rex block zoom -b logs --on
```

### `rex block move [BLOCK] DIRECTION ANCHOR`

将块移动至另一个块旁边。

将块移动到锚点块旁边。

DIRECTION 选择 BLOCK 相对于 ANCHOR 的新位置。必须为 right、left、above 或 below。两个块可以位于不同窗口中，但必须都可见且属于同一会话。

若省略 BLOCK，当 REX_BLOCK 指定了一个可见块时，Rex 将使用该块；否则使用默认窗口中获得焦点的块。`--ratio` 标志设置分配给 BLOCK 的拆分比例百分比。PCT 必须介于 1 和 99 之间。

如果块标签也是方向词，请通过其完整块 ID 或十六进制 ID 后缀来标识该块。

| 选项 | 说明 |
| --- | --- |
| `--ratio PCT` | 为移动的块分配拆分区域的 PCT 百分比。默认为 `50`。 |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `-w, --window string` | 将作用域限定在窗口 WINDOW。 |

```sh
rex block move below editor
rex block move logs right editor --ratio 30
rex block move c2a9f3 above 1bc2a9 -s work
```

### `rex block swap BLOCK OTHER`

交换两个块。

交换两个可见块的布局位置。

这两个块可以位于不同窗口中，但必须属于同一会话。Rex 会在更改布局前解析两个块参数。周围的布局保持不变。

| 选项 | 说明 |
| --- | --- |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `-w, --window string` | 将作用域限定在窗口 WINDOW。 |

```sh
rex block swap editor logs
rex block swap c2a9f3 1bc2a9
```

### `rex block stream BLOCK [DATA_REF]`

流式传输块数据。

### `rex block call METHOD [ARGS]`

调用块方法。

调用块公开的方法。

METHOD 为块方法名称。ARGS 必须为 JSON 对象。可直接传入该对象，或使用 @path 从文件读取，或使用 - 从标准输入读取。省略 ARGS 时，请求不发送任何参数。

当省略 `--block` 时，如果 REX_BLOCK 指定了一个活跃块，Rex 将使用该块；否则使用默认窗口中获得焦点的块。

方法结果为 JSON。写入终端的输出使用两个空格缩进。重定向输出保持在单行以便在脚本中使用。使用 `rex block inspect` 列出方法，使用 `rex block inspect` `--json` 查看其模式。

| 选项 | 说明 |
| --- | --- |
| `-b, --block BLOCK` | 选择块 BLOCK。 |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `-w, --window string` | 将作用域限定在窗口 WINDOW。 |

```sh
rex block call process
rex block call -b c2a9f3 write '{"data":"ls\n"}'
rex block call -b logs format @request.json
echo '{"format":"text","trim":true}' | rex block call format -
```

### `rex block rename [BLOCK] LABEL`

重命名块。

| 选项 | 说明 |
| --- | --- |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `-w, --window string` | 将作用域限定在窗口 WINDOW。 |

### `rex block close BLOCK...`

关闭块。

| 选项 | 说明 |
| --- | --- |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `-w, --window string` | 将作用域限定在窗口 WINDOW。 |

### `rex client`

管理客户端。

检查连接到服务端的客户端。

客户端指连接到服务端的一个程序，例如 Rex.app 或当前命令。每个客户端在连接时声明其类型，用户也可以为其设置标签。

### `rex client ls`

列出客户端。

列出连接到服务端的客户端。

每个客户端在连接时声明其类型。标签是用户为其指定的名称，两个客户端可以共用同一标签。类似当前命令的命令行客户端默认隐藏，除非指定 `--all`。指定 `--json` 时，输出为服务端的完整回复（包含命令行客户端）。使用 `-s` 仅列出附加到某一会话的客户端。

| 选项 | 说明 |
| --- | --- |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `--all` | 包含命令行客户端。 |
| `--json` | 将客户端列表以 JSON 格式输出。 |
| `-q, --quiet` | 仅打印 ID，每行一个。 |
| `--short` | 显示简短 ID（`--short=false` 显示完整 ID）。默认为 `true`。 |

```sh
rex client ls
rex client ls -s work
rex client ls --all
rex client ls -q
```

### `rex client inspect [CLIENT]`

检查客户端。

显示单个客户端及其提供的操作。

CLIENT 为客户端 ID、标签或 ID 后缀。未指定 CLIENT 时，`-C` 或 REX_CLIENT 指定客户端；若均未提供，当恰好有一个应用客户端连接时，使用该应用客户端。

| 选项 | 说明 |
| --- | --- |
| `--json` | 将客户端及其操作以 JSON 格式输出。 |

```sh
rex client inspect studio
rex client inspect 3f9a
rex client inspect --json
```


## 自动化

### `rex events`

实时流式传输服务端事件。

如果不带 `--session`，events 会跟踪整个服务端的会话创建、移除、状态变更以及服务端连通性。使用 `--session` 跟踪单个会话，包括其块发出的自定义事件。使用 `--all` 跟踪所有服务端事件，包括客户端的加入、离开与变更。

默认格式每条事件输出一行人类可读的文本。指定 `--json` 时，每行包含服务端发送的同一事件 JSON 对象，压缩为单行。每条事件输出后都会立即刷新缓冲区，以便管道能够实时处理事件。

该命令持续运行直至被中断或服务端断开连接。`--timeout` 仅限制连接建立及事件传递启动的耗时，不限制流式传输事件的时长。

| 选项 | 说明 |
| --- | --- |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `--all` | 跟踪所有服务端事件，包括客户端加入、离开和变更。 |
| `--json` | 将事件以换行符分隔的 JSON（NDJSON）输出。 |

```sh
rex events
rex events -s build
rex events --all
rex events --json | jq -c 'select(.type == "session_created")'
```

### `rex wait TARGET`

等待块、窗口或会话结束。

对于终端块，wait 返回子进程的退出状态码。它不等待块本身关闭，因此也适用于通过 `--keep-open` 创建的终端。等待任何其他块、窗口或会话时，只要该资源关闭或销毁即返回成功。如果终端在报告子进程退出前关闭，wait 返回 1。在 wait 开始监视之前就已经关闭的块也会返回 1，因为 Rex 已无法判断它是什么类型的块。

默认情况下，wait 一直运行直至目标结束或服务端断开连接。使用 `--for` 限制等待时间。全局选项 `--timeout` 仍限制连接和服务端单独的 API 请求，但不限制事件传递。指定 `--json` 时，命令将结束等待的载荷输出为一行 JSON。

如果 Rex 无法确定终端子进程的退出状态码，wait 返回 1。超过 255 的状态码按模 256 取模，以匹配 Shell 的行为。

目标可以是 ID、标签、ID 后缀，或窗口基于 1 的位置。如果目标匹配多种类型的资源，请使用完整 ID 来选择预期资源。

| 选项 | 说明 |
| --- | --- |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |
| `-w, --window string` | 将作用域限定在窗口 WINDOW。 |
| `--for DURATION` | 在 DURATION 后放弃等待。 |
| `--json` | 将终止载荷以 JSON 格式输出。 |

```sh
rex wait c2a9f3
rex wait build
rex wait 2 -s work
rex wait --for 10m $B || echo timed out
```

### `rex api`

检查并调用服务端 API。

检查并调用服务端控制 API 公开的方法。

使用 call 按名称运行方法。使用 list 发现连接的服务端所公开的方法（包含块创建者提供的方法）。使用 describe 读取某个方法的模式、示例和验证规则。

```sh
rex api call server.status
rex api call -s work session.view
rex api list
rex api describe session.new_split
```

### `rex api call METHOD [ARGS]`

调用服务端 API 方法。

调用服务端控制 API 公开的方法。

METHOD 为 API 方法名，例如 server.status。ARGS 必须为 JSON 对象。可直接传入该对象，或使用 @path 从文件读取，或使用 - 从标准输入读取。省略 ARGS 时，请求不发送任何参数。

接受 session_id 的方法要求连接先附加到该会话。使用 `--session` 按 ID 或标签解析会话并在请求前附加。命令会在缺少 session_id 时将其添加到 ARGS 中。如果 ARGS 已包含 session_id，该值将得到保留且必须与选定的会话匹配。未指定 `--session` 时，ARGS 顶层的 session_id 将用于附加。

方法结果为 JSON。写入终端的输出使用两个空格缩进。重定向输出保持在单行以便在脚本中使用。

| 选项 | 说明 |
| --- | --- |
| `-s, --session string` | 将作用域限定在会话 SESSION。 |

```sh
rex api call server.status
rex api call -s work session.view | jq '.windows | length'
rex api call session.create @layout.json
echo '{"label":"x"}' | rex api call session.create -
```

### `rex api list`

列出服务端 API 方法。

列出连接的服务端所公开的方法。

默认输出分别用独立表格展示常规 API 方法和块创建者提供的方法。使用 `--quiet` 仅打印方法名称，每行一个。使用 `--json` 打印服务端返回的完整帮助文档。

| 选项 | 说明 |
| --- | --- |
| `-q, --quiet` | 仅打印方法名称。 |
| `--json` | 将 API 帮助文档以 JSON 格式输出。 |

### `rex api describe METHOD`

描述服务端 API 方法。

描述连接的服务端所公开的方法。

默认输出包括该方法的说明以及所有可用的模式、示例和验证规则。使用 `--json` 打印服务端帮助文档中该方法的条目。

| 选项 | 说明 |
| --- | --- |
| `--json` | 将方法说明以 JSON 格式输出。 |

### `rex actions`

列出客户端或服务端提供的操作。

列出客户端或服务端提供的操作。

指定 `-C` 或 REX_CLIENT 时，将列出该客户端向服务端最新报告的操作。否则列出服务端提供的操作：由 init.lua 通过 rex.action 定义的操作，紧随其后是每种块类型的操作。按键绑定可以指定任一列表中的任意操作。

ARGS 列列出每个操作的参数。带有 ? 的参数为可选参数。

| 选项 | 说明 |
| --- | --- |
| `--json` | 将操作列表以 JSON 格式输出。 |

```sh
rex actions
rex -C studio actions
rex actions --json
```

## 服务端

### `rex server`

管理 Rex 服务端。

### `rex server run`

运行前台服务端。

在前台运行 Rex 服务端直至其被停止。

Ctrl+C、SIGTERM 和 `rex server stop` 会在服务端保存其会话后将其终止。

在 Unix 上，SIGHUP 的行为取决于服务端的运行方式。在终端中运行的服务端会保存会话并停止，因为关闭终端会发送 SIGHUP。没有终端的服务端（如 systemd、launchd 或容器运行时运行的服务端）会记录该信号并保持运行。在 nohup 下启动的服务端会继续忽略该信号。由 `rex server start` 启动的服务端则会重新打开其日志文件。参见 `rex server logs` `--help`。

如果不再有进程读取服务端的输出（例如由于终端关闭或 ssh 连接断开导致 tee 退出），服务端将继续运行且其日志行会丢失。可使用 `rex server stop` 停止它。

| 选项 | 说明 |
| --- | --- |
| `--listen ENDPOINT` | 监听 ENDPOINT（默认：本地 Rex Unix 套接字，或 Windows 上的 Rex 命名管道）。 |
| `--extra-listen ENDPOINT` | 同时监听 unix、http、tailnet、tailnet-serve 或 login-server ENDPOINT（可重复指定；Windows 上不支持 tailnet-serve 或 login-server）。 |
| `--socket-mode MODE` | 将 Unix 套接字权限设置为 MODE，仅限所有者和组权限位（默认 0600，Windows 上不可用）。 |
| `--allow-anonymous` | 允许纯 TCP 监听器上的匿名调用者（每个连接均获得完全访问权限）。 |
| `--tailnet-allow-identified` | 允许通过宿主机的 tailscaled 识别的所有调用者访问（默认：节点所有者）。 |
| `--tailscaled-socket PATH` | 使用位于 PATH 的 tailscaled LocalAPI 套接字（默认：平台套接字）。 |
| `--tailscale-allow-tailnet-members` | 允许 ACL 许可的任何 tailnet 成员访问 Rex。 |
| `--exit-empty` | 当无剩余会话或控制连接时停止。 |
| `--websocket-origin-pattern PATTERN` | 允许来自跨域 PATTERN 的浏览器 WebSocket 连接（可重复指定）。 |
| `--block-dir DIR` | 在 DIR 中发现可执行块插件（可重复指定）。 |
| `--block-plugin-reload` | 在源码更改后重新加载块插件。 |
| `--state-dir DIR` | 在 DIR 目录下存储持久化服务端状态。 |
| `--restore` | 恢复保存的会话（false 则不恢复且不保存任何内容）。默认为 `true`。 |
| `--config PATH` | 读取位于 PATH 的配置文件（默认：REX_CONFIG，否则为配置目录中的 rex/init.lua）。 |
| `--max-sessions N` | 当服务端容纳 N 个会话时拒绝新会话（0 表示无限制）。默认为 `64`。 |
| `--max-blocks N` | 当服务端跨所有会话总共容纳 N 个块时拒绝新块（0 表示无限制）。默认为 `1024`。 |
| `--max-windows N` | 当一个会话容纳 N 个窗口时拒绝新窗口（0 表示无限制）。默认为 `64`。 |
| `--max-panes N` | 当一个窗口容纳 N 个窗格时拒绝新窗格（0 表示无限制）。默认为 `64`。 |
| `--tailscale` | 同时作为嵌入式 tsnet 节点在 tailnet 上提供 API 服务。 |
| `--tailscale-hostname NAME` | 用于 `--tailscale` 的 tailnet 设备名称 NAME。默认为 `rex`。 |
| `--tailscale-control-url URL` | 向 URL 处的控制服务器（如 Headscale）注册 tailnet 节点。 |
| `--tailscale-auth-key-file FILE` | 使用从 FILE 读取的一次性认证密钥注册 `--tailscale`（'-' 代表标准输入）。 |
| `--tailscale-advertise-tag TAG` | 在 `--tailscale` 注册节点时通告 ACL TAG（tag:name）（可重复指定）。 |
| `--log-format FORMAT` | 将服务端日志写入为 FORMAT：text 或 json。默认为 `text`。 |
| `--log-level LEVEL` <span class="row-tags"><span class="api-tag channel">[Snapshot](../linux/installation.md#发布通道)</span></span> | 记录 LEVEL 及以上级别的日志：debug、info、warn 或 error（默认为 info；若未指定此标志但传入了 `-v`，则为 debug）。 |

### `rex server start`

启动持久化服务端。

start 具有幂等性。start 选项仅在启动新服务端时生效。现有服务端保持其活动配置，直至显式重启。

日志大小限制仅适用于为后台分离服务端创建的文件。在写入会导致超出 `--log-max-size` 之前，Rex 会清理该文件。

| 选项 | 说明 |
| --- | --- |
| `--extra-listen ENDPOINT` | 同时监听 unix、http、tailnet、tailnet-serve 或 login-server ENDPOINT（可重复指定；Windows 上不支持 tailnet-serve 或 login-server）。 |
| `--socket-mode MODE` | 将 Unix 套接字权限设置为 MODE，仅限所有者和组权限位（默认 0600，Windows 上不可用）。 |
| `--allow-anonymous` | 允许纯 TCP 监听器上的匿名调用者（每个连接均获得完全访问权限）。 |
| `--tailnet-allow-identified` | 允许通过宿主机的 tailscaled 识别的所有调用者访问（默认：节点所有者）。 |
| `--tailscaled-socket PATH` | 使用位于 PATH 的 tailscaled LocalAPI 套接字（默认：平台套接字）。 |
| `--websocket-origin-pattern PATTERN` | 允许来自跨域 PATTERN 的浏览器 WebSocket 连接（可重复指定）。 |
| `--block-dir DIR` | 在 DIR 中发现可执行块插件（可重复指定）。 |
| `--block-plugin-reload` | 在源码更改后重新加载块插件。 |
| `--state-dir DIR` | 在 DIR 目录下存储持久化服务端状态。 |
| `--restore` | 恢复保存的会话（false 则不恢复且不保存任何内容）。默认为 `true`。 |
| `--config PATH` | 读取位于 PATH 的配置文件（默认：REX_CONFIG，否则为配置目录中的 rex/init.lua）。 |
| `--max-sessions N` | 当服务端容纳 N 个会话时拒绝新会话（0 表示无限制）。默认为 `64`。 |
| `--max-blocks N` | 当服务端跨所有会话总共容纳 N 个块时拒绝新块（0 表示无限制）。默认为 `1024`。 |
| `--max-windows N` | 当一个会话容纳 N 个窗口时拒绝新窗口（0 表示无限制）。默认为 `64`。 |
| `--max-panes N` | 当一个窗口容纳 N 个窗格时拒绝新窗格（0 表示无限制）。默认为 `64`。 |
| `--tailscale-allow-tailnet-members` | 允许 ACL 许可的任何 tailnet 成员访问 Rex。 |
| `--tailscale` | 同时作为嵌入式 tsnet 节点在 tailnet 上提供 API 服务。 |
| `--tailscale-hostname NAME` | 用于 `--tailscale` 的 tailnet 设备名称 NAME。默认为 `rex`。 |
| `--tailscale-control-url URL` | 向 URL 处的控制服务器（如 Headscale）注册 tailnet 节点。 |
| `--tailscale-auth-key-file FILE` | 使用从 FILE 读取的一次性认证密钥注册 `--tailscale`。 |
| `--tailscale-advertise-tag TAG` | 在 `--tailscale` 注册节点时通告 ACL TAG（tag:name）（可重复指定）。 |
| `--log-format FORMAT` | 将服务端日志写入为 FORMAT：text 或 json。默认为 `text`。 |
| `--log-level LEVEL` <span class="row-tags"><span class="api-tag channel">[Snapshot](../linux/installation.md#发布通道)</span></span> | 记录 LEVEL 及以上级别的日志：debug、info、warn 或 error（默认为 info；若未指定此标志但传入了 `-v`，则为 debug）。 |
| `--log-max-size SIZE` | 通过清理旧内容将活动的后台日志大小限制在 SIZE（0 表示禁用）。默认为 `50MiB`。 |
| `--env NAME` | 将环境变量 NAME 或 NAME=VALUE 传递给新服务端（可重复指定）。 |
| `--json` | 将服务端信息以 JSON 格式输出。 |

### `rex server status`

显示服务端状态。

| 选项 | 说明 |
| --- | --- |
| `--json` | 将服务端信息以 JSON 格式输出。 |

### `rex server logs`

显示后台分离服务端的日志。

显示通过 `rex server start` 启动的服务端所捕获的日志。

在 Windows 上，`rex server install` 作为 Windows 服务运行的服务端也会写入此日志，因此该命令同样会显示其输出。与 `rex server start` 相同，Rex 在该日志增长超过 50MiB 之前会对其进行清理。

由其他服务管理器（如 systemd 或 launchd）启动的服务端则通过相应的管理器记录日志。对于由 Linux 软件包和 home-manager 模块安装的 systemd 用户单元所运行的个人服务端，请运行 journalctl `--user` `-u` rex。对于由 Linux 软件包和 NixOS 模块安装的共享服务端，请运行 journalctl `-u` rex.service。

在 Unix 上，使用 rename/create 进行轮转必须在创建替换文件后向服务端发送 SIGHUP。只有通过 `rex server start` 启动的服务端才会在收到 SIGHUP 时重新打开其日志。有关该信号对其他服务端的作用，请参阅 `rex server run` `--help`。Windows 使用 copy-truncate 或 `--log-max-size`。`--follow` 会在日志轮转过程中持续跟踪。

| 选项 | 说明 |
| --- | --- |
| `--follow` | 持续跟踪追加的日志输出直至服务端停止。 |
| `--state-dir DIR` | 读取 DIR 目录下的服务端日志。 |
| `-n, --lines N` | 显示最新的 N 行日志。默认为 `200`。 |
| `--all` | 显示整个可用的后台日志。 |

### `rex server tailscale`

管理服务端的 Tailscale 节点。

### `rex server tailscale on`

在 tailnet 上提供 API 服务。

on 具有幂等性且仅在运行时生效：重启后的服务端会恢复为其启动标志。若要保持 Tailscale 开启，请使用 `--tailscale` 启动服务端。在 Windows 上，“rex server install -- --tailscale” 会在每次服务端启动时执行此操作。首次启用的节点会开启 Tailscale 的常规认证流程；登录 URL 会出现在服务端日志以及 `rex server status` 中。

一次性认证密钥无需浏览器流程即可注册新节点：传入包含路径的 `--auth-key-file`，或传入 '-' 从标准输入读取密钥。故意不允许在命令行直接传入密钥本身，以防止其在进程列表中可见。该密钥仅在节点首次注册时需要——注册成功的身份保存在服务端上——在节点已处于启用状态时会被忽略。通过 `--advertise-tag` 指定的 ACL 标签以相同方式生效：仅在此次调用首次注册节点时应用。

`--control-url` 将此次调用启动的节点向另一个控制服务器（如 Headscale）注册。每个控制服务器保留其各自保存的登录状态，因此迁移到新控制服务器的节点需要重新登录。若要迁移已处于开启状态的节点，请先将其关闭。省略此标志时使用服务端的 `--tailscale-control-url`。

| 选项 | 说明 |
| --- | --- |
| `--hostname NAME` | 此次调用启动节点时的 tailnet 设备名称 NAME（默认为服务端配置的名称）。 |
| `--allow-tailnet-members` | 允许 tailnet 许可的任何调用者访问，而非仅限该节点的所有者。 |
| `--auth-key-file FILE` | 使用从 FILE 读取的一次性 tailscale 认证密钥注册新节点（'-' 代表标准输入）。 |
| `--advertise-tag TAG` | 此次调用注册新节点时通告 ACL TAG（tag:name）（可重复指定）。 |
| `--control-url URL` | 将此次调用启动的节点向 URL 处的控制服务器（如 Headscale）注册。 |
| `--json` | 将生成的状态以 JSON 格式输出。 |

### `rex server tailscale off`

停止在 tailnet 上提供 API 服务。

多次运行 'off' 均会成功。tailnet 连接会断开，而会话保持运行。保持登录状态。下一次执行 'on' 无需登录即可重新连接。使用 'logout' 可清除此设备。

| 选项 | 说明 |
| --- | --- |
| `--json` | 将生成的状态以 JSON 格式输出。 |

### `rex server tailscale logout`

退出 Tailscale 并停止 tailnet 服务。

退出已启用的 Tailscale 节点并停止 tailnet 服务。下一次执行 'on' 必须重新登录。如果已经处于关闭状态，将保持已保存的登录状态不变。

| 选项 | 说明 |
| --- | --- |
| `--json` | 将生成的状态以 JSON 格式输出。 |

### `rex server tailscale login`

请求 Tailscale 登录链接。

为已启用的 Tailscale 节点请求登录链接。Tailscale 可能需要几秒钟生成链接。如果未显示链接，请重新运行该命令或检查 `rex server status`。

| 选项 | 说明 |
| --- | --- |
| `--json` | 将生成的状态以 JSON 格式输出。 |

### `rex server tailscale rename NAME`

重命名已启用的 Tailscale 节点，无需重启或重新登录。NAME 必须为 1 到 63 个 ASCII 字母、数字或连字符组成的单个 DNS 标签，且首尾不能为连字符。新的 DNS 名称可能会在此命令返回后生效。

| 选项 | 说明 |
| --- | --- |
| `--json` | 将生成的状态以 JSON 格式输出。 |

### `rex server tailscale pair`

显示用于配对其他设备的二维码。

将服务端的 tailnet 地址显示为二维码，供另一台设备上的 Rex 扫描。

二维码仅包含地址，不包含凭证。另一台设备必须处于同一 tailnet 上。Tailscale 必须处于开启状态且其 HTTPS 地址已就绪。

| 选项 | 说明 |
| --- | --- |
| `--json` | 将地址以 JSON 格式输出。 |


### `rex server stop`

停止服务端。

停止服务端会终止在其会话中运行的每个程序。

指定 `--if-idle` 时，服务端仅在其没有会话且无其他客户端连接时才会停止。否则服务端保持运行，命令会说明当前有哪些占用并以状态码 1 退出。在同一时刻尝试连接的客户端将被拒绝，因此绝不会开启即将被停止操作终止的工作。

指定 `--discard` 时，命令在服务端停止后还会删除其保存的会话，以便下次启动时不恢复任何会话。如果没有服务端在运行，则仅删除这些会话。若停止请求被拒绝，则不会删除任何内容。若服务端启动时指定了 `--state-dir`，请同样传入该选项。

`--if-idle` 要求服务端版本足够新以支持该选项。对于较旧版本的服务端，命令会保持服务端运行并以状态码 4 退出。不带 `--if-idle` 时，`rex server stop` 适用于任何版本的服务端。

| 选项 | 说明 |
| --- | --- |
| `--discard` | 服务端停止后删除保存的会话。 |
| `--if-idle` | 仅在服务端没有会话且无其他连接的客户端时停止。 |
| `--state-dir DIR` | 在 DIR 目录下查找用于 `--discard` 的已保存会话。 |

### `rex server install [flags] [ssh://[USER@]HOST[:PORT]] [-- SERVER-FLAG...]`

开机启动服务端并保持运行。

将个人 Rex 服务端设置为自动启动。默认情况下，它会在开机时启动，并在注销登录后保持运行。

在 Linux 上，这将启用 rex.socket，这是一个 systemd 用户单元，在 rex 命令首次连接时启动服务端。它还会通过 “loginctl enable-linger” 为当前账户开启常驻（linger）。常驻使 systemd 用户管理器以及其中的服务端在注销登录后继续运行。无需 sudo 权限。如果运行由 Rex 软件包安装的 rex，则直接启用软件包自带的单元。对于任何其他 rex，运行该二进制文件的单元副本将写入 ~/.config/systemd/user。运行的每条命令和写入的每个文件都会先打印出来。

指定 `--user` 时，服务端在登录时启动并在注销时停止，常驻状态保持原样。

如果已有 rex 命令启动了服务端，该服务端将保留其会话。空闲的服务端会被停止，以便单元或服务立即接管。包含会话的服务端将继续运行，单元或服务改为在下次开机或登录时启动。

如果系统不允许开启常驻，服务端仍会在登录时启动，命令会提示管理员如何开启常驻。如果 ~/.config/systemd/user 中已存在非 rex 写入的 rex.service 或 rex.socket（例如来自 home-manager 模块），命令将保持其不变并报错退出。

在 Windows 上，这会创建一个以当前账户运行 “rex server run” 的 Windows 服务。它在开机时紧随其他自动服务之后启动，在无人登录以及注销之后保持运行。创建服务需要管理员权限，因此请在通过“以管理员身份运行”启动的终端中执行该命令。命令还会授予账户“作为服务登录”的权限（Windows 以该身份启动服务所需），并将 “Rex Server” 注册为事件日志源。它会删除 `--user` 添加的登录启动项，因为两者只能由其一运行服务端。每处更改都会先打印出来。服务端及其启动的每个程序均在无管理员权限下运行（即使账户属于管理员组），如同正常登录后一样。

命令会提示输入 Windows 密码，因为 Windows 需要密码才能在未登录时以当前账户启动服务。Windows 会将密码随服务一同保存。Rex 不会保留密码。请使用 Windows 账户的密码，而非 Windows Hello PIN。如果使用 Microsoft 账户登录，请使用该 Microsoft 账户的密码。在无终端环境下，命令从标准输入读取密码。如果密码发生更改，请重新运行该命令，否则服务无法在下次开机时启动。

在 Windows 上使用 `--user` 时，无需管理员权限。命令会在 HKCU\Software\Microsoft\Windows\CurrentVersion\Run 中添加名为 “Rex Server” 的注册表值，该值在每次登录时运行 “rex server start”。如果当前没有服务端运行，它还会立即启动一个，对已在运行的服务端保持不变。服务端在注销 Windows 时停止，并在下次登录时再次启动。如果在任务管理器的“启动”标签页中禁用了该项，命令会予以提示。若已存在 Windows 服务，该命令会报错失败。请先运行 “rex server uninstall”。

在 Windows 上，可以在 -- 之后传入服务端标志。服务端每次启动都会接收这些标志，因此可将其用于服务端重启后必须保留的设置。例如，“rex server tailscale on” 仅在服务端停止前保持 Tailscale 开启。以下命令可在每次开机启动时开启：

    `rex server install` -- `--tailscale`

Windows 服务会带这些标志运行 “rex server run”，而 `--user` 添加的 “Rex Server” 注册表项会带这些标志运行 “rex server start”。命令会拒绝服务端不支持的标志且不做任何更改。它还会拒绝 `--listen`，因为服务端必须保留在 rex 命令查找它的命名管道上。使用 `--extra-listen` 可添加其他端点。

再次运行不带 -- 的命令将保留已设置的服务端标志。在 -- 之后传入新标志可替换它们，或单独传入 -- 可移除它们。正在运行的服务端会保持其旧标志直至重启。

在 Linux 上，systemd 负责启动服务端，因此该命令在那里不接受服务端标志。请改在 override drop-in 文件中设置，使用 “systemctl `--user` edit rex.service”。

再次运行该命令是安全的。移动 rex 路径后请重新运行。

目前支持带 systemd 的 Linux 以及 Windows。在其他系统上，“rex server start” 启动的服务端会一直运行直至机器重启。

指定 ssh:// 端点时，命令会在可通过 ssh 登录的另一台机器上配置服务端，并先在该机器上安装 Rex。它会在远程机器上使用 `--user` 运行 Rex 安装程序，将 rex 安装到 ~/.local/bin 且无需 sudo。以 root 身份或指定 `--package` 时，它会通过 sudo 为整台机器安装 Rex 软件包。然后它在远程机器上运行 “rex server install”，通过 ssh 连接到新服务端，并将该机器添加到你的 hosts 中，以便通过 “rex `-S` LABEL” 访问。目前仅支持 Linux 远程机器。

在远程机器上运行的每条命令都会先打印出来，且命令在每次更改前都会进行确认。`--yes` 对每个问题均回答 yes。在没有交互终端的环境下，必需指定 `--yes`。

| 选项 | 说明 |
| --- | --- |
| `--user` | 在登录时启动服务端并在注销时停止，而非开机启动。 |
| `--json` | 将命令执行的操作以 JSON 格式输出。 |
| `--package` | 通过 ssh，使用 sudo 为整台机器安装 Rex 软件包。 |
| `--label LABEL` | 通过 ssh，将该机器作为 LABEL 添加到你的 hosts（默认使用其主机名）。 |
| `--channel NAME` | 通过 ssh，从发布通道 NAME 安装：stable、preview 或 snapshot。 |
| `--yes` | 通过 ssh 时，对所有确认问题均回答 yes。 |

### `rex server uninstall [ssh://[USER@]HOST[:PORT]]`

停止服务端自启动。

撤销 “rex server install”。

在 Linux 上，这会禁用并停止 rex.socket 和 rex.service，并删除 `rex server install` 写入 ~/.config/systemd/user 的副本文件。停止服务端会终止在其会话中运行的每个程序。软件包安装的单元保持保留并处于禁用状态。如果 ~/.config/systemd/user 中包含非 rex 写入的 rex.service 或 rex.socket（如来自 home-manager 模块），则不会禁用或删除任何内容。

常驻（linger）保持开启，因为当前账户的其他服务可能需要它。可使用 “loginctl disable-linger” 将其关闭。

在 Windows 上，这会停止并删除 `rex server install` 创建的 Windows 服务，从而终止其会话中运行的每个程序。它还会注销事件日志的 “Rex Server” 源，除非其他账户的服务仍在使用它。删除服务需要通过“以管理员身份运行”启动的终端。当前账户保留“作为服务登录”的权限，因为其他服务可能需要它。

它还会删除 `rex server install` `--user` 添加到 HKCU\Software\Microsoft\Windows\CurrentVersion\Run 的 “Rex Server” 注册表值，这不需要管理员权限。由该注册表项启动的服务端将继续运行及其会话。使用 “rex server stop” 停止它。

接受 `--user` 选项以便两个命令支持相同的标志。无论是否带有该选项，uninstall 执行相同的操作。

指定 ssh:// 端点时，命令会在提示确认后在远程机器上运行 “rex server uninstall”。Rex 在该机器上保持安装，且该机器保留在你的 hosts 中。命令会提示如何分别移除它们。

| 选项 | 说明 |
| --- | --- |
| `--user` | 撤销 `rex server install` `--user`。 |
| `--json` | 将命令执行的操作以 JSON 格式输出。 |
| `--yes` | 通过 ssh 时，对所有确认问题均回答 yes。 |

### `rex config`

处理 Rex 的配置文件。

Rex 为每个账户读取一个配置文件 init.lua。它通过 rex.bind 绑定快捷键，通过 rex.unbind 解除绑定。

当设置了 REX_CONFIG 变量时，配置文件为该变量指定的路径。否则为账户配置目录中的 rex/init.lua，在 macOS 和 Linux 上为 $XDG_CONFIG_HOME/rex 或 ~/.config/rex，在 Windows 上为 %AppData%\rex。

### `rex config check [PATH]`

加载配置文件并报告检查结果。

加载配置文件并报告其所在位置、是否存在、绑定和解除了多少按键、使用了多少模式、定义了多少操作，以及加载过程中的所有警告与问题。未提供 PATH 时使用账户自身的 init.lua。

此处仅执行加载操作。某些错误需要结合文件以外的上下文才能发现，例如绑定了一个此文件和客户端均未提供的操作，或解除绑定了一个原本未绑定的按键。这些取决于发出请求的客户端，“rex keymap” 会报告它们。

该文件由当前 rex 二进制文件加载，因此会根据此版本 Rex 所知的函数和字段进行检查。运行不同版本的服务端可能会有不同的解析结果。“rex keymap” 则直接向正在运行的服务端发起查询。

如果存在任何错误级别的报告，退出状态码为 1。

| 选项 | 说明 |
| --- | --- |
| `--json` | 将检查结果以 JSON 格式输出。 |

### `rex config reload`

使服务端重新读取配置文件，并通知连接的每个客户端其按键可能已变更。

generation（代数）记录了此服务端读取该文件的次数。客户端将其与自身记录进行比较以发现快捷键映射已过期。每次读取都会递增该计数，包括读取失败的情况。

读取失败时保留上一次成功读取的按键配置。此处仅报告文件自身的问题。对于需要结合客户端自身绑定才能发现的问题，请使用 “rex keymap”。

此命令在服务端所在的本机上通过本地套接字运行。能够编辑该文件的人已在本地，远程调用者将被拒绝。

如果存在任何错误级别的报告，退出状态码为 1。

| 选项 | 说明 |
| --- | --- |
| `--json` | 将结果以 JSON 格式输出。 |

### `rex keymap`

显示经服务端解析后每个按键的功能。其结果是将配置文件的绑定叠加在请求客户端自带的绑定之上，并置于该客户端自身设置中记录的快捷键之下。

不带 `--request` 时，此命令不发送任何图层且不声明自身的操作。输出仅为配置文件自身的绑定，且指定操作名称的绑定不会针对任何客户端的操作列表进行校验。传入客户端自身的请求可查看该客户端接收到的按键映射。若该请求设置了 server_actions，输出将列出客户端接收到的相同操作。

绑定按每个按键堆栈的顶部优先列出，这也是客户端尝试匹配它们的顺序。模式中的绑定按配置文件中的书写方式列出（如 resize/left），且仅在该客户端激活该模式期间生效。当存在模式时，按键绑定后会跟随模式表格。若存在任何错误级别的报告，退出状态码为 1。

| 选项 | 说明 |
| --- | --- |
| `--request FILE` | 发送 FILE 中的 client.keymap 请求（“-” 代表标准输入）。 |
| `--json` | 将响应以 JSON 格式输出。 |

```sh
rex keymap
rex keymap --request client.json
rex keymap --json | jq '.bindings[] | select(.keys[0] == "cmd+d")'
```

### `rex login-server`

运行多账户登录服务端。

登录服务端以 root 身份运行。它识别每个调用者，通过账户文件选择操作系统账户，并为该账户启动或复用 Rex 服务端。它将每个接受的连接代理到选定的服务端。客户端使用 https://ACCOUNT@host:port 选择账户。tailnet 监听器允许所有已识别的调用者访问，因为权限控制由账户文件负责。本地用户使用 sudo 请求另一个账户。发送 SIGHUP 可重新加载账户文件。重新加载会关闭被吊销的连接，但保持账户服务端和会话继续运行。

| 选项 | 说明 |
| --- | --- |
| `--listen ENDPOINT` | 监听仅限 root 的 Unix ENDPOINT（默认：unix://RUNTIME-ROOT/login-server.sock）。 |
| `--extra-listen ENDPOINT` | 同时监听 unix、http、tailnet 或 tailnet-serve ENDPOINT（可重复指定）。 |
| `--allow-anonymous` | 允许纯 TCP 监听器上的匿名调用者（每个连接均获得完全访问权限）。 |
| `--tailscaled-socket PATH` | 使用位于 PATH 的 tailscaled LocalAPI 套接字（默认：平台套接字）。 |
| `--accounts FILE` | 使用 HuJSON FILE 将调用者映射到账户（默认 /etc/rex/accounts.jsonc，FreeBSD 上为 /usr/local/etc/rex/accounts.jsonc）。 |
| `--runtime-root DIR` | 在 DIR 目录下保留套接字和 accounts/（默认：$REX_RUNTIME_DIR，否则为 /run/rex，FreeBSD 上为 /var/run/rex）。 |
| `--pam` | 打开 PAM 会话并运行 PAM 账户检查（默认 true；`--pam=false` 使用基于 shadow 的检查且无登录会话）。 |
| `--pam-service NAME` | 使用服务 NAME 的 PAM 策略（默认 rex-login-server）。 |
| `--log-format FORMAT` | 将服务端日志写入为 FORMAT：text 或 json。默认为 `text`。 |

### `rex home`

显示或选择你的主服务端。

显示或选择你的 home（主服务端），即当前设备跟踪以获取主机列表和快捷方式的服务端。

除非另行选择，否则本机就是你的主服务端。任何 Rex 服务端都可以作为主服务端。服务端不会被告知它被设为某人的主服务端，无论哪种情况均以相同方式允许你访问。

不带子命令时，连接到你的主服务端并显示其报告的关于你的信息。你的选择保存在 Rex 状态目录中的 home.json 中。设置 REX_HOME 可为单个环境选择主服务端并优先于该文件。`--server` 选项和 REX_SERVER 选择其他命令与之通信的服务端，它们不会改变你的主服务端。

| 选项 | 说明 |
| --- | --- |
| `--json` | 将主服务端与你的身份以 JSON 格式输出。 |

### `rex home set ENDPOINT`

跟踪 ENDPOINT 以获取主机列表和快捷方式。

将位于 ENDPOINT 的服务端设为你的主服务端。ENDPOINT 接受与 `--server` 相同的形式。

首先会查询服务端的运行状态。如果无法连接，你的主服务端不会被更改，因此输错的地址或停机的服务端绝不会成为你的主服务端。主服务端由 `--label` 命名；若未提供标签，则使用端点的主机名或套接字名称命名。

你的选择会写入 Rex 状态目录中的 home.json，同时记录服务端报告的主机 ID。`rex home` 使用主机 ID 在地址日后指向不同机器时向你发出警告。当设置了 REX_HOME 时此命令会失败，因为该变量优先于文件。

| 选项 | 说明 |
| --- | --- |
| `--label NAME` | 在输出中将主服务端命名为 NAME。 |

### `rex home unset`

重新跟踪本机。

清除你选择的主服务端，使本机自身的服务端重新成为你的主服务端。这会删除 home.json。如果未曾选择主服务端，该命令同样成功。

当设置了 REX_HOME 时此命令会失败，因为该变量优先于文件。

### `rex hosts`

列出并修改你连接的主机。

列出并修改你的主机列表，即通过标签连接的其他 Rex 服务端。

你的主服务端保存你的主机列表，因此跟踪同一主服务端的每台设备都会看到相同的列表。无论你的主服务端是什么，本机自身服务端的主机也始终计算在内。如果本机的某台主机与主服务端的某台主机具有相同的标签，本机的主机优先生效。

新增主机保存到主服务端。对主机的修改保存到主机来源的服务端。如果主服务端离线（away），修改会暂存在本机上，并在 `rex hosts` 下次连接到主服务端时发送。在此之前，列表显示上次连通时主服务端所具有的主机。

若要使用某台主机，将其标签传给 `--server`，如 “rex `-S` studio session ls”。

不带子命令时，列出你的主机。`--server` 选项和 REX_SERVER 不会改变此命令与之通信的服务端。

| 选项 | 说明 |
| --- | --- |
| `--json` | 将主机列表以 JSON 格式输出。 |

### `rex hosts list`

列出你的主机。

列出你的主服务端保存的主机（包括为其暂存的更改），以及本机自身服务端的主机。

FROM 说明主机来自哪个服务端，当主服务端为本机时省略。SOURCE 为声明主机的 init.lua 代码行，对于通过 `rex hosts` 添加的主机显示为 “stored”，对于尚未发送到主服务端的更改显示为 “held”。

如果主服务端离线，列表会显示上次连通时的主机，并说明那是多久之前。警告输出到标准错误。

| 选项 | 说明 |
| --- | --- |
| `--json` | 将主机列表以 JSON 格式输出。 |

### `rex hosts add LABEL ENDPOINT...`

将主机添加到主服务端。

添加名为 LABEL 的主机，按顺序尝试各个 ENDPOINT。端点接受与 `--server` 相同的形式。

套接字路径（如 unix:///tmp/rex.sock）仅在路径存在的设备上有效（例如 ssh `-L` 转发的本地端）。其他设备会跳过它并尝试下一个端点。

主机保存到你的主服务端，因此跟踪你主服务端的每台设备都能看到它。忽略大小写的情况下，你的其他主机不得具有相同的标签。

如果主服务端离线，主机将暂存在本机上并立即列出。它会在 `rex hosts` 下次连接到主服务端时发送。

| 选项 | 说明 |
| --- | --- |
| `--icon NAME` | 在主机旁显示图标 NAME。 |

### `rex hosts edit LABEL`

修改主机。

修改名为 LABEL 的主机（忽略大小写）。至少提供一个选项。`--endpoint` 会替换该主机的所有端点，且可指定多次。

更改保存到主机来源的服务端：你的主服务端或本机。编辑在 init.lua 中声明的主机会存储一个取代该声明的主机。原代码行保留在文件中，但不再生效。

如果该主机属于主服务端且主服务端离线，更改会暂存在本机上并在 `rex hosts` 下次连接到主服务端时发送。

| 选项 | 说明 |
| --- | --- |
| `--label NEW` | 将主机重命名为 NEW。 |
| `--endpoint ENDPOINT` | 在 ENDPOINT 连接该主机（可重复指定，替换所有端点）。 |
| `--icon NAME` | 在主机旁显示图标 NAME（留空则移除）。 |

### `rex hosts remove LABEL`

移除主机。

从主机来源的服务端（你的主服务端或本机）移除名为 LABEL 的主机（忽略大小写）。

移除在 init.lua 中声明的主机会将其隐藏。原代码行保留在文件中，但不再生效。

如果该主机属于主服务端且主服务端离线，移除操作会暂存在本机上并在 `rex hosts` 下次连接到主服务端时发送。

### `rex hosts check [LABEL...]`

检查从此处可达的主机。

尝试连接每台主机，或仅连接名为 LABEL 的主机（忽略大小写）。所有主机同时发起尝试，每台主机最多有 `--timeout` 时间做出响应。

STATUS 为以下之一：

  reachable                Rex 服务端在 ENDPOINT 响应了请求
  not reachable from here  无响应，但该主机可能在其他网络或设备上可用
  down                     机器响应了请求，但不是 Rex 服务端

DETAIL 说明无法连接的原因。对于可达的主机，它会在地址现在指向与添加时不同的机器时予以提示。

无论检查结果如何均返回成功。连接主机的命令会优先尝试最先响应的地址。

| 选项 | 说明 |
| --- | --- |
| `--json` | 将检查结果以 JSON 格式输出。 |

### `rex whoami`

显示你的身份、服务端与 Rex 位置。

| 选项 | 说明 |
| --- | --- |
| `--json` | 将身份、服务端和位置以 JSON 格式输出。 |


## 其他

### `rex completion`

为 Rex 生成 Shell 补全脚本。

### `rex completion bash`

生成 Bash 补全脚本。

使用 source &lt;(`rex completion bash`) 加载它，或将其安装到 bash-completion 目录中。

### `rex completion zsh`

生成 Zsh 补全脚本。

使用 `rex completion zsh` &gt; `"${fpath[1]}/_rex"` 安装它。

### `rex completion fish`

生成 Fish 补全脚本。

使用 `rex completion fish` &gt; ~/.config/fish/completions/rex.fish 安装它。

### `rex completion powershell`

生成 PowerShell 补全脚本。

将 `rex completion powershell` 的输出添加到你的 PowerShell profile 中。

### `rex completion nu`

生成 Nushell 补全脚本。

将 `rex completion nu` 的输出添加到你的 config.nu 中。

### `rex terminfo`

配置并报告 Rex 的终端类型。

Rex 自带专门的 terminfo 条目 xterm-rex，用于描述其终端所支持的功能特性。

只要当前账户完成相关配置，终端就会声明该条目，除非 REX_TERM 指定了其他条目。每个账户运行一次 “rex terminfo setup”，并运行 “rex terminfo status” 查看当前机器的判定结果。

### `rex terminfo status`

报告新终端将被赋予的 TERM 及其原因。

报告新终端将被赋予的 TERM、决定该值的检查项，以及在当前账户尚未配置时如何通过命令进行修复。

服务端在安全的情况下声明 xterm-rex，在其他所有情况下保持使用 xterm-256color。在 REX_TERM 中指定条目会覆盖上述行为并为每个终端赋予该名称，这使得 REX_TERM=xterm-256color 成为关闭开关。值 “auto” 要求遵循服务端已采用的规则。

该报告涵盖 terminfo 条目、ssh 客户端、两个保护文件、已记录的主机，以及决定 ssh 实际发送内容的配置来源。

不会更改你的任何内容，也不会连接任何主机。写入的唯一文件是 Rex 保护文件的临时副本，用于查询 ssh 在仅有该保护文件时会执行的操作。

| 选项 | 说明 |
| --- | --- |
| `--json` | 将报告以 JSON 格式输出。 |

### `rex terminfo setup`

安装 Rex 的 terminfo 条目与 ssh 保护配置。

将 xterm-rex 安装到程序能够找到的位置，并配置 ssh，使该名称绝不会发送给未曾获知该条目的主机。

此过程执行三项操作：将条目安装到 ~/.terminfo；将保护文件写入 Rex 的配置目录；在 ~/.ssh/config 顶部添加一行 Include。随后向 ssh 查询其向未安装该条目的主机发送的内容并报告结果。

如果你的 ssh 配置已包含保护配置（例如通过 home-manager 使用 Rex 模块进行管理），则会跳过保护文件和 Include 行，因为重复添加不会产生任何额外效果。

保护配置需要 OpenSSH 7.8 或更高版本，因为较旧的 ssh 会拒绝包含该配置的任何文件。在较旧的 ssh 下，仅会安装 terminfo 条目，并且命令会失败并说明原因。

指定 `--system` 时，条目会安装到 /usr/share/terminfo，保护文件写入 /etc/ssh/ssh_config.d/50-rex.conf，使当前机器上的每个账户（包括 root）均拥有这两者。这需要 root 权限，并使通过 sudo 和 su 启动的程序能够找到该条目。在 FreeBSD 上（/etc/ssh/ssh_config 不默认读取其他文件），它还会在该文件顶部为保护文件所在目录添加一行 Include。

每个账户运行一次该命令。重复运行无害。

有两个标志适用于代表用户配置账户的程序：`--entry-only` 仅安装条目而保持 ssh 配置不变（这是不需要特殊权限的一半工作）；`--json` 将执行结果作为单个对象输出，而非供人阅读的文本行。

安装条目只是其中一步。只有在保护文件同样就绪后，终端才会声明该名称，且 REX_TERM 可以指定其他条目。“rex terminfo status” 会报告当前机器的决定。

| 选项 | 说明 |
| --- | --- |
| `--entry-only` | 仅安装条目，供稍后添加保护配置的程序使用（仅当保护配置同样就绪后才会声明该名称）。 |
| `--dry-run` | 报告将要进行的更改而不写入任何内容。 |
| `--system` | 为当前机器上的所有账户安装条目与保护配置。 |
| `--json` | 将执行结果以 JSON 格式输出。 |

### `rex terminfo remove`

移除 ssh 保护配置，保留已安装的 terminfo 条目。

移除 Rex 的 ssh 保护文件以及使其生效的 Include 行，使 ssh 恢复转发传入的任意 TERM。

指定 `--system` 时，系统全局保护文件 /etc/ssh/ssh_config.d/50-rex.conf 会被移除。在 FreeBSD 上，setup 添加到 /etc/ssh/ssh_config 的 Include 行也会被一并移除。这需要 root 权限。

在这两种情况下，terminfo 条目均保留在安装位置。当前已使用 TERM=xterm-rex 运行的 Shell 在条目消失的瞬间就会停止工作，因此没有提供删除条目的命令。如果你确实希望删除这些文件，请手动移除。

`--json` 将执行结果作为单个对象输出，其结构与 setup 保持一致。

| 选项 | 说明 |
| --- | --- |
| `--dry-run` | 报告将要进行的更改而不写入任何内容。 |
| `--system` | 移除当前机器上所有账户共享的保护配置。 |
| `--json` | 将执行结果以 JSON 格式输出。 |

### `rex terminfo show`

打印 terminfo 源码。

在其他机器上使用以下命令编译它：`rex terminfo show` &#124; tic `-x` -

### `rex terminfo host`

在其他机器上安装 Rex 的 terminfo 条目。

在远程主机上安装 xterm-rex 并记录其已安装，以便 ssh 停止向其宣告 xterm-256color。

记录会与 ssh 解析出的目标地址进行精确比对，因此同一台机器可以在多种拼写形式下被分别记录。

### `rex terminfo host install DESTINATION [-- SSH_OPTIONS...]`

在远程主机上安装 Rex 的 terminfo 条目。

通过 ssh 在 DESTINATION 上安装 xterm-rex，并记录该主机以便 ssh 停止向其宣告 xterm-256color。

条目源码通过管道传递给远程的 tic，由其编译到远程主机的 ~/.terminfo 中。远程主机上的其他内容均不改动，也不会启动交互式会话。-- 之后的选项会传递给 ssh，因此 “-- `-p` 2222” 和 “-- `-J` jump.example.com” 可照常使用。

条目会保存在你连接时使用的账户主目录中，而记录按主机维护。该主机上的其他账户不会拥有该条目。使用 “rex terminfo host forget” 可撤销记录。

记录的内容是你输入的拼写形式，因为保护配置正是与该形式进行比较。当你的 ssh 配置通过 HostName 重写该地址时，重写后的名称同样会被记录，因为系统全局保护配置会看到重写后的名称。无论哪种情况，同一台机器的其他拼写形式都会保持旧的终端类型，直到你也向它们安装条目。

### `rex terminfo host forget HOST`

遗忘主机已安装 Rex 的 terminfo 条目。

从 hosts 文件中移除 HOST，使 ssh 恢复向其宣告 xterm-256color。

当条目已从该主机移除，或者你以未安装该条目的账户连接时，请使用此命令。

HOST 为已记录的拼写形式。运行 “rex terminfo host ls” 可查看它们。

### `rex terminfo host ls`

列出记录为已安装 Rex terminfo 条目的主机，每行一个，按添加顺序排列。

每行都与 ssh 解析出的目标地址进行精确比对。同一台机器可以出现为多种拼写形式，且每种拼写形式都是一条独立的记录。

| 选项 | 说明 |
| --- | --- |
| `--json` | 将列表以 JSON 格式输出。 |

### `rex skill`

配置 Agent 以使用 Rex。

配置 Claude Code 和 Codex 等 Agent 以使用 Rex。

Rex 会向每个 Agent 安装两项内容：Skill 用于指导 Agent 如何使用 rex 命令；Hook（在支持 Hook 的 Agent 中）会在每次会话开始时告知 Agent 其当前运行的 Rex 会话和终端。两者在 Agent 每次使用时均从 rex 命令获取其文本，因此升级 Rex 也会同步更新向 Agent 提供的内容。

每个账户运行一次 “rex skill setup”，并运行 “rex skill status” 查看已安装的内容。

### `rex skill status`

报告 Rex 的 Skill 与 Hook 是否已安装。

针对 Rex 支持的每个 Agent，报告是否在当前机器上检测到该 Agent，以及是否在其内部安装了 Rex 的 Skill 与 Hook。不更改任何内容。

每个检查项的状态报告为以下之一：

  current      已安装且为最新
  outdated     由较旧版本 Rex 安装，或此后已被编辑修改
  missing      未安装
  foreign      同名文件存在但非 Rex 所安装
  unreadable   文件无法读取
  unsupported  该 Agent 不支持在此处存放该项

| 选项 | 说明 |
| --- | --- |
| `--project` | 针对当前代码仓库进行报告，而非针对你的账户。 |
| `--json` | 将报告以 JSON 格式打印。 |

### `rex skill setup`

为 Agent 安装 Rex 的 Skill 与 Hook。

为当前机器上发现的 Agent（或通过 `--agent` 指定的 Agent）安装 Rex 的 Skill 与 Hook。如果未发现任何 Agent，仅将 Skill 安装到大多数 Agent 读取的共享 ~/.agents/skills 目录中。

Skill 会存放在每个 Agent 的 skill 目录中。部分 Agent 共享同一个目录，该目录仅写入一次。Hook 会添加到每个 Agent 的设置文件中，设置文件的其余部分保持原样。部分 Agent 在运行新 Hook 之前会提示你进行确认，命令输出会说明具体操作方法。

每个账户运行一次该命令。重复运行是安全的，并会更新由较旧版本 Rex 安装的任何内容。

传入 `--session-naming` 可让 Agent 根据其任务命名会话。全新配置默认关闭该选项，再次运行 setup 将保持已安装的选择，除非显式传入该标志。

如果已安装名为 rex 的 Skill 且非 Rex 所安装，命令将保留该 Skill 并报告冲突。使用 `--force` 可强制替换它。

| 选项 | 说明 |
| --- | --- |
| `--agent AGENT` | 仅配置 AGENT，可选值为 claude、codex、opencode 或 pi（可重复指定）。 |
| `--project` | 配置当前代码仓库而非你的账户。 |
| `--dry-run` | 报告将要进行的更改而不进行任何更改。 |
| `--force` | 替换非 Rex 安装的名为 rex 的 Skill。 |
| `--session-naming` | 指示 Agent 根据其任务命名会话（省略则保持已安装的选择）。 |
| `--json` | 将结果以 JSON 格式打印。 |

### `rex skill remove`

从 Agent 中移除 Rex 的 Skill 与 Hook。

从 Rex 支持的每个 Agent（或通过 `--agent` 指定的 Agent）中移除 Rex 的 Skill 与 Hook。已不再安装的 Agent 同样包含在内，因此不会残留 Rex 安装的任何内容。

仅移除由 Rex 安装的文件与 Hook，包括 Agent 读取的其他目录中旧版本的 Skill 副本。其他 Skill、Hook 与设置均保持原样。

| 选项 | 说明 |
| --- | --- |
| `--agent AGENT` | 仅处理 AGENT，可选值为 claude、codex、opencode 或 pi（可重复指定）。 |
| `--project` | 从当前代码仓库中移除而非你的账户。 |
| `--dry-run` | 报告将要进行的更改而不进行任何更改。 |
| `--json` | 将结果以 JSON 格式打印。 |

### `rex skill show`

打印 Rex Skill 提供给 Agent 的指南。

安装了该 Skill 的 Agent 可以通过 Skill 直接读取该指南。未安装该 Skill 的 Agent 可以运行此命令读取同一指南。

### `rex version`

打印版本信息。

| 选项 | 说明 |
| --- | --- |
| `--json` | 将版本信息以 JSON 格式输出。 |

## 全局选项

每个命令均接受以下选项。

| 选项 | 说明 |
| --- | --- |
| `--autostart` | 自动启动缺失的本地服务端。默认为 `true`。 |
| `-C, --client CLIENT` | 针对客户端 CLIENT 执行操作，传入标签或 ID。 |
| `--color WHEN` | 将颜色输出 WHEN 设置为 auto、always 或 never。默认为 `auto`。 |
| `-S, --server SERVER` | 连接到 SERVER，可为主机标签或服务端地址（带端口的值始终视为地址）。 |
| `--timeout DURATION` | 将每个连接和非流式请求限制在 DURATION。默认为 `10s`。 |
| `-v, --verbose count` | 增加诊断输出的详细程度（可重复指定）。 |
