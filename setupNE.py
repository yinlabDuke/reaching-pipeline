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

def setupNE(doc): 
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
    # nex.Rename(doc, doc["ainp1"],"touchSignal")
    # nex.Rename(doc, doc["ainp2"],"beamBreak")
    nex.Rename(doc, doc["digin100016"],"laserPulseTimes")
    nex.Rename(doc, doc["digin101024"],"frameTimes")
    nex.Rename(doc, doc["digin100004"], "beamBreakTimes")
    nex.Rename(doc, doc["digin100256"], "reward")
    nex.Rename(doc, doc["digin108192"], "trigger")

# ==========================================================================================================
# CLASSIFY LASER VS NOLASER BEAMBREAKS
# ==========================================================================================================
    doc["beamBreakTimesFiltered"] = nex.ISIFilter(doc["beamBreakTimes"], 0.25)
    doc["laserStimOnTimes"] = nex.ISIFilter(doc["laserPulseTimes"], 0.25)

    doc["beamBreakTimesNoLaser"] = nex.NotSync(doc["beamBreakTimesFiltered"], doc["laserStimOnTimes"], -0.1, 0.1)
    doc["beamBreakTimesLaser"] = nex.Sync(doc["beamBreakTimesFiltered"], doc["laserStimOnTimes"], -0.1, 0.1)

# ==========================================================================================================
# ADJUST FRAME STARTTIME
# ==========================================================================================================
    nex.Rename(doc, doc["frameTimes"], "frameTimesOrig")
    doc["frameBurstOnsets"] = nex.ISIFilter(doc["frameTimesOrig"], 0.1)
    doc["saveStartTime"] = nex.SelectTrials(doc["frameBurstOnsets"], "2")
    doc["frameTimes"] = nex.Sync(doc["frameTimesOrig"], doc["saveStartTime"], -0.01, 10000)

    temp = doc["frameTimes"].Timestamps()
    if temp[1] > temp[0] + 0.015:
        temp.pop(0)
    doc["frameTimes"].SetTimestamps(temp)

    nex.SaveDocument(doc)

if __name__ == '__main__':
    file = helper.search_for_file_path("Upload NeuroExplorer file. Make sure markers have been split!")[0]
    doc = nex.OpenDocument(file)
    setupNE(doc)



        

