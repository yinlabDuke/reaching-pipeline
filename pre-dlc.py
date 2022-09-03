import helper
import videoProcessing as vp
import setupNE
import nex

NE = helper.search_for_file_path(titles="Select all the neuroexplorer files corresponding to the videos you want to analyze. Ensure you have split all the markers.")
vids = []
for i in NE:
    i = i.replace('neuroexplorer', 'videos')
    vids.append(i[0:-4] + "mp4")


for n, v in zip(NE, vids):
    doc = nex.OpenDocument(n)
    setupNE.setupNE(doc)
    vp.videoProcessing(v, doc)
    nex.CloseDocument(doc)