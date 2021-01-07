from pygame import Rect
from pygame.font import SysFont, init

init()


class Button:
    def __init__(self, context,
                 x, y, width, height,
                 text="Text", tag="", text_color=(0, 0, 0),
                 font=SysFont(None, 20),
                 btn_color=(255, 255, 255), proc=None):
        self._context = context

        self._rect = Rect(x, y, width, height)
        self._text = text
        self._font = font
        self._tag = tag
        self._text_color = text_color
        self._btn_color = btn_color
        self._shown = True
        self._clicked = False
        self._proc = proc

    def get_rect(self):
        return self._rect

    def get_text(self):
        return self._text

    def get_font(self):
        return self._font

    def get_tag(self):
        return self._tag

    def get_text_color(self):
        return self._text_color

    def get_btn_color(self):
        return self._btn_color

    def get_visible(self):
        return self._shown

    def get_pressed(self):
        return self._clicked

    def set_rect(self, x, y, width, height):
        self._rect = Rect(x, y, width, height)

    def set_text(self, text):
        self._text = text

    def set_font(self, font):
        self._font = font

    def set_tag(self, tag):
        self._tag = tag

    def set_text_color(self, text_color):
        self._text_color = text_color

    def set_btn_color(self, btn_color):
        self._btn_color = btn_color

    def set_visibility(self, visibility):
        self._shown = visibility

    def is_clicked(self):
        pressed = any(self._context.get_mouse_pressed())
        if pressed and not self._clicked:
            self._clicked = True
            return True
        elif not pressed:
            self._clicked = False
        return False

    def contains_mouse(self):
        temp_pos = self._context.get_mouse_pos()
        return self._rect.collidepoint(temp_pos[0], temp_pos[1])

    def bind(self, proc):
        self._proc = proc

    def update(self, *args):
        if self.is_clicked():
            if self._proc and self.contains_mouse():
                self._proc(*args)

    def draw(self):
        if self._shown:
            temp_text = self._font.render(self._text, 0, self._text_color)
            temp_rect = temp_text.get_rect()
            temp_center = (self._rect.x + self._rect.w // 2,
                           self._rect.y + self._rect.h // 2)

            self._context.draw_rect(self._rect, self._btn_color)
            self._context.draw_obj(temp_text,
                                   (temp_center[0] - temp_rect.w // 2,
                                    temp_center[1] - temp_rect.h // 2))
