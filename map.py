from settings import settings
from global_states import g


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


g.map = Map()
