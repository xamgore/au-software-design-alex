import unittest
from src.Commands import *
from src.Environment import *


class CommandTest(unittest.TestCase):
    def test_cat(self):
        env = Environment()

        command = Cat(["example.txt"])
        self.assertEqual(command.run("", env),
                         CommandResult("Hello, World!\nBye, World!"))

        command = Cat([])
        self.assertEqual(command.run("Hello, World!", env),
                         CommandResult("Hello, World!"))

    def test_echo(self):
        env = Environment()

        command = Echo(["example.txt"])
        self.assertEqual(command.run("", env),
                         CommandResult("example.txt"))

        command = Echo(["example.txt", "a"])
        self.assertEqual(command.run("", env),
                         CommandResult("example.txt a"))

        command = Echo([""])
        self.assertEqual(command.run("", env),
                         CommandResult(""))

        command = Echo(["'aa'", '"cc"'])
        self.assertEqual(command.run("", env),
                         CommandResult("'aa' \"cc\""))

    def test_assignment(self):
        env = Environment()

        command = Assignment(["x", "123"])
        self.assertEqual(env.get_var("x"), "")
        command.run("", env)
        self.assertEqual(env.get_var("x"), "123")

        command = Assignment(["x", "'aa'"])
        self.assertEqual(env.get_var("x"), "123")
        command.run("", env)
        self.assertEqual(env.get_var("x"), "'aa'")

        command = Assignment(["echo", '"d"'])
        self.assertEqual(env.get_var("echo"), "")
        command.run("", env)
        self.assertEqual(env.get_var("echo"), '"d"')

    def test_wc(self):
        env = Environment()

        command = Wc(["example.txt"])
        self.assertEqual(command.run("", env),
                         CommandResult("\t 2 \t 4 \t 24"))

        command = Wc([])
        self.assertEqual(command.run("Hello, World!", env),
                         CommandResult("\t 1 \t 2 \t 13"))
