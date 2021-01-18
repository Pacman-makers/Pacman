import pygame
from pygame.font import SysFont
import sys, os
from Interface.Button import Button
from math import cos, sin

EXIT_STATE = 1


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def shader(button):
    temp_rect = button.get_rect()
    temp_surf = button.get_surf()

    for x in range(temp_rect.w):
        for y in range(temp_rect.h):
            temp_surf.set_at((x, y), (x % 255 * abs(sin(x)), y % 255 * abs(cos(y)), 100))

    button.set_surf(temp_surf)


def apply_shader(btn_list, shade_func):
    for btn in btn_list:
        shade_func(btn)


class GameManager:
    def __init__(self, window):
        self._window = window
        self._width, self._height = window.get_size()
        self._special_events = []
        self._restart_requested = False

    @staticmethod
    def close():
        pygame.quit()
        sys.exit()

    def _init_buttons(self, data_list, interval):
        btn_list = []
        temp_length = len(data_list)
        for i, data in enumerate(data_list):
            btn_list.append(
                Button(self._window, self._width // 2 - data[0] // 2,
                       self._height // temp_length \
                       + data[1] * i * interval, data[0], data[1],
                       text=data[2], text_color=data[3]))

        return btn_list

    def _update_buttons(self, btn_list):
        for btn in btn_list:
            btn.update()

    def _draw_buttons(self, btn_list):
        apply_shader(btn_list, shader)
        for btn in btn_list:
            btn.draw()

    def _draw_placed_text(self, text_list, start_pos):
        for i in range(len(text_list)):
            temp_rect = text_list[i].get_rect()
            self._window.draw_obj(
                text_list[i],
                (start_pos[0], start_pos[1] + i * temp_rect.h))

    def set_restart_state(self, restart_state):
        self._restart_requested = restart_state

    def get_restart_state(self):
        return self._restart_requested

    def show_story(self):
        sentences = ["Предыстория:",
                     "",
                     "*Вуух* У меня был сегодня тяжёлый день, доиграю в пакмана завтра",
                     "",
                     "лягу, пожалуй, спать пораньше завтра рано вставать. *звуки храпа* *во сне",
                     "",
                     "(приведение, приведение. О фрукт съесть фрукт, съесть приведения, съесть всё) *",
                     "",
                     "Я Пакман, я всегда им был. Приведение не догонят меня, я знаю они",
                     "",
                     "боятся меня. Стоит мне съесть большую точку, и они побегут от меня, главное",
                     "",
                     "Это начинает меня уже доставать, новое приведения снова и снова. Мне",
                     "",
                     "надо выбираться отсюда, но как? Возможно если я съем больше я выберусь отсюда.",
                     "",
                     "Отсюда нет выхода. *Ааа* Как, как я попал сюда, кто я вообще. Я не",
                     "",
                     "могу есть больше, ещё одна точка и я точно лопну. *Звуки будильника*",
                     "",
                     "*Звук будильника* Ох и приснится же такое, поменьше играть надо перед сном.",
                     "",
                     "(Все совпадения с реальным миром случайны. Автор употреблял только кофе)"]

        font_list = [SysFont("Consolas", 20) for _ in range(len(sentences))]
        text_list = []
        happy_img = pygame.transform.scale(load_image("happy_pacman.png"), (300, 300))

        for i in range(len(font_list)):
            text_list.append(font_list[i].render(
                sentences[i], 0, (255, 255, 255)))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                elif event.type == pygame.KEYDOWN:
                    return
            self._window.fill(0)

            self._draw_placed_text(text_list, (100, 100))
            self._window.draw_obj(happy_img, (320, 680))

            pygame.display.flip()

    def show_about(self):
        sentences = ["This Game was made by",
                     "Maxim Egorov and Maxim Mogulev",
                     "",
                     "Controls:",
                     "'p' key - exit from pause",
                     "'o' key - To turn on the sound",
                     "'wasd' keys - move on the board",
                     "'esc' key - exit from the game",
                     "'space' key - stop moving",
                     "", "",
                     "Press any key to exit this menu"]

        font_list = [SysFont("Consolas", 40) for _ in range(len(sentences))]
        text_list = []
        happy_img = pygame.transform.scale(load_image("happy_pacman.png"), (300, 300))

        for i in range(len(font_list)):
            text_list.append(font_list[i].render(
                sentences[i], 0, (255, 255, 255)))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                elif event.type == pygame.KEYDOWN:
                    return
            self._window.fill(0)

            self._draw_placed_text(text_list, (100, 100))
            self._window.draw_obj(happy_img, (320, 680))

            pygame.display.flip()

    def open_menu(self):
        btn_list = self._init_buttons([
            (self._width // 4, self._height // 10, "Start", (100, 255, 255)),
            (self._width // 4, self._height // 10, "About", (255, 255, 100)),
            (self._width // 4, self._height // 10, "Story", (150, 150, 200)),
            (self._width // 4, self._height // 10, "Exit", (255, 100, 100))], 1.5)

        title_img = load_image("pacman_title.png")

        btn_list[0].bind(lambda: self._special_events.append(EXIT_STATE))
        btn_list[1].bind(self.show_about)
        btn_list[2].bind(self.show_story)
        btn_list[3].bind(self.close)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        return

            for event in self._special_events:
                if event == EXIT_STATE:
                    self._restart_requested = True
                    self._special_events.clear()
                    return

            self._update_buttons(btn_list)

            self._window.fill(0)

            self._draw_buttons(btn_list)
            self._window.draw_obj(title_img, (self._width // 2 - 180, 20))

            pygame.display.flip()
