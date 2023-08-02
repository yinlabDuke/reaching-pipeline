import nex
from supplementary import helper

ne = helper.search_for_file_path(dir=r"\D", titles="Upload all NeuroExplorer files", filetypes=[("nex5", "*.nex5"), ('nev', '*.nev')])

for i in ne:
    doc = nex.OpenDocument(i)
    nex.CloseDocument(doc)