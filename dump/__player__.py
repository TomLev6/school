import random
import pygame


class Player:
    def __init__(self, x, y, width, height, bx, by, bwidth, bheight, ex, ey, ewidth, eheight):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = (x, y, width, height)
        self.value = 6.4
        self.bx = bx
        self.by = by
        self.bwidth = bwidth
        self.bheight = bheight
        self.brect = (bx, by, bwidth, bheight)
        self.ex = ex
        self.ey = ey
        self.ewidth = ewidth
        self.eheight = eheight
        self.erect = (ex, ey, ewidth, eheight)
        self.enemyy_value = 4
        self.enemyx_value = 3
        self.score = 0
        self.scorex = 20
        self.scorey = 20
        self.escore = 0
        self.escorex = 1550
        self.escorey = 20
        self.ready = True
        self.click = False
        self.life = 3
        self.lifex = 20
        self.lifey = 100
        self.elife = 3
        self.elifex = 1550
        self.elifey = 100
        self.players = 0
        self.flag = False

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x -= self.value
        if keys[pygame.K_w]:
            self.y -= self.value
        if keys[pygame.K_d]:
            self.x += self.value
        if keys[pygame.K_s]:
            self.y += self.value
        self.update_rect()

    def move_enemy(self):
        if self.ey >= 950:
            self.ey = 950
            self.enemyy_value = -1 * self.enemyy_value
            self.update_erect()

        if self.ey <= 480:
            self.ey = 480
            self.enemyy_value = -1 * self.enemyy_value
            self.update_erect()

        if self.ex <= 120:
            self.ex = 1700
            self.life -= 1
            self.update_erect()

        else:
            self.ey += self.enemyy_value
            self.ex -= self.enemyx_value
            self.update_erect()

    def check_shot(self):
        return self.ready

    def shot(self):
        if self.check_shot():
            if self.bullet_state():
                self.bx += self.value * 3.5
                self.update_brect()
            else:
                if self.bx >= 1880:
                    self.bx = self.x + 100
                    self.by = self.y + 30
                    self.ready = False
                    self.update_brect()

    def add_score(self):
        self.score += 1
        self.replace_enemy()
        self.reset_bullet()

    def replace_enemy(self):
        self.ex = random.randint(1350, 1800)
        self.ey = random.randint(490, 940)

    def check_win(self):
        if self.score == 25 or self.elife == 0:
            self.ex = 3200
            self.ey = 380
            return True

    def check_lost(self):
        if self.escore == 24 or self.life == 0:
            self.add_score()
            return True

    def check_any_click(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.click = True

    def reset_bullet(self):
        self.bx = self.x + 100
        self.by = self.y + 30

    def bullet_state(self):
        return self.bx < 1880

    def update_rect(self):
        self.rect = (self.x, self.y, self.width, self.height)

    def update_brect(self):
        self.brect = (self.bx, self.by, self.bwidth, self.bheight)

    def update_erect(self):
        self.erect = (self.ex, self.ey, self.ewidth, self.eheight)
