import math 
import nex
from supplementary import helper
from scipy.signal import find_peaks
import matplotlib.pyplot as plt 
from neuroexplorer.NexFileData import *
from neuroexplorer import NexFileWriters
from neuroexplorer import NexFileReaders 

fps = 100

def vel_calc1(A, data):
        A0 = data[helper.nexReaderIndex(data.Continuous, A)].Values

        ret = [(A0[i+1] - A0[i])/(1/fps) for i in range(len(A0) - 1)]
        ret.insert(0, 0)
        return ret

def vel_calc2(A, data):
        Ax = data[helper.nexReaderIndex(data.Continuous, A+'X')].Values
        Ay = data[helper.nexReaderIndex(data.Continuous, A+'Y')].Values
        ret =  [math.dist([Ax[i], Ay[i]], 
                [Ax[i+1], Ay[i+1]]) / (1/fps) for i in range(len(Ax) - 1)]
        ret.insert(0, 0)
        return ret

def dist_calc(A, B, data):
        Ax = data[helper.nexReaderIndex(data.Continuous, A+'X')].Values
        Ay = data[helper.nexReaderIndex(data.Continuous, A+'Y')].Values
        Bx = data[helper.nexReaderIndex(data.Continuous, B+'X')].Values
        By = data[helper.nexReaderIndex(data.Continuous, B+'Y')].Values

        return [math.dist((Ax[i], Ay[i]), (Bx[i], By[i])) for i in range(len(Ax))]

def createContVar(name, frameTimes, values, fd):
    fd.Continuous.append(Continuous(name, frameTimes, values))


def createEvent(name, values, fd):
      fd.Events.append()
      fd.Events.append(Event(name, values))

def peakTime(A, data, frameTimes):
      A0 = data[helper.nexReaderIndex(data.Continuous, A)].Values
      reachPeakTimes_index = find_peaks(A0, height=1, distance=10, prominence=2, width=5)[0]
      ret = [frameTimes[i] for i in reachPeakTimes_index if frameTimes[i] - frameTimes[i-1] < 0.2]
      plt.plot(frameTimes, A0)
      plt.scatter(ret, [1 for i in ret], color="orange")
      plt.show()
      
      return ret

if __name__ == "__main__":
    ne_file = helper.search_for_file_path(dir=r"\D", titles="Upload the NeuroExplorer file", filetypes=[('dlc', '*.nex5')])

    for f in ne_file:
        nexReader = NexFileReaders.Nex5FileReader()
        data = nexReader.ReadNex5File(f)
        fd = FileData()
    
        frameTimes = data.Events[helper.nexReaderIndex(data.Events, 'frameTimes')].Timestamps

        '''
        YOUR CODE BELOW
        '''
        createContVar("hand2mouthdist", frameTimes, dist_calc("hand", "mouth", data.Continuous), fd)
        createContVar("hand2spoutdist", frameTimes, dist_calc("hand", "spout", data.Continuous), fd)
        createContVar("handXvel", frameTimes, vel_calc1("handX", data.Continuous), fd)
        createContVar("noseXvel", frameTimes, vel_calc1("noseX", data.Continuous), fd)
        createEvent("reachPeakTimes", peakTime("handX", data.Continuous, frameTimes), fd)

        writerNex5 = NexFileWriters.Nex5FileWriter()
        writerNex5.WriteDataToNex5File(fd, f)
