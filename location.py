from settings import settings


def on_the_map(x, y):
    return 0 <= x < settings.map_columns and 0 <= y < settings.map_rows


def get_neighbours(location, include_vertical):
    result = []
    delta_locations = ((-1, 0), (1, 0), (0, -1), (0, 1))
    if include_vertical:
        delta_locations += ((-1, -1), (-1, 1), (1, -1), (1, 1))
    for dx, dy in delta_locations:
        nx, ny = location.x + dx, location.y + dy
        if on_the_map(nx, ny):
            result.append(Location(nx, ny))
    return result


class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return self.x + self.y * 1000

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Location(self.x + other.x, self.y + other.y)

    @property
    def neighbours(self):
        return get_neighbours(self, include_vertical=False)

    @property
    def all_neighbours(self):
        return get_neighbours(self, include_vertical=True)

    def __repr__(self):
        return '<Location>({}, {})'.format(self.x, self.y)


class WorkerLocation:
    def __init__(self, tile, space):
        self.tile = tile
        self.space = space

    def __repr__(self):
        return '<WorkerLocation>(tile={}, space={})'.format(self.tile, self.space)
