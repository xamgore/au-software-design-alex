class LexerException(Exception):
    def __init__(self, message):
        super(LexerException, self).__init__(message)


class ParserException(Exception):
    def __init__(self, message):
        super(ParserException, self).__init__(message)


class CommandFileException(Exception):
    def __init__(self, message):
        super(CommandFileException, self).__init__(message)


class CommandExternalException(Exception):
    def __init__(self, message):
        super(CommandExternalException, self).__init__(message)
