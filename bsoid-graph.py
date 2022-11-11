import networkx as nx
import matplotlib.pyplot as plt
from supplementary import helper
import pandas as pd 

def group_transition(all_groups, group):
    # Read file and extract list of labels for all frames

    
    initial = []
    final = []
    next = []

    # Identify all transition frames 
    check = False               
    for i in range(len(all_groups)):
        cur = all_groups[i]

        if (not check):
            if cur == group:
                initial.append(i)
                check = True
            
        else:
            if cur != group:
                final.append(i - 1)
                next.append(all_groups[i])
                check = False
            
            if i == len(all_groups) - 1:
                final.append(i)
                next.append(None)
    
    # Create data frame of initial and final frames of label, and next label
    d = {'initial': initial, 'final': final, 'next_group' : next}
    df_transition = pd.DataFrame(data=d)

    # Calculate frequencies of next labels 
    freq = df_transition["next_group"].value_counts(normalize = True)
    
    edges = []
    next_nodes = freq.index.tolist()
    weights = [round(i, 3)*5 for i in freq.values if i > 0.1]

    for i in range(len(weights)):
        edges.append((group, next_nodes[i], weights[i]))
    
    return edges

def bsoid_graph(file):
    DG = nx.DiGraph()

    df = pd.read_csv(file)
    all_groups = df["B-SOiD labels"].tolist()
    unique_groups = set(all_groups)
    for g in unique_groups:
        edges = group_transition(all_groups, g)
        DG.add_weighted_edges_from(edges)
    
    nodelist = DG.nodes()
    pos = nx.spring_layout(DG)
    thickness = nx.get_edge_attributes(DG, "weight")
    print(df["B-SOiD labels"].value_counts(normalize=True))
    durations = df["B-SOiD labels"].value_counts(normalize=True).sort_index().values
    durations = [i * 3000 for i in durations]
    g_durations = [durations[i] for i in nodelist]
    nx.draw_networkx_nodes(DG, pos, nodelist=nodelist, node_size = g_durations)
    nx.draw_networkx_edges(DG, pos, edgelist=thickness.keys(), width=list(thickness.values()))
    nx.draw_networkx_labels(DG, pos=pos, labels=dict(zip(nodelist, nodelist)))

    plt.show()

   

if __name__ == "__main__":
    file = helper.search_for_file_path(titles="Upload BSOiD file", filetypes=[("bsoid file", "*.csv")], dir=r"D:/")[0]
    bsoid_graph(file)