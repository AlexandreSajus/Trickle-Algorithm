import unittest
from node import Node
from random import random, randint

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
neighbors = {0: [B, D], 1: [C, E], 2: [E], 3: [E], 4: [A, B]}


class run_tests(unittest.TestCase):
    def test_shape_and_check_version(self):
        A = Node(0, 1, 2, randint(1, 3), 1, random()*1/2 + 1/2, 0, [],
            ["code_fragment_1_version_2", "code_fragment_2_version_2"], [True, True])
        # Checks whether A has the adequate shape
        assert A.id_number == 0
        assert A.i_min == 1
        assert A.i_max == 2
        assert int(A.k) == A.k and 1 <= A.k <= 3
        assert A.i == 1
        assert A.i /2 <= A.tau <= A.i
        assert A.c == 0
        assert A.messages == []
        assert A.ld == ["code_fragment_1_version_2",
                        "code_fragment_2_version_2"]
        assert A.md == [True, True]

        vers_check = A.check_version(
            (1, ["code_fragment_1_version_1", "code_fragment_2_version_1"], [False, False]), 1)
        assert vers_check == -1
    
    def test_send_message(self):
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
        neighbors = {0: [B, D], 1: [C, E], 2: [E], 3: [E], 4: [A, B]}
        A.send_message(neighbors)
        for node in neighbors[A.id_number]:
            assert [0, ["code_fragment_1_version_2", "code_fragment_2_version_2"], [True, True]] in node.messages
        
    def test_act_2(self):
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
        neighbors = {0: [B, D], 1: [C, E], 2: [E], 3: [E], 4: [A, B]}
        A.send_message(neighbors)
        assert A.c == 0
        B.act_2(False, neighbors) # We are at t < tau
        assert B.ld == A.ld 
        assert B.md == A.md 
        assert B.c == 0
        assert B.messages == []
        # B sent a message to his neighbors
        C.act_2(False, neighbors)
        assert C.ld == B.ld 
        assert C.md == B.md
        assert C.c == 0 
        assert C.messages == []
        # Same thing with C
        D.act_2(False, neighbors)
        assert D.ld == A.ld 
        assert D.md == A.md
        assert D.c == 0 
        assert D.messages == []
        # Same with D
        E.act_2(False, neighbors)
        assert E.ld == D.ld and E.ld == B.ld and E.ld == C.ld 
        assert E.md == D.md and E.md == B.md and E.md == C.md 
        assert E.c == 4
        assert E.messages == []
        # Same : E send a message
        A.act_2(True, neighbors)
        assert A.c == 0
        assert A.i == 2
        assert A.messages == []
        assert A.t == 0
        assert A.i /2 <= A.tau <= A.i
        B.md = [False, False] # to make another update, but after tau this time
        A.send_message(neighbors)
        B.act_2(True, neighbors)
        assert B.messages == []
        assert B.md == [True, True]
        assert B.ld == A.ld 
        assert B.i == 1
        assert B.c == 0
        assert B.t == 0
        assert B.i /2 <= B.tau <= B.i
        



if __name__ == '__main__':
    unittest.main()
