# Create an animation using matplotlib and networkx illustrating the evolving graph

from node import Node, next_step
from time import time
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


def create_simple_graph(n_nodes, neighbor_p, updated_p):
    nodes = []
    for i in range(n_nodes):
        version = False
        if random() < updated_p:
            version = True
        nodes.append(Node(i, 1, 2, randint(1, 3), 1, random()*1/2 + 1/2, 0, [],
                          ["code_fragment_1_version_2", "code_fragment_2_version_2"], [version, version]))

    neighbors = {}
    for i in range(n_nodes):
        neighbor_list = []
        for j in range(n_nodes):
            if i != j and random() < neighbor_p:
                neighbor_list.append(nodes[j])
        neighbors[i] = neighbor_list

    return nodes, neighbors


# Creates a graph with 40 nodes
nodes, neighbors = create_simple_graph(40, 0.04, 0.3)


# For the tourne_pas_a_pas function
non_tau = []
non_i = []

# Create a figure
fig, ax = plt.subplots(figsize=(6, 4))


def animate_nodes(nodes):

    # Creates an empty directed graph
    DG = nx.DiGraph()

    # Add the nodes
    node_list = []
    edge_list = []
    for node in nodes:
        node_list.append(node)
        for neighbour in neighbors[node.id_number]:
            edge_list.append((node, neighbour))
    DG.add_nodes_from(node_list)
    DG.add_edges_from(edge_list)

    # Position layout
    pos = nx.circular_layout(DG)

    # Update function
    def update(i):
        global nodes, non_tau, non_i
        # Execute a step of the simulation
        nodes, non_tau, non_i = next_step(neighbors, nodes, non_tau, non_i)

        ax.clear()
        ax.set_title(
            "Trickle Algorithm (red = up-to-date, blue = out-of-date, red arrow = message sent)")

        node_list_red = []  # Nodes with updated version
        node_list_blue = []  # Outdated nodes
        edge_list = []  # Edges
        edge_list_red = []  # Edges where a message has been sent
        labels = {}  # Labels on the nodes

        for node in nodes:
            # Separating red and blue nodes
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
            DG, pos, ax=ax, nodelist=node_list_blue, node_size=300, node_color="b")
        nx.draw_networkx_nodes(
            DG, pos, ax=ax, nodelist=node_list_red, node_size=300, node_color="r")
        nx.draw_networkx_edges(DG, pos, ax=ax, edgelist=edge_list,
                               width=1.5, alpha=1, edge_color="b", arrowsize=20)
        nx.draw_networkx_edges(DG, pos, ax=ax, edgelist=edge_list_red,
                               width=1.5, alpha=1, edge_color="r", arrowsize=20)
        nx.draw_networkx_labels(DG, pos, ax=ax, labels=labels, font_size=8)
        ax.text(0.6, 1, "up-to-date nodes: " +
                str(len(node_list_red)) + "/" + str(len(node_list)))

    # Initialize the nodes, edges and labels
    update(0)

    # Matplotlib animation function
    animation = FuncAnimation(fig, update, interval=1,
                              frames=1000)
    return animation


# Animate and show
animation = animate_nodes(nodes)
plt.show()
