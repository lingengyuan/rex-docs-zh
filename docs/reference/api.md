> 原文：https://www.superlogical.com/rex/docs/reference/api
> 原文版本：598f733348b4（抓取于 2026-11-20）

# 服务端 API

本页列出控制 API 中的每个方法。有关其调用方法，参见 [服务端 API](../automate/server-api.md)。任何带有 [Snapshot](../linux/installation.md#发布通道) 标记的内容均处于 snapshot 通道，尚未进入 preview。

<div class="reference-page methods" hidden></div>

## `block`

### `block.close`

关闭一个块并终止其中运行的程序。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 包含该块的会话。 |
| `block_id` |  | 要关闭的块。可以是一个分离块。此参数与 window_id 二选一发送，不能同时发送。 |
| `window_id` |  | 要关闭其当前焦点块的窗口。不一定是活动窗口。此参数与 block_id 二选一发送，不能同时发送。 |
| `keep_last` |  | 若为 true，当窗口仅剩一个块时（计入浮动层）将报错失败而非关闭该块。对分离块忽略此选项。 |

`block_id` 与 `window_id` 必须且只能发送其中一个。若两者同时发送或均未发送，调用将失败并返回错误码 `bad_request`。

块关闭时，服务端会发送 `block_closed` 事件。若该块是所在窗口中的最后一个块，该窗口也会随之关闭，且服务端会发送 `window_closed` 事件。

若 `keep_last` 为 true 且该块是窗口中仅剩的一个块（计入浮动层中的块），调用将失败并返回 `bad_request`，且不会关闭任何内容。

若该块的创建者仍在对其进行放置布局，调用会立即返回，块将在放置完成时关闭。

在同一个连接上，`block.close` 会等待可能改变焦点的更早请求（如 `session.new_split` 和 `session.focus_block`）执行完毕。因此，通过 `window_id` 执行的关闭操作会关闭这些请求最终聚焦的块。

若会话不存在，调用将失败并返回 `session_not_found`。若 `block_id` 或 `window_id` 指定了不在该会话中的目标，或者窗口没有获得焦点的块，调用将失败并返回 `not_found`。

### `block.event`

向块发送输入事件，如按键或粘贴。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 包含该块的会话。 |
| `block_id` | 是 | 要接收事件的块。 |
| `event` | 是 | 要发送的事件：其类型（如 paste）及载荷。 |

客户端只能发送 `key`、`paste`、`mouse`、`wheel` 和 `focus` 事件。其他所有类型的事件仅由服务端发送。`paste` 事件的 `payload` 为 `{"text": "..."}`，`focus` 事件的 `payload` 为 `{"action": "in"}` 或 `{"action": "out"}`。

该事件直接传递给块，因此 Lua 按键绑定绝不会接收到它。若要让按键绑定优先处理按键，请改用 `client.key`。

在同一个连接上，`block.event` 调用按顺序逐一执行，并与 `client.key` 保持顺序，因此块会按发送顺序接收事件。

一旦块接收到事件，调用即会返回，此时块可能尚未完成对事件的处理。

若缺少 `event` 或其 `payload` 格式与类型不符，调用将失败并返回 `bad_request`。若 `event.type` 为空、指定了仅服务端发送的事件类型，或指定了当前服务端未知的事件，调用同样失败并返回 `bad_request`。

若会话不存在，调用失败并返回 `session_not_found`；若 `block_id` 指定的块不在该会话中，调用失败并返回 `not_found`。

### `block.method`

调用块提供的方法并返回其结果。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 包含该块的会话。 |
| `block_id` | 是 | 要调用方法的块。 |
| `method` | 是 | 块方法的简短名称，如 write 或 format。 |
| `args` |  | 块方法自身的参数。省略时等同于空对象。 |

在 `method` 中传入块方法的简短名称，如 `write`。`help.all` 在 `block_types` 下列出了各创建者块所提供的方法，以及每个方法的 `args_schema` 和 `output_schema`。

每个块方法也可以使用其全名调用（如 `com.superlogical.terminal.write`），传入相同的 `session_id`、`block_id` 和 `args`。全名中包含块创建者的名称，因此该调用仅适用于该创建者所创建的块。在任何其他块上调用将失败并返回 `conflict`。

结果为块方法自身的结果，格式如其 `output_schema` 所述。`block.method` 自身没有专用的结果模式（schema）。

`block.method` 不会等待同一连接上的更早请求，并且可以与 `client.key` 并发运行。若调用依赖于更早的请求，请先等待该请求的回复。若要按顺序与 `client.key` 一同调用块方法（例如通过按键绑定触发），请使用 `client.action`。

若缺少 `block_id`，调用失败并返回 `bad_request`。若会话不存在，失败并返回 `session_not_found`。若 `block_id` 指定的块不在会话中，失败并返回 `not_found`；若块没有名为 `method` 的方法，失败并返回 `method_not_found`。若 `args` 缺少必填字段或包含类型错误的值，失败并返回 `bad_request`。

## `block_creator`

### `block_creator.list`

列出服务端可用于创建块的创建者及其特点类型（flavors）。

创建者按 `name` 排序。

要创建块，将某一特点类型的 `flavor` 传入 `session.new_block` 或布局中的 `block`，并提供与其 `options_schema` 相匹配的 `options`。

`api.methods` 列出了该创建者的每个块所提供的方法。可使用 `<creator>.<method>`（如 `com.superlogical.terminal.title`）进行调用，在 `session_id`、`block_id` 及 `args` 下传入参数。

方法的 `actions` 指用户可以对块执行的操作，例如在 Rex.app 的命令面板中选择条目或按下快捷键。执行操作会使用该操作的 `args` 调用方法，这些参数是固定值，而非类似 `client.keymap` 为操作所列出 `args` 那样的模式定义。


## `client`

### `client.action`

以当前客户端身份执行来自配置文件或块的操作。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `action` | 是 | 操作的全名，如 dev_layout 或 com.superlogical.terminal.reset。client.keymap 列出了这些名称。 |
| `args` |  | 操作的参数，以 JSON 对象形式传入。若无参数请省略，对于创建者声明的操作始终省略。 |
| `origin` |  | 请求的来源：key、palette 或 api（默认）。操作将其读取为 ctx.origin。其他值均视为 api，但 script 会导致调用失败并返回 bad_request。 |
| `session_id` |  | 操作所应用到的会话。对于块操作为必填项。配置文件操作可以省略，此时没有默认会话。 |
| `block_id` |  | 操作所应用到的块。默认为会话的当前焦点块，除非设置了 server。需要指定 session_id。 |
| `servers` |  | 该客户端连接的其他服务端，配置文件操作可通过 rex.server(name) 进行调用。不要列出当前接收此请求的服务端。 |
| `server` |  | 来自 servers 中保存 session_id 和 block_id 的服务端名称。当它们位于接收当前请求的服务端上时请省略。 |

`action` 决定运行的内容。不带点的名称（如 `dev_layout`）是由配置文件通过 `rex.action` 定义的操作。带点的名称（如 `com.superlogical.terminal.reset`）是以其创建者命名的块操作或方法。`client.keymap` 在 `actions` 中列出了所有名称。

块操作（如 `com.superlogical.terminal.reset`）具有固定参数，因此带有 `args` 的请求会失败并返回 `bad_request`。块方法（如 `com.superlogical.terminal.write`）从 `args` 中获取其参数。

若 `args` 不是对象，调用失败并返回 `bad_request`。`null` 视为省略。

客户端自身的操作（如 `pane.split`）在客户端内部运行，无法发送至此处。针对此类操作或服务端未知的任何名称发起的请求均会失败并返回 `not_found`。

在每个连接上，`client.key`、`client.action`、`block.event` 以及改变焦点或布局的方法均按到达顺序逐一执行。对于绑定到按键的操作，请使用此方法而非按名称直接调用块方法（如 `com.superlogical.terminal.write`），以确保操作在先于其键入的按键之后生效。

当设置了 `session_id` 时，连接必须已通过 `session.attach`、`session.bootstrap` 或 `session.attach_all` 附加到该会话，否则调用失败并返回 `conflict`。若 `session_id` 未指定有效会话，调用失败并返回 `session_not_found`。设置了 `server` 时不执行这两项检查。

对于任何块操作或方法，以及只要发送了 `block_id`，均必须发送 `session_id`，否则调用失败并返回 `bad_request`。块操作或方法在 `block_id` 上运行；若省略该参数，则在会话的当前焦点块上运行。若会话没有焦点块，调用失败并返回 `conflict`。

若该块不属于该操作或方法适用的类型，调用失败并返回 `conflict`。若 `block_id` 指定的块不在会话中，失败并返回 `not_found`。

来自配置文件的操作可以省略 `session_id`。此时它没有 `ctx.session_id`，且其 `rex.session` 调用没有默认会话。指定 `session_id` 时，它将 `block_id`（或焦点块）视作 `ctx.block_id`。

若 `origin` 为 `script`，调用失败并返回 `bad_request`，因为只有 `rex.invoke` 可以报告该来源。

来自配置文件的操作最长可运行 30 秒，包括等待其他服务端的时间。若运行超时，调用失败并返回 `timeout`。若在运行期间重新加载了配置文件，调用失败并返回 `conflict`。

若来自配置文件的操作引发错误，调用失败并返回以发生位置开头的消息（如 `init.lua:4: attempt to index a nil value`）。无论操作因何失败，其中部分逻辑可能已经执行。

`servers` 中的每个条目都需要具有唯一且非空的 `name` 和非空的 `id`，且 `server` 必须指向其中之一。否则调用失败并返回 `bad_request`。服务端不解析这两个值的具体含义。

当会话属于 `servers` 之一时设置 `server`。此时 ID 会未经检查直接传递给操作，且不会自动填充焦点块，因此需自行发送 `block_id`。操作中的 `rex.session`、`rex.block.call` 和 `rex.call` 调用均会定向到该服务端。

设置了 `server` 时，任何带点的名称都会失败并返回 `bad_request`，因为块操作必须在包含该块的服务端上运行。请改将请求直接发送至该服务端。

当操作调用另一个服务端时，此连接会接收到 `client_call_requested` 事件。请在该远程服务端发起调用，并通过 `client.reply` 报告结果。若 10 秒内未收到回复或回复包含错误，操作的发起调用将失败，而操作继续运行。

### `client.inspect`

获取单个已连接客户端的详细信息，包括其提供的操作。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `client_id` | 是 | 要描述的客户端。可以是任何客户端，不仅限于调用者自身。 |

若缺少 `client_id` 或其不是合法的客户端 ID，调用失败并返回 `bad_request`。若其未指向任何已连接的客户端（包括已离开的客户端），调用失败并返回 `not_found`。

若要请求该客户端执行 `actions` 中的某个操作，请调用 `client.perform`。

### `client.key`

向块发送按键，让 Lua 按键绑定优先处理。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 键入按键所在的会话。 |
| `key` | 是 | 键盘报告的按键事件。 |
| `block_id` |  | 要发送按键的目标块。默认为会话的当前焦点块。 |
| `prefix` |  | 当 key 作为按键序列的结束时，在其之前按顺序按下的按键。对于 ctrl+b 紧接着 x，将 x 作为 key 发送，将 ctrl+b 在此处发送。 |

连接必须已通过 `session.attach`、`session.bootstrap` 或 `session.attach_all` 附加到 `session_id`，否则调用失败并返回 `conflict`。若 `session_id` 未指定有效会话，调用失败并返回 `session_not_found`。

未指定 `block_id` 时，按键发送至会话的当前焦点块。服务端在任何 Lua 函数运行前仅读取一次该焦点，因此改变焦点的函数不会改变按键的目标位置。无论哪种方式，Lua 函数均将接收按键的块视为 `ctx.block_id`。

在每个连接上，`client.key`、`client.action`、`block.event` 以及改变焦点或布局的方法均按到达顺序逐一执行。这保证了按键按发送顺序处理。

按键首先传递给该客户端脚本中绑定到该按键的 Lua 函数，然后传递给配置文件中的绑定函数。若没有任何函数接收该按键，它将发送给块。

只有绑定到 Lua 函数的按键才会进入 Lua，且仅在其被按下或处于长按重复状态时触发。其他所有按键均直接发送给块。`client.keymap` 将绑定的按键作为 `client.key.forward` 的绑定进行报告。

若没有 Lua 函数接收该按键且会话没有焦点块，按键不会发送到任何位置。调用仍然成功，且 `handled` 设置为 false。

若要发送按键序列，请等待整个序列完成。然后将其最后一个按键作为 `key` 发送，并将之前的按键作为 `prefix` 发送（如 `["ctrl+b"]`）。服务端不会在多次请求之间记住按键。

带有 `prefix` 的按键仅会传递给绑定到该完全一致序列的函数。不带前缀的按键仅传递给单独绑定到该按键的函数。

若没有函数接收该按键序列，只有 `key` 会继续发送给块。`prefix` 中的按键绝不会发送给块。

绑定到按键的 Lua 函数最长可运行 5 秒。若引发错误或运行超时，调用失败且按键不会到达块。

若 `prefix` 中的某个元素不是服务端能够识别的按键，调用失败并返回 `bad_request`，错误消息会指明该元素。

若没有 Lua 函数接收该按键且 `block_id` 指定的块不在会话中，调用失败并返回 `not_found`。

### `client.keymap`

获取当前客户端中每个按键的功能映射。其结果合并了客户端自身的绑定、配置文件以及客户端的 Lua 脚本。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `actions` |  | 客户端自身执行的操作。省略此项将跳过对未知操作和错误参数的检查。服务端会保留该列表以供 client.inspect 和 client.perform 使用。 |
| `server_actions` |  | 回复中列出服务端的哪些操作：all（默认全部）、configured（仅配置文件的操作）或 none。未知值视为 all。 |
| `defaults` |  | 客户端内置的图层，自底向上排列。它们位于配置文件之下。仅在其中发现的问题不会被报告，因为用户无法编辑它们。 |
| `overrides` |  | 用户在客户端中记录的快捷键图层，自底向上排列。它们位于配置文件及当前客户端脚本之上。其中的问题作为警告返回。 |

按键绑定自底向上分层堆叠：首先是你的 `defaults`，然后是账户的配置文件，接着是该客户端通过 `client.set_script` 加载的脚本，最后是你的 `overrides`。

图层的 `name` 成为其绑定以及关于该图层警告的 `source`。若名称为空、包含冒号，或与任一列表中的另一个图层重名，调用失败并返回 `bad_request`。

按键映射始终归属于发起调用的客户端，因此包含 `client_id` 的请求会失败并返回 `bad_request`。顶层包含 `bindings` 列表（早期服务端曾支持）的请求同样会失败并返回 `bad_request`。请改将这些绑定作为 `defaults` 中的图层发送。

按键序列（如 ctrl+b 后按 c）在 `keys` 中表示为 `["ctrl+b", "c"]`。配置文件将其写作 `ctrl+b>c`，但结果始终分开列出各个按键。服务端不会拆分类似 `ctrl+b>c` 的元素，而是将其视为无法识别的按键。

服务端能够识别的按键会以其标准拼写返回。`cmd+d` 与 `cmd+[KeyD]` 仍然是不同的按键：前者遵循键盘布局，后者指定物理按键。

服务端无法识别的按键拼写会在任一列表中保持原样保留，以便较新的客户端保留其按键。只有具有相同拼写的移除操作才能将其清除。包含任何此类按键的序列同样以这种方式保留。

按键序列位于其首个按键的堆栈上，按该按键其他绑定的顺序排列。若客户端能够执行的顶层绑定是一个序列，客户端需等待下一个按键。服务端在按键之间不保留状态，因此等待是客户端的职责。

在配置文件或该客户端脚本中绑定到 Lua 函数的按键，会作为 `client.key.forward` 的绑定返回。若要执行它，将按键发送到 `client.key`。将其视为始终可用：即使没有函数实际接收该按键，该按键堆栈下方的绑定也绝不会运行。

对于绑定到函数的序列，将其最后一个按键发送给 `client.key`，并将前面的按键作为 `prefix` 传入。该绑定仅针对该精确序列结束堆栈，因此以相同按键开头的其他序列仍然可以正常工作。

一个按键不能既运行其自身的绑定又启动一个序列，因此两者中层级较高者获胜。服务端保留两者并为每个按键添加一个警告，标明无法运行的绑定的 `source`、`action` 和 `key`。即使是对 `defaults` 中的绑定，除非其上方的绑定同样位于 `defaults` 中，服务端也会发出警告。

移除操作需完全匹配按键。移除 `["ctrl+b"]` 会保留以 ctrl+b 开头的所有序列，移除 `["ctrl+b", "c"]` 会保留 ctrl+b。

未移除任何内容的移除操作会收到警告，除非它位于 `defaults` 中、指定了服务端无法识别的按键，或在模式中屏蔽了按键。

带有 `mode` 的绑定或移除操作属于该模式，即客户端仅在该模式激活期间使用的一组绑定。若模式名称包含小写字母、数字、`_` 和 `-` 以外的任何字符，或者是 `root`，调用失败并返回 `bad_request`。

模式中的绑定会像其他绑定一样进行堆叠和检查。模式中的按键绝不会遮蔽模式外部相同的按键，且移除操作仅影响其自身模式。配置文件将模式中的按键写作 `resize/left`。

若任何图层在某一模式中绑定按键、屏蔽按键或通过 `rex.mode` 声明了该模式，`modes` 就会列出该模式。

在模式中未指定 `action` 的移除操作始终会屏蔽其按键，因此无论是否移除了任何内容，该按键都会列在模式的 `blocked` 中。指定了操作的移除操作绝不会屏蔽按键。

带有 `mode` 且没有 `keys` 的移除操作会移除整个模式：包括其绑定、其屏蔽的按键以及下方图层中的声明。若它同时指定了 `action`，调用失败并返回 `bad_request`。

在已移除模式之上，若某个图层绑定、屏蔽或声明了该模式中的按键，该模式会被恢复，但仅包含该图层及其上方图层的内容。否则该模式不会出现在 `modes` 中。

客户端通过自身的 `client.mode.enter`、`client.mode.exit` 和 `client.mode.exit_all` 操作决定哪个模式处于活动状态。服务端不保留模式状态。

若 `client.mode.enter` 绑定的 `name` 参数不是按键映射中的模式，或者声明的模式中未绑定任何内容，服务端会发出警告。

空请求会返回配置文件和该客户端脚本的绑定，而不检查未知操作或错误参数。

当 `actions` 不为空时，服务端在检查前会添加其自身的操作：配置文件通过 `rex.action` 定义的操作、每个块方法以及每个块操作。绑定到这些操作的条目绝不会被报告为未知。

带有错误参数的绑定会被保留并附带警告。绑定到块方法必须传递与其输入模式匹配的参数，未传递任何参数视为 `{}`。绑定到块操作或没有输入模式的方法必须不传递任何参数。

绑定到来自配置文件的操作必须匹配该操作声明的 `args` 模式（如果声明了）。客户端自身的操作不进行检查，因为客户端自行验证其参数。

结果中的 `actions` 按定义顺序列出配置文件的操作，然后按创建者和方法名排序依次列出每个创建者的方法和块操作。它不会重复返回你发送的操作。

`actions` 中的块方法没有 `title`，其 `args` 为其输入模式。可以绑定它，但不要在菜单中显示。块操作具有 `title` 且没有 `args`。

`server_actions` 仅改变结果中 `actions` 所列出的内容，不改变绑定针对哪些操作进行检查。

若要在绑定旁显示相关诊断信息，请将其 `action`、`key` 和 `mode` 与绑定的对应字段进行匹配。

当请求保持不变且 `config.instance_id` 与 `config.hash` 均匹配时，客户端可以继续使用缓存的结果。在每次调用 `client.set_script` 之后，以及在收到其 `hash` 与缓存不同的每次 `keymap_changed` 事件之后，请重新调用此方法。

### `client.list`

按连接顺序列出连接到服务端的客户端。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` |  | 仅列出通过 session.attach 或 session.bootstrap 附加到此会话的客户端。 |
| `kinds` |  | 仅列出属于这些类型（如 app）的客户端。未报告类型的客户端不匹配任何类型。 |

无参数时，结果列出所有已连接的客户端，包括类似 `rex` CLI 的短期客户端。

`session_id` 仅统计通过 `session.attach` 或 `session.bootstrap` 附加到该会话的客户端。仅调用过 `session.attach_all` 的连接不计入。任何客户端均可使用此过滤器，无论是否附加。

在 `kinds` 中，当前服务端未知的类型视为 `other`。未报告类型的客户端不匹配任何过滤器，甚至不匹配 `other`。

若客户端连接断开但未正常关闭，该客户端在列表中保留长达 60 秒，其 `connection_state` 设置为 `lost`，以便其重新连接。未附加到任何对象且没有脚本的客户端会立即移除。

若要保持此列表的副本为最新状态，可调用 `session.attach_all` 并将 `event_scope` 设置为 `all`。连接随后会接收到 `client_joined`、`client_left` 和 `client_changed` 事件。

### `client.perform`

请求另一个客户端执行其某项操作并等待其应答。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `client_id` | 是 | 要请求的客户端。若要按标签查找，调用 target.resolve 并将 kinds 设置为 client。 |
| `action` | 是 | 该客户端声明的操作名称，如 pane.split。client.inspect 列出了这些操作。最多 256 字节。 |
| `args` |  | 操作的参数，以 JSON 对象形式传入。若无参数请省略。 |
| `origin` |  | 引发该请求的原因，如 key、palette、api 或 cli。客户端将原样接收。留空代表 api。 |
| `session_id` |  | 操作所应用到的会话（如果有）。客户端直接接收，服务端不进行校验。 |
| `block_id` |  | 代替客户端焦点块作为操作目标的块（如果有）。客户端直接接收，服务端不进行校验。 |
| `timeout_ms` |  | 将请求发送给客户端后等待应答的时长（毫秒）。默认为 10000。超过 30000 的值视为 30000。 |

服务端向指定的客户端发送 `client_perform_requested` 事件并等待其通过 `client.reply` 做出应答。

服务端根据请求到达的连接告知目标客户端是谁发起的请求，因此客户端无法冒充其他客户端。

连接不需要附加到 `session_id`，因为服务端仅将其转发给客户端。

发往同一个客户端的请求会排队等待，客户端按到达顺序逐一应答。`timeout_ms` 从请求排到队首时开始计时。

缺少 `client_id` 或 `action`、`action` 超过 256 字节、`timeout_ms` 为负数，或者 `args` 不是对象或与操作模式不符的请求会失败并返回 `bad_request`。若 `client_id` 未指向已连接的客户端，调用失败并返回 `not_found`。

若客户端已列出其操作且 `action` 不在其中，调用失败并返回 `not_supported`。对于未列出任何操作的客户端仍会向其发送请求，它自身可能会回复 `not_supported`。

拒绝执行的客户端会回复 `refused`，调用以该错误码失败并附带说明原因的消息。

若客户端正在重新连接、已有 16 个请求在其队列中等待，或者在请求等待期间断开连接，调用失败并返回 `client_unavailable`。

若客户端未在规定时间内应答，调用失败并返回 `timeout`。客户端不会被告知超时，因此它稍后仍可能会执行该操作。

当请求结束时，服务端向将 `event_scope` 设为 `all` 调用了 `session.attach_all` 的连接发送带有执行结果的 `client_performed` 事件。未指定有效连接客户端的请求不发送事件。

### `client.reply`

应答 client_call_requested、client_perform_requested 或 client_prompt_requested 事件。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `call_id` | 是 | 所应答事件的 call_id。 |
| `result` |  | 调用的结果、操作返回的内容或提示的回答。若调用或操作无输出，请使用 null。对于提示，请发送提示结果：text、ids 或 cancelled。此参数与 error 二选一设置，不能同时设置。 |
| `error` |  | 调用失败、操作未执行或无法显示提示的原因。此参数与 result 二选一设置，不能同时设置。 |

`client_call_requested` 事件请求当前客户端在另一个服务端上执行一次调用，以配合仍在运行的 `client.action` 请求。必须应答每个事件，即使调用失败也是如此。在接收该事件的连接上发送事件的 `call_id`。

`client_perform_requested` 事件请求当前客户端为另一个客户端的 `client.perform` 请求执行其自身的操作之一。以相同方式进行应答。`result` 为操作返回的内容，或者为 `null`。

`client_prompt_requested` 事件请求当前客户端向使用它的用户提出一个问题，以响应调用了 `rex.ui` 的操作。待用户回答后进行应答：输入文本时将 `result` 设为 `{"text": "..."}`，选择项目时设为 `{"ids": ["..."]}`，若用户关闭了提示则设为 `{"cancelled": true}`。若发送提示不接受的结果（例如未提供的 ID），会返回 `bad_request` 并使提示继续处于等待状态。若无法显示提示，请将 `error.code` 设为 `not_supported`。

服务端会将提示发送给每个能够显示它的已连接应用，因此同一提示可能会在多个设备上同时打开。首个回答会在所有设备上结束该提示，取消操作亦然。随后，其他所有应用都会收到一条带有各自 `call_id` 的 `client_prompt_ended` 事件。无论该事件的 `reason` 为何，都应关闭提示。此后发出的应答会失败并返回 `not_found`。

同时设置了 `result` 和 `error`，或两者均未设置的回复会失败并返回 `bad_request`。对于没有结果的调用，发送 `"result": null`。

对于失败的调用，使用另一服务端返回的代码和消息，或解释无法发起调用的原因。等待的操作仅能看到错误消息。

对于未执行的操作，将 `error.code` 设置为 `not_supported`、`refused` 或 `internal`。发送 `client.perform` 的客户端将原样收到该代码。空代码作为 `internal` 发送。

如果 `error.message` 超过 4096 字节，服务端会将其截断并在末尾加上省略号（…），但仍会接受该回复。

回复一到达即会执行。它不会在此连接较早的 `client.key` 和 `client.action` 请求后面排队，因为等待该回复的 `client.action` 请求正阻塞着该队列。

未处于等待状态的 `call_id` 会失败并返回 `not_found`。这包括已经应答的调用和已超时的调用。

### `client.set_label`

设置或移除当前客户端的标签。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `label` | 是 | 要设置的标签，如 studio。空字符串表示移除。最多 64 字节，且不能包含控制字符。 |

标签始终归属于发送请求的客户端。包含 `client_id` 的请求会失败并返回 `bad_request`。

服务端在检查标签前会先去除 `label` 两端的空白字符，因此仅包含空格的标签会移除当前标签。

超过 64 字节、不是有效 UTF-8 或包含控制字符的标签会失败并返回 `bad_request`。错误消息会指出违反了哪项规则。

标签无需保持唯一。具有相同标签的两个客户端通过其 ID 进行区分。

标签供用户阅读。服务端绝不使用标签来决定客户端允许执行的操作。

当标签发生变更时，服务端向将 `event_scope` 设为 `all` 调用了 `session.attach_all` 的连接发送 `client_changed` 事件。

客户端在连接时也可以在其 `hello` 消息的 `client` 字段中发送标签。适用相同规则，但服务端会修正标签而非报错失败：截断超过 64 字节的标签，并丢弃其他无效标签。它还会截断超过 256 字节的 `name` 或 `version`。

### `client.set_script`

为当前客户端加载 Lua 脚本，替换其之前加载的所有脚本。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `scripts` | 是 | 要加载的所有 Lua 源码，按顺序执行。它们会替换之前加载的所有脚本。空列表表示卸载脚本。 |

脚本属于该客户端并在其附加的每个会话中生效。包含 `session_id` 或 `client_id` 的请求会失败并返回 `bad_request`。

若脚本存在语法错误、抛出异常，或在加载时运行超过 5 秒，调用失败并返回 `bad_request`。之前加载的脚本继续保持运行。

若要查看脚本绑定到函数的所有按键和按键序列，请调用 `client.keymap`。它将每个按键作为 `client.key.forward` 的绑定进行报告。

能够传递给脚本的按键在脚本加载时确定。脚本在运行期间动态绑定的函数，只有在脚本加载时已有函数绑定到该按键或序列的情况下，才能接收到按键。

成功的调用仍可能返回 `diagnostics`（即使严重级别为 `error`）。error 标记服务端跳过的脚本部分（例如绑定到无法识别的按键）。脚本的其余部分仍会正常加载。

加载脚本会改变该客户端的按键映射，且不会触发 `keymap_changed` 事件。每次调用此方法后请重新调用 `client.keymap`。


## `data`

### `data.connect`

获取用于打开与块的数据连接的一次性凭证。数据连接在块内容发生变化时（如终端输出）对其进行流式传输。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 包含该块的会话。连接必须已通过 session.attach 或 session.bootstrap 附加到该会话。 |
| `block_id` | 是 | 提供数据源的块。 |
| `data_ref_id` | 是 | 要打开该块的哪个数据源，例如 terminal。 |
| `subprotocol` |  | 数据连接将使用的子协议，例如 rex.data.terminal.v1。若设置此项，凭证仅在使用该子协议的连接上生效。 |

连接必须已通过 `session.attach` 或 `session.bootstrap` 附加到 `session_id`。仅通过 `session.attach_all` 附加是不够的。若连接未附加，调用失败并返回 `conflict`。

若要使用该凭证，请在服务端上打开连接至 `/api/data` 的 WebSocket，并在 HELLO 消息中发送该凭证。凭证仅限使用一次（即使握手失败也是如此），并在 `expires_in_ms` 后过期。

若其他用户提交了该凭证，数据连接将收到原因为 0x01 的 REJECT 拒绝响应（如同未知凭证一样）。该凭证随后会被消耗失效，你自身的数据连接也无法再使用它。

服务端仅校验 `data_ref_id` 格式是否规范。若块没有该名称的数据，服务端在握手完成后将以 WebSocket 状态码 1008 关闭数据连接。

将 `subprotocol` 设置为数据连接将使用的子协议，例如 `rex.data.terminal.v1`。若数据连接使用了不同的子协议，服务端会在发送任何数据前以 REJECT 原因 0x07 拒绝该数据连接。

若省略 `subprotocol`，块会在握手完成后检查子协议，并在不支持该子协议时以状态码 1008 关闭数据连接。

若 `data_ref_id` 或 `subprotocol` 格式错误，调用失败并返回 `bad_request`；若块不在会话中或没有可提供的数据，调用失败并返回 `not_found`。

## `focus_history`

### `focus_history.reverse`

按调用主体此前的焦点变更记录向后回退。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` |  | 仅回退到此会话中的块。客户端必须已附加到该会话。 |
| `not_session_id` |  | 仅回退到非此会话中的块。 |
| `window_id` |  | 仅回退到此窗口中的块。 |
| `not_window_id` |  | 仅回退到非此窗口中的块。 |
| `cursor` |  | 来自此前结果的游标，用于从上次调用停止处继续向后回退。省略则从当前焦点开始。 |

## `help`

### `help.all`

描述服务端提供的每个方法，包括块方法。

结果包含两个列表。`methods` 描述每个方法及其参数、结果、示例与说明。`block_types` 列出其块提供方法的每个创建者、其特点类型及这些方法。

结果描述的是当前连接的服务端，因此始终与该服务端的版本相匹配。

通过 HTTP，`GET /api/help` 返回包含附加 `http` 字段的相同文档，`/llms.txt` 则将其以 Markdown 格式展示。

## `hosts`

### `hosts.list`

列出服务端的主机列表：通过标签连接的其他 Rex 服务端。

每个 Rex 服务端都维护一个主机列表。你的每台设备从其作为主服务端的这一台服务端读取主机，因此它们看到的主机列表完全一致。

该列表包含服务端配置文件中通过 `rex.host` 声明的主机，以及客户端通过 `hosts.put` 添加的主机。声明的主机具有 `source`（如 `init.lua:4`）。通过 `hosts.put` 添加的主机没有 source。

每台主机均按其存储时的状态原样返回，包括当前服务端无法识别的字段。通过 `hosts.put` 将主机回传的客户端必须保留这些字段。

存在错误或其标签已被其他主机占用的已声明主机会被排除在 `hosts` 之外。`diagnostics` 中的警告会指明声明该主机的代码行。

没有状态目录启动的服务端无法存储主机，因此仅列出已声明的主机。

若手动编辑损坏了存储主机的文件，调用失败并返回 `conflict`，且错误消息会指明文件名。

### `hosts.put`

向服务端主机列表添加主机，或替换具有相同 ID 的主机。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `host` | 是 | 要添加的主机，或用于替换具有相同 id 的主机。 |

添加主机的设备负责选择其 `id`，因此再次发送相同的请求是安全的且不会重复添加。若 `host` 没有 `id`，服务端会生成一个。

若 `host` 与存储的主机在除 `updated_at` 之外的每个字段均匹配，则不会更改任何内容，且结果返回已存储的主机。

`label` 不能为空，不能以空白字符开头或结尾，且最多包含 64 个字符。忽略大小写的情况下，列表中不得有其他主机具有相同标签。若存在冲突，调用失败并返回 `conflict`，且错误消息会指明该主机（对于声明的主机，还会指明声明它的代码行）。

`endpoints` 至少需要一个端点，每个端点均采用 `rex` 的 `-S` 选项所接受的形式。不允许使用 Unix 套接字和命名管道，因为其路径仅在自身所在的机器上有效。

若要修改已声明的主机，put 一个带有其 `id` 的主机即可。服务端绝不会直接写入配置文件。它会存储你发送的主机，用以替代已声明的主机。put 还可以恢复通过 `hosts.remove` 移除的主机。

服务端会设置 `updated_at` 并去除 `source`。其他字段均按发送时的内容原样存储，包括其无法识别的字段。

当 put 操作改变列表时，每个已连接的客户端都会收到 `hosts_changed` 事件。

若 `host` 未通过校验，调用失败并返回 `bad_request`，错误消息会指明出错字段。没有状态目录启动的服务端无法存储主机，将失败并返回 `not_supported`。手动编辑损坏了存储主机的文件会导致调用失败并返回 `conflict`。

存储主机的文件最多可容纳 1 MiB，足以存储数千台主机。会导致文件超出该大小的 put 操作将失败并返回 `too_large`。

### `hosts.remove`

从服务端的主机列表中移除主机。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `id` | 是 | 要移除的主机。 |

移除不在列表中的主机不会报错。`removed` 为 false，不会更改任何内容，且不发送事件，因此重复调用是安全的。省略 `id` 时行为相同。

服务端绝不会直接写入配置文件，因此移除已声明的主机会将其隐藏。移除替代了已声明主机的已存储主机会将两者一并移除。无论哪种情况，只有后续带有相同 `id` 的 `hosts.put` 才能恢复该主机。

当主机被移除时，每个已连接的客户端都会收到 `hosts_changed` 事件。

若 `id` 不是有效的主机 ID，调用失败并返回 `bad_request`。没有状态目录启动的服务端无法存储主机，将失败并返回 `not_supported`。手动编辑损坏了存储主机的文件会导致调用失败并返回 `conflict`。

## `server`

### `server.apple.grant_file_access`

允许服务端及其运行的每个程序读取 Mac 应用获得的授权文件。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `files` | 是 | 要开放读取权限的文件列表，按拖拽或粘贴的顺序排列。最多 256 个。 |

当文件被拖入终端或粘贴到终端中时，Mac 应用会调用此方法。macOS 允许该应用打开文件，但不一定会允许服务端打开，因为 macOS 将服务端视为不同的应用。

对于每个文件，服务端首先尝试打开 `path`。仅当无法打开时才会使用 `token`，因此大多数文件（如项目中的文件）会返回 `readable`，且其 token 保持未使用。

服务端无法打开的文件不会导致整个调用失败。相对路径始终返回 `denied`。

访问权限持续到服务端退出为止。若文件返回 `denied` 或客户端无法识别的 `access` 值，请将文件复制到服务端可以读取的位置。

指定超过 256 个文件的请求将失败并返回 `bad_request`。

服务端仅在其本地 Unix 套接字（或 Windows 上的命名管道）上接受此方法。在任何其他连接（如 TCP 或 Tailscale）上，调用失败并返回 HTTP 状态码 403。

### `server.apple.privacy_status`

报告服务端及其程序拥有的 macOS 隐私权限。

macOS 根据其认定对进程负责的应用程序来决定隐私权限。服务端运行的每个 Shell 和程序都归属于服务端，因此它们都会获得此处列出的权限，而无论展示其终端的应用被允许了什么权限。

只有服务端能够读取其自身的权限。Mac 应用会调用此方法来展示这些权限，并在用户于“系统设置”中更改权限后再次调用。

读取权限绝不会触发 macOS 向用户弹窗询问任何确认。

`responsible_path` 是 macOS 认定对服务端负责的可执行文件路径。权限归属于包含该可执行文件的应用。当服务端是从终端应用在前台启动时，该负责应用即为该终端应用。

跳过未知的 `service`，并将未知的 `status` 视为 `unknown`。未运行在 macOS 上的服务端不列出任何服务。

服务端仅在其本地 Unix 套接字（或 Windows 上的命名管道）上接受此方法。在任何其他连接（如 TCP 或 Tailscale）上，调用失败并返回 HTTP 状态码 403。

### `server.config_reload`

重新加载配置文件并通知每个客户端重新获取其快捷键映射。

服务端重新读取其启动时读取的相同配置文件（通常是 `init.lua`），以及该文件通过 `require` 加载的模块。

下一次 `client.keymap` 调用的结果会在 `config.generation` 中报告相同的 `generation`，除非在此之前文件再次被重新加载。

阻止文件加载的错误（如 Lua 语法错误）不会导致调用失败。服务端会保留上一次成功加载的绑定、操作和主机，并在 `diagnostics` 中报告该错误。

若文件不再存在，重新加载会清除其先前声明的绑定、操作和主机。这不会报错。

`diagnostics` 仅列出文件自身的问题。取决于客户端的问题（例如绑定到该客户端未提供的操作）改由 `client.keymap` 报告。

加载完成后，每个已连接的客户端都会收到带有新 `generation` 和 `hash` 的 `keymap_changed` 事件。若客户端上一次 `client.keymap` 结果具有相同的 `hash` 且来自同一个服务端进程（即相同的 `instance_id`），客户端可以保留其快捷键映射。

若重新加载改变了主机列表（如添加或删除了 `rex.host` 声明），每个已连接的客户端还会收到 `hosts_changed` 事件。

服务端仅在其本地 Unix 套接字（或 Windows 上的命名管道）上接受此方法。在任何其他连接（如 TCP 或 Tailscale）上，调用失败并返回 HTTP 状态码 403。

### `server.status`

获取服务端的标识、会话计数、配置及 Tailscale 状态。

两个服务端仅在其能够访问相同文件时才会报告相同的 `host_id`，正如单个用户在一台机器上运行的两个服务端通常那样。若值不相同或任一缺失，应假定服务端之间不共享文件。该值不具有其他含义。

`config` 描述配置文件的最新加载状态。其 `generation` 和 `hash` 与同一时刻获取的 `client.keymap` 结果中的 `config` 一致。

保存了按键映射的客户端可以将其保存的值与 `config.hash` 和 `instance_id` 进行比对。若有任何不同，请重新调用 `client.keymap`。

后续对 `tailscale` 的变更会作为 `tailscale_status_changed` 事件送达，只有调用了 `session.attach_all` 或 `session.bootstrap` 的连接才能接收该事件。

### `server.stop`

关闭服务端；指定 if_idle 时仅在无任何占用的情况下关闭。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `if_idle` |  | 仅在服务端没有会话且无其他客户端连接时停止。正在使用的服务端会以 conflict 拒绝请求并保持运行。 |

只有服务端本机上通过 Unix 套接字或命名管道连接的客户端才能调用此方法。

不带 `if_idle` 时，服务端无论当前正在处理什么都会停止，且其会话中运行的每个程序都会终止。

指定 `if_idle` 时，服务端仅在其没有任何会话（包括仍在创建或关闭中的会话）且除调用者外无其他连接客户端时才会停止。否则它将继续运行，且调用失败并返回 `conflict`。错误消息会说明当前有哪些占用。

服务端在一单步操作中完成检查与停止。在检查刚完成之后尝试连接的客户端将被拒绝。

服务端会在关闭之前回复。在读取回复后请关闭连接。服务端在停止前最多等待连接关闭一秒钟。

在另一个程序内部运行且没有自身独立进程的服务端会使此调用失败并返回 `not_supported`。

服务端仅在其本地 Unix 套接字（或 Windows 上的命名管道）上接受此方法。在任何其他连接（如 TCP 或 Tailscale）上，调用失败并返回 HTTP 状态码 403。

### `server.tailscale.disable`

关闭内置 Tailscale，保留其登录凭证以供下次启用。

关闭内置 Tailscale 会断开通过 tailnet 接入的每个连接。会话保持运行。

设备保留其登录凭证，因此下一次 `server.tailscale.enable` 无需登录即可重新连接。若要退出登录，请调用 `server.tailscale.logout`。

若内置 Tailscale 已经处于关闭状态，调用不改变任何内容并返回当前状态，因此重复调用是安全的。

若服务端无法运行内置 Tailscale，调用失败并返回 `not_supported`。

服务端仅在其本地 Unix 套接字（或 Windows 上的命名管道）上接受此方法。在任何其他连接（如 TCP 或 Tailscale）上，调用失败并返回 HTTP 状态码 403。

### `server.tailscale.enable`

开启内置 Tailscale，使你的 tailnet 上的设备能够访问服务端。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `hostname` |  | 若此次调用启动了设备，所使用的设备名称，如 studio。若省略，服务端使用其配置的名称或 rex。 |
| `allow_tailnet_members` | 是 | True 允许 tailnet 访问规则许可的任何人访问。False 仅允许登录该设备的 Tailscale 用户访问。在每次调用时均生效，即使设备已开启。 |
| `auth_key` |  | 用于无需浏览器即可登录设备的 Tailscale 认证密钥。仅在本次调用启动设备时使用。绝不记录日志或保存。 |
| `advertise_tags` |  | 设备登录时携带的 Tailscale 标签（如 tag:rex）。仅在本次调用启动设备时使用。需要将 allow_tailnet_members 设置为 true。 |
| `control_url` |  | 若本次调用启动设备，所登录的控制服务器地址，如 https://headscale.example.com。若省略，服务端使用其配置的控制服务器或 Tailscale 官方服务器。 |

内置 Tailscale 是集成在 Rex 内部的 Tailscale 实现。它使服务端作为独立的设备加入你的 tailnet，因此宿主机无需安装 Tailscale。

若内置 Tailscale 已处于开启状态，调用仅应用 `allow_tailnet_members`，而不会重启设备或中断连接。它会忽略 `hostname`、`auth_key` 和 `advertise_tags`。

设备首次启动时必须登录到 Tailscale。使用有效的 `auth_key` 可以在无浏览器环境下直接登录。否则 `state` 会变为 `needs_login`，且登录链接将出现在 `auth_url` 以及服务端日志中。

设备保留其登录凭证，因此后续调用无需 `auth_key`。服务端绝不记录、保存或返回该密钥。

`advertise_tags` 将设备登录为打标签的设备（无所有者），因此需要将 `allow_tailnet_members` 设置为 true。登录设备的认证密钥或 OAuth 客户端必须被允许授予这些标签。

一旦设备启动，调用即会返回，此时它可能尚未完成连接。只有在 `https.state` 变为 `available` 之后，服务端才能通过 tailnet 访问。在调用了 `session.attach_all` 或 `session.bootstrap` 的连接上，可通过 `tailscale_status_changed` 事件跟踪进度。

若 HTTPS 监听器随后发生故障，内置 Tailscale 会自动关闭：`state` 变为 `disabled`，`error` 说明原因。

当调用启动设备时，若标签不是合法的 Tailscale 标签，或者在 `allow_tailnet_members` 为 false 时指定了标签，调用将失败并返回 `bad_request`。

在服务端正在关闭期间，调用失败并返回 `conflict`。

若服务端无法运行内置 Tailscale，调用失败并返回 `not_supported`。

服务端仅在其本地 Unix 套接字（或 Windows 上的命名管道）上接受此方法。在任何其他连接（如 TCP 或 Tailscale）上，调用失败并返回 HTTP 状态码 403。

### `server.tailscale.login`

向 Tailscale 请求服务端 Tailscale 设备的登录链接。

此调用发起登录请求并立即返回，而不等待链接生成。若 `auth_url` 为空，链接稍后会通过 `tailscale_status_changed` 事件送达（仅调用了 `session.attach_all` 或 `session.bootstrap` 的连接才能接收）。就绪后 `server.status` 同样会显示该链接。

在登录已在进行中时再次调用是安全的，且不会重复发起登录。

若内置 Tailscale 处于关闭状态，调用失败并返回 `conflict`。请先通过 `server.tailscale.enable` 将其开启。

若请求失败，或 Tailscale 在 10 秒内未接受请求，调用失败。服务端会在后台继续重试。

若服务端无法运行内置 Tailscale，调用失败并返回 `not_supported`。

服务端仅在其本地 Unix 套接字（或 Windows 上的命名管道）上接受此方法。在任何其他连接（如 TCP 或 Tailscale）上，调用失败并返回 HTTP 状态码 403。

### `server.tailscale.logout`

退出 Tailscale 并关闭内置 Tailscale。

退出登录后，内置 Tailscale 会自动关闭。下一次执行 `server.tailscale.enable` 必须重新登录。

若内置 Tailscale 已处于关闭状态，调用不改变任何内容且保存的登录状态保持不变。必须先将其开启才能退出登录。

若退出登录失败，或 Tailscale 在 10 秒内未做出响应，调用失败且内置 Tailscale 保持开启，以便你再次尝试。

若服务端无法运行内置 Tailscale，调用失败并返回 `not_supported`。

服务端仅在其本地 Unix 套接字（或 Windows 上的命名管道）上接受此方法。在任何其他连接（如 TCP 或 Tailscale）上，调用失败并返回 HTTP 状态码 403。

### `server.tailscale.rename`

更改服务端的 Tailscale 设备名称，无需重新登录。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `hostname` | 是 | 新的设备名称，如 studio：1 到 63 个 ASCII 字母、数字和连字符，首尾不能为连字符。 |

设备保留其身份与登录凭证。在服务端退出前，后续不带 `hostname` 的 `server.tailscale.enable` 也会使用新名称。

结果中的 `dns_name` 可能仍显示旧名称。新名称会在 `tailscale_status_changed` 事件中送达（在调用了 `session.attach_all` 或 `session.bootstrap` 的连接上）。

若内置 Tailscale 处于关闭状态，调用失败并返回 `conflict`。此时若要选择名称，请改将 `hostname` 传给 `server.tailscale.enable`。

若 `hostname` 不是合法的设备名称，调用失败并返回 `bad_request`。

若服务端无法运行内置 Tailscale，调用失败并返回 `not_supported`。

服务端仅在其本地 Unix 套接字（或 Windows 上的命名管道）上接受此方法。在任何其他连接（如 TCP 或 Tailscale）上，调用失败并返回 HTTP 状态码 403。

### `server.version`

获取服务端正在运行的 Rex 版本及其构建信息。

缺失 `api_revision` 或 `api_min_revision` 代表值为 0。在这些字段出现之前构建的服务端会省略这两者。

### `server.whoami`

获取服务端对你的身份识别结果，以及服务端运行所使用的账户。

`principal` 包含哪些字段取决于其 `kind`。`peer` 拥有 `uid`、`gid`，通常还有 `pid`。`windows_peer` 拥有 `sid`，通常还有 `pid`。`tailscale` 客户端拥有 `user_id`、`login_name` 和 `node`，若其设备被打标签还包含 `tags`。`anonymous` 客户端不包含上述任何字段。

服务端在连接建立时识别客户端。只要连接持续存在，`principal` 就保持不变。

`principal` 描述了服务端在允许客户端接入时已经做出的决定。请将其用于显示当前连接者，而非用于决定客户端允许执行的操作。


## `session`

### `session.attach`

附加到会话：开始接收其事件并获取其当前视图。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要附加到的会话。 |

在服务端读取 `view` 之前，连接即开始接收来自该会话的每条事件（包括 `block_event`）。请先应用 `view`，然后应用 `seq` 高于响应中 `seq` 的每条事件（即使该事件在响应之前送达也是如此）。

大多数接受 `session_id` 的方法仅在附加到该会话的连接上有效（通过此方法、`session.bootstrap` 或 `session.attach_all` 附加）。在未附加的连接上，它们会失败并返回 `conflict`。

附加使该连接的客户端成为会话的客户端之一。服务端会发送 `client_connected` 事件，且 `session.list_clients` 会列出该客户端。

`data.connect`、`session.own_block` 和 `session.disown_block` 需要此类附加。通过 `session.attach_all` 附加对它们来说是不够的。

对同一会话再次调用是安全的。它会返回相同的 `client_id` 和全新的 `view`。

若 `session_id` 未指定有效会话，调用失败并返回 `session_not_found`。

### `session.attach_all`

开始接收来自整个服务端的事件并获取会话列表。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `event_scope` | 是 | 要接收的事件范围。'session' 发送除 block_event 外的每个会话事件，外加 session_created、session_destroyed、session_moved 和 tailscale_status_changed。'all' 还会发送 block_event 和客户端事件（如 client_joined）。 |

除非你需要 `block_event` 或客户端事件，否则请使用 `session`。在 `all` 作用域下，客户端事件包括 `client_joined`、`client_left`、`client_changed`、`client_performed` 和 `client_script_events_dropped`。除 `session` 或 `all` 以外的任何值均失败并返回 `bad_request`。

无论作用域如何，连接仍会接收通过 `session.attach` 所附加会话的每条事件。

连接本身不会加入任何会话。它可以在每个会话上调用方法，但不会列在 `session.list_clients` 中，也无法调用 `data.connect` 或声明拥有块。若要同时加入会话，请调用 `session.attach`，或使用 `session.bootstrap` 在一次调用中完成这两项操作。

再次调用将使用新的 `event_scope` 替换原作用域。

会话列表是在事件开始发送后获取的快照。请在其上依次应用 `seq` 高于响应消息中 `seq` 的每条事件。

事件按顺序到达，且其 `seq` 连续无跳跃。若连接落后超过 8 MiB 的事件，服务端会直接关闭连接而非跳过事件。请打开新连接以获取全新快照。

### `session.bootstrap`

在一次调用中完成新连接的配置：接收事件、列出会话并附加。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `event_scope` | 是 | 要接收的事件范围。'session' 发送除 block_event 外的每个会话事件，外加 session_created、session_destroyed、session_moved 和 tailscale_status_changed。'all' 还会发送 block_event 和客户端事件（如 client_joined）。 |
| `preferred_session_id` |  | 要附加的会话（若存在）。否则服务端附加它能附加的第一个会话。设置 attach_session_ids 时忽略此项。 |
| `attach_session_ids` |  | 要附加的会话列表，按顺序排列。未知和重复的 ID 会被跳过，空列表不附加任何会话。省略此项则由服务端选择一个。 |
| `data_tickets` |  | 要为其签发数据凭证的块类型。响应中包含附加会话中匹配该类型的每个可见块的凭证。最多 8 个条目。 |

将其作为新连接上的第一个请求发送。请先应用其结果，然后应用 `seq` 高于响应中 `seq` 的每条事件（即使该事件在响应之前送达也是如此）。

`event_scope` 的运作方式与 `session.attach_all` 相同，连接随后可在任何会话上调用方法。除 `session` 或 `all` 以外的值均失败并返回 `bad_request`。

若省略 `attach_session_ids`，服务端会附加一个会话并在 `selected_session` 中返回它（若服务端没有会话，该字段为 null）。

若设置了 `attach_session_ids`（即使为空数组），服务端在 `attached_sessions` 中返回其附加的会话，并将 `selected_session` 保持为 null。

`attach_session_ids` 中在调用期间被销毁的会话会从 `attached_sessions` 中排除。若选作 `selected_session` 的会话在调用期间被销毁，调用失败并返回 `session_not_found`。任何其他附加失败也会导致整个调用失败。

若连接落后超过 8 MiB 的事件，服务端会直接关闭连接而非跳过事件。请打开新连接并再次调用 `session.bootstrap`。

若调用失败，请在重试之前关闭当前连接并打开新连接。初始配置中的部分操作可能已经生效。

### `session.close_layer`

关闭浮动层及其中包含的每个块。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `layer_id` | 是 | 要关闭的浮动层。其中的每个块也将随之关闭。 |

`layer_id` 必须指定浮动层。指定窗口的平铺布局（`session.view` 中类型为 `tiled` 的图层）将导致调用失败并返回 `bad_request`。请改用 `session.close_window` 关闭窗口。

服务端会关闭图层中的每个块，从而终止其中运行的程序。一旦块关闭，调用即会返回。

若该图层拥有焦点，焦点会返回给先前拥有焦点的图层中最后聚焦的块。否则焦点保持不变。

若该图层容纳了窗口中最后的块，服务端也会关闭该窗口。

若会话不存在，调用失败并返回 `session_not_found`。若 `layer_id` 未指定会话中的图层，调用失败并返回 `not_found`。

### `session.close_window`

关闭窗口及其中包含的每个块。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `window_id` |  | 要关闭的窗口。省略此项则关闭活动窗口。其中的每个块也将随之关闭。 |

服务端会关闭窗口中的每个块，从而终止其中运行的程序。一旦块关闭，调用即会返回。

若该窗口原本是活动窗口，其后一个窗口会变为活动窗口；若其原本为最后一个窗口，则前一个窗口变为活动窗口。

若会话不存在，调用失败并返回 `session_not_found`。若 `window_id` 指定的窗口不在会话中，失败并返回 `not_found`。窗口在开始关闭时就会立即脱离会话，因此对同一窗口关闭两次同样会失败并返回 `not_found`。

若省略 `window_id` 且会话中没有任何窗口，调用失败并返回 `conflict`。

### `session.create`

创建一个会话，可选择在其中预先包含其初始窗口。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `label` |  | 会话的标签，最多 128 字符。省略此项则由服务端选择一个（如 quiet-meadow）。 |
| `initial_windows` |  | 随会话一同创建的窗口列表，按顺序排列。最后一个窗口成为活动窗口。若其中任何一个失败，服务端不会创建会话。 |

所有参数均为可选。不传入任何参数时，服务端创建一个没有任何窗口的会话。

若省略 `label` 或其为空，服务端会选择一个其他会话未使用的标签（如 `quiet-meadow`）。

只有在 `initial_windows` 中的每个窗口均已就绪后，服务端才会发送 `session_created` 事件，因此没有任何客户端会看到半成品的会话。若有任何窗口创建失败，服务端会关闭会话及其所有块，且调用失败。

初始窗口中的块在创建时没有所有者，因为调用客户端还无法附加到尚未存在的会话。若要拥有这些块，请先调用 `session.attach`，再调用 `session.own_block`。

调用不会自动将连接附加到新会话。请调用 `session.attach` 以接收其事件。

若布局格式错误，调用在创建任何块之前即失败并返回 `bad_request`。没有创建者能够提供的特点类型（flavor）会失败并返回 `not_found`。

若服务端包含的会话数已达到上限，调用失败并返回 `conflict`。

### `session.describe_block`

获取块的详细信息及其提供的方法、事件和操作。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `block_id` | 是 | 要描述的块。可以是一个分离块。 |

`api` 列出了该块提供的方法和事件，格式与 `block_creator.list` 相同。可使用 `<creator>.<method>` 调用方法，传入 `session_id`、`block_id`，并在 `args` 下传入参数。

若 `block_id` 指定的块不在会话中或正在关闭，调用失败并返回 `not_found`。

### `session.destroy`

销毁会话并关闭其中的每个块。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要销毁的会话。其中的每个块都将关闭。 |

服务端会关闭会话中的每个窗口和块。关闭终端会挂断其中运行的程序，正如关闭终端窗口一样。

一旦会话关闭，调用即会返回。`session_destroyed` 是关于该会话的最后一个事件，不过随后可能仍会跟随一条针对该会话的 `client_script_events_dropped` 事件。

连接必须已通过 `session.attach`、`session.bootstrap` 或 `session.attach_all` 附加到该会话，否则调用失败并返回 `conflict`。

若 `session_id` 未指定有效会话，调用失败并返回 `session_not_found`。

### `session.detach`

断开连接与会话的附加关系。连接保持打开且会话继续运行。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要断开附加的会话。 |

连接的其他附加关系以及通过 `session.attach_all` 接收的任何事件均照常继续。

客户端离开该会话。服务端发送 `client_disconnected` 事件，且该客户端拥有的每个块将传递给排队等待的下一个客户端（如果有）。

若连接原本未附加到该会话，调用成功且不做任何更改，即使会话不存在也是如此。

对于同一会话仍在进行中的 `session.attach` 不会被取消。本次调用成功且不断开附加，attach 操作将继续完成。

若连接稍后再次附加到该会话，其客户端保留相同的 `client_id`。

### `session.detach_block`

将块移出其所在窗口而不关闭它。该块继续运行。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `block_id` | 是 | 要分离的块。它将继续运行但脱离其所在窗口。 |

`session.list_blocks` 会列出该块，其 `placement` 设置为 `detached`，随后可使用 `session.move_block` 将其重新放入窗口中。

分离原本已经分离的块会返回成功且不改变任何内容。

若该块是其所在窗口中的最后一个块，该窗口也会随之关闭。若该块是浮动层中的唯一块，该浮动层关闭。

若该块原本拥有焦点，其窗口中的另一个块会获得焦点。

若要改为关闭该块，请调用 `block.close`。

若 `block_id` 指定的块不在会话中，调用失败并返回 `not_found`。

### `session.disown_block`

放弃调用客户端对块的拥有权。结果列出每个块的所有者。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `block_ids` |  | 要放弃声明的块列表。省略或留空表示放弃会话中的所有块。 |

调用客户端必须已通过 `session.attach` 或 `session.bootstrap` 附加到该会话。仅调用过 `session.attach_all` 的连接将失败并返回 `bad_request`。

调用者拥有的块会传递给排队等待的下一个已连接客户端，或者变为无所有者状态。对于调用者原本未拥有的块，调用者仅从排队列表中退出。

`blocks` 列出调用后每个块的所有者，顺序与 `block_ids` 一致，重复的 ID 仅列出一次。当放弃所有块时，按 `block_id` 排序。

每次所有者变更都会发送 `block_owner_changed`。若窗口中的块发生所有者变更，调用还会发送一条 `session_view_changed` 事件。

若 `block_ids` 中的任何 ID 不是会话中的块，调用失败并返回 `bad_request`，且不做任何更改。

### `session.float_block`

将块从其窗口平铺布局中移入新的浮动层。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `block_id` | 是 | 要浮动的块。它必须位于所在窗口的平铺布局中，尚未处于浮动层中。 |
| `bounds` | 是 | 新浮动层所在位置，表示为窗口宽度和高度的分数比例 [x, y, w, h]。必须完全容纳在窗口内。 |

`bounds` 从窗口左上角起算。其宽度和高度必须大于 0。

新图层位于该块自身的窗口中，置于该窗口中所有其他浮动层的前方。

焦点和活动窗口保持不变。若窗口先前处于缩放状态，缩放将结束。

浮动窗口平铺布局中的最后一个块会使该平铺布局变空。窗口保持打开，其在 `session.view` 中类型为 `tiled` 的图层保持相同的 `layer_id`。

若会话不存在，调用失败并返回 `session_not_found`。若 `block_id` 指定的块不在任何窗口中（包括分离块），调用失败并返回 `not_found`；不合法的 `bounds` 失败并返回 `bad_request`。

若该块已处于浮动层中，调用失败并返回 `bad_request`。

### `session.focus_block`

聚焦一个块；若其所在窗口不是活动窗口，则将其设为活动窗口。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `block_id` | 是 | 要聚焦的块。它必须位于窗口中，该窗口将成为活动窗口。 |

该块可以位于窗口的平铺布局中，也可以位于浮动层中。若它尚未是其窗口的焦点块，该窗口中的任何缩放将结束。

若该块已经在活动窗口中拥有焦点，调用不做任何更改。

若会话不存在，调用失败并返回 `session_not_found`。若 `block_id` 指定的块不在任何窗口中（包括分离块），调用失败并返回 `not_found`。

### `session.focus_direction`

将焦点移动到左侧、右侧、上方或下方最近的块。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `direction` | 是 | 从活动窗口中的焦点块向哪个方向移动焦点。 |
| `wrap` |  | 当该方向没有块时是否从对侧边缘环回继续。默认为 false。较旧的服务端忽略此项并始终环回。 |

搜索从活动窗口的焦点块开始。它根据屏幕上的显示位置涵盖该窗口中的每个块（包含浮动层中的块）。当两个块距离相等时，前方层级的块获胜。

若在 `direction` 方向上没有块，焦点保持不变，调用仍然成功。移动焦点会结束窗口中的任何缩放状态。

若会话不存在，调用失败并返回 `session_not_found`。若会话没有任何窗口，调用失败并返回 `conflict`。


### `session.focus_next_pane`

将焦点移动到活动窗口中的下一个块。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `wrap` |  | 是否从最后一个块环回到第一个块。默认为 false。 |

块按布局顺序排列：首先是窗口的平铺布局，每个拆分先读取其 `before` 侧再读取其 `after` 侧，然后每个浮动层从后向前依次读取。

若没有下一个块，焦点保持不变，调用仍然成功。移动焦点会结束窗口中的任何缩放状态。

若会话不存在，调用失败并返回 `session_not_found`。若会话没有任何窗口，调用失败并返回 `conflict`。

### `session.focus_next_window`

将下一个窗口设为活动窗口。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `wrap` |  | 是否从最后一个窗口环回到第一个窗口。默认为 false。 |

窗口顺序即 `session.view` 中 `windows` 的顺序。

每个窗口保留其自身的焦点块，该块随后接收键盘输入。

若没有下一个窗口，不做任何更改，调用仍然成功。

若会话不存在，调用失败并返回 `session_not_found`。若会话没有任何窗口，调用失败并返回 `conflict`。

### `session.focus_previous_pane`

将焦点移动到活动窗口中的上一个块。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `wrap` |  | 是否从第一个块环回到最后一个块。默认为 false。 |

块按布局顺序排列：首先是窗口的平铺布局，每个拆分先读取其 `before` 侧再读取其 `after` 侧，然后每个浮动层从后向前依次读取。

若没有上一个块，焦点保持不变，调用仍然成功。移动焦点会结束窗口中的任何缩放状态。

若会话不存在，调用失败并返回 `session_not_found`。若会话没有任何窗口，调用失败并返回 `conflict`。

### `session.focus_previous_window`

将上一个窗口设为活动窗口。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `wrap` |  | 是否从第一个窗口环回到最后一个窗口。默认为 false。 |

窗口顺序即 `session.view` 中 `windows` 的顺序。

每个窗口保留其自身的焦点块，该块随后接收键盘输入。

若没有上一个窗口，不做任何更改，调用仍然成功。

若会话不存在，调用失败并返回 `session_not_found`。若会话没有任何窗口，调用失败并返回 `conflict`。

### `session.focus_window`

将某一窗口设为活动窗口。焦点进入其先前获得焦点的块。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `window_id` | 是 | 要激活的窗口。焦点移动到其先前获得焦点的块。 |

若该窗口已经是活动窗口，调用不做任何更改。

若会话不存在，调用失败并返回 `session_not_found`。若 `window_id` 指定的窗口不在会话中，调用失败并返回 `not_found`。

### `session.help`

描述此会话接受的方法以及其块提供的方法。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |

结果格式与 `help.all` 相同，并附带 `http` 字段。它仅描述该会话自身响应的方法（如 `session.view` 和 `session.new_split`），以及该会话可使用的创建者的块方法。

大多数客户端改用 `help.all`，后者描述服务端提供的所有方法。

### `session.list`

列出服务端上的会话。

会话按创建顺序列出，直到通过 `session.move` 改变该顺序。`session.attach_all` 与 `session.bootstrap` 按相同顺序列出会话。

### `session.list_blocks`

列出会话中的每个块，包括分离块。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |

将无法识别的 `placement` 视为 `detached`。该块存在且你可以调用其方法，但不要假设它显示在何处。

块按 `block_id` 排序。

若要查看每个块在其窗口中的位置以及哪个块拥有焦点，请调用 `session.view`。

### `session.list_clients`

列出附加到该会话的客户端。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |

仅列出通过 `session.attach` 或 `session.bootstrap` 附加的客户端。仅调用过 `session.attach_all` 的连接不包含在内。若要列出所有已连接的客户端，请调用 `client.list`。

### `session.lower_layer`

将浮动层后移至底层，或移至另一个浮动层的正下方。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `layer_id` | 是 | 要后移的浮动层。 |
| `relative_layer_id` |  | 同一窗口中的另一个浮动层，将目标图层置于其正下方。省略此项则移至所有其他浮动层之后。 |

`layer_id` 必须指定浮动层。指定窗口的平铺布局（`session.view` 中类型为 `tiled` 的图层）将导致调用失败并返回 `bad_request`。

浮动层绝不会移到窗口平铺布局的后方。在最底层时，它位于所有其他浮动层之后、平铺布局之前。

若该图层已处于对应位置，调用不做任何更改。焦点和图层边界绝不改变。

若会话不存在，调用失败并返回 `session_not_found`。若 `layer_id` 未指定会话中的图层，失败并返回 `not_found`；若 `relative_layer_id` 与 `layer_id` 相同，失败并返回 `bad_request`。

若 `relative_layer_id` 指定了类型为 `tiled` 的图层或另一个窗口中的图层，调用失败并返回 `bad_request`。若其未指定会话中的图层，失败并返回 `not_found`。

### `session.move`

将会话移动到 session.list 返回顺序中的另一个位置。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要移动的会话。 |
| `before_session_id` |  | 将其置于该会话正前方。省略此项则将会话移至末尾。 |

所有客户端看到的顺序完全一致。导致顺序改变的每次移动都会发送带有相同 `session_id` 和 `before_session_id` 的 `session_moved` 事件。

将会话移动到其当前所在位置会返回成功且不改变任何内容。

连接必须已通过 `session.attach`、`session.bootstrap` 或 `session.attach_all` 附加到其移动的会话，否则调用失败并返回 `conflict`。

若 `before_session_id` 指定了正在被移动的会话，调用失败并返回 `bad_request`。

若任一 ID 未指定有效会话，调用失败并返回 `session_not_found`，且错误消息会指明是哪一个。

### `session.move_block`

移动块（或放置分离块），在另一个块旁边的新拆分中进行布局。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `block_id` | 是 | 要移动的块。可以是一个分离块或已放置在任何窗口中的块。 |
| `anchor_block_id` | 是 | 要置于其旁的块。它必须已放置在窗口中。 |
| `direction` |  | 如何划分锚点空间：'horizontal' 代表左右并列，或 'vertical' 代表上下排列。默认为 horizontal。 |
| `side` |  | 移动块放置的位置：'before' 代表左侧或上方部分，或 'after' 代表右侧或下方部分。默认为 after。 |
| `ratio` |  | 前部所占空间的比例，大于 0 且小于 1。默认为 0.5。 |

被移动的块与锚点块可以位于不同的窗口或图层中。

若该块在其原窗口中拥有焦点，焦点会随之移动且其新窗口变为活动窗口。分离块不会带走焦点。

本次移动所改变的每个窗口中的缩放状态均会结束。

若移动导致某个浮动层变空，服务端会将其移除。若导致整个窗口变空，服务端会关闭该窗口。窗口的平铺布局在窗口仍有浮动层时变空则仍会保留，并保持相同的 `layer_id`。

除结果中指明的两个拆分外，其他每个拆分均保留其 ID。

若会话不存在，调用失败并返回 `session_not_found`。若 `block_id` 与 `anchor_block_id` 相同，或 `ratio` 超出范围，失败并返回 `bad_request`。若任一块不在会话中，或锚点块不在窗口中，失败并返回 `not_found`。

若该块为分离块或位于另一个窗口中，且锚点所在窗口容纳的块已达到上限，调用失败并返回 `conflict`。

### `session.move_window`

将会话中的窗口移动到窗口顺序中的另一个位置。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `window_id` | 是 | 要移动的窗口。 |
| `before_window_id` |  | 将其置于该窗口正前方。省略此项则将窗口移至末尾。 |

窗口顺序即 `session.view` 中 `windows` 的顺序以及 Rex.app 中标签页的顺序。`session.focus_next_window` 和 `session.focus_previous_window` 遵循该顺序。

活动窗口、焦点及窗口中的块保持不变。若窗口已在对应位置，调用不改变任何内容。

若会话不存在，调用失败并返回 `session_not_found`。若任一窗口不在会话中，失败并返回 `not_found`；若 `before_window_id` 与 `window_id` 相同，失败并返回 `bad_request`。

### `session.new_block`

创建一个块而不将其放置在窗口中。稍后可通过 session.move_block 进行放置。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `flavor` | 是 | 要创建的块特点类型，如 com.superlogical.terminal.shell。block_creator.list 列出了这些类型。 |
| `options` |  | 该块创建者的配置，格式符合 block_creator.list 中该特点类型的 options_schema。 |
| `label` |  | 块的标签，最多 128 字符。默认为特点类型的简短名称，如 shell。 |

服务端将 `options` 原样传递给特点类型的创建者。

块初始状态为分离（detached）：它运行、发送事件并响应方法调用，但没有任何窗口展示它。可使用 `session.move_block` 将其放置在窗口内的某个块旁边。

如果调用客户端已附加到该会话，则会成为该块的所有者；否则该块没有所有者，直到已附加的客户端通过 `session.own_block` 认领它。

格式错误的 `flavor` 或 `label` 失败并返回 `bad_request`。没有创建者提供的特点类型失败并返回 `not_found`。

若服务端容纳的块总数已达到上限，调用失败并返回 `conflict`。


### `session.new_layer`

在窗口前方的新浮动层中创建块。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `window_id` |  | 要添加浮动层的窗口。省略此项则使用活动窗口。 |
| `bounds` | 是 | 新浮动层所在位置，表示为窗口宽度和高度的分数比例 [x, y, w, h]。必须完全容纳在窗口内。 |
| `layout` | 是 | 要在浮动层中创建的块及其排列方式。每个节点包含 block（带有特点类型以及可选的 options 和 label）或 split（带有 direction、before、after 和可选的 ratio）。 |
| `focus` |  | 是否将该窗口设为活动窗口并聚焦第一个新块。默认为 false。 |

`bounds` 从窗口左上角起算。其宽度和高度必须大于 0。

`layout` 中的 `block` 节点根据特点类型（`flavor`，如 `com.superlogical.terminal.shell`）启动一个新块。`split` 节点将其空间划分为两部分，并在 `before` 和 `after` 中各包含另一个节点。

在 `split` 节点中，`direction` 为 `horizontal` 时将 `before` 置于 `after` 左侧，为 `vertical` 时将其置于上方。`ratio` 是 `before` 所占空间的比例，大于 0 且小于 1。默认为 0.5。

`layout` 始终会启动新块。若要将已经存在于窗口平铺布局中的块移动到浮动层中，请使用 `session.float_block`。

新图层位于窗口中所有其他浮动层的前方。

整个布局要么全部创建成功，要么完全不创建。若有任何块启动失败，服务端会关闭已启动的块，且调用失败。

若会话不存在，调用失败并返回 `session_not_found`。若 `window_id` 指定的窗口不在会话中，或者没有创建者能够提供特点类型，失败并返回 `not_found`。不合法的 `bounds`，或格式错误的 `layout` 或 `flavor` 失败并返回 `bad_request`。

若省略 `window_id` 且会话没有任何窗口，调用失败并返回 `conflict`。

若调用会导致超过每个窗口的块数上限或服务端总块数上限，调用失败并返回 `conflict`。

### `session.new_split`

在现有块或拆分节点旁边的新拆分中创建块。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `anchor_id` |  | 要拆分其空间的块或拆分节点。块 ID 会拆分该单个块。拆分 ID 会将新块置于该拆分及其下方所有内容旁边。省略此项则拆分 window_id 的焦点块或活动窗口的焦点块。不要与 window_id 同时发送。 |
| `window_id` |  | 要拆分其焦点块的窗口。仅在省略 anchor_id 时发送。 |
| `direction` | 是 | 如何划分锚点空间：'horizontal' 代表左右并列，或 'vertical' 代表上下排列。 |
| `side` | 是 | 新块放置的位置：'before' 代表左侧或上方部分，或 'after' 代表右侧或下方部分。 |
| `ratio` |  | 前部所占空间的比例，大于 0 且小于 1。默认为 0.5。 |
| `layout` | 是 | 要在锚点旁创建的块及其排列方式。每个节点包含 block（带有特点类型以及可选的 options 和 label）或 split（带有 direction、before、after 和可选的 ratio）。 |
| `focus` |  | 是否将锚点所在窗口设为活动窗口并聚焦第一个新块。默认为 false。 |

服务端在新块启动前先选定要拆分的块，因此启动过程中的焦点变更不会改变拆分位置。

`layout` 中的 `block` 节点根据特点类型（`flavor`，如 `com.superlogical.terminal.shell`）启动一个新块。`split` 节点将其空间划分为两部分，并在 `before` 和 `after` 中各包含另一个节点。

在 `split` 节点中，`direction` 为 `horizontal` 时将 `before` 置于 `after` 左侧，为 `vertical` 时将其置于上方。`ratio` 是 `before` 所占空间的比例，大于 0 且小于 1。默认为 0.5。

无论是否设置 `focus`，窗口中的任何缩放状态均会结束。

若 `anchor_id` 是拆分 ID，新拆分会取代该拆分的位置。原有拆分及其下方所有内容位于一侧，`layout` 位于另一侧。以图层的顶层拆分为锚点会使新块跨越整个图层。仅包含一个块的图层没有拆分，因此请以其块为锚点。

先前已存在的拆分保留其 ID。

整个布局要么全部创建成功，要么完全不创建。若有任何块启动失败，服务端会关闭已启动的块，且调用失败。

若会话不存在，调用失败并返回 `session_not_found`。若 `window_id` 指定的窗口不在会话中，或者没有创建者能够提供特点类型，失败并返回 `not_found`。同时发送 `anchor_id` 与 `window_id`、不合法的 `ratio`，或格式错误的 `layout` 或 `flavor` 失败并返回 `bad_request`。

若 `anchor_id` 指定了不在窗口中的块（包括分离块）或不在任何窗口中的拆分，调用失败并返回 `not_found`。若同时省略 `anchor_id` 与 `window_id` 且会话没有任何窗口，失败并返回 `conflict`。

若调用会导致超过每个窗口的块数上限或服务端总块数上限，调用失败并返回 `conflict`。

### `session.new_window`

创建窗口及其平铺布局中的块。默认成为活动窗口。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `window_label` |  | 窗口的标签，最多 128 字符。省略此项则使用由窗口 ID 生成的标签（如 Window 89abcdef）。 |
| `layout` |  | 要在窗口中创建的块及其排列方式。必填。每个节点包含 block（带有特点类型以及可选的 options 和 label）或 split（带有 direction、before、after 和可选的 ratio）。 |
| `focus` |  | 是否将新窗口设为活动窗口。默认为 true。没有活动窗口的会话始终会将新窗口激活。 |

`layout` 中的 `block` 节点根据特点类型（`flavor`，如 `com.superlogical.terminal.shell`）启动一个新块。`split` 节点将其空间划分为两部分，并在 `before` 和 `after` 中各包含另一个节点。

在 `split` 节点中，`direction` 为 `horizontal` 时将 `before` 置于 `after` 左侧，为 `vertical` 时将其置于上方。`ratio` 是 `before` 所占空间的比例，大于 0 且小于 1。默认为 0.5。

`layout` 始终会启动新块。若要放置已存在的分离块，请使用 `session.move_block`。

在新窗口中，`block_ids` 中的第一个块获得焦点。

整个布局要么全部创建成功，要么完全不创建。若有任何块启动失败，服务端会关闭已启动的块，且调用失败。

若会话不存在，调用失败并返回 `session_not_found`。若缺少 `layout` 或其格式错误，或 `flavor` 格式错误，失败并返回 `bad_request`；若没有创建者能够提供特点类型，失败并返回 `not_found`。

若调用会导致超过每个会话的窗口数上限、每个窗口的块数上限或服务端总块数上限，调用失败并返回 `conflict`。

### `session.own_block`

为调用客户端声明块的所有权。结果列出每个块的所有者。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `block_ids` |  | 要声明拥有的块列表。省略或留空表示声明会话中的所有块。 |
| `mode` |  | 如何声明拥有：'take' 会立即让调用客户端成为所有者；'request' 仅使调用者成为当前无所有者块的所有者，并在其余块的所有者放弃或离开时可能获取它们。默认为 take。 |

当附加到会话的各客户端对块有不同要求时（如终端尺寸），块将遵循其所有者的设置。拥有块不赋予对其的其他额外权限。

调用客户端必须已通过 `session.attach` 或 `session.bootstrap` 附加到该会话。仅调用过 `session.attach_all` 的连接将失败并返回 `bad_request`。

任一模式都会将调用者加入该块的等待队列。当所有者放弃拥有权、断开附加或连接断开时，该块将传递给排队中最新声明拥有的已连接客户端，且任何 `take` 优先于所有 `request`。

连接断开的所有者在重新连接时会重新取回其每个块，除非在此期间块的所有者再次发生了改变。

`blocks` 列出调用后每个块的所有者，顺序与 `block_ids` 一致，重复的 ID 仅列出一次。当声明所有块时，按 `block_id` 排序。

每次所有者变更都会发送 `block_owner_changed`。若窗口中的块发生所有者变更，调用还会发送一条 `session_view_changed`，因为 `session.view` 展示了所有者。

除 `take` 或 `request` 以外的 `mode` 失败并返回 `bad_request`。

若 `block_ids` 中的任何 ID 不是会话中的块，调用失败并返回 `bad_request`，且不做任何更改。

### `session.raise_layer`

将浮动层前移至顶层，或移至另一个浮动层的正上方。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `layer_id` | 是 | 要前移的浮动层。 |
| `relative_layer_id` |  | 同一窗口中的另一个浮动层，将目标图层置于其正上方。省略此项则移至所有其他浮动层的前方。 |

`layer_id` 必须指定浮动层。指定窗口的平铺布局（`session.view` 中类型为 `tiled` 的图层）将导致调用失败并返回 `bad_request`。

若该图层已处于对应位置，调用不做任何更改。焦点和图层边界绝不改变。

若会话不存在，调用失败并返回 `session_not_found`。若 `layer_id` 未指定会话中的图层，失败并返回 `not_found`；若 `relative_layer_id` 与 `layer_id` 相同，失败并返回 `bad_request`。

若 `relative_layer_id` 指定了类型为 `tiled` 的图层或另一个窗口中的图层，调用失败并返回 `bad_request`。若其未指定会话中的图层，失败并返回 `not_found`。

### `session.resize_layer`

移动或调整浮动层的大小。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `layer_id` | 是 | 要移动或调整大小的浮动层。 |
| `bounds` | 是 | 图层的新位置与尺寸，表示为窗口宽度和高度的分数比例 [x, y, w, h]。必须完全容纳在窗口内。 |

`layer_id` 必须指定浮动层。指定窗口的平铺布局（`session.view` 中类型为 `tiled` 的图层）将导致调用失败并返回 `bad_request`。

`bounds` 从窗口左上角起算。其宽度和高度必须大于 0。

焦点和浮动层的堆叠顺序保持不变。设置图层当前已有的边界不做任何更改。

若会话不存在，调用失败并返回 `session_not_found`。若 `layer_id` 未指定会话中的图层，失败并返回 `not_found`；不合法的 `bounds` 失败并返回 `bad_request`。

### `session.resize_pane`

移动两个块之间的边界以改变其大小。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `direction` | 是 | 两个块之间的拆分类型：'horizontal' 代表左右之间的边界，或 'vertical' 代表上下之间的边界。 |
| `before_block_id` | 是 | 边界左侧的块，当 direction 为 vertical 时为边界上方的块。 |
| `after_block_id` | 是 | 边界右侧的块，当 direction 为 vertical 时为边界下方的块。 |
| `ratio` | 是 | 拆分空间中前部所占的比例，大于 0 且小于 1。 |

两个块选定其间的边界。服务端在 `direction` 方向上查找最内层的拆分，该拆分的左侧或上方包含 `before_block_id`，右侧或下方包含 `after_block_id`。这两个块无需直接相邻。

`ratio` 没有默认值。与 `session.new_split` 不同，0 不代表均等拆分。

这些块可以位于任何窗口中（无论活动与否）。焦点保持不变。

调用始终会递增 `revision` 并发送 `session_view_changed`，即使边界已处于你请求的位置也是如此。

若会话不存在，调用失败并返回 `session_not_found`。若两个块 ID 相同，或 `ratio` 超出范围，失败并返回 `bad_request`；若任一块不在任何窗口中，失败并返回 `not_found`。

若块位于不同窗口或图层中，或其间没有匹配的拆分，调用失败并返回 `bad_request`。

### `session.set_block_label`

设置块的标签。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `block_id` |  | 要重新标记的块。必填。 |
| `label` |  | 新标签，最多 128 字符。留空或省略会恢复由块 ID 生成的默认标签。 |

`block_id` 为必填项。省略将失败并返回 `bad_request`。

服务端去除 `label` 两端的空白字符。空的 `label` 会恢复由块 ID 生成的默认标签（如 `Block 89abcdef`），而非新块初始时携带的特点类型名称。

超过 128 字符或包含控制字符的标签失败并返回 `bad_request`。

为窗口中的块重新设置标签会发送 `session_view_changed`。分离块不是视图的一部分，因此为其重新设置标签不发送事件并保持 `revision` 不变。

若 `block_id` 指定的块不在会话中，调用失败并返回 `not_found`。

### `session.set_label`

设置会话的标签。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `label` |  | 新标签，最多 128 字符。留空或省略会恢复服务端创建会话时选择的标签。 |

服务端去除 `label` 两端的空白字符。空的 `label` 会恢复服务端创建会话时选择的标签（如 `quiet-meadow`）。即使会话创建时指定了标签，也会按此规则恢复。

超过 128 字符或包含控制字符的标签失败并返回 `bad_request`。

设置新标签会先发送 `session_label_changed`，然后发送 `session_view_changed`。设置为会话已有的标签不做任何更改。

### `session.set_layer_state`

最小化浮动层或将其恢复为正常状态，可选择同时提升并聚焦该图层。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `layer_id` | 是 | 要更改的图层。 |
| `state` | 是 | 要设置的状态：'normal' 或 'minimized'。 |
| `focus` |  | 是否在单次更改中同时提升图层、聚焦其先前聚焦的块并将所在窗口设为活动窗口。要求 state 为 'normal' 且图层中包含块。默认为 false。 |

只有浮动层可以被最小化。最小化窗口的平铺布局（`session.view` 中类型为 `tiled` 的图层）将失败并返回 `bad_request`。将其设置为 `normal` 会成功且不改变任何内容。

将 `focus` 设置为 `true` 时，图层也会被提升，其先前聚焦的块（或第一个块）获得焦点，且所在窗口变为活动窗口，所有这些在单次版本修订中完成。这同样适用于已处于正常状态的图层以及平铺图层。在 `minimized` 状态下使用 `focus`，或在没有块的图层上使用，将失败并返回 `bad_request` 且不改变任何内容。

`state` 必须为 `normal` 或 `minimized`。任何其他值失败并返回 `bad_request`。

最小化的图层保留在 `session.view` 中，其 `state` 设置为 `minimized`，其块继续运行，且保持其边界和在堆栈中的位置。对于正常图层，省略 `state`。

最小化当前拥有焦点的图层会将焦点转移到其先前使用的图层，或转移到最近的可见窗格，并清除缩放状态。将图层恢复正常会保持焦点位置不变。设置为图层已有的状态不做任何更改。

窗口必须保留至少一个可见窗格，因此最小化容纳窗口最后可见窗格的图层将失败并返回 `bad_request`。

若会话不存在，调用失败并返回 `session_not_found`。若 `layer_id` 未指定会话中的图层，调用失败并返回 `not_found`。

### `session.set_window_label`

设置窗口的标签。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `window_id` | 是 | 要重新标记的窗口。 |
| `label` |  | 新标签，最多 128 字符。留空或省略会恢复由窗口 ID 生成的默认标签。 |

服务端去除 `label` 两端的空白字符。空的 `label` 会恢复由窗口 ID 生成的默认标签（如 `Window 89abcdef`）。

超过 128 字符或包含控制字符的标签失败并返回 `bad_request`。

设置新标签会先发送 `window_label_changed`，然后发送 `session_view_changed`。设置为窗口已有的标签不做任何更改。

若 `window_id` 指定的窗口不在会话中，调用失败并返回 `not_found`。

### `session.swap_blocks`

交换两个块的位置。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `block_id` | 是 | 要交换的两个块之一。 |
| `other_block_id` | 是 | 另一个块。两者的先后顺序无关紧要。 |

两个块都必须位于窗口中。它们可以位于不同的窗口或图层中。

只有这两个块移动。拆分节点、其尺寸与 ID、浮动层以及窗口顺序均保持不变。

若其中一个块在活动窗口中拥有焦点，焦点会随其移动到新位置，且该位置所在的窗口变为活动窗口。

若会话不存在，调用失败并返回 `session_not_found`。若 `block_id` 与 `other_block_id` 相同，失败并返回 `bad_request`。若任一块不在任何窗口中（包括分离块），失败并返回 `not_found`。

### `session.view`

在单次快照中获取会话的窗口、其布局以及其中的块。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |

`revision` 从新会话的 0 开始，每次视图更改时递增 1。请仅在单个会话内比较版本号，并保留版本号最高的视图。

`session_view_changed` 事件仅携带新版本号，不携带视图本身。这些事件可能会乱序送达，因此仅在事件的版本号高于你所持有的视图版本号时调用 `session.view`。

对于同一次变更，`window_created`、`window_closed`、`window_label_changed`、`active_window_changed` 和 `session_label_changed` 均先于 `session_view_changed` 事件送达。

视图仅包含位于窗口中的块。`session.list_blocks` 还会列出分离块。

视图描述的是结构而非内容。若要读取块所展示的内容，请调用其自身的方法之一（如 `com.superlogical.terminal.format`）。

### `session.zoom_block`

将块缩放至填满其窗口，或撤销缩放。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `session_id` | 是 | 要操作的会话。 |
| `block_id` |  | 要缩放的块。它将获得焦点，其所在窗口成为活动窗口。省略此项则使用 window_id 的焦点块或活动窗口的焦点块。 |
| `window_id` |  | 要缩放其焦点块的窗口。活动窗口不变。仅在省略 block_id 时发送。 |
| `zoom` |  | 设置为 true 启用缩放，设置为 false 恢复布局。省略此项则在两者之间切换。 |

传入 `block_id` 时，服务端首先聚焦该块并使其窗口成为活动窗口（类似于 `session.focus_block`）。传入 `window_id` 时，焦点和活动窗口保持不变。

缩放仅改变展示效果。布局保持不变，当焦点移动到窗口中的另一个块时缩放状态结束。

若会话不存在，调用失败并返回 `session_not_found`。若 `block_id` 指定了不在任何窗口中的块，或 `window_id` 指定了不在会话中的窗口，失败并返回 `not_found`。两者同时发送失败并返回 `bad_request`。

若同时省略 `block_id` 与 `window_id` 且会话没有任何窗口，调用失败并返回 `conflict`。


## `target`

### `target.complete`

列出以前缀开头的标签、窗口位置和简短 ID。用于在用户键入名称时进行自动补全。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `kinds` | 是 | 要补全的目标类型：session、window、block 或 client，规则与 target.resolve 相同。补全项按此顺序返回。 |
| `prefix` | 是 | 目前键入的文本。它匹配标签的开头（忽略大小写）、窗口位置和简短 ID。空前缀匹配所有内容。 |
| `context` |  | 调用者所在上下文。仅使用 session_id：不指定 scope.session 时，窗口和块来自该会话。 |
| `scope` |  | 将补全限制在单个会话，或将块补全限制在单个窗口，规则与 target.resolve 相同。 |

`kinds`、`scope` 和 `context.session_id` 选择搜索范围的方式与 `target.resolve` 相同，且在相同情况下调用失败并返回 `bad_request`。

`prefix` 匹配标签的开头（忽略大小写），标签补全项保留标签自身的大小写。`prefix` 两侧的空白字符会被忽略。其中的控制字符（如制表符）会导致调用失败并返回 `bad_request`。

窗口还可以按位置匹配，因此前缀 `1` 会匹配窗口 1、10、11 等。空前缀匹配所有位置。

空前缀或仅由十六进制数字组成的前缀还会匹配简短 ID 的开头。简短 ID 是 ID 的最后六位十六进制数字（如 `12bef5`），`target.resolve` 将其作为 ID 的结尾部分接受。

同一个对象可能出现多次，例如标签和简短 ID 均以前缀开头的窗口。

补全项按类型分组，顺序与 `kinds` 一致。在每个类型中，标签优先排在最前（忽略大小写排序），然后按顺序排列窗口位置，最后按排序顺序列出简短 ID。

若 `scope.session` 或 `scope.window` 未匹配到任何内容或匹配到多个对象，`completions` 为空。调用不会失败。

除非设置了 `scope.window`，否则包含分离块。

若要补全客户端，将 `kinds` 设置为 `["client"]`。客户端按标签和简短 ID 进行补全，每个目标的 `where` 说明其程序信息（如 `Rex.app 1.6.0`）。

### `target.resolve`

按 ID、标签或位置查找会话、窗口、块或客户端。每个查询获得其自身的结果，说明其匹配到一个对象、无匹配还是匹配到多个对象。

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `kinds` | 是 | 每个查询可指定的名称类型：session、window、block 或 client。每种类型仅列出一次，且 client 仅能单独列出。 |
| `queries` | 是 | 要查询的名称列表。每个查询可以是一个完整 ID、标签、窗口位置、ID 结尾部分，或留空代表默认目标。 |
| `context` |  | 调用者所在上下文，如脚本运行所在的终端。其中不再存在的 ID 会被忽略。 |
| `scope` |  | 将搜索限制在单个会话，或将块搜索限制在单个窗口。当 kinds 包含 session 时不允许使用。 |

在 `kinds` 中至少列出一种类型，每种类型仅列出一次，且 `client` 仅能单独列出，否则调用失败并返回 `bad_request`。服务端未知的类型同样失败，这可能在服务端版本早于客户端时发生。

至少发送一个查询，否则调用失败并返回 `bad_request`。每个查询在 `results` 中按相同顺序获得一个条目。匹配不到任何内容或匹配到多个对象的查询不会导致整个调用失败：其 `status` 为 `not_found` 或 `ambiguous`。

服务端分四个步骤尝试每个查询，并在匹配到任何内容的第一步停止：完整 ID、标签（忽略大小写）、窗口位置，然后是 ID 结尾部分（4 到 32 个十六进制数字）。因此标签为 `2` 的窗口优先于第 2 个窗口。若胜出的步骤匹配到多个对象，结果为 `ambiguous`。

以完整 ID 开头的查询（如 `block:`）仅作为完整 ID 进行尝试。若 ID 格式错误、`kinds` 不包含该类型，或没有任何对象具有该 ID，其结果为 `not_found`。

只有窗口具有位置。`1` 是其会话中的第一个窗口（按 Rex.app 作为标签页显示的顺序）。当搜索多个会话时，一个位置可以匹配每个会话中的窗口。

当 `kinds` 列出多种类型时，一个查询可以匹配不同类型的对象（例如具有相同标签的会话和窗口）。此时结果为 `ambiguous`，且每个候选者的 `kind` 会指明其具体类型。

若未指定 `scope.session`，窗口和块仅在 `context.session_id` 指定的会话中搜索。若省略该字段或该会话已不存在，则搜索每个会话。这同样适用于完整 ID，因此位于另一个会话中的块的完整 ID 结果为 `not_found`。

若作用域未匹配到任何内容或匹配到多个对象，每个结果都会获得该 `not_found` 或 `ambiguous` 状态，且其 `reason` 说明是哪个作用域失败。对于多义性歧义作用域，`candidates` 列出该作用域可能指代的目标。

空查询或仅包含空格的查询请求默认目标（如脚本运行所在的块）。当 `kinds` 列出多种类型时，空查询获取最具体类型的默认目标：先是 block，然后是 window，再是 session。

空的会话查询选择 `context.session_id`，或者在仅有一个会话时选择该唯一会话。在没有会话时为 `not_found`，在有多个会话时为 `ambiguous`。

空的窗口查询选择包含 `context.block_id` 的窗口，或者正在搜索会话的活动窗口。若搜索多个会话，即使设置了 `context.block_id` 也是 `ambiguous`，`candidates` 列出可供选择的会话。

若包含被搜索块中存在 `context.block_id`，空的块查询选择 `context.block_id`。否则它选择空窗口查询所选择窗口的焦点块。使用 `scope.window` 时，它忽略 `context.block_id` 并选择该窗口的焦点块。

块搜索包含分离块（正在运行但未放置在任何窗口中的块）。`scope.window` 将其排除。块的 `where` 显示为 `window 2` 或 `detached`。当搜索多个会话时，它还会指明会话名称（如 `window 2 of work`），窗口的 `where` 显示为 `in work`。

若要查找已连接的客户端（如 Rex.app），将 `kinds` 设置为 `["client"]`。客户端查询匹配完整 ID、标签或 ID 结尾，因为客户端没有位置属性。每个已连接的客户端均在搜索范围内，除非 `scope.session` 将搜索限制为附加到该会话的客户端。

空的客户端查询在包含被搜索客户端中存在 `context.client_id` 时选择该客户端。否则它选择连接时将其类型报告为 `app` 的唯一客户端（如 Rex.app）。在没有 app 时为 `not_found`，在有多个 app 时为 `ambiguous`。

`scope.window` 在正在搜索的会话中查找。若 `kinds` 包含 `session` 且发送了 `scope`（即使为空对象），或者设置了 `scope.window` 且 `kinds` 不仅为 `block`，调用失败并返回 `bad_request`。包含控制字符（如换行符）的查询或作用域同样失败。
