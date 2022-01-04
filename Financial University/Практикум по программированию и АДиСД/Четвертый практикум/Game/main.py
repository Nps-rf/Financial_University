import pygame
from Board import Table
from Engine import Engine
from Build import Build
Table = Table()


class Player:
    def __init__(self, letter='w'):
        self.score = 0
        self.letter = letter


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
    BLACK = Player(letter='b')

    @classmethod
    def _prepare_(cls):
        """
        Function that prepares an application for launch
        """
        pygame.init()
        pygame.mixer.init()
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
            Graphics.create_board()
            Controls.run_controls()
            pygame.display.update()  # Updates a screen


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


class Controls(Main):
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
                """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Main.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0] // (cls.RATIO[0] // cls.DIMENSIONS)
                y = event.pos[1] // (cls.RATIO[0] // cls.DIMENSIONS)

                if Table.field[y][x] != '--':
                    cls.chose = True
                    coordinates = [cls.y, cls.x] = y, x
                    cls.piece = (Table.field[y][x], coordinates)

                if Table.field[y][x] == '--' and cls.chose:

                    available = Rules.pawn(cls.x, cls.y)

                    if x in available[0] and y in available[1] and cls.current_player.letter == cls.piece[0][0]:

                        Table.field[y][x] = cls.piece[0]

                        Table.field[cls.piece[1][0]][cls.piece[1][1]] = '--'

                        cls.chose = False

                        if cls.current_player.letter == 'w':
                            print(False)
                            cls.current_player = super().BLACK

                        elif cls.current_player.letter == 'b':
                            print(True)
                            cls.current_player = super().WHITE

                print(f'x = {x}, y = {y}', cls.current_player.letter)


class Rules:
    @staticmethod
    def pawn(p_x, p_y):
        """
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        if Table.field[p_y][p_x][0] == 'b':
            if p_y == 1:
                return [p_x], [p_y + 1, p_y + 2]
            return [p_x], [p_y + 1]
        if p_y == 6:
            return [p_x], [p_y - 1, p_y - 2]
        return [p_x], [p_y - 1]

    @staticmethod
    def knight(p_x, p_y):
        """
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        pass

    @staticmethod
    def bishop(p_x, p_y):
        """
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        pass

    @staticmethod
    def rook(p_x, p_y):
        """
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        pass

    @staticmethod
    def queen(p_x, p_y):
        """
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        pass

    @staticmethod
    def king(p_x, p_y):
        """
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return: coordinates available
        """
        pass


if __name__ == '__main__':
    CHESS_GAME = Engine()
    CHESS_GAME.run(size='medium')
