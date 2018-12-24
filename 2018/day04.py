#!/usr/bin/python3
import re
import unittest
from inputs import DAY4_INPUT


'''

Repose Record

    You've sneaked into another supply closet - this time, it's across from the
    prototype suit manufacturing lab. You need to sneak inside and fix the issues
    with the suit, but there's a guard stationed outside the lab, so this is as
    close as you can safely get.

    As you search the closet for anything that might help, you discover that you're
    not the first person to want to sneak in. Covering the walls, someone has spent
    an hour starting every midnight for the past few months secretly observing this
    guard post! They've been writing down the ID of the one guard on duty that
    night - the Elves seem to have decided that one guard was enough for the
    overnight shift - as well as when they fall asleep or wake up while at their
    post (your puzzle input).

    For example, consider the following records, which have already been organized
    into chronological order:

    [1518-11-01 00:00] Guard #10 begins shift
    [1518-11-01 00:05] falls asleep
    [1518-11-01 00:25] wakes up
    [1518-11-01 00:30] falls asleep
    [1518-11-01 00:55] wakes up
    [1518-11-01 23:58] Guard #99 begins shift
    [1518-11-02 00:40] falls asleep
    [1518-11-02 00:50] wakes up
    [1518-11-03 00:05] Guard #10 begins shift
    [1518-11-03 00:24] falls asleep
    [1518-11-03 00:29] wakes up
    [1518-11-04 00:02] Guard #99 begins shift
    [1518-11-04 00:36] falls asleep
    [1518-11-04 00:46] wakes up
    [1518-11-05 00:03] Guard #99 begins shift
    [1518-11-05 00:45] falls asleep
    [1518-11-05 00:55] wakes up

    Timestamps are written using year-month-day hour:minte format. The guard
    falling asleep or waking up is always the one whose shift most recently
    started. Because all asleep/awake times are during the midnight hour (00:00 -
    00:59), only the minute portion (00 - 59) is relevant for those events.

    Visually, these records show that the guards are asleep at these times:

    Date   ID   Minute
                000000000011111111112222222222333333333344444444445555555555
                012345678901234567890123456789012345678901234567890123456789
    11-01  #10  .....####################.....#########################.....
    11-02  #99  ........................................##########..........
    11-03  #10  ........................#####...............................
    11-04  #99  ....................................##########..............
    11-05  #99  .............................................##########.....

    The columns are Date, which shows the month-day portion of the relevant day;
    ID, which shows the guard on duty that day; and Minute, which shows the minutes
    during which the guard was asleep within the midnight hour. (The Minute
    column's header shows the minute's ten's digit in the first row and the one's
    digit in the second row.) Awake is shown as ., and asleep is shown as #.

    Note that guards count as asleep on the minute they fall asleep, and they count
    as awake on the minute they wake up. For example, because Guard #10 wakes up at
    00:25 on 1518-11-01, minute 25 is marked as awake.

    If you can figure out the guard most likely to be asleep at a specific time,
    you might be able to trick that guard into working tonight so you can have the
    best chance of sneaking in. You have two strategies for choosing the best
    guard/minute combination.

    Strategy 1: Find the guard that has the most minutes asleep. What minute does
    that guard spend asleep the most?

    In the example above, Guard #10 spent the most minutes asleep, a total of 50
    minutes (20+25+5), while Guard #99 only slept for a total of 30 minutes
    (10+10+10). Guard #10 was asleep most during minute 24 (on two days, whereas
    any other minute the guard was asleep was only seen on one day).

    While this example listed the entries in chronological order, your entries are
    in the order you found them. You'll need to organize them before they can be
    analyzed.

    What is the ID of the guard you chose multiplied by the minute you chose? (In
    the above example, the answer would be 10 * 24 = 240.)

    --- Part Two ---

    Strategy 2: Of all guards, which guard is most frequently asleep on the same
    minute?

    In the example above, Guard #99 spent minute 45 asleep more than any other
    guard or minute - three times in total. (In all other cases, any guard spent
    any minute asleep at most twice.)

    What is the ID of the guard you chose multiplied by the minute you chose? (In
    the above example, the answer would be 99 * 45 = 4455.)

'''


EXAMPLE_INPUT = '''\
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-05 00:55] wakes up
'''


class Guard():

    def __init__(self, number):
        self.number = number
        self.sleep = {}
        self.slept = None

    def most_slept_minutes(self):
        max_minutes = max(self.sleep.values())
        return [m % 100 for m, n in self.sleep.items() if n == max_minutes]

    def num_times_on_most_frequent_sleep_minute(self):
        return max(self.sleep.values()) if self.sleep else 0

    def fall_asleep(self, time):
        self.slept = time

    def woke_up(self, time):

        def iter_minutes(start, stop):
            while start < stop:
                yield start
                start += 1 if start % 100 != 59 else 41

        for m in iter_minutes(self.slept, time):
            if m not in self.sleep:
                self.sleep[m] = 0
            self.sleep[m] += 1

    def slept_minutes(self):
        return sum([minutes for _, minutes in self.sleep.items()])


def populate_guards(log):

    current = None
    guards = {}

    for _, _, hour, minutes, event in chronological_parser(log):
        m = (100 * int(hour)) + int(minutes)
        if event.startswith('Guard'):
            current = int(re.match(r'Guard\s#(\d+)\s.*', event.strip()).groups()[0])
            if current not in guards:
                guards[current] = Guard(current)
        elif event.endswith('falls asleep'):
            guards[current].fall_asleep(m)
        elif event.endswith('wakes up'):
            guards[current].woke_up(m)
    return guards


def chronological_parser(log):

    def datestamp(entry):
        month, day, hour, minutes, _ = entry
        return int(month + day + hour + minutes)

    parsed_log = []
    for line in log.splitlines():
        match = re.match(r'\[1518\-(\d\d)\-(\d\d) (\d\d):(\d\d)\] (.*)', line.strip())
        month, day, hour, minutes, event = match.groups()
        parsed_log.append((month, day, hour, minutes, event))

    sorted_log = sorted(parsed_log, key=datestamp)
    return sorted_log


def solve_part_1(lines):
    guards = populate_guards(lines)
    guard_numbers_by_sleep = {g.slept_minutes(): g.number for g in guards.values()}
    max_sleep_time = max(guard_numbers_by_sleep.keys())
    number_who_slept_the_most = guard_numbers_by_sleep[max_sleep_time]
    g = guards[number_who_slept_the_most]
    return g.number * g.most_slept_minutes()[0]


def solve_part_2(lines):
    guards = populate_guards(lines)
    guard_numbers_by_most_frequent_minute_in_sleep = {g.num_times_on_most_frequent_sleep_minute(): g.number for g in guards.values()}
    top_sleeper = guard_numbers_by_most_frequent_minute_in_sleep[max(guard_numbers_by_most_frequent_minute_in_sleep.keys())]
    return top_sleeper * guards[top_sleeper].most_slept_minutes()[0]


class TestDay04(unittest.TestCase):

    def test_logline_parse_line(self):
        s = EXAMPLE_INPUT.splitlines()[0]
        r = r'\[1518\-(\d\d)\-(\d\d) (\d\d):(\d\d)\] (.*)'
        m = re.match(r, s.strip())
        self.assertEqual(m.groups(), ('11', '01', '00', '00', 'Guard #10 begins shift'))

    def test_guard_begins_shift(self):
        s = 'Guard #1034 begins shift'
        m = re.match(r'Guard\s#(\d+)\s.*', s.strip())
        number = m.groups()[0]
        self.assertEqual(number, '1034')

    def test_guard_slept_once(self):
        g = Guard(10)
        g.fall_asleep(2357)
        g.woke_up(2402)
        self.assertEqual(g.sleep, {2357: 1, 2358: 1, 2359: 1, 2400: 1, 2401: 1})

    def test_sort(self):
        sorted_entries = chronological_parser(EXAMPLE_INPUT)
        self.assertEqual(sorted_entries, [('11', '01', '00', '00', 'Guard #10 begins shift'),
                                          ('11', '01', '00', '05', 'falls asleep'),
                                          ('11', '01', '00', '25', 'wakes up'),
                                          ('11', '01', '00', '30', 'falls asleep'),
                                          ('11', '01', '00', '55', 'wakes up'),
                                          ('11', '01', '23', '58', 'Guard #99 begins shift'),
                                          ('11', '02', '00', '40', 'falls asleep'),
                                          ('11', '02', '00', '50', 'wakes up'),
                                          ('11', '03', '00', '05', 'Guard #10 begins shift'),
                                          ('11', '03', '00', '24', 'falls asleep'),
                                          ('11', '03', '00', '29', 'wakes up'),
                                          ('11', '04', '00', '02', 'Guard #99 begins shift'),
                                          ('11', '04', '00', '36', 'falls asleep'),
                                          ('11', '04', '00', '46', 'wakes up'),
                                          ('11', '05', '00', '03', 'Guard #99 begins shift'),
                                          ('11', '05', '00', '45', 'falls asleep'),
                                          ('11', '05', '00', '55', 'wakes up')])

    def test_populate_guards(self):
        guards = populate_guards(EXAMPLE_INPUT)
        self.assertEqual(guards[10].slept_minutes(), 50)
        self.assertEqual(guards[99].slept_minutes(), 30)
        self.assertEqual(guards[10].most_slept_minutes()[0], 24)
        self.assertEqual(guards[99].most_slept_minutes()[0], 45)

    def test_example1(self):
        self.assertEqual(solve_part_1(EXAMPLE_INPUT), 240)

    def test_solution_1(self):
        self.assertEqual(solve_part_1(DAY4_INPUT), 138280)

    def test_example2(self):
        self.assertEqual(solve_part_2(EXAMPLE_INPUT), (99 * 45))

    def test_solution_2(self):
        self.assertEqual(solve_part_2(DAY4_INPUT), 89347)


if __name__ == '__main__':
    unittest.main()
