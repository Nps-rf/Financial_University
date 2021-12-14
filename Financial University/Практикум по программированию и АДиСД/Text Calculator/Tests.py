import unittest
from Text_Сalculator import Calculator as Calc


class TestStrToText(unittest.TestCase):
    case = Calc()

    def test_easy(self):
        """
        Test range:
        1 to 100
        """
        # Tests
        test_1 = 'Два плюс два'
        test_2 = 'Пять в степени два'
        test_3 = 'Сто делить на двадцать'
        test_4 = 'Пять умножить на пять плюс пять'
        test_5 = 'Двадцать восемь в степени два'
        # Answers
        ans_1 = 'Четыре'
        ans_2 = 'Двадцать пять'
        ans_3 = 'Пять'
        ans_4 = 'Тридцать'
        ans_5 = 'Семьсот восемьдесят четыре'
        self.assertEqual(ans_1, self.case.solve(string=test_1))  # 2 + 2 >>> Четыре
        self.assertEqual(ans_2, self.case.solve(string=test_2))  # 5 ** 2 >>> Двадцать пять
        self.assertEqual(ans_3, self.case.solve(string=test_3))  # 100 / 20 >>> Пять
        self.assertEqual(ans_4, self.case.solve(string=test_4))  # 5 * 5 + 5 >>> Тридцать
        self.assertEqual(ans_5, self.case.solve(string=test_5))  # 28 ** 2 >>> Семьсот восемьдесят четыре

    def test_medium(self):
        """
        Test range:
        999 to 19999
        """
        # Tests
        test_1 = 'Десять тысяч двести восемь умножить на четыре'
        test_2 = 'Девять тысяч девятьсот девяносто девять в степени два'
        test_3 = 'Тысяча минус семь умножить на девятьсот девяноста три'
        test_4 = 'Семь умножить на семь умножить на семь умножить на семь умножить на семь плюс семь'
        test_5 = 'Тысяча сто двадцать три умножить на ноль плюс один'
        # Answers
        ans_1 = 'Сорок тысяч восемьсот тридцать два'
        ans_2 = 'Девяносто девять миллионов девятьсот восемьдесят тысяч один'
        ans_3 = 'Восемьсот девяносто три тысячи семьсот девяносто три'
        ans_4 = 'Шестнадцать тысяч восемьсот четырнадцать'
        ans_5 = 'Один'
        self.assertEqual(ans_1, self.case.solve(string=test_1))
        self.assertEqual(ans_2, self.case.solve(string=test_2))
        self.assertEqual(ans_3, self.case.solve(string=test_3))
        self.assertEqual(ans_4, self.case.solve(string=test_4))
        self.assertEqual(ans_5, self.case.solve(string=test_5))

    def test_multiply(self):
        """
        There are only multiply tests
        -inf to +inf
        """
        # Tests
        test_1 = 'Два умножить на два'
        test_2 = 'Двадцать один умножить на десять'
        test_3 = 'Минус восемь умножить на восемь'
        test_4 = 'Сто умножить на сто умножить на сто'
        test_5 = 'Семь тысяч умножить на семь тысяч'
        # Answers
        ans_1 = 'Четыре'
        ans_2 = 'Двести десять'
        ans_3 = 'Минус шестьдесят четыре'
        ans_4 = 'Один миллион'
        ans_5 = 'Сорок девять миллионов'
        self.assertEqual(ans_1, self.case.solve(string=test_1))
        self.assertEqual(ans_2, self.case.solve(string=test_2))
        self.assertEqual(ans_3, self.case.solve(string=test_3))
        self.assertEqual(ans_4, self.case.solve(string=test_4))
        self.assertEqual(ans_5, self.case.solve(string=test_5))


if __name__ == '__main__':
    unittest.main()
