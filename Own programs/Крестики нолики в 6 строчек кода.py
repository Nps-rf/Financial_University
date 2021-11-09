from itertools import cycle
field = [[[] for h in range(3)] for i in range(3)]
for attempts, x in enumerate(cycle(['X', '0'])):
    printer, a = [print('  1  2  3'), [print(n, *i) for i, n in zip(field, range(1, 4))]], input('Введите координаты: ')
    field[int(a.split()[0]) - 1][int(a.split()[1]) - 1] = x if (len(a.split()) == 2 and a.split()[0].isdigit() and a.split()[1].isdigit() and 0 < int(a.split()[0]) < 4 and 0 < int(a.split()[1]) < 4) else exit('Я не терплю ошибок')
    exit(f'Поздравляю {x} с победой!') if (field[0][0] == x and field[1][1] == x and field[2][2] == x) or (any([all(map(lambda g: g == x, field[0])), all(map(lambda g: g == x, field[1])), all(map(lambda g: g == x, field[2]))])) or ((field[0][0] == x and field[1][0] == x and field[2][0] == x) or (field[0][1] == x and field[1][1] == x and field[2][1] == x) or (field[0][2] == x and field[1][2] == x and field[2][2] == x)) else exit('Ничья') if attempts == 8 else print(end='')