
class BackTesting:

    def __init__(self, strategies=()):
        if strategies is None:
            strategies = []
        self.strategies = strategies
