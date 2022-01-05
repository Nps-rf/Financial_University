import pygame
from Board import Table
from Engine import Engine
from Build import Build
Table = Table()


class Player:
    def __init__(self, letter='w', opposite='b'):
        self.score = 0
        self.letter = letter
        self.opposite = opposite


class Main(Engine):
    """
    Creates an application
    """
    def __init__(self):
        super().__init__()

    images = Build.load_images()
    running = True
    FPS = 30
    WHITE = Player()
    BLACK = Player(letter='b', opposite='w')

    @classmethod
    def _prepare_(cls):
        """
        Function that prepares an application for launch
        """
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        cls.screen = pygame.display.set_mode(cls.RATIO)
        pygame.display.set_caption('Chess')
        pass

    @classmethod
    def run(cls, **kwargs):
        """
        The main function for launching the application
        :param kwargs:
        :return: pygame application
        """
        while cls.running:
            cls._prepare_()
            Sound.init()
            Graphics.create_board()
            Controls.run_controls()
            pygame.display.update()  # Updates a screen


class Sound:
    @classmethod
    def init(cls):
        pygame.mixer.init()
        cls.move_sound = pygame.mixer.Sound('Sound/move of piece.ogg')
        cls.beat_sound = pygame.mixer.Sound('Sound/peace beaten.ogg')


class Graphics(Main):
    """
    The class responsible for the graphical component of the application
    """
    @classmethod
    def create_board(cls):  # whole process in couple
        """
        The main function for creating board and putting a pieces
        """
        cls._board_()
        cls._pieces_()

    @classmethod
    def _board_(cls):
        colors = [pygame.Color('white'), pygame.Color('dark gray')]
        for row in range(cls.DIMENSIONS):
            for col in range(cls.DIMENSIONS):
                color = colors[((row + col) % 2)]  # Implementation Color Switching
                pygame.draw.rect(
                    super().screen,
                    color,
                    pygame.Rect(
                        col * cls.SQUARE_SIZE,  # Horizontal coordinate
                        row * cls.SQUARE_SIZE,  # Vertical coordinate
                        cls.SQUARE_SIZE,  # Size of square
                        cls.SQUARE_SIZE)  # Size of square
                                )

    @classmethod
    def _pieces_(cls):
        """
        Put a pieces on board
        """
        board = Table.field
        for row in range(cls.DIMENSIONS):
            for col in range(cls.DIMENSIONS):
                piece = board[row][col]
                if piece != '--':  # if not empty square
                    super().screen.blit(
                        cls.images[piece],  # Picture of piece
                        pygame.Rect(
                            col * cls.SQUARE_SIZE + super().expand,  # Horizontal coordinate
                            row * cls.SQUARE_SIZE + super().expand,  # Vertical coordinate
                            cls.SQUARE_SIZE,  # Size of square
                            cls.SQUARE_SIZE)  # Size of square
                                    )


class Controls(Main, Sound):
    current_player = Main.WHITE
    chose = False
    piece = ('--', [-1, -1])
    x = None
    y = None

    @classmethod
    def run_controls(cls):
        cls._look4click_()

    @classmethod
    def _look4click_(cls):
        """
        Checks whether the user clicked on the cross (or other place)
        It's the biggest trash i've ever made
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Main.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0] // (cls.RATIO[0] // cls.DIMENSIONS)
                y = event.pos[1] // (cls.RATIO[0] // cls.DIMENSIONS)
                p_letter = cls.current_player.letter
                movements = {
                    'p': Rules.pawn,
                    'N': Rules.knight,
                    'B': Rules.bishop,
                    'R': Rules.rook,
                    'Q': Rules.queen,
                    'K': Rules.king
                }

                if Table.field[y][x] != '--' and Table.field[y][x][0] != cls.current_player.opposite:
                    cls.chose = True
                    coordinates = [cls.y, cls.x] = y, x
                    cls.piece = (Table.field[y][x], coordinates)
                if cls.x or cls.y is not None:
                    available = movements[cls.piece[0][1]](cls.x, cls.y, cls.current_player)

                    if cls.chose:  # figure chosen
                        print(available)
                        if [x, y] in available and p_letter == cls.piece[0][0]:  # movement of piece
                            print('PASSED')
                            if Table.field[y][x] == '--':
                                super().move_sound.play()
                            else:
                                super().beat_sound.play()
                            Table.field[y][x] = cls.piece[0]

                            Table.field[cls.piece[1][0]][cls.piece[1][1]] = '--'

                            cls.chose = False
                            cls.current_player = super().BLACK if p_letter == 'w' else super().WHITE
                        print(Table.field[y][x][0], cls.current_player.opposite)

                print(f'x = {x}, y = {y}')


class Rules:
    @staticmethod
    def pawn(p_x, p_y, *_):
        """
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        # Movement section
        available = []
        if Table.field[p_y + 1][p_x] == '--':
            if p_y == 1:
                available.append([p_x, p_y + 2])
                available.append([p_x, p_y + 1])
            else:
                available.append([p_x, p_y + 1])
        if Table.field[p_y - 1][p_x] == '--':
            if p_y == 6:
                available.append([p_x, p_y - 1])
                available.append([p_x, p_y - 2])
            else:
                available.append([p_x, p_y - 1])
        # White Beat section
        if Table.field[p_y][p_x][0] == 'w':
            try:
                if Table.field[p_y - 1][p_x - 1][0] == 'b':
                    available.append([p_x - 1, p_y - 1])
            except IndexError:
                pass

            try:
                if Table.field[p_y - 1][p_x + 1][0] == 'b':
                    available.append([p_x + 1, p_y - 1])
            except IndexError:
                pass

        # Black Beat section?
        if Table.field[p_y][p_x][0] == 'b':
            try:
                if Table.field[p_y + 1][p_x - 1][0] == 'w':
                    available.append([p_x - 1, p_y + 1])
            except IndexError:
                pass

            try:
                if Table.field[p_y + 1][p_x + 1][0] == 'w':
                    available.append([p_x + 1, p_y + 1])
            except IndexError:
                pass

        return available

    @staticmethod
    def knight(p_x, p_y, player):
        """
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        table = Table.field
        available = []

        # leftward
        try:
            if table[p_y - 1][p_x - 2][0] != player.letter:
                available.append([p_x - 2, p_y - 1])
        except IndexError:
            pass
        try:
            if table[p_y + 1][p_x - 2][0] != player.letter:
                available.append([p_x - 2, p_y + 1])
        except IndexError:
            pass
        # above
        try:
            if table[p_y - 2][p_x - 1][0] != player.letter:
                available.append([p_x - 1, p_y - 2])
        except IndexError:
            pass
        try:
            if table[p_y - 2][p_x + 1][0] != player.letter:
                available.append([p_x + 1, p_y - 2])
        except IndexError:
            pass

        # on the right
        try:
            if table[p_y - 1][p_x + 2][0] != player.letter:
                available.append([p_x + 2, p_y - 1])
        except IndexError:
            pass
        try:
            if table[p_y + 1][p_x + 2][0] != player.letter:
                available.append([p_x + 2, p_y + 1])
        except IndexError:
            pass
        # below
        try:
            if table[p_y + 2][p_x - 1][0] != player.letter:
                available.append([p_x - 1, p_y + 2])
        except IndexError:
            pass
        try:
            if table[p_y + 2][p_x + 1][0] != player.letter:
                available.append([p_x + 1, p_y + 2])
        except IndexError:
            pass
        return available

    @staticmethod
    def bishop(p_x, p_y, *_):
        """
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """

        pass

    @staticmethod
    def rook(p_x, p_y, *_):
        """
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        pass

    @staticmethod
    def queen(p_x, p_y, *_):
        """
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        pass

    @staticmethod
    def king(p_x, p_y, *_):
        """
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        pass


if __name__ == '__main__':
    CHESS_GAME = Engine()
    CHESS_GAME.run(size='medium')
