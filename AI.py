from random import choice
from time import sleep

from global_states import g
from simple_logger import log
from draw_game import draw_all
from game_mechanics import draw_random_tile
from game_mechanics import suitable_locations_and_orientations
# from game_mechanics import check_valid_worker_spaces


def get_worker(player):
    workers = g.components.filter(klass='worker', placed=False, player=player)
    if workers:
        return workers[0]
    return None


# class DeterministicAI:
#     def __init__(self, player):
#         self.player = player
#
#     def take_move(self):
#         locations = g.map.available_locations()
#         possible_fits = []
#         while not possible_fits:
#             next_tile = g.components.filter(klass='tile', placed=False)[0]
#             possible_fits = suitable_locations_and_orientations(next_tile)
#         next_location = possible_fits[0]
#         log("Placing tile {}, orientation {} at {}".format(next_tile.id, next_location[1], next_location[0]))
#         next_tile.place(next_location[0], next_location[1])
#         # next_worker_spaces = next_tile.worker_spaces
#
#         if next_tile.worker_spaces:
#             next_worker = get_worker(self.player)
#             if next_worker:
#                 worker_space = choice(next_tile.worker_spaces)
#                 # if worker_space != 'G':
#                 #     worker_space = (worker_space + next_location[1]) % 4
#                 log("Placing worker {} at {}".format(next_worker, worker_space))
#         draw_all()
#         sleep(1)
#         g.next_player()


class RandomAI:
    def __init__(self, player):
        self.player = player

    def take_move(self):
        locations = g.map.available_locations()
        possible_fits = []
        while not possible_fits:
            next_tile = draw_random_tile()
            possible_fits = suitable_locations_and_orientations(next_tile)
        next_location = choice(possible_fits)
        log("Placing tile {}, orientation {} at {}".format(next_tile.id, next_location[1], next_location[0]))
        next_tile.place(next_location[0], next_location[1])
        # if next_tile.worker_spaces:
        #     next_worker = get_worker(self.player)
        #     if next_worker:
        #         worker_space = choice(next_tile.worker_spaces)
        #         # if worker_space != 'G':
        #         #     worker_space = (worker_space + next_location[1]) % 4
        #         next_worker.place(next_tile, worker_space)
        #         log("Placing worker {} at {}".format(next_worker, worker_space))
        draw_all()
        sleep(1)
        g.turn_state.next_player()
