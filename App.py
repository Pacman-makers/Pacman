import pygame
from Window import Window

TICK = 64


class App:
    def __init__(self, size, title):
        pygame.init()

        self.window = Window(size, title)
        self.clock = pygame.time.Clock()
        self.running = True

    def prerun(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def run(self):
        while self.running:
            self.clock.tick(TICK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            self.update()

            self.window.fill(0)

            self.draw()

            pygame.display.flip()

        pygame.quit()
