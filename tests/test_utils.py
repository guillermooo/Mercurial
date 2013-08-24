import unittest
import os

from test_runner import tests_state

from shglib import utils


class TestHelpers(unittest.TestCase):
    def testPushd(self):
        cwd = os.getcwd()
        target = os.environ["TEMP"]
        with utils.pushd(target):
            self.assertEqual(os.getcwdu(), target)
        self.assertEqual(os.getcwdu(), cwd)
