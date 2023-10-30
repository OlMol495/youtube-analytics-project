import json
import os
from googleapiclient.discovery import build
from datetime import timedelta
import isodate

class PlayList:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
    def __init__(self, pl_id: str) -> None:
        self.pl_id = pl_id
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=self.pl_id,
                                                                 part='contentDetails,snippet',
                                                                 maxResults=50, ).execute()
        self.channel_id = self.playlist_videos['items'][0]['snippet']['channelId']
        self.playlists = self.youtube.playlists().list(channelId=self.channel_id,
                                     part='contentDetails,snippet',
                                     maxResults=50,).execute()
        for playlist in self.playlists["items"]:
            if playlist['id'] == self.pl_id:
                self.title = playlist['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.pl_id}"
        self.video_ids: list[str] = [video['contentDetails']['videoId']
                                      for video in self.playlist_videos['items']]
        self.video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                       id=','.join(self.video_ids)).execute()


    def to_json(self, json_file):
        """download to json file"""
        with open(json_file, "w") as f:
            json.dump(self.playlists, f)


    @property
    def total_duration(self) -> timedelta:
        """Returns total length of playlist in datatime.timedelta format"""
        total = timedelta(hours=0, seconds=0)
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total += duration
        return total


    def show_best_video(self):
        """Returns url to a video with max likes"""
        max_likes = 0
        video_url = ""
        for video in self.video_response['items']:
            if max_likes < int(video['statistics']['likeCount']):
                max_likes = int(video['statistics']['likeCount'])
                video_url = f"https://youtu.be/{video['id']}"
        return video_url



pl = PlayList('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw')
print(pl.playlist_videos)

