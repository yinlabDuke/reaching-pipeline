import nex
import helper

ne = helper.search_for_file_path()

for i in ne:
    doc = nex.OpenDocument(i)
    nex.CloseDocument(doc)