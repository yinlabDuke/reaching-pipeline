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

def group_transition(file, dir, ne_feedback):
    try:
        doc = nex.OpenDocument(file)
    except:
        print(file)
        print("Either NE is not open or the file does not exist. Manually upload.")
        helper.search_for_file_path()

    # Read file and extract list of labels for all frames
    all_groups = [int(i) for i in doc["bsoid_labels"].ContinuousValues()]
    unique_groups = set(all_groups)
    frameTimes = doc["frameTimes"].Timestamps()

    for g in unique_groups:
        initial = []
        final = []
        next = []

        # Identify all transition frames 
        check = False               
        for i in range(len(all_groups)):
            cur = all_groups[i]

            if (not check):
                if cur == g:
                    initial.append(i)
                    check = True
                
            else:
                if cur != g:
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

        dir_temp = dir + "/group" + str(g)
        try:
            os.mkdir(dir_temp)
        except:
            pass

        for g2 in set(d["next_group"]):
            name = str(g) + "to" + str(g2)
            df_temp = df_transition[df_transition["next_group"] == g2]
            df_temp.to_csv(dir_temp + "/group" + name + ".csv", index=False)

            if ne_feedback:
                
                doc[name] = nex.NewEvent(doc, 0)
                doc[name].SetTimestamps(df_temp["final"].tolist())
                nex.SaveDocument(doc)
        
    nex.CloseDocument(doc)


if __name__ == "__main__":
    files = helper.search_for_file_path(titles="Upload all the NE files you want to find transition times for.", filetypes=[("nex5", "*.nex5")], dir=r"D:/")
    dir = helper.trimFileName(files[0], latter="neuroexplorer").replace("neuroexplorer", "bsoid/") + "group_transitions"
    try:
        os.mkdir(dir)
    except:
        pass
    
    for i in helper.progressbar(range(len(files))):
        f = files[i]
        dir2 = dir + helper.trimFileName(f, former="neuroexplorer")[13:-5] + "/"

        try:
            os.mkdir(dir2)
        except:
            pass

        group_transition(f, dir2, ne_feedback=True)



