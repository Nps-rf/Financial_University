import pygame
from Board import Table
from Engine import Engine
from Build import Build


class Main(Engine):
    """
    Creates an application
    """
    def __init__(self):
        super().__init__()
    FPS = 24
    images = Build.load_images()
    running = True

    @classmethod
    def _prepare_(cls):
        """
        Function that prepares an application for launch
        :return:
        """
        pygame.init()
        pygame.mixer.init()
        cls.screen = pygame.display.set_mode(cls.RATIO)
        pygame.display.set_caption('Chess')
        cls.clock = pygame.time.Clock()
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
            Support.is_running()
            Graphics.create_board()
            pygame.display.flip()  # Updates a screen


class Support(Main):
    @staticmethod
    def is_running() -> None:
        """
        Checks whether the user clicked on the cross
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Main.running = False


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
        board = Table().field
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


if __name__ == '__main__':
    CHESS_GAME = Engine()
    CHESS_GAME.run(size='medium')
