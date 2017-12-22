import json
import logging
import logging.config
import os

from src.datasource import dataprovider
from src.datastore import database


class ConnectionFactory:
    def __init__(self):
        self.init_logger()
        self._logger = logging.getLogger(__name__)
        self._api_connection = None
        self._database_connection = None

    @staticmethod
    def init_logger():
        try:
            os.mkdir("../log")
        except FileExistsError:
            pass
        # load the logging configuration
        logging.config.fileConfig(
            '../configuration/logging_config.ini',
            defaults={'logfilename': '../log/logFile.log'}
        )


    def get_api_connection(self):
        if self._api_connection is None:
            # getting api keys
            with open('../configuration/api_config.json', 'r') as config:
                api_conf = json.load(config)
            self._api_connection = dataprovider.Provider(api_conf)
        return self._api_connection

    def get_database_connection(self):
        if self._database_connection is None:
            # getting database configuration
            with open('../configuration/database_config.json', 'r') as config:
                database_conf = json.load(config)
            self._database_connection = database.Database(database_conf)
        return self._database_connection
