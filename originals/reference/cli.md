---
title: "CLI Commands"
canonical_url: https://www.superlogical.com/rex/docs/reference/cli
---

# CLI Commands

This page lists every public `rex` command and flag. See [The CLI](https://www.superlogical.com/rex/docs/automate/cli.md) for how to use them. Anything tagged [Snapshot](https://www.superlogical.com/rex/docs/linux/installation.md#channels) is on the snapshot channel and not yet in preview.

<div class="reference-page commands" hidden></div>

## Common Commands

### `rex new [LABEL] [-- COMMAND...]`

Create a session.

| Flag | Description |
| --- | --- |
| `-c, --cwd string` | Working directory for the terminal. |
| `--keep-open` | Keep the terminal open after its command exits. |
| `--shell SHELL` | Run COMMAND through SHELL's login environment (none starts it directly). |
| `--interactive` | Also read the shell's interactive startup files, such as ~/.zshrc. |
| `--window string` | Label for the first window. |
| `--json` | Output the created session as JSON. |

### `rex ls`

List sessions.

| Flag | Description |
| --- | --- |
| `--json` | Output sessions as JSON. |
| `-q, --quiet` | Print IDs only, one per line. |
| `--short` | Show short IDs (`--short=false` shows full IDs). Defaults to `true`. |

### `rex run [flags] -- COMMAND...`

Run a command in a new block.

Run a command in a new terminal block.

COMMAND runs through your login shell's environment but not its interactive configuration, so profile variables and PATH apply and aliases do not. Use `--interactive` to read that configuration too, such as ~/.zshrc, for a program whose directory is added to PATH there. Use `--shell` to pick another shell, or `--shell=none` to start COMMAND directly.

By default, Rex places the block in a new window. Use `--split` to place it beside an existing block. Use `--focus=false` to preserve the active window. With `--wait`, Rex writes the creation result, then waits and returns the terminal child's exit status.

| Flag | Description |
| --- | --- |
| `--split DIRECTION` | Place the new block in DIRECTION relative to the anchor (right, left, above, or below). |
| `--ratio PCT` | Give the new block PCT percent of the split. Defaults to `50`. |
| `-b, --block BLOCK` | Use BLOCK as the split anchor (defaults to focused). |
| `-s, --session string` | Scope to session SESSION. |
| `-w, --window string` | Scope to window WINDOW. |
| `-c, --cwd string` | Working directory for the terminal. |
| `--keep-open` | Keep the terminal open after its command exits. |
| `--shell SHELL` | Run COMMAND through SHELL's login environment (none starts it directly). |
| `--interactive` | Also read the shell's interactive startup files, such as ~/.zshrc. |
| `--label TEXT` | Set the new block label to TEXT. |
| `--focus` | Focus the new block. Defaults to `true`. |
| `--json` | Output the creation result as JSON. |
| `--wait` | Wait and return the terminal child's exit status. |

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

Split the focused block.

Create a terminal block for a shell or command.

A COMMAND runs through your login shell's environment but not its interactive configuration. Use `--interactive` to read that configuration too, `--shell` to pick another shell, or `--shell=none` to start COMMAND directly.

By default, Rex splits the focused block and places the new block on its right. Use `-b` BLOCK to select another anchor or `--split` to choose another direction. Use `--focus=false` to preserve the current focus. With `--wait`, Rex writes the creation result, then waits and returns the terminal child's exit status. Use `rex run` to place the block in a new window.

| Flag | Description |
| --- | --- |
| `--split DIRECTION` | Place the new block in DIRECTION relative to the anchor (right, left, above, or below). Defaults to `right`. |
| `--ratio PCT` | Give the new block PCT percent of the split. Defaults to `50`. |
| `-b, --block BLOCK` | Use BLOCK as the split anchor (defaults to focused). |
| `-s, --session string` | Scope to session SESSION. |
| `-w, --window string` | Scope to window WINDOW. |
| `-c, --cwd string` | Working directory for the terminal. |
| `--keep-open` | Keep the terminal open after its command exits. |
| `--shell SHELL` | Run COMMAND through SHELL's login environment (none starts it directly). |
| `--interactive` | Also read the shell's interactive startup files, such as ~/.zshrc. |
| `--label TEXT` | Set the new block label to TEXT. |
| `--focus` | Focus the new block. Defaults to `true`. |
| `--json` | Output the creation result as JSON. |
| `--wait` | Wait and return the terminal child's exit status. |

```sh
rex split
rex split --split=below
rex split -b editor --split=left -- lazygit
rex split --wait -- make
rex split -- htop
```

### `rex do (ACTION | SCRIPT | -e CODE) [KEY=VALUE...]`

Perform an action or run a Lua script.

Perform an action by name, or run a Lua script.

A name without a dot is an action init.lua defines with rex.action. A name that starts with a client prefix, such as pane.split, is performed by the targeted client. A name that starts with a block type's creator name, such as com.superlogical.terminal.reset, is a block action or method. Run "rex actions" to list them.

An action from init.lua can ask a question with rex.ui.input or rex.ui.pick. `rex do` can't show the question itself, so every connected Rex app shows it, and `rex do` waits for someone to answer it on one of them. By default, `rex do` waits until the action finishes, however long that takes. Use `--timeout` to limit the wait. When the limit passes, `rex do` stops the action and exits with status 1.

To run a Lua script instead, give its path. The first argument is a script path when it contains a slash (or a backslash on Windows) or ends in .lua. Use - to read the script from stdin, or `-e` to give it on the command line. A script can call the same API as init.lua. Its return value prints the same way as an action's result. In a script, rex.invoke runs the actions the script defines and asks the server to run any others.

A script can also call the hosts that "rex hosts" lists. rex.servers() returns their labels, and rex.server(LABEL) returns the same API helpers as rex, with calls going to that host. `rex do` connects to a host on the script's first call to it, and stays connected until the script ends. `--server` chooses only the server that rex itself calls.

With `--action` NAME, `rex do` runs the script, then runs the action the script defines as NAME and prints that action's result. Pairs are typed against that action's schema. Use this to try an action in init.lua before the server reloads it.

A script that registers rex.on handlers keeps running after its last line, and runs its handlers as events arrive, one at a time. It hears the session that `-s`, `-b`, or the environment names, or every session if none is named. `--all` makes it hear every session, including ones created later. While it runs, rex.session.attach and rex.session.detach change what it hears.

Such a script runs until it calls rex.stop(CODE), and `rex do` exits with CODE, or 0 if it is left out. The script also stops, with status 0, when `--for` DURATION has passed, or when the last session it hears is destroyed, unless it hears every session. Ctrl-C stops it with status 130. A failed handler is reported and the script keeps going. With `--fail-fast`, the first failure exits with status 1.

Any script can pause. rex.sleep(SECONDS) waits for time to pass, and rex.wait(EVENT, FILTER, TIMEOUT) waits for an event, such as the exit of a command the script started. Nothing else in the script runs meanwhile. `--for` does not interrupt a pause at the top level of the script.

Arguments are KEY=VALUE pairs typed against the action's schema. Use `--args` to pass a JSON object instead, or @FILE to read one, or - for stdin. A script reads its arguments from rex.args. Scripts have no schema, so each value's type comes from how it is written: n=2 is a number and name=x is a string.

Pass large arguments, such as a long list of items, with @FILE or -. Linux can refuse a single command-line argument longer than 128 KiB. A Rex server accepts a request of up to 1 MiB, arguments included.

A client action needs a client. Use `-C` to name one, or REX_CLIENT. With neither, the app client is used when exactly one is connected. An init.lua action's queued client actions go to the same client, and so do a script's calls to rex.client.queue.

| Flag | Description |
| --- | --- |
| `--args JSON` | Pass the arguments as a JSON object (@FILE, or - for stdin). |
| `-s, --session string` | Scope to session SESSION. |
| `-b, --block BLOCK` | Apply the action to BLOCK (default: the focused block). |
| `--origin ORIGIN` | Report the origin as ORIGIN: key, palette, api, or cli. Defaults to `cli`. |
| `-e, --eval CODE` | Run CODE as a Lua script. |
| `-a, --action NAME` | Run the action NAME that the script defines. |
| `--all` | Listen for events from every session. |
| `--for DURATION` | Stop listening for events after DURATION. |
| `--fail-fast` | Exit at the first rex.on handler that fails. |
| `--json` | Print the result as JSON. |

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

Send input to a terminal

| Flag | Description |
| --- | --- |
| `-b, --block string` | Send to block BLOCK. |
| `-s, --session string` | Scope to session SESSION. |
| `-w, --window string` | Scope to window WINDOW. |

```sh
rex send 'make test'
rex send -b logs $'\003'
printf 'y\n' | rex send
rex send -s build -w 2 'ls'
```

### `rex send-key KEY...`

Send key presses to a terminal

Each KEY uses Rex's key binding syntax. Join modifiers with +, as in ctrl+c or shift+left. A bracketed name such as [Slash] selects a physical key. By default, Rex sends a press followed by a release for each key. Use `--action` to send one action instead.

Rex interprets printable keys using a US keyboard layout because send-key does not receive physical keyboard input. The generated text and physical key may differ on other layouts. Use `rex send` when exact text matters.

| Flag | Description |
| --- | --- |
| `-b, --block string` | Send to block BLOCK. |
| `-s, --session string` | Scope to session SESSION. |
| `-w, --window string` | Scope to window WINDOW. |
| `--action ACTION` | Send one ACTION for each key: press, release, or repeat. |

```sh
rex send-key enter
rex send-key ctrl+c
rex send 'make test' && rex send-key enter
rex send-key -b logs ctrl+c
rex send-key shift+left shift+left
rex send-key --action release ctrl+[KeyQ]
```

### `rex capture`

Print a terminal's screen and scrollback.

Print the screen and scrollback of a terminal block.

When `--block` is omitted, Rex uses REX_BLOCK if it names a live block. Otherwise, it uses the focused block of the default window. Text is the default format. HTML preserves rendered styling. VT preserves terminal control sequences. Output always ends with a newline.

A terminal keeps about 64 MiB of scrollback. That is roughly 100,000 lines of plain text at 80 columns, and fewer in a wider terminal or with styled output. Once the limit is reached, the oldest lines are dropped.

| Flag | Description |
| --- | --- |
| `-b, --block BLOCK` | Select block BLOCK. |
| `-s, --session string` | Scope to session SESSION. |
| `-w, --window string` | Scope to window WINDOW. |
| `--format FORMAT` | Output FORMAT: text, html, or vt. Defaults to `text`. |
| `--trim` | Remove trailing blank lines. |
| `--unwrap` | Join soft-wrapped lines. |

```sh
rex capture
rex capture -b logs --trim > screen.txt
rex capture --format=html > screen.html
rex capture -s build -w 2
```

### `rex kill SESSION...`

Kill sessions.

### `rex forward`

Forward TCP ports.

### `rex forward new (-L|-R) [bind_address:]port:host:hostport...`

Forward ports until interrupted.

Forward TCP connections through a Rex server, like ssh `-L` and ssh `-R`.

`-L` ("client's port; server's network") [bind_address:]port:host:hostport listens on this machine on &lt;port&gt;, and connects each local connection to &lt;host&gt;:&lt;hostport&gt; from the server.

`-R` ("server's port; client's network") [bind_address:]port:host:hostport listens on the server on &lt;port&gt;, and connects each remote connection to &lt;host&gt;:&lt;hostport&gt; from this machine.

The bind address defaults to 127.0.0.1; use * for every interface. Port 0 picks a free port. Give `-L` and `-R` as many times as you like to create multiple forwards. They will all be managed by this process and have the same lifetime.

Each forward is a tunnel block in the session chosen with `--session`, or the default session. `rex forward new` runs in the foreground until interrupted, then closes its blocks. It prints nothing while it works unless `-v` is given.

When the connection to the server drops, `rex forward new` reconnects and carries on with the same blocks. TCP connections that were open when it dropped are reset.

A forward whose block is closed, for example with `rex forward close`, stops. `rex forward new` exits once it has no forwards left. If the session is destroyed, it exits with status 3, as for a session that does not exist.

A `rex forward new` that is killed leaves its forwards' blocks behind. Setting up the same forward again from this machine takes over its block instead of making a new one, so running the same command again works. A `-R` forward on port 0 always gets a new port. Blocks that a client on another machine may still come back for are left alone.

| Flag | Description |
| --- | --- |
| `-L, --local stringArray` | Listen here on port and connect to host:hostport from the server. |
| `-R, --remote stringArray` | Listen on the server on port and connect to host:hostport from here. |
| `-s, --session string` | Keep the forwards' blocks in session SESSION. |

### `rex forward open [flags] (URL | [host:]port | BLOCK)`

Forward a local port to a server-side target and open it.

Forward a port on this machine to a target that the server can reach, and open it. This is `rex forward new` `-L` for the common case of one forward.

The target is a URL, such as http://localhost:8080/app or postgres://db/app, or host:port, or a port, which means that port on the server's localhost. A target without a scheme is taken to be http. A URL without a port uses the usual port for its scheme, if known.

The target can also be a terminal block, given by its ID or label, as rex block ls shows them. The forward then goes to the port that a program in the terminal is listening on, such as a development server started there, and is opened as http. If the terminal's programs listen on several ports, `rex forward open` lists them and forwards none. An argument that reads as a URL, host:port or port is always taken as one, so name a block whose label reads that way by its ID. The server finds the ports of programs that are still attached to the terminal, so it misses e.g. a daemon.

The forward listens on `--bind` and `--port`, by default 127.0.0.1 and a free port. Once it listens, `rex forward open` prints the target's URL with its host and port changed to where the forward listens, and opens that URL. An http or https URL goes to $BROWSER if it is set: a list of commands separated by colons, in which %s stands for the URL. Any other URL, or one $BROWSER cannot open, goes to the system's handler for its scheme. With `--url-only`, it is only printed.

A browser addresses what it sends to localhost and the forward's port rather than to the target's own name, so a site that checks the Host header, or that serves https with a certificate for its own name, may not work through the forward.

The forward's block is kept in the session chosen with `--session`, or the default session. For a terminal block it is kept in the terminal's session, and `--session` says which session to look for the terminal in.

`rex forward open` runs in the foreground like `rex forward new`, until it is interrupted or the forward is closed with `rex forward close`.

| Flag | Description |
| --- | --- |
| `-b, --bind ADDRESS` | Listen on ADDRESS; * means every interface. Defaults to `127.0.0.1`. |
| `-p, --port PORT` | Listen on PORT; 0 picks a free port. |
| `-s, --session string` | Keep the forward's block in session SESSION. |
| `--url-only` | Print the URL without opening it. |

### `rex forward share [flags] (URL | [host:]port)`

Forward a server port to a target on this machine's side.

Forward a port on the server to a target that this machine can reach. This is `rex forward new` `-R` for the common case of one forward.

The target is a URL, such as http://localhost:3000, or host:port, or a port, which means that port on this machine's localhost. URLs without a port are read as for `rex forward open`.

The forward listens on the server on `--bind` and `--port`, by default 127.0.0.1 and a free port. Use `--bind` '*' to let other machines connect to it. Once it listens, `rex forward share` prints where: the target's URL with its host and port changed, if the target is a URL, or else host:port. With `--bind` '*' the host is the server's, as rex reached it.

Clients address what they send to the server rather than to the target's own name, so a site that checks the Host header, or that serves https with a certificate for its own name, may not work through the forward.

`rex forward share` runs in the foreground like `rex forward new`, until it is interrupted or the forward is closed with `rex forward close`.

| Flag | Description |
| --- | --- |
| `-b, --bind ADDRESS` | Listen on ADDRESS; * means every interface. Defaults to `127.0.0.1`. |
| `-p, --port PORT` | Listen on PORT; 0 picks a free port. |
| `-s, --session string` | Keep the forward's block in session SESSION. |

### `rex forward ls`

List forwards.

List the forwards in a session: the tunnel blocks that `rex forward new` and other clients create.

STATE is active while the client carrying the forward is connected, away while it is disconnected but may come back, and orphaned once nothing carries it, for example after its `rex forward new` was killed. An orphaned forward that listens on the server still accepts connections, which then time out, so `rex forward ls` warns about orphans; close them with `rex forward close`.

DIRECTION shows where the forward listens and where it connects from: client -&gt; server is a `-L` forward, and server -&gt; client is a `-R` one. A field the client did not report shows -.

| Flag | Description |
| --- | --- |
| `-s, --session string` | Scope to session SESSION. |
| `-A, --all` | List forwards in every session. |
| `--json` | Output forwards as JSON. |
| `-q, --quiet` | Print IDs only, one per line. |
| `--short` | Show short IDs (`--short=false` shows full IDs). Defaults to `true`. |

### `rex forward close [FORWARD...]`

Close forwards by closing their tunnel blocks. Give the forwards' IDs, as rex forward ls shows them, or close every orphaned forward in the session with `--orphaned`, or every forward in it with `--all`.

A `rex forward new` that is carrying a closed forward stops it, and exits once it has no forwards left.

| Flag | Description |
| --- | --- |
| `-s, --session string` | Scope to session SESSION. |
| `--orphaned` | Close every orphaned forward in the session. |
| `--all` | Close every forward in the session. |

### `rex cp [-r] SOURCE... DEST`

Copy files to or from a server.

Copy files and directories between this machine and a server.

A path on the server starts with a colon, and the server is the one `--server` names, or the default one:

  `rex cp` report.pdf :docs/   rex `-S` build cp ':out/*.tar.gz' .

A known host's label can stand before the colon instead, as in scp:

  `rex cp` `-r` ./site web:/var/www/

Exactly one side is on the server: either every source, or the destination. A path on the server is relative to the home directory there unless it is absolute, and a leading ~ is the home directory too. Quote a pattern meant for the server so that the shell leaves it alone. Patterns use *, ? and [...], and a directory needs `-r`.

The destination follows cp's rules. If it is a directory, the sources go inside it. Otherwise there must be one source, which takes that name. A file replaces a file. A directory that is already there is merged into, and files in it that were not sent are left alone. A file where a directory is, or the reverse, stops the copy before anything changes.

Nothing appears at the destination until the whole copy has arrived, so a copy that fails or is interrupted leaves the destination as it was. Permissions and modification times are kept; ownership is not. A source that is a symbolic link is followed, and links inside a directory are copied as links. Devices, FIFOs and sockets inside a directory are skipped, and one named as a source is an error.

The copy runs through an fs block that `rex cp` creates on the server and closes when it is done. A server started with `--no-fs` does not offer one.

| Flag | Description |
| --- | --- |
| `-r, --recursive` | Copy directories and everything in them. |
| `--progress` | Show how far the copy has got, on standard error. |
| `-s, --session string` | Keep the copy's block in session SESSION. |

## Layout

### `rex focus TARGET|DIRECTION`

Focus a block or window.

The directions left, right, up, and down move between blocks by position. Next and prev move through the blocks in layout order. Focus stops at the edge of the layout or the end of the order. Use `--wrap` to continue from the other side.

A target can be a block or window ID, label, or ID suffix. A positive integer selects a window by its one-based position. If a target matches both a block and a window, use a full ID to select the intended resource.

| Flag | Description |
| --- | --- |
| `-s, --session string` | Scope to session SESSION. |
| `-w, --window string` | Scope to window WINDOW. |
| `--wrap` | Continue from the other side at the edge. |

```sh
rex focus left
rex focus left --wrap
rex focus next --wrap
rex focus 2
rex focus logs
rex focus -s build editor
```

### `rex zoom [BLOCK]`

Zoom a block to fill its window.

Zoom changes only how the block is displayed. It does not change the underlying window layout. Without `--on` or `--off`, the command toggles the current zoom state. Use `--on` or `--off` to set the state explicitly.

BLOCK may be passed as an argument or with `--block`. If BLOCK is omitted, Rex uses REX_BLOCK when it identifies a live block. Otherwise, Rex uses the focused block in the default window.

| Flag | Description |
| --- | --- |
| `-b, --block BLOCK` | Select block BLOCK. |
| `-s, --session string` | Scope to session SESSION. |
| `-w, --window string` | Scope to window WINDOW. |
| `--on` | Enable zoom. |
| `--off` | Disable zoom. |

```sh
rex zoom
rex zoom --off
rex zoom -b logs --on
```

### `rex move [BLOCK] DIRECTION ANCHOR`

Move a block next to another.

Move a block next to an anchor block.

DIRECTION selects BLOCK's new position relative to ANCHOR. It must be right, left, above, or below. The two blocks may be in different windows, but both must be visible and belong to the same session.

If BLOCK is omitted, Rex uses REX_BLOCK when it identifies a visible block. Otherwise, Rex uses the focused block in the default window. The `--ratio` flag sets the percentage of the resulting split assigned to BLOCK. PCT must be between 1 and 99.

If a block label is also a direction word, identify the block by its full block ID or a hexadecimal ID suffix.

| Flag | Description |
| --- | --- |
| `--ratio PCT` | Give the moved block PCT percent of the split. Defaults to `50`. |
| `-s, --session string` | Scope to session SESSION. |
| `-w, --window string` | Scope to window WINDOW. |

```sh
rex move below editor
rex move logs right editor --ratio 30
rex move c2a9f3 above 1bc2a9 -s work
```

### `rex swap BLOCK OTHER`

Swap two blocks.

Swap the layout positions of two visible blocks.

The blocks may be in different windows, but they must belong to the same session. Rex resolves both block arguments before changing the layout. The surrounding layout is unchanged.

| Flag | Description |
| --- | --- |
| `-s, --session string` | Scope to session SESSION. |
| `-w, --window string` | Scope to window WINDOW. |

```sh
rex swap editor logs
rex swap c2a9f3 1bc2a9
```

### `rex resize [BLOCK]`

Resize a block.

## Resources

### `rex session`

Manage sessions.

### `rex session new [LABEL] [-- COMMAND...]`

Create a session.

| Flag | Description |
| --- | --- |
| `-c, --cwd string` | Working directory for the terminal. |
| `--keep-open` | Keep the terminal open after its command exits. |
| `--shell SHELL` | Run COMMAND through SHELL's login environment (none starts it directly). |
| `--interactive` | Also read the shell's interactive startup files, such as ~/.zshrc. |
| `--window string` | Label for the first window. |
| `--json` | Output the created session as JSON. |

### `rex session ls`

List sessions.

| Flag | Description |
| --- | --- |
| `--json` | Output sessions as JSON. |
| `-q, --quiet` | Print IDs only, one per line. |
| `--short` | Show short IDs (`--short=false` shows full IDs). Defaults to `true`. |

### `rex session inspect [SESSION]`

Inspect a session.

| Flag | Description |
| --- | --- |
| `--json` | Output session information as JSON. |

### `rex session rename [SESSION] LABEL`

Rename a session.

### `rex session move [SESSION] (--before S | --after S | --index N)`

Move a session to a new place in the session order.

The session order is the order that session ls prints. SESSION, `--before`, and `--after` name a session by its label or ID, not by its position in the order.

Exactly one of `--before`, `--after`, or `--index` is required. Positions count from one. An index past the end moves the session last. Moving a session to where it already is does nothing and succeeds.

If SESSION is omitted, Rex uses the session containing REX_BLOCK when available. Otherwise, it uses the session in REX_SESSION, or the only session if there is just one.

| Flag | Description |
| --- | --- |
| `--before S` | Move immediately before session S. |
| `--after S` | Move immediately after session S. |
| `--index N` | Move to one-based position N. |

```sh
rex session move logs --before work
rex session move build --after logs
rex session move --index 1
rex session move build --index 99
```

### `rex session kill SESSION...`

Kill sessions.

### `rex window`

Manage windows.

### `rex window new [-s SESSION] [LABEL] [-- COMMAND...]`

Create a window in the selected session. The new window becomes active by default. Use `--focus=false` to keep the active window and focused block unchanged. If the session has no active window, the new window becomes active even with `--focus=false.`

| Flag | Description |
| --- | --- |
| `-s, --session string` | Scope to session SESSION. |
| `-c, --cwd string` | Working directory for the terminal. |
| `--keep-open` | Keep the terminal open after its command exits. |
| `--shell SHELL` | Run COMMAND through SHELL's login environment (none starts it directly). |
| `--interactive` | Also read the shell's interactive startup files, such as ~/.zshrc. |
| `--focus` | Make the new window active (`--focus=false` leaves the current window active). Defaults to `true`. |
| `--json` | Output the created window as JSON. |

```sh
rex window new
rex window new logs -- tail -f app.log
rex window new logs --focus=false -- tail -f app.log
rex window new -s build tests
```

### `rex window ls`

List windows.

| Flag | Description |
| --- | --- |
| `-s, --session string` | Scope to session SESSION. |
| `-A, --all` | List windows in every session. |
| `--json` | Output windows as JSON. |
| `-q, --quiet` | Print IDs only, one per line. |
| `--short` | Show short IDs (`--short=false` shows full IDs). Defaults to `true`. |

### `rex window inspect [WINDOW]`

Inspect a window.

| Flag | Description |
| --- | --- |
| `-s, --session string` | Scope to session SESSION. |
| `--json` | Output window information as JSON. |

### `rex window focus [WINDOW|next|prev]`

Focus a window by ID, label, position, or ID suffix.

If WINDOW is omitted, focus the window containing REX_BLOCK when available. Otherwise, focus the active window in the default session. Use next or prev to move through window order.

| Flag | Description |
| --- | --- |
| `-s, --session string` | Scope to session SESSION. |
| `--wrap` | Wrap next and prev at the ends. |

### `rex window move [WINDOW] (--before W | --after W | --index N | --to SESSION) [-s SESSION]`

Move a window within its session's tab order, or to another session.

Within a session, exactly one of `--before`, `--after`, or `--index` is required. Window positions are numbered from one in the same order shown by window ls. An index past the end moves the window last.

With `--to`, the window moves to SESSION with its blocks still running. Programs keep running and terminals keep their scrollback. The window goes to the end of that session unless `--before`, `--after`, or `--index` places it among the session's windows. Add `--focus` to make it the active window there. A program that is already running keeps the REX_SESSION it started with.

If WINDOW is omitted, Rex uses the window containing REX_BLOCK when available. Otherwise, Rex uses the active window in the default session.

| Flag | Description |
| --- | --- |
| `--before W` | Move immediately before window W. |
| `--after W` | Move immediately after window W. |
| `--index N` | Move to one-based position N. |
| `--to SESSION` | Move to SESSION, keeping the window's blocks running. |
| `--focus` | With `--to`, make the window active in its new session. |
| `-s, --session string` | Scope to session SESSION. |

```sh
rex window move logs --before editor
rex window move 3 --after 1
rex window move --index 1
rex window move -s work build --index 99
rex window move logs --to ops
rex window move -s work build --to ops --before deploy --focus
```

### `rex window rename [WINDOW] LABEL`

Rename a window.

| Flag | Description |
| --- | --- |
| `-s, --session string` | Scope to session SESSION. |

### `rex window close WINDOW...`

Close windows.

| Flag | Description |
| --- | --- |
| `-s, --session string` | Scope to session SESSION. |

### `rex block`

Manage blocks.

### `rex block new FLAVOR`

Create a block.

### `rex block ls`

List blocks.

| Flag | Description |
| --- | --- |
| `-s, --session string` | Scope to session SESSION. |
| `-w, --window string` | Scope to window WINDOW. |
| `-A, --all` | List blocks in every session. |
| `--json` | Output blocks as JSON. |
| `-q, --quiet` | Print IDs only, one per line. |
| `--short` | Show short IDs (`--short=false` shows full IDs). Defaults to `true`. |

### `rex block inspect [BLOCK]`

Inspect a block.

| Flag | Description |
| --- | --- |
| `-s, --session string` | Scope to session SESSION. |
| `-w, --window string` | Scope to window WINDOW. |
| `--json` | Output block information as JSON. |

### `rex block focus [BLOCK]`

Focus a block by ID, label, or ID suffix.

If BLOCK is omitted, focus the block named by REX_BLOCK when available. Otherwise, focus the current block in the default window.

| Flag | Description |
| --- | --- |
| `-s, --session string` | Scope to session SESSION. |
| `-w, --window string` | Scope to window WINDOW. |

### `rex block types`

List block types.

| Flag | Description |
| --- | --- |
| `--json` | Output block types as JSON. |

### `rex block send [TEXT]`

Send input to a terminal

| Flag | Description |
| --- | --- |
| `-b, --block string` | Send to block BLOCK. |
| `-s, --session string` | Scope to session SESSION. |
| `-w, --window string` | Scope to window WINDOW. |

```sh
rex send 'make test'
rex send -b logs $'\003'
printf 'y\n' | rex send
rex send -s build -w 2 'ls'
```

### `rex block send-key KEY...`

Send key presses to a terminal

Each KEY uses Rex's key binding syntax. Join modifiers with +, as in ctrl+c or shift+left. A bracketed name such as [Slash] selects a physical key. By default, Rex sends a press followed by a release for each key. Use `--action` to send one action instead.

Rex interprets printable keys using a US keyboard layout because send-key does not receive physical keyboard input. The generated text and physical key may differ on other layouts. Use `rex send` when exact text matters.

| Flag | Description |
| --- | --- |
| `-b, --block string` | Send to block BLOCK. |
| `-s, --session string` | Scope to session SESSION. |
| `-w, --window string` | Scope to window WINDOW. |
| `--action ACTION` | Send one ACTION for each key: press, release, or repeat. |

```sh
rex send-key enter
rex send-key ctrl+c
rex send 'make test' && rex send-key enter
rex send-key -b logs ctrl+c
rex send-key shift+left shift+left
rex send-key --action release ctrl+[KeyQ]
```

### `rex block capture`

Print a terminal's screen and scrollback.

Print the screen and scrollback of a terminal block.

When `--block` is omitted, Rex uses REX_BLOCK if it names a live block. Otherwise, it uses the focused block of the default window. Text is the default format. HTML preserves rendered styling. VT preserves terminal control sequences. Output always ends with a newline.

A terminal keeps about 64 MiB of scrollback. That is roughly 100,000 lines of plain text at 80 columns, and fewer in a wider terminal or with styled output. Once the limit is reached, the oldest lines are dropped.

| Flag | Description |
| --- | --- |
| `-b, --block BLOCK` | Select block BLOCK. |
| `-s, --session string` | Scope to session SESSION. |
| `-w, --window string` | Scope to window WINDOW. |
| `--format FORMAT` | Output FORMAT: text, html, or vt. Defaults to `text`. |
| `--trim` | Remove trailing blank lines. |
| `--unwrap` | Join soft-wrapped lines. |

```sh
rex block capture
rex block capture -b logs --trim > screen.txt
rex block capture --format=html > screen.html
rex block capture -s build -w 2
```

### `rex block zoom [BLOCK]`

Zoom a block to fill its window.

Zoom changes only how the block is displayed. It does not change the underlying window layout. Without `--on` or `--off`, the command toggles the current zoom state. Use `--on` or `--off` to set the state explicitly.

BLOCK may be passed as an argument or with `--block`. If BLOCK is omitted, Rex uses REX_BLOCK when it identifies a live block. Otherwise, Rex uses the focused block in the default window.

| Flag | Description |
| --- | --- |
| `-b, --block BLOCK` | Select block BLOCK. |
| `-s, --session string` | Scope to session SESSION. |
| `-w, --window string` | Scope to window WINDOW. |
| `--on` | Enable zoom. |
| `--off` | Disable zoom. |

```sh
rex block zoom
rex block zoom --off
rex block zoom -b logs --on
```

### `rex block move [BLOCK] DIRECTION ANCHOR`

Move a block next to another.

Move a block next to an anchor block.

DIRECTION selects BLOCK's new position relative to ANCHOR. It must be right, left, above, or below. The two blocks may be in different windows, but both must be visible and belong to the same session.

If BLOCK is omitted, Rex uses REX_BLOCK when it identifies a visible block. Otherwise, Rex uses the focused block in the default window. The `--ratio` flag sets the percentage of the resulting split assigned to BLOCK. PCT must be between 1 and 99.

If a block label is also a direction word, identify the block by its full block ID or a hexadecimal ID suffix.

| Flag | Description |
| --- | --- |
| `--ratio PCT` | Give the moved block PCT percent of the split. Defaults to `50`. |
| `-s, --session string` | Scope to session SESSION. |
| `-w, --window string` | Scope to window WINDOW. |

```sh
rex block move below editor
rex block move logs right editor --ratio 30
rex block move c2a9f3 above 1bc2a9 -s work
```

### `rex block swap BLOCK OTHER`

Swap two blocks.

Swap the layout positions of two visible blocks.

The blocks may be in different windows, but they must belong to the same session. Rex resolves both block arguments before changing the layout. The surrounding layout is unchanged.

| Flag | Description |
| --- | --- |
| `-s, --session string` | Scope to session SESSION. |
| `-w, --window string` | Scope to window WINDOW. |

```sh
rex block swap editor logs
rex block swap c2a9f3 1bc2a9
```

### `rex block stream BLOCK [DATA_REF]`

Stream block data.

### `rex block call METHOD [ARGS]`

Call a block method.

Call one method exposed by a block.

METHOD is the block method name. ARGS must be a JSON object. Pass the object directly, use @path to read it from a file, or use - to read it from stdin. When ARGS is omitted, the request sends no arguments.

When `--block` is omitted, Rex uses REX_BLOCK if it names a live block. Otherwise, it uses the focused block of the default window.

Method results are JSON. Output written to a terminal uses two-space indentation. Redirected output stays on one line for use in scripts. Use `rex block inspect` to list methods and `rex block inspect` `--json` to view their schemas.

| Flag | Description |
| --- | --- |
| `-b, --block BLOCK` | Select block BLOCK. |
| `-s, --session string` | Scope to session SESSION. |
| `-w, --window string` | Scope to window WINDOW. |

```sh
rex block call process
rex block call -b c2a9f3 write '{"data":"ls\n"}'
rex block call -b logs format @request.json
echo '{"format":"text","trim":true}' | rex block call format -
```

### `rex block rename [BLOCK] LABEL`

Rename a block.

| Flag | Description |
| --- | --- |
| `-s, --session string` | Scope to session SESSION. |
| `-w, --window string` | Scope to window WINDOW. |

### `rex block close BLOCK...`

Close blocks.

| Flag | Description |
| --- | --- |
| `-s, --session string` | Scope to session SESSION. |
| `-w, --window string` | Scope to window WINDOW. |

### `rex client`

Manage clients.

Inspect the clients connected to the server.

A client is one program connected to the server, such as Rex.app or this command. Each client says what it is when it connects, and a person may give it a label.

### `rex client ls`

List clients.

List the clients connected to the server.

Each client says what it is when it connects. The label is the name a person gave it, and two clients may share one. Command line clients such as this one are hidden unless `--all` is given. With `--json`, the output is the server's full reply, including command line clients. Use `-s` to list only the clients attached to one session.

| Flag | Description |
| --- | --- |
| `-s, --session string` | Scope to session SESSION. |
| `--all` | Include command line clients. |
| `--json` | Output clients as JSON. |
| `-q, --quiet` | Print IDs only, one per line. |
| `--short` | Show short IDs (`--short=false` shows full IDs). Defaults to `true`. |

```sh
rex client ls
rex client ls -s work
rex client ls --all
rex client ls -q
```

### `rex client inspect [CLIENT]`

Inspect a client.

Show one client and the actions it offers.

CLIENT is a client ID, label, or ID suffix. With no CLIENT, `-C` or REX_CLIENT names the client, and otherwise the app client is used when exactly one is connected.

| Flag | Description |
| --- | --- |
| `--json` | Output the client and its actions as JSON. |

```sh
rex client inspect studio
rex client inspect 3f9a
rex client inspect --json
```

## Automation

### `rex events`

Stream server events as they occur.

Without `--session`, events follows session creation, removal, state changes, and server connectivity for the whole server. Use `--session` to follow one session, including custom events emitted by its blocks. Use `--all` to follow every server event, including clients joining, leaving, and changing.

The default format writes one human-readable line per event. With `--json`, each line contains the same event JSON object sent by the server, compacted onto one line. Output is flushed after every event so pipelines can process events as they arrive.

The command runs until interrupted or the server disconnects. `--timeout` limits connecting and starting event delivery. It does not limit how long events are streamed.

| Flag | Description |
| --- | --- |
| `-s, --session string` | Scope to session SESSION. |
| `--all` | Follow every server event, including clients joining, leaving, and changing. |
| `--json` | Output events as newline-delimited JSON. |

```sh
rex events
rex events -s build
rex events --all
rex events --json | jq -c 'select(.type == "session_created")'
```

### `rex wait TARGET`

Wait for a block, window, or session to end.

For a terminal block, wait returns the child process's exit status. It does not wait for the block itself to close, so it also works with terminals created with `--keep-open`. Waiting for any other block, a window, or a session succeeds when that resource closes or is destroyed. If a terminal closes before reporting a child exit, wait returns 1. A block that closes before wait starts watching it also returns 1, because Rex can no longer tell what kind of block it was.

By default, wait runs until the target ends or the server disconnects. Use `--for` to limit the wait. The global `--timeout` still limits connections and individual API requests, but it does not limit event delivery. With `--json`, the command writes the payload that ended the wait as one line of JSON.

If Rex cannot determine a terminal child's exit status, wait returns 1. Statuses above 255 are reduced modulo 256 to match shell behavior.

Targets may be IDs, labels, ID suffixes, or a window's one-based position. If a target matches more than one resource kind, use a full ID to select the intended resource.

| Flag | Description |
| --- | --- |
| `-s, --session string` | Scope to session SESSION. |
| `-w, --window string` | Scope to window WINDOW. |
| `--for DURATION` | Give up after DURATION. |
| `--json` | Output the terminating payload as JSON. |

```sh
rex wait c2a9f3
rex wait build
rex wait 2 -s work
rex wait --for 10m $B || echo timed out
```

### `rex api`

Inspect and call the server API.

Inspect and call methods exposed by the server's control API.

Use call to run a method by name. Use list to discover the methods exposed by the connected server, including methods provided by block creators. Use describe to read one method's schemas, examples, and validation rules.

```sh
rex api call server.status
rex api call -s work session.view
rex api list
rex api describe session.new_split
```

### `rex api call METHOD [ARGS]`

Call a server API method.

Call one method exposed by the server's control API.

METHOD is the API method name, such as server.status. ARGS must be a JSON object. Pass the object directly, use @path to read it from a file, or use - to read it from stdin. When ARGS is omitted, the request sends no arguments.

Methods that take a session_id require the connection to attach to that session. Use `--session` to resolve a session by ID or label and attach before the request. The command adds session_id to ARGS when it is missing. If ARGS already contains session_id, the value is preserved and must match the selected session. Without `--session`, a top-level session_id in ARGS is used for the attachment.

Method results are JSON. Output written to a terminal uses two-space indentation. Redirected output stays on one line for use in scripts.

| Flag | Description |
| --- | --- |
| `-s, --session string` | Scope to session SESSION. |

```sh
rex api call server.status
rex api call -s work session.view | jq '.windows | length'
rex api call session.create @layout.json
echo '{"label":"x"}' | rex api call session.create -
```

### `rex api list`

List server API methods.

List methods exposed by the connected server.

The default output has separate tables for regular API methods and methods provided by block creators. Use `--quiet` to print only method names, one per line. Use `--json` to print the complete help document returned by the server.

| Flag | Description |
| --- | --- |
| `-q, --quiet` | Print method names only. |
| `--json` | Output the API help document as JSON. |

### `rex api describe METHOD`

Describe a server API method.

Describe one method exposed by the connected server.

The default output includes the method's description and any available schemas, examples, and validation rules. Use `--json` to print the method's entry from the server's help document.

| Flag | Description |
| --- | --- |
| `--json` | Output the method description as JSON. |

### `rex actions`

List the actions a client or the server offers.

List the actions that a client or the server offers.

With `-C` or REX_CLIENT, this lists the actions that client offers, as it most recently reported them to the server. Otherwise it lists the actions the server offers: those that init.lua defines with rex.action, followed by those of every block type. A key binding can name any action in either list.

The ARGS column lists each action's arguments. An argument followed by ? is optional.

| Flag | Description |
| --- | --- |
| `--json` | Output actions as JSON. |

```sh
rex actions
rex -C studio actions
rex actions --json
```

## Server

### `rex server`

Manage the Rex server.

### `rex server run`

Run a foreground server.

Run a Rex server in the foreground until it is stopped.

Ctrl+C, SIGTERM, and `rex server stop` end the server after it saves its sessions.

On Unix, what SIGHUP does depends on how the server runs. A server in a terminal saves and stops, because closing a terminal sends SIGHUP. A server with no terminal, such as one that systemd, launchd, or a container runtime runs, logs the signal and keeps running. A server started under nohup keeps ignoring the signal. A server that `rex server start` launched reopens its log file instead. See `rex server logs` `--help`.

If nothing reads the server's output any more, for example because tee exited when its terminal closed or an ssh connection dropped, the server keeps running and its log lines are lost. Stop it with `rex server stop`.

| Flag | Description |
| --- | --- |
| `--listen ENDPOINT` | Listen on ENDPOINT (default: the local Rex Unix socket, or the Rex named pipe on Windows). |
| `--extra-listen ENDPOINT` | Also listen on unix, http, tailnet, tailnet-serve, or login-server ENDPOINT (repeatable, but not tailnet-serve or login-server on Windows). |
| `--socket-mode MODE` | Set Unix socket permissions to MODE, owner and group bits only (default 0600, not available on Windows). |
| `--allow-anonymous` | Admit anonymous callers on plain TCP listeners (every connection gets full access). |
| `--tailnet-allow-identified` | Admit every identified caller through the host's tailscaled (default: node owner). |
| `--tailscaled-socket PATH` | Use the tailscaled LocalAPI socket at PATH (default: platform socket). |
| `--tailscale-allow-tailnet-members` | Allow any tailnet member permitted by ACLs to reach Rex. |
| `--exit-empty` | Stop when no sessions or control connections remain. |
| `--websocket-origin-pattern PATTERN` | Allow browser WebSockets from cross-origin PATTERN (repeatable). |
| `--block-dir DIR` | Discover executable block plugins in DIR (repeatable). |
| `--block-plugin-reload` | Reload block plugins after source changes. |
| `--state-dir DIR` | Store persistent server state below DIR. |
| `--restore` | Restore the saved sessions (false starts without them and saves nothing). Defaults to `true`. |
| `--no-fs` | Leave out the fs block, so that clients cannot copy files to or from this machine with `rex cp`. |
| `--config PATH` | Read the config file at PATH (default: REX_CONFIG, else rex/init.lua in the config directory). |
| `--max-sessions N` | Refuse new sessions once the server holds N (0 for no limit). Defaults to `64`. |
| `--max-blocks N` | Refuse new blocks once the server holds N across all sessions (0 for no limit). Defaults to `1024`. |
| `--max-windows N` | Refuse new windows once a session holds N (0 for no limit). Defaults to `64`. |
| `--max-panes N` | Refuse new panes once a window holds N (0 for no limit). Defaults to `64`. |
| `--tailscale` | Also serve the API over the tailnet as an embedded tsnet node. |
| `--tailscale-hostname NAME` | Tailnet device NAME for `--tailscale`. Defaults to `rex`. |
| `--tailscale-control-url URL` | Register the tailnet node with the control server at URL, such as Headscale. |
| `--tailscale-auth-key-file FILE` | Enroll `--tailscale` with the one-time auth key read from FILE ('-' for stdin). |
| `--tailscale-advertise-tag TAG` | Advertise ACL TAG (tag:name) when `--tailscale` enrolls the node (repeatable). |
| `--log-format FORMAT` | Write server logs as FORMAT: text or json. Defaults to `text`. |
| `--log-level LEVEL` | Log at LEVEL and above: debug, info, warn, or error (default info, or debug if `-v` is given without this flag). |

### `rex server start`

Start a persistent server.

Start is idempotent. Start options apply only when a new server is launched. An existing server retains its active configuration until explicitly restarted.

If you pass `--env` and this command does not launch the server, it prints a warning that names the variables it could not apply. To apply them, stop the server and run this command again, or set them in the service that starts the server, such as a systemd unit.

The log size limit applies only to the file created for a detached server. Rex clears that file before a write would exceed `--log-max-size`.

| Flag | Description |
| --- | --- |
| `--extra-listen ENDPOINT` | Also listen on unix, http, tailnet, tailnet-serve, or login-server ENDPOINT (repeatable, but not tailnet-serve or login-server on Windows). |
| `--socket-mode MODE` | Set Unix socket permissions to MODE, owner and group bits only (default 0600, not available on Windows). |
| `--allow-anonymous` | Admit anonymous callers on plain TCP listeners (every connection gets full access). |
| `--tailnet-allow-identified` | Admit every identified caller through the host's tailscaled (default: node owner). |
| `--tailscaled-socket PATH` | Use the tailscaled LocalAPI socket at PATH (default: platform socket). |
| `--websocket-origin-pattern PATTERN` | Allow browser WebSockets from cross-origin PATTERN (repeatable). |
| `--block-dir DIR` | Discover executable block plugins in DIR (repeatable). |
| `--block-plugin-reload` | Reload block plugins after source changes. |
| `--state-dir DIR` | Store persistent server state below DIR. |
| `--restore` | Restore the saved sessions (false starts without them and saves nothing). Defaults to `true`. |
| `--config PATH` | Read the config file at PATH (default: REX_CONFIG, else rex/init.lua in the config directory). |
| `--max-sessions N` | Refuse new sessions once the server holds N (0 for no limit). Defaults to `64`. |
| `--max-blocks N` | Refuse new blocks once the server holds N across all sessions (0 for no limit). Defaults to `1024`. |
| `--max-windows N` | Refuse new windows once a session holds N (0 for no limit). Defaults to `64`. |
| `--max-panes N` | Refuse new panes once a window holds N (0 for no limit). Defaults to `64`. |
| `--tailscale-allow-tailnet-members` | Allow any tailnet member permitted by ACLs to reach Rex. |
| `--tailscale` | Also serve the API over the tailnet as an embedded tsnet node. |
| `--tailscale-hostname NAME` | Tailnet device NAME for `--tailscale`. Defaults to `rex`. |
| `--tailscale-control-url URL` | Register the tailnet node with the control server at URL, such as Headscale. |
| `--tailscale-auth-key-file FILE` | Enroll `--tailscale` with the one-time auth key read from FILE. |
| `--tailscale-advertise-tag TAG` | Advertise ACL TAG (tag:name) when `--tailscale` enrolls the node (repeatable). |
| `--log-format FORMAT` | Write server logs as FORMAT: text or json. Defaults to `text`. |
| `--log-level LEVEL` | Log at LEVEL and above: debug, info, warn, or error (default info, or debug if `-v` is given without this flag). |
| `--log-max-size SIZE` | Limit the active detached log to SIZE by clearing old contents (0 disables). Defaults to `50MiB`. |
| `--env NAME` | Pass environment variable NAME or NAME=VALUE to a new server (repeatable). |
| `--elevated` | Keep the administrator rights of a terminal opened with Run as administrator, and admit only programs with them (Windows only). |
| `--json` | Output server information as JSON. |

### `rex server status`

Show server status.

| Flag | Description |
| --- | --- |
| `--json` | Output server information as JSON. |

### `rex server logs`

Show detached server logs.

Show logs captured for a server launched by `rex server start`.

Without `--server`, the command shows the log of the server that REX_SERVER names, and otherwise the log of your own server. The server must be on this machine.

On Windows, the server that `rex server install` runs as a Windows Service writes to this log too, so this command shows its output as well. As with `rex server start`, Rex clears that log before it grows past 50MiB.

Servers started by other service managers, such as systemd or launchd, log through that manager instead. For a personal server run by the systemd user unit that the Linux packages and the home-manager module install, run journalctl `--user` `-u` rex. For the shared server that the Linux packages and the NixOS module install, run journalctl `-u` rex.service.

On Unix, rename/create rotation must send SIGHUP to the server after creating the replacement file. Only a server that `rex server start` launched reopens its log on SIGHUP. See `rex server run` `--help` for what the signal does to other servers. Windows uses copy-truncate or `--log-max-size`. `--follow` continues across log rotation.

| Flag | Description |
| --- | --- |
| `--follow` | Follow appended log output until the server stops. |
| `--state-dir DIR` | Read server logs below DIR. |
| `-n, --lines N` | Show the newest N log lines. Defaults to `200`. |
| `--all` | Show the entire available detached log. |

### `rex server tailscale`

Manage the server's Tailscale node.

### `rex server tailscale on`

Serve the API over the tailnet.

On is idempotent and runtime-only: a restarted server returns to its start flags. To keep Tailscale on, start the server with `--tailscale`. On Windows, "rex server install -- --tailscale" does that each time the server starts. A node enabled for the first time begins Tailscale's normal authentication flow; the login URL appears in the server log and in `rex server status`.

A one-time auth key enrolls a new node without that browser flow: pass `--auth-key-file` with a path, or '-' to read the key from stdin. There is deliberately no way to pass the key itself on the command line, where it would be visible in the process list. The key is needed only for a node's first enrollment — the enrolled identity is kept on the server — and is ignored while the node is already enabled. ACL tags given with `--advertise-tag` are applied the same way: only when this call enrolls the node for the first time.

`--control-url` registers a node this call starts with another control server, such as Headscale. Each control server keeps its own saved login, so a node moved to a new one signs in again. To move a node that is already on, turn it off first. The server's `--tailscale-control-url` is used when this flag is left out.

| Flag | Description |
| --- | --- |
| `--hostname NAME` | Tailnet device NAME when this call starts the node (defaults to the server's configured name). |
| `--allow-tailnet-members` | Allow any caller admitted by the tailnet instead of only this node's owner. |
| `--auth-key-file FILE` | Enroll a new node with the one-time tailscale auth key read from FILE ('-' for stdin). |
| `--advertise-tag TAG` | Advertise ACL TAG (tag:name) when this call enrolls a new node (repeatable). |
| `--control-url URL` | Register a node this call starts with the control server at URL, such as Headscale. |
| `--json` | Output the resulting state as JSON. |

### `rex server tailscale off`

Stop serving the API over the tailnet.

Running 'off' more than once succeeds. Tailnet connections close while sessions keep running. Keeps you signed in. The next 'on' reconnects without signing in. Use 'logout' to forget this device.

| Flag | Description |
| --- | --- |
| `--json` | Output the resulting state as JSON. |

### `rex server tailscale logout`

Sign out of Tailscale and stop tailnet serving.

Sign out of the enabled Tailscale node and stop tailnet serving. The next 'on' must sign in again. If already off, this leaves the saved login unchanged.

| Flag | Description |
| --- | --- |
| `--json` | Output the resulting state as JSON. |

### `rex server tailscale login`

Request a Tailscale sign-in link.

Request a sign-in link for the enabled Tailscale node. Tailscale can take a few seconds to produce the link. If none is shown, run the command again or check `rex server status`.

| Flag | Description |
| --- | --- |
| `--json` | Output the resulting state as JSON. |

### `rex server tailscale rename NAME`

Rename the enabled Tailscale node without restarting or signing in again. NAME must be one DNS label of 1 to 63 ASCII letters, digits, or hyphens, with no leading or trailing hyphen. The new DNS name may appear after this command returns.

| Flag | Description |
| --- | --- |
| `--json` | Output the resulting state as JSON. |

### `rex server tailscale pair`

Show a QR code to pair another device.

Show the server's tailnet address as a QR code to scan with Rex on another device.

The code holds only the address, not a credential. The other device must be on the same tailnet. Tailscale must be on and its HTTPS address ready.

| Flag | Description |
| --- | --- |
| `--json` | Output the address as JSON. |

### `rex server stop`

Stop the server.

Stopping the server ends every program running in its sessions.

Without `--server`, the command stops the server that REX_SERVER names, as other commands use it, and otherwise your own server on this machine. In a Rex terminal, REX_SERVER names the server that the terminal belongs to. The command never stops a server on another machine. If `--server` or REX_SERVER names one, it reports an error instead.

With `--if-idle`, the server stops only if it has no sessions and no other client is connected. Otherwise it keeps running, and the command says what is using it and exits with status 1. A client that connects at the same moment is refused, so it never starts work that the stop would end.

With `--discard`, the command also deletes the server's saved sessions once it has stopped, so the next start begins with none. If no server is running, it only deletes them. If the stop is refused, nothing is deleted. Pass `--state-dir` if the server was started with one.

`--if-idle` needs a server recent enough to support it. With an older server, the command leaves the server running and exits with status 4. Without `--if-idle`, `rex server stop` works with a server of any version.

| Flag | Description |
| --- | --- |
| `--discard` | Delete the saved sessions once the server has stopped. |
| `--if-idle` | Stop only if the server has no sessions and no other connected clients. |
| `--state-dir DIR` | Find the saved sessions for `--discard` below DIR. |

### `rex server install [flags] [ssh://[USER@]HOST[:PORT]] [-- SERVER-FLAG...]`

Start your server at boot and keep it running.

Set up your personal Rex server to start on its own. By default, it starts when the machine boots and keeps running while you are logged out.

On Linux, this enables rex.socket, a systemd user unit that starts the server the first time a rex command connects. It also turns on lingering for your account with "loginctl enable-linger". Lingering keeps your systemd user manager, and the server with it, running while you are logged out. No sudo is needed. If you run the rex that a Rex package installed, the package's units are enabled as they are. For any other rex, copies of the units that run that binary are written to ~/.config/systemd/user. Each command run and each file written is printed first.

With `--user`, the server starts when you log in and stops when you log out, and lingering is left as it is.

If a rex command already started a server, that server keeps its sessions. An idle server is stopped so that the unit or service takes over right away. A server with sessions keeps running, and the unit or service starts at the next boot or login instead.

If the system does not let you turn on lingering, the server still starts when you log in, and the command says how an administrator can turn lingering on. If ~/.config/systemd/user already has a rex.service or rex.socket that rex did not write, such as one from the home-manager module, the command leaves it alone and fails.

On Windows, this creates a Windows Service that runs "rex server run" as your account. It starts at boot, shortly after the other automatic services, and keeps running while nobody is signed in and after you sign out. Creating it needs administrator rights, so run the command from a terminal started with "Run as administrator". The command also grants your account the right to log on as a service, which Windows needs to start the service as you, and registers "Rex Server" as a source of the Event Log. It deletes the sign-in entry that `--user` adds, because only one of the two can run your server. Each change is printed first. The server and every program it starts run without administrator rights, as they would after a normal sign-in, even if your account is an administrator.

The command asks for your Windows password, because Windows needs it to start the service as your account while you are not signed in. Windows keeps it with the service. Rex does not keep it. Use the password of your Windows account, not a Windows Hello PIN. If you sign in with a Microsoft account, use the password of that Microsoft account. Without a terminal, the command reads the password from its standard input. If your password changes, run the command again, or the service cannot start at the next boot.

With `--user` on Windows, no administrator rights are needed. The command adds a value named "Rex Server" to HKCU\Software\Microsoft\Windows\CurrentVersion\Run, which runs "rex server start" each time you sign in. It also starts a server now if none is running, and leaves a running server alone. The server stops when you sign out of Windows, and starts again the next time you sign in. If the value is turned off in the Startup tab of Task Manager, the command says so. While the service exists, the command fails. Run "rex server uninstall" first.

On Windows, you can give the server flags after --. The server gets them each time it starts, so use them for settings that must last when the server restarts. For example, "rex server tailscale on" turns Tailscale on only until the server stops. This turns it on at every start:

    `rex server install` -- `--tailscale`

The service runs "rex server run" with the flags, and the "Rex Server" value that `--user` adds runs "rex server start" with them. The command refuses flags that the server would refuse, and then changes nothing. It also refuses `--listen`, because the server must stay on the named pipe where rex commands look for it. Use `--extra-listen` to add another endpoint.

Running the command again without -- keeps the server flags that are already set. Give new flags after -- to replace them, or -- on its own to remove them. A server that is already running keeps its old flags until it restarts.

On Linux, systemd starts the server, so the command takes no server flags there. Set them in a drop-in file instead, with "systemctl `--user` edit rex.service".

Running the command again is safe. Run it again after moving rex.

Linux with systemd and Windows are supported so far. Elsewhere, "rex server start" starts a server that runs until the machine restarts.

With an ssh:// endpoint, the command sets up your server on another machine that you can log in to with ssh, and installs Rex there first. It runs the Rex installer there with `--user`, which puts rex in ~/.local/bin and needs no sudo. As root, or with `--package`, it installs the Rex package for the whole machine instead, through sudo. Then it runs "rex server install" there, connects to the new server through ssh, and adds the machine to your hosts, so that "rex `-S` LABEL" reaches it. Only Linux machines are supported so far.

Each command that runs on the other machine is printed first, and the command asks before each change. `--yes` answers yes to every question. Without a terminal to ask on, `--yes` is required.

| Flag | Description |
| --- | --- |
| `--user` | Start the server when you sign in and stop it when you sign out, instead of at boot. |
| `--json` | Output what the command did as JSON. |
| `--package` | Over ssh, install the Rex package for the whole machine through sudo. |
| `--label LABEL` | Over ssh, add the machine to your hosts as LABEL (default its host name). |
| `--channel NAME` | Over ssh, install from the release channel NAME: stable, preview, or snapshot. |
| `--yes` | Over ssh, answer yes to every question. |

### `rex server uninstall [ssh://[USER@]HOST[:PORT]]`

Stop starting your server on its own.

Undo "rex server install".

On Linux, this disables and stops rex.socket and rex.service, and removes the copies of them that `rex server install` wrote to ~/.config/systemd/user. Stopping the server ends every program running in its sessions. Units that a package installed stay in place, disabled. If ~/.config/systemd/user has a rex.service or rex.socket that rex did not write, such as one from the home-manager module, nothing is disabled or removed.

Lingering stays on, because other services of your account may need it. Turn it off with "loginctl disable-linger".

On Windows, this stops and deletes the Windows Service that `rex server install` created, which ends every program running in its sessions. It also unregisters the "Rex Server" source of the Event Log, unless the service of another account still uses it. Removing the service needs a terminal started with "Run as administrator". Your account keeps the right to log on as a service, because other services may need it.

It also deletes the value named "Rex Server" that `rex server install` `--user` added to HKCU\Software\Microsoft\Windows\CurrentVersion\Run, which needs no administrator rights. A server that the value started keeps running, along with its sessions. Stop it with "rex server stop".

`--user` is accepted so that both commands take the same flags. Uninstall does the same with or without it.

With an ssh:// endpoint, the command runs "rex server uninstall" on that machine instead, after asking. Rex stays installed there, and the machine stays in your hosts. The command says how to remove each.

| Flag | Description |
| --- | --- |
| `--user` | Undo a `rex server install` `--user`. |
| `--json` | Output what the command did as JSON. |
| `--yes` | Over ssh, answer yes to every question. |

### `rex config`

Work with Rex's config file.

Rex reads one configuration file per account, init.lua. It binds keys with rex.bind and takes them away with rex.unbind.

The file is REX_CONFIG when that variable is set. Otherwise it is rex/init.lua in the account's configuration directory, which is $XDG_CONFIG_HOME/rex or ~/.config/rex on macOS and Linux, and %AppData%\rex on Windows.

### `rex config check [PATH]`

Load the config file and report what it found.

Load the config file and report where it is, whether it is there, how many keys it binds and unbinds, how many modes it uses, how many actions it defines, which settings are in force and where each came from, which Program Resume trust rules are in force, and everything loading it had to complain about. Without PATH the account's own init.lua is used.

Only loading happens here. Some mistakes take more than the file to see, such as binding an action that neither this file nor the client has, or unbinding a key that nothing was bound to. Those depend on which client is asking, and "rex keymap" reports them.

The file is loaded by this rex binary, so it is checked against the functions and fields this version of Rex knows. A server running a different version may read it differently. "rex keymap" asks the running server instead.

A trust rule names a command that Rex may start again by itself after a restart. Each rule shows its command, the directories it is limited to if it has any, and how many flags of the original command it keeps and drops. When the file changed part of a rule, the line that changed it is shown next to that part. Rules that are not in force are listed last, each with the line that left it out.

The exit status is 1 when any complaint is an error.

| Flag | Description |
| --- | --- |
| `--json` | Output the result as JSON. |

### `rex config reload`

Make the server read the config file again and tell every client connected to it that their keys may have changed.

The generation counts the times this server has read the file. A client compares it against its own to notice that its keymap is out of date. It advances on every read, including one that failed.

A read that fails keeps the keys of the last one that worked. Only the file's own complaints are reported here. For the ones that take a client's own bindings to find, use "rex keymap".

This runs on the server's own machine, over its local socket. Whoever can edit the file is already there, and a remote caller is refused.

The exit status is 1 when any complaint is an error.

| Flag | Description |
| --- | --- |
| `--json` | Output the result as JSON. |

### `rex keymap`

Show what each key does, as the server resolves it. The answer is the config file's bindings stacked over the bindings the asking client ships with, and under the shortcuts recorded in that client's own settings.

Without `--request` this command sends no layers and declares no actions of its own. The output is then the config file's bindings alone, and a binding that names an action is not checked against any client's list of actions. Pass a client's own request to see the keymap that client receives. If that request sets server_actions, the output lists the same actions the client receives.

Bindings are listed with the top of each key's stack first, which is the order a client tries them in. A binding in a mode is listed as the config file writes it, such as resize/left, and applies only while a client has that mode active. When there are modes, a table of them follows the bindings. The exit status is 1 when any complaint is an error.

| Flag | Description |
| --- | --- |
| `--request FILE` | Send the client.keymap request in FILE ("-" reads stdin). |
| `--json` | Output the response as JSON. |

```sh
rex keymap
rex keymap --request client.json
rex keymap --json | jq '.bindings[] | select(.keys[0] == "cmd+d")'
```

### `rex login-server`

Run the multi-account login server.

The login server runs as root. It identifies each caller, selects an operating system account through the accounts file, and starts or reuses a Rex server for that account. It proxies each accepted connection to the selected server. Clients select an account with https://ACCOUNT@host:port. Tailnet listeners admit every identified caller because the accounts file controls authorization. Local users use sudo to request another account. Send SIGHUP to reload the accounts file. Reloading closes revoked connections but leaves account servers and sessions running.

| Flag | Description |
| --- | --- |
| `--listen ENDPOINT` | Listen on the root-only Unix ENDPOINT (default: unix://RUNTIME-ROOT/login-server.sock). |
| `--extra-listen ENDPOINT` | Also listen on unix, http, tailnet, or tailnet-serve ENDPOINT (repeatable). |
| `--allow-anonymous` | Admit anonymous callers on plain TCP listeners (every connection gets full access). |
| `--tailscaled-socket PATH` | Use the tailscaled LocalAPI socket at PATH (default: platform socket). |
| `--accounts FILE` | Map callers to accounts with the HuJSON FILE (default /etc/rex/accounts.jsonc, or /usr/local/etc/rex/accounts.jsonc on FreeBSD). |
| `--runtime-root DIR` | Keep the socket and accounts/ below DIR (default: $REX_RUNTIME_DIR, else /run/rex, or /var/run/rex on FreeBSD). |
| `--pam` | Open PAM sessions and run PAM account checks (default true; `--pam=false` uses shadow-based checks and no login session). |
| `--pam-service NAME` | Use the PAM policy for service NAME (default rex-login-server). |
| `--log-format FORMAT` | Write server logs as FORMAT: text or json. Defaults to `text`. |

### `rex home`

Show or choose your home server.

Show or choose your home, the server this device follows for hosts and shortcuts.

Your home is this machine unless you choose another. Any Rex server can be a home. A server is not told that it is someone's home, and admits you the same way either way.

Without a command, connect to your home and show what it reports about you. Your choice is kept in home.json in Rex's state directory. Setting REX_HOME chooses a home for one environment and takes precedence over the file. The `--server` option and REX_SERVER choose the server other commands talk to. They do not change your home.

| Flag | Description |
| --- | --- |
| `--json` | Output the home and your identity as JSON. |

### `rex home set ENDPOINT`

Follow ENDPOINT for hosts and shortcuts.

Make the server at ENDPOINT your home. ENDPOINT takes the same forms as `--server`.

The server is asked for its status first. If it cannot be reached, your home is not changed, so a mistyped address or a server that is down never becomes your home. The home is named by `--label`, or by the endpoint's host or socket name if no label is given.

Your choice is written to home.json in Rex's state directory, along with the host ID the server reports. `rex home` uses the host ID to warn you if the address later leads to a different machine. This command fails while REX_HOME is set, because that variable takes precedence over the file.

| Flag | Description |
| --- | --- |
| `--label NAME` | Call the home NAME in output. |

### `rex home unset`

Follow this machine again.

Forget the home you chose, so this machine's own server is your home again. This removes home.json. It succeeds if no home was chosen.

This command fails while REX_HOME is set, because that variable takes precedence over the file.

### `rex hosts`

List and change the hosts you connect to.

List and change your hosts, the other Rex servers you connect to by label.

Your home keeps your hosts, so every device that follows the same home sees the same list. The hosts of this machine's own server always count too, whatever your home is. If a host of this machine and a host of your home have the same label, this machine's host wins.

A new host goes to your home. A change to a host goes to the server the host came from. If your home is away, the change is held on this machine and sent the next time `rex hosts` reaches your home. Until then, the list shows the hosts your home had when it was last reached.

To use a host, give its label to `--server`, as in "rex `-S` studio session ls".

Without a command, list your hosts. The `--server` option and REX_SERVER do not change which servers this command talks to.

| Flag | Description |
| --- | --- |
| `--json` | Output the hosts as JSON. |

### `rex hosts list`

List your hosts.

List the hosts your home keeps, including changes held for it, and the hosts of this machine's own server.

FROM says which server a host came from, and is left out when your home is this machine. SOURCE is the init.lua line that declares a host, "stored" for a host added with `rex hosts`, or "held" for a host not yet sent to your home.

If your home is away, the list shows the hosts it had when it was last reached, and says how long ago that was. Warnings go to standard error.

| Flag | Description |
| --- | --- |
| `--json` | Output the hosts as JSON. |

### `rex hosts add LABEL ENDPOINT...`

Add a host to your home.

Add a host called LABEL, reached at each ENDPOINT in turn. An endpoint takes the same forms as `--server`.

A socket path, such as unix:///tmp/rex.sock, works only on a device where the path exists, such as the local end of an ssh `-L` forward. Other devices skip it and try the next endpoint.

The host goes to your home, so every device that follows your home sees it. No other host of yours may have the same label, ignoring case.

If your home is away, the host is held on this machine and listed at once. It is sent the next time `rex hosts` reaches your home.

| Flag | Description |
| --- | --- |
| `--icon NAME` | Show the icon NAME next to the host. |

### `rex hosts edit LABEL`

Change a host.

Change the host called LABEL, ignoring case. Give at least one option. `--endpoint` replaces all of the host's endpoints, and may be given more than once.

The change goes to the server the host came from: your home, or this machine. Editing a host declared in init.lua stores a host that takes the declaration's place. The line stays in the file, but no longer has an effect.

If the host is your home's and your home is away, the change is held on this machine and sent the next time `rex hosts` reaches your home.

| Flag | Description |
| --- | --- |
| `--label NEW` | Rename the host to NEW. |
| `--endpoint ENDPOINT` | Reach the host at ENDPOINT (repeatable, replaces all endpoints). |
| `--icon NAME` | Show the icon NAME next to the host (empty removes it). |

### `rex hosts remove LABEL`

Remove a host.

Remove the host called LABEL, ignoring case, from the server it came from: your home, or this machine.

Removing a host declared in init.lua hides it. The line stays in the file, but no longer has an effect.

If the host is your home's and your home is away, the removal is held on this machine and sent the next time `rex hosts` reaches your home.

### `rex hosts check [LABEL...]`

Check which hosts can be reached from here.

Try to reach each of your hosts, or only the hosts called LABEL, ignoring case. All hosts are tried at once, and each one has up to `--timeout` to answer.

STATUS is one of:

  reachable                a Rex server answered at ENDPOINT   not reachable from here  nothing answered, but the host may work from another network or device   down                     a machine answered, but not a Rex server

DETAIL says why a host could not be reached. For a reachable host, it says when the address now leads to a different machine than the one you added.

The check succeeds whatever it finds. Commands that connect to a host try the address that answered first.

| Flag | Description |
| --- | --- |
| `--json` | Output the results as JSON. |

### `rex whoami`

Show your identity, server, and Rex location.

| Flag | Description |
| --- | --- |
| `--json` | Output identity, server, and location as JSON. |

## Other

### `rex completion`

Generate shell completion scripts for Rex.

### `rex completion bash`

Generate Bash completion.

Load it with source &lt;(`rex completion bash`), or install it in a bash-completion directory.

### `rex completion zsh`

Generate Zsh completion.

Install it with `rex completion zsh` &gt; `"${fpath[1]}/_rex".`

### `rex completion fish`

Generate Fish completion.

Install it with `rex completion fish` &gt; ~/.config/fish/completions/rex.fish.

### `rex completion powershell`

Generate PowerShell completion.

Add the output of `rex completion powershell` to your PowerShell profile.

### `rex completion nu`

Generate Nushell completion.

Add the output of `rex completion nu` to your config.nu.

### `rex terminfo`

Set up and report Rex's terminal type.

Rex carries its own terminfo entry, xterm-rex, describing what its terminals support.

A terminal claims it wherever this account is set up for it, unless REX_TERM names another entry. Run "rex terminfo setup" once per account, and "rex terminfo status" to see what this machine would decide.

### `rex terminfo status`

Report the TERM a new terminal would be given, and why.

Report the TERM a new terminal would be given, what was examined to decide it, and, when this account is not set up, which command fixes it.

A server claims xterm-rex wherever that is safe and keeps xterm-256color everywhere else. Naming an entry in REX_TERM overrides that and gives every terminal that name, which makes REX_TERM=xterm-256color the off switch. The value "auto" asks for the rule the server already follows.

The report covers the terminfo entry, the ssh client, both guard files, the hosts that have been recorded, and which configuration is responsible for what ssh would actually send.

Nothing of yours is changed and no host is contacted. The one file written is a throwaway copy of Rex's guard, used to ask ssh what that guard would do on its own.

| Flag | Description |
| --- | --- |
| `--json` | Output the report as JSON. |

### `rex terminfo setup`

Install Rex's terminfo entry and ssh guard.

Install xterm-rex where programs find it, and configure ssh so that the name never reaches a host that has never heard of it.

Three things happen. The entry is installed in ~/.terminfo. A guard is written to Rex's configuration directory. One Include line is added at the top of ~/.ssh/config. ssh is then asked what it would send to a host without the entry, and the answer is reported.

If your ssh configuration already includes a guard, as it does when home-manager manages it with Rex's module, the guard and the Include line are skipped, because they would add nothing.

The guard needs OpenSSH 7.8 or later, because an older ssh refuses any configuration that contains it. With an older ssh, only the entry is installed, and the command fails with a message that says why.

With `--system` the entry goes into /usr/share/terminfo and the guard into /etc/ssh/ssh_config.d/50-rex.conf, so that every account on this machine has both, root included. That needs root, and it is what makes programs started through sudo and su find the entry. On FreeBSD, where /etc/ssh/ssh_config reads no other files, it also adds an Include line for the guard's directory to the top of that file.

Run this once per account. Repeating it is harmless.

Two flags are meant for a program that sets an account up on someone's behalf. `--entry-only` installs the entry and leaves ssh configuration alone, which is the half that needs no permission. `--json` reports what the run did as one object instead of the lines a person reads.

Installing the entry is not the whole story. A terminal claims the name once the guard is in place as well, and REX_TERM can name another entry instead. "rex terminfo status" reports what this machine would do.

| Flag | Description |
| --- | --- |
| `--entry-only` | Install the entry alone, for a program that adds the guard later (the name is claimed only once the guard is in place too). |
| `--dry-run` | Report what would change without writing anything. |
| `--system` | Install the entry and the guard for every account on this machine. |
| `--json` | Output what the run did as JSON. |

### `rex terminfo remove`

Remove the ssh guard, leaving the terminfo entry installed.

Remove Rex's ssh guard and the Include line that puts it into effect, so that ssh goes back to forwarding whatever TERM it is given.

With `--system` the machine-wide guard /etc/ssh/ssh_config.d/50-rex.conf goes instead. On FreeBSD, so does the Include line the setup added to /etc/ssh/ssh_config. That needs root.

The terminfo entry stays where it was installed, in both cases. Shells that are already running with TERM=xterm-rex stop working the moment the entry disappears, so there is no command that deletes it. Remove the files by hand if you really want them gone.

`--json` reports what the run did as one object instead of the lines a person reads, in the shape the setup uses.

| Flag | Description |
| --- | --- |
| `--dry-run` | Report what would change without writing anything. |
| `--system` | Remove the guard that every account on this machine shares. |
| `--json` | Output what the run did as JSON. |

### `rex terminfo show`

Print the terminfo source.

Compile it on another machine with: `rex terminfo show` &#124; tic `-x` -

### `rex terminfo host`

Install Rex's terminfo entry on other machines.

Install xterm-rex on a remote host and record that it is there, so that ssh stops announcing xterm-256color to it.

A record is compared, as a whole and ignoring case, against the destination as ssh resolves it, so one machine can be recorded under more than one spelling. Only this account's own guard, written by "rex terminfo setup", lets recorded hosts through.

### `rex terminfo host install DESTINATION [-- SSH_OPTIONS...]`

Install Rex's terminfo entry on a remote host.

Install xterm-rex on DESTINATION over ssh, and record the host so that ssh stops announcing xterm-256color to it.

The entry's source is piped to the remote tic, which compiles it into ~/.terminfo there. Nothing else on the remote host is touched, and no interactive session is started. Options after -- are passed to ssh, so "-- `-p` 2222" and "-- `-J` jump.example.com" work as usual.

The entry lands in the home directory of the account you connect as, while the record is kept per host. Another account on that host will not have the entry. Use "rex terminfo host forget" to undo a record.

What gets recorded is the spelling you typed, because that is what the guard compares against. When your ssh config rewrites it with HostName, that name is recorded as well, because a guard included after your Host blocks sees the rewritten one. Either way, other spellings of the same machine keep the old terminal type until you install to them too.

### `rex terminfo host forget HOST`

Forget that a host has Rex's terminfo entry.

Remove HOST from the hosts file, so that ssh goes back to announcing xterm-256color to it.

Use this when the entry is gone from that host, or when you connect to it as an account that does not have it.

HOST is the spelling that was recorded, in any case. Run "rex terminfo host ls" to see them.

### `rex terminfo host ls`

List the hosts recorded as having Rex's terminfo entry, one per line, in the order they were added.

Each line is compared, as a whole and ignoring case, against the destination as ssh resolves it. One machine can appear under more than one spelling, and each spelling is its own record.

| Flag | Description |
| --- | --- |
| `--json` | Output the list as JSON. |

### `rex skill`

Set up agents to use Rex.

Set up agents such as Claude Code and Codex to use Rex.

Rex installs two things into each agent. A skill teaches the agent how to use the rex command. A hook, in agents that support hooks, tells the agent at the start of each session which Rex session and terminal it is running in. Both get their text from the rex command each time the agent uses them, so upgrading Rex also updates what agents are told.

Run "rex skill setup" once per account, and "rex skill status" to see what is installed.

### `rex skill status`

Report whether Rex's skill and hooks are installed.

Report, for each agent Rex knows, whether the agent was found on this machine and whether Rex's skill and hooks are installed in it. Nothing is changed.

Each item is reported as one of:

  current      installed and up to date   outdated     installed by an older Rex, or edited since   missing      not installed   foreign      a file of the same name that Rex did not install   unreadable   the file could not be read   unsupported  the agent cannot hold the item here

| Flag | Description |
| --- | --- |
| `--project` | Report on the current repository instead of your account. |
| `--json` | Print the report as JSON. |

### `rex skill setup`

Install Rex's skill and hooks into agents.

Install Rex's skill and hooks into the agents found on this machine, or into the agents named with `--agent`. If no agent is found, the skill alone goes into the shared ~/.agents/skills directory that most agents read.

The skill goes into each agent's skill directory. Some agents share a directory, and it is written once. Hooks are added to each agent's settings file, and the rest of the file is left as it was. Some agents ask you to approve a new hook before they run it, and the output says how.

Run this once per account. Running it again is safe, and updates anything an older Rex installed.

Pass `--session-naming` to have agents name the session after their task. A new setup leaves that off, and running setup again keeps the choice already installed unless you pass the flag.

If a skill named rex is already installed and Rex did not install it, it is left alone and reported as a conflict. Use `--force` to replace it.

| Flag | Description |
| --- | --- |
| `--agent AGENT` | Use only AGENT, which is claude, codex, opencode or pi (repeatable). |
| `--project` | Set up the current repository instead of your account. |
| `--dry-run` | Report what would change without changing anything. |
| `--force` | Replace a skill named rex that Rex did not install. |
| `--session-naming` | Tell agents to name the session after their task (omit to keep the installed choice). |
| `--json` | Print the result as JSON. |

### `rex skill remove`

Remove Rex's skill and hooks from agents.

Remove Rex's skill and hooks from every agent Rex knows, or from the agents named with `--agent`. Agents that are no longer installed are included, so nothing Rex installed is left behind.

Only files and hooks that Rex installed are removed, including older copies of the skill in other directories the agent reads. Other skills, hooks and settings are left as they were.

| Flag | Description |
| --- | --- |
| `--agent AGENT` | Use only AGENT, which is claude, codex, opencode or pi (repeatable). |
| `--project` | Remove from the current repository instead of your account. |
| `--dry-run` | Report what would change without changing anything. |
| `--json` | Print the result as JSON. |

### `rex skill show`

Print the guide that Rex's skill gives agents.

An agent with the skill installed reads the guide through the skill. An agent without it can run this command to read the same guide.

### `rex version`

Print version information.

| Flag | Description |
| --- | --- |
| `--json` | Output version information as JSON. |

## Global Options

Every command accepts these.

| Flag | Description |
| --- | --- |
| `--autostart` | Start a missing local server. Defaults to `true`. |
| `-C, --client CLIENT` | Act on client CLIENT, given as a label or ID. |
| `--color WHEN` | Set color WHEN to auto, always, or never. Defaults to `auto`. |
| `-S, --server SERVER` | Connect to SERVER, a host's label or a server address (a value with a port is always an address). |
| `--timeout DURATION` | Limit each connection and nonstreaming request to DURATION. Defaults to `10s`. |
| `-v, --verbose count` | Increase diagnostic verbosity (repeatable). |

