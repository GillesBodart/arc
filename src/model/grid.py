from enum import Enum
import copy
import matplotlib.pyplot as plt
from matplotlib import colors
import seaborn as sns

from src.model.cell import Cell
from src.model.molecule import Molecule


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
        self._cell_grid = [[Cell(self, row, column, grid[row][column]) for column in range(self.shape[1])] for row in range(self.shape[0])]
        self.discover_molecules()

    def add_molecule(self, molecule):
        self.molecules.append(molecule)

    def get_cell(self, row, column):
        if row < 0 or row >= self.shape[0] or column < 0 or column >= self.shape[1]:
            return None
        return self._cell_grid[row][column]

    def set_cell(self, row, column, cell):
        if not (row < 0 or row >= self.shape[0] or column < 0 or column >= self.shape[1]):
            self._cell_grid[row][column] = cell

    def sub_grid(self, row_start, row_end, column_start, column_end):
        return Grid(self._grid[row_start:row_end, column_start:column_end])

    def append(self, other, direction):
        new_shape = self.shape
        other_grid = other._grid[:][:]
        if direction == AppendDirection.UP or direction == AppendDirection.DOWN:
            new_shape = (new_shape[0] + other.shape[0], new_shape[1])
        elif direction == AppendDirection.UP_LEFT or direction == AppendDirection.DOWN_LEFT or direction == AppendDirection.UP_RIGHT or direction == AppendDirection.DOWN_RIGHT:
            new_shape = (new_shape[0] + other.shape[0], new_shape[1] + other.shape[1])
        elif direction == AppendDirection.LEFT or direction == AppendDirection.RIGHT:
            new_shape = (new_shape[0], new_shape[1] + other.shape[1])
        new_grid = [[0 for column in range(new_shape[1])] for row in range(new_shape[0])]
        if direction == AppendDirection.UP:
            for row in range(other.shape[0]):
                for col in range(other.shape[1]):
                    new_grid[row][col] = other._grid[row][col]
            for row in range(self.shape[0]):
                for col in range(self.shape[1]):
                    new_grid[row + other.shape[0]][col] = self._grid[row][col]

        if direction == AppendDirection.DOWN:
            for row in range(self.shape[0]):
                for col in range(self.shape[1]):
                    new_grid[row][col] = self._grid[row][col]
            for row in range(other.shape[0]):
                for col in range(other.shape[1]):
                    new_grid[row + other.shape[0]][col] = other._grid[row][col]

        if direction == AppendDirection.RIGHT:
            for row in range(self.shape[0]):
                for col in range(self.shape[1]):
                    new_grid[row][col] = self._grid[row][col]
            for row in range(other.shape[0]):
                for col in range(other.shape[1]):
                    new_grid[row][col + other.shape[1]] = other._grid[row][col]

        if direction == AppendDirection.LEFT:
            for row in range(other.shape[0]):
                for col in range(other.shape[1]):
                    new_grid[row][col] = other._grid[row][col]
            for row in range(self.shape[0]):
                for col in range(self.shape[1]):
                    new_grid[row][col + other.shape[1]] = self._grid[row][col]

        if direction == AppendDirection.UP_LEFT:
            for row in range(other.shape[0]):
                for col in range(other.shape[1]):
                    new_grid[row][col] = other._grid[row][col]
            for row in range(self.shape[0]):
                for col in range(self.shape[1]):
                    new_grid[row + other.shape[0]][col + other.shape[1]] = self._grid[row][col]

        if direction == AppendDirection.UP_RIGHT:
            for row in range(other.shape[0]):
                for col in range(other.shape[1]):
                    new_grid[row][col + other.shape[1]] = other._grid[row][col]
            for row in range(self.shape[0]):
                for col in range(self.shape[1]):
                    new_grid[row + other.shape[0]][col] = self._grid[row][col]

        if direction == AppendDirection.DOWN_LEFT:
            for row in range(other.shape[0]):
                for col in range(other.shape[1]):
                    new_grid[row + other.shape[0]][col] = other._grid[row][col]
            for row in range(self.shape[0]):
                for col in range(self.shape[1]):
                    new_grid[row][col + other.shape[1]] = self._grid[row][col]

        if direction == AppendDirection.DOWN_RIGHT:
            for row in range(self.shape[0]):
                for col in range(self.shape[1]):
                    new_grid[row + other.shape[0]][col + other.shape[1]] = self._grid[row][col]
            for row in range(other.shape[0]):
                for col in range(other.shape[1]):
                    new_grid[row][col] = other._grid[row][col]
        return Grid(new_grid)

    def __sub__(self, other):
        new_grid = copy.deepcopy(self._grid)
        if (other.shape != self.shape):
            raise ValueError("Shapes do not match")
        else:
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    if other._grid[i][j] != 0:
                        new_grid[i][j] = 0
        return Grid(new_grid)

    def __add__(self, other):
        new_grid = copy.deepcopy(self._grid)
        if (other.shape != self.shape):
            raise ValueError("Shapes do not match")
        else:
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    if other._grid[i][j] != 0:
                        new_grid[i][j] = other._grid[i][j]
        return Grid(new_grid)

    def discover_molecules(self):
        self.molecules = []
        mol_memos = {}
        for row in self._cell_grid:
            for cell in row:
                if cell.uuid not in mol_memos and cell.is_active():
                    memo_cell = {}
                    self._propagate(memo_cell, cell)
                    self.add_molecule(Molecule(memo_cell.values()))
                    mol_memos = {**mol_memos, **memo_cell}

    def _propagate(self, memo, cell):
        if cell.is_active() and cell.uuid not in memo:
            memo[cell.uuid] = cell
            for neighbor in cell.get_neighbors():
                self._propagate(memo, neighbor)

    def show(self):
        fig = plt.figure()
        ax = fig.subplots()
        cmap = colors.ListedColormap(['#000000', '#0074D9', '#FF4136', '#2ECC40', '#FFDC00',
                                      '#AAAAAA', '#F012BE', '#FF851B', '#7FDBFF', '#870C25'])
        norm = colors.Normalize(vmin=0, vmax=9)
        input_matrix = self._grid
        ax.imshow(input_matrix, cmap=cmap, norm=norm)
        ax.grid(True, which='both', color='lightgrey', linewidth=0.5)

        plt.setp(plt.gcf().get_axes(), xticklabels=[], yticklabels=[])
        ax.set_xticks([x - 0.5 for x in range(1 + len(input_matrix[0]))])
        ax.set_yticks([x - 0.5 for x in range(1 + len(input_matrix))])
        # plot.set_title(train_or_test + ' ' + input_or_output, fontweight='bold')
