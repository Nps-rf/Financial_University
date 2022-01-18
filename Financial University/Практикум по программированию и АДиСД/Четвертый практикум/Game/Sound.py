class Sound:
    """
    Responsible for the sound operation in the program
    """

    @classmethod
    def init(cls):
        from pygame.mixer import init, Sound
        init()
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