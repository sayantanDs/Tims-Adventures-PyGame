

class GameScene:
    def __init__(self):
        pass

    def render(self, surface):
        raise NotImplementedError

    def update(self, delta_time):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError
