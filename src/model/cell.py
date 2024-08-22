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

    def set_color(self, color):
        self.color = color

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def identical(self, other):
        return self.x == other.x and self.y == other.y and self.color == other.color

    def set_neighbors(self, depth=1):
        self._neighbors = [[None for i in range(3 + (depth - 1) * 2)] for j in range(3 + (depth - 1) * 2)]
        for i in range(3 + (depth - 1) * 2):
            for j in range(3 + (depth - 1) * 2):
                self._neighbors[i][j] = self.grid.get_cell(self.x - i, self.y - j)
            self._neighbors[0][0] = self.grid.get_cell(self.x - depth, self.y - depth)
            self._neighbors[0][1] = self.grid.get_cell(self.x - depth, self.y)
            self._neighbors[0][2] = self.grid.get_cell(self.x - depth, self.y + depth)
            self._neighbors[1][0] = self.grid.get_cell(self.x, self.y - depth)
            self._neighbors[1][1] = self.grid.get_cell(self.x, self.y)
            self._neighbors[1][2] = self.grid.get_cell(self.x, self.y + depth)
            self._neighbors[2][0] = self.grid.get_cell(self.x + depth, self.y - depth)
            self._neighbors[2][1] = self.grid.get_cell(self.x + depth, self.y)
            self._neighbors[2][2] = self.grid.get_cell(self.x + depth, self.y + depth)

    def _init_neighbors(self):
        if self._neighbors is None:
            self.set_neighbors()

    def get_neighbor(self, x, y):
        self._init_neighbors()
        return self._neighbors[x][y]

    def get_neighbors(self):
        self._init_neighbors()
        return [cell for row in self._neighbors for cell in row if cell is not None]

    def get_color_neighbors(self):
        self._init_neighbors()
        return [cell for row in self._neighbors for cell in row if cell is not None and self.color == cell.color]

    def get_color_neighbors_matrix(self):
        self._init_neighbors()
        return [[cell.color if cell is not None else 0 for cell in row] for row in self.get_color_neighbors()]

    def get_neighbors_matrix(self):
        self._init_neighbors()
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
