class GlobalStates:
    def __init__(self):
        self.components = None
        self.screen = None
        self.images = None
        self.map = None
        self.players = None
        self.current_player = 0

    def init(self):
        self.players.init()
        self.components.init()
        self.images.init()


g = GlobalStates()
