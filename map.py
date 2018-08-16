from settings import settings
from global_states import g
from location import Location, on_the_map


class Cell:
    def __init__(self, location):
        self.tile = None
        self.tile_in_progress = None
        self.location = location
        self.has_neighbours = 0
        self.edges = {e: '' for e in range(4)}

    def neighbour_at_edge(self, edge):
        location = self.location + {
            0: Location(0, -1),
            1: Location(1, 0),
            2: Location(0, 1),
            3: Location(-1, 0)
        }[edge]
        return location if on_the_map(location.x, location.y) else None


class Map:
    def __init__(self):
        self.all_locations = [
            Location(x, y)
            for x in range(settings.map_columns)
            for y in range(settings.map_rows)
        ]

        self.cells = {
            location: Cell(location)
            for location in self.all_locations
        }

    def __getitem__(self, item):
        # Pretend that the temporary tile is part of the map - so we can work out roads and cities
        if g.turn_state.next_tile and g.turn_state.next_tile.location and g.turn_state.next_tile.location == item:
            cell = Cell(g.turn_state.next_tile.location)
            cell.tile = g.turn_state.next_tile.orientated_copy(g.turn_state.next_tile_orientation)
            return cell
        return self.cells[item]

    def available_locations(self):
        """
        Find all the locations which are empty and next to a non-empty location
        """
        return [
            location
            for location in self.all_locations
            if self[location].tile is None and self[location].has_neighbours
        ]


g.map = Map()
