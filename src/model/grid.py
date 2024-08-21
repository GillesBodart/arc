from enum import Enum


class AppendDirection(Enum):
    UP = 0
    UP_LEFT = 1
    UP_RIGHT = 2
    LEFT = 3
    RIGHT = 4
    DOWN = 5
    DOWN_LEFT = 6
    DOWN_RIGHT = 7


class Grid(object):

    def __init__(self, grid):
        self.shape = (len(grid[0]), len(grid))
        self._grid = grid

    def sub_grid(self, row_start,row_end, column_start,column_end):
        return Grid(self._grid[row_start:row_end,column_start:column_end])


    def append(self, other, direction):
        new_shape = self.shape
        if direction == AppendDirection.UP or direction == AppendDirection.DOWN:
            new_shape[0] += other.shape[0]
        elif direction == AppendDirection.UP_LEFT or direction == AppendDirection.DOWN_LEFT or direction == AppendDirection.UP_RIGHT or direction == AppendDirection.DOWN_RIGHT:
            new_shape[0] += other.shape[0]
            new_shape[1] += other.shape[1]
        elif direction == AppendDirection.LEFT or direction == AppendDirection.RIGHT:
            new_shape[1] += other.shape[1]
        new_grid = [[0 for column in range(new_shape[1])] for row in range(new_shape[0])]
        if direction == AppendDirection.UP:
            for row in range(other.shape[0]):
                for col in range(other.shape[1]):
                    new_grid[row][col] += other._grid[row][col]
            for row in range(self.shape[0]):
                for col in range(self.shape[1]):
                    new_grid[row+other.shape[0]][col] += self._grid[row][col]
        return Grid(new_grid)

    def __sub__(self, other):
        new_grid = self._grid[:][:]
        if (other.shape != self.shape):
            raise ValueError("Shapes do not match")
        else:
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    if other._grid[i][j] != 0:
                        new_grid[i][j] = 0
        return Grid(new_grid)

    def __add__(self, other):
        new_grid = self._grid[:][:]
        if (other.shape != self.shape):
            raise ValueError("Shapes do not match")
        else:
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    if other._grid[i][j] != 0:
                        self._grid[i][j] = other._grid[i][j]
        return Grid(new_grid)
