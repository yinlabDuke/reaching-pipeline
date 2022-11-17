import cv2 
from supplementary import helper
import matplotlib.pyplot as plt
import numpy as np
import nex 
import pandas as pd 
import random

'''
Manually identify timestamps and record on NeuroExplorer
'''

name = "reachStart"

# Adjust starting point 
buffer = 40 

def findFrame(frameTimes, time):
    for i, v in enumerate(frameTimes):
        if v > time - 0.005 and v < time + 0.005:
            return i

print("Press D to move forward one frame. Press A to move back one frame. Press L to timestamp a lick. Press ESC to move onto the next session.\n")
ne_file = helper.search_for_file_path(titles="Upload the NeuroExplorer file you want to analyze.\n", filetypes=[("nex", "*.nex5")], dir="D:/")[0]
video_file = video_file = (ne_file[0:-5] + ".mp4").replace('neuroexplorer', 'videos')

try:
        doc = nex.OpenDocument(ne_file)
except:
        print(ne_file)
        print("Do you have NeuroExplorer open? If yes, NE document doesn't exist. Check to make sure the file is in the correct location.")

frameTimes = doc["frameTimesPrior"].Timestamps()
reachesDuringStim = doc["reachesDuringStim"].Timestamps()
reachesNoStim = doc["reachesNoStim"].Timestamps()
reachesNoStim2 = []
NoStimTrials = random.sample(range(1, len(reachesNoStim)), len(reachesDuringStim))
for i in NoStimTrials:
    reachesNoStim2.append(reachesNoStim[i])

Timestamps = reachesDuringStim + reachesNoStim2
Timestamps = [findFrame(frameTimes, t) for t in Timestamps]
Timestamps.sort()

input_vid = cv2.VideoCapture(video_file)
lickTimestamps = []

track = 0
for t in Timestamps:
    track += 1
    print(str(track) + " out of " + str(len(Timestamps)) + " completed.\n")
    t = t - buffer
    input_vid.set(1, t)
    cnt = 0
    while(True):
        ret, frame = input_vid.read()
        if not ret:
            break
        
        print(cnt)
        cv2.imshow("video", frame)

        k = -1
        while k not in [108, 100, 97, 27]:
            k = cv2.waitKey(0)

        if k == 108:
            lickTimestamps.append(frameTimes[t+cnt])
            cnt += 1
            continue

        if k == 100:
            cnt += 1
            continue

        if k == 97:
            cnt -= 1
            input_vid.set(1, t + cnt)
            continue
        
        if k == 27:
            break

        
    cv2.destroyAllWindows()

lickTimestamps.sort()
print(lickTimestamps)
doc[name] = nex.NewEvent(doc, 0)
doc[name].SetTimestamps(lickTimestamps)
nex.SaveDocument(doc)
nex.CloseDocument(doc)
print(video_file)
    

