import pygame


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
    class Main:
        def __init__(self):
            self.ratio = {512, 512}
            self.screen = pygame.display.set_mode
            self.clock = pygame.time.Clock
            self.images = Engine.Build.load_images()

        def prepare(self):
            pygame.init()
            self.screen = self.screen(self.ratio)
            self.clock = self.clock()
            self.screen.fill(pygame.Color('white'))
            pass

    class Build:
        @staticmethod
        def load_images():
            images = dict()
            pieces = ['wK', 'wQ', 'wN', 'wR', 'wB', 'wp', 'bK', 'bQ', 'bN', 'bR', 'bB', 'bp']
            for piece in pieces:
                images[piece] = pygame.image.load('Pieces/' + piece + '.png')
            return images


if __name__ == '__main__':
    Chess = Engine()
