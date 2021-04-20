# lecture-search

CLI pipeline to download video, audio, captions and to extract information from them.

## Installing requirements

```
pip install -r requirements.txt
```

## Input parameters 

```
parser.add_argument('--link', required=True, help='Link to youtube video or txt file with videos or keywords to search (comma seperated)')
parser.add_argument('--search_keywords', required=False, default=False, help='Set to True if no link is provided and only keywords')
parser.add_argument('--number_of_links', required=False, default=5, help='Number of videos to get from keyword search')
parser.add_argument('--dataset_path', default=abspath(getcwd()), required=False, help='Location to save dataset, else in current working directory')
parser.add_argument('--video_resolution', required=False, default='480p', help='Video resolution 360p, 480p, 720p, 1080p')
parser.add_argument('--load_pickle', required=False, default=False, help='Load previously stored pickle data')
parser.add_argument('--create_directories', required=False, default=True, help='Create directories of dataset')
parser.add_argument('--download_data', required=True, default=False, help='Specify to download data or not')
parser.add_argument('--extract_data', required=True, default=False, help='Extract text from video and audio')
```

## Running Example 

Get links from text file, each link is on a new line
```
python3 main.py --link links.txt --download_data True --create_directories True 
```

Add link directly to CLI
```
python3 main.py --link https://www.youtube.com/watch?v=gBGoDmLMe3U&list=RDgBGoDmLMe3U&start_radio=1 --download_data True --create_directories True 
```

Get links from keyword search, each keyword is comma seperated
```
python3 main.py --link education,videos --search_keywords True --number_of_links 10 --download_data True --create_directories True 
```


Once downloaded and completed, we can avoid having to redownload data by setting --download_data as False and --load_pickle as True



