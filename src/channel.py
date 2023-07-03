import googleapiclient.discovery
import os
import json


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YOUTUBE_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.youtube = self.get_service()
        self.channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel["items"][0]["snippet"]["title"]
        self.description = self.channel["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/channel/" + self.channel['items'][0]['id']
        self.subscriber_count = int(self.channel["items"][0]["statistics"]["subscriberCount"])
        self.video_count = self.channel["items"][0]["statistics"]["videoCount"]
        self.view_count = self.channel["items"][0]["statistics"]["viewCount"]

    def __str__(self):
        """Магический метод, передставляющий инфо о классе пользователю.
           Выводит название канала и ссылку на него
        """
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        """Магиский метод для сложения кол-ва подписчиков разных каналов"""
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        """Магиский метод для вычитания кол-ва подписчиков разных каналов"""
        return self.subscriber_count - other.subscriber_count

    def __gt__(self, other):
        """Магиский метод для сравнения кол-ва подписчиков разных каналов"""
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        """Магиский метод для сравнения кол-ва подписчиков разных каналов"""
        return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        """Магиский метод для сравнения кол-ва подписчиков разных каналов"""
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        """Магиский метод для сравнения кол-ва подписчиков разных каналов"""
        return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other):
        """Магиский метод для сравнения кол-ва подписчиков разных каналов"""
        return self.subscriber_count == other.subscriber_count

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Класс-метод, возвращающий объект для работы с YouTube API"""
        return googleapiclient.discovery.build('youtube', 'v3', developerKey=cls.api_key)

    def to_json(self, file_name):
        """Метод, сохраняющий в файл значения атрибутов экземпляра `Channel`"""
        channel_dict = {
            "channel_id": self.channel_id,
            "desription": self.description,
            "url": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(channel_dict, file, indent=4, ensure_ascii=False)
