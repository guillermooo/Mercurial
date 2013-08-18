<a href='http://www.pledgie.com/campaigns/19374'><img alt='Click here to lend your support to: Mercurial and make a donation at www.pledgie.com !' src='http://www.pledgie.com/campaigns/19374.png?skin_name=chrome' border='0' /></a>

# Mercurial (Sublime Text Package)

Use Mercurial from Sublime Text 3.


## Requirements

* Mercurial command server (Mercurial 1.9 or above)


## Installation

- [Download](https://bitbucket.org/guillermooo/mercurial/downloads/Mercurial.sublime-package)
- Install to *Installed Packages*


## Configuration

These options can be set in **Preferences | Settings - User**.

`packages.sublime_hg.hg_exe`

By default, the executable name for Mercurial is `hg`. If you need to
use a different one, such as `hg.bat`, change this option.

Example:

```json
{
  "packages.sublime_hg.hg_exe": "hg.bat"
}
```

`packages.sublime_hg.terminal`

Determines the terminal emulator to be used in Linux. Some commands, such
as *serve*, need this information to work.

`packages.sublime_hg.extensions`

A list of Mercurial extension names. Commands belonging to these extensions
will show up in the Mercurial quick panel along with built-in Mercurial
commands.


## How to Use

Mercurial can be used in two ways:

- Through a *menu* (`show_mercurial_menu` command).
- Through a *command-line* interface (`show_mercurial_cli` command).

Regardless of the method used, Mercurial ultimately talks to the Mercurial
command server. The command-line interface is the more flexible option, but
some operations might be quicker through the menu.

By default, you have to follow these steps to use Mercurial:

1. Open the Command Palette (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>) and look for `Mercurial`.
2. Select option
3. Select Mercurial command (or type in command line)

It is however **recommended to assign** `show_sublime_hg_cli` and
`show_sublime_hg_menu` their own **key bindings**.

For example:

```json
{ "keys": ["ctrl+k", "ctrl+k"], "command": "show_mercurial_menu" },
{ "keys": ["ctrl+shift+k"], "command": "show_mercurial_cli" },
```

## Restarting the Current Server

The Mercurial command server will not detect changes to the repository made
from the outside (perhaps from a command line) while it is running. To restart
the current server so that external changes are picked up, select
*Kill Current Server* from the command palette.


## Tab Completion

While in the command-line, top level commands will be autocompleted when you
press <kbd>Tab</kbd>.


## Quick Actions

In some situations, you can perform quick actions.

### In Log Reports

To **diff two revisions**, select two revision numbers and press
<kbd>Ctrl</kbd>+<kbd>Enter</kbd>.

To **update to a revision number**, select a revision number and
press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>Enter</kbd>.


Donations
=========

You can tip me through Gittip ([guillermooo](http://www.gittip.com/guillermooo/)) or Pledgie (see top).
	