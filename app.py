from random import randint

import pygame

from global_states import g
from settings import settings

from map import Map

# TODO: Remove this - just to get init going, hopefully won't need later
import components
import drawing

# size = width, height = 320, 240
# speed = [2, 2]
# black = 0, 0, 0
#
# screen = pygame.display.set_mode(size)
#
# ball = pygame.image.load("ball.bmp")
# ballrect = ball.get_rect()


def random_free_map_cell():
    while True:
        x, y = randint(0, settings.map_columns - 1), randint(0, settings.map_rows - 1)
        if g.map.cells[x][y] is None:
            return x, y


# TODO: Remove this
def set_random_tiles():
    for tile in g.components.tiles:
        x, y = random_free_map_cell()
        g.map.cells[x][y] = tile


def init_game():
    pygame.init()

    g.init()


init_game()
set_random_tiles()
pygame.display.flip()

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

#     # ballrect = ballrect.move(speed)
#     # if ballrect.left < 0 or ballrect.right > width:
#     #     speed[0] = -speed[0]
#     # if ballrect.top < 0 or ballrect.bottom > height:
#     #     speed[1] = -speed[1]
#
#     screen.fill(black)
#     # screen.blit(ball, ballrect)
#     pygame.display.flip()
#