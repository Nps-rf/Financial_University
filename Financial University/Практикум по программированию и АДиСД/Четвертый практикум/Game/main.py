import pygame
from Board import Table


class Build:
    """
    Class for external operations
    """
    @staticmethod
    def load_images():
        images = dict()
        pieces = ['wK', 'wQ', 'wN', 'wR', 'wB', 'wp', 'bK', 'bQ', 'bN', 'bR', 'bB', 'bp']
        for piece in pieces:
            images[piece] = pygame.image.load('Pieces/' + piece + '.png')
        return images


class Engine:
    """
    Abbreviations scheme
    ◈ First letter -> color of piece
    ◈ Second letter -> exact piece
    Example:
        ◈ wK -> White King
    Pieces:
        ◈ K -> King (Король)
        ◈ Q -> Queen (Ферзь)
        ◈ R -> Rook (Ладья)
        ◈ B -> Bishop (Слон)
        ◈ N -> Knight (Конь)
        ◈ P -> Pawn (Пешка)
    """
    RATIO = (WIDTH, HEIGHT) = (720, 720)
    DIMENSIONS = 8
    SQUARE_SIZE = WIDTH // DIMENSIONS
    expand = 6 * 2  # The error for the screen resolution (so that the figures do not move out)

    @classmethod
    def run(cls, size='medium'):
        if size == 'small':
            cls.RATIO = (WIDTH, HEIGHT) = (512, 512)
            cls.expand = 6 * 0
            cls.SQUARE_SIZE = WIDTH // cls.DIMENSIONS
        elif size == 'big':
            cls.RATIO = (WIDTH, HEIGHT) = (1024, 1024)
            cls.expand = 6 * 5
            cls.SQUARE_SIZE = WIDTH // cls.DIMENSIONS
        Chess = Main()
        Chess.run()


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
        :return: PYGAME APP
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
    CHESS_GAME.run(size='big')
