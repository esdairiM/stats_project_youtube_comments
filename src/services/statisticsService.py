import logging
from math import ceil

import matplotlib.pyplot as plt
import pandas as pd

from src.datastore.databaseService import DatabaseService
from src.datastore.factory import DatabaseFactory
from src.services.textPrecessingService import popular_words, prepare_text_list, prepare_text, counte_words


class StatisticsService:
    def __init__(self, logger=None):
        self._logger = logger or logging.getLogger(__name__)
        self._database_service: DatabaseService = DatabaseFactory().build().get_database_service()

    def get_comments_count(self, videoId: str) -> int:
        """
        fetch comments count for a video from the database

        :param videoId:
        :return:
        """
        count = self._database_service.find_by_videoId(videoId)[1]
        return count

    def get_first_quarter(self, videoId: str, remove_zerolikes: bool = False) -> dict:
        """
        fetch the 1st quarter of the video comments based on like count

        :param videoId:
        :param remove_zerolikes: remove comments with zero likes from the 1st quarter
        :return: dict of the 1sr quarter and it's length
        """

        # if video id was given
        comments, count = self._database_service.find_by_videoId(videoId)
        if comments is None:
            res = {"first_qr": list(), "length": 0}
        else:
            # calculate the quarter of the comments
            quarter = ceil(count / 4)
            first_quarter = comments[:quarter]
            if remove_zerolikes:
                first_quarter = list(filter(lambda comment: comment["likes"] > 0, first_quarter))
                quarter = len(first_quarter)
            res = {"first_qr": first_quarter, "length": quarter}

        return res

    def get_most_popular_comment(self, videoId: str):
        try:
            return self._database_service.find_by_videoId(videoId)[0][0]
        except:
            return {
                'videoId': "",
                'created_at': None,
                'author': "",
                'comment': "",
                'original_comment': "",
                'lang': "",
                'likes': None
            }

    def get_words_by_frequency(self, videoId: str, comment_list: list = None, first: int = 10):
        comments = comment_list
        if comments is None:
            comments = self._database_service.find_by_videoId(videoId)[0]
        words = popular_words(comments, first)
        return dict(words)

    def barpolt_dict(self, data: dict):
        plt.bar(range(len(data)), data.values(), align='center')
        plt.xticks(range(len(data)), data.keys())
        plt.show()

    def expression_statistics(self, expression, videoId) -> dict:
        # preparing the expression
        prepared_expression, words_number = self._processe_expressions(expression)

        # searching in the database
        results_list, count = self._database_service.find_expression(prepared_expression, videoId, words_number)

        if results_list == None:
            res = {"frequency": 0, "mpc": 0}

        else:
            # count occurrences
            occurrence = self._expression_occurrence(results_list, prepared_expression, words_number)

            # calculate frequency
            frequency = self._calculate_total_frequency(occurrence, videoId)

            # calculate mentions per comment
            mentions_per_comment = self._calculate_mentions_per_comment(occurrence, len(results_list))

            res = {"frequency": frequency, "mpc": mentions_per_comment}

        return res

    def prob_cond(self, expression1: str, expression2: str, videoId: str) -> dict():
        # preparing expressions
        prepared_expression1, expression1_wc = self._processe_expressions(expression1)
        prepared_expression2, expression2_wc = self._processe_expressions(expression2)

        # query data base fore element containing expression 1
        results_list = self._database_service.find_expression(prepared_expression1, videoId, expression1_wc)[0]

        # if 1st expression doesn't exist in the data set the probability is 0
        if len(results_list) == 0:
            result = {
                "ex1_occurence": 0,
                "ex2_occurence": 0,
                "proba": 0
            }
        else:
            # count occurrences
            expression1_occurrence = self._expression_occurrence(results_list, prepared_expression1, expression1_wc)
            expression2_occurrence = self._expression_occurrence(results_list, prepared_expression2, expression2_wc)
            # calculating the probability
            print(expression1_occurrence)
            print(expression2_occurrence)
            conditional_probability = expression2_occurrence / expression1_occurrence
            result = {
                "ex1_occurence": expression1_occurrence,
                "ex2_occurence": expression2_occurrence,
                "proba": conditional_probability
            }

        return result

    def _processe_expressions(self, expression):
        # prepare expressions
        prepared_words = prepare_text(expression)
        words_number = len(prepared_words)
        prepared_expression = " ".join(prepared_words)
        return prepared_expression, words_number

    def _calculate_total_frequency(self, occurrence: int, videoId: str) -> float:
        comments_count = self._database_service.find_by_videoId(videoId)[1]
        return occurrence / comments_count

    def _calculate_mentions_per_comment(self, occurrence: int, comments_number: int) -> float:
        return occurrence / comments_number

    def _expression_occurrence(self, results_list: list, expression: str, words_number: int) -> int:
        if words_number > 1:
            # create the data frame
            df = self._create_df(results_list)
            # count occurrences_expression_occurrence
            occurrence = df.comments.str.count(expression).sum()
        else:
            occurrence = counte_words(results_list).get(expression)

        return occurrence

    def _create_df(self, results_list: list) -> pd.DataFrame:
        result = prepare_text_list(results_list)
        df = pd.DataFrame(result)
        return df

    def gender_percent(self, videoId):
        try:
            counter = self._database_service.find_video_data(videoId, collection='genderData')[0]
            totalcount = self.get_comments_count(videoId)
            fre = {}
            try:fre.update({'male': counter['male']})
            except KeyError:pass
            try:fre.update({'female': counter['female']})
            except KeyError:pass
            try:fre.update({'other': counter['other']})
            except KeyError:pass
            try:fre.update({ 'uknown': totalcount - counter['male'] - counter['female'] - counter['other']})
            except KeyError:pass
        except IndexError:
            fre = {
                'male': 0,
                'female': 0,
                'other': 0,
                'uknown': 0,
            }
        print(fre)
        return fre
