import cv2 
import helper 
import matplotlib.pyplot as plt
import numpy as np
import nex 
import pandas as pd 
import random

ne_file = helper.search_for_file_path(titles="Upload the NeuroExplorer file you want to analyze.\n")[0]
video_file = video_file = (ne_file[0:-5] + ".mp4").replace('neuroexplorer', 'videos')

try:
        doc = nex.OpenDocument(ne_file)
except:
        print(ne_file)
        print("Do you have NeuroExplorer open? If yes, NE document doesn't exist. Check to make sure the file is in the correct location.")

startTime = doc["saveStartTime"].Timestamps()[0]
reachesDuringStim = doc["reachesDuringStim"].Timestamps()
reachesNoStim = doc["reachesNoStim"].Timestamps()
reachesNoStim2 = []
NoStimTrials = random.sample(range(1, len(reachesNoStim)), len(reachesDuringStim))
for i in NoStimTrials:
    reachesNoStim2.append(reachesNoStim[i])

Timestamps = reachesDuringStim + reachesNoStim2
Timestamps = [int(t) * 100 for t in Timestamps]
Timestamps.sort()

input_vid = cv2.VideoCapture(video_file)
lickTimestamps = []

for t in Timestamps:
    t = t - 70
    input_vid.set(1, t)
    cnt = 0
    print("New set of frames.\n")
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
            lickTimestamps.append((t + cnt) / 100 + startTime)
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

print(lickTimestamps)
doc["lickTimes"] = nex.NewEvent(doc, 0)
doc["lickTimes"].SetTimestamps(lickTimestamps)
nex.SaveDocument(doc)
nex.CloseDocument(doc)
print(video_file)
    

