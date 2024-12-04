from geometry import *
import time
import random

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
        if seed is not None:
            random.seed(seed)

        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        self._cells = []

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
    
    def _create_cells(self):
        for i in range(self._num_cols):
            self._cells.append([])
            for j in range(self._num_rows):
                self._cells[i].append(Cell(self._win))
                self._draw_cell(i, j, 0.0005)

    def _draw_cell(self, i, j, wait_time = 0.005):
        if self._win is None:
            return

        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y

        self._cells[i][j].draw(x1, y1, x2, y2)

        self._animate(wait_time)
    
    def _animate(self, wait_time = 0.05):
        self._win.redraw()
        time.sleep(wait_time)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(0, 0)
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        cell = self._cells[i][j]
        cell.visited = True

        while True:
            to_visit = []

            if i > 0 and not self._cells[i - 1][j].visited:
                to_visit.append(((i - 1, j), "left"))
            if j > 0 and not self._cells[i][j - 1].visited:
                to_visit.append(((i, j - 1), "top"))
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                to_visit.append(((i + 1, j), "right"))
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                to_visit.append(((i, j + 1), "bottom"))

            if len(to_visit) == 0:
                break

            next_cell_info = random.choice(to_visit)
            next_cell = self._cells[next_cell_info[0][0]][next_cell_info[0][1]]

            if next_cell_info[1] == "left":
                cell.has_left_wall = False
                next_cell.has_right_wall = False
            if next_cell_info[1] == "right":
                cell.has_right_wall = False
                next_cell.has_left_wall = False
            if next_cell_info[1] == "top":
                cell.has_top_wall = False
                next_cell.has_bottom_wall = False
            if next_cell_info[1] == "bottom":
                cell.has_bottom_wall = False
                next_cell.has_top_wall = False

            self._draw_cell(i, j)
            self._draw_cell(next_cell_info[0][0], next_cell_info[0][1])

            self._break_walls_r(next_cell_info[0][0], next_cell_info[0][1])

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        cell = self._cells[i][j]
        cell.visited = True

        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        
        to_visit = []
        if i > 0 and not self._cells[i - 1][j].visited and not cell.has_left_wall:
            to_visit.append((i - 1, j))
        if j > 0 and not self._cells[i][j - 1].visited and not cell.has_top_wall:
            to_visit.append((i, j - 1))
        if i < self._num_cols - 1 and not self._cells[i + 1][j].visited and not cell.has_right_wall:
            to_visit.append((i + 1, j))
        if j < self._num_rows - 1 and not self._cells[i][j + 1].visited and not cell.has_bottom_wall:
            to_visit.append((i, j + 1))

        for next_cell_info in to_visit:
            next_cell = self._cells[next_cell_info[0]][next_cell_info[1]]

            cell.draw_move(next_cell)
            self._animate()

            result = self._solve_r(next_cell_info[0], next_cell_info[1])
            if result:
                return True
            
            cell.draw_move(next_cell, True)
            self._animate()

        return False
            