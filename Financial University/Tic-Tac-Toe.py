from typing import Callable, Any
from itertools import cycle, count
from time import sleep


class Game:
    def __init__(self):
        self.choice = None
        self.char = None
        self.name = None

    def check_win(self):
        global field
        func: Callable[[Any], bool] = lambda x: x == self.char
        for row in field:
            if all(list(map(func, row))):
                return True
        if all(list(map(func, [field[0][0], field[1][1], field[2][2]]))):
            return True
        elif all(list(map(func, [field[0][2], field[1][1], field[2][0]]))):
            return True
        elif all(list(map(func, [field[0][0], field[1][0], field[2][0]]))) or\
                all(list(map(func, [field[0][1], field[1][1], field[2][1]]))) or\
                all(list(map(func, [field[0][2], field[1][2], field[2][2]]))):
            return True
        else:
            return False

    @staticmethod
    def pprint() -> None:
        """
        Printing a game-field.
        :rtype: None
        """
        global field
        print(f'  1  2  3')
        for ind, row in enumerate(field):
            print(ind + 1, *row)

    def choose(self) -> None:
        self.choice = input().split()

    def switch(self) -> None:
        global field, already_been
        x, y = self.choice
        if self.char == 'X':
            field[x-1][y-1] = self.char
            already_been.append(list(map(str, self.choice)))
        else:
            field[x-1][y-1] = self.char
            already_been.append(list(map(str, self.choice)))

    # noinspection SpellCheckingInspection
    @property
    def iscorrect(self) -> bool:
        global already_been
        if self.choice not in already_been:
            is_all_digits: Callable[[str], str] = lambda let: let.isdigit()
            if len(self.choice) == 2 and all(list(map(is_all_digits, self.choice))):
                x, y = list(map(int, self.choice))
                if x in (1, 2, 3) and y in (1, 2, 3):
                    self.choice = list(map(int, self.choice))
                    return True
        return False


if __name__ == '__main__':
    # noinspection SpellCheckingInspection
    """
    Author: Pikalov Nikolai
    Group: PI21-7
    """
    player1 = Game()
    player2 = Game()
    player1.char = 'X'
    player2.char = 'O'
    player1.name = 'Крестик'
    player2.name = 'Нолик'
    field = [
        [[], [], []],
        [[], [], []],
        [[], [], []]
    ]
    already_been = []
    answers = ['Погоди, что-то не то, тебе не кажется?',
               'Так, мне казалось играть в крестики нолики было весьма простым занятием, видимо я ошибался',
               'Ты серьезно?',
               ]
    game_control = False
    print('Добро пожаловать в крестики-нолики!')
    sleep(2)
    for who, init_player in zip(cycle([player1.name, player2.name]), cycle([player1, player2])):
        if game_control:
            print('Поздравляем с победой!')
            break
        creating_attempts = 0
        Game.pprint()
        print(f'Ходит {who}!')
        for creating_attempts in count():
            if who == 'крестик':
                init_player = player1
            elif who == 'нолик':
                init_player = player2
            init_player.choose()
            if init_player.iscorrect:
                init_player.switch()
                game_control = init_player.check_win()
                break
            else:
                if creating_attempts < 3:
                    print(answers[creating_attempts])
                else:
                    print(exit('Господи...'))
