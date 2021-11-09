from time import sleep
from math import sqrt, pow


def evaluator() -> str:  # 1
    """
    IN[1] -> (1 + 2i) + (4 + 5i)
    OUT[1] -> (5 + 7i)
    ----------------------------------------------------
    Solving arithmetical operations with complex numbers.
    returns str
    """
    sleep(1)
    print('Пример: (1 + 2i) + (4 + 5i) = (5 + 7i)')
    sleep(1)
    inp = user_in()
    return f'Ответ: {str(eval(inp.replace("i", "j"))).replace("j", "i")}'


def user_in() -> str:
    """
    Input controller, return str class.
    Checks the input for compliance with the format of complex numbers.
    If wrong, return input attempt for user.
    """
    print(
        '___________________________________________ПРИМЕЧАНИЕ_____________________________________________',
        'В вычислениях предпочтительно использовать латинскую букву i '
        'в качестве обозначения мнимой единицы', sep='\n')
    sleep(1)
    print('Что нужно вычислить?')
    while True:
        inp = input()
        try:
            inp = str(complex(eval(inp.replace("i", "j"))))
            inp = str(complex(inp.replace("i", "j")))
            break
        except ValueError and ZeroDivisionError:
            print('Я просил нормальный пример!')
            continue
    return inp


def choice_selection() -> bool:
    """
    The function of continuing the program.
    returns boolean statements
    """
    sleep(1)
    print('Посчитать что-то ещё?')
    sleep(1)
    print('Ответь просто: да или нет')
    answer = input().lower()
    if answer == 'да':
        return True
    elif answer == 'нет':
        print('Ладно, пока(')
        return False
    else:
        print('Ай, не понял ничего, ну и ладно)')
        return False


def trig_form() -> str:  # 2
    """
    Presenting raw trigonometric form of a complex number.
    cos and sin reduced to a 5-digit entry.
    """
    num = complex(user_in())
    x = num.imag
    y = num.real
    r = abs(sqrt(pow(x, 2) + pow(y, 2)))
    cos_ = x / r
    sin_ = y / r
    return f'{r} + ({str(cos_)[:5]} + i({str(sin_)[:5]}))'


def complex_sqrt() -> str:  # 3 WIP
    """
    Presenting raw root-form of a complex number.
    Non-reduced
    """
    num = complex(user_in())
    while True:
        print('Введите степень')
        degree = input()
        if degree.isdigit() and degree != '0':
            degree = float(degree)
            break
    return str(num ** (1 / degree)).replace("j", "i")


def complex_calc() -> bool:
    """
    Initial controlling point of the program.
    """
    print('Выберите режим работы:', '1) Арифметические операции (за исключением корня из числа)',
          '2) Представление комплексного числа в тригонометрической форме',
          '3) Корень n-й степени из комплексного числа', sep='\n')
    choice = input()
    if choice == '1':
        print(evaluator())
        return choice_selection()
    elif choice == '2':
        print(trig_form())
        return choice_selection()
    elif choice == '3':
        print(complex_sqrt())
        return choice_selection()
    else:
        print('Не справиться с вводом одной цифры от 1 до 3...\nЯ думаю комплексные числа будут ещё труднее.')
        global control
        control = False


if __name__ == "__main__":
    # noinspection SpellCheckingInspection
    """
    Author: Nikolai Pikalov
    Group: PI21-7
    """
    while True:
        control = complex_calc()
        if not control:
            break
