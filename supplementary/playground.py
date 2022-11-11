import networkx as nx
import matplotlib.pyplot as plt 

G = nx.DiGraph()

G.add_nodes_from([(1, {'color': 'red'})])
G.add_nodes_from([2, 3])
G.add_edge(3, 2, weight=2)
pos=nx.spring_layout(G)
nx.draw_networkx(G, pos)
labels = nx.get_edge_attributes(G, 'weight')

nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

plt.show()


