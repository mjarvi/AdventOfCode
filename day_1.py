import unittest


THE_ROUTE = 'R5, R4, R2, L3, R1, R1, L4, L5, R3, L1, L1, R4, L2, R1, R4, R4, L2, L2, R4, L4, R1, R3, L3, L1, L2, R1, R5, L5, L1, L1, R3, R5, L1, R4, L5, R5, R1, L185, R4, L1, R51, R3, L2, R78, R1, L4, R188, R1, L5, R5, R2, R3, L5, R3, R4, L1, R2, R2, L4, L4, L5, R5, R4, L4, R2, L5, R2, L1, L4, R4, L4, R2, L3, L4, R2, L3, R3, R2, L2, L3, R4, R3, R1, L4, L2, L5, R4, R4, L1, R1, L5, L1, R3, R1, L2, R1, R1, R3, L4, L1, L3, R2, R4, R2, L2, R1, L5, R3, L3, R3, L1, R4, L3, L3, R4, L2, L1, L3, R2, R3, L2, L1, R4, L3, L5, L2, L4, R1, L4, L4, R3, R5, L4, L1, L1, R4, L2, R5, R1, R1, R2, R1, R5, L1, L3, L5, R2'
NORTH = 0
EAST = 90
SOUTH = 180
WEST = 270


class Integer(object):

    def __init__(self, value):
        self.value = value


class You(object):

    directions = [NORTH, EAST, SOUTH, WEST]

    def __init__(self):
        self._heading = NORTH
        self.x = Integer(0)
        self.y = Integer(0)
        self.visited = []
        self.visited_more_than_twice = []

    def walk(self, command):
        heading, distance = self.split(command)
        self.turn(heading)
        self.go(distance)

    def split(self, command):
        return command[0], int(command[1:])

    def turn(self, direction):
        current = self.directions.index(self._heading)
        next_index = (current + {'R': 1, 'L': -1}[direction]) % len(self.directions)
        self._heading = self.directions[next_index]

    def go(self, distance):
        v, n = {NORTH: (self.y, +1),
                EAST:  (self.x, +1),
                SOUTH: (self.y, -1),
                WEST:  (self.x, -1)}[self._heading]

        for _ in range(distance):
            v.value += n
            self.track(self.get_position())

    def track(self,  position):
        if position in self.visited:
            self.visited_more_than_twice.append(position)
        self.visited.append(position)

    def get_position(self):
        return self.x.value, self.y.value

    def get_distance(self, position=None):
        x, y = position if position else self.get_position()
        return abs(x) + abs(y)

    def travel(self, instructions):
        for step in instructions.split(','):
            self.walk(step.strip())


class TestYou(unittest.TestCase):

    def setUp(self):
        self.i = You()

    def test_i_start_from_origo(self):
        self.assertEqual(You().get_position(), (0, 0))

    def test_two_steps_right_is_two_blocks_away(self):
        self.i.walk('R2')
        self.assertEqual(self.i.get_position(), (2, 0))
        self.assertEqual(self.i.get_distance(), 2)

    def test_init_towards_north(self):
        self.assertEqual(self.i._heading, NORTH)

    def test_turn_left_from_north_is_west(self):
        self.i.turn('L')
        self.assertEqual(i._heading, WEST)

    def test_two_right_turns_and_one_left_is_east(self):
        self.i.walk('R1')
        self.i.walk('R1')
        self.i.walk('L1')
        self.assertEqual(seelf.i._heading, EAST)

    def test_two_steps_right_and_one_left_is_three_blocks_away(self):
        self.i.walk('R2')
        self.i.walk('L1')
        self.assertEqual(seelf.i.get_position(), (2, 1))
        self.assertEqual(seelf.i.get_distance(), 3)

    def test_route(self):
        self.i.travel('L5, R2, L3, L1, R1, R1')
        self.assertEqual(i.get_position(), (-9, 2))

    def test_first_twice_visited(self):
        self.i.travel('R8, R4, R4, R8')
        self.assertEqual(i.visited_more_than_twice[0], (4, 0))

    def test_solution(self):
        self.i.travel(THE_ROUTE)
        self.assertEqual(i.get_distance(), 231)
        self.assertEqual(i.get_distance(i.visited_more_than_twice[0]), 147)


unittest.main()
