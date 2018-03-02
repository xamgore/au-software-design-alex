import copy
import re

from src.Commands import *


class Interpreter:
    def from_abstract_to_concrete(self, commands):

        def delete_quotes(args):
            new_args = []
            for arg in args:
                new_args.append(arg.strip('\"\''))
            return new_args

        result_list = []
        for command in commands:
            name = command.name.strip('\"\'')
            if name == "echo":
                result_list.append(Echo(delete_quotes(command.args)))
            elif name == "cat":
                result_list.append(Cat(delete_quotes(command.args)))
            elif name == "wc":
                result_list.append(Wc(delete_quotes(command.args)))
            elif name == "pwd":
                result_list.append(Pwd(delete_quotes(command.args)))
            elif name == "exit":
                result_list.append(Exit(delete_quotes(command.args)))
            elif name == "=":
                result_list.append(Assignment(delete_quotes(command.args)))
            else:
                result_list.append(
                    External([name] + delete_quotes(command.args)))
        return result_list

    def interpolation_command(self, command, env):

        def find_var(m):
            var = m.group(1)
            return env.get_var(var)

        regex = '\$([A-Za-z0-9]+)'
        new_command = copy.deepcopy(command)
        if not command.name.startswith("'"):
            new_command.name = re.sub(regex, find_var, command.name)

        for i in range(len(command.args)):
            if not command.args[i].startswith("'"):
                new_command.args[i] = re.sub(regex, find_var, command.args[i])

        return new_command

    def interpolation_commands_list(self, commands, env):
        new_commands_list = []
        for i in commands:
            new_commands_list.append(self.interpolation_command(i, env))
        return new_commands_list

    def from_commands_list_to_string(self, commands):
        result = ""
        for i in range(len(commands)):
            command = commands[i]
            if command.name != "=":
                result += command.name + " "
                result += " ".join(command.args)
            else:
                result += command.args[0] + "=" + command.args[1]
            if i < len(commands) - 1:
                result += " | "
        return result

    def run_commands_list(self, commands, env):
        result = commands[0].run("", env)
        for i in range(1, len(commands)):
            result = commands[i].run(result.output_stream, env)
        if result.output_stream != "":
            print(result.output_stream)
