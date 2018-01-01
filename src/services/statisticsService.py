import logging
from math import ceil

import matplotlib.pyplot as plt
import pandas as pd

from src.datastore.databaseService import DatabaseService
from src.datastore.factory import DatabaseFactory
from src.services.textPrecessingService import popular_words, prepare_text_list, prepare_text


class StatisticsService:
    def __init__(self, logger=None):
        self._logger = logger or logging.getLogger(__name__)
        self._database_service: DatabaseService = DatabaseFactory().build().get_database_service()

    def get_comments_count(self, videoId):
        count = self._database_service.find_by_videoId(videoId)[1]
        return count

    def get_first_quarter(self, videoId: str, remove_zerolikes: bool = False) -> dict:
        # if video id was given
        comments, count = self._database_service.find_by_videoId(videoId)
        if comments is not None:
            # calculate the quarter of the comments
            quarter = ceil(count / 4)
            first_quarter = comments[:quarter]
            if remove_zerolikes:
                first_quarter = list(filter(lambda comment: comment["likes"] > 0, first_quarter))
                quarter = len(first_quarter)
            return {"first_qr": first_quarter, "length": quarter}
        else:
            return None

    def get_most_popular_comment(self, videoId):
        try:
            return self._database_service.find_by_videoId(videoId)[0][0]
        except:
            return None

    def get_words_by_frequency(self, videoId, comment_list: list = None, first=10):
        comments = comment_list
        if comments is None:
            comments = self._database_service.find_by_videoId(videoId)[0]
        words = popular_words(comments, first)
        return words

    def barpolt_dict(self, data: dict):
        plt.bar(range(len(data)), data.values(), align='center')
        plt.xticks(range(len(data)), data.keys())
        plt.show()

    def expression_statistics(self, expression, videoId) -> dict:
        prepared_words=prepare_text(expression)
        prepared_expression = " ".join(prepared_words)
        words_number = len(prepared_expression)
        results_list, count = self._database_service.find_expression(prepared_expression, videoId, words_number)
        df = self.create_df(results_list)
        occurence = self._expression_occurence(df, prepared_expression)
        frequance = self._calculate_total_frequancy(occurence, videoId)

        mantiens_per_comment = self._calculate_mantiens_per_comment(occurence, len(results_list))

        return {"frequancy": frequance, "mpc": mantiens_per_comment}

    # def _calculate_total_frequancy(self, expression, results_list, videoId, words_number):
    #     if words_number == 1:
    #         counter = counte_words(results_list)
    #         occurence = counter.get(expression)
    #         print(occurence)
    #         comments_count = self._database_service.find_by_videoId(videoId)[1]
    #         return occurence / comments_count
    #     else:
    #         pass

    #
    # def _calculate_mantiens_per_comment(self, expression, results_list, words_number):
    #     if words_number==1:
    #         counter=parallel_counter(results_list)
    #         occurence=counter.get(expression)
    #         return occurence/len(results_list)
    #     else:
    #         pass

    def _calculate_total_frequancy(self, occurence, videoId):
        comments_count = self._database_service.find_by_videoId(videoId)[1]
        return occurence / comments_count

    def _calculate_mantiens_per_comment(self, occurence, comments_number):
        return occurence / comments_number

    def _expression_occurence(self, df, expression):
        #df['COUNT'] = df.comments.str.count(expression)
        occurence = df.comments.str.count(expression).sum()
        return occurence

    def create_df(self, results_list):
        result = prepare_text_list(results_list)
        df = pd.DataFrame(result)
        return df

    def prob_cond(self,expression1:str,expression2:str,videoId):
        # if expression1
        # prepared_words = prepare_text(expression1)
        # prepared_expression1 = " ".join(prepared_words)
        prepared_expression1=expression1
        #words_number = len(prepared_words)
        prepared_expression2 = " ".join(prepare_text(expression2))
        print("expre1 "+prepared_expression1)
        results_list, count = self._database_service.find_expression(prepared_expression1, videoId, 1)
        df = self.create_df(results_list)
        cnt=self._expression_occurence(df,prepared_expression1)
        print("reslist "+str(count))
        expression2_occurence=self._expression_occurence(df,prepared_expression2)
        print(expression2_occurence)
        print(cnt)
        return expression2_occurence/cnt
