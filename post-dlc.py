import helper
import setupNE
import math
import statistics
import pandas as pd
import nex
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np
import data_interpolation
import sys
sys.path.append('C:\\ProgramData\\Nex Technologies\\NeuroExplorer 5 x64')

'''
This pipeline takes DLC csv file and its corresponding video to 
1. Convert pixels to mm
2. Calculate key feature values and export to NeuroExplorer
3. Create cleaned-up file for B-SOID
'''

class post_dlc():
        def __init__(self, dlc_file=None, ratio=None, origin=None, setting=None):
                self.df = None
                self.df_head = None
                self.df_bsoid = None
                self.d_events = None
                self.df_cont = None
                self.img = None
                self.fps = None
                self.ratio = ratio
                self.origin = origin
                self.doc = None
                self.framecount = None
                self.frameTimes = None
                self.filename = None
                self.savedFrames = None
                self.dlc_file = dlc_file
                self.ne_file = None
                self.bodyparts = {}
                self.reachPeakTimes = None
                self.setting_file = setting

# ==================================================================
# UPLOAD FILES
# * DLC, NE, and video files must have the same file names except video and DLC has "_modified" attached to the end
# ==================================================================
        def upload_file(self, doc=None, dlc_file=None, video_file=None):

                if self.dlc_file == None:
                        self.dlc_file = helper.search_for_file_path(titles="Upload the DLC file.", filetypes=[('dlc', '*.csv')])[0]

                if doc == None:
                        self.ne_file = self.dlc_file
                        i = self.dlc_file.index('_modified') - len(self.dlc_file) 
                        self.ne_file = (self.ne_file[0:i] + '.nev').replace('videos', 'neuroexplorer')
                        
                        try:
                                self.doc = nex.OpenDocument(self.ne_file)
                        except:
                                print(self.ne_file)
                                print("NE document doesn't exist. Check to make sure the file is in the correct location. Processing rest of the videos.")
                                return

                if video_file == None:
                        video_file =  (self.ne_file[0:-4] + '.mp4').replace('neuroexplorer', 'videos')
                
                try:
                        self.img, self.fps, self.framecount = helper.getVideo(video_file)
                except:
                        print(video_file)
                        print("Video file does not exist. Ensure the file is in the correct location. Processing rest of the videos.")
                        return

                self.filename = video_file

                if self.setting_file == None:
                        self.setting_file = helper.search_for_file_path(titles="Upload the neuroexplorer setting.", filetypes=[('yaml', '*.yaml')])[0]

                # Convert dlc to dataframes 
                self.df = pd.read_csv(self.dlc_file, skiprows=[1, 2])
                self.df_head = pd.read_csv(self.dlc_file, skiprows=lambda x: x not in [0, 1, 2])
                self.df_bsoid = self.df.copy()
                header = self.df_head.iloc[0, :].tolist()
                for i in range(1, len(header), 3):
                        self.bodyparts[header[i]] = i

                # NeuroExplorer Split Markers 
                markerName = "digin1"
                timestamps = np.array(self.doc[markerName].Timestamps())
                values = np.array(self.doc[markerName].Markers())
                labels = set(values[0])
                for l in labels:
                        l2 = str(int(l))
                        num_zeroes = 5 - len(l2)
                        l2 = "digin1" + "0" * num_zeroes + l2
                        ts = timestamps[np.where(values[0] == l)]
                        self.doc[l2] = nex.NewEvent(self.doc, 0)
                        self.doc[l2].SetTimestamps(ts.tolist())
                
                nex.SaveDocumentAs(self.doc, self.ne_file[0:-4] + ".nex5")

# ==================================================================
# SETUP NEUROEXPLORER
# * Resolve double signals, rename labels 
# ==================================================================
        def setup(self):
                self.savedFrames = pd.read_csv(self.filename[0:-4] + "_savedframes.csv")["savedFrames"].tolist()
                setupNE.setupNE(self.doc, self.savedFrames, self.setting_file, self.ne_file)
                nex.SaveDocument(self.doc)
                self.frameTimes = self.doc["frameTimes"].Timestamps()[0: len(self.df)]

# ==================================================================
# SMOOTH DATA
# ==================================================================
        def smooth(self):
                data_interpolation.data_interpolation('x', self.bodyparts, self.df, self.frameTimes)
                data_interpolation.data_interpolation('y', self.bodyparts, self.df, self.frameTimes)

# ==================================================================
# CONVERT DLC PIXELS TO MM
# ==================================================================
        def pix2mm(self):
                if self.ratio == None:
                        print("Left click two pixels for calibration. Right click for reference point.\n")

                        check = 0
                        while (check == 0):
                                self.origin, cal_pixels = helper.get_pixel(self.img)
                                check = int(input("Are you happy with the calibration? 1 for yes, 0 for no.\n"))

                        pix_dist = math.dist(cal_pixels[0], cal_pixels[1])

                        mm = float(input("Please enter the distance between the two calibration pixels in mm.\n"))
                        self.ratio = mm / pix_dist

                self.df.iloc[:, range(1, self.df.shape[1], 3)] = self.df.iloc[:, range(1, self.df.shape[1], 3)].applymap(lambda x: (x - self.origin[0]) * self.ratio)
                self.df.iloc[:, range(2, self.df.shape[1], 3)] = self.df.iloc[:, range(2, self.df.shape[1], 3)].applymap(lambda y: (self.origin[1] - y) * self.ratio)

        def dist_calc(self, body1, body2):
                return [math.dist([self.df.iat[i, body1], self.df.iat[i, body1+1]], 
                        [self.df.iat[i, body2], self.df.iat[i, body2+1]]) for i in range(self.df.shape[0])]

# ==================================================================
# FEATURE CALCULATIONS
# ==================================================================
        def vel_calc(self, feature):
                ret = [(feature[i+1] - feature[i])/(1/self.fps) for i in range(self.df.shape[0] - 1)]
                ret.insert(0, 0)
                return ret
        
        def vel_calc2(self, body):
                ret =  [math.dist([self.df.iat[i+1, body], self.df.iat[i+1, body+1]], 
                        [self.df.iat[i, body], self.df.iat[i, body+1]]) / (1/self.fps) for i in range(self.df.shape[0] - 1)]
                ret.insert(0, 0)
                return ret

        def feature_calc(self):
                bodyparts = self.df_head.iloc[0, :].tolist()
                ref = {}
                for i in range(1, len(bodyparts), 3):
                        ref[bodyparts[i]] = i

                eye = self.bodyparts.get("eye")
                nose = self.bodyparts.get("nose")
                mouth = self.bodyparts.get("mouth")
                hand = self.bodyparts.get("hand")
                nonreachhand = self.bodyparts.get("nonreachhand")
                spout = self.bodyparts.get("spout")
                corner = self.bodyparts.get("corner")

                hand2spout_dist = self.dist_calc(hand, spout)
                nose2spout_dist = self.dist_calc(nose, spout)
                hand2nose_dist = self.dist_calc(hand, nose)
                hand2mouth_dist = self.dist_calc(hand, mouth)
                hand2hand_dist = self.dist_calc(hand, nonreachhand)

                hand2spout_vel = self.vel_calc(hand2spout_dist)
                nose2spout_vel = self.vel_calc(nose2spout_dist)
                hand2nose_vel = self.vel_calc(hand2nose_dist)
                hand2mouth_vel = self.vel_calc(hand2mouth_dist)
                hand2hand_vel = self.vel_calc(hand2hand_dist)
                hand_vel = self.vel_calc2(hand)

                d_cont = {"hand2spout_dist": hand2spout_dist, "nose2spout_dist": nose2spout_dist, "hand2nose_dist": hand2nose_dist, 
                        "hand2mouth_dist": hand2mouth_dist, "hand2hand_dist": hand2hand_dist, "hand2spout_vel": hand2spout_vel,
                        "nose2spout_vel": nose2spout_vel, "hand2nose_vel": hand2nose_vel,  "hand2mouth_vel": hand2mouth_vel,
                        "hand2hand_vel": hand2hand_vel, "hand_vel": hand_vel}

                # Uncomment if you don't want any feature calculations
                # d_cont = {}
                
                for b in self.bodyparts:
                        d_cont[b + "X"] = self.df.iloc[:, self.bodyparts.get(b)].tolist()
                        d_cont[b + "Y"] = self.df.iloc[:, self.bodyparts.get(b)+1].tolist()

                self.df_cont = pd.DataFrame(data=d_cont)

                self.frameTimes = self.doc["frameTimes"].Timestamps()
                self.frameTimes = self.frameTimes[0: len(self.df_cont)]
                self.df_cont["frameTimes"] = self.frameTimes

                hand2spout_dist_np = np.array([i * -1 + 10 for i in hand2spout_dist])
                reachPeakTimes_index = find_peaks(hand2spout_dist_np, height=1, distance=15, prominence=5, width=5)[0]
                self.reachPeakTimes = [self.frameTimes[i] for i in reachPeakTimes_index if self.frameTimes[i] - self.frameTimes[i-1] < 0.2]


                plt.plot(self.frameTimes, hand2spout_dist_np)
                plt.scatter(self.reachPeakTimes, [1 for i in self.reachPeakTimes], color="red")
                # plt.show()
                plt.clf()

# ==================================================================
# EXPORT BSOID CSV
# ==================================================================
        def export_bsoid_file(self):
                i1 = self.filename.index("videos") 
                i2 = i1 - len(self.filename)
                bsoid_file = self.filename[0:i2] + 'bsoid/' + self.filename[i1+7:-4] + ".csv"
                self.df_bsoid = pd.concat([self.df_head, self.df_bsoid])
                self.df_bsoid.to_csv(bsoid_file)

        def export_neuroexplorer(self):
                for col in self.df_cont:
                        if col == "frameTimes": continue
                        self.doc[col] = nex.NewContVarWithFloats(self.doc, self.fps) 
                        self.doc[col].SetContVarTimestampsAndValues(self.df_cont["frameTimes"].tolist(), self.df_cont[col].tolist())

# ==================================================================
# EXPORT FEATURES TO NEUROEXPLORER
# ==================================================================
                self.doc["frameTimes"].SetTimestamps(self.df_cont["frameTimes"].tolist())
                self.doc["reachPeakTimes"] = nex.NewEvent(self.doc, 0)
                self.doc["reachPeakTimes"].SetTimestamps(self.reachPeakTimes)

                nex.SaveDocument(self.doc)
                nex.CloseDocument(self.doc)

        # Comment to your liking to skip steps 
        def post_dlc(self):
                self.upload_file()
                if (self.doc != None) and (self.fps != None):
                        self.setup()
                        self.smooth()
                        self.pix2mm()
                        self.feature_calc()
                        self.export_bsoid_file()
                        self.export_neuroexplorer()


if __name__ == "__main__":
        dlc_files = helper.search_for_file_path(titles="Please select dlc files", filetypes=[('csv', '*filtered.csv')])
        dlc_files = [f for f in dlc_files]
        setting_file = helper.search_for_file_path(titles="Please upload the settings for NE", filetypes=[('yaml', '*.yaml')])[0]

        tot = len(dlc_files)
        cnt = 0
        ratio = None
        origin = None
        for f in dlc_files:
                if (cnt != 0):
                        print(str(int(cnt/tot * 100)) + "%")
                        post = post_dlc(dlc_file=f, ratio=ratio, origin=origin, setting = setting_file)
                        post.post_dlc()
                        cnt+=1
                else:
                        post = post_dlc(dlc_file=f, ratio=ratio, origin=origin, setting=setting_file)
                        post.post_dlc()
                        ratio = post.ratio
                        origin = post.origin
                        cnt+=1
        print("Phew! It's finally done!")

# Yin lab
# Stanley Park
# Last updated: 9/25/22


