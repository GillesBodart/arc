import uuid
from uuid import UUID


class Cell(object):

    def __init__(self, grid, x, y, color):
        self.uuid = str(uuid.uuid4())
        self.grid = grid
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.color = color
        self._neighbors = None
        self._depth = None

    def set_color(self, color):
        self.color = color

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def identical(self, other):
        return self.x == other.x and self.y == other.y and self.color == other.color

    def set_neighbors(self, depth=1):
        size = 3 + (depth - 1) * 2
        self._neighbors = [[None for i in range(size)] for j in range(size)]
        x_i = 0
        y_i = 0
        for i in [ int(i - (size -1)/2) for i in range(size) ]:
            for j in [ int(i - (size -1)/2) for i in range(size) ]:
                self._neighbors[x_i][y_i] = self.grid.get_cell(self.x + i, self.y + j)
                y_i +=1
            x_i += 1
            y_i = 0

    def _init_neighbors(self, depth=1):
        if self._neighbors is None or self._depth != depth:
            self.depth = depth
            self.set_neighbors(depth)

    def get_neighbor(self, x, y):
        self._init_neighbors()
        return self._neighbors[x][y]

    def get_neighbors(self):
        self._init_neighbors()
        return [cell for row in self._neighbors for cell in row if cell is not None]

    def get_color_neighbors(self):
        self._init_neighbors()
        return [cell for row in self._neighbors for cell in row if cell is not None and self.color == cell.color]

    def get_color_neighbors_matrix(self, depth=1):
        self._init_neighbors(depth)
        neigh = [[cell if cell is not None and self.color == cell.color else None for cell in row] for row in self._neighbors]
        return [[cell.color if cell is not None else 0 for cell in row] for row in neigh]

    def get_neighbors_matrix(self, depth=1):
        self._init_neighbors(depth)
        return [[cell.color if cell is not None else 0 for cell in row] for row in self._neighbors]

    def touch(self, other):
        distance = abs((self.x - other.x) + (self.y - other.y))
        return 3 > distance > 0

    def color_touch(self, other):
        return self.touch(other) and self.color == other.color

    def __gt__(self, other):
        return self.x < other.x and self.y < other.y

    def __lt__(self, other):
        return self.x > other.x and self.y > other.y

    def __ge__(self, other):
        return self.x <= other.x and self.y <= other.y

    def __le__(self, other):
        return self.x >= other.x and self.y >= other.y

    def __str__(self):
        return self.color

    def is_active(self):
        return self.color > 0
