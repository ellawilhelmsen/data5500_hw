# Write a Python function that takes a NetworkX graph as input and returns the number of nodes in the graph that have a degree greater than 5

import networkx as nx

def num_nodes_abv_5(graph):
    count = 0
    for node in graph.nodes:
        if graph.degree(node) > 5:
            count += 1
    return count



# code to test function
G = nx.Graph()
G.add_edge(1,2)
G.add_edge(1,3)
G.add_edge(1,4)
G.add_edge(1,5)
G.add_edge(1,6)
G.add_edge(1,7)
G.add_edge(2,3)
G.add_edge(2,4)
G.add_edge(2,5)
G.add_edge(2,6)
G.add_edge(3,4)
G.add_edge(3,5)
G.add_edge(3,6)
G.add_edge(3,7)

print(num_nodes_abv_5(G))