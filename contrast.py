import cv2 
import helper 
from statistics import mean


def contrast(filepath):

    input_vid = cv2.VideoCapture(filepath)

    contrast_values = []

    for i in range(1000):
        ret, frame = input_vid.read()

        if not ret:
            break

        contrast = frame.std()
        contrast_values.append(contrast)
    
    print(filepath)
    print(mean(contrast_values))

if __name__ == '__main__': 
    filepath = helper.search_for_file_path(titles="Select the directory where the videos are located.", filetypes=[('mp4', '*modified.mp4')], dir=r"D:\videos")
    for vid in filepath:
        contrast(vid)