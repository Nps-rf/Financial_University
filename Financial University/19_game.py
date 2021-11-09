class Game:
    def __init__(self) -> None:
        """""
        Правила игры: 
            ◈ Нужно выписать подряд числа от 1 до 19
            ◈ в строчку до 9, а потом начать следующую строку,
            ◈ в каждой клетке по 1 цифре. 
            ◈ Затем игроку необходимо вычеркнуть парные цифры или дающие в сумме 10. 
            ◈ Условие -  пары должны находиться рядом или через зачеркнутые цифры по горизонтали или по вертикали. 
            ◈ После того как все возможные пары вычеркнуты, оставшиеся цифры переписываются в конец таблицы. 
            ◈ Цель - полностью вычеркнуть все цифры. 
        """""
        self.board = list()
        self.fix = 17
        self.statement = True
        self.already_visited = []
        self.current_ways = 666
        self.attempts = 0

    def _input(self, point_number) -> map:  # Проверка ввода и сам ввод
        """""
        Функция ввода пользователя
        Запрашивает ввод, проверяет ввод на корректность и соответствие формату:
        [IN 1] -> X1 Y1
        [IN 2] -> X2 Y2
        ◈ X и Y целые числа удовлетворяющие динамическим условиям размера матрицы
        """""
        print(f'Введите координаты {point_number} числа в формате строка | колонна:')
        while True:
            curr = input()
            if not curr.isspace() and len(curr.split()) == 2:
                row, column = choice = curr.split()
                # В следующие после комментариев строчки кода вникать не стоит,
                # тут я просто проверяю, чтобы введенные числа были в пределе поля.
                # А также проверяю чтобы они не были уже посещенными ранее.
                # В силу того, что я отказался от матрицы в пользу арифметики.
                # Я решил использовать именно такую запись ровно как и в проверке значений.
                if all(map(lambda x: x.isdigit(), choice)) \
                        and list(choice) not in self.already_visited \
                        and (int(row) * 9 + int(column)) <= int(len(self.board) + len(self.board) // 1.5)\
                        and (0 < int(column) < 10 and 0 < int(row) < 4):
                    self.already_visited.append(choice)
                    return map(lambda x: int(x) - 1, choice)
                else:
                    print('Что-то ты не то ввёл')
            else:
                print('Что-то ты не то ввёл')

    def game_board(self) -> None:  # Создание игрового поля
        for i in range(19):
            self.board += str(i + 1) if i + 1 != 10 else ''

    def show(self) -> None:  # Вывод игрового поля
        """
        Эта функция красивого вывода и форматирования игрового поля
        Непонятные символы, как например '\033[1m\033[92m', выполняют функцию консольного форматирования
        в данном случае:
            ◈ \033[1m -> Делает текст жирным
            ◈ \033[92m -> Окрашивает текст в зеленый цвет
        :return: None
        """
        print(' ', * [f'\033[1m\033[92m{str(i + 1)}' for i in range(9)], sep='   ', end='\n\033[0m')
        board_to_show = ' '.join(self.board)
        print('\033[1m\033[92m1\033[0m' + '  ', *board_to_show[:self.fix])
        if len(board_to_show) > 2 * (self.fix + 1):
            print('\033[1m\033[92m2\033[0m' + '  ', *board_to_show[self.fix+1:2*(self.fix+1)])
        fix = 2 * (self.fix + 1)
        if len(board_to_show) > fix:
            print('\033[1m\033[92m3\033[0m' + '  ', *board_to_show[fix:])

    def check_ways(self, state=True) -> None:  # Проверка на наличие возможных ходов
        """
        Функция проверки всех возможных чисел для составления комбинаций
        ◈ state - флаг передаваемый из стека функции transform для устранения двойной печати поля при его перестроении
        :return: None
        """
        board = self.board
        ways = 0
        for index, elem in enumerate(board):
            # Прохожусь абсолютно по всему полю.
            # Формирую для каждой точки на поле, соседей и выставляю им необходимые условия соответствия
            bottom = board[index + 9] if index + 9 < len(self.board) else '666'
            over_bottom = board[index + (9 * 2)] if bottom == '#' and index + (9 * 2) < len(self.board) else '666'
            if index >= 9:
                right = str(board[index + 1]) if index + 1 < len(self.board) and index + 1 % 9 != 1 else '666'
                over_right = str(board[index + 2]) \
                    if right == '#' and index + 2 < len(self.board) and index + 2 % 9 != 1 else '666'
            else:
                right = str(board[index + 1]) if index + 1 < len(self.board) else '666'
                over_right = str(board[index + 2]) if right == '#' and index + 2 < len(self.board) else '666'
            left = str(board[index - 1]) if index - 1 >= 0 else '666'
            over_left = str(board[index - 2]) if index - 2 >= 0 and left == '#' else '666'
            top = str(board[index - 9]) if index - 9 >= 0 else '666'
            over_top = str(board[index - (9 * 2)]) if index - (9 * 2) >= 0 and top == '#' else '666'
            if str(elem).isdigit():
                if (right.isdigit() and index != 9 and int(elem) + int(right) == 10) or elem == right != '#':
                    ways += 1
                if (bottom.isdigit() and int(elem) + int(bottom) == 10) or elem == bottom != '#':
                    ways += 1
                if (left.isdigit() and int(elem) + int(left) == 10) or elem == left != '#':
                    ways += 1
                if (top.isdigit() and int(elem) + int(top) == 10) or elem == top != '#':
                    ways += 1
                if (over_bottom.isdigit() and int(elem) + int(over_bottom) == 10) or elem == over_bottom != '#':
                    ways += 1
                if (over_top.isdigit() and int(elem) + int(over_top) == 10) or elem == over_top != '#':
                    ways += 1
                if (over_left.isdigit() and int(elem) + int(over_left) == 10) or elem == over_left != '#':
                    ways += 1
                if (over_right.isdigit() and int(elem) + int(over_right) == 10) or elem == over_right != '#':
                    ways += 1
            else:
                pass

        self.current_ways = int(ways)
        if len(self.board) < 17 and self.current_ways == 0:
            self.statement = False
            print('Количество попыток:', self.statement)
            return exit('Поздравляем с победой!')
        elif self.current_ways == 0:
            self.transform()

        if state:
            print(f'Осталось свободных чисел: {self.current_ways}')

    def choice(self, point_number: str) -> None:  # Функция выбора пользователя
        row, column = self._input(point_number)
        point = row * 9 + column
        self.board[point] = '#'
        if point_number == 'второго' and self.current_ways != 0:
            print()
            self.show()

    def transform(self) -> None:  # Трансформирует поле при нуле возможных вариантов
        board = []
        for index, element in enumerate(self.board):
            if element.isdigit():
                board.append(element)
        self.current_ways = 666
        self.already_visited = list()
        self.board = board
        self.check_ways(state=False)
        if self.current_ways == 0:
            self.statement = False
            print('Количество попыток:', self.statement)
            return exit('Поздравляем, победа!')
        self.show()


if __name__ == '__main__':
    # noinspection SpellCheckingInspection
    """
    ◈ Author: Pikalov Nikolai ◈
    ◈ Group: PI21-7 ◈
    """
    gm = Game()
    gm.game_board()
    gm.show()
    print('Осталось 16 свободных чисел формирующих пары')
    while gm.statement:
        gm.attempts += 1
        gm.choice('первого')
        gm.choice('второго')
        gm.check_ways()
