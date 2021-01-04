from pygame import Rect

# Corners:
# 1 for Upper Left
# 2 for Upper Right
# 3 for Lower Left
# 4 for Lower Right
# . for Nothing

# Vertical Bars:
# V for Vertical                 UUUU
# U for Upper Vertical          UUUUUU
# D for Lower Vertical         V |||| V
# | for Middle Vertical        V |||| V
#                              V |||| V
#                               DDDDDD
#                                DDDD
#

# Horizontal Bars:
# H for Horizontal
# L for Left Horizontal        LLL HHHHHHHHH RRR
# R for Right Horizontal     LLLL ----------- RRRR
# - for Middle Horizontal      LLL HHHHHHHHH RRR

tile_dict = {
    '1': (0, 0),
    '2': (2, 0),
    '3': (0, 2),
    '4': (2, 2),
    '.': (1, 1),

    'V': (0, 1),
    'U': (6, 0),
    'D': (6, 2),
    '|': (6, 1),

    'H': (1, 0),
    'L': (7, 0),
    'R': (9, 0),
    '-': (8, 0)
}


class Map:
    def __init__(self, filename, spr_sheet, tile_size):
        self._filename = filename
        self._spr_sheet = spr_sheet
        self._tile_size = tile_size

        self._tile_list = []
        self._load_tiles()

        self._map = []
        self._load_level()

        self._tile_map = []
        self._create_tile_map()

    def _load_level(self):
        filename = "data/" + self._filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        max_width = max(map(len, level_map))

        self._map = list(map(lambda x: x.ljust(max_width, '.'), level_map))

    def _load_tiles(self):
        temp_count = (self._spr_sheet.get_width() // self._tile_size[0],
                      self._spr_sheet.get_height() // self._tile_size[1])

        for i in range(temp_count[0]):
            self._tile_list.append([])
            for j in range(temp_count[1]):
                self._tile_list[i].append(self._spr_sheet.subsurface(Rect(
                    i * self._tile_size[0], j * self._tile_size[1],
                    self._tile_size[0], self._tile_size[1])))

    def _create_tile_map(self):
        for i in range(len(self._map)):
            self._tile_map.append([])
            for j in range(len(self._map[i])):
                temp_id = tile_dict[self._map[i][j]]
                self._tile_map[i].append(
                    self._tile_list[temp_id[0]][temp_id[1]])

    def get_filename(self):
        return self._filename

    def get_spr_sheet(self):
        return self._spr_sheet

    def get_tile_size(self):
        return self._tile_size

    def get_text_map(self):
        return self._map

    def get_tile_list(self):
        return self._tile_list

    def get_tile_map(self):
        return self._tile_map
