import logging

from pymongo.cursor import Cursor

from src.datastore.databaseService import DatabaseService
from src.datastore.factory import DatabaseFactory
from math import ceil

class StatisticsService:
    def __init__(self, logger=None):
        self._logger = logger or logging.getLogger(__name__)
        self._database_service: DatabaseService = DatabaseFactory().get_database_service()

    def get_comments_count(self, videoId):
        count = self._database_service.find_by_videoId(videoId)[1]
        return count

    def get_first_quarter(self, videoId,zerolikes=False):
        # if video id was given
        comments, count = self._database_service.find_by_videoId(videoId)
        if comments is not None:
            # calculate the quarter of the comments
            quarter = ceil(count / 4)
            with_likes_count=quarter
            # make the cursor a list
            first_quarter = comments[:quarter]
            if zerolikes:
                first_quarter = list(filter(lambda comment: comment["likes"] > 0, first_quarter))
                with_likes_count=len(first_quarter)
            # return the list
            return first_quarter,quarter,with_likes_count
        else:
            return None,None,None

    def get_most_popular_comment(self,videoId):
        try:
            return self._database_service.find_by_videoId(videoId)[0][0]
        except:
            return None