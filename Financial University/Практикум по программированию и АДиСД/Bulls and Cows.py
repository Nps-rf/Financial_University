from typing import Callable
from random import randint
from time import sleep
from itertools import count


class Game:
    """
    Values must be 4 Numbers long
    Bull -> digit is in our hidden number and on it's position
    Cow ->  digit is in our hidden but not at right position
    Class for playing Bulls and Cows Game.
    """
    def __init__(self) -> None:
        self.value = None

    @staticmethod
    def greeting() -> None:  # Приветствие игрока
        greet = '\033[1mДобро пожаловать в игру "Быки и Коровы"!'
        for i in greet:  # этот цикл будет брать по 1 буковке из строки для иммитации печати
            sleep(0.2)
            print(i, end='', flush=True)
        sleep(1)
        print()
        print('Тебе прочитать правила?', sep='\n')
        choice = input()
        if choice.lower() in ['yes', 'да', 'ага', 'давай', 'го', '1']:
            rules = [
                '\033[1mХорошо, начну:',
                'Быки и коровы - логическая игра для двоих игроков',
                'В качестве оппонента, тебе будет предоставлен компьютер',
                'Каждый загадывает в тайне от оппонента четыре цифры без повторений',
                'Например, это может быть число 0834.',
                'Далее игроки по очереди делают ходы, то есть пытаются угадать задуманное противником число',
                'Но спрашивать они обязаны так же в виде четырёхзначного числа.',
                'К примеру нас спросят: "Твоё число 3094?".',
                'В ответ же мы должны сообщить количество быков и коров.',
                'Бык - это цифра, которая есть в нашем загаданном числе и находится на той же позиции.',
                'А корова - это цифра, которая так же есть в нашем числе, но находится не на своём месте.'
            ]
            for string in rules:
                print(string)
                sleep(2.5)
        else:
            print('\033[1mТогда начинаем')
            sleep(1)

    @staticmethod
    def see_bulls(p_value: str, b_value: str) -> int:  # возвращает количество быков
        counter = 0
        for first, second in zip(p_value, b_value):
            if first == second:
                counter += 1
        return counter

    @staticmethod
    def see_cows(p_value: str, b_value: str) -> int:  # возвращает количество коров
        counter = 0
        for first, second in zip(p_value, b_value):
            if first in b_value and first != second:
                counter += 1
        return counter

    def create(self) -> None:  # присваивает значение (для игрока)
        self.value = input()

    def create_opponent(self) -> None:  # присваивает значение (для компьютера)
        self.value = ''
        while len(self.value) < 4:
            curr = str(randint(0, 9))
            if curr not in self.value:
                self.value += curr

    @property
    def is_correct(self) -> bool:  # проверяет правильность ввода пользователем
        value = self.value
        is_all_digits: Callable[[str], str] = lambda x: x.isdigit()  # Является ли символ объекта числом?
        if len(value) == 4 and all(list(map(is_all_digits, value))) and len(set(value)) == len(value):
            return True
        else:
            return False


if __name__ == "__main__":
    # noinspection SpellCheckingInspection
    '''
    ◈ Author: Pikalov Nikolai ◈
    ◈ Group: PI21-7 ◈
    '''
    # Preparing
    player = Game()
    bot = Game()
    bot.create_opponent()
    attempts = 0
    Game.greeting()
    answers = ['\033[1m\033[31mПогоди, что-то не то, тебе не кажется?\n\033[0m',
               '\033[1m\033[31mТак, попробуй прочитать правила\n\033[0m',
               '\033[1m\033[31mТы серьезно?\n\033[0m',
               ]
    print('\033[1mНачинай отгадывать число, ведь втайне от тебя, компьютер уже загадал число!\n\033[0m')
    while True:
        for creating_attempts in count():  # Ввод пользователя и его проверка
            player.create()
            if player.is_correct:
                break
            else:
                if creating_attempts < 3:
                    print(answers[creating_attempts])
                else:
                    print(exit('\033[1m\033[31mГосподи...\n\033[0m'))
        if player.value != bot.value:
            attempts += 1
            bulls, cows = Game.see_bulls(player.value, bot.value), Game.see_cows(player.value, bot.value)
            print(f'\033[1mБыки: {bulls}  Коровы: {cows}', sep='\n')
        else:
            print('\033[1m\033[32mВау, ты угадал!!!', f'Количество попыток: {attempts}', sep='\n')
            break
