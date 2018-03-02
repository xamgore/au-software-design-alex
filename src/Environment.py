import os


class Environment:
    def __init__(self):
        self._vars = dict()
        self._cur_dir = os.getcwd()

    def get_cur_dir(self):
        return self._cur_dir

    def add_var(self, name, value):
        self._vars[name] = value

    def get_var(self, name):
        return self._vars.get(name, "")
