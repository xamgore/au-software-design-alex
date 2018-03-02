import os


class Environment:
    """
    хранит ив себе окружение:
    текущую рабочую директорию и словарь переменных
    """
    def __init__(self):
        self._vars = dict()
        self._cur_dir = os.getcwd()

    def get_cur_dir(self):
        """
        :return: возвращает текущую рабочую директорию
        """
        return self._cur_dir

    def add_var(self, name, value):
        """
        добавляет переменную в словарь
        :param name: имя переменной
        """
        self._vars[name] = value

    def get_var(self, name):
        """
        :param name: имя переменной
        :return: значение переменной
        """
        return self._vars.get(name, "")
