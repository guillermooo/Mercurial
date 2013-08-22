import sublime
import sublime_plugin

import threading
import functools
import subprocess
import os
import re
import logging

from Mercurial.shglib import commands
from Mercurial.shglib import utils
from Mercurial.shglib.utils import status
from Mercurial.shglib.commands import AmbiguousCommandError
from Mercurial.shglib.commands import CommandNotFoundError
from Mercurial.shglib.commands import find_cmd
from Mercurial.shglib.commands import get_commands_by_ext
from Mercurial.shglib.commands import HG_COMMANDS_LIST
from Mercurial.shglib.commands import RUN_IN_OWN_CONSOLE
from Mercurial.shglib.parsing import CommandLexer


# todo: use hg keywords
VERSION = '13.0.0'


CMD_LINE_SYNTAX = 'Packages/Mercurial/Support/SublimeHg Command Line.hidden-tmLanguage'


running_servers = utils.HgServers()
recent_file_name = None


def plugin_loaded():
    logging.basicConfig(level=logging.ERROR)


def hg(server, cmd_string):
    """Runs a Mercurial command through the given command server.
    """
    server.run_command(cmd_string)
    text, exit_code = server.receive_data()
    return text, exit_code


class KillHgServerCommand(sublime_plugin.TextCommand):
    """Shut down the server for the current file if it's running.

    The Mercurial command server does not detect state changes in the
    repo originating outside the command server itself (such as from a
    separate command line). This command makes it easy to restart the
    server so that the newest changes are picked up.
    """

    def run(self, edit):
        try:
            fn = self.view.file_name()
            if not fn:
                status("File does not exist. Aborting.")
                return
            repo = utils.find_repo_root(fn)
        # XXX: Will swallow the same error for the utils. call.
        except AttributeError:
            status("No server found for this file: {0}".format(fn))
            return

        running_servers.shut_down(repo)
        status("Killed server for '{0}'".format(repo))


def run_in_console(hg_bin, cmd, encoding=None):
    if sublime.platform() == 'windows':
        cmd_str = '{0} {1} && pause'.format(hg_bin, cmd)
        subprocess.Popen(['cmd.exe', '/c', cmd_str,])
    elif sublime.platform() == 'linux':
        # Apparently it isn't possible to retrieve the preferred terminal in a general way for
        # different distros:
        # http://unix.stackexchange.com/questions/32547/how-to-launch-an-application-with-default-terminal-emulator-on-ubuntu
        term = utils.get_preferred_terminal()
        if term:
            cmd_str = "bash -c '{0} {1};read'".format(hg_bin, cmd)
            subprocess.Popen([term, '-e', cmd_str])
        else:
            raise EnvironmentError("No terminal found."
                                   "You might want to add packages.sublime_hg.terminal "
                                   "to your settings.")
    elif sublime.platform() == 'osx':
        cmd_str = "{0} {1}".format(hg_bin, cmd)
        osa = "tell application \"Terminal\"\ndo script \"cd '{0}' && {1}\"\nactivate\nend tell".format(os.getcwd(), cmd_str)
        subprocess.Popen(["osascript", "-e", osa])
    else:
        raise NotImplementedError("Cannot run consoles on your OS: {0}. "
                                  "Not implemented.".format(sublime.platform()))


def escape(s, c, esc='\\\\'):
    # FIXME: won't escape \\" and such correctly.
    pat = "(?<!%s)%s" % (esc, c)
    r = re.compile(pat)
    return r.sub(esc + c, s)


class CommandRunnerWorker(threading.Thread):
    """Runs the Mercurial command and reports the output.
    """
    def __init__(self, command_server, command, view, window,
                 fname, display_name, append=False):
        threading.Thread.__init__(self)
        self.command_server = command_server
        self.command = command
        self.view = view
        self.window = window
        self.fname = fname
        extensions = view.settings().get('packages.sublime_hg.extensions', [])
        self.command_data = find_cmd(extensions, display_name)[1]
        self.append = append

    def run(self):
        # The requested command interacts with remote repository or is potentially
        # long-running. We run it in its own console so it can be killed easily
        # by the user. Also, they have a chance to enter credentials if necessary.
        if utils.is_flag_set(self.command_data.flags, RUN_IN_OWN_CONSOLE):
            # FIXME: what if self.fname is None?
            target_dir = (self.fname if os.path.isdir(self.fname)
                                     else os.path.dirname(self.fname))
            with utils.pushd(target_dir):
                try:
                    run_in_console(self.command_server.hg_bin, self.command,
                                   self.command_server.encoding)
                except (EnvironmentError, NotImplementedError) as e:
                    sublime.status_message("Mercurial: Error")
                    logging.info(e.message)
            return

        # Run the requested command through the command server.
        try:
            data, exit_code = hg(self.command_server, self.command)
            sublime.set_timeout(functools.partial(self.show_output, data, exit_code), 0)
        except UnicodeDecodeError as e:
            print ("Mercurial: Can't handle command string characters.")
            print (e)
        except Exception as e:
            print ("Mercurial: Error while trying to run the command server.")
            print ("*" * 80)
            print (e)
            print ("*" * 80)

    def show_output(self, data, exit_code):
        # If we're appending to the console, do it even if there's no data.
        if data or self.append:
            self.create_output(data, exit_code)

            # Make sure we know when to restore the cmdline later.
            global recent_file_name
            recent_file_name = self.view.file_name()
        # Just give feedback if we're running commands from the command
        # palette and there's no data.
        else:
            sublime.status_message("Mercurial - <No output.>")

    def create_output(self, data, exit_code):
        # Output to the console or to a separate buffer.
        if not self.append:
            p = self.window.new_file()
            p.run_command('append', {'characters': data})
            p.set_name("Mercurial - Output")
            p.set_scratch(True)
            p.settings().set('gutter', False)
            if self.command_data and self.command_data.syntax_file:
                p.settings().set('gutter', True)
                p.set_syntax_file(self.command_data.syntax_file)
            p.sel().clear()
            p.sel().add(sublime.Region(0, 0))
        else:
            p = self.view
            p.run_command('append', {'characters': '\n' + data + "\n> "})
            p.show(self.view.size())


class HgCommandRunnerCommand(sublime_plugin.TextCommand):
    def run(self, edit, cmd=None, display_name=None, cwd=None, append=False):
        self.display_name = display_name
        self.cwd = cwd
        self.append = append
        try:
            self.on_done(cmd)
        except CommandNotFoundError:
            # This will happen when we cannot find an unambiguous command or
            # any command at all.
            sublime.status_message("Mercurial: Command not found.")
        except AmbiguousCommandError:
            sublime.status_message("Mercurial: Ambiguous command.")

    def on_done(self, s):
        # FIXME: won't work with short aliases like st, etc.
        self.display_name = self.display_name or s.split(' ')[0]

        try:
            hgs = running_servers[self.cwd]
        except utils.NoRepositoryFoundError as e:
            msg = "Mercurial: %s" % e
            print (msg)
            sublime.status_message(msg)
            return
        except EnvironmentError as e:
            msg = "Mercurial: %s (Is the Mercurial binary on your PATH?)" % e
            print (msg)
            sublime.status_message(msg)
            return
        except Exception as e:
            msg = ("Mercurial: Cannot start server."
                  "(Your Mercurial version might be too old.)")
            print (msg)
            sublime.status_message(msg)
            return

        if getattr(self, 'worker', None) and self.worker.is_alive():
            sublime.status_message("Mercurial: Processing another request. "
                                   "Try again later.")
            return

        self.worker = CommandRunnerWorker(
                                          command_server=hgs,
                                          command=s,
                                          view=self.view,
                                          window=self.view.window(),
                                          fname=self.cwd or self.view.file_name(),
                                          display_name=self.display_name,
                                          append=self.append,)
        self.worker.start()


class ShowMercurialMenuCommand(sublime_plugin.WindowCommand):
    HG_CMDS = []

    def run(self):
        if not self.HG_CMDS:
            extensions = self.get_view().settings().get('packages.sublime_hg.extensions', [])
            ShowMercurialMenuCommand.HG_CMDS = get_commands_by_ext(extensions)

        items = ShowMercurialMenuCommand.HG_CMDS
        utils.show_qpanel(self.window, items, self.on_done)

    def get_view(self):
        return self.window.active_view()

    def on_done(self, s):
        if s == -1:
            return

        hg_cmd = self.HG_CMDS[s][0]
        extensions = self.get_view().settings().get('packages.sublime_hg.extensions', [])
        format_str, cmd_data = find_cmd(extensions, hg_cmd)

        fn = self.get_view().file_name()
        env = {'file_name': fn}

        # Handle commands differently whether they require input or not.
        # Commands requiring input have a "format_str".
        if format_str:
            # Collect single-line inputs from an input panel.
            if '%(input)s' in format_str:
                env['caption'] = cmd_data.prompt
                env['fmtstr'] = format_str
                self.window.run_command('hg_command_asking', env)
                return

            # Command requires additional info, but it's provided automatically.
            self.window.active_view().run_command('hg_command_runner', {
                                              'cmd': format_str % env,
                                              'display_name': hg_cmd})
        else:
            # It's a simple command that doesn't require any input, so just
            # go ahead and run it.
            self.window.active_view().run_command('hg_command_runner', {
                                              'cmd': hg_cmd,
                                              'display_name': hg_cmd})



class HgCommandAskingCommand(sublime_plugin.WindowCommand):
    """Asks the user for missing output and runs a Mercurial command.
    """
    def run(self, caption='', fmtstr='', **kwargs):
        self.fmtstr = fmtstr
        self.content = kwargs
        if caption:
            utils.show_ipanel(self.window, caption, on_done=self.on_done)
        return

        cmd = self.fmtstr % self.content
        self.window.run_command('hg_command_runner', {'cmd': cmd})

    def on_done(self, s):
        self.content['input'] = escape(s, '"')
        cmd = self.fmtstr % self.content
        self.window.run_command('hg_command_runner', {'cmd': cmd})


# XXX not ideal; missing commands
COMPLETIONS = HG_COMMANDS_LIST


#_____________________________________________________________________________
class HgCompletionsProvider(sublime_plugin.EventListener):
    CACHED_COMPLETIONS = []
    CACHED_COMPLETION_PREFIXES = []
    COMPLETIONS = []

    def load_completions(self, view):
        extensions = view.settings().get('packages.sublime_hg.extensions', [])
        extensions.insert(0, 'default')
        self.COMPLETIONS = []
        for ext in extensions:
            self.COMPLETIONS.extend(commands.HG_COMMANDS[ext].keys())
        self.COMPLETIONS = set(sorted(self.COMPLETIONS))

    def on_query_completions(self, view, prefix, locations):
        # Only provide completions to the SublimeHg command line.
        if view.score_selector(0, 'source.sublime_hg_cli') == 0:
            return []

        if not self.COMPLETIONS:
            self.load_completions(view)

        # Only complete top level commands.
        current_line = view.substr(view.line(view.size()))[2:]
        if current_line != prefix:
            return []

        if prefix and prefix in self.CACHED_COMPLETION_PREFIXES:
            return self.CACHED_COMPLETIONS

        new_completions = [x for x in self.COMPLETIONS if x.startswith(prefix)]
        self.CACHED_COMPLETION_PREFIXES = [prefix] + new_completions
        self.CACHED_COMPLETIONS = zip([prefix] + new_completions,
                                                    new_completions + [prefix])
        return self.CACHED_COMPLETIONS
