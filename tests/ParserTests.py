import unittest
from src.Parser import *


class ParserTest(unittest.TestCase):
    def test_param(self):
        parser = Parser(Lexer("aaa bb2b \"a1a b$b cc\" '' '$ads'"))
        self.assertEqual(parser.param(), "aaa")
        self.assertEqual(parser.param(), "bb2b")
        self.assertEqual(parser.param(), '"a1a b$b cc"')
        self.assertEqual(parser.param(), "''")
        self.assertEqual(parser.param(), "'$ads'")

    def test_param_none(self):
        parser = Parser(Lexer(" "))
        self.assertEqual(parser.param(), None)

    def test_command(self):
        parser = Parser(Lexer("cat 1"))
        self.assertEqual(parser.command(), AbstractCommand("cat", ["1"]))
        parser = Parser(Lexer('echo "$a" 1 aa'))
        self.assertEqual(parser.command(),
                         AbstractCommand("echo", ['"$a"', "1", 'aa']))
        parser = Parser(Lexer("git status '$a'"))
        self.assertEqual(parser.command(),
                         AbstractCommand("git", ["status", "'$a'"]))
        parser = Parser(Lexer("exit 0"))
        self.assertEqual(parser.command(), AbstractCommand("exit", ["0"]))
        parser = Parser(Lexer("g"))
        self.assertEqual(parser.command(), AbstractCommand("g", []))
        parser = Parser(Lexer("'1' h"))
        self.assertEqual(parser.command(), AbstractCommand("'1'", ['h']))
        parser = Parser(Lexer('"a" g'))
        self.assertEqual(parser.command(), AbstractCommand('"a"', ["g"]))
        parser = Parser(Lexer('x=6'))
        self.assertEqual(parser.command(), AbstractCommand('=', ["x", "6"]))
        parser = Parser(Lexer('"x"="$s6"'))
        self.assertEqual(parser.command(),
                         AbstractCommand('=', ['"x"', '"$s6"']))

    def test_expr(self):
        parser = Parser(Lexer("cat 1 | echo | grep 5"))
        self.assertEqual(parser.expr(),
                         [AbstractCommand('cat', ["1"]),
                          AbstractCommand('echo', []),
                          AbstractCommand('grep', ["5"])])

        parser = Parser(Lexer("cat | 'exit' | x=''"))
        self.assertEqual(parser.expr(),
                         [AbstractCommand('cat', []),
                          AbstractCommand("'exit'", []),
                          AbstractCommand('=', ["x", "''"])])
