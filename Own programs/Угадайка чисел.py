import random

good_answers = ['да', 'давай', 'го', 'погнали', 'желаю', 'хочу', 'запускай', 'конечно', 'с удовольствием', 'гоу',
                'ну давай', 'ладно', 'даа', 'дааа', 'гоо']


def choose_level() -> str:
    difficulty = input()
    Flag = True
    while Flag : # Выбор сложности
        if difficulty.isdigit() :
            if difficulty in ['1', '2', '3'] :
                print('Отлично!')
                if difficulty == '1' :
                    print('Введите число от 1 до 100')
                if difficulty == '2' :
                    print('Введите число от 1 до 250')
                if difficulty == '3' :
                    print('Введите число от 1 до 777')
                Flag = False
            else :
                print('Введите пожалуйста целое число от 1 до 3, это вроде бы не так сложно) (◕‿◕)')
                difficulty = input()
        else :
            print(f'Вы ввели не число "{difficulty}. Введите число от 1 до 3)')
            difficulty = input()

    return difficulty


def is_valid(insert: str, difficulty: str) -> bool: # Защита от дурака
    if insert.isdigit():
        if difficulty   == '1':
            if int(insert) >= 1 and int(insert) <= 100 :
                return True
        
        elif difficulty == '2':
            if int(insert) >= 1 and int(insert) <= 250 :
                return True
        
        elif difficulty == '3':
            if int(insert) >= 1 and int(insert) <= 777 :
                return True
        
        else:
            return False
    else:
        return False
        

def good_solver(answer: str) -> bool: # Ветвь решения пользователя
    global good_answers
    
    if answer.lower() in good_answers :
        return True
    else:
        print('Прощайте! Ещё увидимся...')
        return False


def numeric_guesser(difficulty: str) -> bool: # Игра
    attempts = 0
    k = 0

    if difficulty   == '1' :
        n = random.randint(1, 100)
    elif difficulty == '2' :
        n = random.randint(1, 250)
    elif difficulty == '3' :
        n = random.randint(1, 777)

    else:
        raise Exception()

    while k != n :
        k = input()
        if k.lower() in ['я сдаюсь', 'хватит', 'стоп'] :
            print('Эхх, я загадал число', n)
            return False

        attempts += 1
        if is_valid(k, difficulty) :
            if int(k) < n :
                print('Ваше число меньше загаданного, попробуйте ещё разок)')
            elif int(k) == n :
                print('Вы угадали, поздравляем!\n'
                     f'Количество попыток: {attempts}\n'
                      'Спасибо, что играли в числовую угадайку. Не желаете сыграть ещё разок?\n')
                answer = input()
                return good_solver(answer)
            elif int(k) > n :
                print('Ваше число больше загаданного, попробуйте ещё разок) ')
            
            else:
                raise Exception()

        else :
            print('А может всё таки введем целое число которое ещё и в диапазоне лежит? ¯\_(ツ)_/¯')


def hello_message():
    print('▌ Добро пожаловать в числовую угадайку! ▌\n'
          'Выберите сложность:\n'
          '1) Пара попыток и я победитель! (Подходит для тех, кто не хочет тратить время на угадывание |1 до 100| ✪\n'
          '2) Ну это чуток посложнее, но тоже легко. (Подходит для каждого) |1 до 250| ✪✪\n'
          '3) Попыток будет много...  (Я думаю описание не нужно) |1 до 777| ✪✪✪\n')


if __name__ == "__main__":
    while True:
        hello_message()

        difficulty = choose_level()

        stay_in_game = numeric_guesser(difficulty)

        if not stay_in_game:
            break
    
