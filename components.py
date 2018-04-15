from settings import settings
from global_states import g


class Tile:
    def __init__(self, id, starting, roads, cities, graveyard):
        self.id = id
        self.starting = starting
        self.roads = roads
        self.cities = cities
        self.graveyard = graveyard


def create_tiles_from_data(line):
    """
    Format:

    Identifier, Number of tiles: description
    '*' for the starting tile
    R/oads, G/raveyards, C/ities

    e.g.: N, 3: C(S), R(N, E, W)

    return
    """
    left, right = line.split(': ')
    id, count = left.split(', ')
    starting = ('*' in id)
    id = id[0]
    count = int(count)

    roads = []
    cities = []
    graveyard = False
    parts = right.split(', ')
    for part in parts:
        if part == 'G':
            graveyard = True
            continue

        left, right = part.split('(')
        right = right.replace(')', '')

        if left == 'C':
            cities = right.split('|')
        elif left == 'R':
            roads = right.split('|')
        else:
            raise ValueError

    return [Tile(id=id, starting=starting, roads=roads, cities=cities, graveyard=graveyard) for _ in range(count)]


def load_tiles():
    result = []
    with open(settings.tiles_data_file) as input_file:
        for line in input_file.readlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            result += create_tiles_from_data(line)

    return result


class Components:
    def __init__(self):
        self.tiles = []

    def init(self):
        self.tiles = load_tiles()


g.components = Components()
