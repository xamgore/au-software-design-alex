from enum import Enum
from src.Exceptions import *


class Type(Enum):
    """
    Тип перечисление для всех видов токенов
    """
    STRING = 'STRING'
    ASSIGNMENT = 'ASSIGNMENT'
    PIPE = 'PIPE'
    ONE_QUOTE = 'ONE_QUOTE'
    TWO_QUOTES = 'TWO_QUOTES'
    EOF = 'EOF'


class Token(object):
    """
    Тип токена(лексемы) для лексера. Хранит (тип токена, значение токена)
    """

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value


class Lexer(object):
    """
    Лексер для лексического разбора команды
    """
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise LexerException('Invalid character')

    def next_char(self):
        """
        Следующий символ для рабора
        """
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        """
        Пропуск пробелов
        """
        while self.current_char is not None and self.current_char.isspace():
            self.next_char()

    def string(self):
        """
        Осуществляет поиск токена-строки (последовательность символов,
        отличных от " ", "=", "|", "\'", "\"" )
        """
        result = ''
        while self.current_char is not None and \
                not self.current_char in (" ", "=", "|", "\'", "\""):
            result += self.current_char
            self.next_char()
        return result

    def get_next_token(self):
        """
        :return:
        Возвращает следующий токен (EOF - если токенов больше нет).
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '=':
                self.next_char()
                return Token(Type.ASSIGNMENT, '=')

            if self.current_char == '|':
                self.next_char()
                return Token(Type.PIPE, '|')

            if self.current_char == '\'':
                self.next_char()
                return Token(Type.ONE_QUOTE, '\'')

            if self.current_char == '"':
                self.next_char()
                return Token(Type.TWO_QUOTES, '"')

            return Token(Type.STRING, self.string())

        return Token(Type.EOF, None)
