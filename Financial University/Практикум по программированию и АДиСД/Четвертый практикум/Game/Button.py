class Button:
    """
    This is just a class for a buttons
    """
    def __init__(self, position, size, clr=None, change_color=None, func=None, text='Hello', font="Segoe Print",
                 font_size=16, font_clr=None):
        if font_clr is None:
            font_clr = [0, 0, 0]
        if clr is None:
            clr = [100, 100, 100]
        import pygame
        self.cursor_color = None
        self.color = clr
        self.size = size
        self.func = func
        self.surf = pygame.Surface(size)
        self.rect = self.surf.get_rect(center=position)

        if change_color:
            self.change_color = change_color
        else:
            self.change_color = clr

        if len(clr) == 4:
            self.surf.set_alpha(clr[3])

        self.font = pygame.font.SysFont(font, font_size)
        self.txt = text
        self.font_clr = font_clr
        self.txt_surf = self.font.render(self.txt, 1, self.font_clr)
        self.txt_rect = self.txt_surf.get_rect(center=[wh // 2 for wh in self.size])

    def draw(self, screen):
        self.mouseover()

        self.surf.fill(self.cursor_color)
        self.surf.blit(self.txt_surf, self.txt_rect)
        screen.blit(self.surf, self.rect)

    def mouseover(self):
        import pygame
        self.cursor_color = self.color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.cursor_color = self.change_color

    def call_back(self, *args):
        if self.func:
            return self.func(*args)
