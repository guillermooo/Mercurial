from Mercurial.test_runner import TestsState
from Mercurial.shglib import parsing

import unittest


class Test_Lexer(unittest.TestCase):
    def testCanInit(self):
        l = parsing.Lexer('foo')
        self.assertEqual(l.index, 0)
        self.assertEqual(l.c, 'f')

    def testCanConsume(self):
        l = parsing.Lexer('foo')
        l.consume()
        self.assertEqual(l.c, 'o')
        l.consume()
        self.assertEqual(l.c, 'o')
        l.consume()
        self.assertEqual(l.c, parsing.EOF)


class Test_CommandLexer(unittest.TestCase):
    def testCanLexSimple(self):
        l = parsing.CommandLexer('status')
        self.assertEqual(list(l), ['status'])

    def testCanLexShortSimpleOption(self):
        l = parsing.CommandLexer('status -n')
        self.assertEqual(list(l), ['status', '-n'])

    def testCanLexLongSimpleOption(self):
        l = parsing.CommandLexer('status --no-status')
        self.assertEqual(list(l), ['status', '--no-status'])

    def testCanLexOptionWithArg(self):
        l = parsing.CommandLexer('diff -r 100')
        self.assertEqual(list(l), ['diff', '-r', '100'])
        l = parsing.CommandLexer('diff -r100')
        self.assertEqual(list(l), ['diff', '-r', '100'])

    def testCanLexShortStringArg(self):
        l = parsing.CommandLexer('commit -m "foo"')
        self.assertEqual(list(l), ['commit', '-m', 'foo'])

    def testCanLexLongStringArg(self):
        l = parsing.CommandLexer('commit -m "foo bar foo"')
        self.assertEqual(list(l), ['commit', '-m', 'foo bar foo'])

    def testCanLexLongStringWithEmbeddedQuotes(self):
        l = parsing.CommandLexer('commit -m "foo \'bar\' foo"')
        self.assertEqual(list(l), ['commit', '-m', 'foo \'bar\' foo'])
        l = parsing.CommandLexer('commit -m "foo \'bar fuzz\' foo"')
        self.assertEqual(list(l), ['commit', '-m', 'foo \'bar fuzz\' foo'])

    def testCanLexLongStringWithEmbeddedEscapedQuotes(self):
        l = parsing.CommandLexer('commit -m "foo \\"bar\\" foo"')
        self.assertEqual(list(l), ['commit', '-m', 'foo "bar" foo'])
        l = parsing.CommandLexer('commit -m "foo \\"bar fuzz\\" foo"')
        self.assertEqual(list(l), ['commit', '-m', 'foo "bar fuzz" foo'])
