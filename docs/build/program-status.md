> 原文：https://www.superlogical.com/rex/docs/build/program-status
> 原文版本：9b3f32f6e539（抓取于 2026-11-13）

# 程序状态协议（OSC 7501）

一种终端转义序列，允许程序告知终端自身当前的状态：空闲、正在工作、等待用户交互、已完成或失败，以及对应原因。

该协议仅共享状态，将呈现方式留给终端决定。它不规定任何展示样式，并避免使用与特定 GUI 元素绑定的术语（如“通知”、“注意力”、“焦点”等）。

```
# Terraform 已完成规划，正在等待用户批准应用变更。
# 该消息解码后为 "Apply 3 to add, 1 to change, 0 to destroy?"。
ESC ] 7501 ; state=blocked:kind=permission:app=terraform:msg=QXBwbHkgMyB0byBhZGQsIDEgdG8gY2hhbmdlLCAwIHRvIGRlc3Ryb3k/ ESC \
```

**说明：**这是一项通用终端协议。虽然它在 Rex 中用于实现丰富的功能，但协议本身不包含任何针对 Superlogical 的专有功能或特定术语。它填补了终端应用领域的普遍需求。

## 设计动机

长时间运行的任务在终端中十分常见：编译构建、服务部署、软件包升级、数据处理以及代码生成智能体。此类程序通常在自主工作、等待用户交互和完成之间交替运行。在此期间，用户通常在处理其他事情，并希望在工作完成或需要用户介入时及时获知。

现有的控制序列仅覆盖了其中的局部片段。OSC 9;4 进度报告可以表示忙碌或非忙碌，但无法表明程序正在等待用户或正在处理什么。桌面通知是一次性事件，仅包含自由格式的文本。同时展示多个程序的工具只能回退到启发式规则（例如解析窗口标题或匹配屏幕内容），或者依赖针对特定程序的插件。[与其他控制序列的关系](#与其他控制序列的关系)一节对此进行了详细探讨。

借助该协议，清楚自身状态的程序能够直接汇报该状态，而终端则能保留其内部运行的每个程序的最新视图。

## 在 Rex 中的应用

当程序在 Rex 中采用程序状态协议时，目前会以多种方式呈现当前活跃状态：

- 包含已完成或被阻塞任务的会话会在会话选择器中带有指示标识。
- 未获得焦点的标签页标头会显示正在进行中的转轮指示器，并为阻塞状态显示各类符号。
- Lua 脚本可以响应 `terminal.program_status_changed` [事件](../automate/lua-events.md)。

未来，计划在更多方面扩展此功能，例如向移动客户端推送通知、统一的高优先级收件箱视图等。

## 约定

关键字 MUST（必须）、MUST NOT（绝不能）、SHOULD（应当）和 MAY（可以）按 RFC 2119 和 RFC 8174 中的说明使用，且仅在其以全大写形式出现时生效。

| 名称 | 字节 |
| --- | --- |
| `ESC` | `0x1B` |
| `OSC` | `ESC ]`，即 `0x1B 0x5D` |
| `ST` | `ESC \`（即 `0x1B 0x5C`）或 `BEL`（即 `0x07`） |

**终端（Terminal）**是指挂接至单个伪终端（pseudo-terminal）的一个窗口、标签页、分屏或窗格。文中提及“终端”的规则均独立适用于每一个终端实例，并由模拟它的程序实现。**程序（Program）**向终端写入数据。**报告（Report）**是程序发送的一个控制序列。**记录（Record）**是终端最终存储的内容。

## 语法

```
OSC 7501 ; pairs ST        report
OSC 7501 ; ? ST            feature detection

pairs    := pair (":" pair)*
pair     := key "=" value
key      := [a-z]+
value    := [A-Za-z0-9_.,+/=-]*
```

- 主体是由 `:` 分隔且无其他多余字符的 `key=value` 键值对列表。值的字符集排除了 `:` 和 `;`，因此不需要任何转义。键和值周围的空白字符会被自动去除。
- 格式错误的键值对（缺少 `=`、键为空、或包含取值字符集以外的字节）会被跳过，报告的其余部分仍继续处理。
- 终端 MUST 忽略未知键。协议通过该机制进行后续扩展。
- 如果键重复出现，以最后一个值为准。
- 自由文本值（`msg`、`title`）为 UTF-8 文本的标准 Base64 编码。填充字符可有可无。解码后的文本 MUST NOT 包含控制字符（`U+0000`–`U+001F`、`U+007F`、`U+0080`–`U+009F`），包括换行符或制表符。这些值专用于单行文本。
- 如果报告超过任何一项[限制](#限制)、Base64 无法解码、或解码后的文本包含控制字符，该报告将被整条丢弃。被丢弃的报告中的任何内容均不生效。

## 记录与 ID

终端维护着**一组记录**，每个 ID 对应一条记录。每条记录严格保存最后一条使用该 ID 的报告中所包含的键。

```
id      := segment ("/" segment)*
segment := [A-Za-z0-9_.+-]{1,32}
```

- 没有 `id` 的报告作用于**根记录（Root record）**。仅汇报自身状态的程序只需使用根记录，可跳过本节的其余内容。
- **每条报告会完全替换其对应的记录。** 报告中缺失的键在替换后的记录中也将不复存在。希望在记录中保留 `app` 或 `title` 的程序必须在每次报告中都包含它们。
- `id` 不匹配上述语法的报告会被直接忽略。若回退到根记录，会导致格式错误的 ID 意外覆盖根记录。
- `/` 为记录赋予父子层级关系：`build/test` 是 `build` 的子记录，`build` 则是根记录的子记录。父记录无需预先存在。终端 MUST 将此关系用于清除记录（参见[状态](#状态)）和 `app` 继承（参见[键](#键)），且 MAY 将其用于记录分组。该层级关系不具备其他含义。
- 根记录与子记录可以同时存在。程序可以在其提示符处保持 `idle`，而其下的某个工作进程处于 `blocked` 状态。
- 记录归属于终端，而非归属于屏幕。在主屏幕与备用屏幕之间切换不会对记录产生任何影响。完全重置（`RIS`）会移除所有记录，而软重置（`DECSTR`）则不会。

## 状态

`state` 键为必填项。缺少 `state` 或包含终端无法识别的状态的报告会被忽略。

| `state` | 含义 | 生命周期 |
| --- | --- | --- |
| `idle` | 处于静止状态，等待用户的下一步指令。 | 直到被替换或清除。 |
| `working` | 正在运行。可携带 `progress`。 | 直到被替换、被清除、进程退出或出现下一个 Shell 提示符。 |
| `done` | 完成了一项工作。结果已就绪供查阅，用户尚未查看。 | 直到被替换或清除。在进程退出和 Shell 提示符之后仍然保留。 |
| `blocked` | 无法继续进行，直到用户执行某些操作。`kind` 说明类型，`msg` 说明原因。可携带 `progress`。 | 与 `working` 相同。 |
| `error` | 执行失败并已停止。 | 与 `done` 相同。 |
| `clear` | 非真实状态。用于移除指定记录及其之下的所有子记录。若不带 `id`，则移除终端上的所有记录。 | |

当用户中断或取消程序时，汇报 `idle`。在完成任务后立即退出的程序 SHOULD 在退出前汇报 `done` 或 `error`，以便为用户保留可供查阅的记录。

**生命周期。** 记录与终端已观测到的事件绑定。协议不设置心跳机制，且终端 MUST NOT 要求程序重复发送以保持记录存活。当挂接到终端的进程退出，或者新的 Shell 提示符开始时（OSC 133 `A`），终端 MUST 丢弃 `working` 和 `blocked` 记录，且 MAY 丢弃 `idle` 记录。`done` 和 `error` 在这两类事件发生后均会继续保留。终端自行决定何时停止展示它们，例如当用户返回终端并按下按键时。

## 键

| 键 | 取值 | 说明 |
| --- | --- | --- |
| `state` | `idle` \| `working` \| `done` \| `blocked` \| `error` \| `clear` | 必填。无法识别的值会导致整条报告被忽略，因此后续新增的状态绝不会在旧版终端上被误当作 `idle`。 |
| `id` | 路径，参见[记录与 ID](#记录与-id) | 缺失即表示根记录。 |
| `kind` | `permission` \| `question` \| `auth` | 仅在 `blocked` 状态下有效，其他情况下被忽略。`permission`：执行某项操作需要批准。`question`：用户必须输入回答。`auth`：需要登录、Token 或凭证。无法识别的值被视作缺失。 |
| `progress` | 整数 `0` 至 `100` | 仅在 `working` 或 `blocked` 状态下有效，其他情况下被忽略。缺失表示不确定进度：程序忙碌但没有具体的百分比可汇报。其他任何值均视作缺失。 |
| `app` | `[A-Za-z0-9_.+-]{1,32}` | 程序的稳定标识符，例如 `cargo`、`terraform` 或 `claude-code`。用于分组、过滤、图标关联等。这不是标签；`title` 才是标签。没有 `app` 的记录会从其最近的具备该属性的祖先记录中继承。超出字符集的值视作缺失。 |
| `title` | Base64 编码的 UTF-8 | 记录的简短人类可读标签。适用于汇报多条记录的程序。根记录的标签通常为窗口标题。 |
| `msg` | Base64 编码的 UTF-8 | 单行人类可读文本：记录正在执行、正在等待或已完成的内容。终端 MAY 将其截短，且 MUST NOT 解析其中的语义。 |

## 特性检测

```
program  → OSC 7501 ; ? ST
terminal → OSC 7501 ; ? : states=idle,working,done,blocked,error : kinds=permission,question,auth ST
```

特性检测是可选的。终端 MUST 忽略未知的 OSC 序列，因此程序 MAY 在不预先查询的情况下直接发送报告，例如在无法读取响应的场景下。

支持该特性的终端 MUST 回复 `?`。终端 MAY 在回复中添加 `states`（其接受的以逗号分隔的 `state` 取值，不含 `clear`）以及 `kinds`（其接受的 `kind` 取值）。

不带 `states` 的回复严格等同于 `idle`、`working`、`done`、`blocked` 和 `error`。不带 `kinds` 的回复严格等同于 `permission`、`question` 和 `auth`。这些列表是固定的，后续修订版中不会更改既有含义。新增状态与类型的方式如下：需要使用后续修订版中状态的程序先检查该列表，并回退到当前支持的状态。程序 MUST 忽略回复中自身无法理解的键值对。

在自行设定的时间内未收到回复的程序，将协议视作不受支持。为避免不必要的等待，可在查询后立即发送首要设备属性（`CSI c`）。所有终端都会对此进行应答，因此如果设备属性的应答先到达，即表明该协议不受支持。

## 安全性

报告中的所有内容均属于不可信输入，来源是已经控制屏幕的程序。

- 终端 MUST 拒绝解码后的 `msg` 或 `title` 包含控制字符的报告，MUST NOT 将其视为标记语言（markup），且在终端网格外部展示时 SHOULD 消除文本方向覆盖（bidi override）及其他不可见格式字符的影响。
- 终端回写的唯一字节是特性检测的回复，其中不包含来自任何报告的内容。ID、标题和消息绝不会被回写，且协议不提供读取记录的方法。
- 终端展示记录中的任何内容时 SHOULD 标明其来源于哪个终端，以防止程序伪装成其他终端中的程序。
- 程序可以以其最快的写入速度更改状态。终端 SHOULD 对记录在终端外部引起的任何动作（例如桌面通知或提示音）进行限流。

## 限制

每项限制均为终端针对单个报告所需存储或处理的硬性上限，以防止恶意或异常程序导致内存无限增长或引发无休止的工作负载。终端 MAY 自行设定更低的上限。超出限制的报告将被整条丢弃。在修改任何已存储记录之前，先检查所有键值对。

| 项目 | 限制 |
| --- | --- |
| 完整序列（从 `OSC` 到 `ST`） | 4096 字节。最大合法报告在 3300 字节以下。 |
| 键长度 | 16 字节 |
| `msg` | 编码后 2732 字节，解码后 2048 字节。在解码前先检查编码后的大小。 |
| `title` | 编码后 256 字节，解码后 192 字节 |
| `app` | 32 字节 |
| `id` | 总长 128 字节，每段 32 字节，最多 8 层深度 |
| 每个终端的记录数 | 256 条。终端 MUST 至少支持 64 条。当新报告创建的记录超出上限时，最久未更新的记录将被移除以腾出空间。 |

## 与其他控制序列的关系

**[OSC 9;4](https://conemu.github.io/en/AnsiEscapeCodes.html#ConEmu_specific_OSC)（进度）。**
仅能表达忙碌、百分比或错误。它无法说明程序正在等待用户或需要什么，也不携带任何消息或程序身份标识。它还与 iTerm2 的通知控制序列共用了编号 9，这在仅了解两者之一的终端中曾导致输出乱码。程序可以同时发送两者。终端 MAY 将 OSC 9;4 映射到本协议的根记录。由于每次报告都会完整替换其记录，映射的 OSC 9;4 会抹去真实报告中的 `kind` 和 `msg`。终端在接收到 OSC 7501 报告后，SHOULD 停止映射 OSC 9;4，直到下一次完全重置。

**OSC 9、[OSC 99](https://sw.kovidgoyal.net/kitty/desktop-notifications/)、OSC 777（桌面通知）。**
通知是一次性事件。一旦展示之后，终端不再保留当前真实状态的记录，因此无法得知程序是否仍在等待或者已经恢复。通知还意味着对用户的打扰，这并不总是恰当的行为。终端 MAY 在记录发生变化时生成通知。

**[OSC 133](https://gitlab.freedesktop.org/Per_Bothner/specifications/blob/master/proposals/semantic-prompts.md)（Shell 集成）。**
标记提示符和命令的起始与结束位置。它由 Shell 发出，而非由程序本身发出，因此它只能表明命令正在运行或已带退出码结束，绝无法说明程序正在做什么或是否陷入阻塞。

**OSC 0 和 2（窗口标题）。**
单一的自由格式字符串，缺乏结构化信息。目前需要展示状态的程序往往在其中塞入特殊字符和转轮动画，但这并不是一种可靠的机器可读进度格式。

**[OSC 21337](https://iterm2.com/documentation-session-status.html)（iTerm2 会话状态）和 OSC 9999 (Orca)。**
针对同一概念的早期尝试。它们规定了具体的呈现方式（包含颜色和指示器），或者需要解析 JSON，总体而言未能契合最核心的设计目标。

## 示例

Base64 编码的值在末尾注释中给出了解码后的内容。

### 单个程序

```
OSC 7501 ; state=working:app=brew:msg=SW5zdGFsbGluZyB1cGRhdGVz ST                              # 正在安装更新
OSC 7501 ; state=blocked:kind=auth:app=brew:msg=UGFzc3dvcmQgcmVxdWlyZWQgdG8gaW5zdGFsbCB1cGRhdGVz ST  # 安装更新需要密码
OSC 7501 ; state=working:app=brew:msg=SW5zdGFsbGluZyB1cGRhdGVz ST                              # 正在安装更新
OSC 7501 ; state=done:app=brew:msg=VXBncmFkZWQgMTIgcGFja2FnZXM= ST                             # 已升级 12 个软件包
```

每条报告都重复包含 `app`，因为报告会完整替换其记录。`done` 记录在随后的 Shell 提示符出现后依然保留。

### 多条记录

```
OSC 7501 ; state=working:app=deploy:msg=RGVwbG95aW5nIHYyLjQuMQ== ST                                               # 正在部署 v2.4.1
OSC 7501 ; state=working:id=us-east:title=VVMgRWFzdA==:progress=40:msg=UHVzaGluZyBpbWFnZQ== ST                    # 美国东部 / 正在推送镜像
OSC 7501 ; state=blocked:kind=permission:id=eu-west:title=RVUgV2VzdA==:msg=QXBwcm92ZSBkZXBsb3kgdG8gZXUtd2VzdCAocHJvZHVjdGlvbik/ ST  # 欧洲西部 / 批准部署至 eu-west (production)？
OSC 7501 ; state=done:id=us-east:title=VVMgRWFzdA==:msg=SGVhbHRoeQ== ST                                           # 美国东部 / 健康
OSC 7501 ; state=clear:id=us-east ST
OSC 7501 ; state=clear:id=eu-west ST
OSC 7501 ; state=done:app=deploy:msg=RGVwbG95ZWQgdG8gMyByZWdpb25z ST                                              # 已部署至 3 个区域
```

区域记录在展示时会从根记录中继承 `app=deploy`。当 `eu-west` 处于阻塞时，根记录仍显示 `working`。两者同时成立，终端自行决定展示哪一个。

### Shell 函数

```sh
status() {
  printf '\e]7501;state=%s:msg=%s\e\\' "$1" "$(printf '%s' "$2" | base64 | tr -d '\n')"
}
status working "Syncing photos"
rsync -a ~/Photos backup:/photos && status done "Photos synced" || status error "rsync failed"
```

## 修订历史

| 日期 | 修订版本 | 变更说明 |
| --- | --- | --- |
| 2026-10-10 | 0.4 | 特性检测回复可列出支持的状态与类型。说明拒绝控制字符的原因以及 `app` 的作用。移除 terminfo。 |
| 2026-10-07 | 0.3 | 缺失 `progress` 表示不确定进度。程序可在不进行特性检测的情况下直接发送报告。 |
| 2026-10-06 | 0.2 | 阐明 MUST NOT，并在更多位置应用规范关键字。 |
| 2026-09-28 | 0.1 | 初始草案。 |
