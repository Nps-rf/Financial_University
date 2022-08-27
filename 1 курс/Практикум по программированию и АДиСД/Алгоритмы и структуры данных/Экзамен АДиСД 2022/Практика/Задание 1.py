from math import pi


class Main(object):
    """Условие:
        Написать программу с интерактивным консольным меню (т.е. вывод списка действий по цифрам)
        по вычислению:
         площади круга (родительский класс),
         длины окружности (подкласс) и
         объема шара (подкласс)
        по задаваемому с клавиатуры радиусу.
        Содержание меню:
         1. Вычислить площадь круга.
         2. Вычислить длину окружности.
         3. Вычислить объем шара.
         """
    @classmethod
    def menu(cls):
        ways = {
            1: Circle.Area,
            2: Circle.Length,
            3: Circle.Volume,
        }
        print(
            'Задание №1!\n'
            'Choose what you need\n'
            '1) Calculate Circle Area\n'
            '2) Calculate Circle Length\n'
            '3) Calculate Circle Volume'
        )
        choose = int(input())
        radius = int(input(
            'Enter circle\'s radius: '
        ))
        print('Result is: ', ways[choose](radius))


class CircleArea(object):
    def __init__(self, radius):
        self.radius = radius
        self.result = pi * radius ** 2

    def __str__(self): return str(self.result)


class CircleLength(CircleArea):
    def __init__(self, radius):
        super().__init__(radius)
        self.result = 2 * pi * radius


class CircleVolume(CircleArea):
    def __init__(self, radius):
        super().__init__(radius)
        self.result = (4 / 3) * pi * (radius ** 3)


class Circle(object):
    Area = CircleArea
    Length = CircleLength
    Volume = CircleVolume


if __name__ == '__main__':
    Main.menu()

