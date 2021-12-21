"""
◈ Вариант 2
1) В большинстве случаев -> csv, но редко -> pickle
>>> import csv
>>> import pickle
2) Используем для этого библиотеку pickle
>>> import pickle
Определяем данные для сохранения
>>> data = {
>>> 'a': [1, 2.0, 3, 4+6j],
>>> 'b': ("character string", b"byte string"),
>>> 'c': {None, True, False}}
Используем менеджер контекста и функцию dump из модуля pickle для создания файла
>>> with open('data.pickle', 'wb') as file:  # режим wb в данном случае очень важен, почитайте про него отдельно
>>>     pickle.dump(data, file)
Для загрузки файла иcпользуем тоже самое, но с заменой функции на load
>>> with open('data.pickle', 'rb') as file:  # режим rb в данном случае очень важен, почитайте про него отдельно
>>>     data = pickle.load(file)
Pickle сам дропает исключения, свои.
3)
>>> with open('data.pickle', 'wb') as file:
>>>     array = list()
>>>     all_lines = file.readlines()
>>>     for line in all_lines:
>>>         for element in line:
>>>             array.append(int(element)) if str(element).isdigit() else array.append(str(element))
4)
>>> import math
>>> a : int  # это для себя пометка
>>> array = [[int((math.log2(a)) % 6), a] for a in range(50, 600 + 1) if a in (64, 128, 256, 512)]  # Попросили написать
            ⡴⠑⡄⠀⠀⠀⠀⠀⠀⠀ ⣀⣀⣤⣤⣤⣀⡀
            ⠸⡇⠀⠿⡀⠀⠀⠀⣀⡴⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀
            ⠀⠀⠀⠀⠑⢄⣠⠾⠁⣀⣄⡈⠙⣿⣿⣿⣿⣿⣿⣿⣿⣆
            ⠀⠀⠀⠀⢀⡀⠁⠀⠀⠈⠙⠛⠂⠈⣿⣿⣿⣿⣿⠿⡿⢿⣆
            ⠀⠀⠀⢀⡾⣁⣀⠀⠴⠂⠙⣗⡀⠀⢻⣿⣿⠭⢤⣴⣦⣤⣹⠀⠀⠀⢀⢴⣶⣆
            ⠀⠀⢀⣾⣿⣿⣿⣷⣮⣽⣾⣿⣥⣴⣿⣿⡿⢂⠔⢚⡿⢿⣿⣦⣴⣾⠸⣼⡿
            ⠀⢀⡞⠁⠙⠻⠿⠟⠉⠀⠛⢹⣿⣿⣿⣿⣿⣌⢤⣼⣿⣾⣿⡟⠉
            ⠀⣾⣷⣶⠇⠀⠀⣤⣄⣀⡀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
            ⠀⠉⠈⠉⠀⠀⢦⡈⢻⣿⣿⣿⣶⣶⣶⣶⣤⣽⡹⣿⣿⣿⣿⡇
            ⠀⠀⠀⠀⠀⠀⠀⠉⠲⣽⡻⢿⣿⣿⣿⣿⣿⣿⣷⣜⣿⣿⣿⡇
            ⠀⠀ ⠀⠀⠀⠀⠀⢸⣿⣿⣷⣶⣮⣭⣽⣿⣿⣿⣿⣿⣿⣿⠇
            ⠀⠀⠀⠀⠀⠀⣀⣀⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇
            ⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃
5)
>>> a = [1, 3, 5, 7, 9]
>>> b = [2, 4, 6, 8, 10]
>>> a = list(map(lambda x: sum(a) / len(a), a))
>>> b = list(map(lambda x: sum(b) / len(b), b))
"""