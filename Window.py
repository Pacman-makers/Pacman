import pygame


class Window:
    def __init__(self, size, title):
        self._size = size

        self._win = pygame.display.set_mode(size)
        pygame.display.set_caption(title)

    def get_size(self):
        return self._size

    def get_title(self):
        return pygame.display.get_caption()

    def get_context(self):
        return self._win

    def get_mouse_pressed(self):
        return pygame.mouse.get_pressed()

    def get_mouse_pos(self):
        return pygame.mouse.get_pos()

    def set_title(self, title):
        pygame.display.set_caption(title)

    def fill(self, color):
        self._win.fill(color)

    def draw_obj(self, obj, draw_pos):
        self._win.blit(obj, draw_pos)

    def draw_rect(self, rect, color):
        pygame.draw.rect(self._win, color, rect)
