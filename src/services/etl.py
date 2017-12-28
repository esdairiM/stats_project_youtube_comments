import logging
import queue
import threading
from time import time

import src.datasource.factory as datasource
import src.datastore.factory as datastore
from src.services import transformer


class ETLService:
    """
    this class is a wrapper that provides ETL functionalities:
        Extract : using the Provider class from the datasource directory
        Transform : using the the transformer module
        Load:  using the Database class from the datastore directory
    """

    def __init__(self, logger=None):
        self._logger = logger or logging.getLogger(__name__)
        self._logger.info('Starting ETL service')
        self._api = datasource.DataSourceFactory().get_api_connection()
        self._database = datastore.DatabaseFactory().get_database_connection()
        self.comments = list()
        self._json_comments = queue.Queue()
        self._extractor_thread: threading.Thread
        self._transformer_thread: threading.Thread
        self.videoId = None

    def extract_and_transform(self, videoId):
        """
        this methode will load data from the api for a given videoid and
        transform it to the desired format

        :param videoId:
        :return self: return this instance of this ETLService
        """
        self.comments = list()
        self._json_comments = queue.Queue()
        self._logger.info('Starting data extraction thread')
        self._extractor_thread = threading.Thread(target=self._get_comments, args=(videoId,))
        self._logger.info('Starting data transformation thread')
        self._transformer_thread = threading.Thread(target=self._process_comments, args=(videoId,))
        self._extractor_thread.start()
        self._transformer_thread.start()
        self._extractor_thread.join()
        self._transformer_thread.join()
        self._logger.info('extraction and transformation finished with success')
        return self

    def load(self):
        """
        this method will try to save the transformed data to

        :return boolean:True if success else False
        """
        try:
            if self.comments:
                self._logger.info('starting to load data')
                self._database.insery(self.comments)
                self._logger.info('finished loading data')
                return True
            else:
                return False
        except Exception as e:
            self._logger.warning(str(e))
            return False

    def _get_comments(self, videoId):
        """
        get a 100 comments each time and add theme to a queue
        :param videoId:
        """
        for res in self._api.get_all_comments(videoId):
            self._json_comments.put(res)

    def _process_comments(self, videoId):
        """
        while the tread is alive it will take out data from the queue and transform it
        :param videoId:
        """
        while self._extractor_thread.isAlive():
            t = time()
            commentlist = transformer.get_comments(self._json_comments.get(), videoId)
            self.comments.extend(commentlist)
            print(time() - t)

    def get_comments(self):
        """
        :return comments: processed comments
        """
        return self.comments
