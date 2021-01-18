class Point:  # В этом файле еда пакмана и всё что за неё отвечает
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.not_on_map = False

    def eat_by_pac(self, pacman):  # Пакман ест еду
        if self.x - pacman.get_x() in range(-10, 10) and self.y - pacman.get_y() in range(-10, 10):
            pacman.add_score(10)
            self.x = 1000
            self.y = 1000
            self.not_on_map = True

    def get_image(self):
        return self.image

    def get_coords(self):
        return self.x, self.y

    def get_on_map(self):
        return self.not_on_map


class BigPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def eat_by_pac(self, pacman, ghost_list):
        for ghost in ghost_list:
            ghost.set_fear(True)
        pacman.add_score(100)
        del self

    def get_coords(self):
        return self.x, self.y


def point_mon(pacman, points):
    for point in points:
        point.eat_by_pac(pacman)
