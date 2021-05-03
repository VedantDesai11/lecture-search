import pickle
from os import listdir, mkdir, rename
from os.path import isfile, join

from pytube import YouTube
from pytube.exceptions import VideoUnavailable
from tqdm import tqdm

import pytesseract

import time

try:
	from PIL import Image
except ImportError:
	import Image

import cv2

import urllib.request
import re

from googleapiclient.discovery import build


class Pipeline:
	def __init__(self, args):

		self.dataset_path = join(args.dataset_path, 'data')
		load_pickle = args.load_pickle
		create_directories = args.create_directories
		self.video_resolution = args.video_resolution
		self.link_file_keyword = args.link
		self.search_keywords = args.search_keywords
		self.number_of_links = args.number_of_links

		if create_directories == 'True':
			try:
				self.create_dataset_directories()
			except:
				pass

		if load_pickle == 'True':
			self.load_dict()
		else:
			self.data_dict = {}

		with open('config.txt', 'r') as apifile:
			self.api_key = apifile.readline()


		self.get_links()

		print(f'{len(self.data_dict)} youtube links loaded')

	def create_dataset_directories(self):
		mkdir(self.dataset_path)
		mkdir(join(self.dataset_path, 'audios'))
		mkdir(join(self.dataset_path, 'captions'))
		mkdir(join(self.dataset_path, 'videos'))
		mkdir(join(self.dataset_path, 'extracted_text'))

	def save_dict(self):
		with open(join(self.dataset_path, 'data_dict.pickle'), 'wb') as handle:
			pickle.dump(self.data_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

		print('Dictionary Saved')

	def load_dict(self):
		with open(join(self.dataset_path, 'data_dict.pickle'), 'rb') as handle:
			self.data_dict = pickle.load(handle)

		print('Dictionary Loaded')

	def get_links(self):

		if self.search_keywords == 'True':

			keywords = self.link_file_keyword.replace(',', '+')

			html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + keywords)
			video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())

			if len(video_ids) > self.number_of_links:
				video_ids = video_ids[:self.number_of_links]

			for link in video_ids:
				self.add_link_to_dict("https://www.youtube.com/watch?v=" + link)

		else:
			if self.link_file_keyword.split(".")[-1] == 'txt':
				with open(self.link_file_keyword) as textfile:
					for link in textfile:
						link = link.replace('\n', '').strip()
						self.add_link_to_dict(link)


			else:
				self.add_link_to_dict(self.link_file_keyword)

	def add_link_to_dict(self, link):
		# check if link exists
		if link not in self.data_dict:

			# check if link is valid and creates a Youtube object
			try:
				_ = YouTube(link)
				self.data_dict[link] = []
			except:
				pass

	def print_directories(self):
		for item in listdir(self.dataset_path):
			if item != '.ipynb_checkpoints':
				path = join(self.dataset_path, item)
				if isfile(path):
					print(item)
				else:
					print(f'{item}/ ({len(listdir(path))} file/s)')

	def print_dictionary(self):
		for key, value in self.data_dict.items():
			print(f'link: {key}')

			for key2, data in value.items():
				print(f'{key2}: {data}')

	def get_captionpath(self, yt):
		# check if video has english captions
		if 'en' in yt.captions:
			video_caption = yt.captions['en'].xml_captions
		elif 'a.en' in yt.captions:
			video_caption = yt.captions['a.en'].xml_captions
		else:
			print(f'CAPTIONS FOR THIS VIDEO: {yt.captions}')
			return False, 0

		caption_path = join(self.dataset_path, f"captions/{yt.title}.xml")

		# write the captions to xml file
		f = open(caption_path, "w")
		f.write(video_caption)
		f.close()

		return True, caption_path

	def get_videopath(self, yt):
		try:
			# get video stream object with required attributes
			video_stream = yt.streams.filter(type='video', res=self.video_resolution, mime_type="video/mp4")
			video_path = join(self.dataset_path, 'videos')
			video_stream.first().download(video_path)
			video_path = join(video_path, f'{yt.title}.mp4')

			return True, video_path
		except:
			return False, 0

	def get_audiopath(self, yt):
		try:
			# get audio stream object with required attributes
			audio_stream = yt.streams.filter(type='audio', mime_type="audio/mp4")
			audio_path = join(self.dataset_path, 'audios')
			audio_stream.first().download(audio_path)
			audio_path = join(audio_path, f'{yt.title}.mp4')

			return True, audio_path
		except:
			return False, 0

	def get_video_comments(self, yt):

		comments = []

		# creating youtube resource object
		youtube = build('youtube', 'v3',
		                developerKey=self.api_key)

		# retrieve youtube video results
		video_response = youtube.commentThreads().list(
			part='snippet,replies',
			videoId=yt.video_id
		).execute()

		# iterate video response
		while video_response:

			# extracting required info
			# from each result object
			for item in video_response['items']:

				# Extracting comments
				comment = item['snippet']['topLevelComment']['snippet']['textDisplay']

				comments.append(comment)

				if len(comments) == 20:
					return comments

			# Again repeat
			if 'nextPageToken' in video_response:
				video_response = youtube.commentThreads().list(
					part='snippet,replies',
					videoId=yt.video_id
				).execute()
			else:
				break

		return comments

	def get_extracted_text(self, video_path, title):

		capture = cv2.VideoCapture(video_path)

		total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
		fps = capture.get(cv2.CAP_PROP_FPS)

		extracted_text_path = join(self.dataset_path, 'extracted_text', f'{title}.txt')

		with open(extracted_text_path, "w") as extracted_text_file:
			s = 0
			for i in tqdm(range(0, total_frames)):
				if i % int(fps) == 0:
					ret, frame = capture.read()

					if ret:
						extractedInformation = pytesseract.image_to_string(Image.fromarray(frame))
						words = extractedInformation.strip().lower().replace('\n', ' ')

						if words:
							extracted_text_file.write(f'second {s}: {words}\n')

					s += 1

		return True, extracted_text_path

	def download_data(self):

		for i, link in enumerate(self.data_dict.keys()):
			print(f'Downloading link {i + 1}: {link}')

			# create youtube object
			try:
				yt = YouTube(link)

			except VideoUnavailable:
				print(f'Video {link} is unavaialable, skipping.')

			else:
				if not self.data_dict[link]:
					# save video title
					video_title = yt.title

					# return True if downloaded and generated path to save caption
					caption_is_downloaded, caption_path = self.get_captionpath(yt)

					# return True if downloaded and generated path to save audio
					audio_is_downloaded, audio_path = self.get_audiopath(yt)

					# return True if downloaded and generated path to save video
					video_is_downloaded, video_path = self.get_videopath(yt)

					try:
						video_comments = self.get_video_comments(yt)
					except:
						video_comments = []

					self.data_dict[link] = {
						'video_title': video_title,
						'caption_path': caption_path,
						'video_path': video_path,
						'audio_path': audio_path,
						'video_comments' : video_comments,
						'extracted_text_path': None,
						'e_r_extracted_path': None
					}

		self.print_directories()
		self.save_dict()

	def extract_from_data(self):

		for i, link in enumerate(self.data_dict.keys()):
			print(f'Extracting from link {i + 1}: {link}')

			# Extracting text from video
			if len(self.data_dict[link]) != 0:
				# return True if text is extracted without errors
				text_is_extracted, extracted_text_path = self.get_extracted_text(self.data_dict[link]['video_path'],
				                                                                 self.data_dict[link]['video_title'])

				if text_is_extracted:
					self.data_dict[link]['extracted_text_path'] = extracted_text_path
