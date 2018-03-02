from src.Lexer import *
from src.Exceptions import *


class AbstractCommand:
    """
    команда интерпретатора
    """
    def __init__(self, name, args=None):
        if args is None:
            args = []
        self.name = name
        self.args = args

    def add_arg(self, arg):
        self.args.append(arg)

    def __str__(self):
        return 'Command({name}, {arg})'.format(
            name=self.name,
            arg=self.args
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.name == other.name and self.args == other.args


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, symbol):
        raise ParserException('Invalid syntax. Wait ' + symbol)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(token_type.value)

    def command(self):
        command_name = self.param()
        if command_name is None:
            self.error("command name")

        if self.current_token.type == Type.ASSIGNMENT:
            self.current_token = self.lexer.get_next_token()
            param = self.param()
            if param is None:
                self.error("arg")
            c = AbstractCommand("=")
            c.add_arg(str(command_name))
            c.add_arg(param)
            return c
        else:
            com = AbstractCommand(command_name)
            param = self.param()
            while True:
                if param is not None:
                    com.add_arg(param)
                if self.current_token.type == Type.PIPE or \
                                self.current_token.type == Type.EOF:
                    break
                param = self.param()
        return com

    def param(self):
        token = self.current_token
        if token.type == Type.STRING:
            self.current_token = self.lexer.get_next_token()
            return token.value
        if token.type in (Type.ONE_QUOTE, Type.TWO_QUOTES):
            result = []
            self.current_token = self.lexer.get_next_token()
            while self.current_token.type == Type.STRING:
                result.append(self.current_token.value)
                self.current_token = self.lexer.get_next_token()
            if token.type == Type.ONE_QUOTE:
                self.eat(Type.ONE_QUOTE)
                return "'" + ' '.join(result) + "'"
            else:
                self.eat(Type.TWO_QUOTES)
                return '"' + ' '.join(result) + '"'

    def expr(self):
        """
        expr            : command (PIPE command)*
        command         : (param param*) | (param ASSIGNMENT param)
        param           : STRING |
                            (ONE_QUOTE STRING* ONE_QUOTE) |
                            (TWO_QUOTES STRING* TWO_QUOTES)
        """
        command_list = []
        com = self.command()
        command_list.append(com)

        while self.current_token.type == Type.PIPE:
            self.current_token = self.lexer.get_next_token()
            com = self.command()
            command_list.append(com)

        return command_list

    def parse(self):
        # self.current_token = self.lexer.get_next_token()
        return self.expr()
