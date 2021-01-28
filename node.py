# Creates the Node object and the next_step function

from random import random, randint, uniform
import numpy as np

# length of LD and MD, number of fragments of software
n_fragments = 2


class Node:
    def __init__(self, id_number, i_min, i_max, k, i, tau, c, messages, ld, md, t=0):
        self.id_number = id_number  # identifies the node, Int
        self.i_min = i_min  # minimum of interval I
        self.i_max = i_max  # maximum of interval I
        self.k = k  # redundancy indicator k
        self.i = i  # current value of I
        self.tau = tau  # at what time does the node transfer its version
        self.c = c  # number of neighbouring nodes with the same version
        # mailbox, messages from other nodes will be stored in this list as tuples (id_number, ld, md)
        self.messages = messages
        self.ld = ld  # LD, contains the current fragments of software
        self.md = md  # MD, contains the current number of version
        self.t = t

    def check_version(self, message, k):
        """
        Compares the current version to a version sent in a message
        :param message: a received message (id_number, ld, md)
        :type message: Tuple
        :param k: the number of the fragment to check in ld and md
        :type k: Int
        :return: 1 if the current version is lower, 0 if it is the same, -1 if it is higher
        :rtype: Int
        """
        if self.md[k] == message[2][k]:
            return 0
        elif self.md[k] == True and message[2][k] == False:
            return -1
        elif self.md[k] == False and message[2][k] == True:
            return 1

    def send_message(self, neighbors):
        # Sends a message with the current version to neighbouring nodes
        for recipient in neighbors[self.id_number]:
            recipient.messages.append([self.id_number, self.ld, self.md])

    def act(self, after_tau, neighbors):
       # check if any version received in messages is different from the current one
        version_change = True

        while len(self.messages) > 0:
            # check the messages, if the current version is lower than the one received, update; if it is higher, send it to neighbouring nodes
            message = self.messages.pop()
            for k in range(n_fragments):
                check_version = self.check_version(message, k)
                if check_version == 0:
                    self.c += 1
                elif check_version == -1:
                    version_change = False
                    self.send_message(neighbors)
                elif check_version == 1:
                    version_change = False
                    self.ld[k] = message[1][k]
                    self.md[k] = message[2][k]

        if self.c < self.k and after_tau == False:
            # if c < k, send our version to neighbouring nodes
            self.send_message(neighbors)

        if after_tau:
            if version_change:
                # if a version was different, extend i
                self.i = self.i*2
            else:
                # if not, reset i and c
                self.i = self.i_min
                self.c = 0
            self.tau = uniform(self.i/2, self.i)
            self.t = 0


def next_step(neighbors, nodes, not_tau=[], non_i=[]):
    before_tau = []  # list of [node, duration_tau] such as t - tau < 0
    before_i = []  # list of [node, duration_i] such as t - i < 0
    for node in nodes:
        duration_tau = node.tau - node.t
        duration_i = node.i - node.t
        if duration_tau >= 0:
            before_tau.append([node, duration_tau])
        if duration_i >= 0:
            before_i.append([node, duration_i])

    # We look for the node that will act first by finding the minimal duration_i or duration_tau
    arg_min = None
    duration_min = np.inf
    after_tau = False  # Checks if the next action is caused by tau or i
    for elem in before_tau:  # Browse through duration_tau
        if elem[1] < duration_min:
            # We check if the node hasn't acted during the previous step, if it did it would cause duration_tau to be equal to 0
            if not elem[0] in not_tau:
                duration_min = elem[1]
                arg_min = elem[0]
    for elem in before_i:  # Browse through duration_i
        if elem[1] < duration_min:
            # We check if the node hasn't acted during the previous step, if it did it would cause duration_i to be equal to 0
            if not elem[0] in non_i:
                duration_min = elem[1]
                arg_min = elem[0]
                after_tau = True

    # not_tau and not_i keep track of every node that acts according to tau or i at this step
    # so that they don't act again at the next step
    if duration_min > 0:
        not_tau = []
        non_i = []

    for node in nodes:
        node.t = node.t + duration_min  # time increases

    # the chosen node acts according to its act function
    arg_min.act(after_tau, neighbors)

    if after_tau == False:
        # if the node acted according to tau, we add it to not_tau
        not_tau.append(arg_min)
    else:
        # same with not_i
        non_i.append(arg_min)
    return nodes, not_tau, non_i


if __name__ == "__main__":
    # An example graph
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
