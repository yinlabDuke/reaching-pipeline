import sys
sys.path.append('C:\\ProgramData\\Nex Technologies\\NeuroExplorer 5 x64')
import nex
from supplementary import helper

def inRange(l, a, b):
    for i in l:
        if a < i and i < b:
            return True 
    
    return False

def beamBreakTimesFilter():
    ne_file = helper.search_for_file_path(titles="Upload NE file", filetypes=[('nex5', '*.nex5')])[0]
    doc = nex.OpenDocument(ne_file)
    beamBreakTimesNoLaser_times = doc["beamBreakTimesNoLaser"].Timestamps()
    reachPeakTimes = doc["reachPeakTimes"].Timestamps()

    remove = []
    for i in range(len(beamBreakTimesNoLaser_times)):
        try:
            if not inRange(reachPeakTimes, beamBreakTimesNoLaser_times[i], beamBreakTimesNoLaser_times[i+1]):
                remove.append(i)
        except:
            continue

    
    beamBreakTimesNoLaser_times = [i for j, i in enumerate(beamBreakTimesNoLaser_times) if j not in remove]
    
    doc["beamBreakTimesNoLaserModified"] = nex.NewEvent(doc, 0)
    doc["beamBreakTimesNoLaserModified"].SetTimestamps(beamBreakTimesNoLaser_times)
    nex.SaveDocument(doc)
    nex.CloseDocument(doc)

if __name__ =="__main__":
    beamBreakTimesFilter()

