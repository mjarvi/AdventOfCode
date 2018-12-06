#!/usr/bin/python3
import unittest
import re
from inputs import DAY3_INPUT


'''

No Matter How You Slice It

    The Elves managed to locate the chimney-squeeze prototype fabric for Santa's
    suit (thanks to someone who helpfully wrote its box IDs on the wall of the
    warehouse in the middle of the night). Unfortunately, anomalies are still
    affecting them - nobody can even agree on how to cut the fabric.

    The whole piece of fabric they're working on is a very large square - at least
    1000 inches on each side.

    Each Elf has made a claim about which area of fabric would be ideal for Santa's
    suit. All claims have an ID and consist of a single rectangle with edges
    parallel to the edges of the fabric. Each claim's rectangle is defined as
    follows:

     - The number of inches between the left edge of the fabric and the left
       edge of the rectangle.
     - The number of inches between the top edge of the fabric and the top edge
       of the rectangle.
     - The width of the rectangle in inches.
     - The height of the rectangle in inches.

    A claim like #123 @ 3,2: 5x4 means that claim ID 123 specifies a rectangle 3
    inches from the left edge, 2 inches from the top edge, 5 inches wide, and 4
    inches tall. Visually, it claims the square inches of fabric represented by #
    (and ignores the square inches of fabric represented by .) in the diagram
    below:

    ...........
    ...........
    ...#####...
    ...#####...
    ...#####...
    ...#####...
    ...........
    ...........
    ...........

    The problem is that many of the claims overlap, causing two or more claims to
    cover part of the same areas. For example, consider the following claims:

    #1 @ 1,3: 4x4
    #2 @ 3,1: 4x4
    #3 @ 5,5: 2x2

    Visually, these claim the following areas:

    ........
    ...2222.
    ...2222.
    .11XX22.
    .11XX22.
    .111133.
    .111133.
    ........

    The four square inches marked with X are claimed by both 1 and 2. (Claim 3,
    while adjacent to the others, does not overlap either of them.)

    If the Elves all proceed with their own plans, none of them will have enough
    fabric. How many square inches of fabric are within two or more claims?
'''


EXAMPLE_CLAIMS = '''\
    #1 @ 1,3: 4x4
    #2 @ 3,1: 4x4
    #3 @ 5,5: 2x2
'''


def parse(string):
    m = re.match(r"#(\d+)\s@\s(\d+),(\d+):\s(\d+)x(\d+)", string.strip())
    return tuple(int(n) for n in m.groups())


class Claim():

    def __init__(self, number, x, y, width, height):
        self.number = number
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_x = x + width
        self.max_y = y + height


class Fabric():

    def __init__(self, claim_list):

        def populate(chart, claims):
            for c in claims:
                for y in range(c.y, c.max_y):
                    for x in range(c.x, c.max_x):
                        if chart[y][x] == '.':
                            chart[y][x] = str(c.number)
                        else:
                            chart[y][x] = 'X'

        claims = tuple(Claim(*parse(values)) for values in claim_list.splitlines())
        self.width, self.height = self.find_limits(claims)
        self.chart = [['.' for _ in range(self.width)] for _ in range(self.height)]
        populate(self.chart, claims)

    @property
    def size(self):
        return (self.width, self.height)

    def find_limits(self, claims):
        width = 0
        height = 0
        for m in claims:
            width = max(width, m.max_x)
            height = max(height, m.max_y)
        return width, height

    def get_overlap(self):
        overlap = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.chart[y][x] == 'X':
                    overlap += 1
        return overlap


class TestDay02(unittest.TestCase):

    def test_claim_knows_max_values(self):
        c = Claim(1, 2, 3, 4, 5)
        self.assertEqual(c.max_x, 6)
        self.assertEqual(c.max_y, 8)

    def test_parse_claim(self):
        self.assertEqual(parse('#1 @ 2,3: 4x5'), (1, 2, 3, 4, 5))

    def test_find_chart_max_size(self):
        f = Fabric(EXAMPLE_CLAIMS)
        self.assertEqual(f.size, (7, 7))

    def test_example1(self):
        f = Fabric(EXAMPLE_CLAIMS)
        self.assertEqual(f.get_overlap(), 4)

    def test_solution_1(self):
        f = Fabric(DAY3_INPUT)
        self.assertEqual(f.get_overlap(), 110827)

    def test_solution_2(self):
        pass


if __name__ == '__main__':
    unittest.main()
