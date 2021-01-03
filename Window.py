import pygame


class Window:
    def __init__(self, size, title):
        self._size = size

        self._win = pygame.display.set_mode(size)
        self._win.blit()
        pygame.display.set_caption(title)

    def get_size(self):
        return self._size

    def get_title(self):
        return pygame.display.get_caption()

    def get_context(self):
        return self._win

    def set_title(self, title):
        pygame.display.set_caption(title)

    def fill(self, color):
        self._win.fill(color)
