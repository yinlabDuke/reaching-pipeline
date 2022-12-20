import nex
from supplementary import helper
import pandas as pd
from supplementary import bsoid_clean as bc

'''
Cleans up bsoid file and imports into NeuroExplorer
'''

def post_bsoid(f):
    bsoid_file = f
    ne_dir = helper.trimFileName(f, latter="processed-file").replace("bsoid/processed-file", "neuroexplorer/")
    ne_file = helper.trimFileName(f, former="Hz", ext=".nex5")[2:]
    ne_file = ne_dir + ne_file

    df = pd.read_csv(bsoid_file, skiprows=[1, 2])
    labels = df["B-SOiD labels"].tolist()
    labels = bc.process(labels)
    labels = bc.process(labels)
    df2 = pd.DataFrame({"B-SOiD labels": labels}) 
    df2.to_csv(f[0:-4] + "_corrected.csv")

    doc = nex.OpenDocument(ne_file)
    frameTimes = doc["frameTimes"].Timestamps()

    doc['bsoid_labels'] = nex.NewContVarWithFloats(doc, 100) 
    try:
        doc['bsoid_labels'].SetContVarTimestampsAndValues(frameTimes, labels)
        print(labels)
    except:
        print("Length of bsoid labels and frametimes do not match.")
        print(len(labels), len(frameTimes))
        
    nex.SaveDocument(doc)   
    nex.CloseDocument(doc)

if __name__ == '__main__':
    bsoid_files = helper.search_for_file_path(titles="Upload all BSOID files to analyze", filetypes=[("csv", "*.csv")], dir=r"D:/")

    for i in helper.progressbar(range(len(bsoid_files))):
        f = bsoid_files[i]
        post_bsoid(f)

# Yin Lab
# Stanley Park
# Last updated Sep 25 2022