from time import time
from src.services import logger
from src.services.etl import ETLService
from src.services.statisticsService import StatisticsService
from pprint import pprint
from src.datastore.factory import DatabaseFactory


if __name__ == "__main__":
    logger.init_logger()
    #etl = ETLService()
    print("finished building ")
    videoId = '-UAvLhaF-Eg'
    res = True
    #res,msg=etl.extract_and_transform(videoId).load()
    #print(msg)
    if res:
        statistics_service = StatisticsService()
        # print("finished building ")
        # count = statistics_service.get_comments_count(videoId)
        # print("number of comments is {}".format(count))
        # quarter,quarter_count,with_likes_count= statistics_service.get_first_quarter(videoId,remove_zerolikes=True)
        # if quarter is not None:
        #     print(quarter_count)
        #     print(with_likes_count)
        # most_popular=statistics_service.get_most_popular_comment(videoId)
        # if most_popular is not None:
        #     pprint(most_popular)
        # t=time()
        # frequent_words=statistics_service.get_words_by_frequency(videoId)
        # print(statistics_service.plot_dict(dict(frequent_words)))
        # print(time()-t)
        # pprint(frequent_words)

        res =statistics_service.expression_statistics("something",videoId)
        print(res)