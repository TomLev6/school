import math
import random
from pygame import mixer
import pygame
import time
import logging

"""
Author: Tom Lev
Date: 03.03.22
"""
IP = "0.0.0.0"
PORT = 8888
QUEUE_LEN = 1

LOG_FORMAT = '%(levelname)s | %(asctime)s | %(processName)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_FILE = "log-of-game.log"
FOLDER_PATH_SAVE = r"C:\Cyber"

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 20, 147)
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)
IMAGE = "C:\Cyber\c0hftsxqll801.png"
MOVE_IMAGE = "C:\Cyber\-leprechaun.png"
REFRESH_RATE = 60
LEFT = 1
SCROLL = 2
RIGHT = 3

pygame.init()

# music and sound
background = "C:\Cyber\-backgroundsound.wav"
mixer.music.load(background)
mixer.music.play(-1)

# screen
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
score_value = 0
font_type = ["freesansbold.ttf", "C:\Cyber\-black_way\Black Way - Personal Use.otf",
             "C:\Cyber\-blue_yellow\-Blue Yellow.ttf"]
font = pygame.font.Font(font_type[2], 64)
mid_font = pygame.font.Font(font_type[2], 128)
textx = 30
texty = 30


def show_score(tx, ty):
    score = font.render("Score: " + str(score_value), True, WHITE)
    screen.blit(score, (tx, ty))


bossx = 1400
bossy = 30


def show_boss_life(box, boy):
    life = over_font.render("*" * boss_life, True, WHITE)
    screen.blit(life, (box, boy))


def show_goal(gx, gy):
    goal = font.render("Goblins Left:" + str(level - score_value), True, WHITE)
    screen.blit(goal, (gx, gy))


previous_round = 0
game_round = 1
level = 50
goalx = 750
goaly = 30


def show_round(rx, ry):
    r = font.render("Round: " + str(game_round), True, WHITE)
    screen.blit(r, (rx, ry))


roundx = 850
roundy = 1000
over_font = pygame.font.Font(font_type[2], 256)
g_over_x = (1920 // 2)
g_over_y = (1080 // 2)

gold = pygame.image.load("C:\Cyber\-gold-pot.png")


def show_gold():
    screen.blit(gold, (0, 700))


def show_game_over():
    font1 = pygame.font.Font(font_type[2], 256)
    text_o = font1.render('Game Over', True, WHITE)
    textRect_o = text_o.get_rect()
    textRect_o.center = (1920 // 2, 1080 // 2)
    screen.blit(text_o, textRect_o)
    pygame.display.flip()
    time.sleep(3)


def pause_game():
    font2 = pygame.font.Font(font_type[2], 172)
    text_o1 = font2.render('Pause Game Tab Space To Resume', True, WHITE)
    textrect_o1 = text_o1.get_rect()
    textrect_o1.center = (1920 // 2, 1080 // 2)
    screen.blit(text_o1, textrect_o1)


def show_victory():
    font = pygame.font.Font(font_type[2], 256)
    text = font.render('You Won!', True, WHITE)
    textRect = text.get_rect()
    textRect.center = (1920 // 2, 1080 // 2)
    screen.blit(text, textRect)
    pygame.display.flip()
    time.sleep(5)


def show_home():
    font1 = pygame.font.Font(font_type[2], 256)
    font2 = pygame.font.Font(font_type[2], 128)
    text = font1.render('Menu', True, WHITE)
    text2 = font2.render('Play', True, WHITE)
    # text3 = font2.render('Quit', True, WHITE)
    textrect = text.get_rect()
    textrect.center = (1920 // 2, 200)
    screen.blit(text, textrect)
    screen.blit(text2, (1920 // 2 - 100, 550))
    # screen.blit(text3, (1920 // 2 - 100, 700))


pygame.display.set_caption("Defend The Gold")
icon_image = pygame.image.load("C:\Cyber\monster.png")
pygame.display.set_icon(icon_image)

clock = pygame.time.Clock()  # ??

# main background
img = pygame.image.load(IMAGE)

# player
move_img = pygame.image.load(MOVE_IMAGE)
px = 200
py = 600

# enemy
enemy_image = []
Enemyx = []
Enemyy = []
Enemyy_change = []
Enemyx_change = []
num_of_ememies = 10

for enemy in range(num_of_ememies):
    enemy_image.append(pygame.image.load("C:\Cyber\-goblin.png"))
    Enemyx.append(random.randint(1100, 1900))
    Enemyy.append(random.randint(800, 1000))
    Enemyy_change.append(0.6)
    Enemyx_change.append(0.8)

# enemy 2
enemy_image2 = []
Enemyx2 = []
Enemyy2 = []
Enemyy_change2 = []
Enemyx_change2 = []
num_of_ememies2 = 5

for enemy2 in range(num_of_ememies2):
    enemy_image2.append(pygame.image.load("C:\Cyber\-ogre.png"))
    Enemyx2.append(random.randint(1100, 1900))
    Enemyy2.append(random.randint(800, 1000))
    Enemyy_change2.append(0.5)
    Enemyx_change2.append(0.6)

# enemy 3 - boss
# "C:\Cyber\-boss.png", "C:\Cyber\-minotaur.png"
enemy_image3 = (pygame.image.load("C:\Cyber\-boss.png"))
Enemyx3 = (random.randint(1100, 1900))
Enemyy3 = random.randint(800, 1000)
Enemyy_change3 = 0.4
Enemyx_change3 = 0.5
num_of_ememies3 = 1
boss_life = 5

# bullet
bullet = pygame.image.load("C:\Cyber\-clover.png")
b_y = py + 60
b_x = px + 130
state = "no"


def calc_distance(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow(enemyx - bulletx, 2)) + math.pow(enemyy - bullety, 2))
    if distance < 32:
        return True
    else:
        return False


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action


# load buttons images
exit_game_ = pygame.image.load("C:\Cyber\-close.png").convert_alpha()
start_game = pygame.image.load("C:\Cyber\-play.png").convert_alpha()
resume_game = pygame.image.load("C:\Cyber\-play.png").convert_alpha()
quit_game = pygame.image.load("C:\Cyber\-power-off.png").convert_alpha()
home_page = pygame.image.load("C:\Cyber\-home.png").convert_alpha()

# create button instances
start_button = Button(1050, 580, start_game, 1)


# resume_button = Button(900, 600, resume_game, 1)
# home_button = Button(700, 200, home_page, 1)


def game():
    pygame.init()
    global py, px, state, b_x, b_y, Enemyx3, Enemyy_change3, Enemyy3, boss_life, previous_round, level, game_round, score_value
    finish = False
    select_option = ""
    pause = ""
    while not finish:
        while select_option == "":
            screen.blit(img, (0, 0))
            show_home()
            if start_button.draw(screen):
                select_option = "play"
            pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
                pygame.quit()
            # User pressed key
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # esc key pressed.
                    while pause == "":
                        pause_game()
                        if event.key == pygame.K_SPACE:
                            pause = "play"
                        pygame.display.flip()
        screen.blit(img, (0, 0))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            py -= 2.4
        if keys[pygame.K_s]:
            py += 2.4
        if keys[pygame.K_d]:
            px += 2.4
        if keys[pygame.K_a]:
            px -= 2.4
        if keys[pygame.K_SPACE]:
            if state == "no":
                bullet_shot = mixer.Sound("C:\Cyber\-laser.wav")
                bullet_shot.play()
                state = "yes"
                b_x = px + 130
                b_y = py + 60
        if px <= 0:
            px = 0
        if px >= 800:
            px = 800
        if py <= 480:
            py = 480
        if py >= 950:
            py = 950

        if b_x >= 1880:
            b_x = px + 130
            b_y = py + 60
            state = "no"

        if state is "yes":
            screen.blit(bullet, (b_x, b_y))
            b_x += 12
        # enemy
        for i in range(num_of_ememies):
            # game over
            if Enemyx[i] <= 120:
                for j in range(num_of_ememies):
                    Enemyx[j] = 3500
                show_game_over()
                pygame.display.flip()
                time.sleep(3)
                finish = True
            Enemyy[i] -= Enemyy_change[i]
            Enemyx[i] -= Enemyx_change[i]
            if Enemyy[i] <= 480:
                Enemyy_change[i] = -0.5

            elif Enemyy[i] >= 950:
                Enemyy_change[i] = 0.5
            # distance
            collision = calc_distance(Enemyx[i], Enemyy[i], b_x, b_y)
            if collision:
                hit_enemy = mixer.Sound("C:\Cyber\-explosion.wav")
                hit_enemy.play()
                b_x = px + 130
                b_y = py + 60
                state = "no"
                score_value += 1
                Enemyx[i] = random.randint(1100, 1820)
                Enemyy[i] = random.randint(480, 949)
            screen.blit(enemy_image[i], (Enemyx[i], Enemyy[i]))

            # enemy 2
        for k in range(num_of_ememies2):
            # game over
            if Enemyx2[k] <= 120:
                for f in range(num_of_ememies2):
                    Enemyx2[f] = 3500
                show_game_over()
                pygame.display.flip()
                time.sleep(3)
                finish = True
            Enemyy2[k] -= Enemyy_change2[k]
            Enemyx2[k] -= Enemyx_change2[k]

            if Enemyy2[k] <= 480:
                Enemyy_change2[k] = -0.5

            elif Enemyy2[k] >= 950:
                Enemyy_change2[k] = 0.5
            # distance
            collision = calc_distance(Enemyx2[k], Enemyy2[k], b_x, b_y)
            if collision:
                hit_enemy = mixer.Sound("C:\Cyber\-explosion.wav")
                hit_enemy.play()
                b_x = px + 130
                b_y = py + 60
                state = "no"
                score_value += 1
                Enemyx2[k] = random.randint(1100, 1820)
                Enemyy2[k] = random.randint(480, 949)
            screen.blit(enemy_image2[k], (Enemyx2[k], Enemyy2[k]))

            # enemy 3 - boss

            # game over
        if Enemyx3 <= 120:
            Enemyx3 = 3500
            show_game_over()
            pygame.display.flip()
            time.sleep(3)
            finish = True
        Enemyy3 -= Enemyy_change3
        Enemyx3 -= Enemyx_change3

        if Enemyy3 <= 480:
            Enemyy_change3 = -0.5

        elif Enemyy3 >= 950:
            Enemyy_change3 = 0.5
        # distance
        collision = calc_distance(Enemyx3, Enemyy3, b_x, b_y)
        if collision:
            boss_life -= 1
            hit_enemy = mixer.Sound("C:\Cyber\-explosion.wav")
            hit_enemy.play()
            b_x = px + 130
            b_y = py + 60
            state = "no"
            score_value += 1
            if boss_life == 0:
                Enemyx3 = random.randint(11000, 18200)
                Enemyy3 = random.randint(4800, 9490)
        if game_round > previous_round and game_round > 1:
            boss_life = 4 + game_round
            previous_round = game_round
            Enemyx3 = random.randint(1100, 1820)
            Enemyy3 = random.randint(480, 949)
        screen.blit(enemy_image3, (Enemyx3, Enemyy3))

        player_image = pygame.image.load(MOVE_IMAGE).convert()
        player_image.set_colorkey(BLACK)
        screen.blit(player_image, (px, py))
        show_score(textx, texty)
        show_boss_life(bossx, bossy)
        show_gold()
        if score_value <= level:
            show_goal(goalx, goaly)
            show_round(roundx, roundy)
        if score_value >= level:  # num_of_ememies + num_of_ememies2 + num_of_ememies3
            # message: You won!
            game_round += 1
            level = level + 50 * game_round
            show_goal(goalx, goaly)
            show_round(roundx, roundy)
        if game_round == 8:
            show_victory()
            finish = True

        # pause = ""
        pygame.display.flip()
    pygame.quit()


game()
