from global_states import g
from game_mechanics import draw_random_tile, suitable_locations_and_orientations, worker_space_is_valid
from simple_logger import log


class TurnState:
    def __init__(self):
        self.current_player_number = 0
        self.next_tile = None
        self.possible_fits = []
        self.next_tile_orientation_id = 0
        self.next_worker_space = None
        self.next_worker = None

    def next_player(self):
        self.current_player_number = (self.current_player_number + 1) % len(g.players)

    @property
    def current_player(self):
        return g.players[self.current_player_number]

    def pick_next(self):
        possible_fits = []
        next_tile = None
        while not possible_fits:
            next_tile = draw_random_tile()
            possible_fits = suitable_locations_and_orientations(next_tile)

        return next_tile, possible_fits

    @property
    def possible_locations(self):
        return set(location for location, orientation in self.possible_fits)

    @property
    def possible_orientations(self):
        return list([
            orientation
            for location, orientation in self.possible_fits
            if location == self.next_tile.location
        ])

    def start_human_move(self):
        log('Started human move')

        self.next_tile, self.possible_fits = self.pick_next()
        self.next_tile_orientation_id = 0

    def rotate_next_tile(self):
        old_rotation_id = self.next_tile_orientation_id
        self.next_tile_orientation_id = (self.next_tile_orientation_id + 1) % len(self.possible_orientations)
        log('Rotated from id {} to {}'.format(old_rotation_id, self.next_tile_orientation_id))

    @property
    def next_tile_orientation(self):
        if not self.next_tile.location:
            log('Tile not placed yet, neutral orientation')
        else:
            log('Next tile, orientation: '.format(self.possible_orientations[self.next_tile_orientation_id]))
        return self.possible_orientations[self.next_tile_orientation_id] if self.next_tile.location else 0

    def clear(self):
        self.next_tile = None
        self.possible_fits = []
        self.next_worker_space = None
        self.next_worker = None

    @property
    def possible_worker_spaces(self):
        result = []
        tile = self.next_tile
        # tile.place(tile.location, self.next_tile_orientation)

        if tile.graveyard:
            result.append('G')

        for edge in range(4):
            if not tile.edges[edge] or tile.edges[edge] is 'B':
                continue
            # if worker_space_is_valid(tile, edge, self.current_player):
            #     log('Can place on |{}| at {}'.format(tile.edges[edge], edge))
            result.append(edge)

        # tile.unplace()

        log('Worker spaces: {}'.format(result))
        return result


g.turn_state = TurnState()
