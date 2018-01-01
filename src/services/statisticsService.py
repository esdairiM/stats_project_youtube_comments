import logging
from math import ceil
import matplotlib.pyplot as plt
from src.datastore.databaseService import DatabaseService
from src.datastore.factory import DatabaseFactory
from src.services.textPrecessingService import popular_words, tokenize,parallel_counter,stemme_text,prepare_texts
from pandas import DataFrame as frame

class StatisticsService:
    def __init__(self, logger=None):
        self._logger = logger or logging.getLogger(__name__)
        self._database_service: DatabaseService = DatabaseFactory().build().get_database_service()

    def get_comments_count(self, videoId):
        count = self._database_service.find_by_videoId(videoId)[1]
        return count

    def get_first_quarter(self, videoId, remove_zerolikes=False):
        # if video id was given
        comments, count = self._database_service.find_by_videoId(videoId)
        if comments is not None:
            # calculate the quarter of the comments
            quarter = ceil(count / 4)
            with_likes_count = quarter
            # make the cursor a list
            first_quarter = comments[:quarter]
            if remove_zerolikes:
                first_quarter = list(filter(lambda comment: comment["likes"] > 0, first_quarter))
                with_likes_count = len(first_quarter)
            # return the list
            return first_quarter, quarter, with_likes_count
        else:
            return None, None, None

    def get_most_popular_comment(self, videoId):
        try:
            return self._database_service.find_by_videoId(videoId)[0][0]
        except:
            return None

    def get_words_by_frequency(self, videoId, first=10):
        comments = self._database_service.find_by_videoId(videoId)[1]
        words = popular_words(comments, first)
        return words

    def barpolt_dict(self, data:dict):
        plt.bar(range(len(data)), data.values(), align='center')
        plt.xticks(range(len(data)), data.keys())
        plt.show()

    def expression_statistics(self, expression, videoId, caseSensitive=False) -> dict:
        prepared_expression=stemme_text(expression,returnList=False)
        words_number=len(prepared_expression.split(" "))
        results_list, count = self._database_service.find_expression(prepared_expression, videoId, words_number, caseSensitive)
        frequance = self._calculate_total_frequancy(prepared_expression, results_list, videoId, words_number)
        mantiens_per_comment = self._calculate_mantiens_per_comment(prepared_expression, results_list, words_number)
        return {"frequancy": frequance, "mpc": mantiens_per_comment}

    def _calculate_total_frequancy(self, expression, results_list, videoId, words_number):
        if words_number==1:
            counter=parallel_counter(results_list)
            occurence=counter.get(expression)
            print(occurence)
            comments_count=self._database_service.find_by_videoId(videoId)[1]
            return occurence/comments_count
        else:
            pass
    #
    # def _calculate_mantiens_per_comment(self, expression, results_list, words_number):
    #     if words_number==1:
    #         counter=parallel_counter(results_list)
    #         occurence=counter.get(expression)
    #         return occurence/len(results_list)
    #     else:
    #         pass

    # def _calculate_total_frequancy(self, expression, results_list, videoId, words_number):
    #     result=prepare_texts(results_list)
    #     df = frame(result)
    #     df['COUNT'] = df["comments"].str.count(expression)
    #     comments_count = self._database_service.find_by_videoId(videoId)[1]
    #     occurence = df['COUNT'].sum()
    #     print(occurence)
    #     return occurence/comments_count

    def _calculate_mantiens_per_comment(self, expression, results_list, words_number):
        pass