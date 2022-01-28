from pygame.mixer import init


class Sound:
    """
    Responsible for the sound operation in the program
    """
    __instance = None
    checkmate = None
    Knight_move = None
    check = None
    beat_sound = None
    move_sound = None
    King = None
    Queen = None
    Rook = None
    Bishop = None
    Knight = None
    Pawn = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def __load__(cls):
        from pygame.mixer import Sound
        cls.move_sound = Sound('Sound/move of piece.ogg')
        cls.beat_sound = Sound('Sound/peace beaten.ogg')
        cls.Knight_move = Sound('Sound/Knight movement.ogg')
        cls.Pawn = Sound('Sound/Pawn.ogg')
        cls.Rook = Sound('Sound/Rook.ogg')
        cls.Knight = Sound('Sound/Knight.ogg')
        cls.Queen = Sound('Sound/Queen.ogg')
        cls.Castle = Sound('Sound/Castle.ogg')
        cls.Bishop = Sound('Sound/Bishop.ogg')
        cls.King = Sound('Sound/King.ogg')
        cls.check = Sound('Sound/Check.ogg')
        cls.checkmate = Sound('Sound/Check Mate.ogg')

    @classmethod
    def init(cls):
        init()
        cls.__load__()

    @classmethod
    def play_sound(cls, name, muted):
        sounds = {
            'p': cls.Pawn.play,
            'N': cls.Knight.play,
            'B': cls.Bishop.play,
            'R': cls.Rook.play,
            'Q': cls.Queen.play,
            'K': cls.King.play,
            'move': cls.move_sound.play,
            'beat': cls.beat_sound.play,
            'check': cls.check.play,
            'Knight_move': cls.Knight_move.play,
            'checkmate': cls.checkmate.play
        }
        if not muted and name in sounds:
            sounds[name]()
