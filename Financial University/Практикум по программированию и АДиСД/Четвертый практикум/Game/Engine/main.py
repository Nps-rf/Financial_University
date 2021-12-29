import pygame
import os


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
    def __init__(self):
        self.ratio = (1024, 768)
        self.images = Engine.load_images()
        self.square_colors = ('grey', 'dark-grey')
        self.square_ratio = (64, 64)

    @staticmethod
    def _is_playing_():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def prepare(self):
        while True:
            pygame.init()
            self._is_playing_()
            pygame.display.set_mode(self.ratio)
            self.clock = pygame.time.Clock()
            pass

    @staticmethod
    def load_images():
        images = dict()
        pieces = ['wK', 'wQ', 'wN', 'wR', 'wB', 'wp', 'bK', 'bQ', 'bN', 'bR', 'bB', 'bp']
        os.chdir(r'C:\Users\Николай\PycharmProjects\pythonProject2\Financial University\Практикум по программированию '
                 r'и АДиСД\Четвертый практикум\Game')
        for piece in pieces:
            images[piece] = pygame.image.load('Pieces/' + piece + '.png')
        return images


if __name__ == '__main__':
    Chess = Engine()
    Chess.prepare()
