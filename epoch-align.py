from supplementary import helper
import cv2
import nex 
from alive_progress import alive_bar; import time

'''
Epoch align video to selected timestamps on NeuroExplorer. 
'''

# All times are in seconds 
marker = "beamBreakTimesLaser"
before_t = 1
after_t = 2
markerTime_t = 1 

def alignVideo(doc, vidPath):
    before = int(before_t * 100)
    after = int(after_t * 100)
    stimTime = int(markerTime_t * 100)

    laserTimes = doc[marker].Timestamps()
    markerFrame = []
    frameTimes = doc["frameTimes"].Timestamps()
    for i in laserTimes:
        temp = frameTimes.copy()
        temp = filter(lambda x: x > i - 0.005 and x < i + 0.005, temp)
        try:
            time = list(temp)[0]
            frameNum = frameTimes.index(time)
            markerFrame.append(frameNum)
        except:
            continue

    input_vid, output_vid = helper.edit_video(vidPath, '_aligned.mp4')       
    input_vid = cv2.VideoCapture(vidPath)

    cnt = 0
    tot = len(markerFrame)

    print("Start extracting frames")
    for i in helper.progressbar(range(len(markerFrame))):
        t = markerFrame[i]
        cnt += 1
        for i in range(t - before, t + after):
            input_vid.set(1, i-1)
            ret, frame = input_vid.read()
            if not ret:
                break

            if i < t:
                frame = cv2.putText(frame, str(cnt) + " / " + str(tot), (500, 465), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)

            if i < t + stimTime and i > t:
                frame = cv2.rectangle(frame, (60, 450), (90, 480), (247, 196, 71), -1)

            output_vid.write(frame)

    input_vid.release()
    output_vid.release()
    print("Finished extracting frames!")

if __name__ == '__main__':


    vidPath = helper.search_for_file_path(titles='Upload all the video you want to align', filetypes=[('video', '*.mp4')], dir=r'D:/videos/')
    vidPath = [i for i in vidPath]

    for v in vidPath:
        ne = v.replace('videos', 'neuroexplorer')[0:-13] + '.nex5'
        doc = nex.OpenDocument(ne)
        alignVideo(doc, v)
        nex.CloseDocument(doc)
