import unittest
from run import *
import random as rd

A = Node(0, 1, 2, randint(1, 3), 1, random()*1/2 + 1/2, 0, [],
             ["code_fragment_1_version_2", "code_fragment_2_version_2"], [True, True])
B = Node(1, 1, 2, randint(1, 3), 1, random()*1/2 + 1/2, 0, [],
            ["code_fragment_1_version_1", "code_fragment_2_version_1"], [False, False])
C = Node(2, 1, 2, randint(1, 3), 1, random()*1/2 + 1/2, 0, [],
            ["code_fragment_1_version_1", "code_fragment_2_version_1"], [False, False])
D = Node(3, 1, 2, randint(1, 3), 1, random()*1/2 + 1/2, 0, [],
            ["code_fragment_1_version_1", "code_fragment_2_version_1"], [False, False])
E = Node(4, 1, 2, randint(1, 3), 1, random()*1/2 + 1/2, 0, [],
            ["code_fragment_1_version_1", "code_fragment_2_version_1"], [False, False])
neighbors = {0: [B, D], 1: [D, E], 2: [E], 3: [E, C], 4: [A, B]}
class run_tests(unittest.TestCase):
    def test1(self):
        # Checks whether A has the adequate shape
        A = Node(0, 1, 3, randint(1, 3), 1, random()*1/2 + 1/2, 0, [],
             ["code_fragment_1_version_2", "code_fragment_2_version_2"], [True, True])
        assert(A.id_number == 0)
        assert(A.i_min == 1)
        assert(A.i_max == 3)
        assert(int(A.k) == A.k and 1 <= A.k <= 3)
        assert(A.i == 1)
        assert(A.i /2 <= A.tau <= A.i)
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
