import nex
from supplementary import helper
import pandas as pd
from supplementary import bsoid_clean as bc

'''
Cleans up bsoid file and imports into NeuroExplorer
'''

def post_bsoid(f):
    bsoid_file = f
    i1 = bsoid_file.index('bsoid')  - len(bsoid_file)
    i2 = bsoid_file.index("pose") + 10
    i3 = bsoid_file.index("Delay") - len(bsoid_file) + 5
    # i3 = bsoid_file.index("0000") - len(bsoid_file) + 4
    ne_file = bsoid_file[0:i1] + 'neuroexplorer/' + bsoid_file[i2:i3] + '.nex5'

    df = pd.read_csv(bsoid_file, skiprows=[1, 2])
    labels = df["B-SOiD labels"].tolist()
    labels = bc.process(labels)
    labels = bc.process(labels)
    df2 = pd.DataFrame({"B-SOiD labels": labels})
    print(df2)
    df2.to_csv(f[0:-4] + "_corrected.csv")

    doc = nex.OpenDocument(ne_file)
    frameTimes = doc["frameTimes"].Timestamps()

    doc['bsoid_labels'] = nex.NewContVarWithFloats(doc, 100) 
    doc['bsoid_labels'].SetContVarTimestampsAndValues(frameTimes, labels)
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