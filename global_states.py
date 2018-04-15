class GlobalStates:
    def __init__(self):
        self.components = None
        self.screen = None

    def init(self):
        self.components.init()


g = GlobalStates()
