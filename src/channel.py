import json
import os
from googleapiclient.discovery import build

API_KEY: str = os.getenv('YT_API_KEY')
class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        dict_to_load = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = dict_to_load["items"][0]["snippet"]["title"]
        self.description = dict_to_load["items"][0]["snippet"]["description"]
        self.url = dict_to_load["items"][0]["snippet"]["thumbnails"]["default"]["url"]
        self.subscriber_count = dict_to_load["items"][0]["statistics"]["subscriberCount"]
        self.video_count = dict_to_load["items"][0]["statistics"]["videoCount"]
        self.viewing_count = dict_to_load["items"][0]["statistics"]["viewCount"]

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
        dict_to_load = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        with open(json_file, "w") as f:
            json.dump(dict_to_load, f)


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        dict_to_print = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))



