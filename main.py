from os import getcwd
from os.path import abspath

import argparse

from pipeline import Pipeline

if __name__ == '__main__':

    # Path to dataset files
    dataset_path = '/content/Lecture_Recommendation/'
    links_csv_path = 'youtube_links.csv'

    print(f'Current working directory {abspath(getcwd())}')

    # Video resolution 360p, 480p, 720p, 1080p
    video_resolution = '480p'

    parser = argparse.ArgumentParser()

    parser.add_argument('--link', required=True, help='Link to youtube video or txt file with videos')
    parser.add_argument('--dataset_path', default=abspath(getcwd()), required=False, help='Location to save dataset, else in current working directory')
    parser.add_argument('--video_resolution', required=False, default='480p', help='Video resolution 360p, 480p, 720p, 1080p')
    parser.add_argument('--load_pickle', required=False, default=False, help='Load previously stored pickle data')
    parser.add_argument('--create_directories', required=False, default=True, help='Create directories of dataset')
    parser.add_argument('--download_data', required=True, default=False, help='Specify to download data or not')

    args = parser.parse_args()

    pipeline = Pipeline(args)

    if args.download_data == 'True':
        pipeline.download_data()





