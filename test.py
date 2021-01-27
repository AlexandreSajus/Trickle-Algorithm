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

nodes = [A, B, C, D, E]
class run_tests(unittest.TestCase):
    def __init__(self):
        pass

    def test_shape_and_check_version(self, nodes, neighbors):
        # Checks whether A has the adequate shape
        A = nodes[0]
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
    
    def test_send_message(self, nodes, neighbors):
        A = nodes[0]
        A.send_message(neighbors)
        for node in neighbors[A.id_number]:
            assert [0, ["code_fragment_1_version_2", "code_fragment_2_version_2"], [True, True]] in node.messages
        
    def test_act_2(self, nodes, neighbors):    
        A, B, C, D, E = nodes[0], nodes[1], nodes[2], nodes[3], nodes[4]
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
        print(A.c)
        assert A.c == 2
        assert A.i == 1/2
        assert A.messages == []
        assert A.t == 0
        assert A.i /2 <= A.tau <= A.i
        B.md = [False, False] # to make another update, but after tau this time
        A.send_message()
        B.act_2(True, neighbors)
        assert B.messages == []
        assert B.md == [True, True]
        assert B.ld == A.ld 
        assert B.i == 1
        assert B.c == 0
        assert B.t == 0
        assert B.i /2 <= B.tau <= B.i
        



if __name__ == '__main__':
    test = run_tests()
    test.test_shape_and_check_version(nodes, neighbors)
    test.test_send_message(nodes, neighbors)
    test.test_act_2(nodes, neighbors)
