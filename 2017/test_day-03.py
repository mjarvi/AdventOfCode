import unittest
from math import fabs
from math import ceil
from math import pow
from math import sqrt
from math import floor


'''
--- Day 3: Spiral Memory ---

You come across an experimental new kind of memory stored on an infinite
two-dimensional grid.

Each square on the grid is allocated in a spiral pattern starting at a location
marked 1 and then counting up while spiraling outward. For example, the first
few squares are allocated like this:

17  16  15  14  13    2..9
18   5   4   3  12
19   6   1   2  11
20   7   8   9  10
21  22  23---> ...

While this is very space-efficient (no squares are skipped), requested data
must be carried back to square 1 (the location of the only access port for this
memory system) by programs that can only move up, down, left, or right. They
always take the shortest path: the Manhattan Distance between the location of
the data and square 1.

For example:

Data from square 1 is carried 0 steps, since it's at the access port.
Data from square 12 is carried 3 steps, such as: down, left, left.
Data from square 23 is carried only 2 steps: up twice.
Data from square 1024 must be carried 31 steps.

How many steps are required to carry the data from the square identified in
your puzzle input all the way to the access port?

Your puzzle input is 265149.


--- Part Two ---

As a stress test on the system, the programs here clear the grid and then store
the value 1 in square 1. Then, in the same allocation order as shown above,
they store the sum of the values in all adjacent squares, including diagonals.

So, the first few squares' values are chosen as follows:

    Square 1 starts with the value 1.

    Square 2 has only one adjacent filled square (with value 1), so it also
    stores 1.

    Square 3 has both of the above squares as neighbors and stores the sum of
    their values, 2.

    Square 4 has all three of the aforementioned squares as neighbors and
    stores the sum of their values, 4.

    Square 5 only has the first and fourth squares as neighbors, so it gets the
    value 5.

Once a square is written, its value does not change. Therefore, the first few
squares would receive the following values:

    147  142  133  122   59
    304    5    4    2   57
    330   10    1    1   54
    351   11   23   25   26
    362  747  806--->   ...

What is the first value written that is larger than your puzzle input?

'''


def steps_from(val, grid):
    for row_index, row in enumerate(grid):
        if val in row:
            return int(fabs(int(len(row) / 2) - row.index(val))) + \
                   int(fabs(int(len(row) / 2) - row_index))


def steps(loops):
    n = -1
    for n in range(1, (loops * 2) - 1, 2):
        yield n, n + 1, n + 1,  n + 2
    yield n + 2, n + 3, n + 3,  n + 3


def add_one_if_even(value):
    return value + (0 if value & 1 else 1)


def get_spiral_parameters(area):
    side = int(ceil(sqrt(area)))
    largest_value = pow(side, 2)
    side = add_one_if_even(side)
    loops = int(floor(side / 2))
    grid = [[0 for n in range(side)] for m in range(side)]
    return largest_value, side, loops, grid


def build_grid_I(area):

    current_value = 0

    def get_next_value(y, x, grid, side):
        nonlocal current_value
        current_value += 1
        return current_value

    return fill_grid(area, get_next_value)


def build_grid_II(area):

    solution = None

    def calc_value(y, x, grid, side):
        nonlocal solution
        val = 0
        for j in range(-1, 2):
            for i in range(-1, 2):
                if y + i < 0 or side <= y + i or x + j < 0 or side <= x + j:
                    continue
                val += grid[y + i][x + j]
        if solution is None and val > area:
            solution = val
        return 1 if val == 0 else val

    return fill_grid(area, calc_value), solution


def fill_grid(area, calc_value):

    largest_value, side, loops, grid = get_spiral_parameters(area)
    x = y = loops

    grid[y][x] = calc_value(y, x, grid, side)
    x += 1
    grid[y][x] = calc_value(y, x, grid, side)

    for up, left, down, right in steps(loops):

        for _ in range(up):
            y -= 1
            grid[y][x] = calc_value(y, x, grid, side)

        for _ in range(left):
            x -= 1
            grid[y][x] = calc_value(y, x, grid, side)

        for _ in range(down):
            y += 1
            grid[y][x] = calc_value(y, x, grid, side)

        for _ in range(right):
            x += 1
            grid[y][x] = calc_value(y, x, grid, side)

    return grid


class TestDayThree(unittest.TestCase):

    def test_examples_9grid(self):
        self.assertEqual(build_grid_I(9), [[5, 4, 3],
                                           [6, 1, 2],
                                           [7, 8, 9]])

    def test_examples_25grid(self):
        self.assertEqual(build_grid_I(25), [[17, 16, 15, 14, 13],
                                            [18,  5,  4,  3, 12],
                                            [19,  6,  1,  2, 11],
                                            [20,  7,  8,  9, 10],
                                            [21, 22, 23, 24, 25]])

    def test_examples_49grid(self):
        self.assertEqual(build_grid_I(49), [[37, 36, 35, 34, 33, 32, 31],
                                            [38, 17, 16, 15, 14, 13, 30],
                                            [39, 18,  5,  4,  3, 12, 29],
                                            [40, 19,  6,  1,  2, 11, 28],
                                            [41, 20,  7,  8,  9, 10, 27],
                                            [42, 21, 22, 23, 24, 25, 26],
                                            [43, 44, 45, 46, 47, 48, 49]])

    def test_steps_for_9grid(self):
        n = steps(1)
        self.assertEqual((1, 2, 2, 2), next(n))

    def test_steps_for_25grid(self):
        n = steps(2)
        self.assertEqual((1, 2, 2, 3), next(n))
        self.assertEqual((3, 4, 4, 4), next(n))

    def test_steps_for_49grid(self):
        n = steps(3)
        self.assertEqual((1, 2, 2, 3), next(n))
        self.assertEqual((3, 4, 4, 5), next(n))
        self.assertEqual((5, 6, 6, 6), next(n))

    def test_distances(self):
        grid = build_grid_I(49)
        self.assertEqual(steps_from(1, grid), 0)
        self.assertEqual(steps_from(12, grid), 3)
        self.assertEqual(steps_from(23, grid), 2)
        self.assertEqual(steps_from(149, build_grid_I(149)), 8)
        self.assertEqual(steps_from(1024, build_grid_I(1024)), 31)

    def test_solution_I(self):
        self.assertEqual(438, steps_from(265149, build_grid_I(265149)))

    def test_example_II(self):
        grid, value = build_grid_II(25)
        self.assertEqual(grid, [[147, 142, 133, 122,  59],
                                [304,   5,   4,   2,  57],
                                [330,  10,   1,   1,  54],
                                [351,  11,  23,  25,  26],
                                [362, 747, 806, 880, 931]])
        self.assertEqual(value, 26)

    def test_solution_II(self):
        _, value = build_grid_II(265149)
        self.assertEqual(266330, value)
