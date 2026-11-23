---
title: "Custom UI"
canonical_url: https://www.superlogical.com/rex/docs/customize/custom-ui
---

# Custom UI

A [custom action](https://www.superlogical.com/rex/docs/customize/actions.md) can stop partway, ask the person a
question in the command palette, and carry on with the answer.
`rex.ui.input` asks for a line of text, and `rex.ui.pick` shows a list to
choose from.

```lua
rex.action{
  name  = "new_branch",
  title = "Git: New Branch…",
  run   = function(ctx, args)
    local name, why = rex.ui.input{
      title       = "New branch",
      placeholder = "feature/…",
      value       = "feature/",
      confirm     = "Create branch",
    }
    if name == nil then return end

    -- Type the command at the focused terminal's prompt.
    rex.block.call("com.superlogical.terminal", "write", {
      data = "git switch -c " .. name .. "\r",
    })
  end,
}

rex.bind("alt+cmd+b", "new_branch")
```


Run `rex config reload`, then press <kbd>Option</kbd>+<kbd>Cmd</kbd>+<kbd>B</kbd>.
The command palette opens with a text field titled "New branch". Press
<kbd>Return</kbd> and the action continues with what you typed.

The action waits for the answer without holding anything else up. Keys,
other actions, and events keep working while the question is open, and the
time the person takes doesn't count toward the action's time limit.

## Asking for Text

`rex.ui.input` takes a table and returns the text the person submitted:

```lua
local name, why = rex.ui.input{ title = "Your name" }
```


| Field | Description |
| --- | --- |
| `title` | Names the question. Required. |
| `placeholder` | The hint shown while the field is empty. |
| `value` | The text the field starts with, for the person to edit. |
| `confirm` | The label of the row that submits. Without it, the row reads `Use "…"` with the typed text. |
| `timeout` | How many seconds to wait for an answer. Defaults to 300, and is at most 3600. |

The text comes back exactly as typed, including any spaces around it. It may
be empty, because a person can submit an empty field.

## Asking for a Choice

`rex.ui.pick` shows a list and returns the `id` of the item the person chose.
It takes the same fields as `rex.ui.input`, where `placeholder` and `value`
apply to the field that filters the list, plus `items`:

```lua
local dir, why = rex.ui.pick{
  title       = "Open project",
  placeholder = "Filter projects",
  items = {
    { id = "/Users/me/Apps/rex", title = "rex",
      subtitle = "~/Apps/rex", icon = "folder" },
    { id = "/Users/me/Apps/rex-app", title = "rex-app",
      subtitle = "~/Apps/rex-app", icon = "folder" },
  },
}
if dir == nil then return end

rex.session.new_window{
  layout = rex.layout.block{
    flavor  = "com.superlogical.terminal.shell",
    options = { cwd = dir },
  },
}
```


`items` is a list, in the order to show it, of at most 2,000 items. It may be
empty. Each item is a table:

| Field | Description |
| --- | --- |
| `id` | What `rex.ui.pick` returns for the item. Required, and unique within the list. |
| `title` | The item's main text. Defaults to `id`. |
| `subtitle` | A second, quieter line. |
| `icon` | One of the icon names below. |
| `detail` | Short text at the far end of the row, such as a file's status. |
| `selected` | Set to `true` to start the item ticked. Only with `multiple`. |

An item can also be a plain string, which is short for an item whose `id` and
`title` are both that string:

```lua
rex.ui.pick{ title = "Pick a fruit", items = { "Apple", "Banana", "Cherry" } }
```

### Icons

`icon` is one of these names. Each Rex app draws them in its own style.

`document`, `folder`, `branch`, `terminal`, `code`, `server`, `database`,
`package`, `globe`, `link`, `person`, `tag`, `clock`, `star`, `gear`, `plus`

Any other name is ignored with a warning, and the item has no icon.

### Choosing Several Items

With `multiple = true`, the person can tick any number of items, and the
result is a list of ids in the order of `items`. It's an empty list if they
confirmed with nothing ticked. The palette shows how many are ticked next to
the `confirm` label, and <kbd>Cmd</kbd>+<kbd>Return</kbd> confirms.

```lua
local files = rex.ui.pick{
  title       = "Stage files",
  placeholder = "Filter changed files",
  multiple    = true,
  confirm     = "Stage",
  items = {
    { id = "README.md", icon = "document", detail = "??", selected = true },
    { id = "docs/notes.md", title = "notes.md", subtitle = "docs",
      icon = "document", detail = "??" },
  },
}
-- files is a list such as { "README.md", "docs/notes.md" }
```


### Accepting Typed Text

With `allow_other = true`, the person can answer with what they typed in
the field instead of choosing an item. The result is then the table
`{ text = "..." }`, so it can't be mistaken for an id. `allow_other` can't be
combined with `multiple`.

```lua
local fruit = rex.ui.pick{
  title       = "Favourite fruit",
  items       = { "Apple", "Banana", "Cherry" },
  allow_other = true,
}
if type(fruit) == "table" then fruit = fruit.text end
```

## When There Is No Answer

When there's no answer, both functions return `nil`, a reason, and sometimes
a detail:

```lua
local name, why, detail = rex.ui.input{ title = "New branch" }
if name == nil then
  if why == "cancelled" then return end
  rex.log("warn", "new_branch: " .. why .. " " .. (detail or ""))
  return
end
```

The reason is always one of these words:

| Reason | Meaning |
| --- | --- |
| `cancelled` | The person closed the prompt without answering. |
| `timeout` | Nobody answered within the timeout. |
| `no_client` | No Rex app was connected, or every app showing the prompt lost its connection. |
| `unsupported` | No connected app can show prompts, usually because they're older than the server. |
| `busy` | Every app that could show the prompt is already showing another one. |
| `failed` | Anything else. `detail` is a sentence that says what. |

`detail` is `nil` for every reason except `failed`. Its wording can change
between versions of Rex, so check the reason, not the detail.

A mistake in the call itself, such as a missing `title` or two items with
the same `id`, raises an error instead.

## Which Apps Are Asked

Every Rex app connected to the server is asked, including on your other
devices, as long as it's new enough to show prompts and isn't already
showing one. The first answer wins, and the prompt closes on the other apps.
Cancelling on any one of them cancels it everywhere.

This is the same when the action is run with `rex do`: the question appears
in the connected apps, and `rex do` waits until someone answers. Use
`--timeout` to limit how long it waits. See [`rex do`](https://www.superlogical.com/rex/docs/reference/cli.md).

## Where You Can Ask

A prompt pauses the action that asked, so it only works where Rex can pause:
inside an action's `run` function, and functions it calls directly. It
doesn't work in:

- a function bound directly to a key, as in `rex.bind(key, function() ... end)`
- a handler registered with [`rex.on`](https://www.superlogical.com/rex/docs/automate/lua-events.md)
- the top level of the configuration file
- a function called through `pcall` or `xpcall`
- an action run by `rex.invoke`
- a function that a library calls, such as a `table.sort` comparator

There, both functions return `nil` and `failed` without asking anyone, and
the log gets a warning. To ask from a key, define an action and bind the key
to its name.

## Running Without a Person

An action can take the answer as an argument and only ask when it's missing.
Then a script or a CI job can run it with nobody there to answer:

```lua
rex.action{
  name  = "greet",
  title = "Greet",
  args  = { name = "string?" },
  run   = function(ctx, args)
    local name = args.name or rex.ui.input{ title = "Your name" }
    if name == nil then return end
    rex.log("info", "Hello, " .. name)
  end,
}
```

```sh
rex do greet name=Ada
```

## Server API

Apps receive a prompt as the `client_prompt_requested` event and answer it
with `client.reply`. Apps that were asked but didn't answer get
`client_prompt_ended` when the prompt closes. Prompts need control API
revision 17. See [Server API Methods](https://www.superlogical.com/rex/docs/reference/api.md).
