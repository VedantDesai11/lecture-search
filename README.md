# lecture-search

CLI pipeline to download video, audio, captions and to extract information from them.

## Installing requirements

```
pip install -r requirements.txt
```

## Input parameters 

```
parser.add_argument('--link', required=True, help='Link to youtube video or txt file with videos')
parser.add_argument('--dataset_path', default=abspath(getcwd()), required=False, help='Location to save dataset, else in current working directory')
parser.add_argument('--video_resolution', required=False, default='480p', help='Video resolution 360p, 480p, 720p, 1080p')
parser.add_argument('--load_pickle', required=False, default=False, help='Load previously stored pickle data')
parser.add_argument('--create_directories', required=False, default=True, help='Create directories of dataset')
parser.add_argument('--download_data', required=True, default=False, help='Specify to download data or not')
parser.add_argument('--extract_data', required=True, default=False, help='Extract text from video and audio')
```









