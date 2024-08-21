from src.model.grid import Grid


class ChallengePair(object):

    def __init__(self, input, output):
        self.input_grid = Grid(input)
        self.output_grid = Grid(output)
