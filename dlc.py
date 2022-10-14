import helper 
import deeplabcut as dlc

createConfig = int(input("Are you creating a new configuration? Enter 1 for yes, 0 for no.\n"))
if (createConfig):
    projectName = input("What is the project name?\n")
    experimenter = input("What is your name?\n")
    videos = helper.search_for_file_path(titles="Upload all the videos you want to analyze.\n")
    videos = [f for f in videos]
    config_path = dlc.create_new_project(projectName, experimenter, videos, copy_videos=False, working_directory=r"D:\DLC Models") # symbolic link doesn't work
    input("Press enter after you have configured the yaml file\n")
else:
    print("Provide the file path for the config file\n")
    config_path = helper.search_for_file_path(titles="Upload the config file\n", filetypes=[('config', '*.yaml')])[0]

check = 1
while (check != 0):
    print("What would you like to do next?\n0: Quit\n1: Add videos\n2: Label videos\n3: Train model (new or next iteration)\n4: Analyze by predicting labels for new videos\n5: Extract outlier frames and refine\n6: Create labelled video")
    check = int(input("Enter your option!"))

    if check == 1:
        print("Upload all the videos you want to add.")
        videos = helper.search_for_file_path(titles="Upload all the videos you want to add.\n")
        videos = [f for f in videos]
        print(videos)
        dlc.add_new_videos(config_path, videos, copy_videos=False)
    
    if check == 2:
        if (int(input("Do you want to extract frames? 1 for yes, 0 for no.\n"))):
            dlc.extract_frames(config_path, mode='automatic', algo='kmeans', userfeedback=False)
        dlc.label_frames(config_path)
    
    if check == 3:
        dlc.create_training_dataset(config_path, augmenter_type='imgaug')
        dlc.train_network(config_path, maxiters=250000)
        if (int(input("Would you like to evaluate your model? Enter 1 for yes, 0 for no.\n"))):
            dlc.evaluate_network(config_path,Shuffles=[1], plotting=True)
        
    if check == 4:
        videos = helper.search_for_file_path(titles="Upload all the videos to analyze\n", filetypes=[('video', '*.mp4')])
        videos = [f for f in videos]
        dlc.analyze_videos(config_path, videos, videotype='.mp4', save_as_csv=True)
        dlc.filterpredictions(config_path, videos, videotype='mp4', save_as_csv=True)
    
    if check == 5:
        if (int(input("Do you want to extract outlier frames? 1 for yes, 0 for no"))):
            videos = helper.search_for_file_path(titles="Upload all the videos to analyze\n", filetypes=[('video', '*.mp4')])
            dlc.extract_outlier_frames(config_path, videos, outlieralgorithm='uncertain', comparisonbodyparts=['hand', 'nonreachinghand', "mouth"], automatic=True)
        dlc.refine_labels(config_path)
        if (int(input("Proceed with retraining dataset? Enter 1 for yes, 0 for no.\n"))):
            dlc.merge_datasets(config_path)
            dlc.create_training_dataset(config_path, augmenter_type='imgaug')
            dlc.train_network(config_path, maxiters=50000)
    
    if check == 6:
        print("Upload all the videos you want to create labelled videos for.")
        videos = helper.search_for_file_path(titles="Upload all the videos to analyze\n", filetypes=[('video', '*.mp4')])
        videos = [f for f in videos]
        dlc.create_labeled_video(config_path, videos, save_frames=False, filtered=True)
    
    if check not in [0, 1, 2, 3, 4, 5, 6]:
        print("Please enter a number among the options provided.")
        

# Yin lab
# Stanley Park
# Last updated Sep 25 2022