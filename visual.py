# Create an animation using matplotlib and networkx illustrating the evolving graph

from alex_run import Node, tourne_pas_a_pas

from random import random, randint
from matplotlib.animation import FuncAnimation
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

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

non_tau = []
non_i = []


def animate_nodes(nodes):

    # Creates an empty directed graph
    DG = nx.DiGraph()

    # Add the nodes
    node_list = []
    for node in nodes:
        node_list.append(node)
    DG.add_nodes_from(node_list)

    # Position layout
    pos = nx.spring_layout(DG)

    # Update function
    def update(i):
        global nodes, non_tau, non_i
        # Execute a step of the simulation
        [nodes, non_tau, non_i] = tourne_pas_a_pas(
            [nodes, non_tau, non_i], neighbors)

        node_list_red = []  # Nodes with updated version
        node_list_blue = []  # Outdated nodes
        edge_list = []  # Edges
        edge_list_red = []  # Edges where a message has been sent
        labels = {}  # Labels on the nodes

        for node in nodes:
            # Separating red and blue nodes
            node_list.append(node)
            if node.md[0] == True:
                node_list_red.append(node)
            else:
                node_list_blue.append(node)

            # Separating red and blue edges
            for neighbour in neighbors[node.id_number]:
                edge_list.append((node, neighbour))
            for message in node.messages:
                edge_list_red.append((nodes[message[0]], node))

            # Creating labels
            labels[node] = str(node.id_number)

        # Draw nodes, edges and labels
        nx.draw_networkx_nodes(
            DG, pos, nodelist=node_list_blue, node_color="b")
        nx.draw_networkx_nodes(DG, pos, nodelist=node_list_red, node_color="r")
        nx.draw_networkx_edges(DG, pos, edgelist=edge_list,
                               width=2, alpha=1, edge_color="b")
        nx.draw_networkx_edges(DG, pos, edgelist=edge_list_red,
                               width=2, alpha=1, edge_color="r")
        nx.draw_networkx_labels(DG, pos, labels, font_size=16)

    # Initialize the nodes, edges and labels
    update(0)

    # Matplotlib animation function
    fig = plt.gcf()
    animation = FuncAnimation(fig, update, interval=1000,
                              frames=1000)
    return animation


#Animate and show
animation = animate_nodes(nodes)
plt.show()
