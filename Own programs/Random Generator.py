from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from random import shuffle, choice
from string import ascii_letters, digits
from typing import Callable, Any
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput


class Password:
    """
    Takes at least 4 optional arguments
    1) length: int -> length of the password
        1.1) Value must be more then 7
    2) Numbers: bool -> (extra optionally). set a 'including Numbers' statement
        2.1) if False: Generator returns a password without Numbers
            2.1.1) if False and all other statements also False, do not generates password
        2.2) if True: Generator returns a password with Numbers
    3) alphas: bool -> set a 'including letters' statement
        3.1) if False: Generator returns a password without letters
        3.2) if True: Generator returns a password with letters
    4) symbols: bool -> set a 'including special letters' statement
        4.1) if False: Generator returns a password without special letters
        4.2) if True: Generator returns a password with special letters
    """
    def __init__(self, length: int = 12, numbers: bool = True, alphas: bool = False, symbols: bool = False) -> None:
        if length >= 8:
            self.length = length
        else:
            self.length = 8
        self.digit = numbers
        self.alpha = alphas
        self.symbols = symbols

    def generate(self) -> str:  # process of generating the password
        while True:
            password = ''
            characters = []
            if self.digit:
                characters += digits
            if self.alpha:
                characters += ascii_letters
            if self.symbols:
                characters += ['-', '-']
            shuffle(characters)
            for _ in range(self.length):
                while True:
                    random_value = choice(characters)
                    if len(password) == 0:
                        password += random_value
                        break
                    elif str(random_value) != password[-1]:
                        password += random_value
                        break
            if self._is_correct(password):  # test-recursion
                return password

    def _is_correct(self, password: str) -> bool:  # is password correct
        tests = []
        if self.digit:
            is_digits: Callable[[Any], Any] = lambda x: x.isdigit()
            tests.append(is_digits)
        elif self.alpha:
            is_alphas: Callable[[Any], Any] = lambda x: x.isalpha()
            tests.append(is_alphas)
        for test in tests:
            if not any(list(map(test, password))):
                return False
        if self.symbols and len(set(password) & set('-')) >= 1:
            if password[0] != '-' and password[-1] != '-':
                return True
            else:
                return False
        elif self.symbols:
            return False
        return True


class GeneratorApp(App):
    def __init__(self, **kwargs):  # Do not important things
        super().__init__(**kwargs)
        self.lbl = None
        self.generator = None
        self.gain_symbols = False
        self.gain_alphas = False
        self.slider = Slider(value_track=True, min=8, max=32, value=12, value_track_color=[1, 0, 0, 1],
                             sensitivity='handle')
        self.old_value = self.slider.value
        self.lbl2 = Label
        self.generate_button = Button
        self.letters_button = Button
        self.special_letters_button = Button

    def build(self) -> BoxLayout:
        self.lbl2 = Label(text=f'Password length: {round(self.slider.value)}', font_size=24)
        self.slider = Slider(value_track=True, min=8, max=32, value=12, value_track_color=[1, 0, 0, 1],
                             sensitivity='handle', on_touch_move=self.update_header_label)
        b1 = BoxLayout(orientation='vertical')
        b1.add_widget(self.lbl2)
        b1.add_widget(self.slider)
        self.lbl = TextInput(font_size=28, background_color=(0, 0, 0), foreground_color=(1, 1, 1), readonly=True,
                             cursor_blink=False, cursor_color=(0, 0, 0), halign='center')
        b1.add_widget(self.lbl)
        self.generate_button = Button(text='Generate', font_size=20,
                                      on_press=self.update_label)
        b1.add_widget(self.generate_button)
        self.letters_button = Button(text='Add letters', font_size=20,
                                     on_press=self._gain_alphas,)
        b1.add_widget(self.letters_button)
        self.special_letters_button = Button(text='Add special symbols', font_size=20,
                                             on_press=self._gain_symbols)
        b1.add_widget(self.special_letters_button)
        return b1

    def update_header_label(self, *args):  # updates Password length Label
        """

        :type args: Garbage
        """
        self.lbl2.text = f'Password length: {round(self.slider.value)}'
        value = round(self.slider.value)
        if 8 <= value <= 14:
            self.slider.value_track_color = (1, 0, 0)
        elif 14 < value <= 19:
            self.slider.value_track_color = (1, 1, 0)
        elif 19 < value:
            self.slider.value_track_color = (0, 1, 0)

    def update_label(self, *args) -> None:  # update password output
        """

        :type args: Garbage
        """
        self.generator = Password(length=round(self.slider.value), alphas=self.gain_alphas, symbols=self.gain_symbols)
        self.lbl.text = self.generator.generate()

    def _gain_alphas(self, instance: bool) -> None:  # controls alphas including
        if self.gain_alphas:
            self.gain_alphas = False
            self.letters_button.background_color = (1, 1, 1, 1)
            return
        self.gain_alphas = instance
        self.letters_button.background_color = (0, 255, 0, 0.75)

    def _gain_symbols(self, instance: bool) -> None:  # controls special letters including
        if self.gain_symbols:
            self.gain_symbols = False
            self.special_letters_button.background_color = (1, 1, 1, 1)
            return
        self.gain_symbols = instance
        self.special_letters_button.background_color = (0, 255, 0, 0.75)


if __name__ == '__main__':
    GeneratorApp().run()
