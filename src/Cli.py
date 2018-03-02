from src.Environment import *
from src.Parser import *
from src.Interpreter import *
from src.Exceptions import *


class Cli:
    def main(self):
        """
        обеспечивает основной цикл ввода команд интерпретатора
        """
        env = Environment()
        while True:
            try:
                text = input('cli> ')
            except EOFError:
                break
            if not text:
                continue

            try:
                lexer = Lexer(text)
                parser = Parser(lexer)
                result = parser.parse()
                inter = Interpreter()
                result = inter.interpolation_commands_list(result, env)
                result = inter.from_abstract_to_concrete(result)
                inter.run_commands_list(result, env)
            except LexerException:
                print("Syntax error. Repeat input ")
            except ParserException as e:
                print("Parsing error: " + str(e))
            except CommandFileException as e:
                print("File error: " + str(e))
            except CommandExternalException as e:
                print("Command error: " + str(e))
