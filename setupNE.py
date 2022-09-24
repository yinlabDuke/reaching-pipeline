import sys
sys.path.append('C:\\ProgramData\\Nex Technologies\\NeuroExplorer 5 x64')
import nex
import helper

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

def setupNE(doc, savedFrames, setting): 
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
        nex.Rename(doc, doc[digin], label)

    doc["beamBreakTimesFiltered"] = nex.ISIFilter(doc["beamBreakTimes"], 0.25)
    doc["laserStimOnTimes"] = nex.ISIFilter(doc["laserPulseTimes"], 0.25)
    doc["beamBreakTimesNoLaser"] = nex.NotSync(doc["beamBreakTimesFiltered"], doc["laserStimOnTimes"], -0.1, 0.1)
    doc["beamBreakTimesLaser"] = nex.Sync(doc["beamBreakTimesFiltered"], doc["laserStimOnTimes"], -0.1, 0.1)

# ==========================================================================================================
# ADJUST FRAME STARTTIME
# ==========================================================================================================
    lines = setting_file.readlines()
    for line in lines:
        while (line != "Trigger:"): continue
        exec(line)
    
    nex.SaveDocument(doc)

if __name__ == '__main__':
    file = helper.search_for_file_path("Upload NeuroExplorer file. Make sure markers have been split!")[0]
    doc = nex.OpenDocument(file)
    setupNE(doc)



        

