import matplotlib.pyplot as plt 
import numpy as np

def data_interpolation(var, bodyparts, df, frameTimes):
    for b in bodyparts:
        fig, ax = plt.subplots(2)
        if var == "x":
            b_index = bodyparts.get(b)
        else:
            b_index = bodyparts.get(b) + 1

        series = df.iloc[:, b_index].copy()
        col = df.iloc[:, b_index].tolist()
        likelihood = df.iloc[:, bodyparts.get(b) + 2].tolist()
        diff = [(col[i+1] - col[i]) for i in range(len(col)-1)]
        diff_abs = [abs(i) for i in diff]

        # Determine cutoff
        (n, bin, patches) = ax[0].hist(diff_abs, bins=10)
        try:
                threshold = [i for i in n if i > 10000]
                index = np.where(n == threshold[-1])[0][0]
                cutoff = bin[index+1]
        except:
                cutoff = np.percentile(diff_abs, 99.7)

        # Replace bad values with NaN
        likelihood_time = []
        for i in range(len(likelihood)):
                if likelihood[i] < .9:  
                        likelihood_time.append(frameTimes[i])
                        series[i] = np.nan

        for i in range(len(diff_abs)):
                if frameTimes[i+1] - frameTimes[i] > 0.02:
                        continue
                if abs(diff[i]) > cutoff:
                        for j in range(i-4, i+5):
                            if 0< j < len(series):
                                series[j] = np.nan

        series = series.interpolate(method='polynomial', order=3)
        df.iloc[:, b_index] = series
        plt.clf()
