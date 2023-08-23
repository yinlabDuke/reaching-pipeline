from supplementary import helper
from supplementary import setupNE
import math
import statistics
import pandas as pd
import nex
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np
from supplementary import data_interpolation
import sys
import os 
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
                self.dir = None
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
                                print("NeuroExplorer must be open. If NE is open, the NE document doesn't exist. Check to make sure the file is in the correct location. Processing rest of the videos.")
                                return

                if video_file == None:
                        for ext in ['.mp4', '.avi']:
                                video_file = (self.ne_file[0:-4] + ext).replace('neuroexplorer', 'videos')
                                self.img, self.fps, self.framecount = helper.getVideo(video_file)
                                if (self.fps < 1 ):
                                        print("poop")
                                        continue
                                else:
                                        break
                
                if self.fps < 1:
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
                if len(self.df) != len(self.frameTimes):
                        print("DLC csv file has " + str(len(self.df)) + " frames, but the video has " + str(len(self.frameTimes)) + " frames.")
                        self.df = self.df[0:len(self.frameTimes)]
                        
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
                        print("Left click two pixels for calibration. Right click for reference point. If you make a mistake, still complete all three clicks, then press enter..\n")

                        self.origin, cal_pixels = helper.get_pixel(self.img)
                        check = int(input("Are you happy with the calibration? 1 for yes, 0 for no.\n"))
                        if check != 1:
                                nex.CloseDocument(self.doc)
                                exit()

                        pix_dist = math.dist(cal_pixels[0], cal_pixels[1])

                        mm = float(input("Please enter the distance between the two calibration pixels in mm.\n"))
                        self.ratio = mm / pix_dist

                self.df.iloc[:, range(1, self.df.shape[1], 3)] = self.df.iloc[:, range(1, self.df.shape[1], 3)].applymap(lambda x: (x - self.origin[0]) * self.ratio)
                self.df.iloc[:, range(2, self.df.shape[1], 3)] = self.df.iloc[:, range(2, self.df.shape[1], 3)].applymap(lambda y: (self.origin[1] - y) * self.ratio)

# ==================================================================
# FEATURE CALCULATIONS
# ==================================================================
        def feature_calc(self):
                bodyparts = self.df_head.iloc[0, :].tolist()
                ref = {}
                for i in range(1, len(bodyparts), 3):
                        ref[bodyparts[i]] = i

                d_cont = {}

                for b in self.bodyparts:
                        d_cont[b + "X"] = self.df.iloc[:, self.bodyparts.get(b)].tolist()
                        d_cont[b + "Y"] = self.df.iloc[:, self.bodyparts.get(b)+1].tolist()

                self.df_cont = pd.DataFrame(data=d_cont)

                self.frameTimes = self.doc["frameTimes"].Timestamps()
                self.frameTimes = self.frameTimes[0: len(self.df_cont)]
                self.df_cont["frameTimes"] = self.frameTimes
                plt.clf()

# ==================================================================
# EXPORT BSOID CSV
# ==================================================================
        def export_bsoid_file(self):
                i1 = self.filename.index("videos") 
                i2 = i1 - len(self.filename)
                data_dir = bsoid_file = self.filename[0:i2] + 'bsoid/data'
                raw_dir = bsoid_file = self.filename[0:i2] + 'bsoid/raw'
                bsoid_dir = data_dir + "/" + self.filename[i1+7:-4]
                bsoid_file = bsoid_dir + "/" + self.filename[i1+7:-4] + ".csv"
                raw_bsoid_file = raw_dir + "/" + self.filename[i1+7:-4] + ".csv"
                self.df_bsoid = pd.concat([self.df_head, self.df_bsoid])
                try:
                        os.mkdir(data_dir)
                except:
                        pass

                try:
                        os.mkdir(raw_dir)
                except:
                        pass

                try:
                        os.mkdir(bsoid_dir)
                        self.df_bsoid.to_csv(bsoid_file, index=False)
                        self.df_bsoid.to_csv(raw_bsoid_file, index=False)
                except:
                        self.df_bsoid.to_csv(bsoid_file, index=False)
                        self.df_bsoid.to_csv(raw_bsoid_file, index=False)

        def export_neuroexplorer(self):
                for col in self.df_cont:
                        if col == "frameTimes": continue
                        self.doc[col] = nex.NewContVarWithFloats(self.doc, self.fps)
                        self.doc[col].SetContVarTimestampsAndValues(self.df_cont["frameTimes"].tolist(), self.df_cont[col].tolist())
                self.doc["frameTimes"].SetTimestamps(self.df_cont["frameTimes"].tolist())
                nex.SaveDocument(self.doc)
                nex.CloseDocument(self.doc)

        # Comment to your liking to skip steps 
        def post_dlc(self):
                self.upload_file()
                if (self.doc != None) and (self.fps > 1):
                        self.pix2mm()
                        self.setup()
                        self.smooth()
                        self.feature_calc()
                        self.export_neuroexplorer()


if __name__ == "__main__":
        dlc_files = helper.search_for_file_path(titles="Please select dlc files", filetypes=[('csv', '*.csv')], dir=dir)
        dlc_files = [f for f in dlc_files]
        # setting_file = helper.search_for_file_path(titles="Please upload the settings for NE", filetypes=[('yaml', '*.yaml')], dir=dir)[0]
        setting_file = r"D:\reaching-pipeline\dlc-settings\reaching-post-trigger-settings.yaml"

        tot = len(dlc_files)
        cnt = 0
        ratio = None
        origin = None
        for i in helper.progressbar(range(len(dlc_files))):
                f = dlc_files[i]
                if (ratio != None):
                        post = post_dlc(dlc_file=f, ratio=ratio, origin=origin, setting = setting_file)
                        post.post_dlc()
                        cnt+=1
                else:
                        post = post_dlc(dlc_file=f, ratio=ratio, origin=origin, setting=setting_file)
                        post.post_dlc()
                        ratio = post.ratio
                        origin = post.origin
                        cnt+=1

# Yin lab
# Stanley Park
# Last updated: 9/25/22


