import queue
import threading
import logging

class Threading:
    def __init__(self, logger = None):
        self._logger = logger or logging.getLogger(__name__)

    def lunch(self,job1,job2,arg1,arg2):
        global processed_comments, json_comments, thread1
        processed_comments = list()
        json_comments = queue.LifoQueue()
        thread1 = threading.Thread(target=get_comments, args=(videoId,))
        thread2 = threading.Thread(target=process_comments, args=(videoId,))
        thread1.start()
        thread2.start()
        thread1.join()
        thread1.join()