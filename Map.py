from pygame import Rect, Surface, SRCALPHA

# Corners:
# 1 for Upper Left
# 2 for Upper Right
# 3 for Lower Left
# 4 for Lower Right
# . for Nothing

# Vertical bars:
# L for Left
# R for Right

# Horizontal bars:
# U for Upper
# D for Lower

# Field parts:
# 5 for Upper Left Strong
# 6 for Upper Right Strong
# 7 for Lower Left Strong
# 8 for Lower Right Strong

tile_dict = {
    # Bars and corners
    '1': (0, 0),
    '2': (5, 0),
    '3': (0, 5),
    '4': (5, 5),
    'U': (1, 0),
    'D': (1, 5),
    'L': (0, 1),
    'R': (5, 1),

    # Strong corners
    '5': (7, 1),
    '6': (8, 1),
    '7': (7, 2),
    '8': (8, 2),
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
        for i in range(len(self._map[0])):
            self._tile_map.append([])
            for j in range(len(self._map)):
                if self._map[j][i] not in (' ', '.'):
                    temp_id = tile_dict[self._map[j][i]]
                    self._tile_map[i].append(
                        self._tile_list[temp_id[0]][temp_id[1]])
                else:
                    self._tile_map[i].append(
                        Surface(self._tile_size, SRCALPHA))

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

    def draw_tile_map(self, window, offset):
        for i in range(len(self._tile_map)):
            for j in range(len(self._tile_map[0])):
                if self._tile_map[i][j]:
                    window.draw_obj(self._tile_map[i][j],
                                    (16 * i + offset[0], 16 * j + offset[1]))
