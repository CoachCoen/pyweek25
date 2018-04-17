from settings import settings
from global_states import g
from vector import Vector


class Map:
    def __init__(self):
        # create a map_columns x map_rows 'array'
        self.cells = {
            column: {
                row: None
                for row in range(settings.map_rows)}
            for column in range(settings.map_columns)
        }

        # TODO, maybe: make it so I can address this directly, as map[r][c]

    def tile_at(self, location):
        return self.cells[location.x][location.y]

    @staticmethod
    def on_map(location):
        return 0 <= location.x < settings.map_columns and 0 <= location.y < settings.map_rows

    def is_free(self, location):
        return self.cells[location.x][location.y] is None

    def neighbour_on_edge(self, location, edge):
        offset = {
            'N': Vector(0, -1),
            'E': Vector(1, 0),
            'S': Vector(0, 1),
            'W': Vector(-1, 0)
        }[edge]
        location += offset

        return self.tile_at(location) if self.on_map(location) else None

        retu1

    def neighbour_locations(self, location):
        return [
            location + offset
            for offset in (Vector(-1, 0), Vector(1, 0), Vector(0, -1), Vector(0, 1))
            if self.on_map(location + offset)
        ]

    def neighbours(self, location):
        return [
            self.tile_at(neighbour_location)
            for neighbour_location in self.neighbour_locations(location)
        ]

    def has_neighbours(self, location):
        for neighbour_location in self.neighbour_locations(location):
            if not self.is_free(neighbour_location):
                return True
        return False

    @staticmethod
    def all_locations():
        for x in range(settings.map_columns):
            for y in range(settings.map_rows):
                yield Vector(x, y)

    def available_locations(self):
        """
        Find all the locations which are empty and next to a non-empty location
        """
        return [location for location in self.all_locations() if self.is_free(location) and self.has_neighbours(location)]

g.map = Map()
