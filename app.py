from random import randint, choice
from time import sleep

import pygame

from global_states import g
from simple_logger import log
from settings import settings
from draw_game import draw_all, draw_one_tile
from game_mechanics import draw_starting_tile, draw_random_tile
from game_mechanics import suitable_locations_and_orientations

# from map import Map

# TODO: Remove this - just to get init going, hopefully won't need later
import components
import images
import players
import map
import buttons
import turn_state

# TODO: Remove this - just to help during development
def mark_locations(locations):
    for location in locations:
        draw_one_tile(None, location, background_colour=(127, 127, 127))


def init_game():
    pygame.init()

    g.init()
    draw_starting_tile()


init_game()

draw_all()

done = False
while not done:
    if not g.buttons.waiting:
        if g.current_player.AI:
            g.current_player.AI.take_move()
            draw_all()
        else:
            g.turn_state.start_human_move()
            draw_all()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Respond to mouse clicks
        if event.type == pygame.MOUSEBUTTONUP:
            g.buttons.process_mouse_click(pygame.mouse.get_pos())
