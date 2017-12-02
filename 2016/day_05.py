import unittest
import hashlib
from collections import Iterator


''' --- Day 5: How About a Nice Game of Chess? ---

You are faced with a security door designed by Easter Bunny engineers that seem
to have acquired most of their security knowledge by watching hacking movies.

The eight-character password for the door is generated one character at a time
by finding the MD5 hash of some Door ID (your puzzle input) and an increasing
integer index (starting with 0).

A hash indicates the next character in the password if its hexadecimal
representation starts with five zeroes. If it does, the sixth character in the
hash is the next character of the password.

For example, if the Door ID is abc:

The first index which produces a hash that starts with five zeroes is 3231929,
which we find by hashing abc3231929; the sixth character of the hash, and thus
the first character of the password, is 1.
5017308 produces the next interesting hash, which starts with 000008f82..., so
        the second character of the password is 8.  The third time a hash
        starts with five zeroes is for abc5278568, discovering the character f.
        In this example, after continuing this search a total of eight times,
        the password is 18f47a30.

Given the actual Door ID, what is the password?

Your puzzle input is abbhdwsy.
'''


class Day5(unittest.TestCase):

    @unittest.SkipTest
    def test_example(self):
        g = pwd_generator('abc', 3231928)
        pwd = ''.join([next(g) for _ in range(8)])
        self.assertEqual('18f47a30', pwd)

    def test_solution(self):
        g = pwd_generator('abbhdwsy')
        pwd = ''.join([next(g) for _ in range(8)])
        self.assertEqual('801b56a7', pwd)

    @unittest.SkipTest
    def test_example_II(self):
        g = complex_pwd_generator('abc', 3231928)
        self.assertEqual((1, '5'), next(g))
        self.assertEqual((4, 'e'), next(g))
        self.assertEqual((7, '3'), next(g))
        self.assertEqual((3, 'c'), next(g))
        self.assertEqual((0, '0'), next(g))
        self.assertEqual((6, 'e'), next(g))
        self.assertEqual((7, 'b'), next(g))
        self.assertEqual((6, '6'), next(g))
        self.assertEqual((5, '8'), next(g))
        self.assertEqual((2, 'a'), next(g))

    def test_solution_II(self):
        g = complex_pwd_generator('abbhdwsy')
        sss = ['', '', '', '', '', '', '', '']
        while len(''.join(sss)) != 8:
            i, c = next(g)
            if sss[i] == '':
                sss[i] = c
        self.assertEqual('424a0197', ''.join(sss))


''' --- Part Two ---

As the door slides open, you are presented with a second door that uses a
slightly more inspired security mechanism. Clearly unimpressed by the last
version (in what movie is the password decrypted in order?!), the Easter Bunny
engineers have worked out a better solution.

Instead of simply filling in the password from left to right, the hash now also
indicates the position within the password to fill. You still look for hashes
that begin with five zeroes; however, now, the sixth character represents the
position (0-7), and the seventh character is the character to put in that
position.

A hash result of 000001f means that f is the second character in the password.
Use only the first result for each position, and ignore invalid positions.

For example, if the Door ID is abc:

The first interesting hash is from abc3231929, which produces 0000015...; so, 5
goes in position 1: _5______.  In the previous method, 5017308 produced an
interesting hash; however, it is ignored, because it specifies an invalid
position (8).  The second interesting hash is at index 5357525, which produces
000004e...; so, e goes in position 4: _5__e___.  You almost choke on your
popcorn as the final character falls into place, producing the password
05ace8e3.

Given the actual Door ID and this new method, what is the password? Be extra
proud of your solution if it uses a cinematic "decrypting" animation.

Your puzzle input is still abbhdwsy.
'''


class PwdHasher(Iterator):

    def __init__(self, door_id, start_index=None):
        self.door_id = door_id
        self.index = 0 if not start_index else start_index

    def next(self):
        while True:
            self.index += 1
            hasher = hashlib.md5()
            hasher.update(self.door_id)
            hasher.update(str(self.index))
            hd = hasher.hexdigest()
            if hd.startswith('00000'):
                return hd


def pwd_generator(door_id, start_index=None):
    g = PwdHasher(door_id, start_index)
    while True:
        n = next(g)
        yield n[5]


def complex_pwd_generator(door_id, start_index=None):
    g = PwdHasher(door_id, start_index)
    while True:
        candidate = next(g)
        if not candidate[5].isdigit():
            continue
        position = int(candidate[5])
        if position < 8:
            yield position, candidate[6]


if __name__ == '__main__':
    unittest.main()
