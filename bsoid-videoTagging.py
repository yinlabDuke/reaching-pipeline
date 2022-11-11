import cv2 
from supplementary import helper 
import matplotlib.pyplot as plt
import numpy as np
import nex 
import pandas as pd 
import random

def videoTagging(filepath, bsoid_groups, color):

    input_vid = cv2.VideoCapture(filepath)
    input_vid.set(1, 1)

    w_frame, h_frame = int(input_vid.get(cv2.CAP_PROP_FRAME_WIDTH)), int(input_vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps, frames = input_vid.get(cv2.CAP_PROP_FPS), input_vid.get(cv2.CAP_PROP_FRAME_COUNT)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_vid = cv2.VideoWriter(filepath[0:-4] + '_bsoid.mp4', fourcc, 100, (w_frame, h_frame))



    tot = len(bsoid_groups)
    for i, v in enumerate(bsoid_groups):
        ret, frame = input_vid.read()

        if not ret:
            break
        
        frame = cv2.putText(frame, "Group " + str(v), (500, 465), cv2.FONT_HERSHEY_PLAIN, 1, color[v], 2)
        output_vid.write(frame)

        progress = i / tot * 100
        print(int(progress), '%')

    input_vid.release()
    output_vid.release()
    

if __name__ == '__main__':
    filepath = helper.search_for_file_path(titles="Select the videos you want to process", filetypes=[("vid", "*.mp4")])
    check = 0
    crop = None
    cutoff = None
    for vid in filepath:
        i = vid.index("_modified") - len(vid)
        
        ne_file = (vid[0:i] + ".nex5").replace("videos", "neuroexplorer")
        try:
            doc = nex.OpenDocument(ne_file)
        except:
            print(ne_file)
            print("Cannot find NE file. Manually upload the NE file.")
            doc = nex.OpenDocument(helper.search_for_file_path()[0])

        bsoid_groups = doc["bsoid_labels"].ContinuousValues()
        bsoid_groups = [int(i) for i in bsoid_groups]
        set_bsoid_groups = set(bsoid_groups)
        color = {}
        for i in set_bsoid_groups:
            if i < 6:
                color[i] = (i * 50, 0, 0)
            elif i < 11:
                i2 = i - 5
                color[i] = (0, i2 * 50, 0)
            else:
                i2 = i - 6
                color[i] = (0, 0, i2 * 50)

        videoTagging(vid, bsoid_groups, color)
