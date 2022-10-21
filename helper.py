import tkinter
from tkinter import filedialog
import os
import cv2 
import numpy as np
import matplotlib.pyplot as plt 

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

if __name__ == "__main__":
    print(getVideo(search_for_file_path(titles="Upload the video corresponding to the DLC")[0]))
