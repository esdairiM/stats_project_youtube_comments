import logging
from datetime import datetime as dt

from src.datastore.database import Database


class DatabaseService:
    def __init__(self, database_connection: Database, collection_name, logger=None):
        self._logger = logger or logging.getLogger(__name__)
        self._database = database_connection
        self._collection_name = collection_name
        self._last_videoId: str = None
        self._last_find_result: list = None
        self._last_find_count = 0
        self._last_kvargs: dict = None

    def load_data(self, comments):
        self._logger.info('starting to load data')
        try:
            # if comments not empty
            if comments:
                comm, cnt = self.find_by_videoId(comments[0]["videoId"], cash=True)
                if cnt == 0 or (dt.now() - comments[0]["created_at"]).days > 1:
                    # try to create collection and index, pass if already exist
                    self.verify_collection_existence()
                    # insert data
                    self._database.insert(self._collection_name, comments)
                    self._logger.info('finished loading data')
                    return True
                else:
                    # data already exists
                    raise Exception("comments for this video were loaded less then a day ago")
            else:
                # comments list is empty
                return False
        except Exception as e:
            # Error occurred while inserting comments
            self._logger.warning(str(e))
            raise e

    def verify_collection_existence(self):
        try:
            self._database.create_store(self._collection_name)
        except Exception as e:
            self._logger.warning(str(e))
            pass
        try:
            self._database.create_text_index(self._collection_name, "comment")
        except Exception as e:
            self._logger.warning(str(e))
            pass

    def find_by_videoId(self, videoId, only_comments=False, cash=True, kvargs={}):
        """

        :param videoId:
        :param sort:
        :param cash:
        :return:
        """
        kvargs = {"comment": 1, "author": 1, "created_at": 1, "lang": 1, "likes": 1,
                  "_id": 0} if kvargs == {} else kvargs

        # if videoid is the same as last one return last result
        if cash and self._last_find_count != 0 and videoId == self._last_videoId and self._last_kvargs == kvargs:
            if only_comments:
                return self._last_find_result
            return self._last_find_result, self._last_find_count
        elif videoId is not None and videoId != "":
            result_list = list(self._database.find_by_video_id(self._collection_name, videoId, kvargs=kvargs))
            count = len(result_list)
            # optimize research by saving the last search result if cash is true
            self.cash_result(cash, count, kvargs, result_list, videoId)
            if only_comments:
                return result_list
            return result_list, count
        else:
            return None, None

    def find_expression(self, expression, words_number, videoId, ignore_stopwords, with_stemming):
        if words_number == 1:
            result = self._database.find_by_query(self._collection_name, {'$comment': {'$search': expression}})
        return result

    def cash_result(self, cash, count, kvargs, result_list, videoId):
        if cash:
            self._last_find_result = result_list
            self._last_videoId = videoId
            self._last_find_count = count
            self._last_kvargs = kvargs

    def uncash_resuls(self):
        self._last_videoId: str = None
        self._last_find_result: list = None
        self._last_find_count = 0
        self._last_kvargs: dict = None
