import sys
sys.path.append('C:\\ProgramData\\Nex Technologies\\NeuroExplorer 5 x64')
import nex
import helper
import dataProcessing as dp

class nexObj():
    def __init__(self, filepath, interval=0.75):
        doc = nex.OpenDocument(filepath)
        self.timestamps = doc["videoTimesUpdated"].Timestamps()
        self.bbh0 = doc["beamBreakTimesNoLaser_Hand"].Timestamps()
        self.bbh1 = doc["beamBreakTimesLaser_hand"].Timestamps()
        self.bbn0 = doc["beamBreakTimesNoLaser_Nose"].Timestamps()
        self.bbn1 = doc["beamBreakTimesLaser_nose"].Timestamps()
        self.handX = doc["mouthXPosition"].ContinuousValues()
        self.noseX = doc["noseXPosition"].ContinuousValues()
        self.hand2mouthVel = doc["hand2Mouth_velocity"].ContinuousValues()
        self.nose2spoutVel = doc["nose2Spout_velocity"].ContinuousValues()
        self.interval = interval

    def handX_avg(self, beambreak, laser=0):
        if laser:
            if beambreak == "hand":
                ref = self.bbh1
            else:   
                ref = self.bbn1
        else:
            if beambreak == "hand":
                ref = self.bbh0
            else:
                ref = self.bbn0
        return dp.avg_values(self.timestamps, self.handX, ref, self.interval)
    
    def noseX_avg(self, beambreak, laser=0):
        if laser:
            if beambreak == "hand":
                ref = self.bbh1
            else:   
                ref = self.bbn1
        else:
            if beambreak == "hand":
                ref = self.bbh0
            else:
                ref = self.bbn0
        return dp.avg_values(self.timestamps, self.noseX, ref, self.interval)

    def hand2mouthVel_avg(self, beambreak, laser=0):
        if laser:
            if beambreak == "hand":
                ref = self.bbh1
            else:   
                ref = self.bbn1
        else:
            if beambreak == "hand":
                ref = self.bbh0
            else:
                ref = self.bbn0
        return dp.avg_values(self.timestamps, self.hand2mouthVel, ref, self.interval)