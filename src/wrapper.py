from src import youtube, database
import json
import os
import logging.config
import logging


class Wrapper:
    def __init__(self):
        self.init_logger()
        self._logger = logging.getLogger(__name__)
        self._youtube_connection = None
        self._database_connection = None

    @staticmethod
    def init_logger():
        try:
            os.mkdir("../log")
        except FileExistsError:
            pass
        # load the logging configuration
        logging.config.fileConfig(
            '../configuration/logging.ini',
            defaults={'logfilename': '../log/youtube_comments_stats.log'}
        )


    def get_youtube_connection(self):
        if self._youtube_connection is None:
            # getting youtube api keys
            with open('../configuration/youout_api_config.json', 'r') as config:
                youtube_conf = json.load(config)
            self._youtube_connection = youtube.Youtube(youtube_conf)
        return self._youtube_connection

    def get_database_connection(self):
        if self._database_connection is None:
            # getting database configuration
            with open('../configuration/database_config.json', 'r') as config:
                database_conf = json.load(config)
            self._database_connection = database.Database(database_conf)
        return self._database_connection
