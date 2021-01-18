import pygame


class Ghost:
    def __init__(self, animation, x, y):
        self.x, self.begin_x = x, 400
        self.y, self.begin_y = y, 500
        self.rect = animation.get_curr_image().get_rect()
        self.rect = pygame.transform.scale(animation.get_curr_image(), (10, 10)).get_rect()
        self.rect.x = x
        self.rect.y = y

        self.fear = False

    def eat_pac(self, pacman, ghost_list, app):
        for ghost in ghost_list:
            ghost.set_coords(200, 310)
        pacman.reborn(app)

    def move(self, pacman_coords, title_map, move_speed):
        move = False
        if self.x - pacman_coords[0] > 0 and self.can_move(-move_speed, 0, title_map):
            self.x -= move_speed
            move = True
        elif self.x - pacman_coords[0] < 0 and self.can_move(move_speed, 0, title_map):
            self.x += move_speed
            move = True
        if self.y - pacman_coords[1] > 0 and self.can_move(0, -move_speed, title_map):
            self.y -= move_speed
            move = True
        elif self.y - pacman_coords[1] < 0 and self.can_move(0, move_speed, title_map):
            self.y += move_speed
            move = True
        if not move:
            if self.can_move(0, -move_speed, title_map):
                self.y -= move_speed
            elif self.can_move(0, move_speed, title_map):
                self.y += move_speed
            if self.can_move(-move_speed, 0, title_map):
                self.x -= move_speed
            elif self.can_move(move_speed, 0, title_map):
                self.x += move_speed

        self.rect.x, self.rect.y = self.x, self.y

    def can_move(self, move_x, move_y, tiles):  # Проверка возможности движения
        offset_rect = pygame.Rect(self.rect.x + move_x,
                                  self.rect.y + move_y,
                                  self.rect.w, self.rect.h)
        rect_map = tiles.extract_rect_map()
        text_map = tiles.get_text_map()
        for i in range(len(rect_map)):
            for j in range(len(rect_map[i])):
                if offset_rect.colliderect(rect_map[i][j]) \
                        and (text_map[j][i] != '.' and text_map[j][i] != '\n' and text_map[j][i] != ' '):
                    # print(text_map[j][i])
                    return False
        return True

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_coords(self, x, y):
        self.x = x
        self.y = y

    def set_fear(self, fear_bool):
        self.fear = bool(fear_bool)

    def get_fear(self):
        return self.fear


class Pacman:
    def __init__(self, animation, x_start, y_start, cur_move, lives):
        self.score = 0
        self.rect = animation.get_curr_image().get_rect()
        self.rect = pygame.transform.scale(animation.get_curr_image(), (12, 12)).get_rect()
        self.rect.x = x_start
        self.rect.y = y_start
        self.cur_move = cur_move
        self.x, self.X_BEGIN = x_start, x_start
        self.y, self.Y_BEGIN = y_start, y_start
        self.lives = lives

    def move(self, move_x, move_y, tile_map, coords):
        if self.can_move(move_x, move_y, tile_map):
            self.x += move_x
            self.y += move_y
            self.cur_move = (move_x, move_y)
            self.rect.x, self.rect.y = self.x, self.y
        elif self.can_move(self.cur_move[0], self.cur_move[1], tile_map):
            self.x += self.cur_move[0]
            self.y += self.cur_move[1]
            self.rect.x, self.rect.y = self.x, self.y
        self.check_return(coords)

    def check_return(self, coords):
        if self.x in range(coords[0], coords[0] + 10):
            self.x = coords[1] + 3
        elif self.x in range(coords[1] - 10, coords[1]):
            self.x = coords[0] - 3

    def eat_ghost(self, ghost, ghost_list, app):
        if (self.x - ghost.get_x() in range(-20, 20) and self.y - ghost.get_y() in range(0, 20)) and ghost.get_fear():
            ghost.destroy(700, 700, 1)
            self.score += 300
        elif (self.x - ghost.get_x() in range(-20, 20) and self.y - ghost.get_y() in range(0, 20)) and\
                not ghost.get_fear():
            ghost.eat_pac(self, ghost_list, app)
            app.delta_time = 0

    def reborn(self, app):
        self.lives -= 1
        if self.lives < 0:
            print('Game Over')
            self.x = 100000
            self.y = 100000
        else:
            self.x = self.X_BEGIN
            self.y = self.Y_BEGIN
            self.rect.x, self.rect.y = self.x, self.y

    def can_move(self, move_x, move_y, tiles):  # Проверка возможности движения
        offset_rect = pygame.Rect(self.rect.x + move_x,
                                  self.rect.y + move_y,
                                  self.rect.w, self.rect.h)
        rect_map = tiles.extract_rect_map()
        text_map = tiles.get_text_map()
        for i in range(len(rect_map)):
            for j in range(len(rect_map[i])):
                if offset_rect.colliderect(rect_map[i][j]) \
                        and (text_map[j][i] != '.' and text_map[j][i] != '\n' and text_map[j][i] != ' '):
                    # print(text_map[j][i])
                    return False
        return True

    def check_boarder(self):
        pass

    def add_score(self, score):
        self.score += score

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_rect(self):
        return self.rect


def monitoring(pacman, ghost_list, app):  # Проверка еды приведений и пакмана
    for ghost in ghost_list:
        pacman.eat_ghost(ghost, ghost_list, app)
