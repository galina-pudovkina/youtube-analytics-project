import datetime
import googleapiclient.discovery
import os
import isodate


class PlayList:
    """Класс для представления плейлиста"""

    api_key: str = os.getenv('YOUTUBE_API_KEY')

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id

        self.youtube = self.get_service()
        self.playlist = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                          part='contentDetails',
                                                          maxResults=50,
                                                          ).execute()
        self.title = \
            self.youtube.playlists().list(id=playlist_id, part='snippet,contentDetails', maxResults=50).execute().get(
                'items')[
                0].get('snippet').get('title')
        self.url = f"https://www.youtube.com/playlist?list=" + self.playlist_id

    @classmethod
    def get_service(cls):
        """Класс-метод, возвращающий объект для работы с YouTube API"""
        return googleapiclient.discovery.build('youtube', 'v3', developerKey=cls.api_key)

    @property
    def total_duration(self):
        """
        Возвращает объект класса datetime.timedelta с суммарной длительность плейлиста
        """

        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)

                                                    ).execute()
        total_duration = 0
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += (datetime.timedelta.total_seconds(duration))
        return datetime.timedelta(seconds=total_duration)

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """

        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        dict_id = {}
        for i in video_ids:
            video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                        id=i
                                                        ).execute()

            like_count = video_response['items'][0]['statistics']['likeCount']
            dict_id[i] = like_count

        v = list(dict_id.values())
        k = list(dict_id.keys())
        return "https://youtu.be/" + k[v.index(max(v))]
