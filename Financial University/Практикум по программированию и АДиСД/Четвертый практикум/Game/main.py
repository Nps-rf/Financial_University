import pygame
from Board import Table
from Engine import Engine
from Build import Build
Table = Table()


class Main(Engine):
    """
    Creates an application
    """
    def __init__(self):
        super().__init__()

    images = Build.load_images()
    running = True
    FPS = 30

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
    chose = False
    piece = ('--', [-1, -1])

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
                    print(True, Table.field[y][x])
                    cls.chose = True
                    cls.piece = (Table.field[y][x], [y, x])

                if Table.field[y][x] == '--' and cls.chose:
                    print(Table.field[y][x])
                    Table.field[y][x] = cls.piece[0]
                    Table.field[cls.piece[1][0]][cls.piece[1][1]] = '--'
                    cls.chose = False

                print(f'x = {x}, y = {y}')


class Rules:
    @staticmethod
    def pawn(p_x, p_y):
        """
        :param p_x: Horizontal coordinate of piece
        :param p_y: Vertical coordinate of piece
        :return:
        """
        pass


if __name__ == '__main__':
    CHESS_GAME = Engine()
    CHESS_GAME.run(size='medium')
