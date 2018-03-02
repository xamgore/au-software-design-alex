class LexerException(Exception):
    """
    исключение лексера
    """
    def __init__(self, message):
        super(LexerException, self).__init__(message)


class ParserException(Exception):
    """
    исключение парсера
    """
    def __init__(self, message):
        super(ParserException, self).__init__(message)


class CommandFileException(Exception):
    """
    исключение при работе с файлами
    """
    def __init__(self, message):
        super(CommandFileException, self).__init__(message)


class CommandExternalException(Exception):
    """
    исключение при работе с внешними командами
    """
    def __init__(self, message):
        super(CommandExternalException, self).__init__(message)
