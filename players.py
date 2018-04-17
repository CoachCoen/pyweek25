from global_states import g


class Player:
    def __init__(self, name, AI, colour):
        self.name = name
        self.AI = AI
        self.colour = colour

    def unplaced_workers(self, alive):
        return g.components.filter(player=self, alive=alive, placed=False)


class Players:
    def __init__(self):
        self.players = []

    def init(self):
        for name, AI, colour in (
                ('Sue', None, 'red'),
                ('John', None, 'green'),
                ('Elisa', None, 'blue'),
                ('Me', None, 'yellow')
        ):
            self.players.append(Player(name, AI, colour))


g.players = Players()
