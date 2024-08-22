import copy


class Molecule(object):

    def __init__(self, cells):
        self.cells = cells
        self.size = len(cells)
        if self.size > 0:
            self.max_x = max([cell.x for cell in self.cells])
            self.min_x = min([cell.x for cell in self.cells])
            self.max_y = max([cell.y for cell in self.cells])
            self.min_y = min([cell.y for cell in self.cells])
            self.width = self.max_x - self.min_x + 1
            self.height = self.max_y - self.min_y + 1

            self.molecule_linked_list = [[cell for cell in cells if cell.x == x] for x in range(self.width)]

            self.molecule_grid = [[None for i in range(self.height)] for j in range(self.width)]
            for cell in cells:
                self.molecule_grid[cell.x - self.min_x][cell.y - self.min_y] = cell

    def __sub__(self, other):
        new_cells = []
        for cell in new_cells:
            found = False
            for other_cell in other.cells:
                found |= cell == other_cell
            if found:
                new_cells.append(copy.copy(cell))
        return Molecule(new_cells)

    def set_color(self, color):
        for cell in self.cells:
            cell.set_color(color)

    def is_same_color(self):
        same = True
        last_color = None
        for cell in self.cells:
            if last_color is None:
                last_color = cell.color
            else:
                same &= cell.color == last_color
        return same

    def is_filled(self):
        filled = True
        for line in self.molecule_linked_list:
            filled &= (max([cell.y for cell in line]) - min([cell.y for cell in line]) + 1) == len(line)
        return filled

    def is_sub_of(self, other):
        if self.size > other.size:
            return False
        diff = self - other
        return diff.size == 0


    def matrix(self):
        return [[cell.color if cell is not None else 0 for cell in row] for row in self.molecule_grid]