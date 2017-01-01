import re
import unittest
from input_day_10 import data


''' --- Day 10: Balance Bots ---

You come upon a factory in which many robots are zooming around handing small
microchips to each other.

Upon closer examination, you notice that each bot only proceeds when it has two
microchips, and once it does, it gives each one to a different bot or puts it
in a marked "output" bin. Sometimes, bots take microchips from "input" bins,
too.

Inspecting one of the microchips, it seems like they each contain a single
number; the bots must use some logic to decide what to do with each chip. You
access the local control computer and download the bots' instructions (your
puzzle input).

Some of the instructions specify that a specific-valued microchip should be
given to a specific bot; the rest of the instructions indicate what a given bot
should do with its lower-value or higher-value chip.

For example, consider the following instructions:

    value 5 goes to bot 2
    bot 2 gives low to bot 1 and high to bot 0
    value 3 goes to bot 1
    bot 1 gives low to output 1 and high to bot 0
    bot 0 gives low to output 2 and high to output 0
    value 2 goes to bot 2

- Initially, bot 1 starts with a value-3 chip, and bot 2 starts with a value-2
chip and a value-5 chip.

- Because bot 2 has two microchips, it gives its lower one (2) to bot 1 and its
higher one (5) to bot 0.

- Then, bot 1 has two microchips; it puts the value-2 chip in output 1 and
gives the value-3 chip to bot 0.

- Finally, bot 0 has two microchips; it puts the 3 in output 2 and the 5 in
output 0.

- In the end, output bin 0 contains a value-5 microchip, output bin 1 contains
a value-2 microchip, and output bin 2 contains a value-3 microchip. In this
configuration, bot number 2 is responsible for comparing value-5 microchips
with value-2 microchips.

Based on your instructions, what is the number of the bot that is responsible
for comparing value-61 microchips with value-17 microchips?


--- Part Two ---

What do you get if you multiply together the values of one chip in each of
outputs 0, 1, and 2?

'''


class Day10(unittest.TestCase):

    def test_create_simple_instruction(self):
        self.assertEqual(InputInstruction, type(Instruction('value 12 goes to bot 23')))
        self.assertEqual(PassInstruction, type(Instruction('bot 2 gives low to bot 1 and high to bot 0')))

    def test_parse_12_goes_to_23(self):
        i = Instruction('value 12 goes to bot 23')
        self.assertEqual(12, i.chip_value)
        self.assertEqual(23, i.bot_index)

    def test_parse_2_gives_low_to_bot_1_and_high_to_output_3(self):
        i = Instruction('bot 2 gives low to bot 1 and high to output 3')
        self.assertEqual(2, i.bot_index)
        self.assertEqual('bot', i.targetLo)
        self.assertEqual(1, i.indexLo)
        self.assertEqual('output', i.targetHi)
        self.assertEqual(3, i.indexHi)

    def test_pass_instruction_will_move_chips_from_a_bot_to_another(self):
        f = Factory()
        f.get_bot(3).chips = [11, 12]
        Instruction('bot 3 gives low to bot 1 and high to bot 4').execute(f)
        self.assertEqual([], f.get_bot(3).chips)
        self.assertEqual([11], f.get_bot(1).chips)
        self.assertEqual([12], f.get_bot(4).chips)

    def test_pass_instruction_can_move_chips_to_output_bins(self):
        f = Factory()
        f.get_bot(3).chips = [11, 12]
        f.get_bot(5).chips = [22, 21]
        Instruction('bot 3 gives low to output 8 and high to output 6').execute(f)
        Instruction('bot 5 gives low to output 6 and high to output 8').execute(f)
        self.assertEqual([12, 21], f.get_bin(6))
        self.assertEqual([11, 22], f.get_bin(8))

    def test_robot_will_not_execute_instruction_with_one_chip(self):
        f = Factory()
        b = f.get_bot(3)
        b.todo(Instruction('bot 3 gives low to output 1 and high to output 5'))
        b.append(12)
        self.assertEqual([], f.get_bin(1))
        self.assertEqual([], f.get_bin(5))

    def test_robot_will_proceed_only_when_it_has_two_chips(self):
        f = Factory()
        b = f.get_bot(3)
        b.todo(Instruction('bot 3 gives low to output 1 and high to output 5'))
        b.append(12)
        b.append(53)
        self.assertEqual([12], f.get_bin(1))
        self.assertEqual([53], f.get_bin(5))

    def test_examples(self):
        f = Factory()
        f.step(Instruction('value 5 goes to bot 2'))
        f.step(Instruction('bot 2 gives low to bot 1 and high to bot 0'))
        f.step(Instruction('value 3 goes to bot 1'))
        f.step(Instruction('bot 1 gives low to output 1 and high to bot 0'))
        f.step(Instruction('bot 0 gives low to output 2 and high to output 0'))
        f.step(Instruction('value 2 goes to bot 2'))
        self.assertEqual([5], f.get_bin(0))
        self.assertEqual([2], f.get_bin(1))
        self.assertEqual([3], f.get_bin(2))
        pass

    def test_solution(self):

        class ProblemOneSolver(object):

            def visit(self, bot):
                if sorted(bot.chips) == [17, 61]:
                    self.solution = bot.index

        f = Factory()
        spy = ProblemOneSolver()
        for line in data.splitlines():
            f.step(Instruction(line, visitor=spy))

        self.assertEqual(86, spy.solution)

    def test_solution_two(self):
        f = Factory()
        for line in data.splitlines():
            f.step(Instruction(line))
        self.assertEqual(22847, reduce(lambda x, y: x * y, f.get_bin(0) + f.get_bin(1) + f.get_bin(2)))


class Instruction(object):

    def __init__(self, instruction, visitor=None):
        cls, args = self.parse(instruction)
        self.__class__ = cls
        self.__init__(*args)
        self.visitor = visitor

    def parse(self, string):
        if string.startswith('value'):
            match = re.split(r'value (\d+) goes to bot (\d+)', string)
            return InputInstruction, (int(match[1]), int(match[2]))
        elif string.startswith('bot'):
            match = re.split(r'bot (\d+) gives low to (\w+) (\d+) and high to (\w+) (\d+)', string)
            return PassInstruction, (int(match[1]), match[2], int(match[3]), match[4], int(match[5]))


class InputInstruction(Instruction):

    def __init__(self, value, bot):
        self.chip_value = value
        self.bot_index = bot

    def execute(self, factory):
        factory.get_bot(self.bot_index).append(self.chip_value)
        factory.get_bot(self.bot_index).accept(self.visitor)


class PassInstruction(Instruction):

    def __init__(self, bot, targetLo, indexLo, targetHi, indexHi):
        self.bot_index = bot
        self.targetLo = targetLo
        self.indexLo = indexLo
        self.targetHi = targetHi
        self.indexHi = indexHi

    def execute(self, factory):
        bot = factory.get_bot(self.bot_index)
        bot.accept(self.visitor)

        if bot.has_not_enough_chips():
            bot.todos.append(self)
            return

        bot.chips.sort()
        self.insert(bot.chips.pop(), self.targetHi, self.indexHi, factory)
        self.insert(bot.chips.pop(), self.targetLo, self.indexLo, factory)

    def insert(self, value, target, index, factory):
        {
            'bot':    factory.get_bot,
            'output': factory.get_bin
        }[target](index).append(value)


class Bot(object):

    def __init__(self, factory, index):
        self.factory = factory
        self.index = index
        self.todos = []
        self.chips = []

    def index():
        pass

    def append(self, value):
        self.chips.append(value)
        self.execute_pending_instructions()

    def execute_pending_instructions(self):
        if self.has_not_enough_chips():
            return
        if self.todos:
            self.todos.pop().execute(self.factory)

    def has_not_enough_chips(self):
        return len(self.chips) < 2

    def todo(self, i):
        self.todos.append(i)

    def accept(self, v):
        if v:
            v.visit(self)


class Factory(object):

    def __init__(self):
        self.bots = {}
        self.bins = {}

    def step(self, instruction):
        instruction.execute(self)

    def get_bot(self, i):
        if i not in self.bots:
            self.bots[i] = Bot(self, i)
        return self.bots[i]

    def get_bin(self, i):
        if i not in self.bins:
            self.bins[i] = []
        return self.bins[i]


if __name__ == '__main__':
    unittest.main()
