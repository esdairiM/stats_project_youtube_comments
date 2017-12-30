import logging
from src.services.textPrecessingService import get_common_words,tokenize
from src.datastore.databaseService import DatabaseService
from src.datastore.factory import DatabaseFactory
from math import ceil
import matplotlib.pyplot as plt

class StatisticsService:
    def __init__(self, logger=None):
        self._logger = logger or logging.getLogger(__name__)
        self._database_service: DatabaseService = DatabaseFactory().build().get_database_service()

    def get_comments_count(self, videoId):
        count = self._database_service.find_by_videoId(videoId)[1]
        return count

    def get_first_quarter(self, videoId,remove_zerolikes=False):
        # if video id was given
        comments, count = self._database_service.find_by_videoId(videoId)
        if comments is not None:
            # calculate the quarter of the comments
            quarter = ceil(count / 4)
            with_likes_count=quarter
            # make the cursor a list
            first_quarter = comments[:quarter]
            if remove_zerolikes:
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

    def get_words_by_frequency(self,videoId,first=10):
        comments=self._database_service.find_by_videoId(videoId,only_comments=True)
        words=get_common_words(comments,first)
        return words

    def plot_dict(self,words_dict):
        plt.bar(range(len(words_dict)), words_dict.values(), align='center')
        plt.xticks(range(len(words_dict)), words_dict.keys())
        plt.show()

    def expression_statistics(self,expression,videoId="",ignore_stopwords=True,with_stemming=True):
        total_frequance:float
        mantiens_per_comment:float
        words_number=len(tokenize(expression))
        results=self._database_service.find_expression(expression,words_number,videoId,ignore_stopwords,with_stemming)
        return total_frequance,mantiens_per_comment