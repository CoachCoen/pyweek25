import pygame

from settings import settings
from global_states import g
from drawing import draw_rectangle, draw_text, draw_circle, map_location_to_screen_location
from vector import Vector
from game_mechanics import get_scores
from simple_logger import log


def edge_offset(edge):
    ts = settings.tile_size.x
    return {
        0: Vector(int(ts/2), 0),
        1: Vector(ts - 20, int(ts/2)),
        2: Vector(int(ts/2), ts - 20),
        3: Vector(0, int(ts/2))
    }[edge]


def worker_space_offset(space):
    ts = settings.tile_size.x
    return {
        0: Vector(int(ts/2), settings.worker_circle_size),
        1: Vector(ts - settings.worker_circle_size, int(ts/2)),
        2: Vector(int(ts/2), ts - settings.worker_circle_size),
        3: Vector(settings.worker_circle_size, int(ts/2)),
        'G': Vector(int(ts/2), int(ts/2))
    }[space]


# TODO: Remove background colour, just used for testing by app.mark_locations
def draw_one_tile(tile, location, background_colour=None, orientation=None):
    location_on_map = Vector(
        location.x * settings.tile_size.width,
        location.y * settings.tile_size.height
    )

    worker = None
    if tile:
        log('draw_one_tile, orientation {}, {}'.format(orientation, tile))
        workers = g.components.filter(on_tile=tile)
        if workers:
            worker = workers[0]
            worker_offset = worker_space_offset(worker.location.space)

    for is_dark, offset in (
            (False, settings.light_map_location),
            (True, settings.dark_map_location)
    ):
        location = location_on_map + offset
        if tile:
            if orientation is None:
                orientation = tile.orientation
            # TODO: Tidy this up
            g.images.images[tile.image_name(is_dark)].draw(
                location=location, orientation=orientation
            )

        if worker and worker.alive is not is_dark:
            draw_circle(location + worker_offset, settings.worker_circle_size, worker.player.colour_code)

        # Draw the outline
        # else:
        #     rect = location.to_rect(settings.tile_size)
        #     draw_rectangle(rect, background_colour=background_colour)


def draw_tiles():
    for location in g.map.all_locations:
        draw_one_tile(g.map[location].tile, location)

        # Draw edges
        if False and settings.debug:
            for edge in range(4):
                edge_state = g.map[location].edges[edge]
                location_on_map = Vector(
                    location.x * settings.tile_size.width,
                    location.y * settings.tile_size.height
                )
                draw_text(location_on_map + settings.light_map_location + edge_offset(edge), edge_state)


def draw_one_player(player, row, score):
    location = Vector(
        settings.player_details_location.x,
        settings.player_details_location.y + row * settings.player_details_height
    )

    name = '>> {}'.format(player.name) if row == g.current_player_number else player.name
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

    draw_text(worker_location, str(score))


def draw_players():
    scores = get_scores()
    # TODO: Better place to do this?
    for row, player in enumerate(g.players):
        draw_one_player(player, row, scores[player])


def draw_next_tile():

    if not g.turn_state.next_tile:
        return

    log('Next tile {}'.format(g.turn_state.next_tile))
    if g.turn_state.next_tile.location:
        orientation = g.turn_state.next_tile_orientation
        draw_one_tile(g.turn_state.next_tile, g.turn_state.next_tile.location, orientation=orientation)

        if g.turn_state.next_worker_space is not None:
            if g.turn_state.next_worker_space == 'G':
                space = g.turn_state.next_worker_space
            else:
                space = (g.turn_state.next_worker_space + g.turn_state.next_tile_orientation) % 4
            worker_offset = worker_space_offset(space)
            location = map_location_to_screen_location(g.turn_state.next_tile.location, not g.turn_state.next_worker.alive) \
                            + worker_offset

            rect = location.to_rect(settings.worker_space_size)
            draw_rectangle(rect, background_colour=g.current_player.colour_code, width=0)

    else:
        g.images.images[g.turn_state.next_tile.image_name(False)].draw(
            location=settings.next_tile_location, orientation=0
        )


def draw_all():
    g.buttons.refresh()
    g.screen.fill((255, 255, 255))
    g.images.images['background_light'].draw(location=settings.light_map_location)
    g.images.images['background_dark'].draw(location=settings.dark_map_location)
    draw_tiles()
    draw_players()
    draw_next_tile()
    g.buttons.draw()
    pygame.display.flip()
