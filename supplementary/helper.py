import tkinter
from tkinter import filedialog
import os
import cv2 
import numpy as np
import matplotlib.pyplot as plt 
import sys

coords = {}

root = tkinter.Tk()
root.withdraw() #use to hide tkinter window

def search_for_file_path(dir=r"C:\Users\jp464\Desktop", titles="Please select files", filetypes=[('all files', '*.*')]):
    currdir = os.getcwd()
    tempdir = filedialog.askopenfilenames(parent=root, initialdir=dir, title=titles, filetypes=filetypes)
    return tempdir

def search_for_directory(titles="Please select directory"):
    currdir = os.getcwd()
    tempdir = filedialog.askdirectory(parent=root, initialdir=currdir, title=titles)
    return tempdir
  
def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        try:
            if len(coords["ref"]) >= 2:
                coords["ref"] = []
        except:
            coords["ref"] = []

        cv2.circle(click_event.img, (x,y), radius=3, color=(0, 0, 255), thickness=-1)
        cv2.imshow('image', click_event.img)
        coords["ref"].append([x, y])


    if event == cv2.EVENT_RBUTTONDOWN:
        cv2.circle(click_event.img, (x,y), radius=3, color=(255, 0, 0), thickness=-1)
        cv2.imshow('image', click_event.img)
        coords["origin"] = [x, y]
 
def get_pixel(img):
    img_copy = img.copy()
    click_event.img = img_copy
    cv2.imshow('image', click_event.img)
    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    ref_pixels = []
    print(coords)
    for key in coords:
        origin = coords["origin"]
        for r in coords["ref"]:
            ref_pixels.append(r)

    return origin, ref_pixels

def get_pixel2(img):
    img_copy = img.copy()
    click_event.img = img_copy
    cv2.imshow('image', click_event.img)
    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    ref_pixels = []
    print(coords)
    for r in coords["ref"]:
        ref_pixels.append(r)

    return ref_pixels   

def getVideo(video_file, frameNum=1):
    video = cv2.VideoCapture(video_file)
    fps = video.get(cv2.CAP_PROP_FPS)
    framecount = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    video.set(1, frameNum)
    success, image = video.read()
    return image, fps, framecount

def likelihood_cutoff(df, df_head, per):
        cnt = 0
        vert = 0
        percentile = []
        fig, axs = plt.subplots(2, 5, figsize=(12, 10)) 
        for i in range(3, df.shape[1], 3):
                series = df.iloc[:, i]
                percentile.append(np.percentile(series, per))

        cutoff = min(percentile)

        for i in range(3, df.shape[1], 3):
                series = df.iloc[:, i]
                axs[vert, cnt].hist(series)
                axs[vert, cnt].axvline(cutoff, color='orange')
                axs[vert, cnt].set_title(df_head.iloc[0, :].tolist()[i])
                cnt += 1
                if (cnt == 5):
                        cnt = 0
                        vert = 1
        fig.suptitle("The cutoff is " + str(round(cutoff, 2)))
        plt.show()
        return cutoff

def edit_video(vid_file, output_name):
    input = cv2.VideoCapture(vid_file)
    w_frame, h_frame = int(input.get(cv2.CAP_PROP_FRAME_WIDTH)), int(input.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output = cv2.VideoWriter(vid_file[0:-4] + output_name, fourcc, 100, (w_frame, h_frame))

    return input, output

def progressbar(it, prefix="", size=60, out=sys.stdout): # Python3.3+
    count = len(it)
    def show(j):
        x = int(size*j/count)
        print("{}[{}{}] {}/{}".format(prefix, "#"*x, "."*(size-x), j, count), 
                end='\r', file=out, flush=True)
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("\n", flush=True, file=out)

def findFrame(frameTimes, time):
    for i, v in enumerate(frameTimes):
        if v > time - 0.005 and v < time + 0.005:
            return i

# 
def trimFileName(name, former=0, latter=0, ext=0, dir=0):
    if former != 0:
        former = name.index(former)
        
    if latter != 0:
        length = len(latter)
        latter = name.index(latter)
        latter += length
    else:
        latter = len(name)
    
    if ext == 0:
        ext = ""
    else:
        name = name[0: name.index(".")]
    
    if dir == 0:
        dir = ""

    return dir + name[former: latter] + ext

def createVideo(filepath, filtered_frames):

    input_vid = cv2.VideoCapture(filepath)
    input_vid.set(1, 1)

    w_frame, h_frame = int(input_vid.get(cv2.CAP_PROP_FRAME_WIDTH)), int(input_vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps, frames = input_vid.get(cv2.CAP_PROP_FPS), input_vid.get(cv2.CAP_PROP_FRAME_COUNT)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_vid = cv2.VideoWriter(filepath[0:-4] + '_bsoid.mp4', fourcc, 100, (w_frame, h_frame))

    for i in progressbar(range(int(frames) + 100)):
        ret, frame = input_vid.read()

        if not ret:
            break

        if i in filtered_frames:
            output_vid.write(frame)

    input_vid.release()
    output_vid.release()

if __name__ == "__main__":
    trimFileName("Nov-04-2022_v2labels_pose_100HzD151_m71_100722_30Hz_30pulse_bilat_atNoseBB_0msDelay_modifiedDLC_resnet50_reaching-task2Nov3shuffle1_250000_filtered_corrected.csv", former="D151", latter="Delay")
