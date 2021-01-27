import unittest
from run import *
import random as rd


class run_tests(unittest.TestCase):
    def test1(self):
        a = rd.randint(1, 3)
        b = random()*1/2 + 1
        A = Node(0, 1, 3, a, 1, b, 0, [],
                 ["code_fragment_1_version_2", "code_fragment_2_version_2"], [True, True])
        assert(A.id_number == 0)
        assert(A.i_min == 1)
        assert(A.i_max == 3)
        assert(A.k == a)
        assert(A.i == 1)
        assert(A.tau == b)
        assert(A.c == 0)
        assert(A.messages == [])
        assert(A.ld == ["code_fragment_1_version_2",
                        "code_fragment_2_version_2"])
        assert(A.md == [True, True])

        vers_check = A.check_version(
            (1, "code_fragment_1_version_1", [False, False]), 1)
        assert(vers_check == -1)


if __name__ == '__main__':
    unittest.main()
