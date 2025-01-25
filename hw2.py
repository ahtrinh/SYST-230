"""SYST 230 HW2: Game of Life with OO Programming
Author: M. Amissah"""

import copy
import turtle


class CellularAutomata:
    def __init__(self, pen, nrows=10, ncols=10):
        """Initializes prescribed attributes as follows:
        pen, nrows, ncols: are given by method arguments
        gen_number is equal to 0
        grid is a nested list nrows x ncols of 0's
        Must invoke the pen's draw_grid method"""
        self.nrows, self.ncols, self.pen = nrows, ncols, pen
        self.gen_number = 0
        self.grid = [[0 for _ in range(self.ncols)] for _ in range(self.nrows)]
        self.pen.draw_grid(self)

    def count_neighbors(self, r: int, c: int) -> int:
        """Given row and column indices (i.e. r and c) and the CA's state (i.e. grid)
        Returns a count of living neighbors of the cell referenced by the given
        indices in the grid i.e. cell at grid[r][c]
        NB: Boundary cells will have fewer than 8 neighbors"""
        hood = [(r, c - 1), (r, c + 1),
                (r + 1, c - 1), (r + 1, c), (r + 1, c + 1),
                (r - 1, c - 1), (r - 1, c), (r - 1, c + 1)]
        # remove bad cells
        hood = [(r, c) for r, c in hood if (-1 < r < self.nrows and -1 < c < self.ncols)]
        return sum(self.grid[i][j] for i, j in hood)

    def apply_rules(self):
        """Given the current state of the CA (i.e. grid) applies
        the rules of the Game of life to each cell in the grid,
        by invoking the count_neighbors function and returns a
        new grid with state values for the next generation
        HINT: Copy grid into a new_grid (USE deepcopy from copy module),
            make changes to new_grid based on old grid
            Must set grid attribute to new_grid,
        Must increment gen_number and invoke pen's draw_grid method"""
        next_gen = copy.deepcopy(self.grid)
        for r in range(self.nrows):
            for c in range(self.ncols):
                n = self.count_neighbors(r, c)
                if self.grid[r][c] == 1 and n < 2:  # R1
                    next_gen[r][c] = 0
                elif self.grid[r][c] == 1 and n > 3:  # R2
                    next_gen[r][c] = 0
                elif self.grid[r][c] == 0 and n == 3:  # R4
                    next_gen[r][c] = 1
        self.grid = next_gen
        self.gen_number += 1
        self.pen.draw_grid(self)

    def add_pattern(self, *living: tuple[int, int]):
        """Given the state of the CA, (i.e. grid) and a list of
        coordinates specifying indices for living cells set cells in grid
        referenced by indices to ALIVE
        Must invoke pen's draw_grid method"""
        living = living or [(7, 1), (7, 2), (7, 3)]
        for r, c in living:
            if -1 < r < self.nrows and -1 < c < self.ncols:
                self.grid[r][c] = 1 if not self.grid[r][c] else 0
        self.pen.draw_grid(self)

    def draw_grid(self):
        self.pen.draw_grid(self)

class Pen(turtle.RawTurtle):
    def __init__(self, screen=None, csize=50, start=(-250, -250)):
        """Initialize prescribed attributes as follows:
        csize, start; are given by method arguments
        screen: if value given is None use default turtle screen
                i.e. turtle.getscreen()
        Must invoke super with screen attribute
        Optional:
            Initialize color options for painting living or dead  CA cells
        """
        self.csize, self.start = csize, start
        screen = screen or turtle.getscreen()
        super().__init__(screen)
        self.pencolor("darkGray")
        self.grid_colors = "#303030", "#ffffff"
        self.ht()

    def draw_cell(self, colr: int=0):
        """Draws a cell in the CA
        (maybe shaded or plane) based on colr parameter """
        col = self.grid_colors[0] if colr else self.grid_colors[1]
        self.fillcolor(col)
        self.begin_fill()
        # fwd size, left 90: 4 times
        [(self.forward(self.csize), self.left(90)) for _ in range(4)]
        self.end_fill()

    def draw_grid(self, ca: CellularAutomata):
        """Uses turtle to draw grid of given CA, with cell size 50
        Cells are colored based on the cell state (i.e. alive or dead) stored
        in CA's grid attribute
        Hint: Use screen attributes tracer function to speed up drawing
            ex. self.screen.tracer(1000)
            Must invoke screen update if tracer is used"""
        self.screen.tracer(1000)
        self.pu()
        self.goto(self.start)
        self.pd()
        x0, y0 = self.start
        y = y0
        for row in ca.grid:
            for cell in row:
                self.draw_cell(cell)
                self.forward(self.csize)
            y += self.csize
            self.pu(); self.goto(x0, y); self.pd()
        self.screen.update()


