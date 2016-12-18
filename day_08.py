import unittest
import re
from mock import patch
from mock import call
from input_day_08 import data

'''
--- Day 8: Two-Factor Authentication ---

You come across a door implementing what you can only assume is an
implementation of two-factor authentication after a long game of requirements
telephone.

To get past the door, you first swipe a keycard (no problem; there was one on a
nearby desk). Then, it displays a code on a little screen, and you type that
code on a keypad. Then, presumably, the door unlocks.

Unfortunately, the screen has been smashed. After a few minutes, you've taken
everything apart and figured out how it works. Now you just have to work out
what the screen would have displayed.

The magnetic strip on the card you swiped encodes a series of instructions for
the screen; these instructions are your puzzle input. The screen is 50 pixels
wide and 6 pixels tall, all of which start off, and is capable of three
somewhat peculiar operations:

rect AxB turns on all of the pixels in a rectangle at the top-left of the
screen which is A wide and B tall.  rotate row y=A by B shifts all of the
pixels in row A (0 is the top row) right by B pixels. Pixels that would fall
off the right end appear at the left end of the row.
rotate column x=A by B shifts all of the pixels in column A (0 is the left
column) down by B pixels. Pixels that would fall off the bottom appear at the
top of the column.  For example, here is a simple sequence on a smaller screen:

rect 3x2 creates a small rectangle in the top-left corner:

###....
###....
.......
rotate column x=1 by 1 rotates the second column down by one pixel:

#.#....
###....
.#.....
rotate row y=0 by 4 rotates the top row right by four pixels:

....#.#
###....
.#.....
rotate column x=1 by 1 again rotates the second column down by one pixel,
causing the bottom pixel to wrap back to the top:

.#..#.#
#.#....
.#.....
As you can see, this display technology is extremely powerful, and will soon
dominate the tiny-code-displaying-screen market. That's what the advertisement
on the back of the display tries to convince you, anyway.

There seems to be an intermediate check of the voltage used by the display:
after you swipe your card, if the screen did work, how many pixels should be
lit?  '''


class Day8(unittest.TestCase):

    def setUp(self):
        self.d = Display(7, 3)

    def test_is_empty_in_the_beginning(self):
        self.assertEqual('''\
.......
.......
.......''', self.d.get())

    def test_examples(self):
        #  rect 3x2 creates a small rectangle in the top-left corner:
        self.d.rect(3, 2)
        self.assertEqual('''\
###....
###....
.......''', self.d.get())

        #  rotate column x=1 by 1 rotates the second column down by one pixel:
        self.d.rotate(x=1, n=1)
        self.assertEqual('''\
#.#....
###....
.#.....''', self.d.get())

        #  rotate row y=0 by 4 rotates the top row right by four pixels:
        self.d.rotate(y=0, n=4)
        self.assertEqual('''\
....#.#
###....
.#.....''', self.d.get())

        #  rotate column x=1 by 1 again rotates the second column down by one
        #  pixel, causing the bottom pixel to wrap back to the top:
        self.d.rotate(x=1, n=1)
        self.assertEqual('''\
.#..#.#
#.#....
.#.....''', self.d.get())

    @patch('day_08.Display.rect')
    def test_parse_command_rect(self, rect_mock):
        self.d.execute('rect 1x1')
        self.assertEqual([call(1, 1)], rect_mock.mock_calls)

    @patch('day_08.Display.rotate_x')
    def test_parse_command_rotate_x(self, rect_mock):
        self.d.execute('rotate column x=13 by 1')
        self.assertEqual([call(13, 1)], rect_mock.mock_calls)

    @patch('day_08.Display.rotate_y')
    def test_parse_command_rotate_y(self, rect_mock):
        self.d.execute('rotate row y=23 by 31')
        self.assertEqual([call(23, 31)], rect_mock.mock_calls)

    def test_sum(self):
        r = Display(20, 4)
        r.rect(10, 2)
        self.assertEqual(20, sum([c == '#' for c in r.get()]))

    def test_solution(self):
        r = Display(50, 6)
        for cmd in data.splitlines():
            r.execute(cmd)
        self.assertEqual(124, r.sum_lit_pixels())
        self.assertEqual('''\
#.#####.############.....#########.#.#############
..##.##..#.####.####....############.##..#.#..####
##....###..#.#..##..####..###.####..#.##.#.#.#...#
..###....#......#....#........#.#...#....#..#.###.
..###...........................#......#.......#..
..#...............#.............................#.''', r.get())


class Display(object):

    def __init__(self, w, h):
        self._width = w
        self._height = h
        self.pixel = []
        for y in range(h):
            self.pixel.append(['.' for _ in range(w)])

    def execute(self, command):
        if command.startswith('rect'):
            self.parse_rect(command)
        if command.startswith('rotate row'):
            self.parse_rotate_y(command)
        if command.startswith('rotate column'):
            self.parse_rotate_x(command)

    def parse_rect(self, command):
            dim = re.split(r'^rect (\d+)x(\d+).*$', command)
            self.rect(int(dim[1]), int(dim[2]))

    def parse_rotate_y(self, command):
            dim = re.split(r'rotate row y=(\d+) by (\d+).*$', command)
            self.rotate_y(int(dim[1]), int(dim[2]))

    def parse_rotate_x(self, command):
            dim = re.split(r'rotate column x=(\d+) by (\d+).*$', command)
            self.rotate_x(int(dim[1]), int(dim[2]))

    def get(self):
        return '\n'.join([''.join(row) for row in self.pixel])

    def rect(self, w, h):
        for y in range(h):
            for x in range(w):
                self.pixel[y][x] = '#'

    def rotate(self, x=None, y=None, n=0):
        if x is not None:
            self.rotate_x(x, n)
        if y is not None:
            self.rotate_y(y, n)

    def rotate_x(self, x, n):
        start = self._height - 1
        wrap_pixel = self.pixel[start][x]
        for y in range(start, 0, -1):
            self.pixel[y][x] = self.pixel[y - 1][x]
        self.pixel[0][1] = wrap_pixel

    def rotate_y(self, y, n):
        self.pixel[y] = self.pixel[y][n - 1:] + self.pixel[y][:n - 1]

    def foo(self):
        return self.baa()

    def baa(self):
        return 42

    def sum_lit_pixels(self):
        return sum([c == '#' for c in self.get()])


if __name__ == '__main__':
    unittest.main()
