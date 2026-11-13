---
title: "Program Status Protocol"
canonical_url: https://www.superlogical.com/rex/docs/build/program-status
---

# Program Status Protocol (OSC 7501)

A terminal escape sequence that lets a program tell the terminal what it
is doing: idle, working, waiting on the user, finished, or failed, and
why.

The protocol shares state and leaves presentation to the terminal. It
does not say how anything is shown, and it avoids terms tied to
particular GUI elements ("notification", "attention", "focus", etc.).

```
# Terraform has finished planning and is waiting for the user to approve
# the apply. The message decodes to "Apply 3 to add, 1 to change, 0 to destroy?".
ESC ] 7501 ; state=blocked:kind=permission:app=terraform:msg=QXBwbHkgMyB0byBhZGQsIDEgdG8gY2hhbmdlLCAwIHRvIGRlc3Ryb3k/ ESC \
```

**Note:** This is a generic terminal protocol. While it is used for rich functionality
within Rex, the protocol itself has no Superlogical-specific functionality
or language. It fills a broad need within terminal applications.

## Motivation

Long-running work is common in terminals: builds, deployments, package
upgrades, data processing, coding agents. Such a program alternates
between working on its own, waiting on the user, and finishing.
Meanwhile the user is usually doing something else and wants to know
when the work finishes or needs them.

Existing sequences cover only slices of this. OSC 9;4 progress can say
busy or not busy, but not that a program is waiting on the user or what
it is working on. Desktop notifications are one-time events with free-form
text. Tools that show many programs at once fall back to
heuristics such as parsing window titles or matching screen contents, or
to program-specific plugins. [Relationship to other sequences](#relationship-to-other-sequences)
goes into detail.

With this protocol the program that knows its state reports it, and the
terminal keeps a current picture of every program running in it.

## In Rex

When your program adopts the Program Status Protocol in Rex, we show
the current active status in a number of ways today:

- Sessions with completed or blocked tasks show up with an indicator in
  the session picker.
- Tab headers for unfocused tabs show an in-progress spinner and a variety
  symbols for blocked states.
- Lua scripts can react to `terminal.program_status_changed` [events](https://www.superlogical.com/rex/docs/automate/lua-events.md).

In the future, we plan to expand this functionality in many more ways,
such as push notifying our mobile applications, a unified priority inbox
view, and many more.

## Conventions

The key words MUST, MUST NOT, SHOULD, and MAY are used as described in
RFC 2119 and RFC 8174, and only when they appear in capitals.

| Name  | Bytes                                                  |
| ----- | ------------------------------------------------------ |
| `ESC` | `0x1B`                                                 |
| `OSC` | `ESC ]`, that is `0x1B 0x5D`                           |
| `ST`  | `ESC \`, that is `0x1B 0x5C`, or `BEL`, that is `0x07` |

A **terminal** is one window, tab, split, or pane attached to one
pseudo-terminal. Rules that say "the terminal" apply to each one
separately and are implemented by whatever emulates it. A **program**
writes to a terminal. A **report** is one sequence sent by a program. A
**record** is what the terminal stores as a result.

## Syntax

```
OSC 7501 ; pairs ST        report
OSC 7501 ; ? ST            feature detection

pairs    := pair (":" pair)*
pair     := key "=" value
key      := [a-z]+
value    := [A-Za-z0-9_.,+/=-]*
```

- The body is a list of `key=value` pairs separated by `:` and nothing
  else. The value character set excludes `:` and `;`, so nothing needs
  escaping. Whitespace around keys and values is removed.
- A malformed pair (no `=`, empty key, or a byte outside the value set)
  is skipped and the rest of the report is still processed.
- Unknown keys MUST be ignored. This is how the protocol is extended.
- If a key repeats, the last value wins.
- Free-text values (`msg`, `title`) are standard base64 of UTF-8 text.
  Padding is optional. The decoded text MUST NOT contain control
  characters (`U+0000`–`U+001F`, `U+007F`, `U+0080`–`U+009F`), including
  newline or tab. These values are meant to be single line values.
- A report is discarded whole if it exceeds one of the [limits](#limits), if its
  base64 does not decode, or if decoded text contains a control
  character. Nothing from a discarded report is applied.

## Records and ids

A terminal holds a **set of records**, one per id. Each record holds
exactly the keys of the last report that used that id.

```
id      := segment ("/" segment)*
segment := [A-Za-z0-9_.+-]{1,32}
```

- A report with no `id` addresses the **root record**. A program that
  only reports its own state uses the root record and can skip the rest
  of this section.
- **Each report replaces its record completely.** A key missing from the
  report is missing from the record afterwards. A program that wants
  `app` or `title` on a record includes them in every report.
- A report whose `id` does not match this grammar is ignored. Falling
  back to the root record would let a malformed id overwrite it.
- `/` gives records a parent and child relationship: `build/test` is a
  child of `build`, and `build` is a child of the root record. A parent
  does not have to exist. Terminals MUST use
  this relationship for clearing (see [States](#states)) and `app` inheritance
  (see [Keys](#keys)), and MAY use it for grouping. It means nothing else.
- Root and child records exist at the same time. A program can be `idle`
  at its prompt while one of its workers is `blocked`.
- Records belong to the terminal, not to a screen. Switching between the
  primary and alternate screen has no effect on them. A full reset
  (`RIS`) removes every record. A soft reset (`DECSTR`) does not.

## States

The `state` key is required. A report with no `state`, or one the
terminal does not recognize, is ignored.

| `state`   | Meaning | Lifetime |
| --------- | ------- | -------- |
| `idle`    | At rest, waiting for the user's next instruction. | Until replaced or cleared. |
| `working` | Running. May carry `progress`. | Until replaced, cleared, process exit, or next shell prompt. |
| `done`    | Finished a piece of work. The result is ready to look at and the user has not seen it yet. | Until replaced or cleared. Survives process exit and shell prompt. |
| `blocked` | Cannot continue until the user does something. `kind` says what, `msg` says why. May carry `progress`. | Same as `working`. |
| `error`   | Failed and stopped. | Same as `done`. |
| `clear`   | Not a state. Removes the addressed record and every record beneath it. With no `id`, removes every record on the terminal. | |

When the user interrupts or cancels a program, report `idle`. A program
that exits as soon as it finishes SHOULD report `done` or `error` right
before exiting, so a record is left behind for the user to find.

**Lifetime.** Records are tied to events the terminal already sees.
There is no heartbeat, and terminals MUST NOT require re-sending to keep
a record alive. When the process attached to the terminal exits, or a new
shell prompt begins (OSC 133 `A`), the terminal MUST drop `working` and
`blocked` records and MAY drop `idle` ones. `done` and `error` survive
both events. The terminal decides when to stop showing them, for example
when the user returns to the terminal and presses a key.

## Keys

| Key        | Value | Notes |
| ---------- | ----- | ----- |
| `state`    | `idle` \| `working` \| `done` \| `blocked` \| `error` \| `clear` | Required. An unrecognized value causes the whole report to be ignored, so a state added later never turns into `idle` on an older terminal. |
| `id`       | path, see [Records and ids](#records-and-ids) | Absent means the root record. |
| `kind`     | `permission` \| `question` \| `auth` | With `blocked` only, ignored otherwise. `permission`: approval to do something. `question`: the user must type an answer. `auth`: a login, token, or credential. Unrecognized values are treated as absent. |
| `progress` | integer `0` to `100` | With `working` or `blocked`, ignored otherwise. Absent means indeterminate: the program is busy but has no percentage to report. Anything else is treated as absent. |
| `app`      | `[A-Za-z0-9_.+-]{1,32}` | Stable identifier for the program, such as `cargo`, `terraform`, or `claude-code`. A key for grouping, filtering, icons, etc. This is not a label; `title` is the label. A record without `app` takes it from its nearest ancestor that has one. A value outside the character set is treated as absent. |
| `title`    | base64 UTF-8 | Short human-readable label for the record. For programs that report several records. The root record's label is normally the window title. |
| `msg`      | base64 UTF-8 | One human-readable line: what the record is doing, waiting for, or finished. Terminals MAY shorten it and MUST NOT read meaning into it. |

## Feature detection

```
program  → OSC 7501 ; ? ST
terminal → OSC 7501 ; ? : states=idle,working,done,blocked,error : kinds=permission,question,auth ST
```

Detection is optional. Terminals MUST ignore unknown OSCs, so a program
MAY send reports without querying first, for example when it cannot
read replies.

A supporting terminal MUST reply with `?`. It MAY add `states`, the
comma-separated `state` values it accepts (not counting `clear`), and
`kinds`, the `kind` values it accepts.

A reply without `states` means exactly `idle`, `working`, `done`, `blocked`,
and `error`. A reply without `kinds` means exactly `permission`, `question`,
and `auth`. Those lists are fixed and do not change in later revisions.
This is how states and kinds are added: a program that wants a state from a
later revision checks the list and falls back to one that is present. Programs
MUST ignore pairs in the reply that they do not understand.

A program that gets no reply within a time of its choosing treats the
protocol as unsupported. To avoid waiting, send primary device
attributes (`CSI c`) right after the query. Every terminal answers that,
so if its reply arrives first, the protocol is unsupported.

## Security

Everything in a report is untrusted input from a program that already
controls the screen.

- Terminals MUST refuse a report whose decoded `msg` or `title` contains
  a control character, MUST NOT treat either as markup, and SHOULD disarm
  text direction overrides and other invisible formatting characters when
  showing them outside the terminal grid.
- The only bytes a terminal writes back are the feature detection
  reply, which contains nothing from any report. Ids, titles, and
  messages are never sent back, and there is no way to read records.
- Anything a terminal shows from a record SHOULD say which terminal it
  came from, so a program cannot pretend to be a program in another
  terminal.
- A program can change state as fast as it can write. Terminals SHOULD
  rate-limit anything a record causes outside the terminal, such as
  desktop notifications or sounds.

## Limits

Every limit is a hard cap on what a terminal has to store or do for one
report, so a hostile or buggy program cannot make memory grow or cause
unbounded work. Terminals MAY choose lower limits. A report that breaks a
limit is discarded whole. Check every pair before touching any stored
record.

| Item | Limit |
| ---- | ----- |
| Whole sequence, `OSC` through `ST` | 4096 bytes. The largest legal report is under 3300. |
| Key length | 16 bytes |
| `msg` | 2732 bytes encoded, 2048 decoded. Check the encoded size before decoding. |
| `title` | 256 bytes encoded, 192 decoded |
| `app` | 32 bytes |
| `id` | 128 bytes total, 32 per segment, 8 levels deep |
| Records per terminal | 256. Terminals MUST support at least 64. When a report would create a record past the cap, the record that was updated least recently is removed to make room. |

## Relationship to other sequences

**[OSC 9;4](https://conemu.github.io/en/AnsiEscapeCodes.html#ConEmu_specific_OSC) (progress).**
Says only busy, a percentage, or error. It cannot say that a program is
waiting on the user or what it wants, and it carries no message or
identity. It also shares the number 9 with iTerm2's notification sequence,
which has caused garbled output in terminals that know only one of the two.
A program may send both. Terminals MAY map OSC 9;4 to the root record of
this protocol. Because each report replaces its record completely, a
mapped OSC 9;4 would wipe out the `kind` and `msg` of a real report. A
terminal SHOULD stop mapping OSC 9;4 once it has received an OSC 7501
report, until the next full reset.

**OSC 9, [OSC 99](https://sw.kovidgoyal.net/kitty/desktop-notifications/), OSC 777 (desktop notifications).**
A notification is a one-time event. Once it is shown, the terminal has no
record of what is currently true, so it cannot tell that a program is
still waiting or that it recovered. A notification also implies
interrupting the user, which is not always the right behavior. A terminal MAY
produce a notification when a record changes.

**[OSC 133](https://gitlab.freedesktop.org/Per_Bothner/specifications/blob/master/proposals/semantic-prompts.md) (shell integration).**
Marks where prompts and commands begin and end. It is emitted by the
shell, not the program, so it can only say that a command is running or
has finished with an exit code, never what the program is doing or
whether it is stuck.

**OSC 0 and 2 (window title).**
A single free-form string with no structure. Programs that need to show
state today overload it with glyphs and spinners, but this isn't a reliable
machine-readable format for progress.

**[OSC 21337](https://iterm2.com/documentation-session-status.html) (iTerm2 session status) and OSC 9999 (Orca).**
Earlier work on the same idea. They describe presentation, with colors
and indicators, or require JSON parsing, and overall I believe are
not aligned with the right goals.

## Examples

Base64 values are shown decoded in a trailing comment.

### One program

```
OSC 7501 ; state=working:app=brew:msg=SW5zdGFsbGluZyB1cGRhdGVz ST                              # Installing updates
OSC 7501 ; state=blocked:kind=auth:app=brew:msg=UGFzc3dvcmQgcmVxdWlyZWQgdG8gaW5zdGFsbCB1cGRhdGVz ST  # Password required to install updates
OSC 7501 ; state=working:app=brew:msg=SW5zdGFsbGluZyB1cGRhdGVz ST                              # Installing updates
OSC 7501 ; state=done:app=brew:msg=VXBncmFkZWQgMTIgcGFja2FnZXM= ST                             # Upgraded 12 packages
```

Every report repeats `app` because a report replaces its record
completely. The `done` record survives the shell prompt that follows.

### Several records

```
OSC 7501 ; state=working:app=deploy:msg=RGVwbG95aW5nIHYyLjQuMQ== ST                                               # Deploying v2.4.1
OSC 7501 ; state=working:id=us-east:title=VVMgRWFzdA==:progress=40:msg=UHVzaGluZyBpbWFnZQ== ST                    # US East / Pushing image
OSC 7501 ; state=blocked:kind=permission:id=eu-west:title=RVUgV2VzdA==:msg=QXBwcm92ZSBkZXBsb3kgdG8gZXUtd2VzdCAocHJvZHVjdGlvbik/ ST  # EU West / Approve deploy to eu-west (production)?
OSC 7501 ; state=done:id=us-east:title=VVMgRWFzdA==:msg=SGVhbHRoeQ== ST                                           # US East / Healthy
OSC 7501 ; state=clear:id=us-east ST
OSC 7501 ; state=clear:id=eu-west ST
OSC 7501 ; state=done:app=deploy:msg=RGVwbG95ZWQgdG8gMyByZWdpb25z ST                                              # Deployed to 3 regions
```

The region records take `app=deploy` from the root when displayed. While
`eu-west` is blocked the root still says `working`. Both are true, and
the terminal decides which to show.

### A shell function

```sh
status() {
  printf '\e]7501;state=%s:msg=%s\e\\' "$1" "$(printf '%s' "$2" | base64 | tr -d '\n')"
}
status working "Syncing photos"
rsync -a ~/Photos backup:/photos && status done "Photos synced" || status error "rsync failed"
```

## Revision history

| Date       | Revision | Changes |
| ---------- | -------- | ------- |
| 2026-10-10 | 0.4      | Feature detection reply may list supported states and kinds. Say why control characters are refused and what `app` is for. Remove terminfo. |
| 2026-10-07 | 0.3      | Absent `progress` means indeterminate. Programs may send reports without feature detection. |
| 2026-10-06 | 0.2      | Clarify MUST NOT and apply keywords in more places. |
| 2026-09-28 | 0.1      | Initial draft. |
