import pygame

from settings import settings

from global_states import g


# TODO: Not sure if we need this. Remove if not used
from vector import Vector


def draw_line(a, b):
    pygame.draw.line(g.screen, settings.line_colour, a, b, width=1)


def draw_rectangle(rect, background_colour=None, frame_colour=None, width=1):
    # TODO: Tidy this up?
    colour = background_colour if background_colour else frame_colour if frame_colour else settings.line_colour
    frame_width = 0 if background_colour else width
    pygame.draw.rect(g.screen, colour, rect, width)


def draw_text(location, text):
    myfont = pygame.font.SysFont('Comic Sans MS', 30)

    textsurface = myfont.render(text, False, (0, 0, 0))
    g.screen.blit(textsurface, location)


def draw_circle(location, size, colour):
    pygame.draw.circle(g.screen, colour, location, size)


g.screen = pygame.display.set_mode(settings.screen_size)


def map_location_to_screen_location(location, is_dark):
    # TODO: same code also used in draw_game
    location_on_map = Vector(
        location.x * settings.tile_size.width,
        location.y * settings.tile_size.height
    )
    map_offset = settings.dark_map_location if is_dark else settings.light_map_location
    return location_on_map + map_offset