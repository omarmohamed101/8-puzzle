
class State:

    def __init__(self, state, parent, move, cost, key):

        self.state = state

        self.parent = parent

        self.move = move

        self.cost = cost

        self.key = key

        if self.state:
            # ex 1234567780
            self.map = ''.join(str(e) for e in self.state)

    # specify method for the heappop operation
    def __lt__(self, other):
        return self.map < other.map
