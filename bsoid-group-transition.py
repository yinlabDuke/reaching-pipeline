# ===================================================================================
# SUMMARY OF CODE
# Identifies the initial and final frame of contiguous frames of the given
# label and the next transition label. The frequencies of the next transition
# label is also given.

# PROCEDURE
# Modify the FILE to be the path of the file you wish to analyze. The DEST 
# is where the result will be stored in. The frequencies of the next transition
# label will be printed. You can also change the name of the file. 
# In the terminal, change the directory to where the program is located and enter
# "python group_transition.py". 
# ===================================================================================

import pandas as pd 
import os
from supplementary import helper
import nex 

def group_transition(file, dir, group):
    # Read file and extract list of labels for all frames
    df = pd.read_csv(file, skiprows=[1, 2])
    all_groups = df["B-SOiD labels"].tolist()

    i = file.index("labels_pose") + 17
    j = file.index('Delay') + 5
    ne_filename = file[i:j] + ".nex5"
    ne_dir = file.replace("bsoid/processed-files", "neuroexplorer")
    ne_dir = ne_dir[0: ne_dir.index("neuroexplorer") + 14]
    ne_file = ne_dir + ne_filename
    try:
        doc = nex.OpenDocument(ne_file)
    except:
        print(ne_file)
        print("Could not find file. Please manually upload.")
        doc = nex.OpenDocument(helper.search_for_file_path()[0])
    frameTimes = doc["frameTimes"].Timestamps()

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

    initial = [frameTimes[i] for i in initial]
    final = [frameTimes[i] for i in final]
    
    # Create data frame of initial and final frames of label, and next label
    d = {'initial': initial, 'final': final, 'next_group' : next}
    df_transition = pd.DataFrame(data=d)

    # Calculate frequencies of next labels 
    freq = df_transition["next_group"].value_counts(normalize = True)
    print(freq)

    dir = dir + "/group" + str(group)
    try:
        os.mkdir(dir)
    except:
        print("The directory already exists.\n")

    for g in set(d["next_group"]):
        df_temp = df_transition[df_transition["next_group"] == g]
        df_temp.to_csv(dir + "/group" + str(group) + "to" + str(g) + ".csv", index=False)


if __name__ == "__main__":
    files = helper.search_for_file_path(titles="Upload all the bsoid files you want to find transition times for.", filetypes=[("csv", "*.csv")], dir=r"D:/")
    
    try:
        group = int(input("Enter the preceding group that you want the transition times for.\n"))
    except:
        print("Please enter an integer.\n")
    for i in helper.progressbar(range(len(files))):
        f = files[i]
        dir = f[0: f.index("bsoid")+5] + "/transitions/" + f[f.index("bsoid")+21: -4]
        try:
            os.mkdir(dir)
        except:
            print("Directory already exists. Using existing directory.")
        group_transition(f, dir, group)



