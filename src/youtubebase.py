from googleapiclient.discovery import build
import os


class YoutubeBase:
    API_KEY = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=API_KEY)
