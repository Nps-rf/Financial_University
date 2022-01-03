import pygame
from Board import Table


class Build:
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

    @classmethod
    def run(cls):
        Chess = Main()
        Chess.run()


class Main(Engine):
    def __init__(self):
        super().__init__()
    FPS = 24
    images = Build.load_images()
    running = True

    @classmethod
    def _prepare_(cls):
        pygame.init()
        pygame.mixer.init()
        cls.screen = pygame.display.set_mode(cls.RATIO)
        pygame.display.set_caption('Chess')
        cls.clock = pygame.time.Clock()
        pass

    @classmethod
    def run(cls):
        while cls.running:
            cls._prepare_()
            Support.is_running()
            Graphics.create_board()
            pygame.display.flip()


class Support(Main):
    @staticmethod
    def is_running():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Main.running = False


class Graphics(Main):
    @classmethod
    def create_board(cls):  # whole process in couple
        cls._board_()
        cls._pieces_()

    @classmethod
    def _board_(cls):  # squares
        colors = [pygame.Color('white'), pygame.Color('dark gray')]
        for row in range(cls.DIMENSIONS):
            for col in range(cls.DIMENSIONS):
                color = colors[((row + col) % 2)]
                pygame.draw.rect(
                    super().screen,
                    color,
                    pygame.Rect(
                        col * cls.SQUARE_SIZE,
                        row * cls.SQUARE_SIZE,
                        cls.SQUARE_SIZE,
                        cls.SQUARE_SIZE)
                                )

    @classmethod
    def _pieces_(cls):  # pieces
        board = Table().field
        for row in range(cls.DIMENSIONS):
            for col in range(cls.DIMENSIONS):
                piece = board[row][col]
                if piece != '--':  # if not empty square
                    super().screen.blit(
                        cls.images[piece],
                        pygame.Rect(
                            col * cls.SQUARE_SIZE + 12,
                            row * cls.SQUARE_SIZE + 12,
                            cls.SQUARE_SIZE,
                            cls.SQUARE_SIZE)
                                    )



if __name__ == '__main__':
    Engine.run()
