---
title: "Agents"
canonical_url: https://www.superlogical.com/rex/docs/automate/agent-skill
---

# Agents

Rex ships with a built-in agent skill that enables agents such as Claude Code
or Codex to efficiently open tabs, split panes, read a terminal's screen,
control connected Rex apps, and more.

Even without the skill, a modern agent is smart enough to discover and use the
[`rex` CLI](https://www.superlogical.com/rex/docs/automate/cli.md) to perform tasks, but the skill makes it far more
efficient and is recommended. You'll use fewer tokens and take less time
to achieve the same tasks.

## What Agents Can Do

Here are some examples of what your agent can do with Rex:

| You ask | The agent |
| --- | --- |
| "Open nvim with top in a narrow pane on the right." | Opens a tab with the editor focused and gives `top` the right third. |
| "Start the dev server in another tab and tell me when it's ready." | Starts the server without taking focus, then reads its tab until the server says it's listening. |
| "Run the tests beside you and fix whatever fails." | Runs the tests in a split, waits for them to finish, and reads the failures from the screen before fixing them. |
| "Run `\dt` in the psql pane and tell me what's there." | Types the command into psql, presses Return, and reads the result. |
| "Switch my Mac to this session and make the text bigger." | Asks the app on that Mac to show the session and increase its font size. |
| "Close everything you opened." | Closes the tabs and panes it created and leaves the rest alone. |

Requests that change the app itself, such as switching your Mac to a session,
need the app running with Remote Control turned on in its settings.

## Agent Setup

On macOS, run **Install Rex for Agents** from the command palette. Press
<kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> to open the palette.

From the CLI, `rex skill setup` finds the agents installed on this
machine and sets up each one. If you install new agents in the future,
it is safe to run multiple times.

```
$ rex skill setup
Claude Code
  skill  created      ~/.claude/skills/rex

Codex, OpenCode, Pi
  skill  created      ~/.agents/skills/rex

...

Start a new agent session inside Rex to use it.
```

This installs two things:

- The **skill** teaches the agent the `rex` commands and when to use them.
  It reads its guide from the installed `rex`, so upgrading Rex updates what
  the agent knows without running setup again.
- A **hook** tells the agent, at the start of each session, that it is
  running in Rex and which session and terminal it is in, so it doesn't
  spend time or tokens finding out.

Rex adds its hook to the agent's settings file and leaves the rest of the
file as it was. Running setup again reports what is already current as
`unchanged` and updates anything an older Rex installed.

Rex finds an agent by its configuration directory, such as `~/.claude`, or by
its program on your `PATH`. To set up an agent Rex didn't find, name it with
`--agent`. These are all of the options:

| Option | Does |
| --- | --- |
| `--agent NAME` | Sets up only the named agent, whether or not Rex found it. Repeat it to name several. |
| `--dry-run` | Reports what would change without changing anything. |
| `--project` | Sets up the current repository instead of your account. |
| `--force` | Replaces a skill named `rex` that Rex didn't install. |
| `--session-naming` | Has agents name the session after their task without being asked. Running setup again without it keeps the choice already installed. |
| `--json` | Prints the result as JSON. |

### Approving the Hook

Some agents won't run a new hook until you allow it:

- **Codex** asks before it runs a new or changed hook. Approve Rex's hook
  with `/hooks` in Codex. Until then, Codex skips it.
- **Claude Code** doesn't ask about each hook, but it runs no hooks at all
  until you trust the folder it starts in.

## Supported Agents

`rex skill setup` can set up these agents:

| Agent | `--agent` | Skill | Hook |
| --- | --- | --- | --- |
| Claude Code | `claude` | `~/.claude/skills/rex` | `~/.claude/settings.json` |
| Codex | `codex` | `~/.agents/skills/rex` | `~/.codex/hooks.json` |
| OpenCode | `opencode` | `~/.agents/skills/rex` | Not supported |
| Pi | `pi` | `~/.agents/skills/rex` | Not supported |

Rex follows the environment variables that move an agent's directory, such
as `CLAUDE_CONFIG_DIR` and `CODEX_HOME`.

Any other agent that can run commands in a Rex terminal can use Rex too.
`rex skill show` prints the guide the skill gives agents, so tell the agent
to run it and follow the guide.

We'll continue to add support for more common agents over time.

## How It Works

An agent runs in a Rex terminal like any other program, so it has the same
`REX_SESSION` and `REX_BLOCK`
[environment variables](https://www.superlogical.com/rex/docs/automate/cli.md#command-targets) as your shell. They
tell the agent which session and terminal it is in.

You may be looking at a different session than the agent is in. The agent
chooses where to act from what you say:

- **"Here", "beside you", or nothing at all.** The agent's own session and
  terminal.
- **"The focused pane" or "the current tab".** The pane or tab that has focus
  in the session you're viewing.
- **A name.** The session, tab, or pane with that label. A name always wins
  over the agent's own location and the app's focus.

An agent started outside Rex has no `REX_SESSION`. It lists the sessions with
`rex ls` and works in the one that matches your request, or asks you to
choose when more than one does.

## Removing the Skill

`rex skill remove` removes the skill and hooks from every agent Rex knows,
including agents you've since uninstalled:

```sh
rex skill remove
```

Only what Rex installed is removed, including copies of the skill an older
Rex left in other directories the agent reads. Other skills, other hooks, and
the rest of each settings file stay as they were. `--agent`, `--project`, and
`--dry-run` work the same as for `rex skill setup`.

Codex remembers which hooks you approved by their place in `hooks.json`. If
removing or updating Rex's hook moves the hooks after it, Codex asks you to
approve those again, and Rex says so in its output.

## Debugging

`rex skill status` reports what is installed in each agent, without changing
anything:

```
$ rex skill status
Claude Code (found)
  skill  current      ~/.claude/skills/rex
  hook   current      ~/.claude/settings.json

Codex (found)
  skill  outdated     ~/.agents/skills/rex
  hook   current      ~/.codex/hooks.json
...

Run "rex skill setup" to install or update the skill.
```

| State | Meaning |
| --- | --- |
| `current` | Installed and up to date. |
| `outdated` | Installed by an older Rex, or edited since. `rex skill setup` updates it. |
| `missing` | Not installed. |
| `foreign` | A skill named `rex` that Rex didn't install. `rex skill setup` leaves it alone unless you pass `--force`. |
| `unreadable` | The file couldn't be read. |
| `unsupported` | The agent can't hold this item, such as a hook in an agent without hooks. |

If an agent doesn't seem to know it's in Rex, check that its session started
after `rex skill setup` ran, since the hook only runs when a session starts.
In Codex, check that the hook is approved with `/hooks`. In Claude Code,
check that you trusted the folder.
