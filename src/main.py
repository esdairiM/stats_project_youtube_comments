import pprint
import time
import queue
import threading

from src.datasource import factory as datasource
from src.datastore import factory as datastore

from src.services import extractot,logger


def get_comments(videoId):
    for res in youtube.get_all_comments(videoId):
        json_comments.put(res)


def process_comments(videoId):
    while thread1.isAlive():
        commentlist = extractot.get_comments(json_comments.get(), videoId)
        processed_comments.extend(commentlist)


if __name__ == "__main__":
    logger.init_logger()
    youtube = datasource.DataSourceFactory().get_api_connection()
    database = datastore.DatabaseFactory().get_database_connection()
    print("finished building ")
    videoId = '-UAvLhaF-Eg'

    global processed_comments, json_comments, thread1
    processed_comments = list()
    json_comments = queue.LifoQueue()

    t = time.time()
    thread1 = threading.Thread(target=get_comments, args=(videoId,))
    thread2 = threading.Thread(target=process_comments, args=(videoId,))
    thread1.start()
    thread2.start()
    thread1.join()
    thread1.join()
    print(time.time() - t)
    pprint.pprint(len(processed_comments))
