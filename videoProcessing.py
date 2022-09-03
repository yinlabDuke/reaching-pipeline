import cv2 
import helper 
import matplotlib.pyplot as plt
import numpy as np
import nex 

def videoProcessing(filepath, doc):

    input_vid = cv2.VideoCapture(filepath)

    w_frame, h_frame = int(input_vid.get(cv2.CAP_PROP_FRAME_WIDTH)), int(input_vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps, frames = input_vid.get(cv2.CAP_PROP_FPS), input_vid.get(cv2.CAP_PROP_FRAME_COUNT)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_vid = cv2.VideoWriter(filepath[0:-4] + '_modified.mp4', fourcc, 100, (w_frame, h_frame))

    pixels = []

    cnt = 0
    while True:
        ret, frame = input_vid.read()

        if not ret:
            break

        crop_img = frame[100:350, 0:350]
        sum = np.sum(crop_img)
        pixels.append(sum)

    fig, axes = plt.subplots(3, figsize=(18, 8))

    axes[0].plot(list(range(len(pixels))), pixels)
    axes[0].set_xlabel("frame number")
    axes[0].set_ylabel("average pixel value")
    (n1, bin1, patches1) = axes[1].hist(pixels, bins=80)
    axes[1].set_xlabel("average pixel value")
    axes[1].set_ylabel("number of frames")

    prop_frames = [round(i / frames * 100, 2) for i in n1]
    (n2, bin2, patches2) = axes[2].hist(prop_frames, bins=15)
    total = np.sum(n2)
    prop_prop = [round(i / total * 100, 2) for i in n2]
    max_pp = max(prop_prop)
    index_pp = prop_prop.index(max_pp)
    for i, v in enumerate(prop_prop):
        if (v < 15 and i > index_pp):
            threshold = bin2[i]
            break

    diff_list = []

    check = 0
    for i in range(len(n1) - 1):
        diff = n1[i+1] - n1[i]

        if check == 1 and prop_frames[i+1] < threshold and diff < 50:
            cutoff = bin1[i+1]
            break

        if prop_frames[i+1] > threshold:
            check = 1

        diff_list.append(diff)

    # plt.show()
    print(cutoff)       
  
        

    input_vid = cv2.VideoCapture(filepath)
    cnt = 0
    savedFrames = []
    while True:
        ret, frame = input_vid.read()

        if not ret:
            break

        crop_img = frame[100:350, 0:350]
        sum = np.sum(crop_img)
        pixels.append(sum)

        sum = np.sum(crop_img)
        if sum < cutoff:
            output_vid.write(frame)
            savedFrames.append(cnt)
        cnt+=1

        progress = cnt / frames * 100
        print(int(progress), '%')

    input_vid.release()
    output_vid.release()

    frameTimes = [v for i, v in enumerate(doc["frameTimes"].Timestamps()) if i in savedFrames]
    doc['frameTimes'].SetTimestamps(frameTimes)
    nex.SaveDocument(doc)

    print(frames, len(frameTimes))

if __name__ == '__main__':
    directory = helper.search_for_directory(titles="Select the directory where the videos are located.")
    filepath = helper.search_for_file_path(dir=directory)
    for vid in filepath:
        videoProcessing(vid)
