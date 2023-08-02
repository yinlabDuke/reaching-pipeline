import networkx as nx
import matplotlib.pyplot as plt
from supplementary import helper
import pandas as pd 
import networkx.algorithms.community as nx_comm
import nex 
from supplementary import bsoid_clean as bc
import numpy as np
import math
from bsoid_graph_node import bsoid_node
import seaborn as sns

'''
Input: bsoid labels and group to find transition time from 
Output: weighted edges from input group to all posible next group 
'''
def group_transition(all_groups, group, weight=False):
    # Read file and extract list of labels for all frames
    initial = []
    final = []
    next = []

    # Identify initial and final frametimes of every group
    check = False               
    for i, v in enumerate(all_groups):
        cur = v
        if (not check):
            if cur == group:
                initial.append(i)
                check = True
            
        else:
            if cur != group:
                final.append(i - 1)
                next.append(v)
                check = False
            
            if i == len(all_groups) - 1:
                final.append(i)
                next.append(None)
     
    # Create data frame of initial and final frames of label, and next label
    d = {'initial': initial, 'final': final, 'next_group' : next}
    df_transition = pd.DataFrame(data=d)

    # Calculate frequencies of next labels 
    freq = df_transition["next_group"].value_counts(normalize = True)
    abs_freq = df_transition["next_group"].value_counts()
    
    # Create weighted edges and return 
    edges = []
    next_nodes = [int(i) for i in freq.index.tolist()]
    weights = freq.values

    for i in range(len(weights)):
        if weights[i] < .1:
            continue
        if weight:
            weights = abs_freq.values
            edges.append((group, next_nodes[i], weights[i]))
        else:
            edges.append((group, next_nodes[i]))
    
    return edges

def create_graph(bsoid_labels, plot=True):
    G = nx.DiGraph()
    # G = nx.Graph()

    # Add edges to graph
    unique_groups = set(bsoid_labels)
    for g in unique_groups:
        edges = group_transition(bsoid_labels, g)
        # G.add_weighted_edges_from(edges)
        # print(edges)
        G.add_edges_from(edges)

    # Plot graph 
    if plot:
        nodelist = G.nodes()
        pos = nx.spring_layout(G)
        # thickness = nx.get_edge_attributes(DG, "weight")
        # print(df["B-SOiD labels"].value_counts(normalize=True))
        # durations = df["B-SOiD labels"].value_counts(normalize=True).sort_index().values
        # durations_index = df["B-SOiD labels"].value_counts(normalize=True).sort_index().index.tolist()
        # durations = [i * 3000 for i in durations]
        # g_durations = [durations[durations_index.index(i)] for i in nodelist]
        nx.draw_networkx_nodes(G, pos, nodelist=nodelist)
        nx.draw_networkx_edges(G, pos)
        # nx.draw_networkx_edges(G, pos, edgelist=thickness.keys(), width=list(thickness.values()))
        nx.draw_networkx_labels(G, pos=pos, labels=dict(zip(nodelist, nodelist)))
        plt.show()

    return G 

def substitute(labels, clustering):
    node_sub = {}
    for i, v in enumerate(clustering):
        for j in v:
            node_sub[int(j)] = i

    temp = labels.copy()
    for i, v in enumerate(labels):
        temp[i] = node_sub[v]
    return temp

def scatter_plot(cycles):
    y = []
    for k in cycles.keys():   
        y.append(len(cycles[k]))
    plt.plot(list(cycles.keys()), y)
    plt.show()

def louvain_evaluation(G, cycles):
    cycle_len = []
    for c in cycles:
        sum = 0
        for i in range(len(c)):
            if i != len(c)-1:
                sum += G.get_edge_data(c[i], c[i+1])["weight"]
            else:
                sum += G.get_edge_data(c[i], c[0])["weight"]
        cycle_len.append(sum)
    return cycle_len

def louvain_eval_vel(cycles, vp):
    profile = list(range(len(cycles)))
    for i in range(len(profile)):
        profile[i] = bsoid_node()
    for i, c in enumerate(cycles):
        for j in c:
            curr = vp[j-1]
            try:
                profile[i].hand_v.append(curr.hand_v)
                profile[i].nose_v.append(curr.nose_v)
            except:
                pass
    
    for obj in profile:
        obj.average()

    return profile

def double_bar(clustering, bsoid_labels, vp):
    unique = set(bsoid_labels)
    cycle_no = list(range(len(unique)))
    for i, c in enumerate(clustering):
        for j in c:
            cycle_no[j-1] = i
    
    node_name = []
    hand_v = []
    hand_l = []
    nose_v = []
    nose_l = []
    for i in range(len(unique)):
        hand_v.append(vp[i].hand_v)
        nose_v.append(vp[i].nose_v)
        hand_l.append("hand")
        nose_l.append("nose")
        i += 1
        node_name.append(i)
    
    vel = hand_v + nose_v
    body = hand_l + nose_l
    node_name = node_name + node_name
    cycle_no = cycle_no + cycle_no
    
    d1 = {"node": node_name, "vel": vel, "body": body, "cycle": cycle_no}
    df = pd.DataFrame(d1)
    ax = sns.barplot(
        data=df,
        x="cycle",
        y="vel",
        hue="body",
        alpha=.7,
        errorbar=None
        )
    
        # Get the legend from just the bar chart
    handles, labels = ax.get_legend_handles_labels()

    # Draw the stripplot
    sns.stripplot(
        data=df, 
        x="cycle", 
        y="vel", 
        hue="body", 
        dodge=True, 
        edgecolor="black", 
        linewidth=.75,
        ax=ax,
    )
    # Remove the old legend
    ax.legend_.remove()
    # Add just the bar chart legend back
    ax.legend(
        handles,
        labels,
        loc=7,
        bbox_to_anchor=(1.25, .5),
    )

    plt.show()


# Louvain clustering 
def louvain(G, bsoid_labels, vp):
    cycles_tot = {}
    for theta in np.arange(0.3, 1.5, 0.05):
        gamma = math.tan(theta)
        clustering = nx_comm.louvain_communities(G, resolution=gamma)
        if len(clustering) > 8:
            break
    
    # Create temporary graph with nodes substituted 
        G_temp = nx.DiGraph()
        temp = substitute(bsoid_labels, clustering)
        unique = set(temp)

        for g in unique:
            edges = group_transition(temp, g, weight=True)
            G_temp.add_weighted_edges_from(edges)
        cycles = sorted(nx.simple_cycles(G_temp))

        cycles_tot[gamma] = cycles

        print(clustering)
        double_bar(clustering, bsoid_labels, vp)


    # scatter_plot(cycles_tot)
    return clustering

# Open NE file
def OpenNE(file):
    dir = helper.trimFileName(file, latter="bsoid").replace("bsoid", "neuroexplorer/")
    ne_file = dir + helper.trimFileName(file, former="Hz")[2:-14] + ".nex5"
    print(ne_file)
    try:
        doc = nex.OpenDocument(ne_file)
    except:
        print(ne_file)
        print("NE file could not be found. Upload manually.")
        ne_file = helper.search_for_file_path()[0]
        doc = nex.OpenDocument(ne_file)
    return doc

def vel_profile(bsoid_labels, doc):
    unique = set(bsoid_labels)
    vel_profile = list(range(len(unique)))
    for i in unique:
        vel_profile[i] = bsoid_node()

    hand_v = doc["handX_vel"].ContinuousValues()
    nose_v = doc["noseX_vel"].ContinuousValues()
    for i, v in enumerate(bsoid_labels):
        curr = vel_profile[v]
        if not math.isnan(hand_v[i]):
            curr.hand.append(hand_v[i])
        
        if not math.isnan(nose_v[i]):
            curr.nose.append(nose_v[i])

    for obj in vel_profile:
        obj.average()

    return vel_profile

def bsoid_group_character(vp):
    x = []
    y_hand = []
    y_nose = []
    y_hand_sd = []
    y_nose_sd = []
    durations = []
    fix, axes = plt.subplots(3)
    for i, v in enumerate(vp):
        if i == 0: continue
        x.append(i)
        y_hand.append(vp[i].hand_v)
        y_hand_sd.append(vp[i].hand_sd)
        y_nose.append(vp[i].nose_v)   
        y_nose_sd.append(vp[i].nose_sd)
        durations.append(len(vp[i].hand))
    x_axis = np.arange(len(x))
    print(durations)
    y = np.subtract(np.array(y_hand), np.array(y_nose))
    axes[1].bar(x_axis, y)
    axes[1].set_xticks(x_axis, x)
    axes[0].bar(x_axis -.2, y_hand, .4, yerr=y_hand_sd, label="hand")
    axes[0].bar(x_axis +.2, y_nose, .4, yerr=y_nose_sd, label="nose")
    axes[0].set_xticks(x_axis, x)
    axes[2].bar(x_axis, durations)
    axes[2].set_xticks(x_axis, x)
    plt.legend()
    plt.show()


def bsoid_reduce(file, userfeedback=True):
    doc = OpenNE(file)
    bsoid_labels = [int(i) for i in doc["bsoid_labels"].ContinuousValues()]
    G = create_graph(bsoid_labels, plot=True)
    vp = vel_profile(bsoid_labels, doc)
    bsoid_group_character(vp)
    # clustering = louvain(G, bsoid_labels, vp)

    # if userfeedback:
    #     feedback = int(input("Are you happy with the clustering? 1 for yes, 0 for no.\n"))
    # else:
    #     feedback = True

    # if (feedback):
    #     node_sub = {}
    #     for i, v in enumerate(clustering):
    #         for j in v:
    #             node_sub[int(j)] = i
    # else:   
    #     return

    # bsoid_labels_reduced = bsoid_labels.copy()
    # for i, v in enumerate(bsoid_labels):
    #     bsoid_labels_reduced[i] = node_sub[v]

    # bsoid_labels_reduced = bc.process(bsoid_labels_reduced)

    # doc["bsoid_labels_reduced"] = nex.NewContVarWithFloats(doc, 1/100)
    # doc["bsoid_labels_reduced"].SetContVarTimestampsAndValues(doc["frameTimes"].Timestamps(), bsoid_labels)
    # nex.SaveDocument(doc)
    # nex.CloseDocument(doc)

if __name__ == "__main__":
    files = helper.search_for_file_path(titles="Upload BSOiD file", filetypes=[("bsoid file", "*.csv")], dir=r"D:/")
    for i in helper.progressbar(range(len(files))):
        f = files[i]
        bsoid_reduce(f, userfeedback=True)
