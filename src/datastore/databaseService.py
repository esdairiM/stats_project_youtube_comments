from src.datastore.database import Database
import logging



class DatabaseService:
    def __init__(self,database_connection:Database,collection_name,logger=None):
        self._logger = logger or logging.getLogger(__name__)
        self._database=database_connection
        self._collection_name=collection_name
        self._last_videoId=None
        self._last_find_result=None
        self._last_find_count=0
        self._last_kvargs=None

    def load_data(self,comments):
        self._logger.info('starting to load data')
        try:
            #if comments not empty
            if comments:
                #try to create collection and index, pass if already exist
                self.verify_collection_existence()
                #insert data
                self._database.insert(self._collection_name,comments)
                self._logger.info('finished loading data')
                return True
            else:
                #comments list is empty
                return False
        except Exception as e:
            # Error occurred while inserting comments
            self._logger.warning(str(e))
            return False

    def verify_collection_existence(self):
        try:
            self._database.create_store(self._collection_name)
        except:
            pass
        try:
            self._database.create_text_index(self._collection_name, "text")
        except:
            pass

    def find_by_videoId(self,videoId,only_comments=False,cash=True,kvargs={"comment":1,"author":1,"lang":1,"likes":1,"_id":0}):
        """

        :param videoId:
        :param sort:
        :param cash:
        :return:
        """

        # if videoid is the same as last one return last result
        if cash and videoId==self._last_videoId and self._last_kvargs==kvargs:
            if only_comments:
                return self._last_find_result
            return self._last_find_result,self._last_find_count
        elif videoId is not None and videoId!= "":
            cursor=list(self._database.find_by_video_id(self._collection_name,videoId,kvargs=kvargs))
            count=len(cursor)
            # optimize research by saving the last search result if cash is true
            if cash:
                self._last_find_result=cursor
                self._last_videoId=videoId
                self._last_find_count=count
                self._last_kvargs= kvargs
            if only_comments:
                return cursor
            return cursor,count
        else:
            return None,None
