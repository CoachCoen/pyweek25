import pygame

from settings import settings

from global_states import g


# TODO: Not sure if we need this. Remove if not used
def draw_line(a, b):
    pygame.draw.line(g.screen, settings.line_colour, a, b, width=1)


def draw_rectangle(rect, background_colour=None):
    colour = background_colour if background_colour else settings.line_colour
    width = 0 if background_colour else 1
    pygame.draw.rect(g.screen, colour, rect, width)


def draw_text(location, text):
    myfont = pygame.font.SysFont('Comic Sans MS', 30)

    textsurface = myfont.render(text, False, (0, 0, 0))
    g.screen.blit(textsurface, location)


g.screen = pygame.display.set_mode(settings.screen_size)
