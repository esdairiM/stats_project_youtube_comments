import pymongo

from src.datastore.factory import DatabaseFactory
import logging


class DatabaseService:
    def __init__(self,collection_name,logger=None):
        self._logger = logger or logging.getLogger(__name__)
        self._bd=DatabaseFactory.get_database_connection()
        self._collection

    def find_by_videoId(self,videoId,sort=False):
        """

        :param videoId:
        :param sort:
        :return:
        """
        comments=self._bd.find_by_video_id(self._collection,videoId)
        if sort:
            comments.sort('likes',pymongo.DESCENDING)
        return (comments,comments.count())

