import pygame

from settings import settings

from global_states import g

g.screen = pygame.display.set_mode(settings.screen_size)

# TODO: Tidy this up?
g.screen.fill((255, 255, 255))
