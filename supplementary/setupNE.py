import sys
sys.path.append('C:\\ProgramData\\Nex Technologies\\NeuroExplorer 5 x64')
import nex
from supplementary import helper
'''
Sets up NeuroExplorer before importing continuous variables
'''

def findIndex(binary, length):
    return [length - i for i, char in enumerate(binary) if char == '1']

def findChannel(name):
    name = name[6:]

    try: 
        binary = bin(int(name)).replace('0b', '')
        length = len(binary)
        positions = findIndex(binary, length)
        return positions
    
    except:
        return None

def setupNE(doc, savedFrames, setting, ne_file): 
# ==========================================================================================================
# REASSIGN DUPLICATE SIGNALS
# ==========================================================================================================
    channels = {}
    duplicates = {}
    for name in doc.EventNames():
        positions = findChannel(name)

        if positions == None:
            continue

        if len(positions) > 1:
            duplicates[name] = positions
        else:
            channels[positions[0]] = name

    for name in duplicates:
        times = doc[name].Timestamps()
        for c in duplicates[name]:
            new = doc[channels[c]].Timestamps() + times
            new.sort()
            doc[channels[c]].SetTimestamps(new)
        nex.Delete(doc, doc[name])

# ==========================================================================================================
# RENAME EVENTS
# ==========================================================================================================
    
    setting_file = open(setting, 'r')
    lines = setting_file.readlines()
    for line in lines:
        if line == "Label:\n": 
            continue
        if line == "Trigger:\n": 
            break
        label_pair = line.split(",")
        digin = label_pair[0]
        label = label_pair[1]
        try:
            nex.Rename(doc, doc[digin], label)
        except:
            print(ne_file)
            print(digin + ", which corresponds to " + label[0:-1] + " does not exist in the neuroexplorer file. Skipping for now.")
            continue
    
    try:
        doc["beamBreakTimesFiltered"] = nex.ISIFilter(doc["beamBreakTimes"], 0.25)
        doc["laserStimOnTimes"] = nex.ISIFilter(doc["laserPulseTimes"], 0.25)
        doc["beamBreakTimesNoLaser"] = nex.NotSync(doc["beamBreakTimesFiltered"], doc["laserStimOnTimes"], -0.1, 0.1)
        doc["beamBreakTimesLaser"] = nex.Sync(doc["beamBreakTimesFiltered"], doc["laserStimOnTimes"], -0.1, 0.1)
    except: 
        print(ne_file)
        print("No beambreak times to clean up. Skipping for now.")

# ==========================================================================================================
# ADJUST FRAME STARTTIME
# ==========================================================================================================
    trigger = 1
    check = False
    for line in lines:
        if check == True:
            trigger = int(line[0:1])
            break
        if line == "Trigger:\n": check = True

    if (trigger):
# POST-TRIGGER 
        nex.Rename(doc, doc["frameTimes"], "frameTimesOrig")
        doc["frameBurstOnsets"] = nex.ISIFilter(doc["frameTimesOrig"], 0.1)
        doc["saveStartTime"] = nex.SelectTrials(doc["frameBurstOnsets"], "2")
        doc["frameTimes"] = nex.Sync(doc["frameTimesOrig"], doc["saveStartTime"], -0.01, 10000)

        frameTimes = doc["frameTimes"].Timestamps()
        if frameTimes[1] > frameTimes[0] + 0.015: 
            frameTimes.pop(0)
        frameTimesPost = [v for i, v in enumerate(doc["frameTimes"].Timestamps()) if i in savedFrames]
        doc["frameTimesPrior"] = nex.NewEvent(doc, 0)
        doc["frameTimesPrior"].SetTimestamps(frameTimes)
        doc["frameTimes"].SetTimestamps(frameTimesPost)

    else:
# PRE-TRIGGER
        frameTimes = doc["frameTimes"].Timestamps()
        frameTimesPost = [v for i, v in enumerate(doc["frameTimes"].Timestamps()) if i in savedFrames]
        doc["frameTimesPrior"] = nex.NewEvent(doc, 0)
        doc["frameTimesPrior"].SetTimestamps(frameTimes)    
        doc["frameTimes"].SetTimestamps(frameTimesPost)
    

    nex.SaveDocument(doc)

if __name__ == '__main__':
    file = helper.search_for_file_path("Upload NeuroExplorer file. Make sure markers have been split!")[0]
    doc = nex.OpenDocument(file)
    setupNE(doc)



        

