from collections import namedtuple


class CommandNotFoundError(Exception):
    pass


class AmbiguousCommandError(Exception):
    pass


cmd_data = namedtuple('cmd_data','invocations prompt enabled syntax_file help flags preferred_output')

# Flags
RUN_IN_OWN_CONSOLE = 0x01

HG_COMMANDS = {}


HG_COMMANDS['default'] = {
    'commit': cmd_data(
                    invocations={
                        'commit...': 'commit -m "%(input)s"',
                        'commit... (this file)': 'commit "%(file_name)s" -m "%(input)s"',
                    },
                    prompt='Commit message:',
                    enabled=True,
                    syntax_file='',
                    help='commit the specified files or all outstanding changes',
                    flags=0,
                    preferred_output='view',
                    ),
    'init': cmd_data(
                    invocations={
                        'init': 'init',
                    },
                    prompt='',
                    enabled=True,
                    syntax_file='',
                    help='create a new repository in the given directory',
                    flags=RUN_IN_OWN_CONSOLE,
                    preferred_output='view',
                    ),
    'add': cmd_data(
                    invocations={
                        'add (this file)': 'add "%(file_name)s"',
                        'add': 'add',
                   },
                    prompt='',
                    enabled=True,
                    syntax_file='',
                    help='add the specified files on the next commit',
                    flags=0,
                    preferred_output='view',
                    ),
    'addremove': cmd_data(
                    invocations={},
                    prompt='',
                    enabled=True,
                    syntax_file='',
                    help='add all new files, delete all missing files',
                    flags=0,
                    preferred_output='view',
                    ),
    'annotate': cmd_data(
                    invocations={
                        'annotate | blame (this file)': 'annotate "%(file_name)s"',
                        'annotate | blame [full] (this file)': 'annotate -nudq "%(file_name)s"',
                   },
                    prompt='',
                    enabled=True,
                    syntax_file='Packages/Mercurial/Support/Mercurial Annotate.hidden-tmLanguage',
                    help='show changeset information by line for each file',
                    flags=0,
                    preferred_output='view',
                    ),
    'bookmark': cmd_data(
                    invocations={
                        'bookmark... (parent revision)': 'bookmark "%(input)s"',
                    },
                    prompt='Bookmark name:',
                    enabled=True,
                    syntax_file='',
                    help='track a line of development with movable markers',
                    flags=0,
                    preferred_output='panel',
                    ),
    'bookmarks': cmd_data(
                    invocations={},
                    prompt='',
                    enabled=True,
                    syntax_file='',
                    help='track a line of development with movable markers',
                    flags=0,
                    preferred_output='panel',
                    ),
    'branch': cmd_data(
                    invocations={},
                    prompt='',
                    enabled=True,
                    syntax_file='',
                    help='set or show the current branch name',
                    flags=0,
                    preferred_output='panel',
                    ),
    'branches': cmd_data(
                    invocations={},
                    prompt='',
                    enabled=True,
                    syntax_file='',
                    help='list repository named branches',
                    flags=0,
                    preferred_output='panel',
                    ),
    'diff': cmd_data(
                    invocations={
                        'diff': 'diff',
                        'diff (this file)': 'diff "%(file_name)s"',
                        'diff [stat]': 'diff --stat',
                        'diff [stat] (this file)': 'diff "%(file_name)s" --stat',
                    },
                    prompt='',
                    enabled=True,
                    syntax_file='Packages/Diff/Diff.tmLanguage',
                    help='diff repository (or selected files)',
                    flags=0,
                    preferred_output='panel',
                    ),
    'forget': cmd_data(
                    invocations={
                        'forget (this file)': 'forget "%(file_name)s"',
                    },
                    prompt='',
                    enabled=True,
                    syntax_file='',
                    help='forget the specified files on the next commit',
                    flags=0,
                    preferred_output='panel',
                    ),
    'grep': cmd_data(
                    invocations={
                        'grep (tip)...': 'grep "%(input)s" -nur tip',
                        'grep (tip)... [case insensitive]': 'grep "%(input)s" --ignore-case -nur tip',
                        'grep (latest 5)...': 'grep "%(input)s" -nur "-5:tip"',
                        'grep (latest 5)... [case insensitive]': 'grep "%(input)s" --ignore-case -nur "-5:tip"',
                        'grep (latest 10)...': 'grep "%(input)s" -nur "-10:tip"',
                        'grep (latest 10)... [case insensitive]': 'grep "%(input)s" --ignore-case -nur "-10:tip"',
                        'grep (all)...': 'grep "%(input)s" -nu',
                        'grep (all)... [case insensitive]': 'grep "%(input)s" --ignore-case -nu',
                    },
                    prompt='Pattern (grep):',
                    enabled=True,
                    syntax_file='',
                    help='search for a pattern in specified files and revisions',
                    flags=0,
                    preferred_output='view',
                    ),
    'identify': cmd_data(
                    invocations={
                        'identify...': 'identify --num --id --branch --tags --bookmarks --rev %(input)s',
                        'identify': 'identify --num --id --branch --tags --bookmarks',
                    },
                    prompt='Revision:',
                    enabled=True,
                    syntax_file='',
                    help='identify the working copy or specified revision',
                    flags=0,
                    preferred_output='panel',
                    ),
    'heads': cmd_data(
                    invocations={},
                    prompt='',
                    enabled=True,
                    syntax_file='',
                    help='show current repository heads or show branch heads',
                    flags=0,
                    preferred_output='panel',
                    ),
    'help': cmd_data(
                    invocations={
                        'help...': 'help "%(input)s"',
                        'help': 'help',
                        },
                    prompt='Help topic:',
                    enabled=True,
                    syntax_file='',
                    help='show help for a given topic or a help overview',
                    flags=0,
                    preferred_output='view',
                    ),
    'incoming': cmd_data(
                    invocations={
                        'incoming...': 'incoming %(input)s',
                        'incoming': 'incoming',
                    },
                    prompt='Incoming source:',
                    enabled=True,
                    syntax_file='',
                    help='show new changesets found in source',
                    flags=RUN_IN_OWN_CONSOLE,
                    preferred_output='view',
                    ),
    'locate': cmd_data(
                    invocations={
                        'locate...': 'locate "%(input)s"'
                    },
                    prompt='Pattern:',
                    enabled=True,
                    syntax_file='',
                    help='locate files matching specific patterns',
                    flags=0,
                    preferred_output='panel',
                    ),
    'log': cmd_data(
                    invocations={
                        'log (this file)': 'log --limit 30 --graph "%(file_name)s"',
                        "log (10 revs)": "log --graph --limit 10",
                        "log + (20 revs)": "log --graph --limit 20",
                        "log ++ (30 revs)": "log --graph --limit 30",
                        'log (this file) [stat]': 'log --limit 15 --graph --stat"%(file_name)s"',
                        'log (20 revs) [stat]': 'log --limit 20 --graph --stat"%(file_name)s"',
                    },
                    prompt='',
                    enabled=True,
                    syntax_file='Packages/Mercurial/Support/Mercurial Log.hidden-tmLanguage',
                    help='show revision history of entire repository or files',
                    flags=0,
                    preferred_output='view',
                    ),
    'manifest': cmd_data(
                    invocations={
                        'manifest...': 'manifest --rev %(input)s',
                        'manifest': 'manifest',
                    },
                    prompt='Revision:',
                    enabled=True,
                    syntax_file='',
                    help='output the current or given revision of the project manifest',
                    flags=0,
                    preferred_output='panel',
                    ),
    'merge': cmd_data(
                    invocations={
                        'merge...': 'merge "%(input)s"',
                        'merge': 'merge',
                    },
                    prompt='',
                    enabled=True,
                    syntax_file='',
                    help='merge working directory with another revision',
                    flags=0,
                    preferred_output='view',
                    ),
    'outgoing': cmd_data(
                    invocations={
                        'outgoing...': 'outgoing %(input)s',
                        'outgoing': 'outgoing',
                    },
                    prompt='Outgoing target:',
                    enabled=True,
                    syntax_file='Packages/Mercurial/Support/Mercurial Log.hidden-tmLanguage',
                    help='show changesets not found in the destination',
                    flags=RUN_IN_OWN_CONSOLE,
                    preferred_output='view',
                    ),
    'parents': cmd_data(
                    invocations={},
                    prompt='',
                    enabled=True,
                    syntax_file='',
                    help='show the parents of the working directory or revision',
                    flags=0,
                    preferred_output='panel',
                    ),
    'paths': cmd_data(
                    invocations={},
                    prompt='',
                    enabled=True,
                    syntax_file='',
                    help='show aliases for remote repositories',
                    flags=0,
                    preferred_output='panel',
                    ),
    'pull': cmd_data(
                    invocations={
                        'pull...': 'pull %(input)s',
                        'pull': 'pull',
                    },
                    prompt='Pull source:',
                    enabled=True,
                    syntax_file='',
                    help='pull changes from the specified source',
                    flags=RUN_IN_OWN_CONSOLE,
                    preferred_output='view',
                    ),
    "push": cmd_data(
                    invocations={
                        'push...': 'push %(input)s',
                        'push': 'push',
                    },
                    prompt="Push target:",
                    enabled=True,
                    syntax_file='',
                    help='push changes to the specified destination',
                    flags=RUN_IN_OWN_CONSOLE,
                    preferred_output='view',
                    ),
    "recover": cmd_data(
                    invocations={},
                    prompt='',
                    enabled=True,
                    syntax_file='',
                    help='roll back an interrupted transaction',
                    flags=0,
                    preferred_output='view',
                    ),
    "remove": cmd_data(
                    invocations={
                        'remove (this file)': 'remove "%(file_name)s"',
                    },
                    prompt='',
                    enabled=True,
                    syntax_file='',
                    help='remove the specified files on the next commit',
                    flags=0,
                    preferred_output='view',
                    ),
    "rename": cmd_data(
                    invocations={
                        'rename... (this file)': 'rename "%(file_name)s" "%(input)s"',
                    },
                    prompt="New name:",
                    enabled=True,
                    syntax_file='',
                    help='rename files; equivalent of copy + remove',
                    flags=0,
                    preferred_output='panel',
                    ),
    "resolve": cmd_data(
                    invocations={
                        'resolve (this file)': 'resolve "%(file_name)s"',
                    },
                    prompt='',
                    enabled=True,
                    syntax_file='',
                    help='redo merges or set/view the merge status of files',
                    flags=0,
                    preferred_output='view',
                    ),
    "revert": cmd_data(
                    invocations={
                        'revert (this file)': 'revert "%(file_name)s"',
                    },
                    prompt='',
                    enabled=True,
                    syntax_file='',
                    help='restore files to their checkout state',
                    flags=0,
                    preferred_output='panel',
                    ),
    "rollback": cmd_data(
                    invocations={},
                    prompt='',
                    enabled=True,
                    syntax_file='',
                    help='roll back the last transaction (dangerous)',
                    flags=0,
                    preferred_output='view',
                    ),
    "root": cmd_data(
                    invocations={},
                    prompt='',
                    enabled=True,
                    syntax_file='',
                    help='print the root (top) of the current working directory',
                    flags=0,
                    preferred_output='panel',
                    ),
    "showconfig": cmd_data(
                    invocations={},
                    prompt='',
                    enabled=True,
                    syntax_file='',
                    help='show combined config settings from all hgrc files',
                    flags=0,
                    preferred_output='panel',
                    ),
    "status": cmd_data(
                    invocations={
                        'status (this file)': 'status "%(file_name)s"',
                        'status': 'status',
                    },
                    prompt='',
                    enabled=True,
                    syntax_file='Packages/Mercurial/Support/Mercurial Status Report.hidden-tmLanguage',
                    help='show changed files in the working directory',
                    flags=0,
                    preferred_output='panel',
                    ),
    "summary": cmd_data(
                    invocations={},
                    prompt='',
                    enabled=True,
                    syntax_file='',
                    help='summarize working directory state',
                    flags=0,
                    preferred_output='panel',
                    ),
    "tag": cmd_data(
                    invocations={
                        'tag...': 'tag "%(input)s"',
                    },
                    prompt="Tag name:",
                    enabled=True,
                    syntax_file='',
                    help='add one or more tags for the current or given revision',
                    flags=0,
                    preferred_output='panel',
                    ),
    "tags": cmd_data(
                    invocations={},
                    prompt='',
                    enabled=True,
                    syntax_file='',
                    help='list repository tags',
                    flags=0,
                    preferred_output='panel',
                    ),
    "tip": cmd_data(
                    invocations={},
                    prompt='',
                    enabled=True,
                    syntax_file='',
                    help='show the tip revision',
                    flags=0,
                    preferred_output='panel',
                    ),
    "update": cmd_data(
                    invocations={
                        'update...': 'update "%(input)s"',
                        'update': 'update',
                    },
                    prompt="Branch:",
                    enabled=True,
                    syntax_file='',
                    help='update working directory (or switch revisions)',
                    flags=0,
                    preferred_output='panel',
                    ),
    "verify": cmd_data(
                    invocations={},
                    prompt='',
                    enabled=True,
                    syntax_file='',
                    help='verify the integrity of the repository',
                    flags=0,
                    preferred_output='panel',
                    ),
    "version": cmd_data(
                    invocations={},
                    prompt='',
                    enabled=True,
                    syntax_file='',
                    help='output version and copyright information',
                    flags=0,
                    preferred_output='panel',
                    ),
    "serve": cmd_data(
                    invocations={
                        "serve": "serve"
                    },
                    prompt='',
                    enabled=True,
                    syntax_file='',
                    help='start stand-alone webserver',
                    flags=RUN_IN_OWN_CONSOLE,
                    preferred_output='panel',
                    ),
    "init": cmd_data(
                    invocations={
                        "init (this file's directory)": "init"
                    },
                    prompt='',
                    enabled=True,
                    syntax_file='',
                    help='create a new repository in the given directory',
                    flags=RUN_IN_OWN_CONSOLE,
                    preferred_output='panel',
                    ),
}

# At some point we'll let the user choose whether to load extensions.
HG_COMMANDS['mq'] = {
        "qapplied": cmd_data(
                        invocations={
                            'qapplied': 'qapplied -s',
                       },
                        prompt='',
                        enabled=True,
                        syntax_file='',
                        help='print the patches already applied',
                        flags=0,
                        preferred_output='panel',
                        ),
        "qdiff": cmd_data(
                        invocations={
                            'qdiff': 'qdiff',
                            'qdiff [stat]': 'qdiff --stat',
                        },
                        prompt='',
                        enabled=True,
                        syntax_file='Packages/Diff/Diff.tmLanguage',
                        help='diff of the current patch and subsequent modifications',
                        flags=0,
                        preferred_output='view',
                        ),
        "qgoto": cmd_data(
                        invocations={
                            'qgoto...':'qgoto "%(input)s"',
                        },
                        prompt="Patch name:",
                        enabled=True,
                        syntax_file='',
                        help='push or pop patches until named patch is at top of stack',
                        flags=0,
                        preferred_output='panel',
                        ),
        "qheader": cmd_data(
                        invocations={
                            'qheader...': 'qheader "%(input)s"',
                            'qheader': 'qheader',
                       },
                        prompt="Patch name:",
                        enabled=True,
                        syntax_file='',
                        help='print the header of the topmost or specified patch',
                        flags=0,
                        preferred_output='panel',
                        ),
        "qnext": cmd_data(
                        invocations={
                            'qnext': 'qnext -s',
                        },
                        prompt='',
                        enabled=True,
                        syntax_file='',
                        help='print the name of the next pushable patch',
                        flags=0,
                        preferred_output='panel',
                        ),
        "qpop": cmd_data(
                        invocations={},
                        prompt='',
                        enabled=True,
                        syntax_file='',
                        help='pop the current patch off the stack',
                        flags=0,
                        preferred_output='panel',
                        ),
        "qprev": cmd_data(
                        invocations={
                            'qprev': 'qprev -s',
                        },
                        prompt='',
                        enabled=True,
                        syntax_file='',
                        help='print the name of the preceding applied patch',
                        flags=0,
                        preferred_output='panel',
                        ),
        "qpush": cmd_data(
                        invocations={},
                        prompt='',
                        enabled=True,
                        syntax_file='',
                        help='push the next patch onto the stack',
                        flags=0,
                        preferred_output='panel',
                        ),
        "qrefresh": cmd_data(
                        invocations={
                            'qrefresh... (EDIT commit message': 'qrefresh -e',
                            'qrefresh... (NEW commit message)': 'qrefresh -m "%(input)s"',
                            'qrefresh': 'qrefresh',
                        },
                        prompt='Commit message:',
                        enabled=True,
                        syntax_file='',
                        help='update the current patch',
                        flags=0,
                        preferred_output='panel',
                        ),
        "qfold": cmd_data(
                        invocations={
                            'qfold...': 'qfold "%(input)s"'
                        },
                        prompt='Patch name:',
                        enabled=True,
                        syntax_file='',
                        help='fold the named patches into the current patch',
                        flags=0,
                        preferred_output='panel',
                        ),
        "qseries": cmd_data(
                        invocations={
                            'qseries': 'qseries -s',
                        },
                        prompt='',
                        enabled=True,
                        syntax_file='',
                        help='print the entire series file',
                        flags=0,
                        preferred_output='panel',
                        ),
        "qfinish": cmd_data(
                        invocations={
                            'qfinish...': 'qfinish "%(input)s"',
                        },
                        prompt='Patch name:',
                        enabled=True,
                        syntax_file='',
                        help='move applied patches into repository history',
                        flags=0,
                        preferred_output='panel',
                        ),
        "qnew": cmd_data(
                        invocations={
                            'qnew...': 'qnew "%(input)s.patch"',
                        },
                        prompt='Patch name (no extension):',
                        enabled=True,
                        syntax_file='',
                        help='create a new patch',
                        flags=0,
                        preferred_output='panel',
                        ),
        "qdelete": cmd_data(
                        invocations={
                            'qdelete...': 'qdelete "%(input)s"',
                        },
                        prompt='Patch name:',
                        enabled=True,
                        syntax_file='',
                        help='remove patches from queue',
                        flags=0,
                        preferred_output='panel',
                        ),
        "qtop": cmd_data(
                        invocations={
                            'qtop': 'qtop -s',
                        },
                        prompt='',
                        enabled=True,
                        syntax_file='',
                        help='print the name of the current patch',
                        flags=0,
                        preferred_output='panel',
                        ),
        "qunapplied": cmd_data(
                        invocations={},
                        prompt='',
                        enabled=True,
                        syntax_file='',
                        help='print the patches not yet applied',
                        flags=0,
                        preferred_output='panel',
                        ),
    }


def format_for_display(extension):
    all_cmds = []
    for name, cmd_data in HG_COMMANDS[extension].items():
        if cmd_data.invocations:
            for display_name, invocation in cmd_data.invocations.items():
                all_cmds.append([display_name, cmd_data.help])
        else:
            all_cmds.append([name, cmd_data.help])

    return sorted(all_cmds, key=lambda x: x[0])


def find_cmd(extensions, search_term):
    candidates = []
    extensions.insert(0, 'default')
    for ext in extensions:
        cmds = HG_COMMANDS[ext]
        for name, cmd_data in cmds.items():
            if search_term in cmd_data.invocations:
                return cmd_data.invocations[search_term], cmd_data
                break
            elif search_term == name:
                return name, cmd_data
                break
            elif name.startswith(search_term):
                candidates.append((name, cmd_data))

    if len(candidates) == 1:
        return candidates[0]

    if len(candidates) > 1:
        raise AmbiguousCommandError
    else:
        raise CommandNotFoundError

def get_commands_by_ext(extensions):
    cmds = []
    for ext in extensions:
        if not ext.lower() == 'default':
            cmds.extend(format_for_display(ext))
    # Make sure we return at least 'default' commands.
    cmds = format_for_display('default') + cmds
    return cmds


HG_COMMANDS_AND_SHORT_HELP = format_for_display("default")
HG_COMMANDS_LIST = [x.replace('.', '') for x in HG_COMMANDS if ' ' not in x]
HG_COMMANDS_LIST = list(sorted(set(HG_COMMANDS_LIST)))
