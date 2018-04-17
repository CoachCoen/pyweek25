from random import randint, choice

from global_states import g
from settings import settings

from vector import Vector


def draw_starting_tile():
    tile = g.components.filter(starting_tile=True)[0]
    tile.place(
        location=Vector(int(settings.map_columns/2), int(settings.map_rows/2)),
        orientation=randint(0, 3)
    )


def next_player():
    g.current_player += 1
    if g.current_player == len(g.players):
        g.current_player = 0


def draw_random_tile():
    return choice(g.components.filter(klass='tile', placed=False))


def suitable_locations_and_orientations(tile):
    result = []
    for location in g.map.available_locations():
        for orientation in range(4):
            if tile.fits(location, orientation):
                # TODO: This can probably be tidier
                result.append((location, orientation))
    return result
