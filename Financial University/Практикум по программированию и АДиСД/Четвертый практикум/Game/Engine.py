class Engine:
    """
    Abbreviations scheme:
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
        from main import Main
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
