import logging

from src.datastore.factory import DatabaseFactory
from src.services.etl import ETLService
from src.services.statisticsService import StatisticsService


class Controller():
    """this class is a wrapper that provides the main with all the resources it needs"""
    def __init__(self):
        self.etl_service = ETLService()
        self._logger = logging.getLogger(__name__)
        self.statistics_service = StatisticsService()
        self.database = DatabaseFactory().build().get_database_service()

    def etl(self, videoId):
        res = self.etl_service.extract_and_transform(videoId).load()
        return res

    def get_comments_count(self, videoId):
        return self.statistics_service.get_comments_count(videoId)

    def get_first_quarter(self, videoId):
        return self.statistics_service.get_first_quarter(videoId, remove_zerolikes=True)

    def get_popular_comment(self, videoId):
        return self.statistics_service.get_most_popular_comment(videoId)

    def get_frequent_words(self, videoId):
        return self.statistics_service.get_words_by_frequency(videoId)

    def get_expression_frequency(self, videoId, expression):
        return self.statistics_service.expression_statistics(expression, videoId)

    def get_expressions_proba(self, videoId, expression1, expression2):
        return self.statistics_service.prob_cond(expression1, expression2, videoId)

    def get_gender_percentage(self, videoId):
        return self.statistics_service.gender_percent(videoId)

    def get_video_data(self,videoId):
        return self.database.find_video_data(videoId)[0]
