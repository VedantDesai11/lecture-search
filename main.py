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

    parser.add_argument('--link', required=True, help='Link to youtube video or txt file with videos or keywords to search (comma seperated)')
    parser.add_argument('--search_keywords', required=False, default=False, help='Set to True if no link is provided and only keywords')
    parser.add_argument('--number_of_links', required=False, default=5, help='Number of videos to get from keyword search')
    parser.add_argument('--dataset_path', default=abspath(getcwd()), required=False, help='Location to save dataset, else in current working directory')
    parser.add_argument('--video_resolution', required=False, default='480p', help='Video resolution 360p, 480p, 720p, 1080p')
    parser.add_argument('--load_pickle', required=False, default=False, help='Load previously stored pickle data')
    parser.add_argument('--create_directories', required=False, default=True, help='Create directories of dataset')
    parser.add_argument('--download_data', required=True, default=False, help='Specify to download data or not')

    args = parser.parse_args()

    pipeline = Pipeline(args)

    #_, _ = pipeline.get_extracted_text('/Users/vedantdesai11/Documents/GitHub/lecture-search/data/videos/Enhanced Science 3  The Importance of Animals.mp4','Enhanced Science 3  The Importance of Animals.mp4')

    if args.download_data == 'True':
        pipeline.download_data()

    pipeline.extract_from_data()

