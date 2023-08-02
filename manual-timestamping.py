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

name = input("Name of variable you are timestamping")

# Adjust starting point 
buffer = 60 

def findFrame(frameTimes, time):
    for i, v in enumerate(frameTimes):
        if v > time - 0.005 and v < time + 0.005:
            return i

print("Press D to move forward one frame. Press A to move back one frame. Press L to timestamp a lick. Press ESC to move onto the next session.\n")
ne_file = helper.search_for_file_path(titles="Upload the NeuroExplorer file you want to analyze.\n", filetypes=[("nex", "*.nex5")], dir="D:/")[0]
video_file = video_file = (ne_file[0:-5] + ".mp4").replace('neuroexplorer', 'videos')

try:
        doc = nex.OpenDocument(ne_file)
        print("hi")
except:
        print(ne_file)
        print("Do you have NeuroExplorer open? If yes, NE document doesn't exist. Check to make sure the file is in the correct location.")

frameTimes = doc["frameTimesPrior"].Timestamps()
ref = doc["reachPeakTimes"].Timestamps()

# NoStimTrials = random.sample(range(1, len(reachesNoStim)), len(reachesDuringStim))
# for i in NoStimTrials:
#     reachesNoStim2.append(reachesNoStim[i])

Timestamps = ref
Timestamps = [findFrame(frameTimes, t) for t in Timestamps]
Timestamps.sort()

# input_vid = cv2.VideoCapture(video_file)
# lickTimestamps = []

# track = 0
# for t in Timestamps:
#     track += 1
#     print(str(track) + " out of " + str(len(Timestamps)) + " completed.\n")
#     t = t - buffer
#     input_vid.set(1, t)
#     cnt = 0
#     while(True):
#         ret, frame = input_vid.read()
#         if not ret:
#             break
        
#         print(cnt)
#         cv2.imshow("video", frame)

#         k = -1
#         while k not in [108, 100, 97, 27]:
#             k = cv2.waitKey(0)

#         if k == 108:
#             print("press")
#             lickTimestamps.append(frameTimes[t+cnt])
#             cnt += 1
#             continue

#         if k == 100:
#             cnt += 1
#             continue

#         if k == 97:
#             cnt -= 1
#             input_vid.set(1, t + cnt)
#             continue
        
#         if k == 27:
#             break

        
#     cv2.destroyAllWindows()

lickTimestamps = [2.4989333333333335, 2.6189, 2.7089, 2.848866666666667, 2.958833333333333, 3.0888, 3.2088, 3.3087666666666666, 3.4187333333333334, 3.5387, 3.6986666666666665, 3.7786666666666666, 3.9086333333333334, 4.0286, 26.193766666666665, 26.323733333333333, 26.4137, 26.803633333333334, 26.9236, 27.013566666666666, 33.8021, 34.03203333333333, 34.6519, 34.96183333333333, 35.1118, 35.431733333333334, 35.5417, 35.67166666666667, 41.34043333333333, 41.4704, 41.610366666666664, 46.76923333333333, 46.869233333333334, 46.9892, 47.28913333333333, 47.4191, 47.51906666666667, 47.61906666666667, 47.73903333333333, 47.859, 47.978966666666665, 48.088966666666664, 52.8579, 52.9579, 53.06786666666667, 53.21783333333333, 53.3178, 53.4478, 53.54776666666667, 53.65773333333333, 53.7677, 139.219, 139.33896666666666, 139.44896666666668, 139.7089, 139.82886666666667, 139.93883333333332, 140.05883333333333, 140.1688, 140.29876666666667, 140.41873333333334, 186.16873333333334, 186.2687, 186.3687, 186.48866666666666, 186.59863333333334, 190.32783333333333, 190.4478, 190.53776666666667, 190.66773333333333, 190.9377, 191.04766666666666, 191.14763333333335, 191.2676, 191.39756666666668, 233.8283, 233.91826666666665, 234.02823333333333, 234.13823333333335, 234.2482, 234.36816666666667, 234.48813333333334, 342.0646, 342.1945666666667, 342.8444333333333, 342.9544, 343.0543666666667, 343.1843666666667, 343.2943333333333, 343.4043, 539.5013666666666, 539.6013333333333, 539.7513, 579.2026666666667, 579.3126666666667, 579.4326333333333, 579.7825333333334, 579.8725333333333, 579.9925, 580.1324666666667, 580.2424333333333, 580.3724333333333, 580.5124]
lickTimestamps.sort()
print(lickTimestamps)
doc[name] = nex.NewEvent(doc, 0)
doc[name].SetTimestamps(lickTimestamps)
nex.SaveDocument(doc)
nex.CloseDocument(doc)

    

