import json
import logging
import logging.config
from src.datastore import database


class DatabaseFactory:
    def __init__(self, logger=None):
        self._logger = logger or logging.getLogger(__name__)
        self._database_connection = None

    def get_database_connection(self):
        try:
            if self._database_connection is None:
                # getting database configuration
                self._logger.info('fetching the database configuration file')
                with open('../configuration/database_config.json', 'r') as config:
                    database_conf = json.load(config)
                self._logger.info('building the database connection provider')
                self._database_connection = database.Database(database_conf)
                self._logger.info('building the database connection provider')
            return self._database_connection
        except Exception as e:
            self._logger.info(str(e))