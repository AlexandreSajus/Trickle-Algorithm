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

nodes = [A, B, C, D, E]
class run_tests(unittest.TestCase):
    def test_shape_and_check_version(self, nodes, neighbors):
        # Checks whether A has the adequate shape
        A = nodes[0]
        assert(A.id_number == 0)
        assert(A.i_min == 1)
        assert(A.i_max == 2)
        assert(int(A.k) == A.k and 1 <= A.k <= 3)
        assert(A.i == 1)
        assert(A.i /2 <= A.tau <= A.i)
        assert(A.c == 0)
        assert(A.messages == [])
        assert(A.ld == ["code_fragment_1_version_2",
                        "code_fragment_2_version_2"])
        assert(A.md == [True, True])

        vers_check = A.check_version(
            (1, ["code_fragment_1_version_1", "code_fragment_2_version_1"], [False, False]), 1)
        assert(vers_check == -1)
    
    def test_send_message(self, nodes, neighbors):
        A = nodes[0]
        A.send_message()
        for node in neighbors[A.id_number]:
            assert([0, ["code_fragment_1_version_2", "code_fragment_2_version_2"], [True, True]] in node.messages)
        
    def test_act_2(self, A, B, C, D, E, neighbors):
        # A doesn't send a message again to avoid redundancy (because we tested send_message before)
        for node in nodes:
            node.send_message()
        



if __name__ == '__main__':
    unittest.main()
