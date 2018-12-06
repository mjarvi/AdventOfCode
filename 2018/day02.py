#!/usr/bin/python3
import unittest
from inputs import DAY2_INPUT


'''

Inventory Management System

    You stop falling through time, catch your breath, and check the screen on the
    device. "Destination reached. Current Year: 1518. Current Location: North Pole
    Utility Closet 83N10." You made it! Now, to find those anomalies.

    Outside the utility closet, you hear footsteps and a voice. "...I'm not sure
    either. But now that so many people have chimneys, maybe he could sneak in that
    way?" Another voice responds, "Actually, we've been working on a new kind of
    suit that would let him fit through tight spaces like that. But, I heard that
    a few days ago, they lost the prototype fabric, the design plans, everything!
    Nobody on the team can even seem to remember important details of the project!"

    "Wouldn't they have had enough fabric to fill several boxes in the warehouse?
    They'd be stored together, so the box IDs should be similar. Too bad it would
    take forever to search the warehouse for two similar box IDs..." They walk too
    far away to hear any more.

    Late at night, you sneak to the warehouse - who knows what kinds of paradoxes
    you could cause if you were discovered - and use your fancy wrist device to
    quickly scan every box and produce a list of the likely candidates (your puzzle
    input).

    To make sure you didn't miss any, you scan the likely candidate boxes again,
    counting the number that have an ID containing exactly two of any letter and
    then separately counting those with exactly three of any letter. You can
    multiply those two counts together to get a rudimentary checksum and compare it
    to what your device predicts.

    For example, if you see the following box IDs:

        abcdef contains no letters that appear exactly two or three times.
        bababc contains two a and three b, so it counts for both.
        abbcde contains two b, but no letter appears exactly three times.
        abcccd contains three c, but no letter appears exactly two times.
        aabcdd contains two a and two d, but it only counts once.
        abcdee contains two e.
        ababab contains three a and three b, but it only counts once.

    Of these box IDs, four of them contain a letter which appears exactly
    twice, and three of them contain a letter which appears exactly three
    times. Multiplying these together produces a checksum of 4 * 3 = 12.

    What is the checksum for your list of box IDs?

    --- Part Two ---

    Confident that your list of box IDs is complete, you're ready to find the boxes
    full of prototype fabric.

    The boxes will have IDs which differ by exactly one character at the same
    position in both strings. For example, given the following box IDs:

        abcde
        fghij
        klmno
        pqrst
        fguij
        axcye
        wvxyz

    The IDs abcde and axcye are close, but they differ by two characters (the
    second and fourth). However, the IDs fghij and fguij differ by exactly one
    character, the third (h and u). Those must be the correct boxes.

    What letters are common between the two correct box IDs? (In the example above,
    this is found by removing the differing character from either ID, producing
    fgij.)

'''


class ID(object):

    def __init__(self, string):
        self.char_by_amount = {}
        for c in string:
            if c not in self.char_by_amount:
                self.char_by_amount[c] = 0
            self.char_by_amount[c] += 1

    def get_first_letter_with_n_occurences(self, amount):
        for l, n in self.char_by_amount.items():
            if n == amount:
                return l
        return ''

    def duples(self):
        return self.get_first_letter_with_n_occurences(2)

    def triples(self):
        return self.get_first_letter_with_n_occurences(3)


def checksum(ids):
    duples = 0
    triples = 0
    for id in ids:
        duples += 1 if id.duples() else 0
        triples += 1 if id.triples() else 0
    return duples * triples


def find_only_common_letters(ids):

    def common_part(string_a, string_b):
        common = ''
        for char, other in zip(string_a, string_b):
            if char == other:
                common += char
        return common

    for string_a in ids:
        for string_b in ids:
            if string_a == string_b:
                continue
            sub_string = common_part(string_a, string_b)
            if len(string_a) - len(sub_string) <= 1:
                return sub_string
    return None


class TestDay02(unittest.TestCase):

    def test_example1(self):
        self.assertEqual(ID('abcdef').duples(), '')
        self.assertEqual(ID('bababc').duples(), 'a')
        self.assertEqual(ID('abbcde').duples(), 'b')
        self.assertEqual(ID('abcccd').duples(), '')
        self.assertEqual(ID('aabcdd').duples(), 'a')
        self.assertEqual(ID('abcdee').duples(), 'e')
        self.assertEqual(ID('ababab').duples(), '')
        self.assertEqual(ID('abcdef').triples(), '')
        self.assertEqual(ID('bababc').triples(), 'b')
        self.assertEqual(ID('abbcde').triples(), '')
        self.assertEqual(ID('abcccd').triples(), 'c')
        self.assertEqual(ID('aabcdd').triples(), '')
        self.assertEqual(ID('abcdee').triples(), '')
        self.assertEqual(ID('ababab').triples(), 'a')

    def test_example2(self):
        ids = [ID('abcdef'), ID('bababc'), ID('abbcde'), ID('abcccd'),
               ID('aabcdd'), ID('abcdee'), ID('ababab')]
        self.assertEqual(checksum(ids), 12)

    def test_solution_1(self):
        ids = [ID(string) for string in DAY2_INPUT.split(' ')]
        self.assertEqual(checksum(ids), 8820)

    def test_example3(self):
        ids = ['abcde', 'fghij', 'klmno', 'pqrst', 'fguij', 'axcye', 'wvxyz']
        self.assertEqual(find_only_common_letters(ids), 'fgij')

    def test_solution_2(self):
        ids = [string for string in DAY2_INPUT.split(' ')]
        self.assertEqual(find_only_common_letters(ids), 'bpacnmglhizqygfsjixtkwudr')


if __name__ == '__main__':
    unittest.main()
