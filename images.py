import pygame

from global_states import g
from settings import settings


class Image:
    def __init__(self, path, size):
        self.image = pygame.transform.scale(
            pygame.image.load(path),
            size)

    def draw(self, location, orientation=0):
        # TODO: May speed it up if we only use .rotate if orientation set
        g.screen.blit(
            pygame.transform.rotate(self.image, orientation * 90),
            location
        )


class ImageCollection:
    def __init__(self):
        self.images = dict()

    def create(self, name, size):
        self.images[name] = Image(name, size)

    def init(self):
        for id in 'abcdefghijklmnopqrs':
            for prefix, path in (
                    ('light', settings.light_tiles_path),
                    ('dark', settings.dark_tiles_path)
            ):
                name = 'tile_{}'.format(id)
                self.images['{}_{}'.format(prefix, name)] = Image(
                    path='{}{}.png'.format(path, name),
                    size=settings.tile_size
                )

        for colour in 'red', 'green', 'blue', 'yellow':
            for prefix, path in (
                    ('light', settings.light_workers_path),
                    ('dark', settings.dark_workers_path)
            ):
                self.images['{}_{}'.format(prefix, colour)] = Image(
                    path='{}{}.png'.format(path, colour),
                    size=settings.worker_size
                )


g.images = ImageCollection()
