import unittest
from inputs import DAY_4_INPUT


'''
--- Day 4: Secure Container ---

You arrive at the Venus fuel depot only to discover it's protected by
a password. The Elves had written the password on a sticky note, but someone
threw it out.

However, they do remember a few key facts about the password:

   - It is a six-digit number.
   - The value is within the range given in your puzzle input.
   - Two adjacent digits are the same (like 22 in 122345).
   - Going from left to right, the digits never decrease; they only ever
     increase or stay the same (like 111123 or 135679).

Other than the range rule, the following are true:

    111111 meets these criteria (double 11, never decreases).
    223450 does not meet these criteria (decreasing pair of digits 50).
    123789 does not meet these criteria (no double).

How many different passwords within the range given in your puzzle input meet
these criteria?

Your puzzle input is 134564-585159.


--- Part Two ---

An Elf just remembered one more important detail: the two adjacent matching
digits are not part of a larger group of matching digits.

Given this additional criterion, but still ignoring the range rule, the
following are now true:

112233 meets these criteria because the digits never decrease and all repeated
       digits are exactly two digits long.
123444 no longer meets the criteria (the repeated 44 is part of a larger group
       of 444).
111122 meets the criteria (even though 1 is repeated more than twice, it still
       contains a double 22).

How many different passwords within the range given in your puzzle input meet
all of the criteria?

'''


def has_two_adjacent_digits(num):
    numbers = list('{}'.format(num))
    for a, b in zip(numbers[1:], numbers):
        if a == b:
            return True
    return False


def has_exactly_two_adjacent_digits(num):
    numbers = list('{}'.format(num))
    amount_adjacent_numbers = []
    for a, b in zip(numbers[1:], numbers):
        if a == b:
            if amount_adjacent_numbers:
                amount_adjacent_numbers[-1] += 1
            else:
                amount_adjacent_numbers.append(2)
        else:
            amount_adjacent_numbers.append(1)
    return 2 in amount_adjacent_numbers 


def numbers_increasing_from_left_to_right(num):
    numbers = list('{}'.format(num))
    for a, b in zip(numbers[1:], numbers):
        if a < b:
            return False
    return True


def is_valid_password(num):
    return has_two_adjacent_digits(num) and numbers_increasing_from_left_to_right(num)


def is_valid_password_2(num):
    return has_exactly_two_adjacent_digits(num) and numbers_increasing_from_left_to_right(num)


class TestDayTwo(unittest.TestCase):

    def test_examples(self):
        self.assertEqual(False, has_two_adjacent_digits(101))
        self.assertEqual(True, has_two_adjacent_digits(22))
        self.assertEqual(True, has_two_adjacent_digits(1033))
        self.assertEqual(True, numbers_increasing_from_left_to_right(127))
        self.assertEqual(False, numbers_increasing_from_left_to_right(1243))
        self.assertEqual(True, numbers_increasing_from_left_to_right(345))
        self.assertEqual(True, is_valid_password(111111))
        self.assertEqual(False, is_valid_password(223450))
        self.assertEqual(False, is_valid_password(123789))

    def test_solution(self):
        valid_passwords = [n for n in range(*DAY_4_INPUT) if is_valid_password(n)]
        self.assertEqual(1929, len(valid_passwords))

    def test_examples_2(self):
        self.assertEqual(True, is_valid_password_2(112233))
        self.assertEqual(False, is_valid_password_2(123444))
        self.assertEqual(True, is_valid_password_2(111122))

    def test_solution_2(self):
        valid_passwords = [n for n in range(*DAY_4_INPUT) if is_valid_password_2(n)]
        self.assertEqual(1306, len(valid_passwords))
