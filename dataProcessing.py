import numpy as np
import scipy.stats as st
import pandas as pd

def filter(timestamps, var, min, max, interval):
    ret = []
    times = []

    for x, y in zip(timestamps, var):
        if (x >= min and x <= max):
            ret.append(y)
            times.append(x)

    if len(ret) != (interval * 2) * 100:
        try:
            ind = timestamps.index(times[-1])
            ret.append(var[ind + 1])
        except:
            return ret
        

    return ret

def avg_values(timestamps, var, reference, interval):
    handX_all = []
    sem_low = []
    sem_high = []
    for i in reference:
        temp = filter(timestamps, var, i-interval, i+interval, interval)
        if (len(temp) != interval * 2 * 100):
            continue

        handX_all.append(temp)    
        
    handX_all = np.array(handX_all)

    for i in handX_all.transpose():
        avg = np.mean(i)
        sem = st.sem(i) 
        # ci = st.t.interval(alpha=0.95, df=i.size-1, loc=np.mean(i), scale=st.sem(i))
        sem_low.append(avg - sem)
        sem_high.append(avg + sem)

    return np.average(handX_all, axis=0), sem_low, sem_high