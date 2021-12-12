# -*- coding: utf-8 -*-
# noinspection SpellCheckingInspection
"""
Created on 09.12.2021 by Nikolai Pikalov
@author: Nikolai Pikalov <ya.pikus@gmail.com>
"""
import unittest
import csv
from num2words import num2words as n2w


class Calc:
    def __init__(self):
        self.words = self.load()
        self.string = str()
        self.result = float()
        self.ok = True
        self.show = False

    def run(self, string=''):
        if string == '':
            self.show = True
        self.ok = True
        self._input(string)
        self.convert()
        self.calculate()
        if self.show:
            print(self.reconvert())
        elif self.ok:
            return self.reconvert()
        else:
            return None

    def _input(self, string):
        self.string = input('Ввод: ').lower() if string == '' else string.lower()

    @staticmethod
    def load(path='words.csv', encoding='utf-8'):
        with open(path, 'r', encoding=encoding) as words:
            return dict(csv.reader(words))

    def convert(self):
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

    def calculate(self):
        try:
            self.result = eval(self.string)
            if int(self.result) == self.result:
                self.result = int(self.result)
        except:
            if self.show:
                print('\n\033[93mCorrect input data was expected\n\033[0m')
            self.ok = False
            self.show = False

    def reconvert(self):
        return n2w(self.result, lang="ru").capitalize()


if __name__ == '__main__':
    while True:
        Calculator = Calc()
        Calculator.run()
        'BETA'


class TestStrToText(unittest.TestCase):
    case = Calc()

    def test_easy(self):
        """
        Test range:
        1 to 100
        """
        test_1 = 'Два плюс два'
        test_2 = 'Пять в степени два'
        test_3 = 'Сто делить на двадцать'
        test_4 = 'Пять умножить на пять плюс пять'
        test_5 = 'Двадцать восемь в степени два'
        ans_1 = 'Четыре'
        ans_2 = 'Двадцать пять'
        ans_3 = 'Пять'
        ans_4 = 'Тридцать'
        ans_5 = 'Семьсот восемьдесят четыре'
        self.assertEqual(ans_1, self.case.run(string=test_1))  # 2 + 2 >>> Четыре
        self.assertEqual(ans_2, self.case.run(string=test_2))  # 5 ** 2 >>> Двадцать пять
        self.assertEqual(ans_3, self.case.run(string=test_3))  # 100 / 20 >>> Пять
        self.assertEqual(ans_4, self.case.run(string=test_4))  # 5 * 5 + 5 >>> Тридцать
        self.assertEqual(ans_5, self.case.run(string=test_5))  # 28 ** 2 >>> Семьсот восемьдесят четыре

    def test_medium(self):
        """
        Test range:
        1000 to 10000
        """
        test_1 = 'Десять тысяч двести восемь умножить на четыре'
        test_2 = 'Девять тысяч девятьсот девяносто девять в степени два'
        test_3 = 'Тысяча минус семь умножить на девятьсот девяноста три'
        test_4 = 'Семь умножить на семь умножить на семь умножить на семь умножить на семь плюс семь'
        test_5 = 'Тысяча сто двадцать три умножить на ноль плюс один'
        ans_1 = 'Сорок тысяч восемьсот тридцать два'
        ans_2 = 'Девяносто девять миллионов девятьсот восемьдесят тысяч один'
        ans_3 = 'Восемьсот девяносто три тысячи семьсот девяносто три'
        ans_4 = 'Шестнадцать тысяч восемьсот четырнадцать'
        ans_5 = 'Один'
        self.assertEqual(ans_1, self.case.run(string=test_1))
        self.assertEqual(ans_2, self.case.run(string=test_2))
        self.assertEqual(ans_3, self.case.run(string=test_3))
        self.assertEqual(ans_4, self.case.run(string=test_4))
        self.assertEqual(ans_5, self.case.run(string=test_5))

    def test_errors(self):
        """
        Test case for extra input
        """
        test_1 = ' '
        test_2 = 'Hello'
        test_3 = 'QWERTY'
        test_4 = '/FH5'
        test_5 = 'Пять плюс five'
        err = None
        self.assertEqual(err, self.case.run(string=test_1))
        self.assertEqual(err, self.case.run(string=test_2))
        self.assertEqual(err, self.case.run(string=test_3))
        self.assertEqual(err, self.case.run(string=test_4))
        self.assertEqual(err, self.case.run(string=test_5))
