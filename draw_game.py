import pygame

from settings import settings
from global_states import g
from drawing import draw_rectangle, draw_text
from vector import Vector

# TODO: Remove background colour, just used for testing by app.mark_locations
def draw_one_tile(tile, x, y, background_colour=None):
    location_on_map = Vector(
        x * settings.tile_size.width,
        y * settings.tile_size.height
    )

    for is_dark, offset in (
            (False, settings.light_map_location),
            (True, settings.dark_map_location)
    ):
        location = location_on_map + offset
        if tile:
            # TODO: Tidy this up
            g.images.images[tile.image_name(is_dark)].draw(location=location, orientation=tile.orientation)
        else:
            rect = location.to_rect(settings.tile_size)
            draw_rectangle(rect, background_colour=background_colour)


def draw_tiles():
    for x in range(settings.map_columns):
        for y in range(settings.map_rows):
            draw_one_tile(g.map.cells[x][y], x, y)


def draw_one_player(player, row):
    location = Vector(
        settings.player_details_location.x,
        settings.player_details_location.y + row * settings.player_details_height
    )

    name = '>> {}'.format(player.name) if row == g.current_player else player.name
    draw_text(location, name)

    live_workers = len(player.unplaced_workers(alive=True))
    ghost_workers = len(player.unplaced_workers(alive=False))

    worker_location = location + settings.player_workers_offset
    for i in range(live_workers):
        g.images.images['light_{}'.format(player.colour)].draw(location=worker_location)
        worker_location.x += settings.worker_size.x

    for i in range(ghost_workers):
        g.images.images['dark_{}'.format(player.colour)].draw(location=worker_location)
        worker_location.x += settings.worker_size.x


def draw_players():
    for row, player in enumerate(g.players.players):
        draw_one_player(player, row)


def draw_all():
    g.screen.fill((255, 255, 255))
    draw_tiles()
    draw_players()
    pygame.display.flip()
