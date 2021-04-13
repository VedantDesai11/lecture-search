# lecture-search

CLI pipeline to download video, audio, captions and to extract information from them.

NOT TESTED YET, WONT RUN RIGHT AWAY

## Input parameters 

* link - required, we can provided a text file with a link sperated by \n or just a single youtube video link
* dataset_path - not required, defaults to current location of main.py unless mentioned
* video_resolution - not required, default value 480p. Options - 360p, 480p (recommended), 720p, 1080p
* load_pickle - not required, default false, Loads previously created dictionary for already created and extracted link information.
* create_directories - not required, default false. Creates the folders needed to for download of the dataset. Select True if running program for the first time

## Using the Pipeline class

Initialize the class in main.py with input arguments. 

Run get_links() on the class to initialize dictionary with youtube links from text file or youtube link.

Run create_dataset() to use links to download the necessary data. 

