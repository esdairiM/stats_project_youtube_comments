import json
import logging
from src.datasource import dataprovider


class DataSourceFactory:
    def __init__(self, logger=None):
        self._logger = logger or logging.getLogger(__name__)
        self._api_connection = None
        return self

    def get_api_connection(self):
        if self._api_connection is None:
            # getting api keys
            self._logger.info('fetching the api configuration file')
            with open('../configuration/api_config.json', 'r') as config:
                api_conf = json.load(config)
            self._logger.info('building the data source connection provider')
            self._api_connection = dataprovider.Provider(api_conf)
        return self._api_connection
