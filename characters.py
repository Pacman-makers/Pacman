import pygame


class Ghost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.fear = False

    def new_ghost(self, x, y, time_of_reborn):
        pass

    def eat_pac(self, pacman):
        if (self.x - pacman.get_x() in range(0, 30) and self.y - pacman.get_y() in range(0, 30)) and not self.fear:
            pacman.reborn()

    def move(self):
        pass

    def destroy(self, x, y, time):
        self.new_ghost(x, y, time)
        del self

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_fear(self):
        return self.fear


class Pacman:
    def __init__(self, x_start, y_start, lives):
        self.score = 0
        self.x, self.X_BEGIN = x_start
        self.y, self.Y_BEGIN = y_start
        self.lives = lives

    def move(self, move_x, move_y):
        self.x += move_x
        self.y += move_y

    def eat_ghost(self, ghost):
        if (self.x - ghost.get_x() in range(0, 30) and self.y - ghost.get_y() in range(0, 30)) and ghost.get_fear:
            ghost.destroy()
            self.score += 300
        elif (self.x - ghost.get_x() in range(0, 30) and self.y - ghost.get_y() in range(0, 30)) and not ghost.get_fear:
            ghost.eat_pac(self)

    def reborn(self):
        self.lives -= 1
        if self.lives < 0:
            pass
        else:
            self.x = self.X_BEGIN
            self.y = self.Y_BEGIN

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


def monitoring(pacman, ghost_list):
    for ghost in ghost_list:
        pacman.eat_ghost(ghost)
