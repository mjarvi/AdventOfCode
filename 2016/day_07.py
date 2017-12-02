import unittest
import re
from input_day_07 import data


''' --- Day 7: Internet Protocol Version 7 ---

While snooping around the local network of EBHQ, you compile a list of IP
addresses (they're IPv7, of course; IPv6 is much too limited). You'd like to
figure out which IPs support TLS (transport-layer snooping).

An IP supports TLS if it has an Autonomous Bridge Bypass Annotation, or ABBA.
An ABBA is any four-character sequence which consists of a pair of two
different characters followed by the reverse of that pair, such as xyyx or
abba. However, the IP also must not have an ABBA within any hypernet sequences,
which are contained by square brackets.

For example:

 - abba[mnop]qrst supports TLS (abba outside square brackets).
 - abcd[bddb]xyyx does not support TLS (bddb is within square brackets, even though xyyx is outside square brackets).
 - aaaa[qwer]tyui does not support TLS (aaaa is invalid; the interior characters must be different).
 - ioxxoj[asdfgh]zxcvbn supports TLS (oxxo is outside square brackets, even though it's within a larger string).

How many IPs in your puzzle input support TLS?
'''


class Day7(unittest.TestCase):

    def test_extract_hypernet(self):
        self.assertEqual((['abba', 'qrst'], ['mnop']), extract_hypernet('abba[mnop]qrst'))
        self.assertEqual((['abba', 'qrst'], ['mnop']), extract_hypernet('abba[mnop]qrst'))
        self.assertEqual((['abcd', 'xyyx'], ['bddb']), extract_hypernet('abcd[bddb]xyyx'))

    def test_find_abba(self):
        self.assertEqual(True, has_tls_support('abbaasdfa[qrst]adsf'))
        self.assertEqual(True, has_tls_support('asdfcbbc[qrst]oss'))
        self.assertEqual(True, has_tls_support('asdfcbc[qrst]osso'))
        self.assertEqual(False, has_tls_support('asdfcbc[qrsttsddd]osso'))

    def test_can_find_all_parts_of_address_and_hypernet(self):
        self.assertEqual((['xfpeuaftjtjzzyrlw', 'klpxbsifaszxapsosjq', 'kodbuiigbiqdbarr', 'yusyefeqfqjkcmnrfd'],
                          ['vxklxjatlbpevalmb', 'kjzdnfadnybfnfvm', 'vkgxvvccoyknqcg']),
                         extract_hypernet('xfpeuaftjtjzzyrlw[vxklxjatlbpevalmb]klpxbsifaszxapsosjq[kjzdnfadnybfnfvm]kodbuiigbiqdbarr[vkgxvvccoyknqcg]yusyefeqfqjkcmnrfd'))

    def test_example(self):

        # supports TLS (abba outside square brackets).
        self.assertEqual(True, has_tls_support('abba[mnop]qrst'))

        # does not support TLS (bddb is within square brackets, even though xyyx is outside square brackets).
        self.assertEqual(False, has_tls_support('abcd[bddb]xyyx'))

        # does not support TLS (aaaa is invalid; the interior characters must be different).
        self.assertEqual(False, has_tls_support('aaaa[qwer]tyui'))

        # supports TLS (oxxo is outside square brackets, even though it's within a larger string).
        self.assertEqual(True, has_tls_support('ioxxoj[asdfgh]zxcvbn'))

    def test_solution(self):
        self.assertEqual(110, sum([has_tls_support(a) for a in data.splitlines()]))


''' --- Part Two ---

You would also like to know which IPs support SSL (super-secret listening).

An IP supports SSL if it has an Area-Broadcast Accessor, or ABA, anywhere in
the supernet sequences (outside any square bracketed sections), and
a corresponding Byte Allocation Block, or BAB, anywhere in the hypernet
sequences. An ABA is any three-character sequence which consists of the same
character twice with a different character between them, such as xyx or aba.
A corresponding BAB is the same characters but in reversed positions: yxy and
bab, respectively.

For example:

    aba[bab]xyz supports SSL (aba outside square brackets with corresponding bab within square brackets).
    xyx[xyx]xyx does not support SSL (xyx, but no corresponding yxy).
    aaa[kek]eke supports SSL (eke in supernet with corresponding kek in hypernet; the aaa sequence is not related, because the interior character must be different).
    zazbz[bzb]cdb supports SSL (zaz has no corresponding aza, but zbz has a corresponding bzb, even though zaz and zbz overlap).

How many IPs in your puzzle input support SSL?
'''


class Day7PartTwo(unittest.TestCase):

    def test_example(self):
        # supports SSL (aba outside square brackets with corresponding bab
        # within square brackets).
        self.assertEqual(True, has_ssl_support('aba[bab]xyz'))

        # does not support SSL (xyx, but no corresponding yxy).
        self.assertEqual(False, has_ssl_support('xyx[xyx]xyx'))

        # supports SSL (eke in supernet with corresponding kek in hypernet; the
        # aaa sequence is not related, because the interior character must be
        # different).
        self.assertEqual(True, has_ssl_support('aaa[kek]eke'))

        # supports SSL (zaz has no corresponding aza, but zbz has
        # a corresponding bzb, even though zaz and zbz overlap).
        self.assertEqual(True, has_ssl_support('zazbz[bzb]cdb'))

    def test_solution(self):
        self.assertEqual(242, sum([has_ssl_support(a) for a in data.splitlines()]))


def extract_hypernet(address):
    splits = re.split(r'(\[.*?\])', address)
    addresses = [a for a in splits if not a.startswith('[')]
    hypernets = [a.strip('[]') for a in splits if a.startswith('[')]
    return addresses, hypernets


def has_tls_support(full_address):
    addresses, hypernets = extract_hypernet(full_address)
    return not any([contains_abba(h) for h in hypernets]) \
        and any([contains_abba(a) for a in addresses])


def contains_abba(address):
    for i in range(len(address) - 3):
        if is_abba(address[i:i + 4]):
            return True
    return False


def has_ssl_support(full_address):
    addresses, hypernets = extract_hypernet(full_address)
    for a in addresses:
        for aba in find_aba(a):
            if find_bab(hypernets, aba):
                return True
    return False


def find_aba(address):
    for i in range(len(address) - 2):
        cand = address[i:i + 3]
        if is_aba(cand):
            yield cand


def find_bab(strings, aba):
    bab = aba[1] + aba[0] + aba[1]
    for s in strings:
        if s.find(bab) != -1:
            return True


def is_abba(n):
    return n[0] == n[3] and n[1] == n[2] and n[0] != n[1]


def is_aba(n):
    return n[0] == n[2] and n[0] != n[1]


if __name__ == '__main__':
    unittest.main()
