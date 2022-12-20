from supplementary import helper
import nex
import pandas as pd
import os 

'''
Filters for relevant frames in dlc file before running bsoid
'''

def pre_bsoid(dlc_file, createVideo=False):
        ne_file = (dlc_file[0:-4] + '.nex5').replace('bsoid/raw', 'neuroexplorer')
                
        try:
                doc = nex.OpenDocument(ne_file)
        except:
                print(ne_file)
                print("Do you have NeuroExplorer open? If yes, NE document doesn't exist. Check to make sure the file is in the correct location. Processing rest of the videos.")

        frameTimes = doc["frameTimes"].Timestamps() 
        reachesNoStim = doc["reachesNoStim"].Timestamps()
        timestamps = [helper.findFrame(frameTimes, i) for i in reachesNoStim]
        final_timestamps = []

        for t in timestamps:
                final_timestamps += (list(range(t-60, t+60)))
        
        if createVideo:
                video_file = helper.trimFileName(ne_file.replace("neuroexplorer", "videos"), latter=".")[0:-1] + "_modified.mp4"
                helper.createVideo(video_file, final_timestamps)

        final_timestamps += [0, 1, 2]

        df = pd.read_csv(dlc_file, skiprows=lambda x: x not in final_timestamps)

        data_dir = helper.trimFileName(ne_file, latter="neuroexplorer").replace("neuroexplorer", "bsoid/data")
        try:
                os.mkdir(data_dir)
        except:
                pass
        
        bsoid_dir = ne_file.replace("neuroexplorer/", "bsoid/data/")[0:-5] + "_modified"
        i1 = bsoid_dir.index("data")
        filename = bsoid_dir[i1+4:] + ".csv"
        try:
                os.mkdir(bsoid_dir)
                df.to_csv(bsoid_dir + "/" + filename, index=False)
        except:
                df.to_csv(bsoid_dir + "/" + filename, index=False)
        nex.CloseDocument(doc)

if __name__ == "__main__":
         files = helper.search_for_file_path(titles="Upload the DLC file from bsoid/raw.", filetypes=[('dlc', '*.csv')], dir="D:/")
         for i in helper.progressbar(range(len(files))):
                f = files[i]
                pre_bsoid(f, createVideo=False)
