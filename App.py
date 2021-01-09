import pygame
import os
import sys
from Window import Window
from Animation import Animation
from Map import Map
from Interface.Button import Button
from characters import Pacman
from music import Music
from pygame.transform import scale

TICK = 64


# TODO: create util file for load_image, terminate, etc
#   make a single function that is responsible for every button
#   in the main menu and binds another functions which are responsible
#   for every option

# TODO: create persons' classes and introduce simple gameplay
#   with high score and maybe console screen

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def btn_control(button, *args):
    contains_mouse = button.contains_mouse()

    if contains_mouse and button._rect.w < 200:
        button._rect.w += 1
    elif not contains_mouse:
        if button._rect.w > 100:
            button._rect.w -= 1


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(window):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return

        window.fill(0)

        pygame.display.flip()


class App:
    def __init__(self, size, title):
        pygame.init()
        pygame.font.init()

        self.window = Window(size, title)
        self.clock = pygame.time.Clock()
        self.stop = True
        self.running = True

        self.pacman = Pacman(0, 0, 3)
        self.move = (0, 0)

        self.mus = Music()

        self.animation = Animation(load_image("pacman-sheet.png"), (730, 310), (80, 101), (1, 5))
        # self.animation2 = Animation(load_image("pacman-sheet.png"), (830, 310), (80, 101), (1, 2))
        self.map = Map("map.txt", load_image("maze_tile.png"), (16, 16))
        # self.map = Map("map.txt", load_image("maze_tile.png"), (16, 16)).get_tile_list()

    def prerun(self):
        pass

    def update(self):
        self.animation.update(0.1)
        # self.animation2.update(0.1)

    def draw(self):
        self.map.draw_tile_map(self.window, (13, 80))
        self.window.draw_obj(self.animation.get_curr_image(), (self.pacman.get_x(), self.pacman.get_y()))
        # self.window.draw_obj(self.animation2.get_curr_image(), (64, 0))

    def run(self):
        self.mus.change_music('231')  # Если поставить "1" будет музыка
        while self.running:
            self.clock.tick(TICK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_p:
                        self.stop = True
                    elif event.key == pygame.K_d:
                        self.move = (5, 0)
                    elif event.key == pygame.K_a:
                        self.move = (-5, 0)
                    elif event.key == pygame.K_w:
                        self.move = (0, -5)
                    elif event.key == pygame.K_s:
                        self.move = (0, 5)
                    elif event.key == pygame.K_SPACE:
                        self.move = (0, 0)

            if self.stop:
                start_screen(self.window)
                self.stop = False

            self.update()

            self.window.fill(0)

            if self.pacman.get_x() + self.move[0] * 15 > self.window.get_size()[0] or self.pacman.get_y() + \
                    self.move[1] * 15 > self.window.get_size()[1] or self.pacman.get_x() + self.move[0] < 0 or \
                    self.pacman.get_y() + self.move[1] < 0:
                self.move = (0, 0)
            # if self.window.get_context().get_at((self.pacman.get_x() + self.move[0],
            #                                     self.pacman.get_y() + self.move[1])) != (0, 0, 0, 255):

                self.move = (0, 0)
            self.pacman.move(self.move[0], self.move[1])

            self.draw()

            pygame.display.flip()

        pygame.quit()


app = App((1000, 1000), 'Pac')
app.run()
