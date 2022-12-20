import networkx as nx
import matplotlib.pyplot as plt
from supplementary import helper
import pandas as pd 
import networkx.algorithms.community as nx_comm
import nex 
from supplementary import bsoid_clean as bc
import numpy as np
import math


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
    weights = [i * 5 for i in freq.values]

    for i in range(len(weights)):
        edges.append((group, next_nodes[i], weights[i]))
    
    return edges

def bsoid_graph(file, userfeedback=True, ne_feedback=True):
    DG = nx.DiGraph()

    dir = helper.trimFileName(file, latter="bsoid").replace("bsoid", "neuroexplorer/")
    ne_file = dir + helper.trimFileName(file, former="Hz")[2:-14] + ".nex5"

    
    try:
        doc = nex.OpenDocument(ne_file)
    except:
        print(ne_file)
        print("NE file could not be found. Upload manually.")
        ne_file = helper.search_for_file_path()[0]
        doc = nex.OpenDocument(ne_file)

    bsoid_labels = [int(i) for i in doc["bsoid_labels"].ContinuousValues()]
    unique_groups = set(bsoid_labels)
    for g in unique_groups:
        edges = group_transition(bsoid_labels, g)
        DG.add_weighted_edges_from(edges)
    
    nodelist = DG.nodes()
    pos = nx.spring_layout(DG)
    thickness = nx.get_edge_attributes(DG, "weight")
    # print(df["B-SOiD labels"].value_counts(normalize=True))
    # durations = df["B-SOiD labels"].value_counts(normalize=True).sort_index().values
    # durations_index = df["B-SOiD labels"].value_counts(normalize=True).sort_index().index.tolist()
    # durations = [i * 3000 for i in durations]
    # g_durations = [durations[durations_index.index(i)] for i in nodelist]
    nx.draw_networkx_nodes(DG, pos, nodelist=nodelist)
    nx.draw_networkx_edges(DG, pos, edgelist=thickness.keys(), width=list(thickness.values()))
    nx.draw_networkx_labels(DG, pos=pos, labels=dict(zip(nodelist, nodelist)))
    plt.show()


    for theta in np.arange(0.7, 1, 0.05):
        gamma = math.tan(theta)
        print(theta)
        clustering = nx_comm.louvain_communities(DG, resolution=gamma)
        print(clustering)

        DG_temp = nx.DiGraph()
        node_sub = {}
        for i, v in enumerate(clustering):
            for j in v:
                node_sub[int(j)] = i

        temp = bsoid_labels.copy()
        for i, v in enumerate(bsoid_labels):
            temp[i] = node_sub[v]
        
        unique = set(temp)
        for g in unique:
            edges = group_transition(temp, g)
            DG_temp.add_weighted_edges_from(edges)
        cycles = sorted(nx.simple_cycles(DG_temp))


        # max_c = 0
        # for c in cycles:
        #     sig = 0
        #     for i in range(len(c)):
        #         if i == len(c) - 1:
        #             sig += DG_temp.get_edge_data(c[i], c[0])['weight']
        #         else:
        #             sig += DG_temp.get_edge_data(c[i], c[i+1])['weight']0
        #     if max_c < sig:
        #         max_c = sig
            
        # print(gamma, ":", clustering)
    
    # m70
    # clustering = [{0, 35, 6, 7, 9, 21, 23, 28, 29}, {24, 1, 4, 15}, {2, 10, 11, 16, 17, 25, 26, 27}, {33, 5, 31}, {18, 19, 20, 8, 12, 14}, {3, 13, 22}]
    # m71
    clustering = [{0, 33, 34, 22, 24, 25, 26, 29}, {1, 4, 6, 7, 8, 12, 13}, {2, 35, 36, 37, 38, 39, 40, 41, 42, 43}, {3}, {16, 5, 9, 10, 11, 14, 15}, {32, 17, 20, 21, 23, 30, 31}, {27, 18, 19, 28}]
    # m72
    # clustering = [{0, 8, 10, 11, 20, 22, 23, 30, 31, 33, 36, 38, 39, 40, 43, 44, 45, 46, 47, 50, 51, 52, 53, 54}, {1, 2, 3, 5, 6, 7, 9, 12, 13, 14, 15, 16, 17, 18, 19, 26, 27, 28, 29, 32, 37, 41}, {24, 4}, {21}, {48, 49, 34, 35, 25, 42}]
        # print(clustering)
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


    for i, v in enumerate(bsoid_labels):
        
        bsoid_labels[i] = node_sub[v]

    bsoid_labels = bc.process(bsoid_labels)

    if ne_feedback:
        doc["bsoid_labels"].SetContVarTimestampsAndValues(doc["frameTimes"].Timestamps(), bsoid_labels)
        nex.SaveDocument(doc)
    nex.CloseDocument(doc)

if __name__ == "__main__":
    files = helper.search_for_file_path(titles="Upload BSOiD file", filetypes=[("bsoid file", "*.csv")], dir=r"D:/")
    for i in helper.progressbar(range(len(files))):
        f = files[i]
        bsoid_graph(f, userfeedback=True, ne_feedback=True)