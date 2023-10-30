import json
from src.youtubebase import YoutubeBase


class Video(YoutubeBase):

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется по id канала.
        Дальше все данные будут подтягиваться по API."""
        self.__video_id = video_id
        try:
            self.video_request = (self.youtube.videos().
                                  list(id=self.__video_id,
                                       part='snippet,statistics').execute())
            self.title = self.video_request["items"][0]["snippet"]["title"]
            self.url = f"https://www.youtube.com/{self.video_id}"
            self.like_count = self.video_request[
                "items"][0]["statistics"]["likeCount"]
            self.viewing_count = self.video_request[
                "items"][0]["statistics"]["viewCount"]
        except Exception:
            self.title = None
            self.url = None
            self.like_count = None
            self.viewing_count = None

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
    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id
