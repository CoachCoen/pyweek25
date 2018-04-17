from random import randint, choice
from time import sleep

import pygame

from global_states import g
from settings import settings
from draw_game import draw_all, draw_one_tile
from game_mechanics import draw_starting_tile, draw_random_tile
from game_mechanics import suitable_locations_and_orientations

from map import Map

# TODO: Remove this - just to get init going, hopefully won't need later
import components
import images
import players


def random_free_map_cell():
    while True:
        x, y = randint(0, settings.map_columns - 1), randint(0, settings.map_rows - 1)
        if g.map.cells[x][y] is None:
            return x, y


# TODO: Remove this - just to help during development
def mark_locations(locations):
    for location in locations:
        draw_one_tile(None, location.x, location.y, background_colour=(127, 127, 127))


def init_game():
    pygame.init()

    g.init()
    draw_starting_tile()


init_game()


# TODO: Remove this - testing only
for _ in range(1):
    next_tile = draw_random_tile()
    locations = g.map.available_locations()
    mark_locations(locations)
    possible_fits = suitable_locations_and_orientations(next_tile)
    next_location = choice(possible_fits)
    next_tile.place(next_location[0], next_location[1])
    draw_all()
    pygame.display.flip()
    sleep(1)

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
