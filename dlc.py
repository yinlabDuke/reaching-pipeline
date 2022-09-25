import helper 
import deeplabcut as dlc

createConfig = int(input("Are you creating a new configuration? Enter 1 for yes, 0 for no.\n"))
if (createConfig == 0):
    addVideos = int(input("Are you adding new videos? Enter 1 for yes, 0 for no.\n"))
else:
    addVideos = 0
labelVideos = int(input("Are you labeling new videos? Enter 1 for yes, 0 for no.\n"))
training = int(input("Are you training a new model?\n"))
analyzeVideo = int(input("Are you predicting labels for new videos? Enter 1 for yes, 0 for no.\n"))
refine = int(input("Would you like the extract outlier frames, refine your labels and train the dataset again? Enter 1 for yes, 0 for no.\n"))
createVideo = int(input("Would you like to create a labelled video?\n"))

if (createConfig):
    projectName = input("What is the project name?\n")
    experimenter = input("What is your name?\n")
    videos = helper.search_for_file_path(titles="Upload all the videos you want to analyze.\n")
    videos = [f for f in videos]
    config_path = dlc.create_new_project(projectName, experimenter, videos, copy_videos=False) # symbolic link doesn't work
    input("Press enter after you have configured the yaml file\n")

else:
    print("Provide the file path for the config file\n")
    config_path = helper.search_for_file_path(titles="Upload the config file\n")[0]

if (addVideos):
    print("Upload all the videos you want to add.")
    videos = helper.search_for_file_path(titles="Upload all the videos you want to add.\n")
    videos = [f for f in videos]
    print(videos)
    dlc.add_new_videos(config_path, videos, copy_videos=False)
    
if (labelVideos):
    if (int(input("Do you want to extract frames? 1 for yes, 0 for no.\n"))):
        dlc.extract_frames(config_path, mode='automatic', algo='kmeans', userfeedback=False)
    dlc.label_frames(config_path)

if (training):
    dlc.create_training_dataset(config_path, augmenter_type='imgaug')
    dlc.train_network(config_path, maxiters=250000)
    if (int(input("Would you like to evaluate your model? Enter 1 for yes, 0 for no.\n"))):
        dlc.evaluate_network(config_path,Shuffles=[1], plotting=True)

if (analyzeVideo):
    videos = helper.search_for_file_path(titles="Upload all the videos to analyze\n", filetypes=[('video', '*.mp4')])
    videos = [f for f in videos]
    dlc.analyze_videos(config_path, videos, videotype='.mp4', save_as_csv=True)
    dlc.filterpredictions(config_path, videos, videotype='mp4', save_as_csv=True)
    

if (refine):
    if (analyzeVideo == 0):
        videos = helper.search_for_file_path(titles="Upload all the videos to analyze\n", filetypes=[('video', '*.mp4')])


    dlc.extract_outlier_frames(config_path, videos, outlieralgorithm='uncertain', comparisonbodyparts=['hand', 'nonreachinghand', "mouth"], automatic=True)
    
    if (int(input("Proceed with retraining dataset? Enter 1 for yes, 0 for no.\n"))):
        dlc.merge_datasets(config_path)
        dlc.create_training_dataset(config_path, augmenter_type='imgaug')
        dlc.train_network(config_path, maxiters=250000)

if (createVideo):
    print("Upload all the videos you want to create labelled videos for.")
    videos = helper.search_for_file_path(titles="Upload all the videos to analyze\n", filetypes=[('video', '*.mp4')])
    videos = [f for f in videos]
    dlc.create_labeled_video(config_path, videos, save_frames=False, filtered=True)

