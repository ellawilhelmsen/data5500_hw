# Write a Python function that takes a NetworkX graph as input and returns the number of nodes in the graph.
import networkx as nx


def num_nodes(graph):
    return graph.number_of_nodes()


# code to test function
G = nx.Graph()
G.add_node(1)
G.add_node(3)
G.add_node(4)
G.add_node(19)
G.add_node(9)

print(num_nodes(G))