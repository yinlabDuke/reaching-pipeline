import helper
import videoProcessing as vp
import setupNE
import nex

if __name__ == "__main__":
    vids = helper.search_for_file_path(titles="Select all the videos you want to analyze.")

    for v in vids:
        vp.videoProcessing(v)

# Yin lab
# Stanley Park
# Last updated Sep 25 2022
