class Build:
    """
    Class for external operations for application
    """
    @staticmethod
    def load_images(folder='Pieces/', form='.png'):
        import pygame
        images = dict()
        pieces = ['wK', 'wQ', 'wN', 'wR', 'wB', 'wp', 'bK', 'bQ', 'bN', 'bR', 'bB', 'bp']
        for piece in pieces:
            images[piece] = pygame.image.load(folder + piece + form)
        return images
