import sys
sys.path.append(r'D:\reaching-pipeline\supplementary')
import helper 
import matplotlib.pyplot as plt 
import numpy as np
import nex 
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

def findIndexTime(t, timestamps, dt=0.01):
    for i in timestamps:
        if i > t - dt and i < t + dt:
            return timestamps.index(i)

def kinematicData(ref, target, marker="4to1"):
    ref = doc[ref].Timestamps()
    target_time = doc[target].Timestamps()
    target = doc[target].ContinuousValues()
    marker_time = doc[marker].Timestamps()
    marker = []
    print(marker_time)

    kinematicData = np.zeros([len(ref), 100])
    for i, t in enumerate(ref):
        index = findIndexTime(t, target_time)
        event = np.zeros(100)
        try:
            for j, v in enumerate(range(index-50, index+50)):
                event[j] = target[v]
        except: continue

        marker_i = findIndexTime(t, marker_time, dt=1)
        try:
            if marker_time[marker_i] - t < 0.5 and marker_time[marker_i] - t > -.5:
                marker.append((i, marker_time[marker_i] - t))
        except: pass

        # if np.min(event) < -150 or np.max(event) > 150:
        #     continue
        kinematicData[i] = event

    kinematicData = kinematicData[~np.all(kinematicData == 0, axis=1)]

    return kinematicData, marker

def rasterplot(ref, target, cbar_label, haveMarker=False):
    KD, marker = kinematicData(ref, target, marker="4to1")

    colormaps = [cm.get_cmap("Spectral")]
    x = np.arange(-.5, .5, .01)
    y = np.arange(0, KD.shape[0], 1)

    fig, axs = plt.subplots(1, 1,
                                constrained_layout=True, squeeze=False)
    for [ax, cmap] in zip(axs.flat, colormaps):
        psm = ax.pcolormesh(x, y, KD, cmap=cmap, rasterized=True, vmin=np.min(KD), vmax=np.max(KD))
        cbar = fig.colorbar(psm, ax=ax)

    if haveMarker:
        for i in marker:
            ax.plot(i[1], i[0], 'm^')
    cbar.set_label(cbar_label)
    plt.xlabel("Time (s)")
    plt.ylabel("Trial number")
    plt.show()

def averageplot(ref, target, ylabel):
    fig, ax = plt.subplots()
    for i in target:
        KD, marker = kinematicData(ref, i)
        average_values = np.mean(KD, axis=0)
        std = np.std(KD, axis=0)

        x = np.arange(-.5, .5, .01)

        ax.plot(x, average_values, linewidth=3, label=i)
        ax.fill_between(x, average_values-std, average_values+std, alpha=.1)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel(ylabel)
    ax.legend()

    plt.show()

ne_file = helper.search_for_file_path(titles="Upload NE file", dir=r"D:/neuroexplorer", filetypes=[("nex5", "*.nex5")])[0]
doc = nex.OpenDocument(ne_file)

rasterplot("reachPeakTimes", "bsoid_labels", "B-SOiD group")
# rasterplot("reachPeakTimes", "handX", "Hand X position (mm)")
# rasterplot("reachPeakTimes", "handX_vel", "Hand X velocity (mm/s)")
# rasterplot("reachPeakTimes", "noseX", "Nose X position (mm)")
# rasterplot("reachPeakTimes", "noseX_vel", "Nose X velocity (mm/s)")
# averageplot("1to0", ["handX", "noseX"], "X position (mm)")
# averageplot("1to0", ["handX_vel", "noseX_vel"], "Velocity (mm/s)")


    
        




