from supplementary import helper
from supplementary import videoProcessing 
import random
import cv2 


'''
Processes video to filter for only relevant frames prior to running dlc 
'''

if __name__ == "__main__":
    filepath = helper.search_for_file_path(titles="Select the videos you want to process", filetypes=[("vid", "*.mp4"), ("vid2", "*.avi")], dir="D:/")
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

# Yin lab
# Stanley Park
# Last updated Sep 25 2022
