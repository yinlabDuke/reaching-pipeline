import nex
import helper
import pandas as pd

def post_bsoid(f):
    bsoid_file = f
    i1 = bsoid_file.index('bsoid')  - len(bsoid_file)
    i2 = bsoid_file.index("pose") + 10
    ne_file = bsoid_file[0:i1] + 'neuroexplorer/' + bsoid_file[i2:-4] + '.nex5'
    print(ne_file)

    df = pd.read_csv(bsoid_file, skiprows=[1, 2])
    labels = df["B-SOiD labels"].tolist()


    doc = nex.OpenDocument(ne_file)
    frameTimes = doc["frameTimes"].Timestamps()

    print(len(frameTimes), len(labels))
    doc['bsoid_labels'] = nex.NewContVarWithFloats(doc, 100) 
    doc['bsoid_labels'].SetContVarTimestampsAndValues(frameTimes, labels)
    nex.SaveDocument(doc)   
    nex.CloseDocument(doc)

if __name__ == '__main__':
    bsoid_files = helper.search_for_file_path(titles="Upload all BSOID files to analyze")

    for f in bsoid_files:
        post_bsoid(f)

# Yin Lab
# Stanley Park
# Last updated Sep 25 2022