import unittest
from input_day_03 import data


''' --- Day 3: Squares With Three Sides ---

Now that you can think clearly, you move deeper into the labyrinth of hallways
and office furniture that makes up this part of Easter Bunny HQ. This must be a
graphic design department; the walls are covered in specifications for
triangles.

Or are they?

The design document gives the side lengths of each triangle it describes,
but... 5 10 25? Some of these aren't triangles. You can't help but mark the
impossible ones.

In a valid triangle, the sum of any two sides must be larger than the remaining
side. For example, the "triangle" given above is impossible, because 5 + 10 is
not larger than 25.

In your puzzle input, how many of the listed triangles are possible?

--- Part Two ---

Now that you've helpfully marked up their design documents, it occurs to you
that triangles are specified in groups of three vertically. Each set of three
numbers in a column specifies a triangle. Rows are unrelated.

For example, given the following specification, numbers with the same hundreds
digit would be part of the same triangle:

101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603

In your puzzle input, and instead reading by columns, how many of the listed
triangles are possible?

'''


class TestTriangles(unittest.TestCase):

    def test_first_solution(self):
        self.assertEqual(982, sum([is_triangle(k) for k in data]))

    def test_second_example(self):

        circles = 0
        numbers = [[101, 301, 501],
                   [102, 302, 502],
                   [103, 303, 503],
                   [201, 401, 601],
                   [202, 402, 602],
                   [203, 403, 603]]

        t = triples(numbers)
        self.assertEqual(next(t), [101, 102, 103])
        self.assertEqual(next(t), [301, 302, 303])
        self.assertEqual(next(t), [501, 502, 503])
        self.assertEqual(next(t), [201, 202, 203])
        self.assertEqual(next(t), [401, 402, 403])
        self.assertEqual(next(t), [601, 602, 603])

        for k in triples(numbers):
            if is_triangle(k):
                circles = circles + 1

        self.assertEqual(circles, 6)

    def test_part_two_solution(self):
        circles = 0
        for k in triples(data):
            if is_triangle(k):
                circles = circles + 1
        self.assertEqual(circles, 1826)


def is_triangle(k):
    n1, n2, n3 = sorted(k)
    return n1 + n2 > n3


def triples(k):
    i = iter(k)
    for _ in range(len(k)):
        a1, b1, c1 = next(i)
        a2, b2, c2 = next(i)
        a3, b3, c3 = next(i)
        yield sorted([a1, a2, a3])
        yield sorted([b1, b2, b3])
        yield sorted([c1, c2, c3])


if __name__ == "__main__":
    unittest.main()
