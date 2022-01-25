class Player:
    __slots__ = ('name', 'letter', 'opposite')

    def __init__(self, letter: str = 'w', opposite: str = 'b', name: str = 'White') -> None:
        # self.score = 0  TODO
        self.name = name
        self.letter = letter
        self.opposite = opposite

    def __repr__(self):
        return f'{self.__class__}: {self.name}'

    def __str__(self):
        return self.name
