class Build:
    """
    Class for external operations
    """
    @staticmethod
    def load_images():
        import pygame
        images = dict()
        pieces = ['wK', 'wQ', 'wN', 'wR', 'wB', 'wp', 'bK', 'bQ', 'bN', 'bR', 'bB', 'bp']
        for piece in pieces:
            images[piece] = pygame.image.load('Pieces/' + piece + '.png')
        return images
