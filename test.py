# Hmm, how about this
# g.map[location].cell
# g.map.all_cells


class Map:
    def __init__(self):
        self.locations = {i: 'test {}'.format(i) for i in range(10)}

    def all_cells(self):
        return 'All cells'

    def __getitem__(self, item):
        return self.locations[item]

map = Map()
