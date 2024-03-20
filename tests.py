import unittest

from maze import Maze
from graphics import Window


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows
        )

    def test_maze_create_cells_large(self):
        num_cols = 16
        num_rows = 12
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_entrance_and_exit_walls(self):
        num_cols = 16
        num_rows = 12
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        entrance = m1._cells[0][0]
        exit = m1._cells[num_cols - 1][num_rows - 1]
        # ^ XOR not both:
        self.assertTrue((not entrance.has_top_wall) ^
                        (not entrance.has_left_wall))
        self.assertTrue((not exit.has_bottom_wall) ^
                        (not exit.has_right_wall))


if __name__ == "__main__":
    unittest.main()
