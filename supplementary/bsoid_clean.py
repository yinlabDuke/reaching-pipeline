import pandas as pd 
from supplementary import helper
import matplotlib.pyplot as plt

'''
Cleans up bsoid data 
* Removes jitters
* Replaces redundant labels 
'''

def durations(labels):
    durations = []
    prev = -1
    cnt = 0
    first = True
    for n, l in enumerate(labels):
        if first: 
            prev = l
            cnt = 1
            first = False
        
        elif l != prev:
            durations.append(cnt)
            prev = l
            cnt = 1
        
        else:
            cnt += 1
        
    data = plt.hist(durations, bins=200)
    print(data)
    plt.show()

def process(labels):
    prev = -1
    prev2 = -1
    cnt = 0
    first = True

    # keys = sub.keys()
    # print(keys)
    # labels = [sub[i] if i in keys else i for i in labels]

    for n, l in enumerate(labels):
        if first: 
            prev = l
            prev = -1
            cnt = 1
            first = False
        
        elif l != prev:
            if (l == prev2): # and cnt < threshold
                for i in range(cnt):
                    i += 1
                    labels[n-i] = l
                first = True

            prev2 = prev 
            prev = l
            cnt = 1
        
        else:
            cnt += 1
    
    return labels

if __name__ == "__main__":
    bsoid_file = helper.search_for_file_path(titles="Upload the bsoid file for processing")[0]
    labels = pd.read_csv(bsoid_file, skiprows = [1, 2])["B-SOiD labels"].tolist()
    process(labels, 4)
    # durations(labels)





