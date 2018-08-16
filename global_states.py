class GlobalStates:
    def __init__(self):
        self.components = None
        self.screen = None
        self.images = None
        self.map = None
        self._players = None
        self.buttons = None
        self.turn_state = None

    def init(self):
        self._players.init()
        self.components.init()
        self.images.init()

    @property
    def players(self):
        return self._players.players

    @property
    def current_player(self):
        return self.turn_state.current_player

    @property
    def current_player_number(self):
        return self.turn_state.current_player_number


g = GlobalStates()
