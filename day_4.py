import unittest
import re
import collections
import string
from day_4_input import data


''' --- Day 4: Security Through Obscurity ---

Finally, you come across an information kiosk with a list of rooms. Of course,
the list is encrypted and full of decoy data, but the instructions to decode
the list are barely hidden nearby. Better remove the decoy data first.

Each room consists of an encrypted name (lowercase letters separated by dashes)
followed by a dash, a sector ID, and a checksum in square brackets.

A room is real (not a decoy) if the checksum is the five most common letters in
the encrypted name, in order, with ties broken by alphabetization. For example:

    aaaaa-bbb-z-y-x-123[abxyz] is a real room because the most common letters
    are a (5), b (3), and then a tie between x, y, and z, which are listed
    alphabetically.  a-b-c-d-e-f-g-h-987[abcde] is a real room because although
    the letters are all tied (1 of each), the first five are listed
    alphabetically.  not-a-real-room-404[oarel] is a real room.
    totally-real-room-200[decoy] is not.  Of the real rooms from the list
    above, the sum of their sector IDs is 1514.

    What is the sum of the sector IDs of the real rooms?

'''


class Day4first(unittest.TestCase):

    def test_example(self):
        self.assertEqual(True, is_real_room('aaaaa-bbb-z-y-x', 'abxyz'))
        self.assertEqual(True, is_real_room('a-b-c-d-e-f-g-h', 'abcde'))
        self.assertEqual(True, is_real_room('not-a-real-room', 'oarel'))
        self.assertEqual(False, is_real_room('totally-real-room', 'decoy'))
        self.assertEqual(1514, sum_sectors_of_real(['aaaaa-bbb-z-y-x-123[abxyz]',
                                                    'a-b-c-d-e-f-g-h-987[abcde]',
                                                    'not-a-real-room-404[oarel]',
                                                    'totally-real-room-200[decoy]']))

    def test_letters_with_same_amounts_are_listed_alphabethically(self):
        self.assertEqual(get_five_first_most_common_letters('aacdccbbabfe'), 'abcde')

    def test_split_name(self):
        self.assertEqual(('aaaaa-bbb-z-y-x', 123, 'abxyz'),
                         split_name_string('aaaaa-bbb-z-y-x-123[abxyz]'))

    def test_most_common_letters(self):
        self.assertEqual('abcde', get_five_first_most_common_letters('aabb-ccd-deef-fg'))

    def test_is_real_room(self):
        self.assertTrue(is_real_room('aaaaa-bbb-z-y-x', 'abxyz'))

    def test_is_not_real_room(self):
        self.assertFalse(is_real_room('totally-real-room', 'decoy'))

    def test_solution(self):
        self.assertEqual(409147, sum_sectors_of_real(data.splitlines()))


''' --- Part Two ---

With all the decoy data out of the way, it's time to decrypt this list and get
moving.

The room names are encrypted by a state-of-the-art shift cipher, which is
nearly unbreakable without the right software. However, the information kiosk
designers at Easter Bunny HQ were not expecting to deal with a master
cryptographer like yourself.

To decrypt a room name, rotate each letter forward through the alphabet
a number of times equal to the room's sector ID. A becomes B, B becomes C,
Z becomes A, and so on. Dashes become spaces.

For example, the real name for qzmt-zixmtkozy-ivhz-343 is very encrypted name.

What is the sector ID of the room where North Pole objects are stored?

'''



class Day4second(unittest.TestCase):

    def test_example(self):
        self.assertEqual('very encrypted name', decrypt('qzmt-zixmtkozy-ivhz', 343))
        
    def test_solution(self):

        def north_pole_objects_sector_id(rooms):
            for n in rooms:
                name, sector, checksum = split_name_string(n)
                if is_real_room(name, checksum):
                    if decrypt(name, sector) == 'northpole object storage':
                        return sector
            
        self.assertEqual(991, north_pole_objects_sector_id(data.splitlines()))

def is_real_room(name, checksum):
    return checksum == get_five_first_most_common_letters(name)


def get_five_first_most_common_letters(name):
    chars_by_freq = collections.Counter([c for c in name if c.isalpha()]).most_common()
    grouped_by_freq = {}
    for c, n in chars_by_freq:
        if n not in grouped_by_freq:
            grouped_by_freq[n] = []
        grouped_by_freq[n].append(c)
    chars_by_freq = []
    for n in sorted(grouped_by_freq, reverse=True):
        chars_by_freq.extend(sorted(grouped_by_freq[n]))
    return ''.join(chars_by_freq)[:5]


def split_name_string(name):
    parts = re.match(r'(.*)-(\d+)\[(.*)\]', name)
    ename = parts.group(1)
    sector = int(parts.group(2))
    checksum = parts.group(3)
    return ename, sector, checksum


def sum_sectors_of_real(names):
    s = 0
    for n in names:
        name, sector, checksum = split_name_string(n)
        if is_real_room(name, checksum):
            s += sector
    return s


def decrypt(encrypted, sector_id):
    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    amount = sector_id % len(alphabets)
    transition = string.maketrans(alphabets, alphabets[amount:] + alphabets[:amount])
    return string.translate(encrypted, transition).replace('-', ' ')
