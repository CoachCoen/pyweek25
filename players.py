import pygame
from global_states import g

from random import choice
from time import sleep

from global_states import g
from simple_logger import log
from draw_game import draw_all
from game_mechanics import draw_random_tile
from game_mechanics import suitable_locations_and_orientations
from AI import RandomAI


class Player:
    def __init__(self, name, AI, colour):
        self.name = name
        self.AI = AI(self) if AI else None
        self.colour = colour
        self.removed_workers_score = 0

    def take_move(self):
        if self.AI:
            self.AI.take_move()

    def unplaced_workers(self, alive):
        return g.components.filter(player=self, alive=alive, placed=False)

    @property
    def colour_code(self):
        return pygame.color.THECOLORS[self.colour]

    def __repr__(self):
        return '<player>(name={}, AI={}, colour={})'.format(self.name, self.AI, self.colour)


class Players:
    def __init__(self):
        self.players = []

    def init(self):
        for name, AI, colour in (
                ('Me', None, 'yellow'),
                ('Me 1', None, 'red'),
                ('Me 2', None, 'green'),
                ('Me 3', None, 'blue'),
                # ('Sue', RandomAI, 'red'),
                # ('John', RandomAI, 'green'),
                # ('Elisa', RandomAI, 'blue'),
        ):
            self.players.append(Player(name, AI, colour))


g._players = Players()
