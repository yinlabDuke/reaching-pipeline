import cv2 
from supplementary import helper
import matplotlib.pyplot as plt
import numpy as np
import nex 
import pandas as pd 
import random

'''
Processes video to filter for only relevant frames prior to running dlc 
'''

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
    

if __name__ == '__main__':
    filepath = helper.search_for_file_path(titles="Select the videos you want to process", filetypes=[("vid", "*.mp4")], dir=r"D:/")
    check = 0
    crop = None
    cutoff = None
    for vid in filepath:
        if crop ==  None or cutoff == None:
            while (check == 0):
                img, fps, framecount = helper.getVideo(vid)
                img, fps, framecount = helper.getVideo(vid, random.randint(1, framecount))
                cv2.imshow("Are you happy with this frame?", img)
                check = int(input("Are you happy with the image to select region of cropping? 1 for yes, 0 for no.\n"))
            
            check = 0
            while (check == 0):
                print("Left click the left upper and right lower vertices of the rectangle you want to crop.\n")
                crop = helper.get_pixel2(img)

                input_vid = cv2.VideoCapture(vid)    
                for i in range(500):
                    ret, frame = input_vid.read()

                    if not ret:
                        break

                    crop_img = frame[crop[0][1]:crop[1][1], crop[0][0]:crop[1][0]]
                    cv2.imshow("original", frame)
                    cv2.imshow("cropped", crop_img)
                    cv2.waitKey(1)
                cv2.destroyAllWindows()
                check = int(input("Are you happy with the cropping of the video? 1 for yes, 0 for no.\n"))
            cutoff = videoProcessing(vid, crop, first=True)
        else:
            videoProcessing(vid, crop, False, cutoff)
