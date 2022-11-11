import matplotlib.pyplot as plt 
import pandas as pd
from supplementary import helper

'''
Check likelihood values of all markers for dlc file
'''
def likelihood_cutoff(df, df_head):
        cnt = 0
        vert = 0
        fig, axs = plt.subplots(2, 5, figsize=(12, 10)) 


        for i in range(3, df.shape[1], 3):
                series = df.iloc[:, i]
                axs[vert, cnt].hist(series)
                axs[vert, cnt].set_title(df_head.iloc[0, :].tolist()[i])
                cnt += 1
                if (cnt == 5):
                        cnt = 0
                        vert = 1
        plt.show()

if __name__ == "__main__":
        dlc_file = helper.search_for_file_path(titles="Upload DLC file", filetypes=[("dlc", "*filtered.csv")], dir=r"D:/videos")
        for f in dlc_file:
                print(f)
                df = pd.read_csv(f, skiprows=[1, 2])
                df_head = pd.read_csv(f, skiprows=lambda x: x not in [0, 1, 2])
                likelihood_cutoff(df, df_head)