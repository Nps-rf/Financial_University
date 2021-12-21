# -*- coding: utf-8 -*-
# noinspection SpellCheckingInspection
"""
Created on 09.12.2021 by Nikolai Pikalov
@author: Nikolai Pikalov <ya.pikus@gmail.com>
Changed on 14.12.2021 by Nikolai Pikalov
"""
import csv
from num2words import num2words as n2w


class Calculator:
    """
    Analog of classic calculator, but it includes text input
    IN[1]  >>> 'Пять плюс пять'
    OUT[1] >>> 'Десять'
    RUSSIAN LANGUAGE ONLY
    """
    def __init__(self):
        self.words = self._load_()
        self.string = str()
        self.result = float()
        self.test = True
        self.show = False

    def solve(self, string: str = None) -> float or int or None:
        if string is None:
            self.show = True
        self._input(string)
        self.string2number()
        self.calculate()
        if self.show:
            print(self.reconvert())
        elif self.test:
            return self.reconvert()
        else:
            return None

    def _input(self, string) -> None:
        self.string = input('Ввод: ').lower() if string is None else string.lower()

    @staticmethod
    def _load_(path: str = 'words.csv', encoding: str = 'utf-8') -> dict:
        """
        Loading a dictionary of all words for string-digit conversion
        You can use your own csv-file to switch language
        """
        with open(path, 'r', encoding=encoding) as words:
            return dict(csv.reader(words))

    def string2number(self) -> None:
        self.string = list(self.string)

        for v in range(len(self.string) - 2):
            if (self.string[v] == ' ' or self.string[v] == '') and (self.string[v + 1] + self.string[v + 2] == 'ты'):
                self.string[v] = '*'

        self.string = ''.join(self.string)

        for key, value in reversed(self.words.items()):
            self.string = self.string.replace(key, str(value))

        self.string = list(self.string)

        for v in range(len(self.string) - 2):
            if self.string[v + 1] + self.string[v + 2] == 'ты':
                self.string[v] = '*'
            if self.string[v] == 'в' and not self.string[v + 1].isalpha():
                self.string[v] = ')'
                self.string.insert(0, '(')
            if self.string[v] == 'а' and self.string[v - 1] == 'н':
                self.string[v - 1] = ''
                self.string[v] = ''
                self.string.insert(v - 3, ')')
                self.string.insert(0, '(')
            if self.string[v] == ')' and self.string.count('(') != self.string.count(')'):
                self.string.insert(0, '(')

        for i in range(1, len(self.string) - 1):
            if self.string[i - 1].isdigit() and (self.string[i] == ' ' or self.string == '') \
                    and not self.string[i + 1].isalpha() and self.string[i + 1] \
                    not in ('*', '/', '-', '+', '.', ' ', '  ', ')', '('):
                self.string[i] = '+'

        self.string = ''.join(self.string).replace('на', '')

    def get(self, obj='string'):
        if obj == 'string':
            return self.string
        elif obj == 'result':
            return self.result

    # noinspection PyBroadException
    # Because i'm too lazy
    def calculate(self) -> None:
        """
        Calculations part using eval
        """
        self.result = eval(self.string)
        if int(self.result) == self.result:
            self.result = int(self.result)

    def reconvert(self, lang='ru') -> str:
        """
        n2w -> Number to words package
        must be installed :(
        Switch "lang" to choose your language
        """
        return n2w(self.result, lang=lang).capitalize()


if __name__ == '__main__':
    while True:
        Calc = Calculator()
        Calc.solve()
