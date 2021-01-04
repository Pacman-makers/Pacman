from pygame import Rect


class Animation:
    def __init__(self, spr_sheet, start_pos, crop_size, crop_count):
        self._spr_sheet = spr_sheet
        self._start_pos = start_pos
        self._crop_count = crop_count
        self._crop_size = crop_size
        self._curr_frame = 0
        self._frame_list = []
        self._crop()
        self._curr_image = self._frame_list[0]

    def get_start_pos(self):
        return self._start_pos

    def get_crop_count(self):
        return self._crop_count

    def get_crop_size(self):
        return self._crop_size

    def get_curr_frame(self):
        return self._curr_frame

    def get_frame_list(self):
        return self._frame_list

    def get_curr_image(self):
        return self._curr_image

    def set_start_pos(self, start_pos):
        self._start_pos = start_pos

    def set_crop_count(self, crop_count):
        self._crop_count = crop_count

    def set_crop_size(self, crop_size):
        self._crop_size = crop_size

    def set_curr_frame(self, curr_frame):
        self._curr_frame = curr_frame

    def _crop(self):
        temp_rect = (*self._start_pos, *self._crop_size)

        for i in range(self._crop_count[0]):
            for j in range(self._crop_count[1]):
                self._frame_list.append(self._spr_sheet.subsurface(
                    Rect(temp_rect[0] + temp_rect[2] * i,
                         temp_rect[1] + temp_rect[3] * j, *temp_rect[2:4])))

    def update(self, speed):
        self._curr_frame = self._curr_frame + speed
        self._curr_image = self._frame_list[int(self._curr_frame) % len(self._frame_list)]
