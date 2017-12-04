import unittest


'''
--- Day 1: Inverse Captcha ---

The night before Christmas, one of Santa's Elves calls you in a panic. "The
printer's broken! We can't print the Naughty or Nice List!" By the time you
make it to sub-basement 17, there are only a few minutes until midnight. "We
have a big problem," she says; "there must be almost fifty bugs in this system,
but nothing else can print The List. Stand in this square, quick! There's no
time to explain; if you can convince them to pay you in stars, you'll be able
to--" She pulls a lever and the world goes blurry.

When your eyes can focus again, everything seems a lot more pixelated than
before. She must have sent you inside the computer! You check the system clock:
25 milliseconds until midnight. With that much time, you should be able to
collect all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each
day millisecond in the advent calendar; the second puzzle is unlocked when you
complete the first. Each puzzle grants one star. Good luck!

You're standing in a room with "digitization quarantine" written in LEDs along
one wall. The only door is locked, but it includes a small interface.
"Restricted Area - Strictly No Digitized Users Allowed."

It goes on to explain that you may only leave by solving a captcha to prove
you're not a human. Apparently, you only get one millisecond to solve the
captcha: too fast for a normal human, but it feels like hours to you.

The captcha requires you to review a sequence of digits (your puzzle input) and
find the sum of all digits that match the next digit in the list. The list is
circular, so the digit after the last digit is the first digit in the list.

For example:

    1122 produces a sum of 3 (1 + 2) because the first digit (1) matches the
         second digit and the third digit (2) matches the fourth digit.
    1111 produces 4 because each digit (all 1) matches the next.
    1234 produces 0 because no digit matches the next.
    91212129 produces 9 because the only digit that matches the next one is the
         last digit, 9. 

    What is the solution to your captcha?

--- Part Two ---

You notice a progress bar that jumps to 50% completion. Apparently, the door
isn't yet satisfied, but it did emit a star as encouragement. The instructions
change:

Now, instead of considering the next digit, it wants you to consider the digit
halfway around the circular list. That is, if your list contains 10 items, only
include a digit in your sum if the digit 10/2 = 5 steps forward matches it.
Fortunately, your list has an even number of elements.

For example:

    1212 produces 6: the list contains 4 items, and all four digits match the
         digit 2 items ahead.
    1221 produces 0, because every comparison is between a 1 and a 2.
    123425 produces 4, because both 2s match each other, but no other digit has
         a match.
    123123 produces 12.
    12131415 produces 4.

    What is the solution to your new captcha?

'''


def get_captcha_I(string):
    digits = [int(v) for v in string]
    return sum_pairs(digits)


def get_captcha_II(string):
    digits = [int(v) for v in string]
    r = len(digits) / 2
    return sum_pairs(digits, r)


def sum_pairs(digits, distance=1):
    with_offset = digits[-distance:] + digits[:-distance]
    return sum(a for a, b in zip(digits, with_offset) if a == b)


class TestDayOne(unittest.TestCase):

    def test_examples_I(self):
        self.assertEqual(3, get_captcha_I('1122'))
        self.assertEqual(4, get_captcha_I('1111'))
        self.assertEqual(0, get_captcha_I('1234'))
        self.assertEqual(9, get_captcha_I('91212129'))

    def test_I_solution(self):
        self.assertEqual(1251, get_captcha_I(inputstring))

    def test_examples_II(self):
        self.assertEqual(6, get_captcha_II('1212'))
        self.assertEqual(0, get_captcha_II('1221'))
        self.assertEqual(4, get_captcha_II('123425'))
        self.assertEqual(12, get_captcha_II('123123'))
        self.assertEqual(4, get_captcha_II('12131415'))

    def test_solution_II(self):
        self.assertEqual(1244, get_captcha_II(inputstring))


inputstring = '516299281491169512719425276194596424291268712697155863651846937925928456958813624428156218468331423858422613471962165756423837756856519754524985759763747559711257977361228357678293572698839754444752898835313399815748562519958329927911861654784216355489319995566297499836295985943899373615223375271231128914745273184498915241488393761676799914385265459983923743146555465177886491979962465918888396664233693243983969412682561799628789569294374554575677368219724142536789649121758582991345537639888858113763738518511184439854223386868764189133964543721941169786274781775658991329331759679943342217578532643519615296424396487669451453728113114748217177826874953466435436129165295379157226345786756899935747336785161745487933721527239394118721517195849186676814232887413175587327214144876898248571248517121796766248817366614333915154796983612174281237846165129114988453188844745119798643314857871527757831265298846833327863781341559381238458322786192379487455671563757123534253463563421716138641611915686247343417126655317378639314168461345613427262786624689498485599942336813995725145169355942616672812792174556866436158375938988738721253664772584577384558696477546232189312287262439452141564522329987139692281984783513691857538335537553448919819545332125483128878925492334361562192621672993868479566688564752226111784486619789588318171745995253645886833872665447241245329935643883892447524286642296955354249478815116517315832179925494818748478164317669471654464867111924676961162162841232473474394739793968624974397916495667233337397241933765513777241916359166994384923869741468174653353541147616645393917694581811193977311981752554551499629219873391493426883886536219455848354426461562995284162323961773644581815633779762634745339565196798724847722781666948626231631632144371873154872575615636322965353254642186897127423352618879431499138418872356116624818733232445649188793318829748789349813295218673497291134164395739665667255443366383299669973689528188264386373591424149784473698487315316676637165317972648916116755224598519934598889627918883283534261513179931798591959489372165295'
