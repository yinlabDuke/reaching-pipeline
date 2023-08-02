import networkx as nx
import matplotlib.pyplot as plt
from supplementary import helper
import pandas as pd 
import networkx.algorithms.community as nx_comm
import nex 
from supplementary import bsoid_clean as bc
import numpy as np
import math
from bsoid_graph_node import bsoid_node
import seaborn as sns
import pickle
import cv2

df = pd.read_csv(dlc_file)
mouthx = df["DLC_resnet50_D155m72Dec15shuffle1_250000.6"].values[2:]
mouthy = df["DLC_resnet50_D155m72Dec15shuffle1_250000.7"].values[2:]

def videoProcessing(filepath, crop, first, cutoff=None):

    input_vid = cv2.VideoCapture(filepath)
    input_vid.set(1, 1)

    w_frame, h_frame = int(input_vid.get(cv2.CAP_PROP_FRAME_WIDTH)), int(input_vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps, frames = input_vid.get(cv2.CAP_PROP_FPS), input_vid.get(cv2.CAP_PROP_FRAME_COUNT)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_vid = cv2.VideoWriter(filepath[0:-4] + '_modified.mp4', fourcc, 100, (w_frame, h_frame))

    if (first):
        pixels = []

        cnt = 0
        preview = 0
        while True:
            ret, frame = input_vid.read()

            if not ret:
                break

            crop_img = frame[crop[0][1]:crop[1][1], crop[0][0]:crop[1][0]]
            sum = np.sum(crop_img)
            pixels.append(sum)


        input_vid = cv2.VideoCapture(filepath)
        check = 0
        while (check == 0 and first):
            fig, axes = plt.subplots(1, figsize=(18, 8))
            (n1, bin1, patches1) = axes.hist(pixels, bins=80)
            axes.set_xlabel("average pixel value")
            axes.set_ylabel("number of frames")
            plt.show()
            cutoff = float(input("Enter the cutoff pixel value you want. Be wary of the exponent. Any frames with greater pixel value will be removed\n"))
            print(str(round(len([i for i in pixels if i > cutoff]) / len(pixels) * 100, 2)) +"% of frames will be removed.")

            time = int(input(("Would you like a preview of what your video will look like? If yes, enter the number of ms you would like to preview for. Otherwise, enter 0.\n")))
            if (time != 0):
                for i in range(time):
                    ret, frame = input_vid.read()

                    if not ret:
                        break
                
                    crop_img = frame[crop[0][1]:crop[1][1], crop[0][0]:crop[1][0]]
                    sum = np.sum(crop_img)
                    if sum < cutoff:
                        cv2.imshow("kept", frame)
                        cv2.waitKey(1)
                    else:
                        cv2.imshow("cut out", frame)
                        cv2.waitKey(1)
                cv2.destroyAllWindows()
            check = int(input("Are you happy with the processing of the video? 1 for yes, 0 for no.\n"))

    input_vid = cv2.VideoCapture(filepath)
    cnt = 0
    savedFrames = []
    for i in helper.progressbar(range(int(frames) + 100)):
        ret, frame = input_vid.read()

        if not ret:
            break

        crop_img = frame[crop[0][1]:crop[1][1], crop[0][0]:crop[1][0]]
        sum = np.sum(crop_img)
        if sum < cutoff:
            output_vid.write(frame)
            savedFrames.append(cnt)
        cnt+=1

    input_vid.release()
    output_vid.release()

    df = pd.DataFrame(data={"savedFrames": savedFrames})
    df.to_csv(filepath[0:-4] + "_savedframes.csv")
    return cutoff 
    


