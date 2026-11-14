> 原文：https://www.superlogical.com/rex/docs/automate/server-api
> 原文版本：6e3111864904（抓取于 2026-11-13）

# 服务端 API

服务端自带对其自身 API 的完整文档。在 CLI 中即可列出所有方法、查阅某一方法的参数与返回值，以及调用该方法：

```sh
rex api list
rex api describe session.new_split
rex api call server.version
```

由于文档直接来自所连接的服务端，因此其内容始终与当前服务端的版本严格一致。

CLI 和 Lua API 均动态派生自所连接的服务端 API，因此这些命令在构建更高层次的脚本与自动化方案时同样至关重要。

## 发现方法

`rex api list` 打印每个方法及其简要描述：

```
$ rex api list
METHOD              DESCRIPTION
block.close         Close a block within a session. ...
block.event         Deliver an external event to a block within a session.
block.method        Invoke a typed method on a block within a session ...
...
```

第二个表格列出了[块提供的方法](#块方法)，例如读取终端屏幕等操作。

使用 `-q` 仅输出方法名称，便于进行搜索筛选：

```
$ rex api list -q | grep label
client.set_label
session.set_block_label
session.set_label
session.set_window_label
```

## 阅读方法文档

`rex api describe` 打印服务端掌握的关于指定方法的所有信息：功能用途、接受的参数、返回的结果以及各自的示例。

```
$ rex api describe session.set_block_label
Update a block's human-readable display label. ...

Method: session.set_block_label

Input schema:
{
  "type": "object",
  "properties": {
    "block_id": { "type": ["string", "null"] },
    "label": { "type": "string" },
    "session_id": { "type": "string" }
  },
  "required": ["session_id"],
  "additionalProperties": false
}

Output schema:
{
  "type": "object",
  "properties": {
    "revision": { "type": "integer", "minimum": 0 }
  },
  "required": ["revision"],
  "additionalProperties": false
}

Request example:
{
  "session_id": "session:<uuid>",
  "block_id": "block:<uuid>",
  "label": "shell"
}

Response example:
{"revision": 42}
```

这些 Schema 遵循 [JSON Schema](https://json-schema.org) 规范。解读方式如下：

- `properties` 列出每个参数及其类型。
- `required` 列出必须提供的参数。
- `additionalProperties: false` 意味着传入拼写错误的参数会直接报错，而不会被静默忽略。

查看请求示例通常是了解调用格式最快捷的方式。部分方法还会输出校验说明，用以描述 Schema 无法表达的业务规则。

## 调用方法

`rex api call` 调用指定方法并将其结果打印为 JSON：

```
$ rex api call server.version
{
  "rex_version": "0.1.0",
  "platform": "darwin_arm64",
  ...
}
```

参数为一个 JSON 对象。可以直接传入该 JSON 字符串、使用 `@` 从文件读取，或使用 `-` 从标准输入读取：

```sh
rex api call -s work session.set_label '{"label": "api"}'
rex api call session.create @layout.json
echo '{"label": "work"}' | rex api call session.create -
```

大多数 `session.` 方法都需要 `session_id`。使用 `-s` 指定会话后，`rex api call` 会自动将其加入到参数中：

```sh
rex api call -s work session.view
```

与其他 `rex` 命令不同，`rex api call` 默认不会自动采用当前所处的会话。在 Rex 终端内部，请传入 `-s "$REX_SESSION"` 以使用当前会话。

其他 ID 绝不会自动填入。作用于块的方法必须在参数中显式包含其 `block_id`。

输出打印到终端时会自动缩进排版，通过管道传递时则保持在单行中，便于配合 [`jq`](https://jqlang.org) 处理：

```sh
rex api call -s work session.view | jq '.windows | length'
```

### 错误处理

失败的调用会打印服务端的错误消息并以非零状态码退出：

```
$ rex api call -s work session.set_block_label '{"lable": "x"}'
Error: ... input: validating: block_id is required (status=400 code=bad_request)
```

`code` 指明失败的类型。`bad_request` 表示参数有误，而 `method_not_found` 表示服务端不存在该名称的方法，这通常发生在服务端版本低于当前阅读的文档版本时。

## 在 Lua 中调用

`rex.call` 接收方法的完整名称并以表的形式接收其参数：

```lua
local version = rex.call("server.version")
print(version.rex_version)
```

每个作用于单个会话的 `session.` 方法在 `rex.session` 下均有同名的辅助函数：

| API 方法 | Lua |
| --- | --- |
| `session.view` | `rex.session.view{}` |
| `session.set_label` | `rex.session.set_label{ label = "work" }` |
| `session.new_split` | `rex.session.new_split{ ... }` |

参数和结果与 `rex api describe` 显示的完全一致，仅以 Lua 表的形式书写而非 JSON。当省略 `session_id` 时，这些辅助函数会自动进行补全。`rex.call` 则不会自动补全，因此通过它调用 `session.` 方法时需自行传入 `rex.session_id`。

少数 `session.` 方法没有提供辅助函数，因为它们不作用于已存在的会话，例如 `session.list` 和 `session.create`。请使用 `rex.call` 调用这些方法。

失败的调用会返回 `nil` 和服务端的错误消息：

```lua
local result, err = rex.session.set_block_label{ lable = "x" }
if err ~= nil then error(err, 0) end
```

[Lua API 参考](../reference/lua.md#调用-rex)对这些函数进行了完整介绍。

## 块方法

块提供了各自专属的方法。`rex api list` 在第二个表格中打印它们，按提供这些方法的块类型命名：

```
Block methods:
CREATOR                    METHOD                             DESCRIPTION
com.superlogical.terminal  com.superlogical.terminal.format   Format the current terminal screen ...
com.superlogical.terminal  com.superlogical.terminal.pwd      Return the working directory ...
com.superlogical.terminal  com.superlogical.terminal.title    Return the current terminal title.
...
```

查阅块方法文档的方式与任何其他方法相同：

```sh
rex api describe com.superlogical.terminal.format
```

调用块方法时，传入目标块的 `block_id`，并将该方法自身的参数置于 `args` 下：

```sh
rex api call -s work com.superlogical.terminal.format \
  '{"block_id": "block:01a1...", "args": {"trim": true}}'
```

在 Lua 中，`rex.block.call` 会自动构建该包装层并填入当前块：

```lua
local terminal = "com.superlogical.terminal"
local screen = rex.block.call(terminal, "format", { trim = true })
print(screen.content)
```

## 机器可读文档

两个发现命令均支持 `--json` 参数，用于输出服务端对其自身 API 的结构化描述：

```sh
rex api list --json       # 所有方法，附带 Schema 与示例
rex api describe session.view --json
```

每个方法包含 `name`、`description`、`input_schema`、`output_schema`，以及在服务端具备时的 `request_example`、`response_example` 和 `validation_notes`。

这在生成语言绑定、在运行前针对服务端校验脚本、以及为编程智能体提供即将调用的 API 精确结构时非常有用。
