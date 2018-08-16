from settings import settings
from global_states import g
from functools import partial
from simple_logger import log
from location import WorkerLocation


class Worker:
    def __init__(self, player, alive):
        self.player = player
        self.location = None
        self.alive = alive

    def place(self, tile, worker_space):
        self.location = WorkerLocation(tile, worker_space)

    def retire(self):
        self.location = None

    def __repr__(self):
        return '<Worker>(player={}, location={}, alive={})'.format(self.player, self.location, self.alive)


def rotate(x, orientation):
    if isinstance(x, int):
        return (x + orientation) % 4
    if isinstance(x, (list, tuple)):
        return [rotate(l, orientation) for l in x]
    raise ValueError


def flip_edge(edge):
    return {0: 2, 1: 3, 2: 0, 3: 1}[edge]


def get_edges(roads, cities):
    edges = {
        e: 'B'
        for e in range(4)
    }

    for a in roads:
        for b in a:
            edges[b] = 'R'

    for a in cities:
        for b in a:
            edges[b] = 'C'

    return edges


class Tile:
    def __init__(self, id, starting, roads, cities, graveyard):
        self.id = id
        self._image_name = 'tile_{}'.format(id.lower())
        self.starting = starting
        self.roads = roads
        self.cities = cities
        self.graveyard = graveyard
        self.worker = None
        self.worker_at = None

        # 0: 0 degrees, 1: 90, 2: 180, 3: 270
        self.orientation = 0

        self.location = None

        self.edges = get_edges(roads, cities)

    def image_name(self, is_dark):
        return 'dark_{}'.format(self._image_name) if is_dark else 'light_{}'.format(self._image_name)

    # @property
    # def road_edges(self):
    #     return "".join(self.roads)
    #
    # @property
    # def city_edges(self):
    #     return "".join(self.cities)
    #

    def space_on_road(self, space):
        for road in self.roads:
            if space in road:
                return True
        return False

    def space_in_city(self, space):
        for city in self.cities:
            if space in city:
                return True
        return False

    def orientated_copy(self, orientation):
        tile = Tile(
            id=self.id,
            starting=self.starting,
            roads=rotate(self.roads, orientation),
            cities=rotate(self.cities, orientation),
            graveyard=self.graveyard
        )
        if self.roads:
            log('Rotated roads {} by {} to get {}'.format(self.roads, orientation, rotate(self.roads, orientation)))
        if self.cities:
            log('Rotated cities {} by {} to get {}'.format(self.cities, orientation, rotate(self.cities, orientation)))
        tile.orientation = orientation
        return tile

    def unplace(self):
        location = self.location
        orientation = self.orientation

        g.map[location].edges = {e: '' for e in range(4)}
        for l in location.neighbours:
            g.map[l].has_neighbours -= 1

        not_blank = []

        for cities in self.cities:
            for c in cities:
                not_blank.append(c)
                l = g.map[location].neighbour_at_edge(c)
                if l and not g.map[l].edges[flip_edge(c)]:
                    g.map[l].edges[flip_edge(c)] = ''

        for roads in self.roads:
            for r in roads:
                not_blank.append(r)
                l = g.map[location].neighbour_at_edge(r)
                if l and g.map[l].tile is None and not g.map[l].edges[flip_edge(r)]:
                    g.map[l].edges[flip_edge(r)] = ''

        for s in range(4):
            if s not in not_blank:
                l = g.map[location].neighbour_at_edge(s)
                if l and g.map[l].tile is None and not g.map[l].edges[flip_edge(s)]:
                    g.map[l].edges[flip_edge(s)] = ''

        self.cities = rotate(self.cities, -orientation)
        self.roads = rotate(self.roads, -orientation)
        self.edges = get_edges(self.roads, self.cities)

        # self.location = None
        # self.orientation = 0
        g.map[location].tile = None

        log('Just unplaced {}'.format(self))

    def place(self, location, orientation):
        self.cities = rotate(self.cities, orientation)
        self.roads = rotate(self.roads, orientation)
        self.edges = get_edges(self.roads, self.cities)

        g.map[location].edges = {e: '' for e in range(4)}
        g.map[location].tile = self
        self.location = location
        self.orientation = orientation
        for l in location.neighbours:
            g.map[l].has_neighbours += 1

        not_blank = []

        log('Just placed {}'.format(self))

        for cities in self.cities:
            for c in cities:
                not_blank.append(c)
                g.map[location].edges[c] = 'C'
                l = g.map[location].neighbour_at_edge(c)
                if l and not g.map[l].edges[flip_edge(c)]:
                    g.map[l].edges[flip_edge(c)] = 'C'

        for roads in self.roads:
            for r in roads:
                not_blank.append(r)
                g.map[location].edges[r] = 'R'
                l = g.map[location].neighbour_at_edge(r)
                if l and g.map[l].tile is None and not g.map[l].edges[flip_edge(r)]:
                    g.map[l].edges[flip_edge(r)] = 'R'

        for s in range(4):
            if s not in not_blank:
                l = g.map[location].neighbour_at_edge(s)
                if l and g.map[l].tile is None and not g.map[l].edges[flip_edge(s)]:
                    g.map[l].edges[flip_edge(s)] = 'B'

    def fits(self, location):
        for edge in range(4):
            if g.map[location].edges[edge] and g.map[location].edges[edge] != self.edges[edge]:
                log('{}, {} fit in {} at {}? No'.format(self.id, self.edges, g.map[location].edges, location))
                return False

        log('{}, {} fit in {} at {}? Yes'.format(self.id, self.edges, g.map[location].edges, location))
        return True

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
            cities = [[int(x) for x in y] for y in right.split('|')]
        elif left == 'R':
            roads = [[int(x) for x in y] for y in right.split('|')]
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
    for player in g.players:
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
    def _filter_by_on_tile(component, tile):
        return isinstance(component, Worker) and component.location and component.location.tile == tile

    @staticmethod
    def matches_filters(component, filters):
        for filter in filters:
            if not filter(component):
                return False
        return True

    def filter(self, starting_tile=None, player=None, alive=None, placed=None, klass=None, on_tile=None):
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

        if on_tile is not None:
            filters.append(partial(self._filter_by_on_tile, tile=on_tile))

        return [component for component in self.all if self.matches_filters(component, filters)]


g.components = Components()
