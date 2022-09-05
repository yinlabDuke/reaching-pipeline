# Reaching Task Data Analysis Pipeline
***

## Installation
Ensure you have DLC installed. Click [here](https://deeplabcut.github.io/DeepLabCut/docs/installation.html) for more information. 

To use the pipeline, type:
  (base) C:/Users/username> git clone git@github.com:yinlabDuke/reaching-pipeline.git
  
Then activate the DLC environemnt and install nex:
  (base) C:/Users/username> activate DEEPLABCUT
  (DEEPLABCUT) C:/Users/username> pip install nex 
  
Then go to the reaching directory:
  (DEEPLABCUT) C:/Users/username> cd reaching-pipeline
  
## Usage
#### Video preprocessing
This is where you can trim out frames where the animal is not present in the recording. You can upload multiple videos as long as they're in the same directory.  
  (DEEPLABCUT) C:/Users/username/reaching-pipeline> python pre-dlc.py
  
Note: There may be cases when the automated filtering process incorrectly filters too many frames. If this happens, you can manually decide on the threshold:
  TODO

#### DLC
After you have preprocessed the videos, they're ready for DLC. You can either use the command line or the GUI version.

##### Command-line version:
  (DEEPLABCUT) C:/Users/username/reaching-pipeline> python dlc.py
  
##### GUI version:
  (DEEPLABCUT) C:/Users/username/reaching-pipeline> python -m deeplabcut
  
Tips for DLC: 
+ You will have to create a new config file if you do not already have a model. 
+ Recommend at least 100 frames labelled for one video, and 30 for the rest.
+ Nose marker should be placed at the tip of the nose. Mouse marker should be placed at the cleft of the mouse.
+ When reaching hand is not visible, make your best guess as to where it will be. If you are unable to make a good guess, skip the label.
+ After training is complete, you should refine labels and check how accurate the labels are. Consider retraining after adjusting if labels are misplaced.

#### Post-DLC 
This is where the pixels produced by DLC are converted to mm, and various features are calculated to be imported into NeuroExplorer. 

**IMPORTANT**
File structure must be exactly as follows:
- reaching-pipeline
  - neuroexplorer
  - videos
  - bsoid

In "neuroexplorer", add all the .nev files. In "videos", add all the videos. Eventually, the dlc files will also be added to the "videos" directory. Additionally, the file names of corresponding neuroexplorer and video files must be identical, except the extension name. 

#### B-SOiD 
Follow the instructions [here](https://bsoid.org)

After you have run B-SOiD, move all the csv filese with the predicted labels to the "bsoid" directory. Then run:
  (DEEPLABCUT) C:/Users/username/reaching-pipeline> python bsoid.py
This will add the bsoid labels to the corresponding neuroexplorer file. 
