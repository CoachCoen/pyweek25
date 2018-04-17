from settings import settings
from global_states import g
from functools import partial


class Worker:
    def __init__(self, player, alive):
        self.player = player
        self.location = None
        self.alive = alive


class Tile:
    def __init__(self, id, starting, roads, cities, graveyard):
        self.id = id
        self._image_name = 'tile_{}'.format(id.lower())
        self.starting = starting
        self._roads = roads
        self._cities = cities
        self.graveyard = graveyard

        # 0: 0 degrees, 1: 90, 2: 180, 3: 270
        self.orientation = 0

        self.location = None

    def image_name(self, is_dark):
        return 'dark_{}'.format(self._image_name) if is_dark else 'light_{}'.format(self._image_name)

    @property
    def roads(self):
        return self.orientate_edges_list(self._roads, self.orientation)

    @property
    def cities(self):
        return self.orientate_edges_list(self._cities, self.orientation)

    @property
    def road_edges(self):
        return "".join(self.roads)

    @property
    def city_edges(self):
        return "".join(self.cities)

    @staticmethod
    def rotate(edge, orientation):
        return {
            'E': 'ESWN',
            'S': 'SWNE',
            'W': 'WNES',
            'N': 'NESW'
        }[edge][orientation]

    def orientate_edges_list(self, edges_list, orientation):
        return [self.orientate(edges, orientation) for edges in edges_list]

    # TODO: More OO?
    def orientate(self, edges, orientation):
        return ''.join(self.rotate(edge, orientation) for edge in edges)

    @staticmethod
    def flip_edge(edge):
        return {
            'E': 'W',
            'W': 'E',
            'N': 'S',
            'S': 'N'
        }[edge]

    def has_road_edge(self, edge):
        # print("has_road_edge, {} in {}: {}".format(edge, self.road_edges, edge in self.road_edges))
        return edge in self.road_edges

    def has_city_edge(self, edge):
        # print("has_city_edge, {} in {}: {}".format(edge, self.city_edges, edge in self.city_edges))

        return edge in self.city_edges

    @property
    def neighbours(self):
        return g.map.neighbours(self.location)

    def fits(self, location, orientation):
        # print('Fits?')
        print('')

        for road_edge in self.road_edges:
            neighbour = g.map.neighbour_on_edge(location, road_edge)
            if neighbour and not neighbour.has_road_edge(self.flip_edge(road_edge)):
                # print("Missing road edge")
                return False

        for city_edge in self.city_edges:
            neighbour = g.map.neighbour_on_edge(location, city_edge)
            if neighbour and not neighbour.has_city_edge(self.flip_edge(city_edge)):
                # print("Missing city edge")
                return False

        print(self)
        print('fits at {} matches'.format(location))
        for neighbour in g.map.neighbours(location):
            if neighbour:
                print(neighbour)

        return True

    def place(self, location, orientation):
        g.map.cells[location.x][location.y] = self
        self.orientation = orientation
        self.location = location

    def __repr__(self):
        return '[{x}, {y}, cities: {cities}, roads: {roads}, orientation: {orientation}, id: {id}'.format(
            x=self.location.x if self.location else '',
            y=self.location.y if self.location else '',
            cities=self.cities,
            roads=self.roads,
            orientation=self.orientation,
            id=self.id,
        )


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


def create_workers():
    result = []
    for player in g.players.players:
        for _ in range(settings.workers_per_player):
            for alive in True, False:
                result.append(Worker(player=player, alive=alive))
    return result


class Components:
    def __init__(self):
        self.tiles = []
        self.workers = []

    def init(self):
        self.tiles = load_tiles()
        self.workers = create_workers()

    @property
    def all(self):
        return self.tiles + self.workers

    @staticmethod
    def _filter_by_starting(component, is_starting):
        return isinstance(component, Tile) and component.starting == is_starting

    @staticmethod
    def _filter_by_player(component, player):
        return isinstance(component, Worker) and component.player == player

    @staticmethod
    def _filter_by_is_alive(component, alive):
        return isinstance(component, Worker) and component.alive == alive

    @staticmethod
    def _filter_by_is_placed(component, placed):
        return placed == (component.location is not None)

    @staticmethod
    def _filter_by_klass(component, klass):
        if klass == 'tile':
            return isinstance(component, Tile)
        if klass == 'worker':
            return isinstance(component, Worker)
        raise ValueError

    @staticmethod
    def matches_filters(component, filters):
        for filter in filters:
            if not filter(component):
                return False
        return True

    def filter(self, starting_tile=None, player=None, alive=None, placed=None, klass=None):
        filters = []
        if starting_tile is not None:
            filters.append(partial(self._filter_by_starting, is_starting=starting_tile))

        if player is not None:
            filters.append(partial(self._filter_by_player, player=player))

        if alive is not None:
            filters.append(partial(self._filter_by_is_alive, alive=alive))

        if placed is not None:
            filters.append(partial(self._filter_by_is_placed, placed=placed))

        if klass is not None:
            filters.append(partial(self._filter_by_klass, klass=klass))

        return [component for component in self.all if self.matches_filters(component, filters)]


g.components = Components()
