import googleapiclient.discovery
import os


class Video:
    """Класс для представления видео"""

    api_key: str = os.getenv('YOUTUBE_API_KEY')

    def __init__(self, video_id):
        self.youtube = self.get_service()
        try:
            self.video = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=video_id
                                                    ).execute()

            self.video_id = video_id
            self.title = self.video["items"][0]["snippet"]["title"]
            self.url = f"https://www.youtube.com/video/" + self.video['items'][0]['id']
            self.view_count = self.video["items"][0]["statistics"]["viewCount"]
            self.like_count = self.video['items'][0]['statistics']['likeCount']
        except IndexError:
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    @classmethod
    def get_service(cls):
        """Класс-метод, возвращающий объект для работы с YouTube API"""
        return googleapiclient.discovery.build('youtube', 'v3', developerKey=cls.api_key)

    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):
    """Дочерний класс для представления видео из плейлиста"""

    api_key: str = os.getenv('YOUTUBE_API_KEY')

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.youtube = self.get_service()
        self.playlist = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                          part='contentDetails',
                                                          maxResults=50,
                                                          ).execute()

        self.title = self.video["items"][0]["snippet"]["title"]
        self.url = f"https://www.youtube.com/video/" + self.video['items'][0]['id']
        self.view_count = self.video["items"][0]["statistics"]["viewCount"]
        self.likes = self.video['items'][0]['statistics']['likeCount']

    @classmethod
    def get_service(cls):
        """Класс-метод, возвращающий объект для работы с YouTube API"""
        return googleapiclient.discovery.build('youtube', 'v3', developerKey=cls.api_key)

    def __str__(self):
        return f'{self.title}'
