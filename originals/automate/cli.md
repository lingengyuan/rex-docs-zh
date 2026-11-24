---
title: "The CLI"
canonical_url: https://www.superlogical.com/rex/docs/automate/cli
---

# The CLI

`rex` is the command-line interface to Rex.

`rex` is both an administrative tool for Rex as well as a foundation for
automation. As an administrative tool, it can create sessions, split panes,
list active clients, force disconnect a client, etc. As an automation tool,
it has a complete, powerful Lua scripting interface.

Rex adds `rex` to the `PATH` of every terminal it opens, and sets up the
context so that the CLI already knows what session you're in, which block
you're looking at, and so on.

If `rex` isn't found, see [PATH](#path).

Open a terminal and try it:

```sh
rex ls                 # list your sessions
rex session inspect    # show details of the session you are in
rex block inspect      # show details of the terminal you are typing in
```

Run `rex help` for every command, or `rex help <command>` for the details of
one.

## Taxonomy

Rex organizes work into four kinds of things. Every command acts on one or
more of them.

- A **session** is a group of related work, such as one project. The server
  keeps a session running whether or not anything is looking at it.
- A **window** is a tab within a session. It holds a layout of blocks.
- A **block** is one application in a window. Today that means a terminal.
- A **client** is a program connected to the server, such as the app. Clients
  matter when you ask the app itself to do something, like open its command
  palette.

Each one has an ID that never changes and is never reused, such as
`block:01a10d99-0c06-7795-bf67-798ce4c36a33`. Sessions, windows, blocks, and
clients can also have a label, which is a name you choose and can change.

## Command Targets

With no options, a CLI command acts based on its context. Inside a Rex
terminal that is the terminal's own block and session, so `rex split` splits the terminal you
typed it in. Rex knows where you are from two environment variables it sets
in every terminal:

| Variable | Holds |
| --- | --- |
| `REX_BLOCK` | The ID of the terminal's own block |
| `REX_SERVER` | The address of the server that runs the terminal |

To act somewhere else, specify it with a flag:

| Option | Chooses |
| --- | --- |
| `-s`, `--session` | A session |
| `-w`, `--window` | A window within the session |
| `-b`, `--block` | A block |
| `-C`, `--client` | A client. `REX_CLIENT` sets a default. |
| `-S`, `--server` | A server, by the label of a host from `rex hosts` or by address. `REX_SERVER` sets a default. |

```sh
rex send -s build -w 2 'make test'   # type into window 2 of the "build" session
rex capture -b logs                  # print the screen of the block labeled "logs"
rex -S studio ls                     # list the sessions on the host labeled "studio"
```

Anywhere a command takes a session, you can also pass the full ID of a block.
Rex uses the session that holds the block, so `-s "$REX_BLOCK"` always means
the session of the terminal you're typing in.

### Targets

Rex tries to match a session, window, block, or client target (such as `-C`)
in this order and stops at the first kind of match it finds:

1. A full ID, such as `session:01a10cf3-2655-7e48-9b9c-43dd6612bef5`.
2. A case-insensitive label, such as `build`.
3. A position, counting from one. Windows are numbered in tab order, so `-w 2`
   is the second tab.
4. The end of an ID, at least four characters long, such as `12bef5`. Listing
   commands print these short IDs.

If a target matches more than one thing, the command stops without changing
anything, lists what matched, and exits with status 3:

```
Error: session target "work" is ambiguous
  first   …001234
  second  …00abcd
```

A server is the exception. `-S` takes only a host label or an address, and a
value with a port is always an address.

Labels are convenient at a prompt, but they can change and two things can
share one. In a script that has to keep working, save the ID a command returns
and use that.

## Machine-Readable Output

Most commands print a table meant for reading. Pass `--json` to get JSON
instead, which is stable to parse and includes full IDs:

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

The exit status says how a command ended:

| Status | Meaning |
| --- | --- |
| 0 | The command succeeded |
| 1 | The command failed |
| 2 | The command line was invalid |
| 3 | A target was not found or was ambiguous |
| 4 | The server could not be reached |
| 130 | The command was interrupted |

Commands that wait for a program, such as `rex wait` and `rex run --wait`,
exit with that program's status instead.

## PATH

When Rex opens a terminal, it puts the directory that holds the server's `rex`
executable at the front of `PATH`. It also sets `REX_BIN_DIR` to the same
directory. Your shell's startup files run after that. A startup file that sets
`PATH` to a fixed list leaves `rex` out. One that reorders `PATH` can put a
different copy of `rex` ahead of the one that matches your server.

To check, compare the two:

```sh
echo "$REX_BIN_DIR"
echo "$PATH"
```

If `PATH` doesn't start with `REX_BIN_DIR`, add it back to the front at the
end of your shell's startup file. Adding it to the end of `PATH` instead can
still pick up another copy of `rex` first.

```sh
# ~/.zshrc, or ~/.bashrc
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

NixOS and nix-darwin set `PATH` to a fixed list each time a shell starts. This
affects you if your `PATH` includes `/run/current-system/sw/bin`, even if you
only used Nix to install your shell. Add the same check to your system
configuration so it runs in every interactive `bash` and `zsh`:

```nix
environment.interactiveShellInit = ''
  if [ -n "$REX_BIN_DIR" ]; then
    export PATH="$REX_BIN_DIR:$PATH"
  fi
'';
```

For `fish`, put the `fish` example above in `programs.fish.interactiveShellInit`.
With home-manager, use your shell's init option, such as
`programs.zsh.initContent`. Don't add `REX_BIN_DIR` to `home.sessionPath`.
Outside Rex the variable is empty, which adds an empty entry to `PATH`.
