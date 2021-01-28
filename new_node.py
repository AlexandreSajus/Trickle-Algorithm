#Experimental version, to be tested/commented

from random import random, randint, uniform
import numpy as np


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

    def send_message(self, ite, ordre, neighbors, code=False):
        # Sends a message with the current version to neighbouring nodes
        for recipient in neighbors[self.id_number]:
            recipient.messages.append(
                [self.id_number, self.ld, self.md, ite, ordre, code])

    def act_2(self, apres_tau, arg_min, ite, ordre, neighbors):
       # check if any version received in messages is different from the current one
        version_change = True
        # le noeud a reçu ses messages AVANT de regarder ce qu'il fait.
        for l in range(len(self.messages)-1, -1, -1):
            message = self.messages[l]
            # check the messages, if the current version is lower, update; if it is higher, send it to neighbouring nodes
            if message[3] != ite or message[4] != ordre:
                self.messages.pop(l)
                if self.check_version(message, 0) == 0:
                    self.c += 1
                elif self.check_version(message, 0) == -1:
                    version_change = False
                    self.send_message(ite, ordre, neighbors, True)
                elif self.check_version(message, 0) == 1 and message[5] == True:
                    version_change = False
                    for k in range(n_fragments):
                        self.ld[k] = message[1][k]
                        self.md[k] = message[2][k]
                elif self.check_version(message, 0) == 1 and message[5] == False:
                    version_change = False
                    self.send_message(ite, ordre, neighbors, False)

        if self.c < self.k and apres_tau == False and self == arg_min:
            # if c < k, send our version to neighbouring
            self.send_message(ite, ordre, neighbors, False)

        if apres_tau == True and arg_min == self and ordre == 0:
            if version_change == True:
                # if a version was different, extend i
                self.i = self.i*2
            else:
                # if not, reset i and c
                self.i = self.i_min
                self.c = 0
            self.tau = uniform(self.i/2, self.i)
            self.t = 0


def tourne(nodes, neighbors, T_max):
    '''Fait tourner le réseau pendant T_max'''
    T_tot = 0  # Durée totale de l'expérience
    non_tau = []  # à ne pas refaire agire, initialiser
    non_i = []  # à ne pas refaire agire, initialiser
    duree_min = np.inf  # durée minimale avant la prochaine action, initialiser
    ite = 0
    while T_tot < T_max:
        avant_tau = []
        avant_i = []
        for node in nodes:
            duree_tau = node.tau - node.t
            duree_i = node.i - node.t
            if duree_tau >= 0:
                avant_tau.append([node, duree_tau])
            avant_i.append([node, duree_i])
        arg_min = None
        duree_min = np.inf
        apres_tau = False
        for elem in avant_tau:  # trouver le noeud qui va agir en prochain. Est-ce en arrivant à tau?
            if elem[1] < duree_min:
                if not elem[0] in non_tau:
                    duree_min = elem[1]
                    arg_min = elem[0]
        for elem in avant_i:  # trouver le noeud qui va agir en prochain. Est-ce en arrivant à i?
            if elem[1] < duree_min:
                if not elem[0] in non_i:
                    duree_min = elem[1]
                    arg_min = elem[0]
                    apres_tau = True
        if duree_min > 0:  # Si on a bougé en temps depuis la dernière fois, on peut refaire agir les noeuds ayant agi la dernière fois
            non_tau = []
            non_i = []
        for node in nodes:
            node.t = node.t + duree_min  # le temps avance de durée_min
        T_tot = T_tot + duree_min  # le temps avance de durée min
        file = [[arg_min, 0]]
        while len(file) > 0:
            noeud = file[0][0]
            ordre = file.pop(0)[1]
            noeud.act_2(apres_tau, arg_min, ite, ordre, neighbors)
            for vois in neighbors[noeud.id_number]:
                if len(vois.messages) > 0:
                    file.append([vois, ordre + 1])
        if apres_tau == False:
            # ne pas refaire agir ce noeud tant qu'on a pas changé d'instant
            non_tau.append(arg_min)
        else:
            # ne pas refaire agir ce noeud tant qu'on a pas changé d'instant
            non_i.append(arg_min)
        nouvelle_trace = []
        for node in nodes:
            nouvelle_trace.append(
                [node.id_number, node.i, node.tau, node.t, node.md, node.c])
        ite = ite + 1
        print(nouvelle_trace)
    return nodes


def tourne_pas_a_pas(liste):
    '''liste = [nodes,neighbors,non_tau,non_i,ite] ou seulement [nodes,neighbors] pour initialiser'''
    duree_min = np.inf  # durée minimale avant la prochaine action, initialiser
    avant_tau = []
    avant_i = []
    if len(liste) < 5:
        liste = [liste[0], liste[1], [], [], 0]
    nodes = liste[0]
    non_tau = liste[2]
    non_i = liste[3]
    ite = liste[4]
    neighbors = liste[1]
    for node in nodes:
        duree_tau = node.tau - node.t
        duree_i = node.i - node.t
        if duree_tau >= 0:
            avant_tau.append([node, duree_tau])
        avant_i.append([node, duree_i])
    arg_min = None
    duree_min = np.inf
    apres_tau = False
    for elem in avant_tau:  # trouver le noeud qui va agir en prochain. Est-ce en arrivant à tau?
        if elem[1] < duree_min:
            if not elem[0] in non_tau:
                duree_min = elem[1]
                arg_min = elem[0]
    for elem in avant_i:  # trouver le noeud qui va agir en prochain. Est-ce en arrivant à i?
        if elem[1] < duree_min:
            if not elem[0] in non_i:
                duree_min = elem[1]
                arg_min = elem[0]
                apres_tau = True
    if duree_min > 0:  # Si on a bougé en temps depuis la dernière fois, on peut refaire agir les noeuds ayant agi la dernière fois
        non_tau = []
        non_i = []
    for node in nodes:
        node.t = node.t + duree_min  # le temps avance de durée_min
    file = [[arg_min, 0]]
    while len(file) > 0:
        noeud = file[0][0]
        ordre = file.pop(0)[1]
        noeud.act_2(apres_tau, arg_min, ite, ordre, neighbors)
        for vois in neighbors[noeud.id_number]:
            if len(vois.messages) > 0:
                file.append([vois, ordre + 1])
    if apres_tau == False:
        non_tau.append(arg_min)
    else:
        non_i.append(arg_min)
    ite = ite + 1
    return [nodes, neighbors, non_tau, non_i, ite]


if __name__ == "__main__":

    A = Node(0, 1, 5, 10, 1, random()*1/2 + 1/2, 0, [],
             ["code_fragment_1_version_2", "code_fragment_2_version_2"], [True, True])
    B = Node(1, 1, 5, 10, 1, random()*1/2 + 1/2, 0, [],
             ["code_fragment_1_version_1", "code_fragment_2_version_1"], [False, False])
    C = Node(2, 1, 5, 10, 1, random()*1/2 + 1/2, 0, [],
             ["code_fragment_1_version_1", "code_fragment_2_version_1"], [False, False])
    D = Node(3, 1, 5, 10, 1, random()*1/2 + 1/2, 0, [],
             ["code_fragment_1_version_1", "code_fragment_2_version_1"], [False, False])
    E = Node(4, 1, 5, 10, 1, random()*1/2 + 1/2, 0, [],
             ["code_fragment_1_version_1", "code_fragment_2_version_1"], [False, False])
    neighbors = {0: [B, D], 1: [D, E], 2: [E, A], 3: [E, C], 4: [A, B]}
    nodes = [A, B, C, D, E]
    n_fragments = 2
    print(tourne_pas_a_pas(tourne_pas_a_pas([nodes, neighbors]))[0][3].md)
