import helper
import nex
import pandas as pd

dlc_file = helper.search_for_file_path(titles="Upload the DLC file.", filetypes=[('dlc', '*.csv')])[0]

ne_file = dlc_file
i = dlc_file.index('_modified') - len(dlc_file) 
ne_file = (ne_file[0:i] + '.nev').replace('videos', 'neuroexplorer')
            
try:
        doc = nex.OpenDocument(ne_file)
except:
        print(ne_file)
        print("Do you have NeuroExplorer open? If yes, NE document doesn't exist. Check to make sure the file is in the correct location. Processing rest of the videos.")



reachesNoStim = doc["reachesNoStim"].Timestamps()
timestamps = [round(i * 100, 0) + 2 for i in reachesNoStim]
final_timestamps = []

for t in timestamps:
    final_timestamps.append(list(range(t-60, t+60)))

df = pd.read_csv(dlc_file, skiprows=lambda x: x not in final_timestamps)
df.to_csv()