import json
import logging
import logging.config

from src.datastore import database, databaseService


class DatabaseFactory:
    def __init__(self, logger=None):
        self._logger = logger or logging.getLogger(__name__)

    def get_database_service(self, collection_name="comments"):
        try:
            self._logger.info('fetching the database configuration file')
            with open('../configuration/database_config.json', 'r') as config:
                database_conf = json.load(config)
            self._logger.info('building the database connection provider')
            database_connection = database.Database(database_conf)
            self._logger.info('building the database service')
            database_service = databaseService.DatabaseService(database_connection,collection_name)
            return database_service
        except Exception as e:
            # error occurred
            self._logger.info(str(e))
            return None
