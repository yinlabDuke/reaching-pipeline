import networkx as nx
import matplotlib.pyplot as plt
from supplementary import helper
import pandas as pd 
import networkx.algorithms.community as nx_comm
import nex 
from supplementary import bsoid_clean as bc

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
    next_nodes = [int(i) for i in freq.index.tolist()]
    weights = [round(i, 3)*5 for i in freq.values if i > 0.10]

    for i in range(len(weights)):
        edges.append((group, next_nodes[i], weights[i]))
    
    return edges

def bsoid_graph(file, userfeedback=True):
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
    # print(df["B-SOiD labels"].value_counts(normalize=True))
    durations = df["B-SOiD labels"].value_counts(normalize=True).sort_index().values
    durations = [i * 3000 for i in durations]
    g_durations = [durations[i] for i in nodelist]
    nx.draw_networkx_nodes(DG, pos, nodelist=nodelist, node_size = g_durations)
    nx.draw_networkx_edges(DG, pos, edgelist=thickness.keys(), width=list(thickness.values()))
    nx.draw_networkx_labels(DG, pos=pos, labels=dict(zip(nodelist, nodelist)))

    clustering = nx_comm.louvain_communities(DG, seed=123)
    clustering=[{0, 2, 9, 5, 1, 6}, {3, 4}, {8, 7, 10}, {11}]
    
    if userfeedback:
        print(clustering)
        plt.show()

    if userfeedback:
        feedback = int(input("Are you happy with the clustering? 1 for yes, 0 for no.\n"))
    else:
        feedback = True

    if (feedback):
        node_sub = {}
        for i, v in enumerate(clustering):
            for j in v:
                node_sub[int(j)] = i

    ne_file = helper.trimFileName(file, former="D151", latter="Delay", ext=".nex5")
    
    try:
        doc = nex.OpenDocument(ne_file)
    except:
        print(ne_file)
        print("NE file could not be found. Upload manually.")
        ne_file = helper.search_for_file_path()[0]
        doc = nex.OpenDocument(ne_file)
    
    bsoid_labels = doc["bsoid_labels"].ContinuousValues()
    bsoid_labels = [int(i) for i in bsoid_labels]

    for i, v in enumerate(bsoid_labels):
        bsoid_labels[i] = node_sub[v]

    bsoid_labels = bc.process(bsoid_labels)
    doc["bsoid_labels"].SetContVarTimestampsAndValues(doc["frameTimes"].Timestamps(), bsoid_labels)
    nex.SaveDocument(doc)
    nex.CloseDocument(doc)

if __name__ == "__main__":
    files = helper.search_for_file_path(titles="Upload BSOiD file", filetypes=[("bsoid file", "*.csv")], dir=r"D:/")
    for i in helper.progressbar(range(len(files))):
        f = files[i]
        bsoid_graph(f, userfeedback=False)