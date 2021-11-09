from random import shuffle
import numpy as np


class Game:
    def __init__(self):
        self.correct_board = np.reshape(np.array([i for i in range(1, 16)] + [' ']), (4, 4))
        self.current_board = [i for i in range(1, 16)] + [' ']
        shuffle(self.current_board)
        self.current_board = np.reshape(self.current_board, (4, 4))
        self.is_going = True
        self.point_to_go = (0, 0)
        self.point_to_move = (1, 1)
        self.attempts = 0

    def _win(self) -> exit:
        """""
        Функция проверки победного условия
        """""
        flag = True
        for row in range(4):
            for a, b, in zip(self.current_board[row], self.correct_board[row]):  # я не знаю что случилось,
                # но numpy не дал мне нормально сравнивать массивы, пришлось так
                if a == b:
                    flag = True
                else:
                    flag = False
                    break
        if flag:
            self.is_going = False
            print('Количество попыток:', self.attempts)
            exit('Поздравляем с победой! Я надеюсь вам хватило терпения дойти до конца...')

    def print(self) -> None:
        """""
        Эта функция красивого вывода и форматирования игрового поля
        Непонятные символы, как например '\033[1m\033[92m', выполняют функцию консольного форматирования
        в данном случае:
            ◈ \033[1m -> Делает текст жирным
            ◈ \033[92m -> Окрашивает текст в зеленый цвет
        .format выполняет функцию выравнивания, чтобы ничего не съезжало
        """""
        max_len = max([len(str(e)) for row in self.current_board for e in row])
        print(' ', *list(map('{{:>{length}}}'.format(length=max_len).format,
                             [f'\033[1m\033[92m {i}' for i in range(1, 5)])))  # жесть
        for index, row in enumerate(self.current_board):
            print(f'\033[1m\033[92m{index + 1} \033[0m', *list(map('{{:{length}}}'.format(length=max_len).format, row)))

    def _is_correct(self, choice: list, procedure: str) -> bool:
        """""
        Функция проверки входных данных по критериям
        """""
        emp_point = 666
        for i in range(4):
            for z in range(4):
                if self.current_board[i][z] == ' ':
                    emp_point = i * 4 + z

        left = self.current_board[(emp_point - 1) // 4][(emp_point - 1) % 4] if (emp_point - 1) % 4 != 3 else '666'
        right = self.current_board[(emp_point + 1) // 4][(emp_point + 1) % 4] if (emp_point + 1) % 4 != 0 else '666'
        up = self.current_board[emp_point // 4 - 1][emp_point % 4] if emp_point // 4 != 0 else '666'
        down = self.current_board[emp_point // 4 + 1][emp_point % 4] if emp_point // 4 != 3 else '666'
        is_len = len(choice) == 2
        is_all_digits = all(map(lambda x: x.isdigit(), choice))
        is_out_of_range = (1 <= int(choice[0]) <= 4 and 1 <= int(choice[1]) <= 4) if is_all_digits and is_len else False
        correctors = [is_len, is_all_digits, is_out_of_range]
        if procedure == 'для перемещения костяшки':
            is_exact_point = self.point_to_move != choice
            correctors.append(is_exact_point)
        if all(correctors):
            if procedure == 'выбранной костяшки':
                return True if \
                    self.current_board[int(choice[0]) - 1][int(choice[1]) - 1] in [up, down, right, left] else False
            else:
                return True if self.current_board[int(choice[0]) - 1][int(choice[1]) - 1] == ' ' else False
        return False

    def move(self) -> None:
        """""
        Перемещает костяшки на доске согласно входным данным
        """""
        x1, y1 = self.point_to_move
        x2, y2 = self.point_to_go
        old_p = self.current_board[x1 - 1][y1 - 1]
        self.current_board[x1 - 1][y1 - 1] = self.current_board[x2 - 1][y2 - 1]
        self.current_board[x2 - 1][y2 - 1] = old_p
        self._win()

    def input(self, procedure: str) -> None:
        """""
        Функция ввода и управления входным данными
        """""
        print(f'Введите координаты {procedure} (СТРОКА | КОЛОННА)')
        while True:
            choice = input().split()
            if self._is_correct(choice, procedure):
                if procedure == 'выбранной костяшки':
                    self.point_to_move = map(int, choice)
                else:
                    self.point_to_go = map(int, choice)
                    self.move()
                break
            else:
                print('Давай по новой Миша')


if __name__ == '__main__':
    # noinspection SpellCheckingInspection
    """
    FINANCIAL UNIVERSITY
    Author: Pikalov Nikolai
    Group: PI21-7
    FINANCIAL UNIVERSITY
    """
    game = Game()
    while game.is_going:
        game.print()
        game.attempts += 1
        game.input('выбранной костяшки')
        game.input('для перемещения костяшки (Пустое поле)')
