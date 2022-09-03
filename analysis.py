import numpy as np 
import matplotlib.pyplot as plt
import sys
sys.path.append('C:\\ProgramData\\Nex Technologies\\NeuroExplorer 5 x64')
import nex
import scipy.stats as st
import helper
import dataProcessing as dp
from nexObj import nexObj


interval = 0.75
beambreak = "nose"

files = helper.search_for_file_path(titles="Please select all the nex files to analyze")
print(files[0], files[1], files[2])
nex10 = nexObj(files[0], interval=interval)
nex20 = nexObj(files[1], interval=interval)
nex30 = nexObj(files[2], interval=interval)
x = np.arange(-interval, interval, 1/100)

fig, axes = plt.subplots(3, 1, figsize=(12, 9))

# ==============================================================================
# Average hand x position over time 
# ==============================================================================
y, low, high = nex10.handX_avg(beambreak, laser=0)
axes[0].plot(x, y)
axes[0].fill_between(x, low, high, alpha=0.2)

y, low, high = nex10.handX_avg(beambreak, laser=1)
axes[0].plot(x, y)
axes[0].fill_between(x, low, high, alpha=0.2)

y, low, high = nex20.handX_avg(beambreak, laser=1)
axes[0].plot(x, y)
axes[0].fill_between(x, low, high, alpha=0.2)

y, low, high = nex30.handX_avg(beambreak, laser=1)
axes[0].plot(x, y)
axes[0].fill_between(x, low, high, alpha=0.2)

axes[0].set_xlabel('Time from ' + beambreak + ' beam break (s)')
axes[0].set_ylabel('X position (mm)')
axes[0].set_title("Hand positions for varying stimulation frequency")
axes[0].legend(['baseline', '10hz', '20hz', '30hz'])

# ==============================================================================
# Average nose x position over time 
# ==============================================================================
y, low, high = nex10.noseX_avg(beambreak, laser=0)
axes[1].plot(x, y)
axes[1].fill_between(x, low, high, alpha=0.2)

y, low, high = nex10.noseX_avg(beambreak, laser=1)
axes[1].plot(x, y)
axes[1].fill_between(x, low, high, alpha=0.2)

y, low, high = nex20.noseX_avg(beambreak, laser=1)
axes[1].plot(x, y)
axes[1].fill_between(x, low, high, alpha=0.2)

y, low, high = nex30.noseX_avg(beambreak, laser=1)
axes[1].plot(x, y)
axes[1].fill_between(x, low, high, alpha=0.2)

axes[1].set_xlabel('Time from ' + beambreak + ' beam break (s)')
axes[1].set_ylabel('X position (mm)')
axes[1].set_title("Nose positions for varying stimulation frequency")
axes[1].legend(['baseline', '10hz', '20hz', '30hz'])

# ==============================================================================
# Average hand2mouth velocity over time 
# ==============================================================================
y, low, high = nex10.hand2mouthVel_avg(beambreak, laser=0)
axes[2].plot(x, y)
axes[2].fill_between(x, low, high, alpha=0.2)

y, low, high = nex10.hand2mouthVel_avg(beambreak, laser=1)
axes[2].plot(x, y)
axes[2].fill_between(x, low, high, alpha=0.2)

y, low, high = nex20.hand2mouthVel_avg(beambreak, laser=1)
axes[2].plot(x, y)
axes[2].fill_between(x, low, high, alpha=0.2)

y, low, high = nex30.hand2mouthVel_avg(beambreak, laser=1)
axes[2].plot(x, y)
axes[2].fill_between(x, low, high, alpha=0.2)

axes[2].set_xlabel('Time from ' + beambreak + ' beam break (s)')
axes[2].set_ylabel('Velocity (mm/s)')
axes[2].set_title("Rate at which hand and mouth distance changes for varying stimulation frequency")
axes[2].legend(['baseline', '10hz', '20hz', '30hz'])



fig.tight_layout()
plt.show()

    
    
