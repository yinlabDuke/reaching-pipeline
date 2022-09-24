import helper
import setupNE
import math
import statistics
import pandas as pd
import nex
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np
import sys
import numpy as np
from scipy.interpolate import interp1d
sys.path.append('C:\\ProgramData\\Nex Technologies\\NeuroExplorer 5 x64')

'''
This pipeline takes DLC csv file and its corresponding video to 
1. Convert pixels to mm
2. Calculate key feature values and export to NeuroExplorer
3. Create cleaned-up file for B-SOID
'''

class post_dlc():
        def __init__(self, dlc_file=None, ratio=None, origin=None):
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
                self.bodyparts = {}
                self.reachPeakTimes = None

# Upload dlc, NE, and video files. 
        def upload_file(self, doc=None, dlc_file=None, video_file=None):

                if self.dlc_file == None:
                        self.dlc_file = helper.search_for_file_path(titles="Upload the DLC file.", filetypes=[('dlc', '*.csv')])[0]

                if doc == None:
                        ne_file = self.dlc_file.replace('videos', 'neuroexplorer')
                        i = self.dlc_file.index('_modified') - len(self.dlc_file) 
                        ne_file = ne_file[0:i] + '.nev'
                        self.doc = nex.OpenDocument(ne_file)

                if video_file == None:
                        video_file =  ne_file.replace('neuroexplorer', 'videos')
                        video_file = video_file[0:-4] + '.mp4'
                self.img, self.fps, self.framecount = helper.getVideo(video_file)

                self.filename = video_file

                self.df = pd.read_csv(self.dlc_file, skiprows=[1, 2])
                self.df_head = pd.read_csv(self.dlc_file, skiprows=lambda x: x not in [0, 1, 2])
                self.df_bsoid = self.df.copy()

                self.savedFrames = pd.read_csv(video_file[0:-4] + "_savedframes.csv")["savedFrames"].tolist()

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
                
                nex.SaveDocumentAs(self.doc, ne_file[0:-4] + ".nex5")

        def setup(self):
                setupNE.setupNE(self.doc, self.savedFrames)
                nex.SaveDocument(self.doc)


        def smooth(self):
                self.frameTimes = self.doc["frameTimes"].Timestamps()[0: len(self.df)]
                for b in self.bodyparts:

                        # Load variables
                        fig, ax = plt.subplots(2)
                        pre_x = self.df.iloc[:, self.bodyparts.get(b)].tolist()
                        likelihood = self.df.iloc[:, self.bodyparts.get(b)+2].tolist()
                        diff_x = [(pre_x[i+1] - pre_x[i]) for i in range(len(pre_x)-1)]
                        diff_abs_x = [abs(i) for i in diff_x]

                        pre_y = self.df.iloc[:, self.bodyparts.get(b)+1].tolist()
                        likelihood = self.df.iloc[:, self.bodyparts.get(b)+2].tolist()
                        diff_y = [(pre_y[i+1] - pre_y[i]) for i in range(len(pre_y)-1)]
                        diff_abs_y = [abs(i) for i in diff_y]

                        # Determine cutoff
                        (n, bin, patches) = ax[0].hist(diff_abs_x, bins=10)
                        try:
                                threshold = [i for i in n if i > 10000]
                                index = np.where(n == threshold[-1])[0][0]
                                cutoff_x = bin[index+1]
                        except:
                                cutoff_x = np.percentile(diff_abs_x, 99.7)

                        (n, bin, patches) = ax[0].hist(diff_abs_y, bins=10)

                        try:
                                threshold = [i for i in n if i > 10000]
                                index = np.where(n == threshold[-1])[0][0]
                                cutoff_y = bin[index+1]
                        except:
                                cutoff_y = np.percentile(diff_abs_y, 99.7)

                        series_x = self.df.iloc[:, self.bodyparts.get(b)]
                        series_y = self.df.iloc[:, self.bodyparts.get(b)+1]

                        likelihood_time = []
                        for i in range(len(likelihood)):
                                if likelihood[i] < .9:  
                                        likelihood_time.append(self.frameTimes[i])
                                        series_x[i] = np.nan

                        # for i in range(len(diff_x)):
                        #         if abs(diff_x[i]) > 0.02:
                        #                 continue
                        #         if abs(diff_x[i]) > cutoff_x:
                        #                 for j in range(i-2, i+3):
                        #                         if j < (len(series_x)-1):
                        #                                 series_x[j] = np.nan

                        likelihood_time = []
                        for i in range(len(likelihood)):
                                if likelihood[i] < .9:  
                                        likelihood_time.append(self.frameTimes[i])
                                        series_y[i] = np.nan

                        # for i in range(len(diff_y)):
                        #         if self.frameTimes[i+1] - self.frameTimes[i] > 0.02:
                        #                 continue
                        #         if abs(diff_y[i]) > cutoff_y:
                        #                 for j in range(i-2, i+3):
                        #                         if j < (len(series_y) - 1):
                        #                                 series_y[j] = np.nan
                        
                        x = series_x.interpolate(method='polynomial', order=3)
                        print(len(x))
                        print(len(self.df.iloc[:, self.bodyparts.get(b)]))
                        self.df.iloc[:, self.bodyparts.get(b)] = x

                        y = series_y.interpolate(method='polynomial', order=3)

                        self.df.iloc[:, self.bodyparts.get(b)+1] = y

                        median_marker = statistics.median(pre_y)
                        norm_marker = [i-median_marker for i in pre_y]
                        median_vel = statistics.median(pre_y)
                        norm_vel=[i-median_vel for i in pre_y]
                        ax[1].plot(self.frameTimes, norm_marker)
                        ax[1].plot(self.frameTimes, norm_vel)
                        ax[1].axhline(y=cutoff_x, linestyle='dashed', color="green")
                        ax[1].axhline(y=cutoff_x*-1, linestyle='dashed', color="green")
                        ax[1].set_title(b)
                        median_marker_fixed = statistics.median(y)
                        norm_marker_fixed=[i-median_marker_fixed for i in y]
                        ax[1].plot(self.frameTimes, norm_marker_fixed, color="purple")
                        ax[1].scatter(x = likelihood_time, y = [100 for i in likelihood_time], color = "red")
                        fig.clear()
                        # plt.show()

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
                
                for b in self.bodyparts:
                        print(b, len(self.df.iloc[:, self.bodyparts.get(b)].tolist()))
                        d_cont[b + "X"] = self.df.iloc[:, self.bodyparts.get(b)].tolist()
                        d_cont[b + "Y"] = self.df.iloc[:, self.bodyparts.get(b)+1].tolist()

                self.df_cont = pd.DataFrame(data=d_cont)

                self.frameTimes = self.doc["frameTimes"].Timestamps()
                self.frameTimes = self.frameTimes[0: len(self.df_cont)]
                self.df_cont["frameTimes"] = self.frameTimes

                hand2spout_dist_np = np.array([i * -1 + 10 for i in hand2spout_dist])
                # plt.plot(hand2spout_dist_np)
                reachPeakTimes_index = find_peaks(hand2spout_dist_np, height=1, distance=10, prominence=5, width=5)[0]
                print(reachPeakTimes_index)
                self.reachPeakTimes = [self.frameTimes[i] for i in reachPeakTimes_index if self.frameTimes[i] - self.frameTimes[i-1] < 0.2]


                plt.plot(self.frameTimes, hand2spout_dist)
                plt.scatter(self.reachPeakTimes, [1 for i in self.reachPeakTimes], color="red")
                # plt.show()

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

                self.doc["frameTimes"].SetTimestamps(self.df_cont["frameTimes"].tolist())
                self.doc["reachPeakTimes"] = nex.NewEvent(self.doc, 0)
                self.doc["reachPeakTimes"].SetTimestamps(self.reachPeakTimes)

                nex.SaveDocument(self.doc)
                nex.CloseDocument(self.doc)
        
        def post_dlc(self):
                self.upload_file()
                self.setup()
                self.smooth()
                self.pix2mm()
                self.feature_calc()
                self.export_bsoid_file()
                self.export_neuroexplorer()


if __name__ == "__main__":
        dlc_files = helper.search_for_file_path(titles="Please select dlc files", filetypes=[('csv', '*filtered.csv')])
        dlc_files = [f for f in dlc_files]

        cnt = 0
        ratio = None
        origin = None
        for f in dlc_files:
                if (cnt != 0):
                        post = post_dlc(dlc_file=f, ratio=ratio, origin=origin)
                        post.post_dlc()
                else:
                        post = post_dlc(dlc_file=f, ratio=ratio, origin=origin)
                        post.post_dlc()
                        ratio = post.ratio
                        origin = post.origin
                        cnt+=1
        print("Done!")



