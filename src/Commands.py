from src.Exceptions import *
from abc import ABC
import os
import sys
import subprocess
from pathlib import Path


class CommandResult:
    """
    описывает результат работы каждой команды
    хранит в себе выходной поток
    """
    def __init__(self, output_stream=""):
        self.output_stream = output_stream

    def __eq__(self, other):
        return self.output_stream == other.output_stream


class Command(ABC):
    def __init__(self, args):
        self.args = args

    def run(self, input_stream, env):
        pass


class External(Command):
    """
    внешняя команды
    например, git status
    """
    def run(self, input_stream, env):
        process_result = None
        try:

            process_result = subprocess.run(self.args, input=input_stream,
                                            stdout=subprocess.PIPE,
                                            encoding=sys.stdout.encoding)
        except FileNotFoundError:
            raise CommandExternalException("external command not found")
        return CommandResult(process_result.stdout)


class Assignment(Command):
    """
    команда присваивания
    например, x=5
    """
    def run(self, input_stream, env):
        env.add_var(self.args[0], self.args[1])
        return CommandResult()


class Echo(Command):
    """
    команда echo вывода в поток
    например, echo 5
    """
    def run(self, input_stream, env):
        return CommandResult(
            " ".join(self.args) if len(self.args) != 0 else " ")


class Cat(Command):
    """
    команда cat чтения файла и вывода в поток
    например, cat "example.txt"
    """
    def run(self, input_stream, env):
        if len(self.args) == 0:
            return CommandResult(input_stream)
        else:
            if os.path.isfile(self.args[0]) and \
                    os.access(self.args[0], os.R_OK):
                with open(self.args[0], "r") as file:
                    return CommandResult(file.read())
            else:
                raise CommandFileException(
                    "CAT error (bad permission, not exists)")


class Wc(Command):
    """
    команда wc - отображает число строк, слов, байт в файле
    например, wc "example.txt"
    """
    def __wc(self, input_stream):
        line_count = words_count = bytes_count = 0
        for line in input_stream.split('\n'):
            words_count += len(line.split())
            bytes_count += len(line.encode('utf8'))
            line_count += 1
        return "\t {:d} \t {:d} \t {:d}".format(line_count, words_count,
                                                bytes_count)

    def run(self, input_stream, env):
        if len(self.args) == 0:
            return CommandResult(self.__wc(input_stream))
        else:
            if os.path.isfile(self.args[0]) and \
                    os.access(self.args[0], os.R_OK):
                with open(self.args[0], "r") as file:
                    return CommandResult(self.__wc(file.read()))
            else:
                raise CommandFileException(
                    "WC error (bad permission, not exists)")


class Pwd(Command):
    """
    команда pwd отображает текущую рабочую директорию
    например, pwd
    """
    def run(self, input_stream, env):
        return CommandResult(env.get_cur_dir())


class Exit(Command):
    """
    команда exit выхода из консоли
    например, exit
    """
    def run(self, input_stream, env):
        sys.exit()


class Ls(Command):
    """
    команда ls вывода содержимого текущей дериктории
    например, ls /home
    """
    def run(self, input_stream, env):
        path = (self.args + ['.'])[0]

        try:
            dirs = os.listdir(path)
            return CommandResult('\n'.join(dirs))
        except Exception as e:
            raise CommandFileException(e)


class Cd(Command):
    """
    команда cd смены текущей директории
    """
    def run(self, input_stream, env):
        home = str(Path.home())
        path = (self.args + [home])[0]

        try:
            os.chdir(path)
            return CommandResult()
        except Exception as e:
            raise CommandFileException(e)
