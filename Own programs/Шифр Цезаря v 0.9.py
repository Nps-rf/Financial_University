ru_alphabet = [chr(i) for i in range(ord('а'), ord('я') + 1)]
ru_h_alphabet = [chr(i) for i in range(ord('А'), ord('Я') + 1)]
eng_alphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)]
eng_h_alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)]


def decoder(new_string, sdvig, string, alpha_low, alpha_high, control_ords, control_value) :
    for i in string :
        if i.isalpha() :
            if i in alpha_low and ord(i) - sdvig >= ord(control_ords[0]) :
                new_string += chr(ord(i) - sdvig)
            elif i in alpha_high and ord(i) - sdvig >= ord(control_ords[1]) :
                new_string += chr(ord(i) - sdvig)
            else :
                new_string += chr(ord(i) - sdvig + control_value)
        else :
            new_string += i
    return new_string


def caesar() :
    print('Что нужно сделать:', '1 - кодировать', '2 - декодировать', '3 - декодировать перебором', sep='\n')
    way = input()
    print('Выберите язык текста для работы:', '1 - английский', '2 - русский', sep='\n')
    language = input()
    print('Введите текст:')
    string = input()
    if way != '3' :
        print('Введите необходимый сдвиг:')
        sdvig = int(input())
    else :
        sdvig = None
    new_string = ''

    def process(way, language, string, sdvig, new_string) :
        if language == '1' :
            control_ords = ['a', 'A', 'z', 'Z']
            control_value = 26
            alpha_low = eng_alphabet
            alpha_high = eng_h_alphabet
        elif language == '2' :
            control_ords = ['а', 'А', 'я', 'Я']
            control_value = 32
            alpha_low = ru_alphabet
            alpha_high = ru_h_alphabet
        if way == '1' :
            for i in string :
                if i.isalpha() :
                    if i in alpha_low and ord(i) + sdvig <= ord(control_ords[2]) :
                        new_string += chr(ord(i) + sdvig)
                    elif i in alpha_high and ord(i) + sdvig <= ord(control_ords[3]) :
                        new_string += chr(ord(i) + sdvig)
                    else :
                        new_string += chr(ord(i) + sdvig - control_value)
                else :
                    new_string += i
        elif way == '2' :
            decoder(new_string, sdvig, string, alpha_low, alpha_high, control_ords, control_value)
        elif way == '3' :
            for j in range(1, len(alpha_low) + 1) :
                new_string = ''
                sdvig = j
                decoder(new_string, sdvig, string, alpha_low, alpha_high, control_ords, control_value)
                if sdvig in [1, 21] :
                    print(
                        f'Расшифровка для сдвига в {sdvig} символ влево: {decoder(new_string, sdvig, string, alpha_low, alpha_high, control_ords, control_value)}')
                elif sdvig in [2, 3, 4, 22, 23, 24] :
                    print(
                        f'Расшифровка для сдвига в {sdvig} символа влево: {decoder(new_string, sdvig, string, alpha_low, alpha_high, control_ords, control_value)}')
                else :
                    print(
                        f'Расшифровка для сдвига в {sdvig} символов влево: {decoder(new_string, sdvig, string, alpha_low, alpha_high, control_ords, control_value)}')
        if way != '3' :
            print('Результат работы:', f'|| {new_string} ||', sep='\n')
        elif way == '2' :
            print('Результат работы:',
                  f'|| {decoder(new_string, sdvig, string, alpha_low, alpha_high, control_ords, control_value)} ||',
                  sep='\n')

    process(way, language, string, sdvig, new_string)


############
caesar()  #
############
