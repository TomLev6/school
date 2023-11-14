import math
import time
import pygame
from __network__ import Network
from pygame import mixer

pygame.font.init()
WIDTH = 1920
HEIGHT = 1080
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")
PORT = 8080
IP = "127.0.0.1"
BACKGROUND_IMAGE = pygame.image.load("C:\Cyber\c0hftsxqll801.png")

MOVE_IMAGE = pygame.image.load("C:\Cyber\-leprechaun.png")
MOVE_IMAGE2 = pygame.image.load("C:\Cyber\wizard.png")

MOVE_BULLET = pygame.image.load("C:\Cyber\-clover.png")
MOVE_BULLET2 = pygame.image.load("C:\Cyber\-bigfire.png")

MOVE_ENEMY = pygame.image.load("C:\Cyber\-goblin.png")
MOVE_ENEMY2 = pygame.image.load("C:\Cyber\-minotaur.png")

CLOCK = pygame.time.Clock()
FPS = 60

FONTS = ["freesansbold.ttf", "C:\Cyber\-black_way\Black Way - Personal Use.otf",
         "C:\Cyber\-blue_yellow\-blue_yellow\-BLUE.otf"]
font = pygame.font.Font(FONTS[2], 64)

# COLORS R G B - RED GREEN BLUE
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)
select_option = False


def redraw_window(player, player2):
    """
    :param player: player 1 object.
    :param player2: player 2 object.
    :return: the window after every change.
    """
    WINDOW.blit(BACKGROUND_IMAGE, (0, 0))
    WINDOW.blit(MOVE_IMAGE, (player.x, player.y))
    WINDOW.blit(MOVE_IMAGE2, (player2.x, player2.y))

    if player.y <= 480:
        player.y = 480
    if player.y >= 950:
        player.y = 950

    if player2.y <= 480:
        player2.y = 480
    if player2.y >= 950:
        player2.y = 950

    if player.x > 3000:
        player.x = 200
    if player.x <= 0:
        player.x = 0
    if player.x >= 1580:
        player.x = 1580

    if player2.x <= 0:
        player2.x = 0
    if player2.x > 3000:
        player2.x = 200
    if player2.x >= 1580:
        player2.x = 1580

    WINDOW.blit(MOVE_BULLET, (player.bx, player.by))
    WINDOW.blit(MOVE_BULLET2, (player2.bx, player2.by))

    if player.bx >= 1880:
        player.bx = player.x + 100
        player.by = player.y + 30

    if player2.bx >= 1880:
        player2.bx = player2.x + 100
        player2.by = player2.y + 30

    WINDOW.blit(MOVE_ENEMY, (player.ex, player.ey))
    WINDOW.blit(MOVE_ENEMY2, (player2.ex, player2.ey))

    if player.ey >= 950:
        player.ey = 950
    if player.ey <= 480:
        player.ey = 480
    if player.ex > 3000:
        player.ex = 1700
    if player.ex <= 120:
        player.ex = 1700
        player.life -= 1

    if player2.ey >= 950:
        player2.ey = 950
    if player2.ey <= 480:
        player2.ey = 480
    if player2.ex > 3000:
        player2.ex = 1700
    if player2.ex <= 120:
        player2.ex = 1700
        player2.elife -= 1

    player.escore = player2.score
    player.elife = player2.life

    score = font.render("Your Score: " + str(player.score), True, COLOR_WHITE)
    WINDOW.blit(score, (player.scorex, player.scorey))

    life = font.render("Your Life: " + player.life * '*', True, COLOR_WHITE)
    WINDOW.blit(life, (player.lifex, player.lifey))

    enemy_score = font.render("Enemy Score: " + str(player2.score), True, COLOR_WHITE)
    WINDOW.blit(enemy_score, (player.escorex, player.escorey))

    enemy_life = font.render("Enemy Life: " + player2.life * '*', True, COLOR_WHITE)
    WINDOW.blit(enemy_life, (player.elifex, player.elifey))

    goal = font.render("Goal: 25", True, COLOR_WHITE)
    WINDOW.blit(goal, (950, 20))

    pygame.display.flip()


def calc_distance(player):
    """
    :param player:
    :return: if a player bullet hit the enemy.
    """
    distance = math.sqrt((math.pow(player.ex - player.bx, 2)) + math.pow(player.ey - player.by, 2))
    if distance < 32:
        return True
    else:
        return False


def show_victory():
    """
    Shows victory screen ( You Won )
    """
    font1 = pygame.font.Font(FONTS[2], 256)
    text = font1.render('You Won!', True, COLOR_WHITE)
    textrect = text.get_rect()
    textrect.center = (1920 // 2, 1080 // 2)
    WINDOW.blit(text, textrect)
    pygame.display.flip()
    time.sleep(5)


def show_game_over():
    """
    Shows game over screen ( You Lost )
    """
    font1 = pygame.font.Font(FONTS[2], 256)
    text_o = font1.render('You Lost!', True, COLOR_WHITE)
    textrect_o = text_o.get_rect()
    textrect_o.center = (1920 // 2, 1080 // 2)
    WINDOW.blit(text_o, textrect_o)
    pygame.display.flip()
    time.sleep(5)


def show_home():
    """
    Shows open screen.
    """
    WINDOW.blit(BACKGROUND_IMAGE, (0, 0))
    font1 = pygame.font.Font(FONTS[2], 256)
    font2 = pygame.font.Font(FONTS[2], 128)
    text = font1.render('Loading...', True, COLOR_WHITE)
    text2 = font2.render('This May Take a Few Seconds', True, COLOR_WHITE)
    textrect = text.get_rect()
    textrect.center = (1920 // 2, 200)
    WINDOW.blit(text, textrect)
    WINDOW.blit(text2, (1920 // 2 - 500, 550))


def music():
    """
    Plays the opening music.
    """
    background_music = "C:\Cyber\-backgroundsound.wav"
    pygame.mixer.init()
    mixer.music.load(background_music)
    mixer.music.play(-1)


def hit():
    """
    Plays when a player hit his enemy.
    """
    hit_music = "C:\Cyber\-explosion.wav"
    pygame.mixer.init()
    mixer.music.load(hit_music)
    mixer.music.play()


def main():
    """
    Handles the client.
    Creates a socket for the client and connects him to the server and receives the current player object data.
     n.getpos()
    Sends the player object to the server and receives the enemy player object data.
    n.send(p)
    :return:
    The current position and data from the current player and sends to the server,
     and receives the enemy player data as well.
    """

    n = Network()
    p = n.get_pos()
    finish = False
    i = 1
    while not finish:
        for _ in range(0, i):
            show_home()
            pygame.display.flip()
            time.sleep(4)
            i -= 1

        p2 = n.send(p)
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
                pygame.quit()
        p.move()
        p.shot()
        p.move_enemy()

        collision = calc_distance(p)
        if collision:
            hit()
            p.add_score()

        if p.check_lost():
            show_game_over()
            finish = True

        elif p.check_win():
            show_victory()
            finish = True

        redraw_window(p, p2)


if __name__ == '__main__':
    music()
    main()
