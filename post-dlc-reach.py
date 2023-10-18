import math 
import nex
from supplementary import helper
from scipy.signal import find_peaks
import matplotlib.pyplot as plt 

fps = 100

def vel_calc1(A, doc):
        A0 = doc[A].ContinuousValues()

        ret = [(A0[i+1] - A0[i])/(1/fps) for i in range(len(A0) - 1)]
        ret.insert(0, 0)
        return ret

def vel_calc2(A, doc):
        Ax = doc[A + "X"].ContinuousValues()
        Ay = doc[A + "Y"].ContinuousValues()
        ret =  [math.dist([Ax[i], Ay[i]], 
                [Ax[i+1], Ay[i+1]]) / (1/fps) for i in range(len(Ax) - 1)]
        ret.insert(0, 0)
        return ret

def dist_calc(A, B, doc):
        Ax = doc[A + "X"].ContinuousValues()
        Ay = doc[A + "Y"].ContinuousValues()
        Bx = doc[B + "X"].ContinuousValues()
        By = doc[B + "Y"].ContinuousValues()

        return [math.dist((Ax[i], Ay[i]), (Bx[i], By[i])) for i in range(len(Ax))]

def createContVar(name, frameTimes, values):
        doc[name] = nex.NewContVarWithFloats(doc, fps)
        doc[name].SetContVarTimestampsAndValues(frameTimes, values)

def createEvent(name, values):
        doc[name] = nex.NewEvent(doc, 0)
        doc[name].SetTimestamps(values)

def peakTime(A, doc, frameTimes):
      A0 = doc[A].ContinuousValues()
      reachPeakTimes_index = find_peaks(A0, height=1, distance=10, prominence=2, width=5)[0]
      ret = [frameTimes[i] for i in reachPeakTimes_index if frameTimes[i] - frameTimes[i-1] < 0.2]
      plt.plot(frameTimes, A0)
      plt.scatter(ret, [1 for i in ret], color="orange")
      plt.show()
      
      return ret

if __name__ == "__main__":
    ne_file = helper.search_for_file_path(dir=r"\D", titles="Upload the NeuroExplorer file", filetypes=[('dlc', '*.nex5')])

    for f in ne_file:
        try:
            doc = nex.OpenDocument(f)
                
        except:
            print(f)
            print("Error opening NE file. Check that the file exists and that NE is open.")
            continue

        frameTimes = doc['frameTimes'].Timestamps()

        doc["handX"].ContinuousValues()

        '''
        YOUR CODE BELOW
        '''
        createContVar("hand2mouthdist", frameTimes, dist_calc("hand", "mouth", doc))
        createContVar("hand2spoutdist", frameTimes, dist_calc("hand", "spout", doc))
        createContVar("handXvel", frameTimes, vel_calc1("handX", doc))
        createContVar("noseXvel", frameTimes, vel_calc1("noseX", doc))
        createEvent("reachPeakTimes", peakTime("handX", doc, frameTimes))

        nex.SaveDocument(doc)
        nex.CloseDocument(doc)