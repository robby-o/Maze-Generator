import time
import random
from graphics import Window
from cell import Cell


class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells = []
        for _ in range(self._num_cols):
            cols_cells = []
            for _ in range(self._num_rows):
                cols_cells.append(Cell(self._win))
            self._cells.append(cols_cells)
        for col in range(self._num_cols):
            for row in range(self._num_rows):
                self._draw_cell(col, row)

    def _draw_cell(self, col, row):
        if self._win is None:
            return
        x1 = self._x1 + col * self._cell_size_x
        y1 = self._y1 + row * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[col][row].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        entrance_wall = random.choice(["has_left_wall", "has_top_wall"])
        entrance_cell = self._cells[0][0]
        setattr(entrance_cell, entrance_wall, False)
        self._draw_cell(0, 0)

        exit_wall = random.choice(["has_right_wall", "has_bottom_wall"])
        exit_cell = self._cells[self._num_cols - 1][self._num_rows - 1]
        setattr(exit_cell, exit_wall, False)
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, col, row):
        self._cells[col][row].visited = True
        while True:
            next_index_list = []

            # determine which cell(s) to visit next
            # left
            if col > 0 and not self._cells[col - 1][row].visited:
                next_index_list.append((col - 1, row))
            # right
            if col < self._num_cols - 1 and not self._cells[col + 1][row].visited:
                next_index_list.append((col + 1, row))
            # up
            if row > 0 and not self._cells[col][row - 1].visited:
                next_index_list.append((col, row - 1))
            # down
            if row < self._num_rows - 1 and not self._cells[col][row + 1].visited:
                next_index_list.append((col, row + 1))

            # if there is nowhere to go from here
            # just break out
            if not next_index_list:
                self._draw_cell(col, row)
                return

            # randomly choose next direction to go
            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]

            # knock out walls between this cell and the next cell(s)
            # right
            if next_index[0] == col + 1:
                self._cells[col][row].has_right_wall = False
                self._cells[col + 1][row].has_left_wall = False
            # left
            if next_index[0] == col - 1:
                self._cells[col][row].has_left_wall = False
                self._cells[col - 1][row].has_right_wall = False
            # up
            if next_index[1] == row + 1:
                self._cells[col][row].has_bottom_wall = False
                self._cells[col][row + 1].has_top_wall = False
            # down
            if next_index[1] == row - 1:
                self._cells[col][row].has_top_wall = False
                self._cells[col][row - 1].has_bottom_wall = False

            # recursively visit the next cell
            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    # returns True if this is the end cell, OR if it leads to the end cell.
    # returns False if this is a loser cell.
    def _solve_r(self, col, row):
        self._animate()

        current_cell = self._cells[col][row]

        # visit the current cell
        current_cell.visited = True

        # if we are at the end cell ,we are done!
        if col == self._num_cols - 1 and row == self._num_rows - 1:
            return True

        # move left if there is no wall and it hasn't been visited
        if (
            col > 0
            and not current_cell.has_left_wall
            and not self._cells[col - 1][row].visited
        ):
            current_cell.draw_move(self._cells[col - 1][row])
            if self._solve_r(col - 1, row):
                return True
            else:
                current_cell.draw_move(self._cells[col - 1][row], True)

        # move right if there is no wall and it hasn't been visited
        if (
            col < self._num_cols - 1
            and not current_cell.has_right_wall
            and not self._cells[col + 1][row].visited
        ):
            current_cell.draw_move(self._cells[col + 1][row])
            if self._solve_r(col + 1, row):
                return True
            else:
                current_cell.draw_move(self._cells[col + 1][row], True)

        # move up if there is no wall and it hasn't been visited
        if (
            row > 0
            and not current_cell.has_top_wall
            and not self._cells[col][row - 1].visited
        ):
            current_cell.draw_move(self._cells[col][row - 1])
            if self._solve_r(col, row - 1):
                return True
            else:
                current_cell.draw_move(self._cells[col][row - 1], True)

        # move down if there is no wall and it hasn't been visited
        if (
            row < self._num_rows - 1
            and not current_cell.has_bottom_wall
            and not self._cells[col][row + 1].visited
        ):
            current_cell.draw_move(self._cells[col][row + 1])
            if self._solve_r(col, row + 1):
                return True
            else:
                current_cell.draw_move(self._cells[col][row + 1], True)

        # we went the wrong way; let the previous cell know by returning Flase
        return False

    # create the move sfor the solution using a depth first search

    def solve(self):
        return self._solve_r(0, 0)
