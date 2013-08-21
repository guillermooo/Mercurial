from AAAPT.runner import TestsState
from Mercurial.shglib import client

import unittest
import os
import tempfile
import datetime
import time
import shutil


class WithTemporaryDirectory(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.d)

    def tearDown(self):
        os.chdir(self.old_cwd)
        try:
            shutil.rmtree(self.d)
        except Exception as e:
            print(e)


class WithTemporaryRepository(WithTemporaryDirectory):
    def setUp(self):
        super().setUp()
        hg_bin = 'hg' if (os.name != 'nt') else 'hg.bat'
        client.init_repo(hg_bin, ".")
        time.sleep(.25)


class Test_init_repo(WithTemporaryDirectory):
    def testCanInit(self):
        hg_bin = 'hg' if (os.name != 'nt') else 'hg.bat'
        client.init_repo(hg_bin, ".")
        time.sleep(.25)
        self.assertTrue(os.path.exists("./.hg"))


class Test_get_startup_info(unittest.TestCase):
    def testCanCreateStartupInfo(self):
        sui = client.get_startup_info()
        sui = (sui is not None) if (os.name == 'nt') else (sui is None)
        self.assertTrue(sui)


class Test_start_server(WithTemporaryRepository):
    def testCanStart(self):
        hg_bin = 'hg' if (os.name != 'nt') else 'hg.bat'
        try:
            server = client.start_server(hg_bin, ".")
            # Ensure the server is responding.
            self.assertTrue(server.communicate()[0])
        finally:
            server.stdin.close()


class Test_CmdServerClient(WithTemporaryRepository):
    def setUp(self):
        super().setUp()
        self.bin = hg_bin = 'hg' if (os.name != 'nt') else 'hg.bat'

    def testCanStart(self):
        c = client.CmdServerClient(".", self.bin)
        self.assertEqual(c.hg_bin, self.bin)
        self.assertIsNotNone(c.server)
        self.assertIsNotNone(c.encoding)
        self.assertIsNotNone(c.capabilities)

    def testCanShutDown(self):
        c = client.CmdServerClient(".", self.bin)
        c.shut_down()
        time.sleep(.1)
        self.assertRaises(ValueError, c.server.stdin.write)

    def testSendReceive(self):
        c = client.CmdServerClient(".", self.bin)
        c.run_command(['version'])
        rv = c.receive_data()
        self.assertTrue(rv[0])


