import pygame


class Bullet:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = (x, y, width, height)
        self.value = 4
        self.ready = False

    def shot(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if not self.ready:
                self.ready = True
                while True:
                    self.x += self.value
                    self.update_rect()
                    if self.x >= 1880:
                        self.ready = False
                        break

    def update_rect(self):
        self.rect = (self.x, self.y, self.width, self.height)


