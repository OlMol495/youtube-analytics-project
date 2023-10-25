import json
import os
from googleapiclient.discovery import build

class Video:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__video_id = video_id
        self.video_request = self.youtube.videos().list(id=self.__video_id, part='snippet,statistics').execute()
        self.title = self.video_request["items"][0]["snippet"]["title"]
        self.url = f"https://www.youtube.com/{self.video_id}"
        self.like_count = self.video_request["items"][0]["statistics"]["likeCount"]
        self.viewing_count = self.video_request["items"][0]["statistics"]["viewCount"]

    def __str__(self) -> str:
        return f"{self.title}"
    @property
    def video_id(self):
        return self.__video_id

    def to_json(self, json_file):
        """download to json file"""
        with open(json_file, "w") as f:
            json.dump(self.video_request, f)


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

