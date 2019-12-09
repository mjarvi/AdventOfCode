import unittest
from inputs import DAY_3_INPUT


'''
--- Day 3: Crossed Wires ---

The gravity assist was successful, and you're well on your way to the Venus
refuelling station. During the rush back on Earth, the fuel management system
wasn't completely installed, so that's next on the priority list.

Opening the front panel reveals a jumble of wires. Specifically, two wires are
connected to a central port and extend outward on a grid. You trace the path
each wire takes as it leaves the central port, one wire per line of text (your
puzzle input).

The wires twist and turn, but the two wires occasionally cross paths. To fix
the circuit, you need to find the intersection point closest to the central
port. Because the wires are on a grid, use the Manhattan distance for this
measurement. While the wires do technically cross right at the central port
where they both start, this point does not count, nor does a wire count as
crossing with itself.

For example, if the first wire's path is R8,U5,L5,D3, then starting from the
central port (o), it goes right 8, up 5, left 5, and finally down 3:

...........
...........
...........
....+----+.
....|....|.
....|....|.
....|....|.
.........|.
.o-------+.
...........

Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6, down 4,
and left 4:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........

These wires cross at two locations (marked X), but the lower-left one is closer
to the central port: its distance is 3 + 3 = 6.

Here are a few more examples:

    R75,D30,R83,U83,L12,D49,R71,U7,L72
    U62,R66,U55,R34,D71,R55,D58,R83 = distance 159
    R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
    U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135

What is the Manhattan distance from the central port to the closest
intersection?

--- Part Two ---

It turns out that this circuit is very timing-sensitive; you actually need to
minimize the signal delay.

To do this, calculate the number of steps each wire takes to reach each
intersection; choose the intersection where the sum of both wires' steps is
lowest. If a wire visits a position on the grid multiple times, use the steps
value from the first time it visits that position when calculating the total
value of a specific intersection.

The number of steps a wire takes is the total number of grid squares the wire
has entered to get to that location, including the intersection being
considered. Again consider the example from above:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........

In the above example, the intersection closest to the central port is reached
after 8+5+5+2 = 20 steps by the first wire and 7+6+4+3 = 20 steps by the second
wire for a total of 20+20 = 40 steps.

However, the top-right intersection is better: the first wire takes only 8+5+2
= 15 and the second wire takes only 7+6+2 = 15, a total of 15+15 = 30 steps.

Here are the best steps for the extra examples from above:

    R75,D30,R83,U83,L12,D49,R71,U7,L72
    U62,R66,U55,R34,D71,R55,D58,R83 = 610 steps
    R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
    U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = 410 steps

What is the fewest combined steps the wires must take to reach an intersection?

'''


def distance_to_closest_crossing(start, route_a, route_b):
    crossings = find_crossings(start, route_a, route_b)
    return min(manhattan_distance(start, pos) for pos in crossings)


def manhattan_distance(pos_a, pos_b):
    ax, ay = pos_a
    bx, by = pos_b
    return abs(ay - by) + abs(ax - bx)


def generate_route_points(start, steps):
    x, y = start
    for step in steps.split(','):
        direction = step[0]
        amount = int(step[1:])
        for n in range(amount):
            if direction == 'R':
                x += 1
            if direction == 'L':
                x -= 1
            if direction == 'D':
                y += 1
            if direction == 'U':
                y -= 1
            yield((x, y))


def steps_to_first_crossing(start, route_a, route_b):

    steps_a = {}
    for amount, position in enumerate(generate_route_points(start, route_a)):
        steps_a[position] = amount + 1

    steps_b = {}
    for amount, position in enumerate(generate_route_points(start, route_b)):
        steps_b[position] = amount + 1

    intersections = set(steps_a.keys()) & set(steps_b.keys()) 

    lenghts = [steps_a[p] + steps_b[p] for p in intersections]
    return min(lenghts)


def find_crossings(start, route_a, route_b):
    path_a = set(generate_route_points(start, route_a))
    path_b = set(generate_route_points(start, route_b))
    return [pos for pos in path_a if pos in path_b]


class TestDayTwo(unittest.TestCase):

    def test_manhattan_distance(self):
        self.assertEqual(6, manhattan_distance((8, 1), (5, 4)))
        self.assertEqual(8, manhattan_distance((9, 1), (5, 5)))

    def test_simple_example(self):
        self.assertEqual([(4, 1), (5, 1), (6, 1)], route_points((3, 1), "R3"))
        self.assertEqual([(1, 2), (1, 3), (1, 4), (1, 5)], route_points((1, 1), "D4"))

    def test_simple_example(self):
        self.assertEqual([(7, 3), (4, 5)],
                         find_crossings((1, 8), "R8,U5,L5,D3", "U7,R6,D4,L4"))

    def test_examples(self):
        self.assertEqual(
            159,
            distance_to_closest_crossing(
                (1, 8), 
                "R75,D30,R83,U83,L12,D49,R71,U7,L72",
                "U62,R66,U55,R34,D71,R55,D58,R83"))

        self.assertEqual(
            135,
            distance_to_closest_crossing(
                (1, 8), 
                "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
                "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"))

    def test_solution(self):
        route_a, route_b = DAY_3_INPUT.splitlines()
        self.assertEqual(
            5319,
            distance_to_closest_crossing((1, 8), route_a, route_b))

    def test_examples_2(self):
        self.assertEqual(30, steps_to_first_crossing((1, 8), "R8,U5,L5,D3", "U7,R6,D4,L4"))
        self.assertEqual(610, steps_to_first_crossing((1, 8), "R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"))
        self.assertEqual(410, steps_to_first_crossing((1, 8), "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"))

    def test_solution_2(self):
        route_a, route_b = DAY_3_INPUT.splitlines()
        self.assertEqual(122514, steps_to_first_crossing((1, 8), route_a, route_b))


if __name__ == '__main__':
    unittest.main()
