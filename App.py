import pygame
from Window import Window
from Animation import Animation
from Map import Map
from Interface.Button import Button
from characters import Pacman, Ghost, monitoring
from music import Music
from pygame.transform import scale
from GameManager import GameManager, load_image
from Points import Point, BigPoint, point_mon
from Map1coords import COORD_FOOD

TICK = 64


# TODO: create util file for load_image, terminate, etc
#   make a single function that is responsible for every button
#   in the main menu and binds another functions which are responsible
#   for every option

# TODO: create persons' classes and introduce simple gameplay
#   with high score and maybe console screen

def btn_control(button, *args):
    contains_mouse = button.contains_mouse()

    if contains_mouse and button._rect.w < 200:
        button._rect.w += 1
    elif not contains_mouse:
        if button._rect.w > 100:
            button._rect.w -= 1


def start_screen(window):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameManager.close()
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
        self.manager = GameManager(self.window)
        self.win = True
        self.restart = False

        self.ghost_speed = 3
        self.count_for_music = 0

        self.count = 0
        self.font = pygame.font.SysFont("Consolas", 60)

        self.spr_sheet = load_image("pacman-sheet.png")
        self.animation = Animation(self.spr_sheet, (730, 310), (80, 101), (1, 5))
        self.map = Map("map.txt", load_image("maze_tile.png"), (16, 16), draw_offset=(13, 80))

        # Pacman
        self.move = (-5, 0)
        self.pacman = Pacman(self.animation, 235, 465, self.move, 3)
        self.rotate = 0

        # Создание еды
        self.points = []
        self.points_coords = COORD_FOOD

        self.point_animations = []
        for i in range(len(self.points_coords)):
            self.point_animations.append(Animation(self.spr_sheet,
                                                   (125, 20), (20, 20), (1, 1)))
        counter = 0
        for elem in self.points_coords:
            self.points.append(Point(elem[0], elem[1], self.point_animations[counter]))
            counter += 1

        self.mus = Music()
        # Анимации приведений и сами приведения
        self.animation2 = Animation(self.spr_sheet, (925, 727), (80, 101), (1, 2))
        self.animation3 = Animation(self.spr_sheet, (925, 18), (80, 101), (1, 2))
        self.animation4 = Animation(self.spr_sheet, (533, 121), (80, 101), (1, 2))
        self.animation5 = Animation(self.spr_sheet, (840, 120), (80, 101), (1, 2))

        self.blue_ghost = Ghost(self.animation4, 220, 310)
        self.pink_ghost = Ghost(self.animation3, 200, 310)
        self.red_ghost = Ghost(self.animation2, 200, 260)
        self.orange_ghost = Ghost(self.animation5, 240, 310)
        self.ghost_list = [self.red_ghost, self.pink_ghost, self.blue_ghost, self.orange_ghost]
        self.open_clock = pygame.time.Clock()
        self.delta_time = 0
        # self.map = Map("map.txt", load_image("maze_tile.png"), (16, 16)).get_tile_list()

    def prerun(self):
        pass

    # Обновление анимации
    def update(self):
        self.animation.update(0.2, (26, 36), self.rotate)
        self.animation2.update(0.1, (26, 36), 0)
        self.animation3.update(0.1, (26, 36), 0)
        self.animation4.update(0.1, (26, 36), 0)
        self.animation5.update(0.1, (26, 36), 0)
        for elem in self.point_animations:
            elem.update(0.1, (10, 10), 0)

    # Отрисовка объектов
    def draw(self):
        self.map.draw_tile_map(self.window)
        self.window.draw_obj(self.animation.get_curr_image(), (self.pacman.get_x() - 15, self.pacman.get_y() - 20))
        self.window.draw_obj(self.animation2.get_curr_image(), (self.red_ghost.get_x(), self.red_ghost.get_y()))
        self.window.draw_obj(self.animation3.get_curr_image(), (self.pink_ghost.get_x(), self.pink_ghost.get_y()))
        self.window.draw_obj(self.animation4.get_curr_image(), (self.blue_ghost.get_x(), self.blue_ghost.get_y()))
        self.window.draw_obj(self.animation5.get_curr_image(), (self.orange_ghost.get_x(), self.orange_ghost.get_y()))
        for i in range(len(self.point_animations)):
            self.window.draw_obj(self.point_animations[i].get_curr_image(), self.points[i].get_coords())

    def run(self):
        while self.running:
            self.win = True
            self.clock.tick(TICK)

            for event in pygame.event.get():  # Проверка событий
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_p:
                        self.stop = True
                        self.manager.set_restart_state(False)
                    elif event.key == pygame.K_d:
                        self.move = (4, 0)
                        self.rotate = 0
                    elif event.key == pygame.K_a:
                        self.move = (-4, 0)
                        self.rotate = 180
                    elif event.key == pygame.K_w:
                        self.move = (0, -4)
                        self.rotate = 90
                    elif event.key == pygame.K_s:
                        self.move = (0, 4)
                        self.rotate = 270
                    elif event.key == pygame.K_SPACE:
                        self.move = (0, 0)
                    elif event.key == pygame.K_o:
                        self.count_for_music += 1
                        self.mus.change_music(str(self.count_for_music % 2))

            if self.stop:  # Главное меню
                self.manager.open_menu()
                self.stop = False

            self.update()

            self.window.fill(0)

            if self.pacman.get_x() + self.move[0] * 15 > self.window.get_size()[0] or self.pacman.get_y() + \
                    self.move[1] * 15 > self.window.get_size()[1] or self.pacman.get_x() + self.move[0] < 0 or \
                    self.pacman.get_y() + self.move[1] < 0:
                self.move = (0, 0)

                self.move = (0, 0)
            self.pacman.move(self.move[0], self.move[1], self.map, [462, 10])

            # Выпускаем приведений
            self.delta_time += self.open_clock.tick()
            if 1000 > self.delta_time > 0:
                self.red_ghost.set_coords(220, 260)
            elif 3000 > self.delta_time > 2000:
                self.pink_ghost.set_coords(220, 260)
            elif 5000 > self.delta_time > 4000:
                self.blue_ghost.set_coords(220, 260)
            elif 7000 > self.delta_time > 6000:
                self.orange_ghost.set_coords(220, 260)

            # Движение приведений и проверка на паузу
            if self.move == (0, 0):
                self.ghost_speed = 0
            else:
                self.ghost_speed = 3

            pacman_pos = self.pacman.get_x(), self.pacman.get_y()
            self.red_ghost.move((pacman_pos[0], pacman_pos[1]), self.map, self.ghost_speed)
            self.pink_ghost.move((pacman_pos[0], pacman_pos[1]), self.map, self.ghost_speed)
            self.blue_ghost.move((pacman_pos[0], pacman_pos[1]), self.map, self.ghost_speed)
            self.orange_ghost.move((pacman_pos[0], pacman_pos[1]), self.map, self.ghost_speed)

            monitoring(self.pacman, self.ghost_list, app)
            point_mon(self.pacman, self.points)
            for elem in self.points:
                self.win = self.win * elem.get_on_map()

            if self.win:
                print("Your Win")

            self.draw()

            pygame.display.flip()

        pygame.quit()


# Запускаем
app = App((1000, 1000), 'Pac')
app.run()
