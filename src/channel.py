import json
import os
from googleapiclient.discovery import build

API_KEY: str = os.getenv('YT_API_KEY')
class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.dict_to_load = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.dict_to_load["items"][0]["snippet"]["title"]
        self.description = self.dict_to_load["items"][0]["snippet"]["description"]
        self.url = self.dict_to_load["items"][0]["snippet"]["thumbnails"]["default"]["url"]
        self.subscriber_count = self.dict_to_load["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.dict_to_load["items"][0]["statistics"]["videoCount"]
        self.viewing_count = self.dict_to_load["items"][0]["statistics"]["viewCount"]

    def __str__(self):
        return f"{self.title} ({self.url}"


    @classmethod
    def get_service(cls):
        """return object to work with API"""
        service = build('youtube', 'v3', developerKey=API_KEY)
        return service

    @property
    def channel_id(self):
        """make channel_id impossible to change"""
        return self.__channel_id

    def to_json(self, json_file):
        """download to json file"""
        with open(json_file, "w") as f:
            json.dump(self.dict_to_load, f)


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.dict_to_load, indent=2, ensure_ascii=False))

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count

    def __ne__(self, other):
        return self.subscriber_count != other.subscriber_count




