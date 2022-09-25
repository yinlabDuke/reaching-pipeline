import helper 
import cv2
import nex 

def alignVideo(doc, vidPath):
    before = 1
    after = 2.5
    stimTime = 1
    before = int(before * 100)
    after = int(after * 100)
    stimTime = int(stimTime * 100)

    laserTimes = doc['beamBreakTimesLaser'].Timestamps()
    laserTimesFrame = []
    frameTimes = doc["frameTimesPrior"].Timestamps()
    for i in laserTimes:
        temp = frameTimes.copy()
        temp = filter(lambda x: x > i - 0.005 and x < i + 0.005, temp)
        try:
            time = list(temp)[0]
            frameNum = frameTimes.index(time)
            laserTimesFrame.append(frameNum)
        except:
            continue

    

    input_vid = cv2.VideoCapture(vidPath)
    w_frame, h_frame = int(input_vid.get(cv2.CAP_PROP_FRAME_WIDTH)), int(input_vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_vid = cv2.VideoWriter(vidPath[0:-4] + '_aligned.mp4', fourcc, 100, (w_frame, h_frame))
    cnt = 0
    load = '|'
    tot = len(laserTimesFrame)

    print("Start extracting frames")
    for t in laserTimesFrame:
        print(load * int(1/tot*100) + str(round(cnt/tot*100, 0)) + '%' + load * int(1/tot*100))
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
    vidPath = helper.search_for_file_path(titles='Upload all the video you want to align', filetypes=[('video', '*lay.mp4')])
    vidPath = [i for i in vidPath]

    for v in vidPath:
        ne = v.replace('videos', 'neuroexplorer')[0:-4] + '.nex5'
        doc = nex.OpenDocument(ne)
        alignVideo(doc, v)
        nex.CloseDocument(doc)
