"""simple client for the mercurial command server"""

import sublime

import subprocess
import struct
import os
import logging

from Mercurial.shglib import parsing

CH_DEBUG = 'd'
CH_ERROR = 'e'
CH_INPUT = 'I'
CH_LINE_INPUT = 'L'
CH_OUTPUT = 'o'
CH_RETVAL = 'r'


def get_startup_info():
    startup_info = None
    if os.name == 'nt':
        startup_info = subprocess.STARTUPINFO()
        startup_info.dwFlags = subprocess.STARTF_USESHOWWINDOW
    return startup_info


def start_server(hg_bin, repo_root, **kwargs):
    """Returns a command server ready to be used."""
    try:
        return subprocess.Popen(
                    [hg_bin, "serve",
                            "--cmdserver", "pipe",
                            "--repository", repo_root,
                            "--config", "ui.interactive=False"],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    # If we don't redirect stderr and the server does not support an enabled
                    # extension, we won't be able to read stdout.
                    stderr=subprocess.PIPE,
                    startupinfo=get_startup_info()
                    )
    except Exception as e:
        logging.error(e)
        raise


def init_repo(hg_bin="hg", root="."):
    return subprocess.Popen([hg_bin, "init", "--repository", root],
                            startupinfo=get_startup_info(),
                            )


class CmdServerClient(object):
    def __init__(self, repo_root, hg_bin='hg'):
        self.hg_bin = hg_bin
        self.server = start_server(hg_bin, repo_root)
        self.read_greeting()

    def shut_down(self):
        self.server.stdin.close()

    def read_channel(self):
        # read channel name (1 byte) plus data length (4 bytes, BE)
        fmt = '>cI'
        ch, length = struct.unpack(fmt,
                                   self.server.stdout.read(struct.calcsize(fmt)))

        assert len(ch) == 1, "Expected channel name of length 1."
        if ch.decode('ascii') in 'LI':
            raise NotImplementedError("Can't provide more data to server.")

        text = self.server.stdout.read(length)
        return ch, text

    def read_greeting(self):
        _, ascii_txt = self.read_channel()
        ascii_txt = ascii_txt.decode('ascii')
        assert ascii_txt, "Expected hello message from server."

        # Parse hello message.
        capabilities, encoding = ascii_txt.split('\n')
        self.encoding = encoding.split(':')[1].strip().lower()
        self.capabilities = capabilities.split(':')[1].strip().split()

        if not 'runcommand' in self.capabilities:
            raise EnvironmentError("Server doesn't support basic features.")

    # TODO: test better: make_block (string) + write_block (void)
    def _write_block(self, data):
        # Encoding won't work well on Windows:
        # http://mercurial.selenic.com/wiki/CharacterEncodingOnWindows
        if sublime.platform() == 'windows':
            try:
                ' '.join(data).encode('ascii')
            except UnicodeEncodeError:
                sublime.status_message("Mercurial: Warning")
                # todo: use warnings module instead?
                logging.warning("Encoding non-ascii text may not work well on Windows: {0}".format(' '.join(data)))

        encoded_data = [x.encode(self.encoding) for x in data]

        new_data = b''
        for i, d in enumerate(encoded_data):
            if i != 0:
                d = b'\0' + d
            new_data += d

        preamble = struct.pack(">I", len(new_data))
        self.server.stdin.write(preamble + new_data)
        self.server.stdin.flush()

    def run_command(self, cmd):
        args = list(parsing.CommandLexer(cmd))
        if args[0] == 'hg':
            logging.debug("Stripped superfluous 'hg' from command.")
            args = args[1:]

        logging.debug("Sending command '%s' as %s" % (args, args))
        self.server.stdin.write('runcommand\n'.encode('ascii'))
        self._write_block(args)

    def receive_data(self):
        lines = []
        while True:
            channel, data = self.read_channel()
            channel = channel.decode('ascii')
            if channel == CH_OUTPUT:
                lines.append(data.decode(self.encoding))
            elif channel == CH_RETVAL:
                return (''.join(lines)[:-1], struct.unpack(">l", data)[0])
            elif channel == CH_DEBUG:
                logging.debug(data)
            elif channel == CH_ERROR:
                lines.append(data.decode(self.encoding))
                logging.error("Mercurial server error. Data follows.")
                logging.error(data)
            elif channel in (CH_INPUT, CH_LINE_INPUT):
                logging.error("More data requested, can't satisfy.")
                self.shut_down()
                return
            else:
                self.shut_down()
                logging.error("Didn't expect such channel: " + channel)
                return
