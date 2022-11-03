# ===================================================================================
# SUMMARY OF CODE
# Filters for given next transition label 

# PROCEDURE
# Modify the FILE to be the path of the file you wish to analyze. The DEST 
# is where the result will be stored in. You can also change the name of the file. 
# In the terminal, change the directory to where the program is located and enter
# "python filter.py". 
# ===================================================================================

import helper
import pandas as pd 
import pathlib

# File and Destination path
PATH = pathlib.Path(__file__).parent.resolve()
fname = input("Enter the file name you want to filter. Include the extension.")
FILE = str(PATH) + "/output/" + fname
DEST = str(PATH) + "/output/" + fname[0:len(fname) - 5] + "_filtered_frame_transitions.csv"

df = pd.read_csv(FILE)

label = input("Enter label to filter for").split(" ")
label = list(map(lambda x: int(x), label))

df = df[df["next_label"].isin(label)]
df.to_csv(DEST)

if __name__ == "__main__":
    files = helper.search_for_file_path()
    