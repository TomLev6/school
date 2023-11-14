import pygame
from __network__ import Network
WIDTH = 1920
HEIGHT = 1080
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")
PORT = 8080
CON = 1024
IP = "127.0.0.1"
BACKGROUND_IMAGE = "C:\Cyber\c0hftsxqll801.png"
ClientNum = 0
CLOCK = pygame.time.Clock()
FPS = 60
# COLORS R G B - RED GREEN BLUE
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)


def redraw_window(player, player2):
    WINDOW.fill(COLOR_WHITE)
    player.draw(window=WINDOW)
    player2.draw(window=WINDOW)
    pygame.display.flip()


def main():
    """
    Handles the client's requests.
    :return:
    """
    n = Network()

    p = n.get_pos()
    finish = False
    while not finish:
        p2 = n.send(p)

        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
                pygame.quit()
        p.move()
        redraw_window(p, p2)


if __name__ == '__main__':
    main()
