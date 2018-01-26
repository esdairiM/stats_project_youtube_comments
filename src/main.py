from pprint import pprint

from src.services import logger
from src.services.etl import ETLService
from time import time
from src.services.statisticsService import StatisticsService

if __name__ == "__main__":
    logger.init_logger()
    etl = ETLService()
    print("finished building ")
    videoId = '-UAvLhaF-Eg'
    # videoId="g4nyUkm0ILg"
    res=etl.extract_and_transform(videoId).load()
    print(res)
    # if True:
    #     statistics_service = StatisticsService()
    #     print("finished building ")
    #     t = time()
    #     count = statistics_service.get_comments_count(videoId)
    #     print("get_comments_count "+str(time() - t))
    #     print("number of comments is {}".format(count))
    #     t = time()
    #     res= statistics_service.get_first_quarter(videoId,remove_zerolikes=True)
    #     print("get_first_quarter "+str(time() - t))
    #     if res is not None:
    #         print(res["first_qr"])
    #         print(res["length"])
    #     t = time()
    #     most_popular=statistics_service.get_most_popular_comment(videoId)
    #     print("get_most_popular_comment "+str(time() - t))
    #     if most_popular is not None:
    #         pprint(most_popular["original_comment"])
    #     t=time()
    #     frequent_words=statistics_service.get_words_by_frequency(videoId)
    #     print("frequent_words "+str(time() - t))
    #     t = time()
    #     statistics_service.barpolt_dict(dict(frequent_words))
    #     print("plot "+str(time()-t))
    #     pprint(frequent_words)
    #     t = time()
    #     res = statistics_service.expression_statistics("love Bill Maher",videoId)
    #     print(time() - t)
    #     print(res)
    #
    #     prob = statistics_service.prob_cond("bill", "bill", videoId)
    #     print(prob)
